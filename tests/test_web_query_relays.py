import asyncio
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi import Request, UploadFile

from app import main


class QueryRelayTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {
            "OPENETR_QUERY_RELAYS": "records.example.org,backup.example.org",
            "OPENETR_QUERY_RELAYS_FILE": "",
            "OPENETR_HOME_RELAYS": "wss://home.example.org",
            "OPENETR_HOME_RELAYS_FILE": "",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.expected = "wss://records.example.org,wss://backup.example.org"

    def test_query_pool_is_independent_of_home_and_session(self):
        self.assertEqual(main.configured_query_relays({"default_relays": "wss://old.example.org"}), self.expected)
        self.assertEqual(main.configured_home_relays(), "wss://home.example.org")

    def test_unset_preserves_existing_defaults(self):
        os.environ["OPENETR_QUERY_RELAYS"] = ""
        self.assertEqual(main.configured_query_relays({"default_relays": "wss://session.example.org"}), "wss://session.example.org")
        self.assertEqual(main.configured_query_relays(), main.DEFAULT_RELAYS)

    def test_file_takes_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "query-relays"
            path.write_text("wss://file.example.org\n", encoding="utf-8")
            os.environ["OPENETR_QUERY_RELAYS_FILE"] = str(path)
            self.assertEqual(main.configured_query_relays(), "wss://file.example.org")

    def test_explicit_query_override_and_publication_unchanged(self):
        self.assertEqual(main.normalize_query_relays_form("", {}), self.expected)
        self.assertEqual(main.normalize_query_relays_form("custom.example.org", {}), "wss://custom.example.org")
        self.assertEqual(main.normalize_relays_form("publish.example.org"), "wss://publish.example.org")

    def test_query_routes_use_configured_pool(self):
        # Stop at the query service boundary: no relay, Blossom, or identity traffic.
        class QueryReached(Exception):
            pass

        identity = {"logged_in": False, "pubkey_hex": None, "default_relays": "wss://old.example.org"}
        request = Request({"type": "http", "method": "GET", "path": "/", "headers": [], "session": {}})
        query = AsyncMock(side_effect=QueryReached)
        validate = AsyncMock(side_effect=lambda relays, **kwargs: relays)
        with patch.object(main, "build_query_etr_result", query), patch.object(main, "validate_relays", validate):
            with self.assertRaises(QueryReached):
                asyncio.run(main.public_etr_lookup(request, "a" * 64, qr_encoding=None, identity=identity))
            self.assertEqual(query.call_args.kwargs["relays"], self.expected)
            for route in ("/api/query-etr-from-upload", "/warehouse-receipts/query", "/digital-product-passports/query"):
                registered = next(item for item in main.app.routes if item.path == route)
                dependency = next(item for item in registered.dependant.dependencies if item.name == "relays")
                self.assertIs(dependency.call, main.normalize_query_relays_form)
                for submitted, expected in (({}, self.expected), ({"relays": "wss://override.example.org"}, "wss://override.example.org")):
                    with self.subTest(route=route, submitted=submitted):
                        with self.assertRaises(QueryReached):
                            asyncio.run(registered.endpoint(
                                request,
                                file=UploadFile(filename="record.txt", file=io.BytesIO(b"record")),
                                relays=dependency.call(submitted.get("relays", ""), identity),
                                identity=identity,
                            ))
                        self.assertEqual(query.call_args.kwargs["relays"], expected)


if __name__ == "__main__":
    unittest.main()
