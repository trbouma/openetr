from __future__ import annotations

import asyncio
from typing import Any

from monstr.client.client import ClientPool
from monstr.event.event import Event

from openetr.config import DEFAULT_KIND, DEFAULT_LIMIT, DEFAULT_QUERY_TIMEOUT
from openetr.control import (
    ACTION_ACCEPT,
    ACTION_ENCUMBER,
    ACTION_INITIATE,
    ACTION_TERMINATE,
    CONTROL_EVENT_KIND,
)
from openetr.services.control_guard_policy import (
    DEFAULT_CONTROL_GUARD_POLICY,
    ControlEventError,
    ControlGuardPolicy,
)
from openetr.helpers import (
    assert_hex_event_id,
    assert_hex_object_identifier,
    assert_hex_pubkey,
    format_object_identifier,
    format_pubkey,
    normalize_event_reference,
    resolve_keys,
)


def event_tag_value(event: Event, tag_name: str) -> str | None:
    values = event.get_tags_value(tag_name)
    return values[0] if values else None


def control_action_changes_controller(action: str | None) -> bool:
    return action == ACTION_INITIATE


def control_action_terminates(action: str | None) -> bool:
    return action == ACTION_TERMINATE


def split_relays(relays: str) -> list[str]:
    return [relay.strip() for relay in relays.split(",") if relay.strip()]


def normalize_verify_value(verify: str) -> str:
    value = verify.strip()
    lowered = value.lower()
    if lowered in {"any", "majority", "all"}:
        return lowered
    if not lowered.startswith(("wss://", "ws://")):
        return f"wss://{value}"
    return value


async def find_existing_control_records(
    relays: str,
    object_digest: str,
    action: str,
    pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_pubkey(pubkey_hex)
    assert_hex_object_identifier(object_digest)
    async with ClientPool(
        split_relays(relays),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "authors": [pubkey_hex],
                "kinds": [CONTROL_EVENT_KIND],
                "#o": [object_digest],
                "limit": limit,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    events = [event for event in events if event_tag_value(event, "action") == action]
    Event.sort(events, inplace=True, reverse=True)
    return events


async def find_control_events_for_object(
    relays: str,
    object_digest: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_object_identifier(object_digest)
    async with ClientPool(
        split_relays(relays),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "kinds": [CONTROL_EVENT_KIND],
                "#o": [object_digest],
                "limit": limit,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    Event.sort(events, inplace=True, reverse=False)
    return events


async def find_origin_events_for_object(
    relays: str,
    object_digest: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_object_identifier(object_digest)
    async with ClientPool(
        split_relays(relays),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "kinds": [DEFAULT_KIND],
                "#o": [object_digest],
                "limit": limit,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    Event.sort(events, inplace=True, reverse=False)
    return events


async def fetch_event_by_id(
    relays: str,
    event_id_hex: str,
    query_timeout: int,
) -> Event | None:
    assert_hex_event_id(event_id_hex)
    async with ClientPool(
        split_relays(relays),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "ids": [event_id_hex],
                "limit": 1,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    if not events:
        return None

    Event.sort(events, inplace=True, reverse=True)
    return events[0]


def latest_chain_event(origin_event: Event, chain_events: list[Event]) -> Event:
    if not chain_events:
        return origin_event
    return max(chain_events, key=lambda evt: ((evt.created_at or 0), evt.id))


def latest_state_event(origin_event: Event, chain_events: list[Event]) -> Event:
    state_events = [
        evt
        for evt in chain_events
        if control_action_changes_controller(event_tag_value(evt, "action"))
        or control_action_terminates(event_tag_value(evt, "action"))
    ]
    if not state_events:
        return origin_event
    return max(state_events, key=lambda evt: ((evt.created_at or 0), evt.id))


def resolve_root_origin_id_for_event(
    event: Event,
    origin_events_by_id: dict[str, Event],
    all_events_by_id: dict[str, Event],
) -> str | None:
    current_event = event
    visited_ids: set[str] = set()
    while True:
        if current_event.id in visited_ids:
            return None
        visited_ids.add(current_event.id)

        if current_event.kind == DEFAULT_KIND:
            return current_event.id if current_event.id in origin_events_by_id else None
        if current_event.kind != CONTROL_EVENT_KIND:
            return None

        previous_event_id = event_tag_value(current_event, "e")
        if previous_event_id is None:
            return None
        previous_event = all_events_by_id.get(previous_event_id)
        if previous_event is None:
            return None
        current_event = previous_event


def group_control_events_by_origin(
    origin_events: list[Event],
    control_events: list[Event],
) -> dict[str, list[Event]]:
    origin_events_by_id = {event.id: event for event in origin_events}
    all_events_by_id = {event.id: event for event in origin_events + control_events}
    events_by_origin_id: dict[str, list[Event]] = {}
    for event in control_events:
        root_origin_id = resolve_root_origin_id_for_event(event, origin_events_by_id, all_events_by_id)
        if root_origin_id is not None:
            events_by_origin_id.setdefault(root_origin_id, []).append(event)
    return events_by_origin_id


async def resolve_active_chain_for_controller(
    relays: str,
    object_digest: str,
    author_pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    return await DEFAULT_CONTROL_GUARD_POLICY.resolve_active_chain_for_controller(
        relays,
        object_digest,
        author_pubkey_hex,
        query_timeout,
        limit,
    )


async def resolve_pending_initiate_for_transferee(
    relays: str,
    object_digest: str,
    author_pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    return await DEFAULT_CONTROL_GUARD_POLICY.resolve_pending_initiate_for_transferee(
        relays,
        object_digest,
        author_pubkey_hex,
        query_timeout,
        limit,
    )


async def resolve_single_active_chain_for_object(
    relays: str,
    object_digest: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    return await DEFAULT_CONTROL_GUARD_POLICY.resolve_single_active_chain_for_object(
        relays,
        object_digest,
        query_timeout,
        limit,
    )


def derive_origin_object_digest(origin_event: Event) -> str:
    if origin_event.kind != DEFAULT_KIND:
        raise ControlEventError(f"referenced origin event must be kind {DEFAULT_KIND}")
    digest = event_tag_value(origin_event, "o") or event_tag_value(origin_event, "d")
    if digest is None:
        raise ControlEventError("referenced origin event does not contain an object identifier in o or d")
    return assert_hex_object_identifier(digest)


async def resolve_origin_from_prior_event(
    relays: str,
    prior_event_id_hex: str,
    query_timeout: int,
) -> tuple[Event, Event]:
    return await DEFAULT_CONTROL_GUARD_POLICY.resolve_origin_from_prior_event(
        relays,
        prior_event_id_hex,
        query_timeout,
    )


async def publish_event_and_verify(
    relays: str,
    event: Event,
    publish_wait: float,
    query_timeout: int,
    verify: str = "any",
) -> dict[str, Any]:
    ok_results: list[dict[str, Any]] = []

    def on_ok(the_client, event_id: str, success: bool, message: str) -> None:
        ok_results.append({"event_id": event_id, "success": success, "message": message})

    relay_list = split_relays(relays)
    async with ClientPool(
        relay_list,
        on_ok=on_ok,
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        client.publish(event)
        if publish_wait > 0:
            await asyncio.sleep(publish_wait)

    normalized_verify = normalize_verify_value(verify)
    verify_relays = relay_list if normalized_verify in {"any", "majority", "all"} else [normalized_verify]
    o_value = event_tag_value(event, "o")
    fallback_filter: dict[str, Any] = {
        "authors": [assert_hex_pubkey(event.pub_key)],
        "kinds": [event.kind],
        "limit": 10,
    }
    if o_value is not None:
        fallback_filter["#o"] = [assert_hex_object_identifier(o_value)]

    verification_results: dict[str, list[Event]] = {}
    for attempt in range(1, 4):
        verification_results = {}
        exact_count = 0
        for relay in verify_relays:
            async with ClientPool([relay], timeout=query_timeout, query_timeout=query_timeout) as verify_client:
                relay_events = await verify_client.query(
                    {"ids": [event.id], "limit": 1},
                    emulate_single=True,
                    wait_connect=True,
                    timeout=query_timeout,
                )
                if not relay_events:
                    relay_events = await verify_client.query(
                        fallback_filter,
                        emulate_single=True,
                        wait_connect=True,
                        timeout=query_timeout,
                    )
            Event.sort(relay_events, inplace=True, reverse=True)
            verification_results[relay] = relay_events
            if any(found.id == event.id for found in relay_events):
                exact_count += 1

        total_relays = len(verify_relays)
        majority_threshold = (total_relays // 2) + 1
        if normalized_verify == "any" and exact_count >= 1:
            break
        if normalized_verify == "majority" and exact_count >= majority_threshold:
            break
        if normalized_verify == "all" and exact_count == total_relays:
            break
        if normalized_verify not in {"any", "majority", "all"} and exact_count == 1:
            break
        if attempt < 3:
            await asyncio.sleep(2.0)

    exact_relays = [relay for relay, events in verification_results.items() if any(found.id == event.id for found in events)]
    slot_relays = [relay for relay, events in verification_results.items() if events]
    return {
        "event_id": event.id,
        "event": event,
        "event_ref": event.id,
        "kind": event.kind,
        "pubkey": format_pubkey(event.pub_key),
        "author_pubkey_hex": event.pub_key,
        "author_npub": format_pubkey(event.pub_key),
        "tags": event.tags,
        "content": event.content,
        "relays": relays,
        "ok_results": ok_results,
        "verification": {
            "mode": verify,
            "exact": len(exact_relays),
            "slot": len(slot_relays),
            "total": len(verify_relays),
            "exact_relays": exact_relays,
            "slot_relays": slot_relays,
        },
    }


async def publish_auxiliary_control_event(
    *,
    relays: str,
    object_digest: str | None,
    prior_event_id: str | None,
    signer_nsec: str,
    action: str,
    comment: str | None = None,
    publish_wait: float = 2.0,
    query_timeout: int = DEFAULT_QUERY_TIMEOUT,
    limit: int = DEFAULT_LIMIT,
    verify: str = "any",
    participant_pubkey_hex: str | None = None,
    control_type: str | None = None,
    external_ref: str | None = None,
    encumbrance_event_id: str | None = None,
    force: bool = False,
    guard_policy: ControlGuardPolicy | None = None,
) -> dict[str, Any]:
    keys = resolve_keys(signer_nsec)
    author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
    guards = guard_policy or DEFAULT_CONTROL_GUARD_POLICY
    if prior_event_id is not None:
        resolved_origin, referenced_event = await guards.resolve_origin_from_prior_event(
            relays, assert_hex_event_id(normalize_event_reference(prior_event_id)), query_timeout
        )
        object_digest_for_event = derive_origin_object_digest(resolved_origin)
    else:
        if object_digest is None:
            raise ControlEventError("object_digest is required when prior_event_id is not supplied")
        if action == ACTION_TERMINATE:
            resolved_origin, referenced_event = await guards.resolve_active_chain_for_controller(
                relays, object_digest, author_pubkey_hex, query_timeout, limit
            )
        else:
            resolved_origin, referenced_event = await guards.resolve_single_active_chain_for_object(
                relays, object_digest, query_timeout, limit
            )
        object_digest_for_event = assert_hex_object_identifier(object_digest)

    if encumbrance_event_id is not None:
        encumbrance_event_id = assert_hex_event_id(normalize_event_reference(encumbrance_event_id))
        encumbrance_event = await fetch_event_by_id(relays, encumbrance_event_id, query_timeout)
        if encumbrance_event is None:
            raise ControlEventError("encumbrance event could not be found on the configured relays")
        if encumbrance_event.kind != CONTROL_EVENT_KIND or event_tag_value(encumbrance_event, "action") != ACTION_ENCUMBER:
            raise ControlEventError(f"encumbrance event must be a kind {CONTROL_EVENT_KIND} action=encumber event")

    existing_events = await find_existing_control_records(
        relays, object_digest_for_event, action, author_pubkey_hex, query_timeout, limit
    )
    if existing_events and not force:
        raise ControlEventError(
            f"an {action} event already exists for this author and object; pass force to publish another event"
        )

    resolved_comment = comment or (
        f"{action}; object={format_object_identifier(object_digest_for_event)}; "
        f"prior_event={referenced_event.id}; origin_event={resolved_origin.id}; signer={format_pubkey(author_pubkey_hex)}"
    )
    tags = [
        ["o", object_digest_for_event],
        ["e", referenced_event.id],
        ["origin", resolved_origin.id],
        ["action", action],
    ]
    if participant_pubkey_hex is not None:
        tags.append(["p", assert_hex_pubkey(participant_pubkey_hex)])
    if encumbrance_event_id is not None:
        tags.append(["enc", encumbrance_event_id])
    if control_type:
        tags.append(["type", control_type])
    if external_ref:
        tags.append(["ref", external_ref])

    event = Event(kind=CONTROL_EVENT_KIND, content=resolved_comment, pub_key=author_pubkey_hex, tags=tags)
    event.sign(keys.private_key_hex())
    result = await publish_event_and_verify(relays, event, publish_wait, query_timeout, verify)
    result.update(
        {
            "action": action,
            "object_digest": object_digest_for_event,
            "object_id": format_object_identifier(object_digest_for_event),
            "origin_event_id": resolved_origin.id,
            "prior_event_id": referenced_event.id,
            "previous_existing_event_id": existing_events[0].id if existing_events else None,
            "replaced_existing_event_id": None,
        }
    )
    return result


async def publish_transfer_initiate_event(
    *,
    relays: str,
    object_digest: str | None,
    prior_event_id: str | None,
    signer_nsec: str,
    transferee_pubkey_hex: str,
    comment: str | None = None,
    publish_wait: float = 2.0,
    query_timeout: int = DEFAULT_QUERY_TIMEOUT,
    limit: int = DEFAULT_LIMIT,
    verify: str = "any",
    force: bool = False,
    guard_policy: ControlGuardPolicy | None = None,
) -> dict[str, Any]:
    keys = resolve_keys(signer_nsec)
    author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
    guards = guard_policy or DEFAULT_CONTROL_GUARD_POLICY
    if prior_event_id is not None:
        resolved_origin, referenced_event = await guards.resolve_origin_from_prior_event(
            relays, assert_hex_event_id(normalize_event_reference(prior_event_id)), query_timeout
        )
        object_digest_for_event = derive_origin_object_digest(resolved_origin)
    else:
        if object_digest is None:
            raise ControlEventError("object_digest is required when prior_event_id is not supplied")
        resolved_origin, referenced_event = await guards.resolve_active_chain_for_controller(
            relays, object_digest, author_pubkey_hex, query_timeout, limit
        )
        object_digest_for_event = assert_hex_object_identifier(object_digest)

    if referenced_event.kind == DEFAULT_KIND:
        origin_author_pubkey_hex = assert_hex_pubkey(resolved_origin.pub_key)
        if author_pubkey_hex != origin_author_pubkey_hex:
            raise ControlEventError(
                "transfer initiate signer must match the issuer of the referenced origin event "
                f"({format_pubkey(origin_author_pubkey_hex)})"
            )
    elif referenced_event.kind == CONTROL_EVENT_KIND:
        prior_transferee = event_tag_value(referenced_event, "p")
        if prior_transferee is None or author_pubkey_hex != assert_hex_pubkey(prior_transferee):
            raise ControlEventError("transfer initiate signer must match the transferee named in the referenced prior transfer event")

    existing_events = await find_existing_control_records(
        relays, object_digest_for_event, ACTION_INITIATE, author_pubkey_hex, query_timeout, limit
    )
    if existing_events and not force:
        raise ControlEventError(
            "a transfer initiate event already exists for this author and object; pass force to publish another event"
        )

    transferee_pubkey_hex = assert_hex_pubkey(transferee_pubkey_hex)
    resolved_comment = comment or (
        "transfer initiate; "
        f"object={format_object_identifier(object_digest_for_event)}; prior_event={referenced_event.id}; "
        f"origin_event={resolved_origin.id}; transferee={format_pubkey(transferee_pubkey_hex)}; "
        f"initiator={format_pubkey(author_pubkey_hex)}"
    )
    event = Event(
        kind=CONTROL_EVENT_KIND,
        content=resolved_comment,
        pub_key=author_pubkey_hex,
        tags=[
            ["o", object_digest_for_event],
            ["e", referenced_event.id],
            ["origin", resolved_origin.id],
            ["p", transferee_pubkey_hex],
            ["action", ACTION_INITIATE],
        ],
    )
    event.sign(keys.private_key_hex())
    result = await publish_event_and_verify(relays, event, publish_wait, query_timeout, verify)
    result.update(
        {
            "action": ACTION_INITIATE,
            "object_digest": object_digest_for_event,
            "object_id": format_object_identifier(object_digest_for_event),
            "origin_event_id": resolved_origin.id,
            "prior_event_id": referenced_event.id,
            "previous_existing_event_id": existing_events[0].id if existing_events else None,
            "replaced_existing_event_id": None,
        }
    )
    return result


async def publish_transfer_accept_event(
    *,
    relays: str,
    object_digest: str | None = None,
    initiate_event_id: str | None = None,
    signer_nsec: str,
    comment: str | None = None,
    publish_wait: float = 2.0,
    query_timeout: int = DEFAULT_QUERY_TIMEOUT,
    limit: int = DEFAULT_LIMIT,
    verify: str = "any",
    force: bool = False,
    guard_policy: ControlGuardPolicy | None = None,
) -> dict[str, Any]:
    keys = resolve_keys(signer_nsec)
    author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
    guards = guard_policy or DEFAULT_CONTROL_GUARD_POLICY
    if initiate_event_id is not None:
        if object_digest is not None:
            raise ControlEventError("supply either initiate_event_id or object_digest, not both")
        resolved_origin, initiate_event = await guards.resolve_origin_from_prior_event(
            relays,
            assert_hex_event_id(normalize_event_reference(initiate_event_id)),
            query_timeout,
        )
        if initiate_event.kind != CONTROL_EVENT_KIND:
            raise ControlEventError(f"referenced initiate event must be kind {CONTROL_EVENT_KIND}")
        if event_tag_value(initiate_event, "action") != ACTION_INITIATE:
            raise ControlEventError("referenced event must be a transfer initiate event")
        object_digest = event_tag_value(initiate_event, "o")
        if object_digest is None:
            raise ControlEventError("referenced initiate event does not contain an o tag")
        object_digest = assert_hex_object_identifier(object_digest)
    else:
        if object_digest is None:
            raise ControlEventError("object_digest is required when initiate_event_id is not supplied")
        object_digest = assert_hex_object_identifier(object_digest)
        resolved_origin, initiate_event = await guards.resolve_pending_initiate_for_transferee(
            relays, object_digest, author_pubkey_hex, query_timeout, limit
        )

    intended_transferee_pubkey_hex = event_tag_value(initiate_event, "p")
    if intended_transferee_pubkey_hex is None:
        raise ControlEventError("referenced initiate event does not contain a p tag for the intended transferee")
    if author_pubkey_hex != assert_hex_pubkey(intended_transferee_pubkey_hex):
        raise ControlEventError(
            "transfer accept signer must match the intended transferee named in the referenced initiate event "
            f"({format_pubkey(intended_transferee_pubkey_hex)})"
        )

    existing_events = await find_existing_control_records(
        relays, object_digest, ACTION_ACCEPT, author_pubkey_hex, query_timeout, limit
    )
    if existing_events and not force:
        raise ControlEventError(
            "a transfer accept event already exists for this author and object; pass force to publish another event"
        )

    resolved_comment = comment or (
        "transfer accept; "
        f"object={format_object_identifier(object_digest)}; prior_event={initiate_event.id}; "
        f"origin_event={resolved_origin.id}; acceptor={format_pubkey(author_pubkey_hex)}"
    )
    event = Event(
        kind=CONTROL_EVENT_KIND,
        content=resolved_comment,
        pub_key=author_pubkey_hex,
        tags=[
            ["o", object_digest],
            ["e", initiate_event.id],
            ["origin", resolved_origin.id],
            ["action", ACTION_ACCEPT],
        ],
    )
    event.sign(keys.private_key_hex())
    result = await publish_event_and_verify(relays, event, publish_wait, query_timeout, verify)
    result.update(
        {
            "action": ACTION_ACCEPT,
            "object_digest": object_digest,
            "object_id": format_object_identifier(object_digest),
            "origin_event_id": resolved_origin.id,
            "prior_event_id": initiate_event.id,
            "previous_existing_event_id": existing_events[0].id if existing_events else None,
            "replaced_existing_event_id": None,
        }
    )
    return result
