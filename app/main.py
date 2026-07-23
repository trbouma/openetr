import asyncio
import base64
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import io
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
import tempfile
import time
from typing import Any
import urllib.error
import urllib.request

import bech32
import click
from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from monstr.encrypt import Keys
from monstr.event.event import Event
from starlette.staticfiles import StaticFiles

from openetr.bitcoin import broadcast_blockstream_transaction, create_p2tr_send_result, create_p2tr_sweep_result, derive_bitcoin_wallet_material, derive_p2tr_balance_for_nostr_input, derive_recent_transactions_for_nostr_input, fetch_blockstream_wallet_balance_sats
from app.encrypted_session import EncryptedSessionMiddleware
from openetr.config import DEFAULT_LIMIT, DEFAULT_PROFILE_NAME, DEFAULT_QUERY_TIMEOUT, DEFAULT_RELAYS, _async_load_aliases_index, _async_load_profile_record, _async_load_profile_secret, _async_load_profiles_index, load_user_config, packaged_defaults, reset_runtime_bootstrap_overrides, set_runtime_bootstrap_overrides
from openetr.guards import evaluate_issue_etr_guard
from openetr.helpers import assert_hex_object_identifier, assert_hex_pubkey, format_object_identifier, format_pubkey, normalize_alias, normalize_object_identifier, normalize_relays, resolve_author, resolve_keys, validate_relays
from openetr.control import ACTION_DISCHARGE, ACTION_ENCUMBER, ACTION_REDEEM, ACTION_TERMINATE, CONTROL_EVENT_KIND
from openetr.services.control_events import ControlEventError, publish_auxiliary_control_event, publish_transfer_accept_event, publish_transfer_initiate_event
from openetr.services.issue_etr import publish_issue_etr
from openetr.services.profile_admin import create_relay_backed_profile, initialize_relay_backed_root
from openetr.services.profile_publish import PROFILE_FIELDS, publish_profile_updates
from openetr.services.query_etr import build_query_etr_result, compact_profile, fetch_profile, profile_picture_url
from openetr.silent_payments import create_silent_payment_sweep_result, derive_silent_payment_material, fetch_blockstream_tip_height, frigate_scan_subscribe, resolve_silent_payment_wallet_mode_material, silent_payment_address_belongs_to_nostr_key
from openetr.trivia import random_openetr_trivia_fact


APP_TITLE = "OpenETR Demo App"
CONTROL_TRANSFER_KIND = CONTROL_EVENT_KIND
NOBJ_PREFIX = "nobj"
SESSION_ROOT_NSEC_KEY = "openetr_root_nsec"
SESSION_SIGNER_NSEC_KEY = "openetr_signer_nsec"
SESSION_PROFILE_KEY = "openetr_profile"
SESSION_BOOTSTRAP_RELAYS_KEY = "openetr_bootstrap_relays"
SESSION_DEFAULT_RELAYS_KEY = "openetr_default_relays"
DEFAULT_MAX_UPLOAD_BYTES = 10 * 1024 * 1024
UPLOAD_READ_CHUNK_BYTES = 1024 * 1024
MEDIA_PREVIEW_TTL_SECONDS = 60 * 60
MEDIA_PREVIEW_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]{16,64}$")
MEDIA_PREVIEW_EXTENSIONS = {
    "application/pdf": ".pdf",
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
BLOSSOM_DEFAULT_SERVER = "https://blossom.getsafebox.app"
BLOSSOM_AUTH_KIND = 24242
BLOSSOM_AUTH_TTL_SECONDS = 5 * 60


def read_runtime_value(name: str, default: str | None = None) -> str | None:
    file_path = (os.environ.get(f"{name}_FILE") or "").strip()
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()

    value = os.environ.get(name)
    if value not in (None, ""):
        return value
    return default


SESSION_SECRET = read_runtime_value("OPENETR_APP_SESSION_SECRET", "openetr-demo-session-secret") or "openetr-demo-session-secret"
SITE_URL = read_runtime_value("OPENETR_SITE_URL", "https://trbouma.github.io/openetr/") or "https://trbouma.github.io/openetr/"
GIT_COMMIT = read_runtime_value("OPENETR_GIT_COMMIT", "unknown") or "unknown"
BLOCKSTREAM_API_BASE = read_runtime_value("OPENETR_BLOCKSTREAM_API_BASE", "https://blockstream.info/api") or "https://blockstream.info/api"
FRIGATE_HOST = read_runtime_value("OPENETR_FRIGATE_HOST", "frigate.2140.dev") or "frigate.2140.dev"
FRIGATE_SSL = (read_runtime_value("OPENETR_FRIGATE_SSL", "true") or "true").strip().lower() in {"1", "true", "yes", "on"}
FRIGATE_PORT = int(read_runtime_value("OPENETR_FRIGATE_PORT", "50002" if FRIGATE_SSL else "50001") or ("50002" if FRIGATE_SSL else "50001"))
FRIGATE_TIMEOUT = float(read_runtime_value("OPENETR_FRIGATE_TIMEOUT", "120") or "120")
MAX_UPLOAD_BYTES = int(read_runtime_value("OPENETR_MAX_UPLOAD_BYTES", str(DEFAULT_MAX_UPLOAD_BYTES)) or str(DEFAULT_MAX_UPLOAD_BYTES))
PUBLIC_BASE_URL = (read_runtime_value("OPENETR_PUBLIC_BASE_URL") or "").rstrip("/")
BLOSSOM_SERVER = (read_runtime_value("OPENETR_BLOSSOM_SERVER", BLOSSOM_DEFAULT_SERVER) or BLOSSOM_DEFAULT_SERVER).rstrip("/")
BLOSSOM_TIMEOUT_SECONDS = float(read_runtime_value("OPENETR_BLOSSOM_TIMEOUT_SECONDS", "20") or "20")
MEDIA_PREVIEW_DIR = Path(tempfile.gettempdir()) / "openetr-media-previews"
TEMPLATE_DIR = Path(__file__).parent / "templates"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
APP_ASSETS_DIR = Path(__file__).parent / "assets"
QR_LOGO_PATH = ASSETS_DIR / "images" / "openetr.png"

app = FastAPI(
    title=APP_TITLE,
    description="Demonstration FastAPI app kept separate from the installable openetr component.",
    version="0.1.0",
)
app.add_middleware(EncryptedSessionMiddleware, secret_key=SESSION_SECRET)
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")
if APP_ASSETS_DIR.exists():
    app.mount("/app-assets", StaticFiles(directory=str(APP_ASSETS_DIR)), name="app-assets")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def configured_home_relays() -> str:
    return normalize_relays(read_runtime_value("OPENETR_HOME_RELAYS", DEFAULT_RELAYS) or DEFAULT_RELAYS)


def bytes_to_nobj(data: bytes, prefix: str = NOBJ_PREFIX) -> str:
    digest = hashlib.sha256(data).hexdigest()
    return digest_to_nobj(digest, prefix)


def digest_to_nobj(digest: str, prefix: str = NOBJ_PREFIX) -> str:
    as_int = [int(digest[i:i + 2], 16) for i in range(0, len(digest), 2)]
    converted = bech32.convertbits(as_int, 8, 5)
    return bech32.bech32_encode(prefix, converted)


def upload_limit_label(max_bytes: int = MAX_UPLOAD_BYTES) -> str:
    mib = max_bytes / (1024 * 1024)
    if mib.is_integer():
        return f"{int(mib)} MiB"
    return f"{mib:.1f} MiB"


def forwarded_header_value(header_value: str, key: str) -> str | None:
    first_forwarded = header_value.split(",", 1)[0]
    for item in first_forwarded.split(";"):
        name, separator, value = item.strip().partition("=")
        if separator and name.lower() == key:
            return value.strip().strip('"')
    return None


def request_base_url(request: Request) -> str:
    forwarded = request.headers.get("forwarded", "")
    forwarded_proto = forwarded_header_value(forwarded, "proto") if forwarded else None
    forwarded_host = forwarded_header_value(forwarded, "host") if forwarded else None
    scheme = (
        forwarded_proto
        or request.headers.get("x-forwarded-proto", "").split(",", 1)[0].strip()
        or request.url.scheme
    )
    host = (
        forwarded_host
        or request.headers.get("x-forwarded-host", "").split(",", 1)[0].strip()
        or request.headers.get("host", "").strip()
        or request.url.netloc
    )
    if host:
        return f"{scheme}://{host}".rstrip("/")
    return str(request.base_url).rstrip("/")


def public_base_url(request: Request) -> str:
    return PUBLIC_BASE_URL or request_base_url(request)


def public_etr_url(request: Request, digest: str) -> str:
    return f"{public_base_url(request)}/etr/{digest}"


def qr_context_for_digest(request: Request, digest: str) -> dict[str, str]:
    return {
        "public_query_url": public_etr_url(request, digest),
        "public_query_qr_url": f"/etr/qr/{digest}",
    }


def branded_qr_image(qr_text: str, logo_path: Path = QR_LOGO_PATH):
    import qrcode
    from PIL import Image, ImageDraw

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    if not logo_path.exists():
        return image

    logo = Image.open(logo_path).convert("RGBA")
    logo_size = max(1, int(image.size[0] * 0.18))
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    logo.thumbnail((logo_size, logo_size), resampling)

    padding = max(6, int(logo_size * 0.18))
    badge_size = (logo.size[0] + padding * 2, logo.size[1] + padding * 2)
    badge = Image.new("RGBA", badge_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(badge)
    radius = max(8, int(badge_size[0] * 0.18))
    draw.rounded_rectangle((0, 0, badge_size[0] - 1, badge_size[1] - 1), radius=radius, fill="white")
    badge.alpha_composite(logo, (padding, padding))

    position = ((image.size[0] - badge.size[0]) // 2, (image.size[1] - badge.size[1]) // 2)
    image.alpha_composite(badge, position)
    return image.convert("RGB")


def remove_stale_media_previews(now: float | None = None) -> None:
    if not MEDIA_PREVIEW_DIR.exists():
        return
    current_time = now or time.time()
    for path in MEDIA_PREVIEW_DIR.iterdir():
        if not path.is_file():
            continue
        try:
            if current_time - path.stat().st_mtime > MEDIA_PREVIEW_TTL_SECONDS:
                path.unlink()
        except OSError:
            continue


def media_preview_path(token: str, media_type: str) -> Path:
    if not MEDIA_PREVIEW_TOKEN_PATTERN.fullmatch(token):
        raise HTTPException(status_code=404, detail="Media preview not found.")
    extension = MEDIA_PREVIEW_EXTENSIONS.get(media_type)
    if extension is None:
        raise HTTPException(status_code=404, detail="Media preview not found.")
    return MEDIA_PREVIEW_DIR / f"{token}{extension}"


def media_type_from_preview_path(path: Path) -> str | None:
    for media_type, extension in MEDIA_PREVIEW_EXTENSIONS.items():
        if path.suffix.lower() == extension:
            return media_type
    return None


def preview_media_type(filename: str, declared_type: str | None, first_chunk: bytes | None) -> str | None:
    normalized_declared_type = (declared_type or "").split(";")[0].strip().lower()
    if normalized_declared_type in {"", "application/octet-stream", "binary/octet-stream"}:
        normalized_declared_type = ""
    guessed_type = normalized_declared_type or (mimetypes.guess_type(filename)[0] or "").lower()
    first_bytes = first_chunk or b""

    if guessed_type == "application/pdf" and first_bytes.startswith(b"%PDF-"):
        return "application/pdf"
    if guessed_type in {"image/jpeg", "image/jpg"} and first_bytes.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if guessed_type == "image/png" and first_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if guessed_type == "image/gif" and (first_bytes.startswith(b"GIF87a") or first_bytes.startswith(b"GIF89a")):
        return "image/gif"
    if guessed_type == "image/webp" and len(first_bytes) >= 12 and first_bytes[:4] == b"RIFF" and first_bytes[8:12] == b"WEBP":
        return "image/webp"
    return None


@dataclass
class UploadedFileInfo:
    filename: str
    size_bytes: int
    digest: str
    media_preview: dict[str, str] | None
    content: bytes | None = None
    media_type: str | None = None


def parse_optional_checkbox(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def blossom_blob_url(digest: str, server: str = BLOSSOM_SERVER) -> str:
    return f"{server.rstrip('/')}/{digest}"


def blossom_upload_url(server: str = BLOSSOM_SERVER) -> str:
    return f"{server.rstrip('/')}/upload"


def blossom_upload_auth_header(*, signer_nsec: str, digest: str) -> str:
    keys = resolve_keys(signer_nsec)
    expires_at = int(time.time()) + BLOSSOM_AUTH_TTL_SECONDS
    event = Event(
        kind=BLOSSOM_AUTH_KIND,
        content="Authorize OpenETR document upload",
        pub_key=keys.public_key_hex(),
        tags=[
            ["t", "upload"],
            ["x", digest],
            ["expiration", str(expires_at)],
        ],
    )
    event.sign(keys.private_key_hex())
    token = base64.b64encode(
        json.dumps(event.data(), separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).decode("ascii")
    return f"Nostr {token}"


def blossom_head_exists(digest: str, server: str = BLOSSOM_SERVER) -> bool:
    request = urllib.request.Request(blossom_blob_url(digest, server), method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=BLOSSOM_TIMEOUT_SECONDS) as response:
            return 200 <= response.status < 300
    except urllib.error.HTTPError as exc:
        if exc.code in {404, 405}:
            return False
        raise


def blossom_fetch_bytes(digest: str, server: str = BLOSSOM_SERVER) -> tuple[bytes, str | None]:
    request = urllib.request.Request(blossom_blob_url(digest, server), method="GET")
    with urllib.request.urlopen(request, timeout=BLOSSOM_TIMEOUT_SECONDS) as response:
        if not 200 <= response.status < 300:
            raise RuntimeError(f"Blossom fetch failed with HTTP {response.status}")
        content = response.read(MAX_UPLOAD_BYTES + 1)
        if len(content) > MAX_UPLOAD_BYTES:
            raise RuntimeError(f"Blossom blob exceeds the {upload_limit_label()} preview limit")
        media_type = response.headers.get_content_type()
    if hashlib.sha256(content).hexdigest() != digest:
        raise RuntimeError("Blossom blob digest did not match the requested object digest")
    return content, media_type


async def blossom_media_preview_for_digest(digest: str) -> dict[str, str] | None:
    try:
        content, declared_type = await asyncio.to_thread(blossom_fetch_bytes, digest)
    except Exception:
        return None
    media_type = preview_media_type(f"OpenETR object {digest}", declared_type, content[:UPLOAD_READ_CHUNK_BYTES])
    if not media_type:
        return None
    return {
        "url": f"/etr/blob/{digest}",
        "filename": f"OpenETR object {format_object_identifier(digest)}",
        "media_type": media_type,
        "kind": "pdf" if media_type == "application/pdf" else "image",
        "source": "blossom",
    }


def blossom_upload_bytes(
    *,
    content: bytes,
    digest: str,
    media_type: str | None,
    filename: str,
    signer_nsec: str,
    server: str = BLOSSOM_SERVER,
) -> dict[str, Any]:
    if hashlib.sha256(content).hexdigest() != digest:
        raise ValueError("uploaded content digest does not match expected digest")

    headers = {
        "Authorization": blossom_upload_auth_header(signer_nsec=signer_nsec, digest=digest),
        "Content-Type": media_type or "application/octet-stream",
        "Content-Length": str(len(content)),
        "X-SHA-256": digest,
        "X-Content-SHA256": digest,
    }
    if filename:
        headers["X-Filename"] = filename

    if blossom_head_exists(digest, server):
        return {
            "stored": True,
            "already_present": True,
            "server": server,
            "url": blossom_blob_url(digest, server),
            "message": "Stored on Blossom.",
        }

    request = urllib.request.Request(
        blossom_upload_url(server),
        data=content,
        headers=headers,
        method="PUT",
    )
    with urllib.request.urlopen(request, timeout=BLOSSOM_TIMEOUT_SECONDS) as response:
        response_body = response.read()
        if not 200 <= response.status < 300:
            raise RuntimeError(f"Blossom upload failed with HTTP {response.status}")

    descriptor: dict[str, Any] = {}
    if response_body:
        try:
            parsed = json.loads(response_body.decode("utf-8"))
            if isinstance(parsed, dict):
                descriptor = parsed
        except (UnicodeDecodeError, json.JSONDecodeError):
            descriptor = {}

    if not blossom_head_exists(digest, server):
        raise RuntimeError("Blossom upload completed, but the blob was not retrievable by digest")

    return {
        "stored": True,
        "already_present": False,
        "server": server,
        "url": blossom_blob_url(digest, server),
        "descriptor": descriptor,
        "message": "Stored on Blossom.",
    }


async def maybe_store_on_blossom(
    upload: UploadedFileInfo,
    should_store: bool,
    *,
    signer_nsec: str | None,
) -> dict[str, Any] | None:
    if not should_store:
        return None
    if not signer_nsec:
        return {
            "stored": False,
            "server": BLOSSOM_SERVER,
            "message": "Blossom storage requires an issuing signer.",
        }
    if upload.content is None:
        return {
            "stored": False,
            "server": BLOSSOM_SERVER,
            "message": "Blossom storage was requested, but the uploaded bytes were not retained.",
        }
    try:
        return await asyncio.to_thread(
            blossom_upload_bytes,
            content=upload.content,
            digest=upload.digest,
            media_type=upload.media_type,
            filename=upload.filename,
            signer_nsec=signer_nsec,
        )
    except Exception as exc:
        return {
            "stored": False,
            "server": BLOSSOM_SERVER,
            "message": f"Blossom storage failed: {exc}",
        }


async def hash_uploaded_file(
    file: UploadFile,
    *,
    default_filename: str = "upload",
    max_bytes: int = MAX_UPLOAD_BYTES,
    retain_content: bool = False,
) -> UploadedFileInfo:
    filename = file.filename or default_filename
    size_bytes = 0
    file_hash = hashlib.sha256()
    first_chunk: bytes | None = None
    preview_file = None
    preview_path = None
    media_preview = None
    media_type = preview_media_type(filename, file.content_type, None)
    retained_chunks: list[bytes] = []

    try:
        while True:
            chunk = await file.read(UPLOAD_READ_CHUNK_BYTES)
            if not chunk:
                break

            if first_chunk is None:
                first_chunk = chunk
                media_type = preview_media_type(filename, file.content_type, first_chunk)
                if media_type:
                    remove_stale_media_previews()
                    MEDIA_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
                    token = secrets.token_urlsafe(24)
                    preview_path = media_preview_path(token, media_type)
                    preview_file = preview_path.open("wb")
                    media_preview = {
                        "url": f"/api/upload-preview/{token}",
                        "filename": filename,
                        "media_type": media_type,
                        "kind": "pdf" if media_type == "application/pdf" else "image",
                    }

            size_bytes += len(chunk)
            if size_bytes > max_bytes:
                raise HTTPException(
                    status_code=413,
                    detail=f"Uploaded file exceeds the {upload_limit_label(max_bytes)} limit.",
                )
            file_hash.update(chunk)
            if retain_content:
                retained_chunks.append(chunk)
            if preview_file is not None:
                preview_file.write(chunk)
    except Exception:
        if preview_file is not None:
            preview_file.close()
        if preview_path is not None:
            try:
                preview_path.unlink()
            except OSError:
                pass
        raise
    finally:
        if preview_file is not None:
            preview_file.close()

    return UploadedFileInfo(
        filename=filename,
        size_bytes=size_bytes,
        digest=file_hash.hexdigest(),
        media_preview=media_preview,
        content=b"".join(retained_chunks) if retain_content else None,
        media_type=media_type,
    )


def short_id(value: str | None, head: int = 12, tail: int = 8) -> str:
    if not value:
        return ""
    if len(value) <= head + tail + 1:
        return value
    return f"{value[:head]}...{value[-tail:]}"


templates.env.filters["short_id"] = short_id


def is_htmx_request(request: Request) -> bool:
    return request.headers.get("HX-Request", "").lower() == "true"


def default_spend_form() -> dict[str, str]:
    return {
        "destination_address": "",
        "amount_sats": "",
        "fee_rate": "2.0",
        "change_address": "",
    }


def default_balance_form() -> dict[str, str]:
    return {
        "nostr_key": "",
        "transaction_limit": "5",
    }


def default_sweep_form() -> dict[str, str]:
    return {
        "nostr_key": "",
        "destination_address": "",
        "fee_rate": "2.0",
        "transaction_limit": "5",
    }


def default_silent_payment_form() -> dict[str, str]:
    return {
        "nostr_key": "",
        "txid": "",
        "destination_address": "",
        "fee_rate": "2.0",
        "transaction_limit": "5",
    }


def default_silent_payment_scan_form() -> dict[str, str]:
    return {
        "nostr_key": "",
        "transaction_limit": "5",
        "blockheight": "",
        "mode": "nsp",
    }


def default_silent_payment_ownership_form() -> dict[str, str]:
    return {
        "nostr_key": "",
        "silent_payment_address": "",
    }


def parse_transaction_limit(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise click.ClickException("Transaction count must be an integer.") from exc
    if parsed <= 0:
        raise click.ClickException("Transaction count must be greater than zero.")
    return parsed


async def resolve_balance_page_data(
    nostr_key: str,
    transaction_limit: str,
) -> tuple[dict[str, str], dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, str], dict[str, str]]:
    balance_form = {
        "nostr_key": nostr_key.strip(),
        "transaction_limit": transaction_limit.strip() or "5",
    }
    if not balance_form["nostr_key"]:
        raise click.ClickException("Enter an nsec, npub, NIP-05 identifier, or a bare domain for NIP-05 lookup.")

    tx_limit_value = parse_transaction_limit(balance_form["transaction_limit"])
    balance_result = await asyncio.to_thread(
        derive_p2tr_balance_for_nostr_input,
        balance_form["nostr_key"],
        BLOCKSTREAM_API_BASE,
        5.0,
    )
    recent_transactions_result = await asyncio.to_thread(
        derive_recent_transactions_for_nostr_input,
        balance_form["nostr_key"],
        BLOCKSTREAM_API_BASE,
        5.0,
        tx_limit_value,
    )
    silent_payment_result = await asyncio.to_thread(
        derive_silent_payment_material,
        balance_form["nostr_key"],
    )
    sweep_form = {
        "nostr_key": balance_form["nostr_key"],
        "destination_address": "",
        "fee_rate": "2.0",
        "transaction_limit": balance_form["transaction_limit"],
    }
    silent_payment_form = {
        "nostr_key": balance_form["nostr_key"],
        "txid": "",
        "destination_address": "",
        "fee_rate": "2.0",
        "transaction_limit": balance_form["transaction_limit"],
    }
    return (
        balance_form,
        sweep_form,
        balance_result,
        recent_transactions_result["recent_transactions"],
        silent_payment_result,
        silent_payment_form,
    )


async def resolve_silent_payment_scan_form(
    nostr_key: str,
    transaction_limit: str,
    blockheight: str = "",
    mode: str = "nsp",
) -> dict[str, str]:
    normalized_mode = (mode or "nsp").strip().lower()
    if normalized_mode == "nsw":
        normalized_mode = "nsp"
    if normalized_mode not in {"nsp", "bip352"}:
        raise click.ClickException("Silent Payments mode must be either nsp or bip352.")

    normalized_blockheight = blockheight.strip()
    if not normalized_blockheight:
        current_tip = await asyncio.to_thread(
            fetch_blockstream_tip_height,
            BLOCKSTREAM_API_BASE,
            5.0,
        )
        normalized_blockheight = str(current_tip)

    return {
        "nostr_key": nostr_key.strip(),
        "transaction_limit": transaction_limit.strip() or "5",
        "blockheight": normalized_blockheight,
        "mode": normalized_mode,
    }


async def resolve_silent_payment_ownership_data(
    nostr_key: str,
    silent_payment_address: str,
) -> tuple[dict[str, str], dict[str, Any], str]:
    ownership_form = {
        "nostr_key": nostr_key.strip(),
        "silent_payment_address": silent_payment_address.strip(),
    }
    if not ownership_form["nostr_key"]:
        raise click.ClickException("Enter an npub, nsec, NIP-05 identifier, or bare domain before checking Silent Payments ownership.")

    derived_material = await asyncio.to_thread(
        derive_silent_payment_material,
        ownership_form["nostr_key"],
    )
    success_message = "Derived Silent Payment address from the provided Nostr identity."
    belongs = None
    checked_address = ownership_form["silent_payment_address"]
    if checked_address:
        belongs = await asyncio.to_thread(
            silent_payment_address_belongs_to_nostr_key,
            ownership_form["nostr_key"],
            checked_address,
        )
        success_message = (
            "The provided Silent Payment address matches the resolved Nostr identity."
            if belongs
            else "The provided Silent Payment address does not match the resolved Nostr identity."
        )
    else:
        checked_address = derived_material["silent_payment_address"]

    return ownership_form, {
        "input_value": ownership_form["nostr_key"],
        "input_kind": derived_material["input_kind"],
        "npub": derived_material["npub"],
        "derived_silent_payment_address": derived_material["silent_payment_address"],
        "checked_silent_payment_address": checked_address,
        "belongs": belongs,
        "warning": derived_material["warning"],
    }, success_message


async def render_profile_edit_response(
    request: Request,
    identity: dict[str, Any],
    relays: str,
    profile_name: str,
    profile_fields: dict[str, str],
    current_profile: list[tuple[str, str]],
    *,
    bitcoin_wallet: dict[str, Any] | None = None,
    error_message: str | None = None,
    success_message: str | None = None,
    publish_result: dict[str, Any] | None = None,
    spend_form: dict[str, str] | None = None,
    spend_preview: dict[str, Any] | None = None,
    spend_broadcast: dict[str, Any] | None = None,
    status_code: int = 200,
):
    if bitcoin_wallet is None:
        bitcoin_wallet = await build_bitcoin_wallet_context(identity)
    template_name = "profile_edit_fragment.html" if is_htmx_request(request) else "profile_edit.html"
    return templates.TemplateResponse(
        request,
        template_name,
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "available_profiles": await get_available_profiles(identity),
            "relays": relays,
            "profile_name": profile_name,
            "profile_fields": profile_fields,
            "current_profile": current_profile,
            "bitcoin_wallet": bitcoin_wallet,
            "error_message": error_message,
            "success_message": success_message,
            "publish_result": publish_result,
            "spend_form": spend_form or default_spend_form(),
            "spend_preview": spend_preview,
            "spend_broadcast": spend_broadcast,
        },
        status_code=status_code,
    )


def render_profile_publish_response(
    request: Request,
    *,
    current_profile: list[tuple[str, str]],
    publish_result: dict[str, Any] | None = None,
    error_message: str | None = None,
    success_message: str | None = None,
    status_code: int = 200,
):
    return templates.TemplateResponse(
        request,
        "profile_publish_fragment.html",
        {
            "current_profile": current_profile,
            "publish_result": publish_result,
            "error_message": error_message,
            "success_message": success_message,
        },
        status_code=status_code,
    )


def render_bitcoin_balance_response(
    request: Request,
    identity: dict[str, Any],
    *,
    balance_form: dict[str, str] | None = None,
    balance_result: dict[str, Any] | None = None,
    recent_transactions: list[dict[str, Any]] | None = None,
    silent_payment_result: dict[str, str] | None = None,
    sweep_form: dict[str, str] | None = None,
    sweep_preview: dict[str, Any] | None = None,
    sweep_broadcast: dict[str, Any] | None = None,
    silent_payment_form: dict[str, str] | None = None,
    silent_payment_scan_form: dict[str, str] | None = None,
    silent_payment_scan_result: dict[str, Any] | None = None,
    silent_payment_error: str | None = None,
    silent_payment_success: str | None = None,
    silent_payment_preview: dict[str, Any] | None = None,
    silent_payment_broadcast: dict[str, Any] | None = None,
    silent_payment_ownership_form: dict[str, str] | None = None,
    silent_payment_ownership_result: dict[str, Any] | None = None,
    silent_payment_ownership_error: str | None = None,
    silent_payment_ownership_success: str | None = None,
    error_message: str | None = None,
    success_message: str | None = None,
    status_code: int = 200,
):
    if is_htmx_request(request) and request.url.path == "/bitcoin/silent-payment/ownership":
        return templates.TemplateResponse(
            request,
            "silent_payment_ownership_fragment.html",
            {
                "silent_payment_ownership_form": (
                    silent_payment_ownership_form or default_silent_payment_ownership_form()
                ),
                "silent_payment_ownership_result": silent_payment_ownership_result,
                "silent_payment_ownership_error": silent_payment_ownership_error,
                "silent_payment_ownership_success": silent_payment_ownership_success,
            },
            status_code=status_code,
        )
    template_name = "bitcoin_balance_fragment.html" if is_htmx_request(request) else "bitcoin_balance.html"
    return templates.TemplateResponse(
        request,
        template_name,
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "balance_form": balance_form or default_balance_form(),
            "balance_result": balance_result,
            "recent_transactions": recent_transactions or [],
            "silent_payment_result": silent_payment_result,
            "sweep_form": sweep_form or default_sweep_form(),
            "sweep_preview": sweep_preview,
            "sweep_broadcast": sweep_broadcast,
            "silent_payment_form": silent_payment_form or default_silent_payment_form(),
            "silent_payment_scan_form": silent_payment_scan_form or default_silent_payment_scan_form(),
            "silent_payment_scan_result": silent_payment_scan_result,
            "silent_payment_error": silent_payment_error,
            "silent_payment_success": silent_payment_success,
            "silent_payment_preview": silent_payment_preview,
            "silent_payment_broadcast": silent_payment_broadcast,
            "silent_payment_ownership_form": (
                silent_payment_ownership_form or default_silent_payment_ownership_form()
            ),
            "silent_payment_ownership_result": silent_payment_ownership_result,
            "silent_payment_ownership_error": silent_payment_ownership_error,
            "silent_payment_ownership_success": silent_payment_ownership_success,
            "error_message": error_message,
            "success_message": success_message,
        },
        status_code=status_code,
    )


def render_silent_payment_preview_fragment(
    request: Request,
    *,
    preview_target_id: str,
    silent_payment_form: dict[str, str] | None = None,
    silent_payment_preview: dict[str, Any] | None = None,
    silent_payment_broadcast: dict[str, Any] | None = None,
    error_message: str | None = None,
    success_message: str | None = None,
    status_code: int = 200,
):
    return templates.TemplateResponse(
        request,
        "silent_payment_preview_fragment.html",
        {
            "preview_target_id": preview_target_id,
            "silent_payment_form": silent_payment_form or default_silent_payment_form(),
            "silent_payment_preview": silent_payment_preview,
            "silent_payment_broadcast": silent_payment_broadcast,
            "error_message": error_message,
            "success_message": success_message,
        },
        status_code=status_code,
    )


async def build_bitcoin_wallet_context(identity: dict[str, Any]) -> dict[str, Any]:
    wallet = derive_bitcoin_wallet_material(identity["nsec"])
    try:
        wallet["balance"] = await asyncio.to_thread(
            fetch_blockstream_wallet_balance_sats,
            wallet,
            BLOCKSTREAM_API_BASE,
            5.0,
        )
        wallet["balance_error"] = None
    except (click.ClickException, ControlEventError) as exc:
        wallet["balance"] = None
        wallet["balance_error"] = str(exc)
    return wallet

def session_identity(request: Request) -> dict[str, Any]:
    root_nsec = request.session.get(SESSION_ROOT_NSEC_KEY)
    signer_nsec = request.session.get(SESSION_SIGNER_NSEC_KEY)
    bootstrap_relays = request.session.get(SESSION_BOOTSTRAP_RELAYS_KEY) or configured_home_relays()
    default_relays = request.session.get(SESSION_DEFAULT_RELAYS_KEY) or DEFAULT_RELAYS
    if not root_nsec and not signer_nsec:
        return {
            "logged_in": False,
            "nsec": None,
            "npub": None,
            "pubkey_hex": None,
            "root_nsec": None,
            "bootstrap_relays": bootstrap_relays,
            "default_relays": default_relays,
        }

    effective_nsec = signer_nsec or root_nsec
    if effective_nsec is None:
        return {
            "logged_in": False,
            "nsec": None,
            "npub": None,
            "pubkey_hex": None,
            "root_nsec": None,
            "bootstrap_relays": bootstrap_relays,
            "default_relays": default_relays,
        }

    try:
        keys = resolve_keys(effective_nsec)
    except click.ClickException:
        request.session.pop(SESSION_ROOT_NSEC_KEY, None)
        request.session.pop(SESSION_SIGNER_NSEC_KEY, None)
        return {
            "logged_in": False,
            "nsec": None,
            "npub": None,
            "pubkey_hex": None,
            "root_nsec": None,
            "bootstrap_relays": bootstrap_relays,
            "default_relays": default_relays,
        }

    return {
        "logged_in": True,
        "nsec": effective_nsec,
        "root_nsec": root_nsec,
        "signer_nsec": signer_nsec,
        "bootstrap_relays": bootstrap_relays,
        "default_relays": default_relays,
        "npub": keys.public_key_bech32(),
        "pubkey_hex": keys.public_key_hex(),
        "profile": request.session.get(SESSION_PROFILE_KEY),
    }


def get_session_identity(request: Request) -> dict[str, Any]:
    return session_identity(request)


@contextmanager
def session_bootstrap(identity: dict[str, Any]):
    root_nsec = identity.get("root_nsec") or identity.get("nsec")
    if not root_nsec:
        yield
        return
    home_relays = identity.get("bootstrap_relays") or configured_home_relays()
    token = set_runtime_bootstrap_overrides(root_nsec=root_nsec, home_relays=home_relays)
    try:
        yield
    finally:
        reset_runtime_bootstrap_overrides(token)


async def get_default_template_context(
    identity: dict[str, Any] = Depends(get_session_identity),
) -> dict[str, Any]:
    with session_bootstrap(identity):
        available_profiles = await get_available_profiles(identity)
        selected_profile_social = []
        if identity.get("logged_in") and identity.get("profile"):
            relays = str((await relay_profile_config(identity["profile"])).get("relays") or DEFAULT_RELAYS)
            selected_profile_social = compact_profile(
                await fetch_profile(
                    relays=relays,
                    pubkey_hex=identity["pubkey_hex"],
                    timeout=DEFAULT_QUERY_TIMEOUT,
                    ssl_disable_verify=False,
                )
            )
    return {
        "app_title": APP_TITLE,
        "site_url": SITE_URL,
        "git_commit": GIT_COMMIT,
        "default_relays": identity.get("default_relays") or DEFAULT_RELAYS,
        "bootstrap_relays": identity.get("bootstrap_relays") or configured_home_relays(),
        "identity": identity,
        "available_profiles": available_profiles,
        "selected_profile_social": selected_profile_social,
        "upload_limit_label": upload_limit_label(),
        "error_message": None,
        "success_message": None,
        "generated_nsec": None,
        "created_profile": None,
    }


def merge_compact_profiles(
    primary: list[tuple[str, Any]] | None,
    fallback: list[tuple[str, Any]] | None,
) -> list[tuple[str, Any]]:
    merged = list(primary or [])
    seen = {field for field, _value in merged}
    for field, value in fallback or []:
        if field not in seen:
            merged.append((field, value))
            seen.add(field)
    return merged


async def selected_profile_social(identity: dict[str, Any]) -> list[tuple[str, Any]]:
    if not identity.get("logged_in") or not identity.get("profile") or not identity.get("pubkey_hex"):
        return []
    relays = str((await relay_profile_config(identity["profile"])).get("relays") or DEFAULT_RELAYS)
    return compact_profile(
        await fetch_profile(
            relays=relays,
            pubkey_hex=identity["pubkey_hex"],
            timeout=DEFAULT_QUERY_TIMEOUT,
            ssl_disable_verify=False,
        )
    )


async def enrich_query_controller_profile_for_identity(
    query_context: dict[str, Any],
    identity: dict[str, Any],
) -> None:
    current_controller = query_context.get("current_controller") or {}
    if not current_controller.get("is_current_profile"):
        return

    active_profile = await selected_profile_social(identity)
    if not active_profile:
        return

    current_controller["profile"] = merge_compact_profiles(
        current_controller.get("profile"),
        active_profile,
    )
    current_controller["picture_url"] = current_controller.get("picture_url") or profile_picture_url(
        current_controller["profile"]
    )


def normalize_relays_form(relays: str = Form(DEFAULT_RELAYS)) -> str:
    raw = relays or DEFAULT_RELAYS
    return normalize_relays(raw)


@app.post("/settings")
async def update_settings(
    request: Request,
    bootstrap_relays: str = Form(""),
    default_relays: str = Form(""),
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    try:
        normalized_bootstrap_relays = await validate_relays(bootstrap_relays or configured_home_relays(), timeout=DEFAULT_QUERY_TIMEOUT)
        normalized_default_relays = await validate_relays(default_relays or DEFAULT_RELAYS, timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(
            request,
            "settings.html",
            template_context,
            status_code=400,
        )

    request.session[SESSION_BOOTSTRAP_RELAYS_KEY] = normalized_bootstrap_relays
    request.session[SESSION_DEFAULT_RELAYS_KEY] = normalized_default_relays

    template_context = await get_default_template_context(session_identity(request))
    template_context["success_message"] = "Updated relay settings for this session."
    return templates.TemplateResponse(
        request,
        "settings.html",
        template_context,
    )


@app.get("/settings")
async def settings_page(
    request: Request,
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    return templates.TemplateResponse(
        request,
        "settings.html",
        template_context,
    )


async def relay_profile_names() -> tuple[str, list[str]]:
    config = load_user_config()
    try:
        index = await _async_load_profiles_index(config)
    except click.ClickException:
        return DEFAULT_PROFILE_NAME, []
    if index is None:
        return DEFAULT_PROFILE_NAME, []
    return index.active_profile, sorted(index.profiles)


async def relay_profile_config(profile_name: str | None) -> dict[str, Any]:
    resolved = packaged_defaults()
    if not profile_name:
        return resolved
    config = load_user_config()
    try:
        record = await _async_load_profile_record(profile_name, config)
    except click.ClickException:
        return resolved
    if record is None:
        return resolved
    values = record.model_dump(exclude_none=True)
    values.pop("schema_version", None)
    values.pop("profile", None)
    resolved.update(values)
    return resolved


async def resolve_profile_signer_nsec(profile_name: str, config: dict | None = None) -> tuple[str | None, str]:
    resolved_config = config or load_user_config()
    try:
        remote_value = await _async_load_profile_secret(profile_name, resolved_config)
    except click.ClickException:
        return None, "relay unavailable"
    if remote_value:
        return remote_value, "relay"

    return None, "none"


async def relay_aliases(config: dict | None = None) -> dict[str, str]:
    resolved_config = config or load_user_config()
    try:
        index = await _async_load_aliases_index(resolved_config)
    except click.ClickException:
        index = None
    if index is not None:
        return dict(index.aliases)
    return dict(resolved_config.get("aliases", {}))


async def resolve_control_party_pubkey_hex(value: str, identity: dict[str, Any]) -> str:
    candidate = value.strip()
    if not candidate:
        raise click.ClickException("party must not be empty")

    if candidate.startswith("npub"):
        author_hex = Keys.bech32_to_hex(candidate)
        if author_hex is None:
            raise click.ClickException(f"invalid npub key: {candidate}")
        return assert_hex_pubkey(author_hex.lower())

    if len(candidate) == 64:
        return assert_hex_pubkey(candidate.lower())

    config = load_user_config()
    with session_bootstrap(identity):
        _, profile_names = await relay_profile_names()
        if candidate in profile_names:
            signer_nsec, _ = await resolve_profile_signer_nsec(candidate, config)
            if not signer_nsec:
                raise click.ClickException(f"profile '{candidate}' does not have a relay-backed signer key")
            return resolve_keys(signer_nsec).public_key_hex()

        if "@" not in candidate:
            alias_value = (await relay_aliases(config)).get(normalize_alias(candidate))
            if alias_value:
                candidate = alias_value

    if candidate.startswith("npub"):
        author_hex = Keys.bech32_to_hex(candidate)
        if author_hex is None:
            raise click.ClickException(f"invalid npub key: {candidate}")
        return assert_hex_pubkey(author_hex.lower())

    return await asyncio.to_thread(resolve_author, candidate)


def profile_switch_signer_source_label(signer_source: str) -> str:
    if signer_source == "relay":
        return "its root-managed signer"
    return f"the {signer_source} signer secret"


async def get_available_profiles(identity: dict[str, Any]) -> list[dict[str, Any]]:
    if not identity.get("logged_in"):
        return []

    root_pubkey_hex = None
    root_nsec = identity.get("root_nsec")
    if root_nsec:
        try:
            root_pubkey_hex = resolve_keys(root_nsec).public_key_hex()
        except click.ClickException:
            root_pubkey_hex = None

    with session_bootstrap(identity):
        config = load_user_config()
        active_profile, profile_names = await relay_profile_names()
        profiles: list[dict[str, Any]] = []
        for profile_name in profile_names:
            signer_nsec, signer_source = await resolve_profile_signer_nsec(profile_name, config)
            signer_npub = None
            signer_matches_session = False
            if signer_nsec:
                try:
                    signer_keys = resolve_keys(signer_nsec)
                    signer_npub = signer_keys.public_key_bech32()
                    signer_matches_session = signer_keys.public_key_hex() == identity["pubkey_hex"]
                    if (
                        profile_name == DEFAULT_PROFILE_NAME
                        and root_pubkey_hex is not None
                        and signer_keys.public_key_hex() == root_pubkey_hex
                    ):
                        continue
                except click.ClickException:
                    signer_npub = None

            profiles.append(
                {
                    "name": profile_name,
                    "is_active": profile_name == active_profile,
                    "is_selected": profile_name == identity.get("profile"),
                    "signer_npub": signer_npub,
                    "signer_source": signer_source,
                    "signer_matches_session": signer_matches_session,
                    "can_select": signer_nsec is not None,
                    "usable_label": (
                        "matches current session signer"
                        if signer_matches_session
                        else ("signer unavailable in this environment" if signer_source == "relay unavailable" else "session override available")
                    ),
                }
            )

    return profiles


def profile_form_values(profile: dict[str, Any] | None) -> dict[str, str]:
    source = profile or {}
    return {field: str(source.get(field, "")) for field in PROFILE_FIELDS}


async def render_warehouse_receipts_page(
    request: Request,
    identity: dict[str, Any],
    *,
    error_message: str | None = None,
    success_message: str | None = None,
    status_code: int = 200,
):
    template_context = await get_default_template_context(identity)
    template_context["error_message"] = error_message
    template_context["success_message"] = success_message
    template_context["trivia_fact"] = random_openetr_trivia_fact()
    return templates.TemplateResponse(
        request,
        "warehouse_receipts.html",
        template_context,
        status_code=status_code,
    )


async def render_digital_product_passports_page(
    request: Request,
    identity: dict[str, Any],
    *,
    error_message: str | None = None,
    success_message: str | None = None,
    status_code: int = 200,
):
    template_context = await get_default_template_context(identity)
    template_context["error_message"] = error_message
    template_context["success_message"] = success_message
    return templates.TemplateResponse(
        request,
        "digital_product_passports.html",
        template_context,
        status_code=status_code,
    )


def normalize_profile_return_to(return_to: str | None) -> str:
    allowed_return_paths = {"/", "/openetr", "/warehouse-receipts", "/digital-product-passports"}
    normalized = (return_to or "/").strip() or "/"
    if normalized not in allowed_return_paths:
        return "/"
    return normalized


async def render_profile_return_page(
    request: Request,
    identity: dict[str, Any],
    return_to: str | None,
    *,
    error_message: str | None = None,
    success_message: str | None = None,
    created_profile: dict[str, Any] | None = None,
    status_code: int = 200,
):
    normalized_return_to = normalize_profile_return_to(return_to)
    if normalized_return_to == "/warehouse-receipts":
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message=error_message,
            success_message=success_message,
            status_code=status_code,
        )
    if normalized_return_to == "/digital-product-passports":
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message=error_message,
            success_message=success_message,
            status_code=status_code,
        )

    template_context = await get_default_template_context(identity)
    template_context["error_message"] = error_message
    template_context["success_message"] = success_message
    template_context["created_profile"] = created_profile
    template_name = "control_desk.html" if normalized_return_to == "/" else "index.html"
    return templates.TemplateResponse(
        request,
        template_name,
        template_context,
        status_code=status_code,
    )


async def render_warehouse_receipt_result(
    request: Request,
    identity: dict[str, Any],
    *,
    filename: str,
    size_bytes: int,
    digest: str,
    relays: str,
    query_context: dict[str, Any],
    issue_result: dict[str, Any] | None = None,
    control_result: dict[str, Any] | None = None,
    success_message: str | None = None,
    media_preview: dict[str, str] | None = None,
    blossom_storage: dict[str, Any] | None = None,
):
    return templates.TemplateResponse(
        request,
        "warehouse_receipt_result.html",
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "available_profiles": await get_available_profiles(identity),
            "filename": filename,
            "size_bytes": size_bytes,
            "sha256": digest,
            "object_id": format_object_identifier(digest),
            "relays": relays,
            "query": query_context,
            "issue_result": issue_result,
            "control_result": control_result,
            "success_message": success_message,
            "media_preview": media_preview,
            "blossom_storage": blossom_storage,
            **qr_context_for_digest(request, digest),
        },
    )


async def read_uploaded_receipt(file: UploadFile, *, retain_content: bool = False) -> UploadedFileInfo:
    return await hash_uploaded_file(file, default_filename="warehouse-receipt", retain_content=retain_content)


async def read_uploaded_product_passport(file: UploadFile, *, retain_content: bool = False) -> UploadedFileInfo:
    return await hash_uploaded_file(file, default_filename="digital-product-passport", retain_content=retain_content)


def parse_optional_force(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


async def render_warehouse_control_result(
    request: Request,
    identity: dict[str, Any],
    *,
    digest: str,
    relays: str,
    control_result: dict[str, Any],
    success_message: str,
):
    query_context = await build_query_etr_result(
        digest=digest,
        relays=relays,
        author_pubkey_hex=identity.get("pubkey_hex"),
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    return await render_warehouse_receipt_result(
        request,
        identity,
        filename="warehouse receipt object",
        size_bytes=0,
        digest=digest,
        relays=relays,
        query_context=query_context,
        control_result=control_result,
        success_message=success_message,
    )

@app.get("/")
async def landing_page(
    request: Request,
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    return templates.TemplateResponse(
        request,
        "control_desk.html",
        template_context,
    )


@app.get("/openetr")
async def openetr_general_page(
    request: Request,
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    return templates.TemplateResponse(
        request,
        "index.html",
        template_context,
    )


@app.get("/login")
async def login_page(
    request: Request,
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    return templates.TemplateResponse(
        request,
        "login.html",
        template_context,
    )


@app.get("/overview")
async def overview_page(
    request: Request,
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    template_context["overview_image_url"] = "/app-assets/images/info-graphic.png"
    template_context["architecture_image_url"] = "/app-assets/images/relay-backed-architecture.png"
    return templates.TemplateResponse(
        request,
        "overview.html",
        template_context,
    )


@app.get("/warehouse-receipts")
async def warehouse_receipts_page(
    request: Request,
    identity: dict[str, Any] = Depends(get_session_identity),
):
    return await render_warehouse_receipts_page(request, identity)


@app.get("/digital-product-passports")
async def digital_product_passports_page(
    request: Request,
    identity: dict[str, Any] = Depends(get_session_identity),
):
    return await render_digital_product_passports_page(request, identity)


@app.get("/experimental")
async def experimental_page(
    request: Request,
    identity: dict[str, Any] = Depends(get_session_identity),
):
    return render_bitcoin_balance_response(request, identity)


@app.get("/etr/qr/{digest}", responses={200: {"content": {"image/png": {}}}})
async def public_etr_query_qr(request: Request, digest: str):
    return render_etr_query_qr(request, digest)


@app.get("/etr/blob/{digest}", include_in_schema=False)
async def public_etr_blossom_blob(digest: str):
    try:
        object_digest = normalize_object_identifier(digest.strip())
        content, declared_type = await asyncio.to_thread(blossom_fetch_bytes, object_digest)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Verified Blossom blob not found: {exc}") from exc
    media_type = preview_media_type(f"OpenETR object {object_digest}", declared_type, content[:UPLOAD_READ_CHUNK_BYTES])
    if not media_type:
        raise HTTPException(status_code=415, detail="Blossom blob is not a supported preview media type.")
    return StreamingResponse(
        io.BytesIO(content),
        media_type=media_type,
        headers={
            "Cache-Control": "no-store",
            "Content-Disposition": "inline",
        },
    )


@app.get("/etr/{digest}")
async def public_etr_lookup(
    request: Request,
    digest: str,
    identity: dict[str, Any] = Depends(get_session_identity),
):
    try:
        object_digest = normalize_object_identifier(digest.strip())
        validated_relays = await validate_relays(
            identity.get("default_relays") or DEFAULT_RELAYS,
            timeout=DEFAULT_QUERY_TIMEOUT,
        )
    except (click.ClickException, ControlEventError) as exc:
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    query_context = await build_query_etr_result(
        digest=object_digest,
        relays=validated_relays,
        author_pubkey_hex=identity.get("pubkey_hex"),
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    media_preview = await blossom_media_preview_for_digest(object_digest)
    return templates.TemplateResponse(
        request,
        "query_etr_result.html",
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "available_profiles": await get_available_profiles(identity),
            "filename": f"OpenETR object {format_object_identifier(object_digest)}",
            "size_bytes": 0,
            "sha256": object_digest,
            "object_id": format_object_identifier(object_digest),
            "relays": validated_relays,
            "query": query_context,
            "media_preview": media_preview,
            **qr_context_for_digest(request, object_digest),
        },
    )


def render_etr_query_qr(request: Request, digest: str) -> StreamingResponse:
    try:
        object_digest = normalize_object_identifier(digest.strip())
    except click.ClickException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    try:
        import qrcode  # noqa: F401
        import PIL  # noqa: F401
    except ImportError as exc:
        raise HTTPException(status_code=503, detail="QR code support is not installed.") from exc
    # The image path accepts a digest or nobj; the QR payload is the full query URL.
    qr_text = public_etr_url(request, object_digest)
    image = branded_qr_image(qr_text)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="image/png",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/qr/{digest}", include_in_schema=False)
async def legacy_short_etr_query_qr(request: Request, digest: str):
    return render_etr_query_qr(request, digest)


@app.get("/etr/{digest}/qr", include_in_schema=False)
async def legacy_public_etr_query_qr(request: Request, digest: str):
    return render_etr_query_qr(request, digest)


@app.get("/api/etr-qr/{digest}", include_in_schema=False)
async def etr_query_qr(request: Request, digest: str):
    return render_etr_query_qr(request, digest)


@app.post("/warehouse-receipts/query")
async def warehouse_receipts_query(
    request: Request,
    file: UploadFile = File(...),
    relays: str = Depends(normalize_relays_form),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message=str(exc),
            status_code=400,
        )

    try:
        upload = await read_uploaded_receipt(file)
    except HTTPException as exc:
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message=str(exc.detail),
            status_code=exc.status_code,
        )
    query_context = await build_query_etr_result(
        digest=upload.digest,
        relays=validated_relays,
        author_pubkey_hex=identity.get("pubkey_hex"),
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    return await render_warehouse_receipt_result(
        request,
        identity,
        filename=upload.filename,
        size_bytes=upload.size_bytes,
        digest=upload.digest,
        relays=validated_relays,
        query_context=query_context,
        media_preview=upload.media_preview,
    )


@app.post("/warehouse-receipts/issue")
async def warehouse_receipts_issue(
    request: Request,
    file: UploadFile = File(...),
    relays: str = Depends(normalize_relays_form),
    receipt_reference: str = Form(""),
    goods_description: str = Form(""),
    force: str | None = Form(None),
    store_upload: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    should_store_upload = parse_optional_checkbox(store_upload)
    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message=str(exc),
            status_code=400,
        )

    if not identity.get("logged_in"):
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message="Log in with an nsec before creating a warehouse receipt control record.",
            status_code=400,
        )

    if not identity.get("profile"):
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message="Select a warehouse operator or issuer profile before creating a warehouse receipt control record.",
            status_code=400,
        )

    try:
        upload = await read_uploaded_receipt(file, retain_content=should_store_upload)
    except HTTPException as exc:
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message=str(exc.detail),
            status_code=exc.status_code,
        )
    guard = await evaluate_issue_etr_guard(
        relays=validated_relays,
        digest=upload.digest,
        author_pubkey_hex=identity["pubkey_hex"],
        query_timeout=DEFAULT_QUERY_TIMEOUT,
        limit=DEFAULT_LIMIT,
    )
    if guard["should_warn"] and force != "true":
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message=(
                "This receipt file already has a control record from the current signer. "
                "Select the force checkbox if you intentionally want to publish a replacement origin event."
            ),
            status_code=400,
        )
    blossom_storage = await maybe_store_on_blossom(
        upload,
        should_store_upload,
        signer_nsec=identity["nsec"],
    )

    extra_tags = [
        ["domain", "mlwr"],
        ["document_type", "warehouse_receipt"],
    ]
    if receipt_reference.strip():
        extra_tags.append(["record_reference", receipt_reference.strip()])
    if goods_description.strip():
        extra_tags.append(["record_description", goods_description.strip()])

    issue_result = await publish_issue_etr(
        filename=upload.filename,
        size_bytes=upload.size_bytes,
        digest=upload.digest,
        relays=validated_relays,
        signer_nsec=identity["nsec"],
        comment=f"Created warehouse receipt control record {receipt_reference.strip() or upload.filename}",
        extra_tags=extra_tags,
    )
    query_context = await build_query_etr_result(
        digest=issue_result["sha256"],
        relays=validated_relays,
        author_pubkey_hex=identity["pubkey_hex"],
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    return await render_warehouse_receipt_result(
        request,
        identity,
        filename=issue_result["filename"],
        size_bytes=issue_result["size_bytes"],
        digest=issue_result["sha256"],
        relays=validated_relays,
        query_context=query_context,
        issue_result=issue_result,
        success_message="Warehouse receipt control record published through the general OpenETR issue service.",
        media_preview=upload.media_preview,
        blossom_storage=blossom_storage,
    )


@app.post("/digital-product-passports/query")
async def digital_product_passports_query(
    request: Request,
    file: UploadFile = File(...),
    relays: str = Depends(normalize_relays_form),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
        upload = await read_uploaded_product_passport(file)
    except (click.ClickException, ControlEventError) as exc:
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message=str(exc),
            status_code=400,
        )
    except HTTPException as exc:
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message=str(exc.detail),
            status_code=exc.status_code,
        )

    query_context = await build_query_etr_result(
        digest=upload.digest,
        relays=validated_relays,
        author_pubkey_hex=identity.get("pubkey_hex"),
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    return templates.TemplateResponse(
        request,
        "query_etr_result.html",
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "available_profiles": await get_available_profiles(identity),
            "filename": upload.filename,
            "size_bytes": upload.size_bytes,
            "sha256": upload.digest,
            "object_id": format_object_identifier(upload.digest),
            "relays": validated_relays,
            "query": query_context,
            "media_preview": upload.media_preview,
            **qr_context_for_digest(request, upload.digest),
        },
    )


@app.post("/digital-product-passports/create")
async def digital_product_passports_create(
    request: Request,
    file: UploadFile = File(...),
    relays: str = Depends(normalize_relays_form),
    product_name: str = Form(""),
    product_id: str = Form(""),
    manufacturer: str = Form(""),
    batch_or_lot: str = Form(""),
    description: str = Form(""),
    store_upload: str | None = Form(None),
    force: str = Form("false"),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    should_store_upload = parse_optional_checkbox(store_upload)
    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message=str(exc),
            status_code=400,
        )

    if not identity.get("logged_in"):
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message="Log in with an nsec before creating a product passport control record.",
            status_code=400,
        )

    if not identity.get("profile"):
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message="Select a manufacturer, importer, or issuer profile before creating a product passport control record.",
            status_code=400,
        )

    try:
        upload = await read_uploaded_product_passport(file, retain_content=should_store_upload)
    except HTTPException as exc:
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message=str(exc.detail),
            status_code=exc.status_code,
        )

    guard = await evaluate_issue_etr_guard(
        relays=validated_relays,
        digest=upload.digest,
        author_pubkey_hex=identity["pubkey_hex"],
        query_timeout=DEFAULT_QUERY_TIMEOUT,
        limit=DEFAULT_LIMIT,
    )
    if guard["should_warn"] and force != "true":
        return await render_digital_product_passports_page(
            request,
            identity,
            error_message=(
                "This Product Passport file already has a control record from the current signer. "
                "Select the force checkbox if you intentionally want to publish a replacement origin event."
            ),
            status_code=400,
        )

    blossom_storage = await maybe_store_on_blossom(
        upload,
        should_store_upload,
        signer_nsec=identity["nsec"],
    )

    extra_tags = [
        ["domain", "digital_product_passport"],
        ["document_type", "product_passport"],
    ]
    if product_name.strip():
        extra_tags.append(["product_name", product_name.strip()])
    if product_id.strip():
        extra_tags.append(["product_id", product_id.strip()])
        extra_tags.append(["record_reference", product_id.strip()])
    if manufacturer.strip():
        extra_tags.append(["manufacturer", manufacturer.strip()])
    if batch_or_lot.strip():
        extra_tags.append(["batch_or_lot", batch_or_lot.strip()])
    if description.strip():
        extra_tags.append(["record_description", description.strip()])

    reference = product_id.strip() or product_name.strip() or upload.filename
    issue_result = await publish_issue_etr(
        filename=upload.filename,
        size_bytes=upload.size_bytes,
        digest=upload.digest,
        relays=validated_relays,
        signer_nsec=identity["nsec"],
        comment=f"Created digital product passport control record {reference}",
        extra_tags=extra_tags,
    )
    query_context = await build_query_etr_result(
        digest=issue_result["sha256"],
        relays=validated_relays,
        author_pubkey_hex=identity["pubkey_hex"],
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    return templates.TemplateResponse(
        request,
        "query_etr_result.html",
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "available_profiles": await get_available_profiles(identity),
            "filename": issue_result["filename"],
            "size_bytes": issue_result["size_bytes"],
            "sha256": issue_result["sha256"],
            "object_id": issue_result["object_id"],
            "relays": validated_relays,
            "query": query_context,
            "issue_result": issue_result,
            "success_message": "Digital product passport control record published through the general OpenETR issue service.",
            "media_preview": upload.media_preview,
            "blossom_storage": blossom_storage,
            **qr_context_for_digest(request, issue_result["sha256"]),
        },
    )


async def require_warehouse_action_context(
    request: Request,
    identity: dict[str, Any],
    relays: str,
    digest: str,
) -> tuple[str, str] | Any:
    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
        object_digest = normalize_object_identifier(digest.strip())
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=str(exc), status_code=400)

    if not identity.get("logged_in"):
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message="Log in with an nsec before publishing a warehouse receipt action.",
            status_code=400,
        )
    if not identity.get("profile"):
        return await render_warehouse_receipts_page(
            request,
            identity,
            error_message="Select a warehouse receipt profile before publishing this action.",
            status_code=400,
        )
    return validated_relays, object_digest


@app.post("/warehouse-receipts/transfer/initiate")
async def warehouse_receipts_transfer_initiate(
    request: Request,
    digest: str = Form(""),
    relays: str = Depends(normalize_relays_form),
    transferee: str = Form(""),
    reference: str = Form(""),
    force: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    context = await require_warehouse_action_context(request, identity, relays, digest)
    if not isinstance(context, tuple):
        return context
    validated_relays, object_digest = context
    try:
        transferee_pubkey_hex = await resolve_control_party_pubkey_hex(transferee, identity)
    except click.ClickException as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=f"Transferee could not be resolved: {exc}", status_code=400)
    comment = "warehouse receipt transfer initiate"
    if reference.strip():
        comment += f"; ref={reference.strip()}"
    try:
        control_result = await publish_transfer_initiate_event(
            relays=validated_relays,
            object_digest=object_digest,
            prior_event_id=None,
            signer_nsec=identity["nsec"],
            transferee_pubkey_hex=transferee_pubkey_hex,
            comment=comment,
            force=parse_optional_force(force),
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=str(exc), status_code=400)
    return await render_warehouse_control_result(
        request,
        identity,
        digest=object_digest,
        relays=validated_relays,
        control_result=control_result,
        success_message="Warehouse receipt transfer initiated.",
    )


@app.post("/warehouse-receipts/transfer/accept")
async def warehouse_receipts_transfer_accept(
    request: Request,
    digest: str = Form(""),
    relays: str = Depends(normalize_relays_form),
    reference: str = Form(""),
    force: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    context = await require_warehouse_action_context(request, identity, relays, digest)
    if not isinstance(context, tuple):
        return context
    validated_relays, object_digest = context
    comment = "warehouse receipt transfer accept"
    if reference.strip():
        comment += f"; ref={reference.strip()}"
    try:
        control_result = await publish_transfer_accept_event(
            relays=validated_relays,
            object_digest=object_digest,
            signer_nsec=identity["nsec"],
            comment=comment,
            force=parse_optional_force(force),
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=str(exc), status_code=400)
    return await render_warehouse_control_result(
        request,
        identity,
        digest=object_digest,
        relays=validated_relays,
        control_result=control_result,
        success_message="Warehouse receipt transfer accepted.",
    )


@app.post("/warehouse-receipts/encumber")
async def warehouse_receipts_encumber(
    request: Request,
    digest: str = Form(""),
    relays: str = Depends(normalize_relays_form),
    beneficiary: str = Form(""),
    claim_type: str = Form("pledge"),
    reference: str = Form(""),
    force: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    context = await require_warehouse_action_context(request, identity, relays, digest)
    if not isinstance(context, tuple):
        return context
    validated_relays, object_digest = context
    try:
        beneficiary_pubkey_hex = await resolve_control_party_pubkey_hex(beneficiary, identity)
    except click.ClickException as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=f"Secured party could not be resolved: {exc}", status_code=400)
    try:
        control_result = await publish_auxiliary_control_event(
            relays=validated_relays,
            object_digest=object_digest,
            prior_event_id=None,
            signer_nsec=identity["nsec"],
            action=ACTION_ENCUMBER,
            comment="warehouse receipt encumbrance",
            participant_pubkey_hex=beneficiary_pubkey_hex,
            control_type=claim_type.strip() or "pledge",
            external_ref=reference.strip() or None,
            force=parse_optional_force(force),
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=str(exc), status_code=400)
    return await render_warehouse_control_result(
        request,
        identity,
        digest=object_digest,
        relays=validated_relays,
        control_result=control_result,
        success_message="Warehouse receipt pledge, lien, or restriction recorded.",
    )


@app.post("/warehouse-receipts/discharge")
async def warehouse_receipts_discharge(
    request: Request,
    digest: str = Form(""),
    relays: str = Depends(normalize_relays_form),
    encumbrance_event: str = Form(""),
    releasing_party: str = Form(""),
    reference: str = Form(""),
    force: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    context = await require_warehouse_action_context(request, identity, relays, digest)
    if not isinstance(context, tuple):
        return context
    validated_relays, object_digest = context
    participant_pubkey_hex = None
    if releasing_party.strip():
        try:
            participant_pubkey_hex = await resolve_control_party_pubkey_hex(releasing_party, identity)
        except click.ClickException as exc:
            return await render_warehouse_receipts_page(request, identity, error_message=f"Releasing party could not be resolved: {exc}", status_code=400)
    try:
        control_result = await publish_auxiliary_control_event(
            relays=validated_relays,
            object_digest=object_digest,
            prior_event_id=None,
            signer_nsec=identity["nsec"],
            action=ACTION_DISCHARGE,
            comment="warehouse receipt encumbrance discharge",
            participant_pubkey_hex=participant_pubkey_hex,
            encumbrance_event_id=encumbrance_event,
            external_ref=reference.strip() or None,
            force=parse_optional_force(force),
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=str(exc), status_code=400)
    return await render_warehouse_control_result(
        request,
        identity,
        digest=object_digest,
        relays=validated_relays,
        control_result=control_result,
        success_message="Warehouse receipt pledge, lien, or restriction released.",
    )


@app.post("/warehouse-receipts/redeem")
async def warehouse_receipts_redeem(
    request: Request,
    digest: str = Form(""),
    relays: str = Depends(normalize_relays_form),
    obligor: str = Form(""),
    reference: str = Form(""),
    force: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    context = await require_warehouse_action_context(request, identity, relays, digest)
    if not isinstance(context, tuple):
        return context
    validated_relays, object_digest = context
    try:
        obligor_pubkey_hex = await resolve_control_party_pubkey_hex(obligor, identity)
    except click.ClickException as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=f"Warehouse operator / obligor could not be resolved: {exc}", status_code=400)
    try:
        control_result = await publish_auxiliary_control_event(
            relays=validated_relays,
            object_digest=object_digest,
            prior_event_id=None,
            signer_nsec=identity["nsec"],
            action=ACTION_REDEEM,
            comment="warehouse receipt presentation for delivery",
            participant_pubkey_hex=obligor_pubkey_hex,
            external_ref=reference.strip() or None,
            force=parse_optional_force(force),
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=str(exc), status_code=400)
    return await render_warehouse_control_result(
        request,
        identity,
        digest=object_digest,
        relays=validated_relays,
        control_result=control_result,
        success_message="Warehouse receipt presented for delivery.",
    )


@app.post("/warehouse-receipts/terminate")
async def warehouse_receipts_terminate(
    request: Request,
    digest: str = Form(""),
    relays: str = Depends(normalize_relays_form),
    reference: str = Form(""),
    force: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    context = await require_warehouse_action_context(request, identity, relays, digest)
    if not isinstance(context, tuple):
        return context
    validated_relays, object_digest = context
    comment = "warehouse receipt delivery complete"
    if reference.strip():
        comment += f"; ref={reference.strip()}"
    try:
        control_result = await publish_auxiliary_control_event(
            relays=validated_relays,
            object_digest=object_digest,
            prior_event_id=None,
            signer_nsec=identity["nsec"],
            action=ACTION_TERMINATE,
            comment=comment,
            force=parse_optional_force(force),
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_warehouse_receipts_page(request, identity, error_message=str(exc), status_code=400)
    return await render_warehouse_control_result(
        request,
        identity,
        digest=object_digest,
        relays=validated_relays,
        control_result=control_result,
        success_message="Warehouse receipt lifecycle completed.",
    )


@app.get("/bitcoin/check-balance")
async def bitcoin_balance_page(
    request: Request,
    nostr_key: str = Query(""),
    transaction_limit: str = Query("5"),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    if not nostr_key.strip():
        return render_bitcoin_balance_response(request, identity)

    try:
        balance_form, sweep_form, balance_result, recent_transactions, silent_payment_result, silent_payment_form = await resolve_balance_page_data(
            nostr_key,
            transaction_limit,
        )
        silent_payment_scan_form = await resolve_silent_payment_scan_form(
            nostr_key,
            transaction_limit,
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form={
                "nostr_key": nostr_key.strip(),
                "transaction_limit": transaction_limit.strip() or "5",
            },
            error_message=str(exc),
            status_code=400,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        balance_form=balance_form,
        balance_result=balance_result,
        recent_transactions=recent_transactions,
        silent_payment_result=silent_payment_result,
        sweep_form=sweep_form,
        silent_payment_form=silent_payment_form,
        silent_payment_scan_form=silent_payment_scan_form,
        success_message="Resolved Taproot wallet balance.",
    )


@app.post("/bitcoin/check-balance")
async def bitcoin_balance_submit(
    request: Request,
    nostr_key: str = Form(""),
    transaction_limit: str = Form("5"),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    try:
        balance_form, sweep_form, balance_result, recent_transactions, silent_payment_result, silent_payment_form = await resolve_balance_page_data(
            nostr_key,
            transaction_limit,
        )
        silent_payment_scan_form = await resolve_silent_payment_scan_form(
            nostr_key,
            transaction_limit,
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form={
                "nostr_key": nostr_key.strip(),
                "transaction_limit": transaction_limit.strip() or "5",
            },
            error_message=str(exc),
            status_code=400,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        balance_form=balance_form,
        balance_result=balance_result,
        recent_transactions=recent_transactions,
        silent_payment_result=silent_payment_result,
        sweep_form=sweep_form,
        silent_payment_form=silent_payment_form,
        silent_payment_scan_form=silent_payment_scan_form,
        success_message="Resolved Taproot wallet balance.",
    )


@app.post("/bitcoin/silent-payment/ownership")
async def bitcoin_silent_payment_ownership(
    request: Request,
    nostr_key: str = Form(""),
    silent_payment_address: str = Form(""),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    try:
        ownership_form, ownership_result, ownership_success = await resolve_silent_payment_ownership_data(
            nostr_key,
            silent_payment_address,
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            silent_payment_ownership_form={
                "nostr_key": nostr_key.strip(),
                "silent_payment_address": silent_payment_address.strip(),
            },
            silent_payment_ownership_error=str(exc),
            status_code=400,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        silent_payment_ownership_form=ownership_form,
        silent_payment_ownership_result=ownership_result,
        silent_payment_ownership_success=ownership_success,
    )


@app.post("/bitcoin/silent-payment/transactions")
async def bitcoin_silent_payment_transactions(
    request: Request,
    nostr_key: str = Form(""),
    transaction_limit: str = Form("5"),
    blockheight: str = Form(""),
    mode: str = Form("nsp"),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    balance_form = {
        "nostr_key": nostr_key.strip(),
        "transaction_limit": transaction_limit.strip() or "5",
    }
    try:
        silent_payment_scan_form = await resolve_silent_payment_scan_form(
            nostr_key,
            transaction_limit,
            blockheight,
            mode,
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            silent_payment_scan_form={
                "nostr_key": nostr_key.strip(),
                "transaction_limit": transaction_limit.strip() or "5",
                "blockheight": blockheight.strip(),
                "mode": mode.strip().lower() or "nsp",
            },
            error_message=str(exc),
            status_code=400,
        )

    try:
        _, sweep_form, balance_result, recent_transactions, silent_payment_result, silent_payment_form = await resolve_balance_page_data(
            silent_payment_scan_form["nostr_key"],
            silent_payment_scan_form["transaction_limit"],
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message=str(exc),
            status_code=400,
        )

    if balance_result["input_kind"] != "nsec":
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message="Silent Payments transaction lookup requires an nsec so the receiver scan key is available.",
            status_code=400,
        )

    try:
        scan_blockheight = int(silent_payment_scan_form["blockheight"])
    except ValueError:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message="Silent Payments block height must be an integer.",
            status_code=400,
        )
    if scan_blockheight < 0:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message="Silent Payments block height must be zero or greater.",
            status_code=400,
        )

    try:
        wallet_material = await asyncio.to_thread(
            resolve_silent_payment_wallet_mode_material,
            silent_payment_scan_form["nostr_key"],
            silent_payment_scan_form["mode"],
        )
        frigate_result = await asyncio.to_thread(
            frigate_scan_subscribe,
            wallet_material["scan_private_key_hex"],
            wallet_material["spend_public_key_hex"],
            scan_blockheight,
            FRIGATE_HOST,
            FRIGATE_PORT,
            FRIGATE_SSL,
            FRIGATE_TIMEOUT,
        )
        silent_payment_scan_result = {
            "wallet_mode": wallet_material["wallet_mode"],
            "silent_payment_address": wallet_material["silent_payment_address"],
            "scan_mode": "frigate",
            "discovery_only": True,
            "scan_source": f"{'ssl' if FRIGATE_SSL else 'tcp'}://{FRIGATE_HOST}:{FRIGATE_PORT}",
            "subscription": frigate_result["subscription"],
            "progress_updates": frigate_result["progress_updates"],
            "transactions": [
                {
                    "txid": str(entry.get("tx_hash") or ""),
                    "height": int(entry.get("height", 0) or 0),
                    "tweak_key": str(entry.get("tweak_key") or ""),
                }
                for entry in frigate_result["history"]
                if entry.get("tx_hash")
            ],
        }
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message=str(exc),
            status_code=400,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        balance_form=balance_form,
        balance_result=balance_result,
        recent_transactions=recent_transactions,
        silent_payment_result=silent_payment_result,
        sweep_form=sweep_form,
        silent_payment_form=silent_payment_form,
        silent_payment_scan_form=silent_payment_scan_form,
        silent_payment_scan_result=silent_payment_scan_result,
        success_message="Experimental Silent Payments transaction lookup completed for the selected block height.",
    )


@app.post("/bitcoin/sweep-preview")
async def bitcoin_sweep_preview(
    request: Request,
    nostr_key: str = Form(""),
    destination_address: str = Form(""),
    fee_rate: str = Form("2.0"),
    transaction_limit: str = Form("5"),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    balance_form = {
        "nostr_key": nostr_key.strip(),
        "transaction_limit": transaction_limit.strip() or "5",
    }
    sweep_form = {
        "nostr_key": nostr_key.strip(),
        "destination_address": destination_address.strip(),
        "fee_rate": fee_rate.strip() or "2.0",
        "transaction_limit": transaction_limit.strip() or "5",
    }
    if not sweep_form["nostr_key"]:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            sweep_form=sweep_form,
            error_message="Enter an nsec before sweeping the wallet.",
            status_code=400,
        )

    try:
        tx_limit_value = int(balance_form["transaction_limit"])
    except ValueError:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            sweep_form=sweep_form,
            error_message="Transaction count must be an integer.",
            status_code=400,
        )
    if tx_limit_value <= 0:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            sweep_form=sweep_form,
            error_message="Transaction count must be greater than zero.",
            status_code=400,
        )

    try:
        _, _, balance_result, recent_transactions, silent_payment_result, silent_payment_form = await resolve_balance_page_data(
            sweep_form["nostr_key"],
            balance_form["transaction_limit"],
        )
        silent_payment_scan_form = await resolve_silent_payment_scan_form(
            sweep_form["nostr_key"],
            balance_form["transaction_limit"],
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            sweep_form=sweep_form,
            error_message=str(exc),
            silent_payment_scan_form=default_silent_payment_scan_form(),
            status_code=400,
        )

    if balance_result["input_kind"] != "nsec":
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message="Sweep Wallet requires an nsec so the Taproot transaction can be signed.",
            status_code=400,
        )

    try:
        fee_rate_value = float(sweep_form["fee_rate"])
    except ValueError:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message="Fee rate must be a number in sats/vbyte.",
            status_code=400,
        )

    try:
        sweep_preview = await asyncio.to_thread(
            create_p2tr_sweep_result,
            sweep_form["nostr_key"],
            sweep_form["destination_address"],
            fee_rate_value,
            BLOCKSTREAM_API_BASE,
            5.0,
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            error_message=str(exc),
            status_code=400,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        balance_form=balance_form,
        balance_result=balance_result,
        recent_transactions=recent_transactions,
        silent_payment_result=silent_payment_result,
        sweep_form=sweep_form,
        silent_payment_form=silent_payment_form,
        silent_payment_scan_form=silent_payment_scan_form,
        sweep_preview=sweep_preview,
        success_message="Signed sweep transaction preview created. Review it carefully before broadcasting.",
    )


@app.post("/bitcoin/sweep-broadcast")
async def bitcoin_sweep_broadcast(
    request: Request,
    nostr_key: str = Form(""),
    destination_address: str = Form(""),
    fee_rate: str = Form("2.0"),
    transaction_limit: str = Form("5"),
    tx_hex: str = Form(""),
    txid: str = Form(""),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    balance_form = {
        "nostr_key": nostr_key.strip(),
        "transaction_limit": transaction_limit.strip() or "5",
    }
    sweep_form = {
        "nostr_key": nostr_key.strip(),
        "destination_address": destination_address.strip(),
        "fee_rate": fee_rate.strip() or "2.0",
        "transaction_limit": transaction_limit.strip() or "5",
    }

    try:
        tx_limit_value = int(balance_form["transaction_limit"])
    except ValueError:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            sweep_form=sweep_form,
            error_message="Transaction count must be an integer.",
            status_code=400,
        )
    if tx_limit_value <= 0:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            sweep_form=sweep_form,
            error_message="Transaction count must be greater than zero.",
            status_code=400,
        )

    try:
        _, _, balance_result, recent_transactions, silent_payment_result, silent_payment_form = await resolve_balance_page_data(
            sweep_form["nostr_key"],
            balance_form["transaction_limit"],
        )
        silent_payment_scan_form = await resolve_silent_payment_scan_form(
            sweep_form["nostr_key"],
            balance_form["transaction_limit"],
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            sweep_form=sweep_form,
            error_message=str(exc),
            silent_payment_scan_form=default_silent_payment_scan_form(),
            status_code=400,
        )

    try:
        broadcast_txid = await asyncio.to_thread(broadcast_blockstream_transaction, tx_hex, BLOCKSTREAM_API_BASE, 10.0)
    except (click.ClickException, ControlEventError) as exc:
        sweep_preview = {
            "tx_hex": tx_hex,
            "txid": txid,
            "destination_address": sweep_form["destination_address"],
            "fee_rate": sweep_form["fee_rate"],
            "source_address": balance_result["p2tr"],
        }
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            sweep_preview=sweep_preview,
            error_message=str(exc),
            status_code=400,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        balance_form=balance_form,
        balance_result=balance_result,
        recent_transactions=recent_transactions,
        silent_payment_result=silent_payment_result,
        sweep_form=sweep_form,
        silent_payment_form=silent_payment_form,
        silent_payment_scan_form=silent_payment_scan_form,
        sweep_broadcast={"broadcast_txid": broadcast_txid, "txid": txid},
        success_message="Sweep transaction broadcast submitted successfully.",
    )


@app.post("/bitcoin/silent-payment/preview")
async def bitcoin_silent_payment_preview(
    request: Request,
    nostr_key: str = Form(""),
    txid: str = Form(""),
    destination_address: str = Form(""),
    fee_rate: str = Form("2.0"),
    transaction_limit: str = Form("5"),
    preview_target_id: str = Form(""),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    form_error_status_code = 200 if is_htmx_request(request) else 400
    silent_payment_form = {
        "nostr_key": nostr_key.strip(),
        "txid": txid.strip(),
        "destination_address": destination_address.strip(),
        "fee_rate": fee_rate.strip() or "2.0",
        "transaction_limit": transaction_limit.strip() or "5",
    }
    target_id = preview_target_id.strip()

    if is_htmx_request(request) and target_id:
        if not silent_payment_form["nostr_key"]:
            return render_silent_payment_preview_fragment(
                request,
                preview_target_id=target_id,
                silent_payment_form=silent_payment_form,
                error_message="Enter an nsec before searching for a Silent Payments receipt.",
                status_code=form_error_status_code,
            )
        try:
            fee_rate_value = float(silent_payment_form["fee_rate"])
        except ValueError:
            return render_silent_payment_preview_fragment(
                request,
                preview_target_id=target_id,
                silent_payment_form=silent_payment_form,
                error_message="Fee rate must be a number in sats/vbyte.",
                status_code=form_error_status_code,
            )

        try:
            silent_payment_preview = await asyncio.to_thread(
                create_silent_payment_sweep_result,
                silent_payment_form["nostr_key"],
                silent_payment_form["txid"],
                silent_payment_form["destination_address"],
                fee_rate_value,
                BLOCKSTREAM_API_BASE,
                5.0,
                None,
            )
        except (click.ClickException, ControlEventError) as exc:
            return render_silent_payment_preview_fragment(
                request,
                preview_target_id=target_id,
                silent_payment_form=silent_payment_form,
                error_message=str(exc),
                status_code=form_error_status_code,
            )

        return render_silent_payment_preview_fragment(
            request,
            preview_target_id=target_id,
            silent_payment_form=silent_payment_form,
            silent_payment_preview=silent_payment_preview,
            success_message="Signed sweep preview created. Review it carefully before broadcasting.",
        )

    balance_form = {
        "nostr_key": nostr_key.strip(),
        "transaction_limit": transaction_limit.strip() or "5",
    }

    if not silent_payment_form["nostr_key"]:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            silent_payment_form=silent_payment_form,
            silent_payment_error="Enter an nsec before searching for a Silent Payments receipt.",
            status_code=form_error_status_code,
        )

    try:
        _, sweep_form, balance_result, recent_transactions, silent_payment_result, _ = await resolve_balance_page_data(
            silent_payment_form["nostr_key"],
            balance_form["transaction_limit"],
        )
        silent_payment_scan_form = await resolve_silent_payment_scan_form(
            silent_payment_form["nostr_key"],
            balance_form["transaction_limit"],
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=default_silent_payment_scan_form(),
            silent_payment_error=str(exc),
            status_code=form_error_status_code,
        )

    if balance_result["input_kind"] != "nsec":
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            silent_payment_error="Silent Payments receipt search and sweep requires an nsec so the receipt can be validated and signed.",
            status_code=form_error_status_code,
        )

    try:
        fee_rate_value = float(silent_payment_form["fee_rate"])
    except ValueError:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            silent_payment_error="Fee rate must be a number in sats/vbyte.",
            status_code=form_error_status_code,
        )

    try:
        silent_payment_preview = await asyncio.to_thread(
            create_silent_payment_sweep_result,
            silent_payment_form["nostr_key"],
            silent_payment_form["txid"],
            silent_payment_form["destination_address"],
            fee_rate_value,
            BLOCKSTREAM_API_BASE,
            5.0,
            None,
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            silent_payment_error=str(exc),
            status_code=form_error_status_code,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        balance_form=balance_form,
        balance_result=balance_result,
        recent_transactions=recent_transactions,
        silent_payment_result=silent_payment_result,
        sweep_form=sweep_form,
        silent_payment_form=silent_payment_form,
        silent_payment_scan_form=silent_payment_scan_form,
        silent_payment_preview=silent_payment_preview,
        silent_payment_success="Matched Silent Payments receipt and signed a sweep preview. Review it carefully before broadcasting.",
    )


@app.post("/bitcoin/silent-payment/broadcast")
async def bitcoin_silent_payment_broadcast(
    request: Request,
    nostr_key: str = Form(""),
    receipt_txid: str = Form(""),
    destination_address: str = Form(""),
    fee_rate: str = Form("2.0"),
    transaction_limit: str = Form("5"),
    tx_hex: str = Form(""),
    signed_txid: str = Form(""),
    preview_target_id: str = Form(""),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    form_error_status_code = 200 if is_htmx_request(request) else 400
    silent_payment_form = {
        "nostr_key": nostr_key.strip(),
        "txid": receipt_txid.strip(),
        "destination_address": destination_address.strip(),
        "fee_rate": fee_rate.strip() or "2.0",
        "transaction_limit": transaction_limit.strip() or "5",
    }
    target_id = preview_target_id.strip()

    if is_htmx_request(request) and target_id:
        try:
            broadcast_txid = await asyncio.to_thread(
                broadcast_blockstream_transaction,
                tx_hex,
                BLOCKSTREAM_API_BASE,
                10.0,
            )
        except (click.ClickException, ControlEventError) as exc:
            return render_silent_payment_preview_fragment(
                request,
                preview_target_id=target_id,
                silent_payment_form=silent_payment_form,
                silent_payment_preview={
                    "matched_txid": receipt_txid.strip(),
                    "destination_address": silent_payment_form["destination_address"],
                    "fee_rate": silent_payment_form["fee_rate"],
                    "tx_hex": tx_hex,
                    "txid": signed_txid,
                },
                error_message=str(exc),
                status_code=form_error_status_code,
            )

        return render_silent_payment_preview_fragment(
            request,
            preview_target_id=target_id,
            silent_payment_form=silent_payment_form,
            silent_payment_broadcast={
                "broadcast_txid": broadcast_txid,
                "receipt_txid": receipt_txid.strip(),
                "txid": signed_txid,
            },
            success_message="Silent Payments sweep transaction broadcast submitted successfully.",
        )

    balance_form = {
        "nostr_key": nostr_key.strip(),
        "transaction_limit": transaction_limit.strip() or "5",
    }

    try:
        _, sweep_form, balance_result, recent_transactions, silent_payment_result, _ = await resolve_balance_page_data(
            silent_payment_form["nostr_key"],
            balance_form["transaction_limit"],
        )
        silent_payment_scan_form = await resolve_silent_payment_scan_form(
            silent_payment_form["nostr_key"],
            balance_form["transaction_limit"],
        )
    except (click.ClickException, ControlEventError) as exc:
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=default_silent_payment_scan_form(),
            silent_payment_error=str(exc),
            status_code=form_error_status_code,
        )

    try:
        broadcast_txid = await asyncio.to_thread(
            broadcast_blockstream_transaction,
            tx_hex,
            BLOCKSTREAM_API_BASE,
            10.0,
        )
    except (click.ClickException, ControlEventError) as exc:
        try:
            fee_rate_value = float(silent_payment_form["fee_rate"])
            silent_payment_preview = await asyncio.to_thread(
                create_silent_payment_sweep_result,
                silent_payment_form["nostr_key"],
                silent_payment_form["txid"],
                silent_payment_form["destination_address"],
                fee_rate_value,
                BLOCKSTREAM_API_BASE,
                5.0,
                None,
            )
        except Exception:
            silent_payment_preview = {
                "matched_txid": receipt_txid,
                "destination_address": silent_payment_form["destination_address"],
                "fee_rate": silent_payment_form["fee_rate"],
                "tx_hex": tx_hex,
                "txid": signed_txid,
            }
        return render_bitcoin_balance_response(
            request,
            identity,
            balance_form=balance_form,
            balance_result=balance_result,
            recent_transactions=recent_transactions,
            silent_payment_result=silent_payment_result,
            sweep_form=sweep_form,
            silent_payment_form=silent_payment_form,
            silent_payment_scan_form=silent_payment_scan_form,
            silent_payment_preview=silent_payment_preview,
            silent_payment_error=str(exc),
            status_code=form_error_status_code,
        )

    return render_bitcoin_balance_response(
        request,
        identity,
        balance_form=balance_form,
        balance_result=balance_result,
        recent_transactions=recent_transactions,
        silent_payment_result=silent_payment_result,
        sweep_form=sweep_form,
        silent_payment_form=silent_payment_form,
        silent_payment_scan_form=silent_payment_scan_form,
        silent_payment_broadcast={"broadcast_txid": broadcast_txid, "receipt_txid": receipt_txid, "txid": signed_txid},
        silent_payment_success="Silent Payments sweep transaction broadcast submitted successfully.",
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/login")
async def login(
    request: Request,
    nsec: str = Form(...),
    bootstrap_relays: str = Form(""),
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    try:
        keys = resolve_keys(nsec.strip())
    except (click.ClickException, ControlEventError) as exc:
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(
            request,
            "login.html",
            template_context,
            status_code=400,
        )

    try:
        normalized_bootstrap_relays = await validate_relays(bootstrap_relays or configured_home_relays(), timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(
            request,
            "login.html",
            template_context,
            status_code=400,
        )

    normalized_nsec = keys.private_key_bech32()
    bootstrap_token = set_runtime_bootstrap_overrides(
        root_nsec=normalized_nsec,
        home_relays=normalized_bootstrap_relays,
    )
    try:
        profiles_index = await _async_load_profiles_index(load_user_config())
    except (click.ClickException, ControlEventError) as exc:
        reset_runtime_bootstrap_overrides(bootstrap_token)
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(
            request,
            "login.html",
            template_context,
            status_code=400,
        )
    finally:
        reset_runtime_bootstrap_overrides(bootstrap_token)

    if profiles_index is None:
        template_context["error_message"] = (
            "No relay-backed profile configuration was found for this nsec on the selected bootstrap relays. "
            "If this is meant to be a brand-new identity, use 'Generate New nsec'. "
            "If the identity already exists, specify the correct bootstrap relay(s)."
        )
        return templates.TemplateResponse(
            request,
            "login.html",
            template_context,
            status_code=400,
        )

    request.session[SESSION_ROOT_NSEC_KEY] = normalized_nsec
    request.session[SESSION_SIGNER_NSEC_KEY] = normalized_nsec
    request.session[SESSION_BOOTSTRAP_RELAYS_KEY] = normalized_bootstrap_relays
    request.session.pop(SESSION_PROFILE_KEY, None)
    return RedirectResponse(url="/", status_code=303)


@app.get("/logout")
async def logout_page(
    request: Request,
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    if not template_context["identity"].get("logged_in"):
        return templates.TemplateResponse(
            request,
            "login.html",
            template_context,
        )
    return templates.TemplateResponse(
        request,
        "logout_confirm.html",
        template_context,
    )


@app.post("/logout")
async def logout(
    request: Request,
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    request.session.pop(SESSION_ROOT_NSEC_KEY, None)
    request.session.pop(SESSION_SIGNER_NSEC_KEY, None)
    request.session.pop(SESSION_PROFILE_KEY, None)
    request.session.pop(SESSION_BOOTSTRAP_RELAYS_KEY, None)
    request.session.pop(SESSION_DEFAULT_RELAYS_KEY, None)
    template_context = await get_default_template_context(session_identity(request))
    template_context["success_message"] = "Logged out."
    return templates.TemplateResponse(
        request,
        "index.html",
        template_context,
    )


@app.post("/generate-login")
async def generate_login(
    request: Request,
    bootstrap_relays: str = Form(""),
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    try:
        normalized_bootstrap_relays = await validate_relays(bootstrap_relays or configured_home_relays(), timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(
            request,
            "login.html",
            template_context,
            status_code=400,
        )

    keys = Keys()
    generated_nsec = keys.private_key_bech32()
    bootstrap_token = set_runtime_bootstrap_overrides(
        root_nsec=generated_nsec,
        home_relays=normalized_bootstrap_relays,
    )
    try:
        await initialize_relay_backed_root(load_user_config())
    except (click.ClickException, ControlEventError) as exc:
        reset_runtime_bootstrap_overrides(bootstrap_token)
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(
            request,
            "login.html",
            template_context,
            status_code=400,
        )
    finally:
        reset_runtime_bootstrap_overrides(bootstrap_token)

    request.session[SESSION_ROOT_NSEC_KEY] = generated_nsec
    request.session[SESSION_SIGNER_NSEC_KEY] = generated_nsec
    request.session[SESSION_BOOTSTRAP_RELAYS_KEY] = normalized_bootstrap_relays
    request.session[SESSION_DEFAULT_RELAYS_KEY] = normalized_bootstrap_relays
    request.session.pop(SESSION_PROFILE_KEY, None)
    template_context = await get_default_template_context(session_identity(request))
    template_context["success_message"] = (
        "Generated a new nsec, initialized the new identity on the selected bootstrap relay(s), "
        "and started a session. You can use this same nsec and bootstrap relay set to log back in later."
    )
    template_context["generated_nsec"] = generated_nsec
    return templates.TemplateResponse(
        request,
        "login.html",
        template_context,
    )


@app.post("/profiles/create")
async def create_profile(
    request: Request,
    profile_name: str = Form(...),
    relays: str = Form(DEFAULT_RELAYS),
    signer_nsec: str = Form(""),
    allow_root_signer: str | None = Form(None),
    return_to: str = Form("/"),
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    identity = template_context["identity"]
    if not identity.get("logged_in"):
        return await render_profile_return_page(
            request,
            identity,
            return_to,
            error_message="You must log in with an nsec before creating a profile.",
            status_code=400,
        )

    provided_signer = signer_nsec.strip()
    if provided_signer and identity.get("root_nsec"):
        try:
            provided_keys = resolve_keys(provided_signer)
            root_keys = resolve_keys(identity["root_nsec"])
        except (click.ClickException, ControlEventError) as exc:
            return await render_profile_return_page(
                request,
                identity,
                return_to,
                error_message=str(exc),
                status_code=400,
            )

        if provided_keys.public_key_hex() == root_keys.public_key_hex() and allow_root_signer != "true":
            return await render_profile_return_page(
                request,
                identity,
                return_to,
                error_message=(
                    "Warning: the provided signer matches your root admin nsec. "
                    "The root key should normally remain separate from profile signer keys. "
                    "If you intentionally want to reuse it, confirm that choice in the profile form and submit again."
                ),
                status_code=400,
            )

    try:
        normalized_relays = await validate_relays(relays or DEFAULT_RELAYS, timeout=DEFAULT_QUERY_TIMEOUT)
        with session_bootstrap(identity):
            created_profile = await create_relay_backed_profile(
                profile_name=profile_name,
                relays=normalized_relays,
                config=load_user_config(),
                signer_nsec=signer_nsec,
                root_nsec=identity.get("root_nsec"),
                require_existing_profile=bool(provided_signer),
            )
    except ValueError as exc:
        return await render_profile_return_page(
            request,
            identity,
            return_to,
            error_message=str(exc),
            status_code=400,
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_profile_return_page(
            request,
            identity,
            return_to,
            error_message=str(exc),
            status_code=400,
        )

    request.session[SESSION_SIGNER_NSEC_KEY] = created_profile["signer_nsec"]
    request.session[SESSION_PROFILE_KEY] = created_profile["profile_name"]
    if created_profile["generated_signer"]:
        success_message = f"Created relay-backed profile '{created_profile['profile_name']}' and selected it for this session."
    else:
        success_message = f"Added existing profile '{created_profile['profile_name']}' to this root and selected it for this session."
    return await render_profile_return_page(
        request,
        session_identity(request),
        return_to,
        success_message=success_message,
        created_profile=created_profile,
    )


@app.post("/profiles/use")
async def use_profile(
    request: Request,
    profile: str = Form(...),
    return_to: str = Form("/"),
    template_context: dict[str, Any] = Depends(get_default_template_context),
):
    with session_bootstrap(template_context["identity"]):
        config = load_user_config()
        signer_nsec, signer_source = await resolve_profile_signer_nsec(profile, config)
    if signer_nsec is None:
        return await render_profile_return_page(
            request,
            template_context["identity"],
            return_to,
            error_message=f"No signer nsec is available for profile '{profile}'.",
            status_code=200 if is_htmx_request(request) else 400,
        )

    try:
        keys = resolve_keys(signer_nsec)
    except (click.ClickException, ControlEventError) as exc:
        return await render_profile_return_page(
            request,
            template_context["identity"],
            return_to,
            error_message=f"Profile '{profile}' signer is invalid: {exc}",
            status_code=200 if is_htmx_request(request) else 400,
        )

    request.session[SESSION_SIGNER_NSEC_KEY] = keys.private_key_bech32()
    request.session[SESSION_PROFILE_KEY] = profile
    template_context = await get_default_template_context(session_identity(request))
    template_context["success_message"] = (
        f"Switched to profile '{profile}' using {profile_switch_signer_source_label(signer_source)}."
    )
    return await render_profile_return_page(
        request,
        template_context["identity"],
        return_to,
        success_message=template_context["success_message"],
    )


@app.get("/profiles/edit")
async def edit_profile_page(
    request: Request,
    identity: dict[str, Any] = Depends(get_session_identity),
):
    if not identity.get("logged_in"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "You must log in with an nsec before editing a profile."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    if not identity.get("profile"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "Select a profile before editing its profile."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    with session_bootstrap(identity):
        relays = str((await relay_profile_config(identity["profile"])).get("relays") or DEFAULT_RELAYS)
        current_profile = await fetch_profile(
            relays=relays,
            pubkey_hex=identity["pubkey_hex"],
            timeout=DEFAULT_QUERY_TIMEOUT,
            ssl_disable_verify=False,
        ) or {}
    bitcoin_wallet = await build_bitcoin_wallet_context(identity)
    return await render_profile_edit_response(
        request,
        identity,
        relays,
        identity["profile"],
        profile_form_values(current_profile),
        compact_profile(current_profile),
        bitcoin_wallet=bitcoin_wallet,
    )


@app.post("/profiles/edit")
async def edit_profile_submit(
    request: Request,
    relays: str = Depends(normalize_relays_form),
    replace: str | None = Form(None),
    name: str = Form(""),
    display_name: str = Form(""),
    about: str = Form(""),
    address: str = Form(""),
    picture: str = Form(""),
    banner: str = Form(""),
    website: str = Form(""),
    nip05: str = Form(""),
    lud16: str = Form(""),
    lud06: str = Form(""),
    lei: str = Form(""),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    if not identity.get("logged_in"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "You must log in with an nsec before editing a profile."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    if not identity.get("profile"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "Select a profile before editing its profile."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    field_values = {
        "name": name,
        "display_name": display_name,
        "about": about,
        "address": address,
        "picture": picture,
        "banner": banner,
        "website": website,
        "nip05": nip05,
        "lud16": lud16,
        "lud06": lud06,
        "lei": lei,
    }

    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        if is_htmx_request(request):
            return render_profile_publish_response(
                request,
                current_profile=[],
                error_message=str(exc),
                status_code=400,
            )
        return await render_profile_edit_response(
            request,
            identity,
            relays,
            identity["profile"],
            field_values,
            [],
            error_message=str(exc),
            status_code=400,
        )

    try:
        with session_bootstrap(identity):
            publish_result = await publish_profile_updates(
                relays=validated_relays,
                signer_nsec=identity["nsec"],
                field_values=field_values,
                replace=replace == "true",
                publish_wait=2.0,
                query_timeout=DEFAULT_QUERY_TIMEOUT,
            )
    except (click.ClickException, ControlEventError) as exc:
        current_profile = await fetch_profile(
            relays=validated_relays,
            pubkey_hex=identity["pubkey_hex"],
            timeout=DEFAULT_QUERY_TIMEOUT,
            ssl_disable_verify=False,
        ) or {}
        if is_htmx_request(request):
            return render_profile_publish_response(
                request,
                current_profile=compact_profile(current_profile),
                error_message=str(exc),
                status_code=400,
            )
        return await render_profile_edit_response(
            request,
            identity,
            validated_relays,
            identity["profile"],
            field_values,
            compact_profile(current_profile),
            error_message=str(exc),
            status_code=400,
        )

    latest_profile = publish_result["latest_content"] or publish_result["published_content"]
    if is_htmx_request(request):
        return render_profile_publish_response(
            request,
            current_profile=compact_profile(latest_profile),
            publish_result=publish_result,
            success_message="Published updated profile.",
        )
    return await render_profile_edit_response(
        request,
        identity,
        validated_relays,
        identity["profile"],
        profile_form_values(latest_profile),
        compact_profile(latest_profile),
        success_message="Published updated profile.",
        publish_result=publish_result,
    )


@app.post("/profiles/bitcoin/send-preview")
async def bitcoin_send_preview(
    request: Request,
    destination_address: str = Form(""),
    amount_sats: str = Form(""),
    fee_rate: str = Form("2.0"),
    change_address: str = Form(""),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    if not identity.get("logged_in"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "You must log in with an nsec before spending Bitcoin."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    if not identity.get("profile"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "Select a profile before spending Bitcoin."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    spend_form = {
        "destination_address": destination_address.strip(),
        "amount_sats": amount_sats.strip(),
        "fee_rate": fee_rate.strip() or "2.0",
        "change_address": change_address.strip(),
    }

    with session_bootstrap(identity):
        relays = str((await relay_profile_config(identity["profile"])).get("relays") or DEFAULT_RELAYS)
        current_profile = await fetch_profile(
            relays=relays,
            pubkey_hex=identity["pubkey_hex"],
            timeout=DEFAULT_QUERY_TIMEOUT,
            ssl_disable_verify=False,
        ) or {}

    try:
        amount_value = int(spend_form["amount_sats"])
    except ValueError:
        return await render_profile_edit_response(
            request, identity, relays, identity["profile"], profile_form_values(current_profile), compact_profile(current_profile),
            error_message="Amount must be an integer number of sats.", spend_form=spend_form, status_code=400,
        )

    try:
        fee_rate_value = float(spend_form["fee_rate"])
    except ValueError:
        return await render_profile_edit_response(
            request, identity, relays, identity["profile"], profile_form_values(current_profile), compact_profile(current_profile),
            error_message="Fee rate must be a number in sats/vbyte.", spend_form=spend_form, status_code=400,
        )

    try:
        spend_preview = await asyncio.to_thread(
            create_p2tr_send_result,
            identity["nsec"],
            spend_form["destination_address"],
            amount_value,
            fee_rate_value,
            BLOCKSTREAM_API_BASE,
            spend_form["change_address"] or None,
            5.0,
        )
    except (click.ClickException, ControlEventError) as exc:
        return await render_profile_edit_response(
            request, identity, relays, identity["profile"], profile_form_values(current_profile), compact_profile(current_profile),
            error_message=str(exc), spend_form=spend_form, status_code=400,
        )

    return await render_profile_edit_response(
        request, identity, relays, identity["profile"], profile_form_values(current_profile), compact_profile(current_profile),
        success_message="Signed Taproot transaction preview created. Review it carefully before broadcasting.",
        spend_form=spend_form, spend_preview=spend_preview,
    )


@app.post("/profiles/bitcoin/send-broadcast")
async def bitcoin_send_broadcast(
    request: Request,
    destination_address: str = Form(""),
    amount_sats: str = Form(""),
    fee_rate: str = Form("2.0"),
    change_address: str = Form(""),
    tx_hex: str = Form(""),
    txid: str = Form(""),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    if not identity.get("logged_in"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "You must log in with an nsec before spending Bitcoin."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    if not identity.get("profile"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "Select a profile before spending Bitcoin."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    spend_form = {
        "destination_address": destination_address.strip(),
        "amount_sats": amount_sats.strip(),
        "fee_rate": fee_rate.strip() or "2.0",
        "change_address": change_address.strip(),
    }

    with session_bootstrap(identity):
        relays = str((await relay_profile_config(identity["profile"])).get("relays") or DEFAULT_RELAYS)
        current_profile = await fetch_profile(
            relays=relays,
            pubkey_hex=identity["pubkey_hex"],
            timeout=DEFAULT_QUERY_TIMEOUT,
            ssl_disable_verify=False,
        ) or {}

    try:
        broadcast_txid = await asyncio.to_thread(broadcast_blockstream_transaction, tx_hex, BLOCKSTREAM_API_BASE, 10.0)
    except (click.ClickException, ControlEventError) as exc:
        spend_preview = {"tx_hex": tx_hex, "txid": txid, "destination_address": spend_form["destination_address"], "amount_sats": spend_form["amount_sats"], "fee_rate": spend_form["fee_rate"], "change_address": spend_form["change_address"]}
        return await render_profile_edit_response(
            request, identity, relays, identity["profile"], profile_form_values(current_profile), compact_profile(current_profile),
            error_message=str(exc), spend_form=spend_form, spend_preview=spend_preview, status_code=400,
        )

    spend_broadcast = {
        "broadcast_txid": broadcast_txid,
        "txid": txid,
    }
    return await render_profile_edit_response(
        request, identity, relays, identity["profile"], profile_form_values(current_profile), compact_profile(current_profile),
        success_message="Taproot transaction broadcast submitted successfully.",
        spend_form=spend_form, spend_broadcast=spend_broadcast,
    )


@app.post("/api/nobj-from-upload")
async def nobj_from_upload(request: Request, file: UploadFile = File(...)) -> dict[str, Any]:
    upload = await hash_uploaded_file(file)
    query_share = qr_context_for_digest(request, upload.digest)
    return {
        "filename": upload.filename,
        "size_bytes": upload.size_bytes,
        "sha256": upload.digest,
        "nobj": digest_to_nobj(upload.digest),
        "media_preview": upload.media_preview,
        **query_share,
    }


@app.get("/api/upload-preview/{token}")
async def uploaded_media_preview(token: str):
    remove_stale_media_previews()
    if not MEDIA_PREVIEW_TOKEN_PATTERN.fullmatch(token):
        raise HTTPException(status_code=404, detail="Media preview not found.")
    matches = [path for path in MEDIA_PREVIEW_DIR.glob(f"{token}.*") if path.is_file()]
    if not matches:
        raise HTTPException(status_code=404, detail="Media preview not found.")
    path = matches[0]
    media_type = media_type_from_preview_path(path)
    if media_type is None:
        raise HTTPException(status_code=404, detail="Media preview not found.")
    return FileResponse(
        path,
        media_type=media_type,
        headers={
            "Cache-Control": "no-store",
            "Content-Disposition": "inline",
        },
    )


@app.post("/api/query-etr-from-upload")
async def query_etr_from_upload(
    request: Request,
    file: UploadFile = File(...),
    relays: str = Depends(normalize_relays_form),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    try:
        upload = await hash_uploaded_file(file)
    except HTTPException as exc:
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = str(exc.detail)
        return templates.TemplateResponse(request, "index.html", template_context, status_code=exc.status_code)
    query_context = await build_query_etr_result(
        digest=upload.digest,
        relays=validated_relays,
        author_pubkey_hex=identity["pubkey_hex"],
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    return templates.TemplateResponse(
        request,
        "query_etr_result.html",
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "available_profiles": await get_available_profiles(identity),
            "filename": upload.filename,
            "size_bytes": upload.size_bytes,
            "sha256": upload.digest,
            "object_id": format_object_identifier(upload.digest),
            "relays": validated_relays,
            "query": query_context,
            "media_preview": upload.media_preview,
            **qr_context_for_digest(request, upload.digest),
        },
    )


@app.post("/api/issue-etr-from-upload")
async def issue_etr_from_upload(
    request: Request,
    file: UploadFile | None = File(None),
    relays: str = Depends(normalize_relays_form),
    comment: str = Form(""),
    file_digest: str = Form(""),
    file_name: str = Form(""),
    file_size: int = Form(0),
    store_upload: str | None = Form(None),
    identity: dict[str, Any] = Depends(get_session_identity),
):
    should_store_upload = parse_optional_checkbox(store_upload)
    try:
        validated_relays = await validate_relays(relays, timeout=DEFAULT_QUERY_TIMEOUT)
    except (click.ClickException, ControlEventError) as exc:
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = str(exc)
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    if not identity.get("logged_in"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "You must log in with an nsec before issuing an ETR."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    if not identity.get("profile"):
        template_context = await get_default_template_context(identity)
        template_context["error_message"] = "Select a profile before issuing an ETR."
        return templates.TemplateResponse(request, "index.html", template_context, status_code=400)

    confirmation = request.query_params.get("confirm") == "true"
    if file is not None:
        try:
            upload = await hash_uploaded_file(file, retain_content=should_store_upload)
        except HTTPException as exc:
            template_context = await get_default_template_context(identity)
            template_context["error_message"] = str(exc.detail)
            return templates.TemplateResponse(request, "index.html", template_context, status_code=exc.status_code)
        filename = upload.filename
        size_bytes = upload.size_bytes
        digest = upload.digest
        media_preview = upload.media_preview
        blossom_storage = None
    else:
        if not confirmation or not file_digest or not file_name or file_size <= 0:
            template_context = await get_default_template_context(identity)
            template_context["error_message"] = "A file upload is required unless you are confirming a guarded issue flow."
            return templates.TemplateResponse(request, "index.html", template_context, status_code=400)
        try:
            digest = normalize_object_identifier(file_digest.strip())
        except click.ClickException as exc:
            template_context = await get_default_template_context(identity)
            template_context["error_message"] = str(exc)
            return templates.TemplateResponse(request, "index.html", template_context, status_code=400)
        filename = file_name
        size_bytes = file_size
        media_preview = None
        blossom_storage = None

    guard = await evaluate_issue_etr_guard(
        relays=validated_relays,
        digest=digest,
        author_pubkey_hex=identity["pubkey_hex"],
        query_timeout=DEFAULT_QUERY_TIMEOUT,
        limit=DEFAULT_LIMIT,
    )
    if guard["should_warn"] and not confirmation:
        existing_issuer_profile = []
        if guard.get("latest_issuer_hex"):
            existing_issuer_profile = compact_profile(
                await fetch_profile(
                    relays=relays,
                    pubkey_hex=guard["latest_issuer_hex"],
                    timeout=DEFAULT_QUERY_TIMEOUT,
                    ssl_disable_verify=False,
                )
            )
        return templates.TemplateResponse(
            request,
            "issue_etr_confirm.html",
            {
                "app_title": APP_TITLE,
                "site_url": SITE_URL,
                "git_commit": GIT_COMMIT,
                "identity": identity,
                "available_profiles": await get_available_profiles(identity),
                "filename": filename,
                "size_bytes": size_bytes,
                "sha256": digest,
                "object_id": format_object_identifier(digest),
                "relays": validated_relays,
                "comment": comment.strip(),
                "guard": guard,
                "existing_issuer_profile": existing_issuer_profile,
            },
        )
    if file is not None:
        blossom_storage = await maybe_store_on_blossom(
            upload,
            should_store_upload,
            signer_nsec=identity["nsec"],
        )

    issue_result = await publish_issue_etr(
        filename=filename,
        size_bytes=size_bytes,
        digest=digest,
        relays=validated_relays,
        signer_nsec=identity["nsec"],
        comment=comment.strip() or None,
    )
    query_context = await build_query_etr_result(
        digest=issue_result["sha256"],
        relays=validated_relays,
        author_pubkey_hex=identity["pubkey_hex"],
    )
    await enrich_query_controller_profile_for_identity(query_context, identity)
    return templates.TemplateResponse(
        request,
        "query_etr_result.html",
        {
            "app_title": APP_TITLE,
            "site_url": SITE_URL,
            "git_commit": GIT_COMMIT,
            "identity": identity,
            "available_profiles": await get_available_profiles(identity),
            "filename": issue_result["filename"],
            "size_bytes": issue_result["size_bytes"],
            "sha256": issue_result["sha256"],
            "object_id": issue_result["object_id"],
            "relays": validated_relays,
            "query": query_context,
            "issue_result": issue_result,
            "media_preview": media_preview,
            "blossom_storage": blossom_storage,
            **qr_context_for_digest(request, issue_result["sha256"]),
        },
    )
