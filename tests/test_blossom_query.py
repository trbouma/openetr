import asyncio
from contextlib import ExitStack
import hashlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException, Request, UploadFile
from stroma import BlossomError, BlossomOutcome, BlossomPool, BlossomRetrievalResult, BlossomStoreResult, Event, Keys

from app import blossom_query, main
from openetr.services.issue_etr import build_issue_event_tags
from openetr.services.query_etr import event_to_view
from datetime import datetime, timezone


CONTENT = b"%PDF-1.7\nexample"
DIGEST = hashlib.sha256(CONTENT).hexdigest()
SERVERS = ("https://one.example.org", "https://two.example.org")
KEYS = Keys(priv_k="0" * 63 + "1")


def anchor(tags=None, digest=DIGEST):
    event = Event(kind=1415, pub_key=KEYS.public_key_hex(),
                  tags=[["o", digest], ["action", "issue"], *(tags or [])])
    event.sign(KEYS.private_key_hex())
    return event


def context(*events):
    return {"origin_events": [{"event": {"raw_event": event}} for event in events]}


class BlossomQueryTests(unittest.TestCase):
    def test_anchor_hint_display_normalizes_links_and_handles_old_anchors(self):
        event = anchor([
            ["blossom", SERVERS[0] + "/"], ["blossom", SERVERS[0]],
            ["blossom", SERVERS[1]], ["blossom", "javascript:alert(1)"],
            ["blossom", "https://127.0.0.1"], ["blossom", "https://example.org/path"],
        ])
        view = event_to_view(event)
        self.assertEqual(view["blossom_servers"], list(SERVERS))
        template = main.templates.env.get_template("_anchor_blossom_hints.html")
        rendered = template.render(anchor_event=view)
        for server in SERVERS:
            self.assertEqual(rendered.count(f'href="{server}"'), 1)
        self.assertNotIn("javascript:", rendered)
        self.assertNotIn("127.0.0.1", rendered)
        self.assertIn("current availability is not guaranteed", rendered)
        rendered = template.render(anchor_event=event_to_view(anchor()))
        self.assertIn("No Blossom hints advertised.", rendered)

    def test_configuration_plural_precedence_and_legacy_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(main.configured_blossom_servers(), (main.BLOSSOM_DEFAULT_SERVER,))
            os.environ["OPENETR_BLOSSOM_SERVER"] = SERVERS[0]
            self.assertEqual(main.configured_blossom_servers(), SERVERS[:1])
            os.environ["OPENETR_BLOSSOM_SERVERS"] = f"{SERVERS[1]}/, {SERVERS[0]} {SERVERS[1]}"
            self.assertEqual(main.configured_blossom_servers(), (SERVERS[1], SERVERS[0]))

    def test_query_configuration_is_independent_with_fallback_and_file_precedence(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ["OPENETR_BLOSSOM_SERVERS"] = SERVERS[0]
            self.assertEqual(main.configured_blossom_query_servers(), SERVERS[:1])
            os.environ["OPENETR_BLOSSOM_QUERY_SERVERS"] = ""
            self.assertEqual(main.configured_blossom_query_servers(), SERVERS[:1])
            os.environ["OPENETR_BLOSSOM_QUERY_SERVERS"] = f"{SERVERS[1]}/, {SERVERS[1]}"
            self.assertEqual(main.configured_blossom_query_servers(), SERVERS[1:])
            self.assertEqual(main.configured_blossom_servers(), SERVERS[:1])
            os.environ["OPENETR_BLOSSOM_QUERY_SERVERS_FILE"] = "/test/query-servers"
            with patch.object(Path, "read_text", return_value=SERVERS[0]):
                self.assertEqual(main.configured_blossom_query_servers(), SERVERS[:1])
            with patch.object(Path, "read_text", return_value="https://127.0.0.1"):
                with self.assertRaises(ValueError):
                    main.configured_blossom_query_servers()

    def test_public_https_origin_validation(self):
        for value in ("http://example.org", "https://user:secret@example.org",
                      "https://example.org/path", "https://example.org?q=1",
                      "https://127.0.0.1", "https://[::1]", "https://10.0.0.1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                BlossomPool([value])
        self.assertEqual(BlossomPool(["https://EXAMPLE.org:443/"]).servers, ("https://example.org",))

    def test_hints_require_valid_matching_anchor_and_skip_bad_optional_tags(self):
        valid = anchor([["blossom", SERVERS[0] + "/"], ["blossom", SERVERS[0]],
                        ["blossom", "http://example.org"], ["blossom"],
                        ["blossom", "https://127.0.0.1"]])
        tampered = anchor([["blossom", SERVERS[1]]])
        tampered.content = "changed"
        wrong_digest = anchor([["blossom", SERVERS[1]]], digest="a" * 64)
        self.assertEqual(blossom_query.anchor_blossom_hints(context(valid, tampered, wrong_digest), DIGEST), [SERVERS[0]])
        self.assertEqual(blossom_query.anchor_blossom_hints(context(anchor()), DIGEST), [])

    def test_retrieval_combines_configured_selected_and_verified_hints(self):
        result = BlossomRetrievalResult(DIGEST, CONTENT, SERVERS[1], "application/pdf")
        event = anchor([["blossom", SERVERS[1]]])
        seen = []

        async def retrieve(pool, digest):
            seen.append(pool.servers)
            return result

        with patch.object(main, "BLOSSOM_QUERY_SERVERS", SERVERS[:1]), patch.object(main, "BLOSSOM_SERVERS", SERVERS), patch.object(BlossomPool, "retrieve", retrieve):
            self.assertEqual(asyncio.run(main.blossom_fetch_bytes(DIGEST, query_context=context(event))), (CONTENT, "application/pdf"))
            self.assertEqual(seen[-1], (SERVERS[1], SERVERS[0]))
            asyncio.run(main.blossom_fetch_bytes(DIGEST))
            self.assertEqual(seen[-1], SERVERS)
            asyncio.run(main.blossom_fetch_bytes(DIGEST, SERVERS[0].upper() + "/", query_context=context(event)))
            self.assertEqual(seen[-1], (SERVERS[1], SERVERS[0]))
            asyncio.run(main.blossom_fetch_bytes(DIGEST, "https://selected.example.org", query_context=context(event)))
            self.assertEqual(seen[-1], (SERVERS[1], "https://selected.example.org", SERVERS[0]))
            with self.assertRaises(ValueError):
                asyncio.run(main.blossom_fetch_bytes(DIGEST, "https://127.0.0.1"))

    def test_combined_retrieval_preserves_all_bounded_candidates(self):
        query_servers = tuple(f"https://query-{i}.example.org" for i in range(32))
        upload_servers = tuple(f"https://upload-{i}.example.org" for i in range(32))
        hints = [f"https://hint-{i}.example.org" for i in range(32)]
        event = anchor([["blossom", server] for server in hints])
        seen = []

        async def retrieve(pool, digest):
            seen.extend(pool.servers)
            return BlossomRetrievalResult(digest, CONTENT, upload_servers[-1], "application/pdf")

        with patch.object(main, "BLOSSOM_QUERY_SERVERS", query_servers), patch.object(main, "BLOSSOM_SERVERS", upload_servers), patch.object(BlossomPool, "retrieve", retrieve):
            asyncio.run(main.blossom_fetch_bytes(DIGEST, "https://selected.example.org", query_context=context(event)))
        self.assertEqual(seen, [*hints, "https://selected.example.org", *query_servers, *upload_servers])

    def test_upload_and_retrieval_use_distinct_pools(self):
        seen = {}

        async def retrieve(pool, digest, *, hints=()):
            seen["query"] = pool.servers
            return BlossomRetrievalResult(digest, CONTENT, SERVERS[1], "application/pdf")

        async def store(pool, content, **kwargs):
            seen["upload"] = pool.servers
            return BlossomStoreResult(DIGEST, "any", 1, (BlossomOutcome(SERVERS[0], "confirmed"),))

        upload = main.UploadedFileInfo("record.pdf", len(CONTENT), DIGEST, None, CONTENT, "application/pdf")
        with patch.object(main, "BLOSSOM_SERVERS", SERVERS[:1]), patch.object(main, "BLOSSOM_QUERY_SERVERS", SERVERS[1:]), patch.object(BlossomPool, "retrieve", retrieve), patch.object(BlossomPool, "store", store):
            asyncio.run(main.blossom_fetch_bytes(DIGEST))
            asyncio.run(main.maybe_store_on_blossom(upload, True, signer_nsec=KEYS.private_key_bech32()))
        self.assertEqual(seen, {"query": (SERVERS[1], SERVERS[0]), "upload": SERVERS[:1]})

    def test_storage_thresholds_and_confirmed_tags(self):
        upload = main.UploadedFileInfo("record.pdf", len(CONTENT), DIGEST, None, CONTENT, "application/pdf")
        for require, required in (("any", 1), ("half", 1), ("majority", 2), ("all", 2)):
            outcome = BlossomStoreResult(DIGEST, require, required, (
                BlossomOutcome(SERVERS[0], "confirmed"),
                BlossomOutcome(SERVERS[1], "unconfirmed", "Timeout"),
            ))
            with self.subTest(require=require), patch.object(main, "BLOSSOM_REQUIRE", require), patch.object(BlossomPool, "store", AsyncMock(return_value=outcome)) as store:
                result = asyncio.run(main.maybe_store_on_blossom(upload, True, signer_nsec=KEYS.private_key_bech32()))
                self.assertEqual(result["stored"], required == 1)
                self.assertEqual(result["confirmed_servers"], [SERVERS[0]])
                self.assertEqual(store.call_args.kwargs["require"], require)
                tags = build_issue_event_tags(DIGEST, "record.pdf", len(CONTENT), datetime.now(timezone.utc), main.blossom_storage_tags(result))
                self.assertIn(["blossom", SERVERS[0]], tags)
                self.assertNotIn(["blossom", SERVERS[1]], tags)
        with patch.object(BlossomPool, "store", AsyncMock()) as store:
            self.assertIsNone(asyncio.run(main.maybe_store_on_blossom(upload, False, signer_nsec=None)))
            store.assert_not_called()
        with patch.object(BlossomPool, "store", AsyncMock(side_effect=BlossomError("Deadline exceeded"))):
            self.assertFalse(asyncio.run(main.maybe_store_on_blossom(upload, True, signer_nsec=KEYS.private_key_bech32()))["stored"])

    def test_query_uses_selected_server_and_cached_verified_preview(self):
        request = Request({"type": "http", "method": "POST", "path": "/", "headers": [], "session": {}})
        identity = {"pubkey_hex": None}
        with tempfile.TemporaryDirectory() as directory, patch.object(main, "MEDIA_PREVIEW_DIR", Path(directory)), patch.object(main, "validate_relays", AsyncMock(return_value="wss://example.org")), patch.object(main, "build_query_etr_result", AsyncMock(return_value={})), patch.object(main, "enrich_query_controller_profile_for_identity", AsyncMock()), patch.object(main, "get_available_profiles", AsyncMock(return_value=[])), patch.object(main, "qr_context_for_digest", return_value={}), patch.object(main.templates, "TemplateResponse", side_effect=lambda request, name, context: context), patch.object(main, "blossom_fetch_bytes", AsyncMock(return_value=(CONTENT, "application/pdf"))) as fetch:
            for server in (SERVERS[1], ""):
                result = asyncio.run(main.query_etr_from_upload(request, file=UploadFile(filename="record.pdf", file=io.BytesIO(CONTENT)), relays="wss://example.org", identity=identity, blossom_server=server))
                self.assertEqual(fetch.call_args.args[1], server or main.BLOSSOM_QUERY_SERVERS[0])
                preview = result["media_preview"]
                self.assertTrue(preview["url"].startswith("/api/upload-preview/"))
                token = preview["url"].rsplit("/", 1)[1]
                self.assertEqual(main.media_preview_path(token, "application/pdf").read_bytes(), CONTENT)
            fetch.side_effect = BlossomError("Unavailable")
            result = asyncio.run(main.query_etr_from_upload(request, file=UploadFile(filename="record.pdf", file=io.BytesIO(CONTENT)), relays="wss://example.org", identity=identity, blossom_server=SERVERS[1]))
            self.assertIsNone(result["media_preview"])
            self.assertIn("could not be retrieved", result["artifact_retrieval_message"])

    def test_public_preview_uses_verified_cached_bytes(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(main, "MEDIA_PREVIEW_DIR", Path(directory)), patch.object(main, "blossom_fetch_bytes", AsyncMock(return_value=(CONTENT, "application/pdf"))) as fetch:
            query = context(anchor())
            preview = asyncio.run(main.blossom_media_preview_for_digest(DIGEST, query))
            fetch.assert_awaited_once_with(DIGEST, query_context=query)
            self.assertTrue(preview["url"].startswith("/api/upload-preview/"))

    def test_all_upload_routes_stop_on_failure_and_include_confirmed_tags(self):
        class Published(Exception):
            pass

        request = Request({"type": "http", "method": "POST", "path": "/", "headers": [], "query_string": b"", "session": {}})
        identity = {"logged_in": True, "profile": "issuer", "nsec": KEYS.private_key_bech32(), "pubkey_hex": KEYS.public_key_hex()}
        upload = main.UploadedFileInfo("record.pdf", len(CONTENT), DIGEST, None, CONTENT, "application/pdf")
        routes = [
            (main.issue_etr_from_upload, dict(comment="", file_digest="", file_name="", file_size=0)),
            (main.warehouse_receipts_issue, dict(receipt_reference="", goods_description="", force=None)),
            (main.digital_product_passports_create, dict(product_name="", product_id="", manufacturer="", batch_or_lot="", description="", force="false")),
        ]
        for route, arguments in routes:
            for stored in (False, True):
                with self.subTest(route=route.__name__, stored=stored), ExitStack() as stack:
                    for name, value in {
                        "validate_relays": "wss://example.org",
                        "hash_uploaded_file": upload, "read_uploaded_receipt": upload,
                        "read_uploaded_product_passport": upload,
                        "evaluate_issue_etr_guard": {"should_warn": False},
                        "get_default_template_context": {},
                        "render_warehouse_receipts_page": "failed",
                        "render_digital_product_passports_page": "failed",
                        "maybe_store_on_blossom": {"stored": stored, "message": "Storage result", "confirmed_servers": [SERVERS[0]]},
                    }.items():
                        stack.enter_context(patch.object(main, name, AsyncMock(return_value=value)))
                    publish = stack.enter_context(patch.object(main, "publish_issue_etr", AsyncMock(side_effect=Published)))
                    stack.enter_context(patch.object(main.templates, "TemplateResponse", return_value="failed"))
                    call = route(request, file=UploadFile(filename="record.pdf", file=io.BytesIO(CONTENT)), relays="wss://example.org", identity=identity, store_upload="true", **arguments)
                    if stored:
                        with self.assertRaises(Published):
                            asyncio.run(call)
                        self.assertIn(["blossom", SERVERS[0]], publish.call_args.kwargs["extra_tags"])
                    else:
                        self.assertEqual(asyncio.run(call), "failed")
                        publish.assert_not_called()

    def test_confirmation_requires_storage_bytes(self):
        request = Request({"type": "http", "method": "POST", "path": "/", "headers": [], "query_string": b"confirm=true", "session": {}})
        identity = {"logged_in": True, "profile": "issuer"}
        with patch.object(main, "validate_relays", AsyncMock(return_value="wss://example.org")), patch.object(main, "publish_issue_etr", AsyncMock()) as publish:
            with self.assertRaises(HTTPException) as error:
                asyncio.run(main.issue_etr_from_upload(request, file=None, relays="wss://example.org", comment="", file_digest=DIGEST, file_name="record.pdf", file_size=len(CONTENT), store_upload="true", identity=identity))
            self.assertEqual(error.exception.status_code, 400)
            publish.assert_not_called()


if __name__ == "__main__":
    unittest.main()
