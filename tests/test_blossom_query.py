import asyncio
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi import Request, UploadFile

from app import blossom_query, main


class BlossomQueryTests(unittest.TestCase):
    def test_url_validation(self):
        self.assertEqual(blossom_query.normalize_server(" https://example.org/ "), "https://example.org")
        for value in ("http://example.org", "https://user:password@example.org", "https://example.org:8080", "https://example.org?q=1", "https://example.org/#fragment"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                blossom_query.normalize_server(value)

    def test_private_addresses_are_rejected_before_connection(self):
        for address in ("127.0.0.1", "10.0.0.1", "169.254.169.254", "::1"):
            with patch.object(blossom_query.socket, "getaddrinfo", return_value=[(None, None, None, None, (address, 443))]), patch.object(blossom_query.http.client, "HTTPSConnection") as connection:
                with self.assertRaises(ValueError):
                    blossom_query.fetch_verified("a" * 64, "https://example.org", timeout=1, max_bytes=100)
                connection.assert_not_called()

    def test_verified_fetch_rejects_mismatch_oversize_and_redirects(self):
        digest = hashlib.sha256(b"record").hexdigest()
        with patch.object(blossom_query.socket, "getaddrinfo", return_value=[(None, None, None, None, ("8.8.8.8", 443))]), patch.object(blossom_query.http.client, "HTTPSConnection") as factory:
            connection = factory.return_value
            response = connection.getresponse.return_value
            response.status = 200
            response.read.return_value = b"record"
            response.getheader.return_value = "text/plain"
            self.assertEqual(blossom_query.fetch_verified(digest, "https://example.org", timeout=1, max_bytes=100), (b"record", "text/plain"))
            with patch.object(blossom_query.socket, "create_connection") as connect:
                connection._create_connection(("example.org", 443))
                connect.assert_called_once_with(("8.8.8.8", 443), timeout=1)
            for status, content, limit in ((200, b"wrong", 100), (200, b"record", 2), (302, b"record", 100)):
                response.status, response.read.return_value = status, content
                with self.assertRaises(ValueError):
                    blossom_query.fetch_verified(digest, "https://example.org", timeout=1, max_bytes=limit)

    def test_query_uses_selected_server_and_cached_verified_preview(self):
        content = b"%PDF-1.7\nexample"
        request = Request({"type": "http", "method": "POST", "path": "/", "headers": [], "session": {}})
        identity = {"pubkey_hex": None}
        with tempfile.TemporaryDirectory() as directory, patch.object(main, "MEDIA_PREVIEW_DIR", Path(directory)), patch.object(main, "validate_relays", AsyncMock(return_value="wss://example.org")), patch.object(main, "build_query_etr_result", AsyncMock(return_value={})), patch.object(main, "enrich_query_controller_profile_for_identity", AsyncMock()), patch.object(main, "get_available_profiles", AsyncMock(return_value=[])), patch.object(main, "qr_context_for_digest", return_value={}), patch.object(main.templates, "TemplateResponse", side_effect=lambda request, name, context: context), patch.object(main, "fetch_verified", return_value=(content, "application/pdf")) as fetch:
            for server in ("https://other.example.org", ""):
                result = asyncio.run(main.query_etr_from_upload(request, file=UploadFile(filename="record.pdf", file=io.BytesIO(content)), relays="wss://example.org", identity=identity, blossom_server=server))
                self.assertEqual(fetch.call_args.args[1], server or main.BLOSSOM_SERVER)
                preview = result["media_preview"]
                self.assertTrue(preview["url"].startswith("/api/upload-preview/"))
                token = preview["url"].rsplit("/", 1)[1]
                self.assertEqual(main.media_preview_path(token, "application/pdf").read_bytes(), content)
            fetch.side_effect = TimeoutError()
            result = asyncio.run(main.query_etr_from_upload(request, file=UploadFile(filename="record.pdf", file=io.BytesIO(content)), relays="wss://example.org", identity=identity, blossom_server="https://other.example.org"))
            self.assertIsNone(result["media_preview"])
            self.assertIn("could not be retrieved", result["artifact_retrieval_message"])


if __name__ == "__main__":
    unittest.main()
