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
    action_d_value,
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


class ControlEventError(Exception):
    """Raised when a control event cannot be built, resolved, or published."""


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
    d_value: str,
    pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_pubkey(pubkey_hex)
    async with ClientPool(
        split_relays(relays),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "authors": [pubkey_hex],
                "kinds": [CONTROL_EVENT_KIND],
                "#d": [d_value],
                "limit": limit,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

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
    origin_events = await find_origin_events_for_object(relays, object_digest, query_timeout, limit)
    if not origin_events:
        raise ControlEventError("no origin event was found for this object on the configured relays")

    control_events = await find_control_events_for_object(relays, object_digest, query_timeout, limit)
    events_by_origin_id = group_control_events_by_origin(origin_events, control_events)

    candidates: list[tuple[Event, Event]] = []
    for origin_event in origin_events:
        chain_events = events_by_origin_id.get(origin_event.id, [])
        latest_event = latest_state_event(origin_event, chain_events)
        latest_action = event_tag_value(latest_event, "action")
        if control_action_terminates(latest_action):
            continue
        if latest_event.kind == DEFAULT_KIND:
            current_controller_pubkey_hex = assert_hex_pubkey(origin_event.pub_key)
        else:
            current_controller_pubkey_hex = event_tag_value(latest_event, "p") or latest_event.pub_key
            current_controller_pubkey_hex = assert_hex_pubkey(current_controller_pubkey_hex)

        if current_controller_pubkey_hex == author_pubkey_hex:
            candidates.append((origin_event, latest_event))

    if not candidates:
        raise ControlEventError(
            "the current signer is not the current controller of any active control chain for this object"
        )
    if len(candidates) > 1:
        raise ControlEventError(
            "multiple active control chains for this object are currently controlled by this signer; the target chain is ambiguous"
        )
    return candidates[0]


async def resolve_pending_initiate_for_transferee(
    relays: str,
    object_digest: str,
    author_pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    origin_events = await find_origin_events_for_object(relays, object_digest, query_timeout, limit)
    if not origin_events:
        raise ControlEventError("no origin event was found for this object on the configured relays")

    control_events = await find_control_events_for_object(relays, object_digest, query_timeout, limit)
    events_by_origin_id = group_control_events_by_origin(origin_events, control_events)

    candidates: list[tuple[Event, Event]] = []
    for origin_event in origin_events:
        chain_events = events_by_origin_id.get(origin_event.id, [])
        if not chain_events:
            continue
        latest_event = latest_state_event(origin_event, chain_events)
        if event_tag_value(latest_event, "action") != ACTION_INITIATE:
            continue
        intended_transferee_pubkey_hex = event_tag_value(latest_event, "p")
        if intended_transferee_pubkey_hex and assert_hex_pubkey(intended_transferee_pubkey_hex) == author_pubkey_hex:
            candidates.append((origin_event, latest_event))

    if not candidates:
        raise ControlEventError(
            "no pending transfer initiate event was found for this signer on an active control chain for this object"
        )
    if len(candidates) > 1:
        raise ControlEventError(
            "multiple pending transfer initiate events for this object are addressed to this signer; the target chain is ambiguous"
        )
    return candidates[0]


async def resolve_single_active_chain_for_object(
    relays: str,
    object_digest: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    origin_events = await find_origin_events_for_object(relays, object_digest, query_timeout, limit)
    if not origin_events:
        raise ControlEventError("no origin event was found for this object on the configured relays")

    control_events = await find_control_events_for_object(relays, object_digest, query_timeout, limit)
    events_by_origin_id = group_control_events_by_origin(origin_events, control_events)

    candidates: list[tuple[Event, Event]] = []
    for origin_event in origin_events:
        chain_events = events_by_origin_id.get(origin_event.id, [])
        latest_state = latest_state_event(origin_event, chain_events)
        if control_action_terminates(event_tag_value(latest_state, "action")):
            continue
        candidates.append((origin_event, latest_chain_event(origin_event, chain_events)))

    if not candidates:
        raise ControlEventError("no active control chain was found for this object on the configured relays")
    if len(candidates) > 1:
        raise ControlEventError("multiple active control chains exist for this object; the target chain is ambiguous")
    return candidates[0]


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
    starting_event = await fetch_event_by_id(relays, prior_event_id_hex, query_timeout)
    if starting_event is None:
        raise ControlEventError("prior event could not be found on the configured relays")
    if starting_event.kind not in {DEFAULT_KIND, CONTROL_EVENT_KIND}:
        raise ControlEventError(
            f"prior event must be kind {DEFAULT_KIND} (origin) or {CONTROL_EVENT_KIND} (control event)"
        )

    current_event = starting_event
    visited_ids: set[str] = set()
    while True:
        if current_event.id in visited_ids:
            raise ControlEventError("prior event chain contains a cycle and could not be resolved to origin")
        visited_ids.add(current_event.id)
        if current_event.kind == DEFAULT_KIND:
            return current_event, starting_event
        previous_event_id = event_tag_value(current_event, "e")
        if previous_event_id is None:
            raise ControlEventError("prior control event does not reference an earlier event in its e tag")
        previous_event = await fetch_event_by_id(relays, assert_hex_event_id(previous_event_id), query_timeout)
        if previous_event is None:
            raise ControlEventError("prior control event could not be traversed back to an origin event")
        current_event = previous_event


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
    d_value = event_tag_value(event, "d")
    o_value = event_tag_value(event, "o")
    fallback_filter: dict[str, Any] = {
        "authors": [assert_hex_pubkey(event.pub_key)],
        "kinds": [event.kind],
        "limit": 10,
    }
    if d_value is not None:
        fallback_filter["#d"] = [d_value]
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
) -> dict[str, Any]:
    keys = resolve_keys(signer_nsec)
    author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
    if prior_event_id is not None:
        resolved_origin, referenced_event = await resolve_origin_from_prior_event(
            relays, assert_hex_event_id(normalize_event_reference(prior_event_id)), query_timeout
        )
        object_digest_for_event = derive_origin_object_digest(resolved_origin)
    else:
        if object_digest is None:
            raise ControlEventError("object_digest is required when prior_event_id is not supplied")
        resolved_origin, referenced_event = await resolve_single_active_chain_for_object(
            relays, object_digest, query_timeout, limit
        )
        object_digest_for_event = assert_hex_object_identifier(object_digest)

    if encumbrance_event_id is not None:
        encumbrance_event_id = assert_hex_event_id(normalize_event_reference(encumbrance_event_id))
        encumbrance_event = await fetch_event_by_id(relays, encumbrance_event_id, query_timeout)
        if encumbrance_event is None:
            raise ControlEventError("encumbrance event could not be found on the configured relays")
        if encumbrance_event.kind != CONTROL_EVENT_KIND or event_tag_value(encumbrance_event, "action") != ACTION_ENCUMBER:
            raise ControlEventError("encumbrance event must be a kind 31416 action=encumber event")

    d_value = action_d_value(object_digest_for_event, action)
    existing_events = await find_existing_control_records(relays, d_value, author_pubkey_hex, query_timeout, limit)
    if existing_events and not force:
        raise ControlEventError(
            f"an {action} event already exists for this author and object; pass force to replace it"
        )

    resolved_comment = comment or (
        f"{action}; object={format_object_identifier(object_digest_for_event)}; "
        f"prior_event={referenced_event.id}; origin_event={resolved_origin.id}; signer={format_pubkey(author_pubkey_hex)}"
    )
    tags = [
        ["d", d_value],
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
            "replaced_existing_event_id": existing_events[0].id if existing_events else None,
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
) -> dict[str, Any]:
    keys = resolve_keys(signer_nsec)
    author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
    if prior_event_id is not None:
        resolved_origin, referenced_event = await resolve_origin_from_prior_event(
            relays, assert_hex_event_id(normalize_event_reference(prior_event_id)), query_timeout
        )
        object_digest_for_event = derive_origin_object_digest(resolved_origin)
    else:
        if object_digest is None:
            raise ControlEventError("object_digest is required when prior_event_id is not supplied")
        resolved_origin, referenced_event = await resolve_active_chain_for_controller(
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

    d_value = action_d_value(object_digest_for_event, ACTION_INITIATE)
    existing_events = await find_existing_control_records(relays, d_value, author_pubkey_hex, query_timeout, limit)
    if existing_events and not force:
        raise ControlEventError("a transfer initiate event already exists for this author and object; pass force to replace it")

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
            ["d", d_value],
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
            "replaced_existing_event_id": existing_events[0].id if existing_events else None,
        }
    )
    return result


async def publish_transfer_accept_event(
    *,
    relays: str,
    object_digest: str,
    signer_nsec: str,
    comment: str | None = None,
    publish_wait: float = 2.0,
    query_timeout: int = DEFAULT_QUERY_TIMEOUT,
    limit: int = DEFAULT_LIMIT,
    verify: str = "any",
    force: bool = False,
) -> dict[str, Any]:
    keys = resolve_keys(signer_nsec)
    author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
    object_digest = assert_hex_object_identifier(object_digest)
    resolved_origin, initiate_event = await resolve_pending_initiate_for_transferee(
        relays, object_digest, author_pubkey_hex, query_timeout, limit
    )
    d_value = action_d_value(object_digest, ACTION_ACCEPT)
    existing_events = await find_existing_control_records(relays, d_value, author_pubkey_hex, query_timeout, limit)
    if existing_events and not force:
        raise ControlEventError("a transfer accept event already exists for this author and object; pass force to replace it")

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
            ["d", d_value],
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
            "replaced_existing_event_id": existing_events[0].id if existing_events else None,
        }
    )
    return result
