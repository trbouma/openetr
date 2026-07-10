from __future__ import annotations

import click
from monstr.encrypt import Keys

from openetr.config import (
    DEFAULT_RELAYS,
    DEFAULT_QUERY_TIMEOUT,
    ProfileConfigRecord,
    ProfilesIndexRecord,
    _async_load_profiles_index,
    _async_store_profile_record,
    _async_store_profile_secret,
    _async_store_profiles_index,
)
from openetr.helpers import format_pubkey, resolve_keys
from openetr.services.query_etr import fetch_profile


async def initialize_relay_backed_root(config: dict) -> ProfilesIndexRecord:
    existing_index = await _async_load_profiles_index(config)
    if existing_index is not None:
        return existing_index

    index = ProfilesIndexRecord(active_profile="default", profiles=[])
    await _async_store_profiles_index(index, config)
    return index


async def create_relay_backed_profile(
    profile_name: str,
    relays: str | None,
    config: dict,
    signer_nsec: str | None = None,
    root_nsec: str | None = None,
    require_existing_profile: bool = False,
) -> dict:
    normalized_name = profile_name.strip()
    if not normalized_name:
        raise ValueError("profile name must not be empty")

    existing_index = await _async_load_profiles_index(config)
    current_profiles = sorted(existing_index.profiles) if existing_index else []
    active_profile = existing_index.active_profile if existing_index else "default"

    if normalized_name in current_profiles:
        raise ValueError(f"profile '{normalized_name}' already exists")

    provided_signer = (signer_nsec or "").strip()
    if provided_signer:
        try:
            signer_keys = resolve_keys(provided_signer)
        except click.ClickException as exc:
            raise ValueError(str(exc)) from exc
        stored_signer_nsec = signer_keys.private_key_bech32()
        generated_signer = False
    else:
        signer_keys = Keys()
        stored_signer_nsec = signer_keys.private_key_bech32()
        generated_signer = True

    resolved_relays = (relays or DEFAULT_RELAYS).strip() or DEFAULT_RELAYS
    existing_profile = None
    if require_existing_profile:
        existing_profile = await fetch_profile(
            relays=resolved_relays,
            pubkey_hex=signer_keys.public_key_hex(),
            timeout=DEFAULT_QUERY_TIMEOUT,
            ssl_disable_verify=False,
        )
        if not existing_profile:
            raise ValueError(
                f"no published profile was found for signer {signer_keys.public_key_bech32()} on {resolved_relays}"
            )

    await _async_store_profile_secret(normalized_name, stored_signer_nsec, config)
    await _async_store_profile_record(
        normalized_name,
        ProfileConfigRecord(
            profile=normalized_name,
            relays=resolved_relays,
        ).model_dump(exclude_none=True),
        config,
    )

    updated_profiles = sorted({*current_profiles, normalized_name})
    await _async_store_profiles_index(
        ProfilesIndexRecord(
            active_profile=active_profile,
            profiles=updated_profiles,
        ),
        config,
    )

    return {
        "profile_name": normalized_name,
        "signer_nsec": stored_signer_nsec,
        "signer_npub": signer_keys.public_key_bech32(),
        "signer_pubkey": format_pubkey(signer_keys.public_key_hex()),
        "relays": resolved_relays,
        "generated_signer": generated_signer,
        "existing_profile": existing_profile,
        "uses_root_signer": bool(root_nsec and stored_signer_nsec == resolve_keys(root_nsec).private_key_bech32()),
    }
