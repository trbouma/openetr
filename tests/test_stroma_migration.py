"""Offline migration checks, including local WebSocket relays and legacy wire data."""

import asyncio
import json
import unittest
from datetime import datetime
from unittest.mock import patch

import click
from aiohttp import web
from stroma import Event, Keys, NIP44Encrypt, RelayError, RelayPool

from openetr import config
from openetr.commands.output import to_jsonable
from openetr.helpers import resolve_keys
from openetr.relay import publish_event, query_events
from openetr.services.control_events import publish_event_and_verify, publish_transfer_initiate_event, publish_transfer_accept_event
from openetr.services.issue_etr import publish_issue_etr
from openetr.services.profile_publish import publish_profile_content
from openetr.services.query_etr import build_query_etr_result, format_event_date_compact


# Public, deliberately insecure fixture key (scalar 1), never a user credential.
FIXTURE_KEY = "0" * 63 + "1"
LEGACY_CIPHERTEXT = "AroU8JdHQJxfswN9yg0myHu3EpFloQYzxJRoKecnU7ANuq/zCVxdDFCEWwYKn0HT70OdAKj8Qj4U85zlIA0SYea1B56+vDuVmV/mh0ZhGxTvk8kKBiwRrzEd3vO+0DXXXqdHqel5QN/k8XKufhPU747cC0eMF3yulxh8QrBHwzzakQEznPetbxpQMqvylHWP4XCqL0r9nZyiYXkft00mXts+jYWiLoV5TgxSfnBRJdHVdhl1wnM2llssw5KP+KqLBhAapHFU/fmj+oPj5poHYIJyOxzKDSA/W9+H529+95a3QHFnz2bmFYy1jNkmgwo++P4TMZ7/xQjgO8Ikn448YMrh0Zq6ryK6UxQ917E/Qbbc3ULCHVGVRGsL73cM9duMxTCR"


class WireCompatibilityTests(unittest.TestCase):
    def test_legacy_event_id_signature_and_tags(self):
        keys = Keys(priv_k=FIXTURE_KEY)
        event = Event(
            kind=1415, pub_key=keys.public_key_hex(), created_at=1700000000,
            content="Synthetic migration fixture", tags=[["o", "a" * 64], ["action", "issue"]],
            id="d475bcb588afd859a31c3bae7411142cc9ae52cc302eebe470746e6168f163fd",
            sig="387df9f7f611e41e35feb31667b0bcc7136884797bc19fd5b17a3453c33a6b0b915809d612f1be8adfccfd4c0f4ffe23acb002ef7ea4415bd87c1be391ae4f35",
        )
        self.assertTrue(event.is_valid())
        self.assertEqual(event.id, event.calculate_id())
        self.assertEqual(json.loads(json.dumps(to_jsonable(event.tags))), [["o", "a" * 64], ["action", "issue"]])
        self.assertEqual(to_jsonable(event)["created_at"], 1700000000)
        self.assertEqual(format_event_date_compact(event.created_at), "20231114")
        event.content = "tampered"
        self.assertFalse(event.is_valid())

    def test_legacy_encrypted_profile_secret(self):
        keys = Keys(priv_k=FIXTURE_KEY)
        record = config.ProfileSecretRecord.model_validate_json(NIP44Encrypt(keys).decrypt(LEGACY_CIPHERTEXT, keys.public_key_hex()))
        self.assertEqual(record.as_user, keys.private_key_bech32())
        self.assertEqual(record.npub, keys.public_key_bech32())
        self.assertEqual(record.profile, "warehouse")

    def test_invalid_nsec_has_cli_error(self):
        with self.assertRaises(click.ClickException):
            resolve_keys("nsec1invalid")


class StromaRelayTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.events = {}
        self.keys = Keys(priv_k=FIXTURE_KEY)
        app = web.Application()
        app.router.add_get("/{mode}", self.relay)
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, "127.0.0.1", 0)
        await self.site.start()
        port = self.site._server.sockets[0].getsockname()[1]
        self.url = f"ws://127.0.0.1:{port}/ok"
        self.reject = f"ws://127.0.0.1:{port}/reject"
        self.silent = f"ws://127.0.0.1:{port}/silent"

    async def asyncTearDown(self):
        await self.runner.cleanup()

    async def relay(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for message in ws:
            data = json.loads(message.data)
            if request.match_info["mode"] == "silent":
                continue
            if data[0] == "EVENT":
                event = Event.load(data[1], validate=True)
                accepted = event is not None and request.match_info["mode"] != "reject"
                if accepted:
                    self.events[event.id] = event
                await ws.send_json(["OK", data[1]["id"], accepted, "stored" if accepted else "blocked"])
            elif data[0] == "REQ":
                for event in self.events.values():
                    for filters in data[2:]:
                        if "ids" in filters and event.id not in filters["ids"]:
                            continue
                        if "authors" in filters and event.pub_key not in filters["authors"]:
                            continue
                        if "kinds" in filters and event.kind not in filters["kinds"]:
                            continue
                        if any(not set(values).intersection(event.tags.get_tags_value(key[1:])) for key, values in filters.items() if key.startswith("#")):
                            continue
                        await ws.send_json(["EVENT", data[1], event.data()])
                await ws.send_json(["EOSE", data[1]])
            elif data[0] == "CLOSE":
                await ws.close()
        return ws

    def event(self, kind=1415):
        event = Event(kind=kind, tags=[["o", "a" * 64], ["action", "issue"]])
        event.sign(self.keys)
        return event

    async def test_pool_publish_acknowledgement_and_query_deduplication(self):
        event = self.event()
        pool = RelayPool([self.url, self.reject], timeout=1)
        results = await publish_event(pool, event)
        self.assertEqual([result.relay for result in results], [self.url])
        events = await query_events(pool, {"#o": ["a" * 64]})
        self.assertEqual([found.id for found in events], [event.id])
        with self.assertRaisesRegex(RelayError, "not confirmed"):
            await publish_event(RelayPool([self.reject], timeout=1), event)

    async def test_unresponsive_relay_is_bounded(self):
        with self.assertRaisesRegex(RelayError, "timed out"):
            await query_events(RelayPool([self.silent], timeout=.05), {})
        with self.assertRaisesRegex(RelayError, "not confirmed"):
            await publish_event(RelayPool([self.silent], timeout=.05), self.event())

    async def test_invalid_signature_is_not_returned_as_evidence(self):
        event = self.event()
        event.content = "tampered after signing"
        self.events[event.id] = event
        self.assertEqual(await query_events(RelayPool([self.url], timeout=1), {}), [])

    async def test_transfer_preserves_links_and_controller(self):
        anchor = self.event()
        await publish_event(RelayPool([self.url], timeout=1), anchor)
        recipient = Keys(priv_k="0" * 63 + "2")
        initiate = await publish_transfer_initiate_event(
            relays=self.url, object_digest=None, prior_event_id=anchor.id,
            signer_nsec=self.keys.private_key_bech32(), transferee_pubkey_hex=recipient.public_key_hex(),
            publish_wait=0, query_timeout=1,
        )
        accepted = await publish_transfer_accept_event(
            relays=self.url, initiate_event_id=initiate["event_id"],
            signer_nsec=recipient.private_key_bech32(), publish_wait=0, query_timeout=1,
        )
        self.assertEqual(self.events[accepted["event_id"]].tags.get_tags_value("e"), [initiate["event_id"]])
        result = await build_query_etr_result("a" * 64, self.url, timeout=1)
        self.assertEqual(result["current_controller"]["npub"], recipient.public_key_bech32())

    async def test_issue_profile_control_and_query_services(self):
        result = await publish_issue_etr("receipt.pdf", 5, "a" * 64, self.url, self.keys.private_key_bech32(), None, publish_wait=0)
        self.assertTrue(result["ok_results"][0]["success"])
        self.assertEqual(result["query_count_after_publish"], 1)
        profile = await publish_profile_content(self.url, self.keys.private_key_bech32(), {"name": "Warehouse"}, publish_wait=0)
        self.assertTrue(profile["exact_match"])
        control = self.event(1416)
        control.tags = type(control.tags)([["o", "a" * 64], ["e", result["event_id"]], ["action", "attest"]])
        control.sign(self.keys)
        verification = await publish_event_and_verify(self.url, control, 0, 1)
        self.assertEqual(verification["verification"]["exact"], 1)
        query = await build_query_etr_result("a" * 64, self.url, timeout=1)
        self.assertFalse(query["no_events"])
        self.assertIsInstance(query["initial_event"]["created_at"], datetime)
        json.dumps(to_jsonable(query))

    async def test_relay_backed_records_roundtrip_and_delete(self):
        with patch.object(config, "_get_root_keys", return_value=self.keys), patch.object(config, "resolve_home_relays", return_value=[self.url]):
            index = config.ProfilesIndexRecord(active_profile="warehouse", profiles=["warehouse"])
            await config._async_store_profiles_index(index, {})
            self.assertEqual(await config._async_load_profiles_index({}), index)
            aliases = config.AliasIndexRecord(aliases={"warehouse": self.keys.public_key_bech32()})
            await config._async_store_aliases_index(aliases, {})
            self.assertEqual(await config._async_load_aliases_index({}), aliases)
            known = config.KnownEntitiesRecord(npubs=[self.keys.public_key_bech32()])
            await config._async_store_known_entities_index(known, {})
            self.assertEqual(await config._async_load_known_entities_index({}), known)
            await config._async_store_profile_record("warehouse", {"relays": self.url}, {})
            self.assertEqual((await config._async_load_profile_record("warehouse", {})).relays, self.url)
            await config._async_store_profile_secret("warehouse", self.keys.private_key_bech32(), {})
            self.assertEqual(await config._async_load_profile_secret("warehouse", {}), self.keys.private_key_bech32())
            self.assertTrue(await config._async_delete_profile_record("warehouse", {}))
            self.assertTrue(await config._async_delete_profile_secret("warehouse", {}))
            self.assertTrue(any(event.kind == 5 for event in self.events.values()))


if __name__ == "__main__":
    unittest.main()
