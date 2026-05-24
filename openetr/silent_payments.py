from __future__ import annotations

import hashlib
import json
import math
import socket
import ssl
import time
from urllib import error, parse, request

import bech32
import click
import secp256k1
from btclib.bip32 import BIP32KeyData, derive, rootxprv_from_seed
from monstr.encrypt import Keys
from btclib.script.script_pub_key import ScriptPubKey

from openetr.bitcoin import _estimate_signed_p2tr_vsize, build_signed_p2tr_transaction, confirmed_utxos_only, dust_threshold_for_script_pub_key, fetch_blockstream_address_utxos
from openetr.helpers import format_pubkey, normalize_nip05_identifier, resolve_author, resolve_keys

SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
BECH32M_CONST = 0x2BC830A3
SCAN_OUTPUT_SEARCH_LIMIT = 4096
SILENT_PAYMENT_SCAN_TAG = "nostr-sp/scan"
SILENT_PAYMENT_SPEND_TAG = "nostr-sp/spend"


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def tagged_hash(tag: str, payload: bytes) -> bytes:
    tag_hash = sha256(tag.encode("utf-8"))
    return sha256(tag_hash + tag_hash + payload)


def derive_compressed_pubkey(privkey_bytes: bytes) -> bytes:
    key = secp256k1.PrivateKey(privkey_bytes, raw=True)
    return key.pubkey.serialize(compressed=True)


def normalize_bip340_private_key(privkey_hex: str) -> tuple[bytes, bytes, bool]:
    scalar = int(privkey_hex, 16)
    if scalar <= 0 or scalar >= SECP256K1_ORDER:
        raise click.ClickException("private key is outside the valid secp256k1 scalar range")

    privkey_bytes = bytes.fromhex(privkey_hex)
    compressed_pubkey = derive_compressed_pubkey(privkey_bytes)
    if compressed_pubkey[0] == 0x02:
        return privkey_bytes, compressed_pubkey, False

    normalized_scalar = SECP256K1_ORDER - scalar
    normalized_bytes = normalized_scalar.to_bytes(32, "big")
    normalized_pubkey = derive_compressed_pubkey(normalized_bytes)
    if normalized_pubkey[0] != 0x02:
        raise click.ClickException("failed to normalize private key to the BIP-340 even-y representative")
    return normalized_bytes, normalized_pubkey, True


def bech32m_create_checksum(hrp: str, data: list[int]) -> list[int]:
    values = bech32.bech32_hrp_expand(hrp) + list(data)
    polymod = bech32.bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ BECH32M_CONST
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32m_encode(hrp: str, data: list[int]) -> str:
    combined = list(data) + bech32m_create_checksum(hrp, data)
    return hrp + "1" + "".join(bech32.CHARSET[d] for d in combined)


def encode_silent_payment_address(scan_pubkey: bytes, spend_pubkey: bytes, hrp: str = "sp", version: int = 0) -> str:
    if len(scan_pubkey) != 33 or len(spend_pubkey) != 33:
        raise click.ClickException("silent payment scan and spend public keys must be 33-byte compressed pubkeys")
    data = bech32.convertbits(scan_pubkey + spend_pubkey, 8, 5, True)
    return bech32m_encode(hrp, [version] + data)


def silent_payment_hrp(silent_payment_address: str) -> str:
    normalized = (silent_payment_address or "").strip().lower()
    if not normalized or "1" not in normalized:
        raise click.ClickException("silent payment address must be a valid bech32m string")
    hrp, _ = normalized.split("1", 1)
    if not hrp:
        raise click.ClickException("silent payment address is missing its human-readable prefix")
    return hrp


def normalize_nostr_key_input(nostr_key: str) -> tuple[str, str]:
    candidate = nostr_key.strip()
    if not candidate:
        raise click.ClickException("nostr key input cannot be empty")

    if candidate.startswith("nsec"):
        return candidate, "nsec"

    if candidate.startswith("npub"):
        return candidate, "npub"

    nip05_candidate = normalize_nip05_identifier(candidate)
    if "@" in nip05_candidate:
        return format_pubkey(resolve_author(nip05_candidate)), "nip05"

    raise click.ClickException("input must be a valid nsec, npub, or NIP-05 identifier")


def _derive_tweak_scalar(base_pubkey: bytes, tag: str) -> int:
    tweak_int = int.from_bytes(tagged_hash(tag, base_pubkey), "big") % SECP256K1_ORDER
    if tweak_int == 0:
        raise click.ClickException(f"{tag} derivation produced an invalid zero tweak")
    return tweak_int


def _tweak_pubkey(base_pubkey: bytes, tweak_scalar: int) -> bytes:
    pubkey = secp256k1.PublicKey(base_pubkey, raw=True)
    return pubkey.tweak_add(tweak_scalar.to_bytes(32, "big")).serialize(compressed=True)


def derive_bip352_wallet_silent_payment_material(
    seed_bytes: bytes,
    hrp: str = "sp",
    coin_type: int = 0,
) -> dict[str, str]:
    master_xprv = rootxprv_from_seed(seed_bytes)
    account_path = f"m/352h/{coin_type}h/0h"
    spend_path = f"{account_path}/0h/0"
    scan_path = f"{account_path}/1h/0"
    spend_xprv = derive(master_xprv, spend_path)
    scan_xprv = derive(master_xprv, scan_path)
    spend_data = BIP32KeyData.b58decode(spend_xprv)
    scan_data = BIP32KeyData.b58decode(scan_xprv)
    spend_privkey_bytes = spend_data.key[1:]
    scan_privkey_bytes = scan_data.key[1:]
    spend_pubkey = derive_compressed_pubkey(spend_privkey_bytes)
    scan_pubkey = derive_compressed_pubkey(scan_privkey_bytes)
    return {
        "bip352_master_xprv": master_xprv,
        "bip352_account_path": account_path,
        "bip352_spend_path": spend_path,
        "bip352_scan_path": scan_path,
        "bip352_spend_xprv": spend_xprv,
        "bip352_scan_xprv": scan_xprv,
        "bip352_spend_public_key_hex": spend_pubkey.hex(),
        "bip352_scan_public_key_hex": scan_pubkey.hex(),
        "bip352_silent_payment_address": encode_silent_payment_address(scan_pubkey, spend_pubkey, hrp=hrp),
    }


def derive_silent_payment_material(nostr_key: str, hrp: str = "sp") -> dict[str, str]:
    normalized_input, input_kind = normalize_nostr_key_input(nostr_key)
    keys = resolve_keys(normalized_input) if input_kind == "nsec" else Keys(pub_k=normalized_input)
    npub = keys.public_key_bech32()
    privkey_hex = keys.private_key_hex()
    warning = ""
    bip340_normalized = "no"
    bip352_wallet_material: dict[str, str] = {
        "bip352_master_xprv": "",
        "bip352_account_path": "",
        "bip352_spend_path": "",
        "bip352_scan_path": "",
        "bip352_spend_xprv": "",
        "bip352_scan_xprv": "",
        "bip352_spend_public_key_hex": "",
        "bip352_scan_public_key_hex": "",
        "bip352_silent_payment_address": "",
    }

    if privkey_hex is not None:
        raw_privkey_bytes = bytes.fromhex(privkey_hex)
        base_privkey_bytes, base_pubkey, normalized = normalize_bip340_private_key(privkey_hex)
        bip340_normalized = "yes" if normalized else "no"
        base_scalar = int.from_bytes(base_privkey_bytes, "big")
        bip352_wallet_material = derive_bip352_wallet_silent_payment_material(raw_privkey_bytes, hrp=hrp)
        if normalized:
            warning = (
                "nsec input was normalized to the BIP-340 even-y representative before deriving Silent Payments "
                "scan and spend keys. The wallet-compatible BIP352 address below is derived separately from the raw nsec bytes."
            )
    else:
        pubkey_hex = keys.public_key_hex()
        if pubkey_hex is None:
            raise click.ClickException("input must be a valid nsec or npub key")
        base_pubkey = b"\x02" + bytes.fromhex(pubkey_hex)
        base_scalar = None
        warning = (
            "npub input derives Silent Payments public keys only. Private scan and spend keys are unavailable "
            "without the matching nsec."
        )

    scan_tweak = _derive_tweak_scalar(base_pubkey, SILENT_PAYMENT_SCAN_TAG)
    spend_tweak = _derive_tweak_scalar(base_pubkey, SILENT_PAYMENT_SPEND_TAG)
    scan_pubkey = _tweak_pubkey(base_pubkey, scan_tweak)
    spend_pubkey = _tweak_pubkey(base_pubkey, spend_tweak)

    scan_priv_hex = ""
    spend_priv_hex = ""
    if base_scalar is not None:
        scan_scalar = (base_scalar + scan_tweak) % SECP256K1_ORDER
        spend_scalar = (base_scalar + spend_tweak) % SECP256K1_ORDER
        if scan_scalar == 0 or spend_scalar == 0:
            raise click.ClickException("silent payment derivation produced an invalid zero private key")
        scan_priv_hex = scan_scalar.to_bytes(32, "big").hex()
        spend_priv_hex = spend_scalar.to_bytes(32, "big").hex()

    return {
        "input_value": nostr_key,
        "input_kind": input_kind,
        "npub": npub,
        "bip340_normalized": bip340_normalized,
        "base_public_key_hex": base_pubkey.hex(),
        "scan_private_key_hex": scan_priv_hex,
        "spend_private_key_hex": spend_priv_hex,
        "scan_public_key_hex": scan_pubkey.hex(),
        "spend_public_key_hex": spend_pubkey.hex(),
        "silent_payment_address": encode_silent_payment_address(scan_pubkey, spend_pubkey, hrp=hrp),
        "warning": warning,
        **bip352_wallet_material,
    }


def resolve_silent_payment_wallet_mode_material(
    nostr_key: str,
    mode: str = "nsw",
    hrp: str = "sp",
) -> dict[str, str]:
    normalized_mode = (mode or "nsw").strip().lower()
    if normalized_mode not in {"nsw", "bip352"}:
        raise click.ClickException("silent payment wallet mode must be either 'nsw' or 'bip352'")

    material = derive_silent_payment_material(nostr_key, hrp=hrp)
    if normalized_mode == "nsw":
        material["wallet_mode"] = "nsw"
        return material

    if material["input_kind"] != "nsec":
        raise click.ClickException("bip352 wallet mode requires an nsec so the wallet-compatible scan key is available")
    if not material["bip352_scan_xprv"] or not material["bip352_spend_xprv"]:
        raise click.ClickException("wallet-compatible BIP352 material is unavailable for this input")

    bip352_scan_data = BIP32KeyData.b58decode(material["bip352_scan_xprv"])
    bip352_spend_data = BIP32KeyData.b58decode(material["bip352_spend_xprv"])
    material = dict(material)
    material["wallet_mode"] = "bip352"
    material["scan_private_key_hex"] = bip352_scan_data.key[1:].hex()
    material["spend_private_key_hex"] = bip352_spend_data.key[1:].hex()
    material["scan_public_key_hex"] = material["bip352_scan_public_key_hex"]
    material["spend_public_key_hex"] = material["bip352_spend_public_key_hex"]
    material["silent_payment_address"] = material["bip352_silent_payment_address"]
    return material


def silent_payment_address_belongs_to_nostr_key(
    nostr_key: str,
    silent_payment_address: str,
) -> bool:
    normalized_address = (silent_payment_address or "").strip().lower()
    if not normalized_address:
        raise click.ClickException("silent payment address cannot be empty")

    expected = derive_silent_payment_material(
        nostr_key,
        hrp=silent_payment_hrp(normalized_address),
    )["silent_payment_address"].lower()
    return expected == normalized_address


def _script_type(script_hex: str) -> str:
    if script_hex.startswith("76a914") and script_hex.endswith("88ac") and len(script_hex) == 50:
        return "p2pkh"
    if script_hex.startswith("a914") and script_hex.endswith("87") and len(script_hex) == 46:
        return "p2sh"
    if script_hex.startswith("0014") and len(script_hex) == 44:
        return "p2wpkh"
    if script_hex.startswith("5120") and len(script_hex) == 68:
        return "p2tr"
    return "unknown"


def _normalize_script_type_name(script_type: str) -> str:
    normalized = script_type.strip().lower()
    aliases = {
        "v0_p2wpkh": "p2wpkh",
        "v1_p2tr": "p2tr",
        "v0_p2wsh": "p2wsh",
        "p2sh-p2wpkh": "p2sh",
    }
    return aliases.get(normalized, normalized)


def _outpoint_bytes(txid: str, vout: int) -> bytes:
    return bytes.fromhex(txid)[::-1] + int(vout).to_bytes(4, "little")


def _ser32(value: int) -> bytes:
    return int(value).to_bytes(4, "big")


def _compressed_pub_from_xonly(xonly_hex: str) -> bytes:
    xonly = bytes.fromhex(xonly_hex)
    if len(xonly) != 32:
        raise click.ClickException("x-only public key must be 32 bytes")
    return b"\x02" + xonly


def _xonly_pubkey_bytes(xonly_hex: str) -> bytes:
    xonly = bytes.fromhex(xonly_hex)
    if len(xonly) != 32:
        raise click.ClickException("x-only public key must be 32 bytes")
    return xonly


def _json_rpc_send(file_obj, message: dict[str, object]) -> None:
    file_obj.write((json.dumps(message) + "\n").encode("utf-8"))
    file_obj.flush()


def _json_rpc_readline(file_obj, timeout: float) -> dict[str, object]:
    raw = file_obj.readline()
    if not raw:
        raise click.ClickException("Frigate closed the JSON-RPC connection before completing the request")
    try:
        message = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Frigate returned invalid JSON-RPC data: {exc}") from exc
    if not isinstance(message, dict):
        raise click.ClickException("Frigate returned a non-object JSON-RPC message")
    return message


def _frigate_negotiate_version(file_obj, timeout: float) -> object:
    request_payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "server.version",
        "params": [
            "openetr 0.1",
            [
                "1.4",
                "1.6",
            ],
        ],
    }
    _json_rpc_send(file_obj, request_payload)
    response = _json_rpc_readline(file_obj, timeout)
    error_payload = response.get("error")
    if error_payload is not None:
        raise click.ClickException(f"Frigate server.version failed: {error_payload}")
    if response.get("id") != 0:
        raise click.ClickException("Frigate returned an unexpected response while negotiating the Electrum version")
    return response.get("result")


def frigate_server_features(
    host: str,
    port: int,
    use_ssl: bool = False,
    timeout: float = 10.0,
) -> dict[str, object]:
    request_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "server.features",
        "params": [],
    }
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            wrapped = ssl.create_default_context().wrap_socket(sock, server_hostname=host) if use_ssl else sock
            try:
                file_obj = wrapped.makefile("rwb")
                _frigate_negotiate_version(file_obj, timeout)
                _json_rpc_send(file_obj, request_payload)
                response = _json_rpc_readline(file_obj, timeout)
            finally:
                wrapped.close()
    except (OSError, ssl.SSLError) as exc:
        scheme = "ssl" if use_ssl else "tcp"
        raise click.ClickException(f"failed to connect to Frigate over {scheme}://{host}:{port}: {exc}") from exc

    error_payload = response.get("error")
    if error_payload is not None:
        raise click.ClickException(f"Frigate server.features failed: {error_payload}")
    result = response.get("result")
    if not isinstance(result, dict):
        raise click.ClickException("Frigate server.features returned an unexpected result payload")
    return result


def _validate_frigate_features(features: dict[str, object]) -> None:
    supported_versions = features.get("silent_payments")
    if not isinstance(supported_versions, list) or 0 not in supported_versions:
        raise click.ClickException("Frigate server does not advertise Silent Payments protocol version 0 support")


def frigate_scan_subscribe(
    scan_private_key_hex: str,
    spend_public_key_hex: str,
    start: int | str | None,
    host: str,
    port: int,
    use_ssl: bool = False,
    timeout: float = 30.0,
    labels: list[int] | None = None,
) -> dict[str, object]:
    features = frigate_server_features(host, port, use_ssl=use_ssl, timeout=timeout)
    _validate_frigate_features(features)

    subscribe_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "blockchain.silentpayments.subscribe",
        "params": [
            scan_private_key_hex,
            spend_public_key_hex,
            start,
            labels or [],
        ],
    }
    history_entries: list[dict[str, object]] = []
    progress_updates: list[float] = []
    subscription_result: object | None = None
    saw_notification = False
    notification_idle_timeout = min(timeout, 5.0)
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            wrapped = ssl.create_default_context().wrap_socket(sock, server_hostname=host) if use_ssl else sock
            try:
                file_obj = wrapped.makefile("rwb")
                _frigate_negotiate_version(file_obj, timeout)
                _json_rpc_send(file_obj, subscribe_payload)
                while True:
                    try:
                        message = _json_rpc_readline(
                            file_obj,
                            notification_idle_timeout if subscription_result is not None else timeout,
                        )
                    except TimeoutError:
                        if subscription_result is not None:
                            break
                        raise
                    except socket.timeout:
                        if subscription_result is not None:
                            break
                        raise
                    if message.get("id") == 2:
                        error_payload = message.get("error")
                        if error_payload is not None:
                            raise click.ClickException(f"Frigate subscription failed: {error_payload}")
                        result = message.get("result")
                        subscription_result = result
                        if isinstance(result, list):
                            for entry in result:
                                if isinstance(entry, dict):
                                    history_entries.append(entry)
                        continue

                    if message.get("method") != "blockchain.silentpayments.subscribe":
                        continue

                    saw_notification = True
                    params = message.get("params")
                    progress_value: float | None = None
                    history: object = None
                    if isinstance(params, list) and len(params) == 3:
                        _, progress, history = params
                        if isinstance(progress, (int, float)):
                            progress_value = float(progress)
                    elif isinstance(params, dict):
                        progress = params.get("progress")
                        history = params.get("history")
                        if isinstance(progress, (int, float)):
                            progress_value = float(progress)
                        subscription = params.get("subscription")
                        if isinstance(subscription, dict) and not isinstance(subscription_result, dict):
                            subscription_result = subscription
                    else:
                        continue

                    if progress_value is not None:
                        progress_updates.append(progress_value)

                    if isinstance(history, list):
                        for entry in history:
                            if isinstance(entry, dict):
                                history_entries.append(entry)

                    if progress_value == 1.0:
                        break
            finally:
                wrapped.close()
    except (OSError, ssl.SSLError) as exc:
        scheme = "ssl" if use_ssl else "tcp"
        raise click.ClickException(f"failed to complete Frigate scan over {scheme}://{host}:{port}: {exc}") from exc

    if subscription_result is None:
        raise click.ClickException("Frigate did not return a subscription result")

    if isinstance(subscription_result, dict):
        normalized_subscription: dict[str, object] = dict(subscription_result)
    else:
        normalized_subscription = {
            "address": "",
            "start_height": start,
            "labels": labels or [],
            "raw_result": subscription_result,
        }

    return {
        "features": features,
        "subscription": normalized_subscription,
        "progress_updates": progress_updates,
        "history": history_entries,
        "saw_notification": saw_notification,
    }


def frigate_debug_subscription(
    nostr_key: str,
    host: str,
    port: int,
    use_ssl: bool = False,
    timeout: float = 30.0,
    start: int | str | None = None,
    mode: str = "nsw",
    labels: list[int] | None = None,
) -> dict[str, object]:
    material = derive_silent_payment_material(nostr_key)
    if material["input_kind"] != "nsec":
        raise click.ClickException("Frigate debugging requires an nsec so the scan private key is available")

    modes: list[tuple[str, str, str, str]] = []
    if mode in {"nsw", "both"}:
        modes.append(
            (
                "nsw",
                material["silent_payment_address"],
                material["scan_private_key_hex"],
                material["spend_public_key_hex"],
            )
        )
    if mode in {"bip352", "both"}:
        if not material["bip352_scan_xprv"] or not material["bip352_spend_public_key_hex"]:
            raise click.ClickException("wallet-compatible BIP352 material is unavailable for this input")
        bip352_scan_data = BIP32KeyData.b58decode(material["bip352_scan_xprv"])
        bip352_scan_privkey_hex = bip352_scan_data.key[1:].hex()
        modes.append(
            (
                "bip352",
                material["bip352_silent_payment_address"],
                bip352_scan_privkey_hex,
                material["bip352_spend_public_key_hex"],
            )
        )

    results: list[dict[str, object]] = []
    for mode_name, address, scan_private_key_hex, spend_public_key_hex in modes:
        raw_messages: list[dict[str, object]] = []
        history_entries: list[dict[str, object]] = []
        progress_updates: list[float] = []
        subscription_result: object | None = None
        version_result: object | None = None
        features_result = frigate_server_features(host, port, use_ssl=use_ssl, timeout=timeout)
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                sock.settimeout(timeout)
                wrapped = ssl.create_default_context().wrap_socket(sock, server_hostname=host) if use_ssl else sock
                try:
                    file_obj = wrapped.makefile("rwb")

                    version_payload = {
                        "jsonrpc": "2.0",
                        "id": 0,
                        "method": "server.version",
                        "params": [
                            "openetr 0.1 debug",
                            ["1.4", "1.6"],
                        ],
                    }
                    _json_rpc_send(file_obj, version_payload)
                    version_response = _json_rpc_readline(file_obj, timeout)
                    raw_messages.append(version_response)
                    if version_response.get("error") is not None:
                        raise click.ClickException(f"Frigate server.version failed: {version_response['error']}")
                    version_result = version_response.get("result")

                    subscribe_payload = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "blockchain.silentpayments.subscribe",
                        "params": [
                            scan_private_key_hex,
                            spend_public_key_hex,
                            start,
                            labels or [],
                        ],
                    }
                    _json_rpc_send(file_obj, subscribe_payload)
                    while True:
                        try:
                            message = _json_rpc_readline(file_obj, min(timeout, 5.0) if subscription_result is not None else timeout)
                        except (TimeoutError, socket.timeout):
                            if subscription_result is not None:
                                break
                            raise
                        raw_messages.append(message)
                        if message.get("id") == 2:
                            if message.get("error") is not None:
                                raise click.ClickException(f"Frigate subscription failed: {message['error']}")
                            subscription_result = message.get("result")
                            if isinstance(subscription_result, list):
                                for entry in subscription_result:
                                    if isinstance(entry, dict):
                                        history_entries.append(entry)
                            continue
                        if message.get("method") != "blockchain.silentpayments.subscribe":
                            continue
                        params = message.get("params")
                        if not isinstance(params, list) or len(params) != 3:
                            continue
                        _, progress, history = params
                        if isinstance(progress, (int, float)):
                            progress_updates.append(float(progress))
                            if float(progress) == 1.0:
                                if isinstance(history, list):
                                    for entry in history:
                                        if isinstance(entry, dict):
                                            history_entries.append(entry)
                                break
                        if isinstance(history, list):
                            for entry in history:
                                if isinstance(entry, dict):
                                    history_entries.append(entry)
                finally:
                    wrapped.close()
        except (OSError, ssl.SSLError) as exc:
            scheme = "ssl" if use_ssl else "tcp"
            raise click.ClickException(f"failed to complete Frigate debug scan over {scheme}://{host}:{port}: {exc}") from exc

        results.append(
            {
                "mode": mode_name,
                "silent_payment_address": address,
                "scan_private_key_hex": scan_private_key_hex,
                "spend_public_key_hex": spend_public_key_hex,
                "version_result": version_result,
                "features_result": features_result,
                "subscription_result": subscription_result,
                "progress_updates": progress_updates,
                "history": history_entries,
                "raw_messages": raw_messages,
            }
        )

    return {
        "input_value": nostr_key,
        "npub": material["npub"],
        "host": host,
        "port": port,
        "use_ssl": use_ssl,
        "start": start,
        "labels": labels or [],
        "results": results,
    }


def _extract_input_pubkey(vin: dict[str, object]) -> bytes | None:
    prevout = vin.get("prevout")
    if not isinstance(prevout, dict):
        return None
    script_hex = str(prevout.get("scriptpubkey") or "")
    script_type = _normalize_script_type_name(str(prevout.get("scriptpubkey_type") or _script_type(script_hex)))
    witness = vin.get("witness") or []
    scriptsig_hex = str(vin.get("scriptsig") or "")

    if script_type == "p2wpkh":
        if isinstance(witness, list) and witness:
            pubkey_hex = str(witness[-1])
            pubkey = bytes.fromhex(pubkey_hex)
            if len(pubkey) == 33:
                return pubkey
        return None

    if script_type == "p2sh":
        redeem_hex = scriptsig_hex[2:] if scriptsig_hex.startswith("16") else scriptsig_hex
        if redeem_hex.startswith("0014") and isinstance(witness, list) and witness:
            pubkey_hex = str(witness[-1])
            pubkey = bytes.fromhex(pubkey_hex)
            if len(pubkey) == 33:
                return pubkey
        return None

    if script_type == "p2tr":
        if script_hex.startswith("5120"):
            return _compressed_pub_from_xonly(script_hex[4:])
        return None

    if script_type == "p2pkh":
        script_bytes = bytes.fromhex(scriptsig_hex)
        for idx in range(len(script_bytes), 32, -1):
            candidate = script_bytes[idx - 33:idx]
            if len(candidate) == 33 and candidate[0] in (0x02, 0x03):
                return candidate
        return None

    return None


def inspect_silent_payment_transaction(
    txid: str,
    api_base: str = "https://blockstream.info/api",
    timeout: float = 5.0,
) -> dict[str, object]:
    tx = fetch_blockstream_transaction(txid, api_base=api_base, timeout=timeout)
    vin = tx.get("vin")
    vout = tx.get("vout")
    if not isinstance(vin, list) or not isinstance(vout, list):
        raise click.ClickException("transaction payload is missing vin/vout arrays")

    inputs: list[dict[str, object]] = []
    extracted_pubkeys = 0
    for index, txin in enumerate(vin):
        if not isinstance(txin, dict):
            continue
        prevout = txin.get("prevout")
        prevout_dict = prevout if isinstance(prevout, dict) else {}
        script_hex = str(prevout_dict.get("scriptpubkey") or "")
        script_type = _normalize_script_type_name(str(prevout_dict.get("scriptpubkey_type") or _script_type(script_hex)))
        witness = txin.get("witness") or []
        pubkey = _extract_input_pubkey(txin)
        notes: list[str] = []
        if not isinstance(prevout, dict):
            notes.append("missing prevout")
        if not witness:
            notes.append("no witness stack")
        if script_type == "p2sh" and not str(txin.get("scriptsig") or ""):
            notes.append("no scriptsig redeem data")
        if pubkey is None:
            notes.append("no eligible pubkey extracted")
        else:
            extracted_pubkeys += 1

        inputs.append(
            {
                "index": index,
                "txid": str(txin.get("txid") or ""),
                "vout": int(txin.get("vout", 0) or 0),
                "sequence": int(txin.get("sequence", 0) or 0),
                "prevout_script_type": script_type,
                "prevout_scriptpubkey": script_hex,
                "witness_items": len(witness) if isinstance(witness, list) else 0,
                "scriptsig_length": len(str(txin.get("scriptsig") or "")) // 2,
                "pubkey_extracted": pubkey is not None,
                "pubkey_hex": pubkey.hex() if pubkey is not None else "",
                "notes": notes,
            }
        )

    outputs: list[dict[str, object]] = []
    taproot_outputs = 0
    for index, output in enumerate(vout):
        if not isinstance(output, dict):
            continue
        script_hex = str(output.get("scriptpubkey") or "")
        script_type = _normalize_script_type_name(str(output.get("scriptpubkey_type") or _script_type(script_hex)))
        if script_type == "p2tr":
            taproot_outputs += 1
        outputs.append(
            {
                "index": index,
                "value": int(output.get("value", 0) or 0),
                "script_type": script_type,
                "scriptpubkey_address": str(output.get("scriptpubkey_address") or ""),
                "scriptpubkey": script_hex,
            }
        )

    return {
        "txid": str(tx.get("txid") or txid),
        "api_base": api_base.rstrip("/"),
        "status": tx.get("status") if isinstance(tx.get("status"), dict) else {},
        "input_count": len(inputs),
        "eligible_input_pubkeys": extracted_pubkeys,
        "taproot_output_count": taproot_outputs,
        "inputs": inputs,
        "outputs": outputs,
    }


def _combine_pubkeys(pubkeys: list[bytes]) -> bytes | None:
    if not pubkeys:
        return None
    try:
        pubkey_objects = [secp256k1.PublicKey(pubkey, raw=True) for pubkey in pubkeys]
        combined = secp256k1.PublicKey()
        combined.combine([pubkey.public_key for pubkey in pubkey_objects])
    except Exception:
        return None
    return combined.serialize(compressed=True)


def _get_input_hash(outpoint_bytes: list[bytes], summed_input_pubkey: bytes) -> bytes:
    lowest_outpoint = sorted(outpoint_bytes)[0]
    return tagged_hash("BIP0352/Inputs", lowest_outpoint + summed_input_pubkey)


def fetch_blockstream_transaction(
    txid: str,
    api_base: str = "https://blockstream.info/api",
    timeout: float = 5.0,
) -> dict[str, object]:
    url = f"{api_base.rstrip('/')}/tx/{parse.quote(txid)}"
    last_rate_limit_error: error.HTTPError | None = None
    for attempt in range(4):
        req = request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "openetr/0.1",
            },
        )
        try:
            with request.urlopen(req, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                last_rate_limit_error = exc
                retry_after = exc.headers.get("Retry-After") if exc.headers is not None else None
                try:
                    delay = float(retry_after) if retry_after else (1.5 * (2 ** attempt))
                except ValueError:
                    delay = 1.5 * (2 ** attempt)
                time.sleep(min(delay, 12.0))
                continue
            raise click.ClickException(
                f"Blockstream transaction lookup failed for {txid}: HTTP {exc.code}"
            ) from exc
        except error.URLError as exc:
            raise click.ClickException(
                f"Blockstream transaction lookup failed for {txid}: {exc.reason}"
            ) from exc
        except TimeoutError as exc:
            raise click.ClickException(
                f"Blockstream transaction lookup timed out for {txid}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise click.ClickException(
                f"Blockstream transaction lookup returned invalid JSON for {txid}"
            ) from exc
    else:
        raise click.ClickException(
            f"Blockstream transaction lookup failed for {txid}: HTTP 429 after multiple retries"
        ) from last_rate_limit_error
    if not isinstance(payload, dict):
        raise click.ClickException(f"Blockstream transaction lookup returned an unexpected payload for {txid}")
    return payload


def fetch_blockstream_tip_height(
    api_base: str = "https://blockstream.info/api",
    timeout: float = 5.0,
) -> int:
    url = f"{api_base.rstrip('/')}/blocks/tip/height"
    req = request.Request(
        url,
        headers={
            "Accept": "text/plain",
            "User-Agent": "openetr/0.1",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = response.read().decode("utf-8").strip()
    except error.HTTPError as exc:
        raise click.ClickException(
            f"Blockstream tip-height lookup failed: HTTP {exc.code}"
        ) from exc
    except error.URLError as exc:
        raise click.ClickException(
            f"Blockstream tip-height lookup failed: {exc.reason}"
        ) from exc
    except TimeoutError as exc:
        raise click.ClickException("Blockstream tip-height lookup timed out") from exc
    try:
        return int(payload)
    except ValueError as exc:
        raise click.ClickException("Blockstream tip-height lookup returned an invalid height") from exc


def fetch_blockstream_block_hash_for_height(
    height: int,
    api_base: str = "https://blockstream.info/api",
    timeout: float = 5.0,
) -> str:
    url = f"{api_base.rstrip('/')}/block-height/{height}"
    req = request.Request(
        url,
        headers={
            "Accept": "text/plain",
            "User-Agent": "openetr/0.1",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = response.read().decode("utf-8").strip()
    except error.HTTPError as exc:
        raise click.ClickException(
            f"Blockstream block-hash lookup failed for height {height}: HTTP {exc.code}"
        ) from exc
    except error.URLError as exc:
        raise click.ClickException(
            f"Blockstream block-hash lookup failed for height {height}: {exc.reason}"
        ) from exc
    except TimeoutError as exc:
        raise click.ClickException(
            f"Blockstream block-hash lookup timed out for height {height}"
        ) from exc
    if not payload:
        raise click.ClickException(f"Blockstream block-hash lookup returned an empty hash for height {height}")
    return payload


def fetch_blockstream_block_txids(
    block_hash: str,
    api_base: str = "https://blockstream.info/api",
    timeout: float = 5.0,
) -> list[str]:
    url = f"{api_base.rstrip('/')}/block/{parse.quote(block_hash)}/txids"
    req = request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "openetr/0.1",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise click.ClickException(
            f"Blockstream block txid lookup failed for {block_hash}: HTTP {exc.code}"
        ) from exc
    except error.URLError as exc:
        raise click.ClickException(
            f"Blockstream block txid lookup failed for {block_hash}: {exc.reason}"
        ) from exc
    except TimeoutError as exc:
        raise click.ClickException(
            f"Blockstream block txid lookup timed out for {block_hash}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise click.ClickException(
            f"Blockstream block txid lookup returned invalid JSON for {block_hash}"
        ) from exc
    if not isinstance(payload, list):
        raise click.ClickException(f"Blockstream block txid lookup returned an unexpected payload for {block_hash}")
    return [str(txid) for txid in payload if txid]


def collect_block_txids(
    api_base: str = "https://blockstream.info/api",
    start_blockheight: int | None = None,
    block_count: int = 1,
    timeout: float = 5.0,
) -> tuple[list[str], list[dict[str, object]]]:
    if block_count <= 0:
        raise click.ClickException("block_count must be a positive integer")

    tip_height = fetch_blockstream_tip_height(api_base=api_base, timeout=timeout)
    effective_start = tip_height if start_blockheight is None else start_blockheight
    if effective_start < 0:
        raise click.ClickException("start_blockheight must be zero or greater")
    if effective_start > tip_height:
        raise click.ClickException(
            f"start_blockheight {effective_start} is above the current tip height {tip_height}"
        )

    block_summaries: list[dict[str, object]] = []
    txids: list[str] = []
    for offset in range(block_count):
        height = effective_start - offset
        if height < 0:
            break
        block_hash = fetch_blockstream_block_hash_for_height(height, api_base=api_base, timeout=timeout)
        block_txids = fetch_blockstream_block_txids(block_hash, api_base=api_base, timeout=timeout)
        block_summaries.append(
            {
                "height": height,
                "block_hash": block_hash,
                "tx_count": len(block_txids),
            }
        )
        txids.extend(block_txids)
    return txids, block_summaries


def scan_silent_payment_transaction(
    nostr_key: str,
    tx: dict[str, object],
    mode: str = "nsw",
) -> dict[str, object]:
    material = resolve_silent_payment_wallet_mode_material(nostr_key, mode=mode)
    if not material["scan_private_key_hex"] or not material["spend_private_key_hex"]:
        raise click.ClickException("nsec input is required to scan Silent Payments receipts")

    vin = tx.get("vin")
    vout = tx.get("vout")
    if not isinstance(vin, list) or not isinstance(vout, list):
        raise click.ClickException("transaction payload is missing vin/vout arrays")

    input_pubkeys: list[bytes] = []
    outpoints: list[bytes] = []
    for txin in vin:
        if not isinstance(txin, dict):
            continue
        pubkey = _extract_input_pubkey(txin)
        if pubkey is None:
            continue
        txid = str(txin.get("txid") or "")
        vout_index = int(txin.get("vout", 0) or 0)
        if not txid:
            continue
        input_pubkeys.append(pubkey)
        outpoints.append(_outpoint_bytes(txid, vout_index))

    if not input_pubkeys or not outpoints:
        return {
            "txid": str(tx.get("txid", "")),
            "matched_outputs": [],
            "input_pubkey_count": 0,
            "warning": "No eligible input public keys were found for Silent Payments scanning.",
        }

    summed_input_pubkey = _combine_pubkeys(input_pubkeys)
    if summed_input_pubkey is None:
        return {
            "txid": str(tx.get("txid", "")),
            "matched_outputs": [],
            "input_pubkey_count": len(input_pubkeys),
            "warning": "Input public keys summed to an invalid point for Silent Payments scanning.",
        }

    scan_priv_bytes = bytes.fromhex(material["scan_private_key_hex"])
    spend_pubkey = bytes.fromhex(material["spend_public_key_hex"])
    input_hash = _get_input_hash(outpoints, summed_input_pubkey)
    input_hash_scalar = int.from_bytes(input_hash, "big") % SECP256K1_ORDER
    if input_hash_scalar == 0:
        return {
            "txid": str(tx.get("txid", "")),
            "matched_outputs": [],
            "input_pubkey_count": len(input_pubkeys),
            "warning": "Silent Payments input hash resolved to an invalid zero scalar.",
        }

    scan_priv_scalar = int.from_bytes(scan_priv_bytes, "big")
    shared_scalar = (input_hash_scalar * scan_priv_scalar) % SECP256K1_ORDER
    if shared_scalar == 0:
        return {
            "txid": str(tx.get("txid", "")),
            "matched_outputs": [],
            "input_pubkey_count": len(input_pubkeys),
            "warning": "Silent Payments shared secret resolved to an invalid zero scalar.",
        }

    summed_input_point = secp256k1.PublicKey(summed_input_pubkey, raw=True)
    ecdh_point = summed_input_point.tweak_mul(shared_scalar.to_bytes(32, "big"))
    ecdh_compressed = ecdh_point.serialize(compressed=True)

    remaining_outputs: dict[bytes, dict[str, object]] = {}
    for output in vout:
        if not isinstance(output, dict):
            continue
        script_hex = str(output.get("scriptpubkey") or "")
        script_type = _normalize_script_type_name(str(output.get("scriptpubkey_type") or _script_type(script_hex)))
        if script_type != "p2tr":
            continue
        remaining_outputs[_xonly_pubkey_bytes(script_hex[4:])] = output

    matched_outputs: list[dict[str, object]] = []
    warning = ""
    for k in range(SCAN_OUTPUT_SEARCH_LIMIT):
        if not remaining_outputs:
            break
        t_k = tagged_hash("BIP0352/SharedSecret", ecdh_compressed + _ser32(k))
        tweak_scalar = int.from_bytes(t_k, "big") % SECP256K1_ORDER
        if tweak_scalar == 0:
            continue
        derived_pubkey = (
            secp256k1.PublicKey(spend_pubkey, raw=True)
            .tweak_add(tweak_scalar.to_bytes(32, "big"))
            .serialize(compressed=True)
        )
        output = remaining_outputs.pop(derived_pubkey[1:], None)
        if output is not None:
            matched_outputs.append(
                {
                    "vout": int(output.get("vout", 0) or 0),
                    "value": int(output.get("value", 0) or 0),
                    "scriptpubkey_address": str(output.get("scriptpubkey_address") or ""),
                    "output_pubkey_hex": derived_pubkey.hex(),
                    "priv_key_tweak_hex": t_k.hex(),
                    "shared_secret_index": k,
                }
            )
    if remaining_outputs and not matched_outputs:
        warning = (
            "No matching Silent Payments outputs were found within the current scan window. "
            "A larger search window or fuller BIP-352 labeling support may be required."
        )

    return {
        "txid": str(tx.get("txid", "")),
        "matched_outputs": matched_outputs,
        "input_pubkey_count": len(input_pubkeys),
        "warning": warning,
    }


def scan_silent_payment_receipts(
    nostr_key: str,
    txids: list[str] | None = None,
    api_base: str = "https://blockstream.info/api",
    start_blockheight: int | None = None,
    block_count: int = 1,
    timeout: float = 5.0,
    frigate_host: str | None = None,
    frigate_port: int | None = None,
    frigate_ssl: bool = False,
    frigate_timeout: float = 120.0,
    mode: str = "nsw",
    discovery_only: bool = False,
) -> dict[str, object]:
    material = resolve_silent_payment_wallet_mode_material(nostr_key, mode=mode)
    if not material["scan_private_key_hex"] or not material["spend_private_key_hex"]:
        raise click.ClickException("nsec input is required to scan Silent Payments receipts")

    effective_txids = [txid for txid in (txids or []) if txid]
    block_summaries: list[dict[str, object]] = []
    scan_mode = "txids"
    frigate_result: dict[str, object] | None = None
    if frigate_host:
        effective_frigate_port = frigate_port or (50002 if frigate_ssl else 50001)
        if effective_frigate_port <= 0:
            raise click.ClickException("frigate_port must be a positive integer when frigate_host is provided")
        if effective_txids:
            raise click.ClickException("explicit --txid values cannot be combined with the Frigate scanning backend")
        if block_count <= 0:
            raise click.ClickException("block_count must be greater than zero")
        frigate_start: int | str | None
        if start_blockheight is None:
            frigate_start = None
        elif block_count == 1:
            frigate_start = start_blockheight
        else:
            range_end = max(start_blockheight - (block_count - 1), 0)
            frigate_start = f"{range_end}-{start_blockheight}"

        frigate_result = frigate_scan_subscribe(
            material["scan_private_key_hex"],
            material["spend_public_key_hex"],
            frigate_start,
            host=frigate_host,
            port=effective_frigate_port,
            use_ssl=frigate_ssl,
            timeout=frigate_timeout,
        )
        scan_mode = "frigate"
        seen_txids: set[str] = set()
        for entry in frigate_result["history"]:
            tx_hash = str(entry.get("tx_hash") or "")
            if tx_hash and tx_hash not in seen_txids:
                effective_txids.append(tx_hash)
                seen_txids.add(tx_hash)
    elif not effective_txids:
        scan_mode = "blocks"
        effective_txids, block_summaries = collect_block_txids(
            api_base=api_base,
            start_blockheight=start_blockheight,
            block_count=block_count,
            timeout=timeout,
        )

    scanned_transactions: list[dict[str, object]] = []
    frigate_history_by_txid: dict[str, list[dict[str, object]]] = {}
    if frigate_result is not None:
        for entry in frigate_result["history"]:
            tx_hash = str(entry.get("tx_hash") or "")
            if tx_hash:
                frigate_history_by_txid.setdefault(tx_hash, []).append(entry)
    if discovery_only:
        for txid in effective_txids:
            frigate_entries = frigate_history_by_txid.get(txid, [])
            scanned_transactions.append(
                {
                    "txid": txid,
                    "input_pubkey_count": 0,
                    "matched_outputs": [],
                    "warning": "",
                    "frigate_history": [
                        {
                            "height": int(entry.get("height", 0) or 0),
                            "tx_hash": str(entry.get("tx_hash") or ""),
                            "tweak_key": str(entry.get("tweak_key") or ""),
                        }
                        for entry in frigate_entries
                    ],
                }
            )
    else:
        for txid in effective_txids:
            tx = fetch_blockstream_transaction(txid, api_base=api_base, timeout=timeout)
            result = scan_silent_payment_transaction(nostr_key, tx, mode=mode)
            frigate_entries = frigate_history_by_txid.get(txid, [])
            if frigate_entries:
                result["frigate_history"] = [
                    {
                        "height": int(entry.get("height", 0) or 0),
                        "tx_hash": str(entry.get("tx_hash") or ""),
                        "tweak_key": str(entry.get("tweak_key") or ""),
                    }
                    for entry in frigate_entries
                ]
            scanned_transactions.append(result)

    response = {
        "input_value": nostr_key,
        "npub": material["npub"],
        "wallet_mode": material["wallet_mode"],
        "silent_payment_address": material["silent_payment_address"],
        "api_base": api_base.rstrip("/"),
        "scan_mode": scan_mode,
        "discovery_only": discovery_only,
        "block_summaries": block_summaries,
        "transactions": scanned_transactions,
    }
    if frigate_result is not None:
        subscription = frigate_result["subscription"]
        response["scan_source"] = (
            f"{'ssl' if frigate_ssl else 'tcp'}://{frigate_host}:{effective_frigate_port}"
        )
        response["frigate_features"] = frigate_result["features"]
        response["frigate_subscription"] = subscription
        response["frigate_progress_updates"] = frigate_result["progress_updates"]
    return response


def _silent_payment_output_private_key_hex(
    spend_private_key_hex: str,
    tweak_hex: str,
    output_pubkey_hex: str,
) -> str:
    spend_scalar = int(spend_private_key_hex, 16)
    tweak_scalar = int(tweak_hex, 16) % SECP256K1_ORDER
    if tweak_scalar == 0:
        raise click.ClickException("receipt tweak resolved to an invalid zero scalar")
    output_scalar = (spend_scalar + tweak_scalar) % SECP256K1_ORDER
    if output_scalar == 0:
        raise click.ClickException("receipt spend key resolved to an invalid zero scalar")
    if output_pubkey_hex.startswith("03"):
        output_scalar = (SECP256K1_ORDER - output_scalar) % SECP256K1_ORDER
        if output_scalar == 0:
            raise click.ClickException("receipt spend key normalization resolved to an invalid zero scalar")
    return output_scalar.to_bytes(32, "big").hex()


def create_silent_payment_sweep_result(
    nsec: str,
    txid: str,
    destination_address: str,
    fee_rate: float,
    api_base: str = "https://blockstream.info/api",
    timeout: float = 5.0,
    vout: int | None = None,
) -> dict[str, object]:
    material = derive_silent_payment_material(nsec)
    if not material["scan_private_key_hex"] or not material["spend_private_key_hex"]:
        raise click.ClickException("nsec input is required to sweep a Silent Payments receipt")

    scan_result = scan_silent_payment_receipts(
        nsec,
        [txid],
        api_base=api_base,
        timeout=timeout,
    )
    tx_result = scan_result["transactions"][0]
    matches = tx_result["matched_outputs"]
    if not matches:
        raise click.ClickException(f"no Silent Payments receipt was detected in transaction {txid}")

    selected_match: dict[str, object] | None = None
    if vout is not None:
        for match in matches:
            if int(match["vout"]) == vout:
                selected_match = match
                break
        if selected_match is None:
            raise click.ClickException(f"transaction {txid} does not contain a matched Silent Payments receipt at vout {vout}")
    elif len(matches) == 1:
        selected_match = matches[0]
    else:
        matched_vouts = ", ".join(str(match["vout"]) for match in matches)
        raise click.ClickException(
            f"transaction {txid} contains multiple matched Silent Payments receipts ({matched_vouts}); specify --vout"
        )

    source_address = str(selected_match["scriptpubkey_address"])
    source_vout = int(selected_match["vout"])
    all_address_utxos = fetch_blockstream_address_utxos(source_address, api_base=api_base, timeout=timeout)
    confirmed_utxos = confirmed_utxos_only(all_address_utxos)
    selected_utxos = [
        utxo
        for utxo in confirmed_utxos
        if str(utxo["txid"]) == txid and int(utxo["vout"]) == source_vout
    ]
    if not selected_utxos:
        matching_unconfirmed_utxos = [
            utxo
            for utxo in all_address_utxos
            if str(utxo["txid"]) == txid and int(utxo["vout"]) == source_vout
        ]
        if matching_unconfirmed_utxos:
            raise click.ClickException(
                f"matched Silent Payments output {txid}:{source_vout} exists but is not yet confirmed as an unspent output"
            )
        raise click.ClickException(
            f"matched Silent Payments output {txid}:{source_vout} appears to have already been spent"
        )

    if fee_rate <= 0:
        raise click.ClickException("fee_rate must be greater than zero")

    destination_spk = ScriptPubKey.from_address(destination_address)
    destination_dust_threshold = dust_threshold_for_script_pub_key(destination_spk)
    total_in = sum(int(utxo["value"]) for utxo in selected_utxos)
    fee_sats = math.ceil(
        _estimate_signed_p2tr_vsize(len(selected_utxos), [destination_spk]) * fee_rate
    )
    amount_sats = total_in - fee_sats
    if amount_sats <= 0:
        raise click.ClickException("insufficient funds to sweep the Silent Payments receipt at the requested fee rate")
    if amount_sats < destination_dust_threshold:
        raise click.ClickException(
            f"sweep amount {amount_sats} sats is dust for {destination_spk.type}; minimum supported amount is {destination_dust_threshold} sats"
        )

    receipt_private_key_hex = _silent_payment_output_private_key_hex(
        material["spend_private_key_hex"],
        str(selected_match["priv_key_tweak_hex"]),
        str(selected_match["output_pubkey_hex"]),
    )
    tx_build_result = build_signed_p2tr_transaction(
        receipt_private_key_hex,
        source_address,
        selected_utxos,
        destination_address,
        amount_sats,
        fee_rate,
        change_address=source_address,
    )
    tx_build_result["api_base"] = api_base.rstrip("/")
    tx_build_result["npub"] = material["npub"]
    tx_build_result["silent_payment_address"] = material["silent_payment_address"]
    tx_build_result["matched_txid"] = txid
    tx_build_result["matched_vout"] = source_vout
    tx_build_result["matched_value"] = int(selected_match["value"])
    tx_build_result["matched_tweak_hex"] = str(selected_match["priv_key_tweak_hex"])
    tx_build_result["matched_output_pubkey_hex"] = str(selected_match["output_pubkey_hex"])
    tx_build_result["matched_shared_secret_index"] = int(selected_match["shared_secret_index"])
    tx_build_result["sweep"] = True
    return tx_build_result
