import asyncio
import json
import logging
from pathlib import Path

import click
from monstr.client.client import ClientPool
from monstr.encrypt import Keys
from monstr.event.event import Event

from openetr.config import (
    CONFIG_AS_USER_KEY,
    DEFAULT_KIND,
    DEFAULT_LIMIT,
    DEFAULT_PUBLISH_WAIT,
    DEFAULT_QUERY_TIMEOUT,
    DEFAULT_RELAYS,
    get_profile_config,
    USER_CONFIG_PATH,
    get_active_profile_name,
    load_user_config,
    remove_local_profile_secret,
    store_profile_secret,
)
from openetr.control import (
    ACTION_DISCHARGE,
    ACTION_ENCUMBER,
    ACTION_INITIATE,
    ACTION_REDEEM,
    ACTION_TERMINATE,
    CONTROL_EVENT_KIND,
    action_d_value,
)
from openetr.helpers import (
    GENERATE_LEI_SENTINEL,
    assert_hex_event_id,
    assert_hex_object_identifier,
    assert_hex_pubkey,
    build_comment,
    build_digest,
    format_object_identifier,
    format_pubkey,
    normalize_event_reference,
    parse_authors,
    resolve_query_digest,
    resolve_keys,
    resolve_lei,
)
from openetr.guards import evaluate_issue_etr_guard, find_existing_origin_records_for_object
from openetr.services.issue_etr import build_issue_event_content, build_issue_event_tags

CONTROL_TRANSFER_KIND = CONTROL_EVENT_KIND


def _control_action_changes_controller(action: str | None) -> bool:
    return action == ACTION_INITIATE


def _control_action_terminates(action: str | None) -> bool:
    return action == ACTION_TERMINATE


def _split_relays(relays: str) -> list[str]:
    return [relay.strip() for relay in relays.split(",") if relay.strip()]


def _normalize_verify_value(verify: str) -> str:
    value = verify.strip()
    lowered = value.lower()
    if lowered in {"any", "majority", "all"}:
        return lowered
    if not lowered.startswith(("wss://", "ws://")):
        return f"wss://{value}"
    return value


async def _run_publish_object(
    relays: str,
    digest: str,
    as_user,
    comment: str,
    publish_wait: float,
    query_timeout: int,
    limit: int,
    digest_file: Path | None,
    digest_generated_at,
    digest_file_size: int | None,
    display_hex_tags: bool = False,
    extra_tags: list[list[str]] | None = None,
) -> None:
    ok_results = []
    assert_hex_object_identifier(digest)
    assert_hex_pubkey(as_user.public_key_hex())

    def on_ok(the_client, event_id: str, success: bool, message: str) -> None:
        ok_results.append(
            {
                "event_id": event_id,
                "success": success,
                "message": message,
            }
        )
        click.echo(f"OK from relay for {event_id}: success={success} message={message}")

    event = Event(
        kind=DEFAULT_KIND,
        content=comment,
        pub_key=as_user.public_key_hex(),
        tags=build_issue_event_tags(
            digest=digest,
            filename=digest_file.name if digest_file is not None else format_object_identifier(digest),
            size_bytes=digest_file_size,
            generated_at=digest_generated_at,
            extra_tags=extra_tags,
        ),
    )
    event.sign(as_user.private_key_hex())

    click.echo(f"Relays:  {relays}")
    click.echo(f"Pubkey:  {format_pubkey(as_user.public_key_hex())}")
    click.echo(f"Event ID:{event.id}")
    click.echo(f"Object:  {format_object_identifier(digest)}")
    click.echo(f"Kind:    {event.kind}")
    click.echo(f"d tag:   {digest if display_hex_tags else format_object_identifier(digest)}")
    click.echo(f"o tag:   {digest if display_hex_tags else format_object_identifier(digest)}")
    if digest_file is not None:
        click.echo(f"Source:  sha256({digest_file})")
    click.echo(f"Content: {event.content}")
    click.echo("Event tags:")
    for tag in event.tags:
        click.echo(f"  {tag}")
    click.echo()

    async with ClientPool(
        relays.split(","),
        on_ok=on_ok,
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        click.echo("Publishing event...")
        client.publish(event)

        if publish_wait > 0:
            click.echo(f"Waiting {publish_wait:.1f}s for relay indexing...")
            await asyncio.sleep(publish_wait)

        query_filter = {
            "authors": [as_user.public_key_hex()],
            "kinds": [DEFAULT_KIND],
            "#o": [digest],
            "#d": [digest],
            "limit": limit,
        }

        click.echo(f"Querying with filter: {query_filter}")
        events = await client.query(
            query_filter,
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    click.echo()
    click.echo(f"Query returned {len(events)} event(s)")

    matched = []
    for evt in events:
        d_values = evt.get_tags_value("d")
        o_values = evt.get_tags_value("o")
        has_tag_match = digest in d_values and digest in o_values
        same_event = evt.id == event.id
        click.echo(
            f"- id={evt.id} created_at={evt.created_at} kind={evt.kind} "
            f"author={format_pubkey(evt.pub_key)} "
            f"d_values={[format_object_identifier(value) for value in d_values]} "
            f"o_values={[format_object_identifier(value) for value in o_values]}"
        )
        click.echo(f"  content={evt.content}")
        if has_tag_match:
            matched.append(evt)
        if same_event:
            click.echo("  exact published event matched")

    click.echo()
    if matched:
        click.echo("PASS: relay returned at least one event for the combined #d and #o filter.")
        if any(evt.id == event.id for evt in matched):
            click.echo("PASS: the exact event we published was returned by the combined #d and #o filter.")
        else:
            click.echo("PARTIAL: query matched the d/o tags, but not the exact event id we just published.")
    else:
        click.echo("FAIL: relay did not return any events for the combined #d and #o filter.")

    if ok_results:
        last_ok = ok_results[-1]
        click.echo(
            f"Last OK status: success={last_ok['success']} "
            f"event_id={last_ok['event_id']} message={last_ok['message']}"
        )
    else:
        click.echo("No relay OK message was observed before the command exited; the event may still have been accepted.")


async def _find_existing_object_records(
    relays: str,
    digest: str,
    pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_object_identifier(digest)
    assert_hex_pubkey(pubkey_hex)
    async with ClientPool(
        relays.split(","),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "authors": [pubkey_hex],
                "kinds": [DEFAULT_KIND],
                "#d": [digest],
                "limit": limit,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    Event.sort(events, inplace=True, reverse=True)
    return events


async def _find_existing_transfer_records(
    relays: str,
    d_value: str,
    pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_pubkey(pubkey_hex)
    async with ClientPool(
        relays.split(","),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "authors": [pubkey_hex],
                "kinds": [CONTROL_TRANSFER_KIND],
                "#d": [d_value],
                "limit": limit,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    Event.sort(events, inplace=True, reverse=True)
    return events


async def _find_control_events_for_object(
    relays: str,
    object_digest: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_object_identifier(object_digest)
    async with ClientPool(
        relays.split(","),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "kinds": [CONTROL_TRANSFER_KIND],
                "#o": [object_digest],
                "limit": limit,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    Event.sort(events, inplace=True, reverse=False)
    return events


def _latest_chain_event(origin_event: Event, chain_events: list[Event]) -> Event:
    if not chain_events:
        return origin_event
    return max(
        chain_events,
        key=lambda evt: ((evt.created_at or 0), evt.id),
    )


def _latest_state_event(origin_event: Event, chain_events: list[Event]) -> Event:
    state_events = [
        evt
        for evt in chain_events
        if _control_action_changes_controller(_event_tag_value(evt, "action"))
        or _control_action_terminates(_event_tag_value(evt, "action"))
    ]
    if not state_events:
        return origin_event
    return max(
        state_events,
        key=lambda evt: ((evt.created_at or 0), evt.id),
    )


async def _find_origin_events_for_object(
    relays: str,
    object_digest: str,
    query_timeout: int,
    limit: int,
) -> list[Event]:
    assert_hex_object_identifier(object_digest)
    async with ClientPool(
        relays.split(","),
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


def _warn_if_missing_prior_accept(referenced_event: Event) -> None:
    if referenced_event.kind != CONTROL_TRANSFER_KIND:
        return
    prior_action = _event_tag_value(referenced_event, "action")
    if prior_action != "initiate":
        return
    click.secho(
        "WARNING: the referenced prior transfer event is an initiate event and no corresponding "
        "accept check is being enforced here. Publication may continue, but later attestors or "
        "assessors may require an accept event for full validity.",
        fg="yellow",
        bold=True,
    )


def _resolve_root_origin_id_for_event(
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
        if current_event.kind != CONTROL_TRANSFER_KIND:
            return None

        previous_event_id = _event_tag_value(current_event, "e")
        if previous_event_id is None:
            return None
        previous_event = all_events_by_id.get(previous_event_id)
        if previous_event is None:
            return None
        current_event = previous_event


async def _resolve_active_chain_for_controller(
    relays: str,
    object_digest: str,
    author_pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    origin_events = await _find_origin_events_for_object(
        relays=relays,
        object_digest=object_digest,
        query_timeout=query_timeout,
        limit=limit,
    )
    if not origin_events:
        raise click.ClickException("no origin event was found for this object on the configured relays")

    transfer_events = await _find_control_events_for_object(
        relays=relays,
        object_digest=object_digest,
        query_timeout=query_timeout,
        limit=limit,
    )

    origin_events_by_id = {event.id: event for event in origin_events}
    all_events_by_id = {event.id: event for event in origin_events + transfer_events}
    transfers_by_origin_id: dict[str, list[Event]] = {}
    for event in transfer_events:
        root_origin_id = _resolve_root_origin_id_for_event(event, origin_events_by_id, all_events_by_id)
        if root_origin_id is not None:
            transfers_by_origin_id.setdefault(root_origin_id, []).append(event)

    candidates: list[tuple[Event, Event]] = []
    for origin_event in origin_events:
        chain_transfers = transfers_by_origin_id.get(origin_event.id, [])
        latest_event = _latest_state_event(origin_event, chain_transfers)
        latest_action = _event_tag_value(latest_event, "action")
        if _control_action_terminates(latest_action):
            continue
        if latest_event.kind == DEFAULT_KIND:
            current_controller_pubkey_hex = assert_hex_pubkey(origin_event.pub_key)
        else:
            current_controller_pubkey_hex = _event_tag_value(latest_event, "p")
            if current_controller_pubkey_hex is None:
                current_controller_pubkey_hex = latest_event.pub_key
            current_controller_pubkey_hex = assert_hex_pubkey(current_controller_pubkey_hex)

        if current_controller_pubkey_hex == author_pubkey_hex:
            candidates.append((origin_event, latest_event))

    if not candidates:
        raise click.ClickException(
            "the current signer is not the current controller of any active control chain for this object"
        )

    if len(candidates) > 1:
        raise click.ClickException(
            "multiple active control chains for this object are currently controlled by this signer; "
            "the target chain is ambiguous"
        )

    return candidates[0]


async def _resolve_pending_initiate_for_transferee(
    relays: str,
    object_digest: str,
    author_pubkey_hex: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    origin_events = await _find_origin_events_for_object(
        relays=relays,
        object_digest=object_digest,
        query_timeout=query_timeout,
        limit=limit,
    )
    if not origin_events:
        raise click.ClickException("no origin event was found for this object on the configured relays")

    transfer_events = await _find_control_events_for_object(
        relays=relays,
        object_digest=object_digest,
        query_timeout=query_timeout,
        limit=limit,
    )

    origin_events_by_id = {event.id: event for event in origin_events}
    all_events_by_id = {event.id: event for event in origin_events + transfer_events}
    transfers_by_origin_id: dict[str, list[Event]] = {}
    for event in transfer_events:
        root_origin_id = _resolve_root_origin_id_for_event(event, origin_events_by_id, all_events_by_id)
        if root_origin_id is not None:
            transfers_by_origin_id.setdefault(root_origin_id, []).append(event)

    candidates: list[tuple[Event, Event]] = []
    for origin_event in origin_events:
        chain_transfers = transfers_by_origin_id.get(origin_event.id, [])
        if not chain_transfers:
            continue

        latest_event = _latest_state_event(origin_event, chain_transfers)
        latest_action = _event_tag_value(latest_event, "action")
        if latest_action != "initiate":
            continue
        intended_transferee_pubkey_hex = _event_tag_value(latest_event, "p")
        if intended_transferee_pubkey_hex is None:
            continue
        intended_transferee_pubkey_hex = assert_hex_pubkey(intended_transferee_pubkey_hex)
        if intended_transferee_pubkey_hex == author_pubkey_hex:
            candidates.append((origin_event, latest_event))

    if not candidates:
        raise click.ClickException(
            "no pending transfer initiate event was found for this signer on an active control chain for this object"
        )

    if len(candidates) > 1:
        raise click.ClickException(
            "multiple pending transfer initiate events for this object are addressed to this signer; "
            "the target chain is ambiguous"
        )

    return candidates[0]


async def _resolve_single_active_chain_for_object(
    relays: str,
    object_digest: str,
    query_timeout: int,
    limit: int,
) -> tuple[Event, Event]:
    origin_events = await _find_origin_events_for_object(
        relays=relays,
        object_digest=object_digest,
        query_timeout=query_timeout,
        limit=limit,
    )
    if not origin_events:
        raise click.ClickException("no origin event was found for this object on the configured relays")

    transfer_events = await _find_control_events_for_object(
        relays=relays,
        object_digest=object_digest,
        query_timeout=query_timeout,
        limit=limit,
    )

    origin_events_by_id = {event.id: event for event in origin_events}
    all_events_by_id = {event.id: event for event in origin_events + transfer_events}
    transfers_by_origin_id: dict[str, list[Event]] = {}
    for event in transfer_events:
        root_origin_id = _resolve_root_origin_id_for_event(event, origin_events_by_id, all_events_by_id)
        if root_origin_id is not None:
            transfers_by_origin_id.setdefault(root_origin_id, []).append(event)

    candidates: list[tuple[Event, Event]] = []
    for origin_event in origin_events:
        chain_transfers = transfers_by_origin_id.get(origin_event.id, [])
        latest_state_event = _latest_state_event(origin_event, chain_transfers)
        latest_action = _event_tag_value(latest_state_event, "action")
        if _control_action_terminates(latest_action):
            continue
        latest_event = _latest_chain_event(origin_event, chain_transfers)
        candidates.append((origin_event, latest_event))

    if not candidates:
        raise click.ClickException("no active control chain was found for this object on the configured relays")

    if len(candidates) > 1:
        raise click.ClickException(
            "multiple active control chains exist for this object; the target chain is ambiguous"
        )

    return candidates[0]


async def _fetch_current_profile(
    relays: str,
    pubkey_hex: str,
    query_timeout: int,
) -> dict:
    async with ClientPool(
        relays.split(","),
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        events = await client.query(
            {
                "authors": [pubkey_hex],
                "kinds": [0],
                "limit": 1,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    Event.sort(events, inplace=True, reverse=True)
    if not events or not events[0].content:
        return {}

    try:
        return json.loads(events[0].content)
    except json.JSONDecodeError:
        return {}


async def _fetch_event_by_id(
    relays: str,
    event_id_hex: str,
    query_timeout: int,
) -> Event | None:
    assert_hex_event_id(event_id_hex)
    async with ClientPool(
        relays.split(","),
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


def _event_tag_value(event: Event, tag_name: str) -> str | None:
    values = event.get_tags_value(tag_name)
    return values[0] if values else None


def _derive_origin_object_digest(origin_event: Event) -> str:
    if origin_event.kind != DEFAULT_KIND:
        raise click.ClickException(f"referenced origin event must be kind {DEFAULT_KIND}")

    digest = _event_tag_value(origin_event, "o") or _event_tag_value(origin_event, "d")
    if digest is None:
        raise click.ClickException("referenced origin event does not contain an object identifier in o or d")
    return assert_hex_object_identifier(digest)


async def _resolve_origin_from_prior_event(
    relays: str,
    prior_event_id_hex: str,
    query_timeout: int,
) -> tuple[Event, Event]:
    starting_event = await _fetch_event_by_id(
        relays=relays,
        event_id_hex=prior_event_id_hex,
        query_timeout=query_timeout,
    )
    if starting_event is None:
        raise click.ClickException("prior event could not be found on the configured relays")
    if starting_event.kind not in {DEFAULT_KIND, CONTROL_TRANSFER_KIND}:
        raise click.ClickException(
            f"prior event must be kind {DEFAULT_KIND} (origin) or {CONTROL_TRANSFER_KIND} (control transfer)"
        )

    current_event = starting_event
    visited_ids = set()
    while True:
        if current_event.id in visited_ids:
            raise click.ClickException("prior event chain contains a cycle and could not be resolved to origin")
        visited_ids.add(current_event.id)

        if current_event.kind == DEFAULT_KIND:
            return current_event, starting_event

        if current_event.kind != CONTROL_TRANSFER_KIND:
            raise click.ClickException(
                f"prior event chain must terminate in kind {DEFAULT_KIND} and may only traverse kind {CONTROL_TRANSFER_KIND} events"
            )

        previous_event_id = _event_tag_value(current_event, "e")
        if previous_event_id is None:
            raise click.ClickException(
                "prior transfer event does not reference an earlier event in its e tag"
            )
        previous_event_id = assert_hex_event_id(previous_event_id)

        previous_event = await _fetch_event_by_id(
            relays=relays,
            event_id_hex=previous_event_id,
            query_timeout=query_timeout,
        )
        if previous_event is None:
            raise click.ClickException(
                "prior transfer event could not be traversed back to an origin event"
            )

        current_event = previous_event


async def _run_publish_transfer_event(
    relays: str,
    event: Event,
    publish_wait: float,
    query_timeout: int,
    verify: str,
) -> None:
    indexing_retry_attempts = 3
    indexing_retry_delay_seconds = 2.0
    ok_results = []

    def on_ok(the_client, event_id: str, success: bool, message: str) -> None:
        ok_results.append(
            {
                "event_id": event_id,
                "success": success,
                "message": message,
            }
        )
        click.echo(f"OK from relay for {event_id}: success={success} message={message}")

    click.echo(f"Relays:  {relays}")
    click.echo(f"Pubkey:  {format_pubkey(event.pub_key)}")
    click.echo(f"Event ID:{event.id}")
    click.echo(f"Kind:    {event.kind}")
    click.echo("Tags:")
    for tag in event.tags:
        click.echo(f"  {tag}")
    click.echo(f"Content: {event.content}")
    click.echo(f"Verify:  {verify}")
    click.echo()

    relay_list = _split_relays(relays)
    async with ClientPool(
        relay_list,
        on_ok=on_ok,
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        click.echo("Publishing transfer event...")
        client.publish(event)

        if publish_wait > 0:
            click.echo(f"Waiting {publish_wait:.1f}s for relay indexing...")
            await asyncio.sleep(publish_wait)

    normalized_verify = _normalize_verify_value(verify)
    if normalized_verify in {"any", "majority", "all"}:
        verify_relays = relay_list
    else:
        verify_relays = [normalized_verify]

    d_value = _event_tag_value(event, "d")
    o_value = _event_tag_value(event, "o")
    fallback_filter = {
        "authors": [assert_hex_pubkey(event.pub_key)],
        "kinds": [event.kind],
        "limit": 10,
    }
    if d_value is not None:
        fallback_filter["#d"] = [d_value]
    if o_value is not None:
        fallback_filter["#o"] = [assert_hex_object_identifier(o_value)]

    verification_results: dict[str, list[Event]] = {}
    for attempt in range(1, indexing_retry_attempts + 1):
        verification_results = {}
        exact_count = 0
        slot_count = 0

        for relay in verify_relays:
            async with ClientPool(
                [relay],
                timeout=query_timeout,
                query_timeout=query_timeout,
            ) as verify_client:
                relay_events = await verify_client.query(
                    {
                        "ids": [event.id],
                        "limit": 1,
                    },
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
            if relay_events:
                slot_count += 1
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

        if attempt < indexing_retry_attempts:
            click.echo(
                f"Relay indexing advisory: {exact_count} of {total_relays} verification target(s) "
                f"currently show the exact transfer event; waiting {indexing_retry_delay_seconds:.1f}s "
                f"before retry {attempt + 1} of {indexing_retry_attempts}..."
            )
            await asyncio.sleep(indexing_retry_delay_seconds)

    exact_relays = [relay for relay, events in verification_results.items() if any(found.id == event.id for found in events)]
    slot_relays = [relay for relay, events in verification_results.items() if events]
    total_relays = len(verify_relays)
    majority_threshold = (total_relays // 2) + 1

    click.echo()
    click.echo(
        f"Verification summary: exact={len(exact_relays)}/{total_relays} "
        f"slot={len(slot_relays)}/{total_relays}"
    )
    if normalized_verify == "any":
        pass_condition = len(exact_relays) >= 1
    elif normalized_verify == "majority":
        pass_condition = len(exact_relays) >= majority_threshold
    elif normalized_verify == "all":
        pass_condition = len(exact_relays) == total_relays
    else:
        pass_condition = len(exact_relays) == 1

    if pass_condition:
        click.echo("PASS: transfer verification requirement was satisfied.")
    elif slot_relays:
        click.echo("PARTIAL: transfer verification found the replaceable transfer slot, but not enough exact event matches.")
        click.echo(f"Published event id: {event.id}")
        for relay in verify_relays:
            relay_events = verification_results.get(relay, [])
            if relay_events:
                latest = relay_events[0]
                click.echo(f"Relay: {relay}")
                click.echo(f"  returned event id: {latest.id}")
                click.echo(f"  returned created_at: {latest.created_at}")
            else:
                click.echo(f"Relay: {relay}")
                click.echo("  returned event id: none")
    else:
        click.echo("FAIL: no transfer event was returned after publish.")

    if ok_results:
        last_ok = ok_results[-1]
        click.echo(
            f"Last OK status: success={last_ok['success']} "
            f"event_id={last_ok['event_id']} message={last_ok['message']}"
        )
    else:
        click.echo("No relay OK message was observed before the command exited; the event may still have been accepted.")


async def _run_publish_profile(
    relays: str,
    as_user,
    content: dict,
    publish_wait: float,
    query_timeout: int,
) -> None:
    ok_results = []

    def on_ok(the_client, event_id: str, success: bool, message: str) -> None:
        ok_results.append(
            {
                "event_id": event_id,
                "success": success,
                "message": message,
            }
        )
        click.echo(f"OK from relay for {event_id}: success={success} message={message}")

    event = Event(
        kind=0,
        content=json.dumps(content, separators=(",", ":"), ensure_ascii=True),
        pub_key=as_user.public_key_hex(),
    )
    event.sign(as_user.private_key_hex())

    click.echo(f"Relays:  {relays}")
    click.echo(f"Pubkey:  {format_pubkey(as_user.public_key_hex())}")
    click.echo(f"Event ID:{event.id}")
    click.echo("Kind:    0")
    click.echo("Profile content:")
    click.echo(event.content)
    click.echo()

    async with ClientPool(
        relays.split(","),
        on_ok=on_ok,
        timeout=query_timeout,
        query_timeout=query_timeout,
    ) as client:
        click.echo("Publishing profile event...")
        client.publish(event)

        if publish_wait > 0:
            click.echo(f"Waiting {publish_wait:.1f}s for relay indexing...")
            await asyncio.sleep(publish_wait)

        events = await client.query(
            {
                "authors": [as_user.public_key_hex()],
                "kinds": [0],
                "limit": 1,
            },
            emulate_single=True,
            wait_connect=True,
            timeout=query_timeout,
        )

    Event.sort(events, inplace=True, reverse=True)
    click.echo()
    click.echo(f"Query returned {len(events)} event(s)")

    if events:
        latest = events[0]
        click.echo(f"Latest profile event: {latest.id}")
        click.echo(latest.content)
        if latest.id == event.id:
            click.echo("PASS: the exact profile event we published was returned.")
        else:
            click.echo("PARTIAL: a profile event was returned, but it was not the exact new event id.")
    else:
        click.echo("FAIL: no kind 0 profile event was returned after publish.")

    if ok_results:
        last_ok = ok_results[-1]
        click.echo(
            f"Last OK status: success={last_ok['success']} "
            f"event_id={last_ok['event_id']} message={last_ok['message']}"
        )
    else:
        click.echo("No relay OK message was observed before the command exited; the event may still have been accepted.")


def _resolve_publish_key(profile: str, as_user: str | None, force: bool) -> Keys:
    profile_config = get_profile_config(profile, load_user_config())
    configured_key = profile_config.get(CONFIG_AS_USER_KEY)

    if as_user is not None:
        keys = resolve_keys(as_user)
        if configured_key:
            configured_keys = resolve_keys(configured_key)
            if configured_keys.public_key_hex() != keys.public_key_hex() and not force:
                click.secho(
                    "WARNING: this command is using a temporary identity that differs from the current profile.",
                    fg="yellow",
                    bold=True,
                )
                click.echo(f"Profile:          {profile}")
                click.echo(f"Profile signer:   {configured_keys.public_key_bech32()}")
                click.echo(f"Temporary signer: {keys.public_key_bech32()}")
                click.confirm(
                    click.style("Continue with the temporary identity override?", fg="yellow", bold=True),
                    default=False,
                    abort=True,
                )
        return keys

    if configured_key:
        return resolve_keys(configured_key)

    click.confirm(
        f"No --as-user value was supplied and no key exists in {USER_CONFIG_PATH}. "
        "Generate a new key and store it in relay-backed profile storage?",
        default=True,
        abort=True,
    )
    keys = Keys()
    config = load_user_config()
    store_profile_secret(profile, keys.private_key_bech32(), config)
    remove_local_profile_secret(profile, config)
    click.echo("Generated a new key and stored it in relay-backed profile storage.")
    return keys


def _profile_updates(
    name: str | None,
    display_name: str | None,
    about: str | None,
    address: str | None,
    picture: str | None,
    banner: str | None,
    website: str | None,
    nip05: str | None,
    lud16: str | None,
    lud06: str | None,
    lei: str | None,
) -> dict:
    updates = {}
    if name is not None:
        updates["name"] = name
    if display_name is not None:
        updates["display_name"] = display_name
    if about is not None:
        updates["about"] = about
    if address is not None:
        updates["address"] = address
    if picture is not None:
        updates["picture"] = picture
    if banner is not None:
        updates["banner"] = banner
    if website is not None:
        updates["website"] = website
    if nip05 is not None:
        updates["nip05"] = nip05
    if lud16 is not None:
        updates["lud16"] = lud16
    if lud06 is not None:
        updates["lud06"] = lud06
    if lei is not None:
        updates["lei"] = resolve_lei(lei)
    return updates


@click.command("publish-object")
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--digest",
    default=None,
    help="nobj or 32-byte hex digest to use as the d and o tag values; autogenerated if omitted.",
)
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option(
    "--comment",
    default=None,
    help="Comment string to publish as event content; autogenerated if omitted.",
)
@click.option(
    "--publish-wait",
    type=float,
    default=None,
    help="Seconds to wait after publish before querying.",
)
@click.option(
    "--query-timeout",
    type=int,
    default=None,
    help="Seconds to wait for the query to complete.",
)
@click.option(
    "--limit",
    type=int,
    default=None,
    help="Query result limit.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def publish_object(
    profile: str | None,
    relays: str | None,
    digest: str | None,
    digest_file: Path | None,
    as_user: str | None,
    force: bool,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    debug: bool,
) -> None:
    """Publish and query a replaceable event with matching d and o tags."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    resolved_query_timeout = query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)
    resolved_limit = limit if limit is not None else profile_config.get("limit", DEFAULT_LIMIT)

    keys = _resolve_publish_key(profile_name, as_user, force)
    resolved_digest, generated_at, resolved_file, file_size = build_digest(
        digest=digest,
        digest_file=str(digest_file) if digest_file is not None else None,
        keys=keys,
    )
    resolved_comment = build_comment(
        comment=comment,
        digest=resolved_digest,
        generated_at=generated_at,
        digest_file=resolved_file,
        digest_file_size=file_size,
    )

    asyncio.run(
        _run_publish_object(
            relays=resolved_relays,
            digest=resolved_digest,
            as_user=keys,
            comment=resolved_comment,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
            digest_file=resolved_file,
            digest_generated_at=generated_at,
            digest_file_size=file_size,
            display_hex_tags=False,
        )
    )


@click.command("issue-etr")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option(
    "--digest",
    default=None,
    help="nobj or 32-byte hex digest to use as the d and o tag values; autogenerated if omitted.",
)
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option(
    "--comment",
    default=None,
    help="Comment string to publish as event content; autogenerated if omitted.",
)
@click.option(
    "--publish-wait",
    type=float,
    default=None,
    help="Seconds to wait after publish before querying.",
)
@click.option(
    "--query-timeout",
    type=int,
    default=None,
    help="Seconds to wait for the query to complete.",
)
@click.option(
    "--limit",
    type=int,
    default=None,
    help="Query result limit.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def issue_etr(
    profile: str | None,
    relays: str | None,
    digest: str | None,
    digest_file: Path | None,
    as_user: str | None,
    force: bool,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    debug: bool,
) -> None:
    """Issue an ETR record using the canonical publish-object event structure."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    if digest is not None and digest_file is not None:
        raise click.ClickException("supply either DIGEST_FILE as an argument or --digest, not both")

    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = (
        publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    )
    resolved_query_timeout = (
        query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)
    )
    resolved_limit = limit if limit is not None else profile_config.get("limit", DEFAULT_LIMIT)

    keys = _resolve_publish_key(profile_name, as_user, force)
    resolved_digest, generated_at, resolved_file, file_size = build_digest(
        digest=digest,
        digest_file=str(digest_file) if digest_file is not None else None,
        keys=keys,
    )
    resolved_comment = comment or build_issue_event_content(
        resolved_file.name if resolved_file is not None else format_object_identifier(resolved_digest)
    )

    issue_guard = asyncio.run(
        evaluate_issue_etr_guard(
            relays=resolved_relays,
            digest=resolved_digest,
            author_pubkey_hex=keys.public_key_hex(),
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
        )
    )
    if issue_guard["should_warn"]:
        click.secho(issue_guard["warning_message"], fg="yellow", bold=True)
        click.echo(f"Existing event:  {issue_guard['latest_event_id']}")
        click.echo(f"Existing issuer: {issue_guard['latest_issuer_npub']}")
        click.echo(f"Existing object: {issue_guard['object_id']}")
        click.confirm(
            click.style("Continue issuing this ETR record?", fg="yellow", bold=True),
            default=False,
            abort=True,
        )

    asyncio.run(
        _run_publish_object(
            relays=resolved_relays,
            digest=resolved_digest,
            as_user=keys,
            comment=resolved_comment,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
            digest_file=resolved_file,
            digest_generated_at=generated_at,
            digest_file_size=file_size,
            display_hex_tags=True,
        )
    )


@click.group("transfer")
def transfer_group() -> None:
    """Create control transfer events."""


@transfer_group.command("initiate")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option(
    "--prior-event",
    default=None,
    help="Prior event id in hex or simple nevent form; may be the origin event or a prior transfer event.",
)
@click.option(
    "--digest",
    default=None,
    help="nobj or 32-byte hex digest for the ETR object to transfer.",
)
@click.option(
    "--transferee",
    required=True,
    help="Transferee npub to reference in the transfer initiate event.",
)
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option(
    "--comment",
    default=None,
    help="Optional event content. If omitted, a descriptive transfer-initiation comment is generated.",
)
@click.option("--publish-wait", type=float, default=None, help="Seconds to wait after publish before querying.")
@click.option("--query-timeout", type=int, default=None, help="Seconds to wait for the query to complete.")
@click.option("--limit", type=int, default=None, help="Query result limit.")
@click.option(
    "--verify",
    default="any",
    help="Verification mode after publish: any, majority, all, or a specific relay URL.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def transfer_initiate(
    digest_file: Path | None,
    profile: str | None,
    relays: str | None,
    prior_event: str | None,
    digest: str | None,
    transferee: str,
    as_user: str | None,
    force: bool,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    verify: str,
    debug: bool,
) -> None:
    """Initiate a control transfer from an origin or prior transfer event."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = (
        publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    )
    resolved_query_timeout = (
        query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)
    )
    resolved_limit = limit if limit is not None else profile_config.get("limit", DEFAULT_LIMIT)

    keys = _resolve_publish_key(profile_name, as_user, force)
    if prior_event is not None and (digest is not None or digest_file is not None):
        raise click.ClickException("supply either --prior-event or one of --digest/DIGEST_FILE, not both")
    if prior_event is None and (digest is None) == (digest_file is None):
        raise click.ClickException("supply either --prior-event or exactly one of --digest or DIGEST_FILE")

    prior_event_id = normalize_event_reference(prior_event) if prior_event is not None else None
    object_digest = None
    if prior_event is None:
        object_digest, _ = resolve_query_digest(digest, digest_file)
    transferee_hex = parse_authors(transferee)
    if not transferee_hex:
        raise click.ClickException("transferee must resolve to a valid npub")
    transferee_pubkey_hex = transferee_hex[0]

    async def _publish() -> None:
        author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
        if prior_event_id is not None:
            resolved_origin, referenced_event = await _resolve_origin_from_prior_event(
                relays=resolved_relays,
                prior_event_id_hex=prior_event_id,
                query_timeout=resolved_query_timeout,
            )
            object_digest_for_event = _derive_origin_object_digest(resolved_origin)
        else:
            resolved_origin, referenced_event = await _resolve_active_chain_for_controller(
                relays=resolved_relays,
                object_digest=object_digest,
                author_pubkey_hex=author_pubkey_hex,
                query_timeout=resolved_query_timeout,
                limit=resolved_limit,
            )
            object_digest_for_event = object_digest

        if referenced_event.kind == DEFAULT_KIND:
            origin_author_pubkey_hex = assert_hex_pubkey(resolved_origin.pub_key)
            if author_pubkey_hex != origin_author_pubkey_hex:
                raise click.ClickException(
                    "transfer initiate signer must match the issuer of the referenced origin event "
                    f"({format_pubkey(origin_author_pubkey_hex)})"
                )
        elif referenced_event.kind == CONTROL_TRANSFER_KIND:
            prior_transferee_pubkey_hex = _event_tag_value(referenced_event, "p")
            if prior_transferee_pubkey_hex is None:
                raise click.ClickException(
                    "referenced prior transfer event does not contain a p tag for the prior transferee"
                )
            prior_transferee_pubkey_hex = assert_hex_pubkey(prior_transferee_pubkey_hex)
            if author_pubkey_hex != prior_transferee_pubkey_hex:
                raise click.ClickException(
                    "transfer initiate signer must match the transferee named in the referenced prior transfer event "
                    f"({format_pubkey(prior_transferee_pubkey_hex)})"
                )
        else:
            raise click.ClickException(
                f"prior event must be kind {DEFAULT_KIND} (origin) or {CONTROL_TRANSFER_KIND} (control transfer)"
            )
        _warn_if_missing_prior_accept(referenced_event)
        d_value = f"{object_digest_for_event}:initiate"
        resolved_comment = comment or (
            "transfer initiate; "
            f"object={format_object_identifier(object_digest_for_event)}; "
            f"prior_event={referenced_event.id}; "
            f"origin_event={resolved_origin.id}; "
            f"transferee={format_pubkey(transferee_pubkey_hex)}; "
            f"initiator={format_pubkey(author_pubkey_hex)}"
        )
        existing_events = await _find_existing_transfer_records(
            relays=resolved_relays,
            d_value=d_value,
            pubkey_hex=author_pubkey_hex,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
        )
        if existing_events:
            latest = existing_events[0]
            click.secho(
                "WARNING: a transfer initiate event already exists for this author and object; "
                "you may be overwriting an existing replaceable transfer record.",
                fg="yellow",
                bold=True,
            )
            click.echo(f"Existing event: {latest.id}")
            click.echo(f"Object:         {format_object_identifier(object_digest_for_event)}")
            click.confirm(
                click.style("Continue publishing this transfer initiate event?", fg="yellow", bold=True),
                default=False,
                abort=True,
            )
        event = Event(
            kind=CONTROL_TRANSFER_KIND,
            content=resolved_comment,
            pub_key=author_pubkey_hex,
            tags=[
                ["d", d_value],
                ["o", object_digest_for_event],
                ["e", referenced_event.id],
                ["origin", resolved_origin.id],
                ["p", transferee_pubkey_hex],
                ["action", "initiate"],
            ],
        )
        event.sign(keys.private_key_hex())
        await _run_publish_transfer_event(
            relays=resolved_relays,
            event=event,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            verify=verify,
        )

    asyncio.run(_publish())


@click.command("terminate-etr")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option(
    "--digest",
    default=None,
    help="nobj or 32-byte hex digest for the ETR object to terminate.",
)
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option(
    "--comment",
    default=None,
    help="Optional event content. If omitted, a descriptive termination comment is generated.",
)
@click.option("--publish-wait", type=float, default=None, help="Seconds to wait after publish before querying.")
@click.option("--query-timeout", type=int, default=None, help="Seconds to wait for the query to complete.")
@click.option("--limit", type=int, default=None, help="Query result limit.")
@click.option(
    "--verify",
    default="any",
    help="Verification mode after publish: any, majority, all, or a specific relay URL.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def terminate_etr(
    digest_file: Path | None,
    profile: str | None,
    relays: str | None,
    digest: str | None,
    as_user: str | None,
    force: bool,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    verify: str,
    debug: bool,
) -> None:
    """Terminate the active ETR control chain for an object."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = (
        publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    )
    resolved_query_timeout = (
        query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)
    )
    resolved_limit = limit if limit is not None else profile_config.get("limit", DEFAULT_LIMIT)

    keys = _resolve_publish_key(profile_name, as_user, force)
    if (digest is None) == (digest_file is None):
        raise click.ClickException("supply exactly one of --digest or DIGEST_FILE")
    object_digest, resolved_digest_file = resolve_query_digest(digest, digest_file)

    async def _publish() -> None:
        author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
        resolved_origin, referenced_event = await _resolve_active_chain_for_controller(
            relays=resolved_relays,
            object_digest=object_digest,
            author_pubkey_hex=author_pubkey_hex,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
        )

        _warn_if_missing_prior_accept(referenced_event)
        d_value = f"{object_digest}:terminate"
        resolved_comment = comment or (
            "terminate etr; "
            f"object={format_object_identifier(object_digest)}; "
            f"prior_event={referenced_event.id}; "
            f"origin_event={resolved_origin.id}; "
            f"terminator={format_pubkey(author_pubkey_hex)}"
        )
        existing_events = await _find_existing_transfer_records(
            relays=resolved_relays,
            d_value=d_value,
            pubkey_hex=author_pubkey_hex,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
        )
        if existing_events:
            latest = existing_events[0]
            click.secho(
                "WARNING: a terminate event already exists for this author and object; "
                "you may be overwriting an existing replaceable termination record.",
                fg="yellow",
                bold=True,
            )
            click.echo(f"Existing event: {latest.id}")
            click.echo(f"Object:         {format_object_identifier(object_digest)}")
            if resolved_digest_file is not None:
                click.echo(f"Source:         sha256({resolved_digest_file})")
            click.confirm(
                click.style("Continue publishing this termination event?", fg="yellow", bold=True),
                default=False,
                abort=True,
            )

        event = Event(
            kind=CONTROL_TRANSFER_KIND,
            content=resolved_comment,
            pub_key=author_pubkey_hex,
            tags=[
                ["d", d_value],
                ["o", object_digest],
                ["e", referenced_event.id],
                ["origin", resolved_origin.id],
                ["action", "terminate"],
            ],
        )
        event.sign(keys.private_key_hex())
        await _run_publish_transfer_event(
            relays=resolved_relays,
            event=event,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            verify=verify,
        )

    asyncio.run(_publish())


@click.command("attest")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option(
    "--prior-event",
    default=None,
    help="Prior event id in hex or simple nevent form to attach the attestation to.",
)
@click.option(
    "--digest",
    default=None,
    help="nobj or 32-byte hex digest for the ETR object to attest.",
)
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option("--type", "attestation_type", default=None, help="Optional attestation type tag.")
@click.option("--subject", default=None, help="Optional subject npub to place in the p tag.")
@click.option("--ref", "external_ref", default=None, help="Optional external reference tag value.")
@click.option(
    "--comment",
    default=None,
    help="Optional event content. If omitted, a descriptive attestation comment is generated.",
)
@click.option("--publish-wait", type=float, default=None, help="Seconds to wait after publish before querying.")
@click.option("--query-timeout", type=int, default=None, help="Seconds to wait for the query to complete.")
@click.option("--limit", type=int, default=None, help="Query result limit.")
@click.option(
    "--verify",
    default="any",
    help="Verification mode after publish: any, majority, all, or a specific relay URL.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def attest(
    digest_file: Path | None,
    profile: str | None,
    relays: str | None,
    prior_event: str | None,
    digest: str | None,
    as_user: str | None,
    force: bool,
    attestation_type: str | None,
    subject: str | None,
    external_ref: str | None,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    verify: str,
    debug: bool,
) -> None:
    """Publish an attestation event for an ETR object."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = (
        publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    )
    resolved_query_timeout = (
        query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)
    )
    resolved_limit = limit if limit is not None else profile_config.get("limit", DEFAULT_LIMIT)

    keys = _resolve_publish_key(profile_name, as_user, force)
    if prior_event is not None and (digest is not None or digest_file is not None):
        raise click.ClickException("supply either --prior-event or one of --digest/DIGEST_FILE, not both")
    if prior_event is None and (digest is None) == (digest_file is None):
        raise click.ClickException("supply either --prior-event or exactly one of --digest or DIGEST_FILE")

    prior_event_id = normalize_event_reference(prior_event) if prior_event is not None else None
    object_digest = None
    if prior_event is None:
        object_digest, _ = resolve_query_digest(digest, digest_file)

    async def _publish() -> None:
        author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
        if prior_event_id is not None:
            resolved_origin, referenced_event = await _resolve_origin_from_prior_event(
                relays=resolved_relays,
                prior_event_id_hex=prior_event_id,
                query_timeout=resolved_query_timeout,
            )
            object_digest_for_event = _derive_origin_object_digest(resolved_origin)
        else:
            resolved_origin, referenced_event = await _resolve_single_active_chain_for_object(
                relays=resolved_relays,
                object_digest=object_digest,
                query_timeout=resolved_query_timeout,
                limit=resolved_limit,
            )
            object_digest_for_event = object_digest

        subject_pubkey_hex = None
        if subject:
            parsed_subjects = parse_authors(subject)
            if not parsed_subjects:
                raise click.ClickException("subject must resolve to a valid npub")
            subject_pubkey_hex = parsed_subjects[0]

        d_value = f"{object_digest_for_event}:attest"
        resolved_comment = comment or (
            "attest; "
            f"object={format_object_identifier(object_digest_for_event)}; "
            f"prior_event={referenced_event.id}; "
            f"origin_event={resolved_origin.id}; "
            f"attestor={format_pubkey(author_pubkey_hex)}"
        )
        existing_events = await _find_existing_transfer_records(
            relays=resolved_relays,
            d_value=d_value,
            pubkey_hex=author_pubkey_hex,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
        )
        if existing_events:
            latest = existing_events[0]
            click.secho(
                "WARNING: an attestation event already exists for this author and object; "
                "you may be overwriting an existing replaceable attestation record.",
                fg="yellow",
                bold=True,
            )
            click.echo(f"Existing event: {latest.id}")
            click.echo(f"Object:         {format_object_identifier(object_digest_for_event)}")
            click.confirm(
                click.style("Continue publishing this attestation event?", fg="yellow", bold=True),
                default=False,
                abort=True,
            )

        tags = [
            ["d", d_value],
            ["o", object_digest_for_event],
            ["e", referenced_event.id],
            ["origin", resolved_origin.id],
            ["action", "attest"],
        ]
        if attestation_type:
            tags.append(["type", attestation_type])
        if subject_pubkey_hex:
            tags.append(["p", subject_pubkey_hex])
        if external_ref:
            tags.append(["ref", external_ref])

        event = Event(
            kind=CONTROL_TRANSFER_KIND,
            content=resolved_comment,
            pub_key=author_pubkey_hex,
            tags=tags,
        )
        event.sign(keys.private_key_hex())
        await _run_publish_transfer_event(
            relays=resolved_relays,
            event=event,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            verify=verify,
        )

    asyncio.run(_publish())


async def _publish_auxiliary_control_event(
    relays: str,
    object_digest: str | None,
    prior_event_id: str | None,
    keys: Keys,
    action: str,
    comment: str | None,
    publish_wait: float,
    query_timeout: int,
    limit: int,
    verify: str,
    participant_pubkey_hex: str | None = None,
    control_type: str | None = None,
    external_ref: str | None = None,
    encumbrance_event_id: str | None = None,
) -> None:
    author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
    if prior_event_id is not None:
        resolved_origin, referenced_event = await _resolve_origin_from_prior_event(
            relays=relays,
            prior_event_id_hex=prior_event_id,
            query_timeout=query_timeout,
        )
        object_digest_for_event = _derive_origin_object_digest(resolved_origin)
    else:
        resolved_origin, referenced_event = await _resolve_single_active_chain_for_object(
            relays=relays,
            object_digest=object_digest,
            query_timeout=query_timeout,
            limit=limit,
        )
        object_digest_for_event = object_digest

    if encumbrance_event_id is not None:
        encumbrance_event = await _fetch_event_by_id(
            relays=relays,
            event_id_hex=encumbrance_event_id,
            query_timeout=query_timeout,
        )
        if encumbrance_event is None:
            raise click.ClickException("encumbrance event could not be found on the configured relays")
        if (
            encumbrance_event.kind != CONTROL_TRANSFER_KIND
            or _event_tag_value(encumbrance_event, "action") != ACTION_ENCUMBER
        ):
            raise click.ClickException("encumbrance event must be a kind 31416 action=encumber event")

    d_value = action_d_value(object_digest_for_event, action)
    resolved_comment = comment or (
        f"{action}; "
        f"object={format_object_identifier(object_digest_for_event)}; "
        f"prior_event={referenced_event.id}; "
        f"origin_event={resolved_origin.id}; "
        f"signer={format_pubkey(author_pubkey_hex)}"
    )
    existing_events = await _find_existing_transfer_records(
        relays=relays,
        d_value=d_value,
        pubkey_hex=author_pubkey_hex,
        query_timeout=query_timeout,
        limit=limit,
    )
    if existing_events:
        latest = existing_events[0]
        click.secho(
            f"WARNING: an {action} event already exists for this author and object; "
            f"you may be overwriting an existing replaceable {action} record.",
            fg="yellow",
            bold=True,
        )
        click.echo(f"Existing event: {latest.id}")
        click.echo(f"Object:         {format_object_identifier(object_digest_for_event)}")
        click.confirm(
            click.style(f"Continue publishing this {action} event?", fg="yellow", bold=True),
            default=False,
            abort=True,
        )

    tags = [
        ["d", d_value],
        ["o", object_digest_for_event],
        ["e", referenced_event.id],
        ["origin", resolved_origin.id],
        ["action", action],
    ]
    if participant_pubkey_hex is not None:
        tags.append(["p", participant_pubkey_hex])
    if encumbrance_event_id is not None:
        tags.append(["enc", encumbrance_event_id])
    if control_type:
        tags.append(["type", control_type])
    if external_ref:
        tags.append(["ref", external_ref])

    event = Event(
        kind=CONTROL_TRANSFER_KIND,
        content=resolved_comment,
        pub_key=author_pubkey_hex,
        tags=tags,
    )
    event.sign(keys.private_key_hex())
    await _run_publish_transfer_event(
        relays=relays,
        event=event,
        publish_wait=publish_wait,
        query_timeout=query_timeout,
        verify=verify,
    )


def _resolve_control_publish_context(
    profile: str | None,
    relays: str | None,
    as_user: str | None,
    force: bool,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
) -> tuple[str, float, int, int, Keys]:
    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = (
        publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    )
    resolved_query_timeout = (
        query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)
    )
    resolved_limit = limit if limit is not None else profile_config.get("limit", DEFAULT_LIMIT)
    keys = _resolve_publish_key(profile_name, as_user, force)
    return resolved_relays, resolved_publish_wait, resolved_query_timeout, resolved_limit, keys


def _resolve_control_object_args(
    prior_event: str | None,
    digest: str | None,
    digest_file: Path | None,
) -> tuple[str | None, str | None]:
    if prior_event is not None and (digest is not None or digest_file is not None):
        raise click.ClickException("supply either --prior-event or one of --digest/DIGEST_FILE, not both")
    if prior_event is None and (digest is None) == (digest_file is None):
        raise click.ClickException("supply either --prior-event or exactly one of --digest or DIGEST_FILE")
    prior_event_id = normalize_event_reference(prior_event) if prior_event is not None else None
    object_digest = None
    if prior_event is None:
        object_digest, _ = resolve_query_digest(digest, digest_file)
    return prior_event_id, object_digest


@click.command("encumber")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option("--prior-event", default=None, help="Prior event id in hex or simple nevent form.")
@click.option("--digest", default=None, help="nobj or 32-byte hex digest for the ETR object to encumber.")
@click.option("--beneficiary", required=True, help="Beneficiary or secured-party npub for the p tag.")
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option("--type", "control_type", default=None, help="Optional encumbrance type tag.")
@click.option("--ref", "external_ref", default=None, help="Optional external reference tag value.")
@click.option("--comment", default=None, help="Optional event content.")
@click.option("--publish-wait", type=float, default=None, help="Seconds to wait after publish before querying.")
@click.option("--query-timeout", type=int, default=None, help="Seconds to wait for the query to complete.")
@click.option("--limit", type=int, default=None, help="Query result limit.")
@click.option(
    "--verify",
    default="any",
    help="Verification mode after publish: any, majority, all, or a specific relay URL.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def encumber(
    digest_file: Path | None,
    profile: str | None,
    relays: str | None,
    prior_event: str | None,
    digest: str | None,
    beneficiary: str,
    as_user: str | None,
    force: bool,
    control_type: str | None,
    external_ref: str | None,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    verify: str,
    debug: bool,
) -> None:
    """Publish an encumbrance event for an ETR object."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)
    resolved_relays, resolved_publish_wait, resolved_query_timeout, resolved_limit, keys = (
        _resolve_control_publish_context(profile, relays, as_user, force, publish_wait, query_timeout, limit)
    )
    prior_event_id, object_digest = _resolve_control_object_args(prior_event, digest, digest_file)
    parsed_beneficiary = parse_authors(beneficiary)
    if not parsed_beneficiary:
        raise click.ClickException("beneficiary must resolve to a valid npub")
    asyncio.run(
        _publish_auxiliary_control_event(
            relays=resolved_relays,
            object_digest=object_digest,
            prior_event_id=prior_event_id,
            keys=keys,
            action=ACTION_ENCUMBER,
            comment=comment,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
            verify=verify,
            participant_pubkey_hex=parsed_beneficiary[0],
            control_type=control_type,
            external_ref=external_ref,
        )
    )


@click.command("discharge")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option("--prior-event", default=None, help="Prior event id in hex or simple nevent form.")
@click.option("--digest", default=None, help="nobj or 32-byte hex digest for the ETR object to discharge.")
@click.option("--encumbrance-event", required=True, help="Encumbrance event id in hex or simple nevent form.")
@click.option("--releasing-party", default=None, help="Optional beneficiary or releasing-party npub for the p tag.")
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option("--ref", "external_ref", default=None, help="Optional external reference tag value.")
@click.option("--comment", default=None, help="Optional event content.")
@click.option("--publish-wait", type=float, default=None, help="Seconds to wait after publish before querying.")
@click.option("--query-timeout", type=int, default=None, help="Seconds to wait for the query to complete.")
@click.option("--limit", type=int, default=None, help="Query result limit.")
@click.option(
    "--verify",
    default="any",
    help="Verification mode after publish: any, majority, all, or a specific relay URL.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def discharge(
    digest_file: Path | None,
    profile: str | None,
    relays: str | None,
    prior_event: str | None,
    digest: str | None,
    encumbrance_event: str,
    releasing_party: str | None,
    as_user: str | None,
    force: bool,
    external_ref: str | None,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    verify: str,
    debug: bool,
) -> None:
    """Publish a discharge event for a prior encumbrance."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)
    resolved_relays, resolved_publish_wait, resolved_query_timeout, resolved_limit, keys = (
        _resolve_control_publish_context(profile, relays, as_user, force, publish_wait, query_timeout, limit)
    )
    prior_event_id, object_digest = _resolve_control_object_args(prior_event, digest, digest_file)
    participant_pubkey_hex = None
    if releasing_party:
        parsed_releasing_party = parse_authors(releasing_party)
        if not parsed_releasing_party:
            raise click.ClickException("releasing-party must resolve to a valid npub")
        participant_pubkey_hex = parsed_releasing_party[0]
    asyncio.run(
        _publish_auxiliary_control_event(
            relays=resolved_relays,
            object_digest=object_digest,
            prior_event_id=prior_event_id,
            keys=keys,
            action=ACTION_DISCHARGE,
            comment=comment,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
            verify=verify,
            participant_pubkey_hex=participant_pubkey_hex,
            external_ref=external_ref,
            encumbrance_event_id=normalize_event_reference(encumbrance_event),
        )
    )


@click.command("redeem")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option("--prior-event", default=None, help="Prior event id in hex or simple nevent form.")
@click.option("--digest", default=None, help="nobj or 32-byte hex digest for the ETR object to redeem.")
@click.option("--obligor", required=True, help="Obligor npub for the p tag.")
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option("--ref", "external_ref", default=None, help="Optional presentation or claim reference tag value.")
@click.option("--comment", default=None, help="Optional event content.")
@click.option("--publish-wait", type=float, default=None, help="Seconds to wait after publish before querying.")
@click.option("--query-timeout", type=int, default=None, help="Seconds to wait for the query to complete.")
@click.option("--limit", type=int, default=None, help="Query result limit.")
@click.option(
    "--verify",
    default="any",
    help="Verification mode after publish: any, majority, all, or a specific relay URL.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def redeem(
    digest_file: Path | None,
    profile: str | None,
    relays: str | None,
    prior_event: str | None,
    digest: str | None,
    obligor: str,
    as_user: str | None,
    force: bool,
    external_ref: str | None,
    comment: str | None,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    verify: str,
    debug: bool,
) -> None:
    """Publish a redemption-presentation event for an ETR object."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)
    resolved_relays, resolved_publish_wait, resolved_query_timeout, resolved_limit, keys = (
        _resolve_control_publish_context(profile, relays, as_user, force, publish_wait, query_timeout, limit)
    )
    prior_event_id, object_digest = _resolve_control_object_args(prior_event, digest, digest_file)
    parsed_obligor = parse_authors(obligor)
    if not parsed_obligor:
        raise click.ClickException("obligor must resolve to a valid npub")
    asyncio.run(
        _publish_auxiliary_control_event(
            relays=resolved_relays,
            object_digest=object_digest,
            prior_event_id=prior_event_id,
            keys=keys,
            action=ACTION_REDEEM,
            comment=comment,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
            verify=verify,
            participant_pubkey_hex=parsed_obligor[0],
            external_ref=external_ref,
        )
    )


@transfer_group.command("accept")
@click.argument("digest_file", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option(
    "--initiate-event",
    default=None,
    help="Transfer initiate event id in hex or simple nevent form.",
)
@click.option(
    "--digest",
    default=None,
    help="nobj or 32-byte hex digest for the ETR object to accept.",
)
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option("--comment", default="", help="Optional event content.")
@click.option("--publish-wait", type=float, default=None, help="Seconds to wait after publish before querying.")
@click.option("--query-timeout", type=int, default=None, help="Seconds to wait for the query to complete.")
@click.option("--limit", type=int, default=None, help="Query result limit.")
@click.option(
    "--verify",
    default="any",
    help="Verification mode after publish: any, majority, all, or a specific relay URL.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def transfer_accept(
    digest_file: Path | None,
    profile: str | None,
    relays: str | None,
    initiate_event: str | None,
    digest: str | None,
    as_user: str | None,
    force: bool,
    comment: str,
    publish_wait: float | None,
    query_timeout: int | None,
    limit: int | None,
    verify: str,
    debug: bool,
) -> None:
    """Accept a previously initiated control transfer."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = (
        publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    )
    resolved_query_timeout = (
        query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)
    )
    resolved_limit = limit if limit is not None else profile_config.get("limit", DEFAULT_LIMIT)

    keys = _resolve_publish_key(profile_name, as_user, force)
    if initiate_event is not None and (digest is not None or digest_file is not None):
        raise click.ClickException("supply either --initiate-event or one of --digest/DIGEST_FILE, not both")
    if initiate_event is None and (digest is None) == (digest_file is None):
        raise click.ClickException("supply either --initiate-event or exactly one of --digest or DIGEST_FILE")

    initiate_event_id = normalize_event_reference(initiate_event) if initiate_event is not None else None
    object_digest = None
    if initiate_event is None:
        object_digest, _ = resolve_query_digest(digest, digest_file)

    async def _publish() -> None:
        author_pubkey_hex = assert_hex_pubkey(keys.public_key_hex())
        current_initiate_event_id = initiate_event_id
        if current_initiate_event_id is not None:
            initiate = await _fetch_event_by_id(
                relays=resolved_relays,
                event_id_hex=current_initiate_event_id,
                query_timeout=resolved_query_timeout,
            )
            if initiate is None:
                raise click.ClickException("transfer initiate event could not be found on the configured relays")
            if initiate.kind != CONTROL_TRANSFER_KIND:
                raise click.ClickException(f"referenced initiate event must be kind {CONTROL_TRANSFER_KIND}")
            initiate_action = _event_tag_value(initiate, "action")
            if initiate_action != "initiate":
                raise click.ClickException("referenced event must be a transfer initiate event")
            object_digest_for_event = _event_tag_value(initiate, "o")
            if object_digest_for_event is None:
                raise click.ClickException("referenced initiate event does not contain an o tag")
            object_digest_for_event = assert_hex_object_identifier(object_digest_for_event)
        else:
            _, initiate = await _resolve_pending_initiate_for_transferee(
                relays=resolved_relays,
                object_digest=object_digest,
                author_pubkey_hex=author_pubkey_hex,
                query_timeout=resolved_query_timeout,
                limit=resolved_limit,
            )
            current_initiate_event_id = initiate.id
            object_digest_for_event = object_digest

        intended_transferee_pubkey_hex = _event_tag_value(initiate, "p")
        if intended_transferee_pubkey_hex is None:
            raise click.ClickException("referenced initiate event does not contain a p tag for the intended transferee")
        intended_transferee_pubkey_hex = assert_hex_pubkey(intended_transferee_pubkey_hex)
        if author_pubkey_hex != intended_transferee_pubkey_hex:
            raise click.ClickException(
                "transfer accept signer must match the intended transferee named in the referenced initiate event "
                f"({format_pubkey(intended_transferee_pubkey_hex)})"
            )

        d_value = f"{object_digest_for_event}:accept"
        resolved_comment = comment or (
            "transfer accept; "
            f"object={format_object_identifier(object_digest_for_event)}; "
            f"initiate_event={current_initiate_event_id}; "
            f"acceptor={format_pubkey(author_pubkey_hex)}; "
            f"initiator={format_pubkey(initiate.pub_key)}"
        )
        existing_events = await _find_existing_transfer_records(
            relays=resolved_relays,
            d_value=d_value,
            pubkey_hex=author_pubkey_hex,
            query_timeout=resolved_query_timeout,
            limit=resolved_limit,
        )
        if existing_events:
            latest = existing_events[0]
            click.secho(
                "WARNING: a transfer accept event already exists for this author and object; "
                "you may be overwriting an existing replaceable accept record.",
                fg="yellow",
                bold=True,
            )
            click.echo(f"Existing event: {latest.id}")
            click.echo(f"Object:         {format_object_identifier(object_digest_for_event)}")
            click.confirm(
                click.style("Continue publishing this transfer accept event?", fg="yellow", bold=True),
                default=False,
                abort=True,
            )
        click.confirm(
            "Confirm publishing this transfer accept event?",
            default=True,
            abort=True,
        )
        event = Event(
            kind=CONTROL_TRANSFER_KIND,
            content=resolved_comment,
            pub_key=author_pubkey_hex,
            tags=[
                ["d", d_value],
                ["o", object_digest_for_event],
                ["e", current_initiate_event_id],
                ["p", initiate.pub_key],
                ["action", "accept"],
            ],
        )
        event.sign(keys.private_key_hex())
        await _run_publish_transfer_event(
            relays=resolved_relays,
            event=event,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
            verify=verify,
        )

    asyncio.run(_publish())


@click.command("publish-profile")
@click.option("--profile", default=None, help="Profile to use; defaults to the active profile.")
@click.option("--relays", default=None, help="Comma separated relay URLs to use.")
@click.option(
    "--as-user",
    default=None,
    help="nsec private key to publish with; loaded from config or generated if omitted.",
)
@click.option("--force", is_flag=True, help="Suppress confirmation prompts.")
@click.option("--name", default=None, help="Profile name.")
@click.option("--display-name", default=None, help="Profile display_name.")
@click.option("--about", default=None, help="Profile about text.")
@click.option("--address", default=None, help="Profile address.")
@click.option("--picture", default=None, help="Profile picture URL.")
@click.option("--banner", default=None, help="Profile banner image URL.")
@click.option("--website", default=None, help="Profile website URL.")
@click.option("--nip05", default=None, help="Profile NIP-05 identifier.")
@click.option("--lud16", default=None, help="Lightning address.")
@click.option("--lud06", default=None, help="LNURL pay string.")
@click.option(
    "--lei",
    default=None,
    flag_value=GENERATE_LEI_SENTINEL,
    help="Profile legal entity identifier, or pass --lei with no value to generate an example LEI.",
)
@click.option("--replace", is_flag=True, help="Replace the entire profile instead of merging with the current one.")
@click.option(
    "--publish-wait",
    type=float,
    default=None,
    help="Seconds to wait after publish before querying.",
)
@click.option(
    "--query-timeout",
    type=int,
    default=None,
    help="Seconds to wait for the query to complete.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def publish_profile(
    profile: str | None,
    relays: str | None,
    as_user: str | None,
    force: bool,
    name: str | None,
    display_name: str | None,
    about: str | None,
    address: str | None,
    picture: str | None,
    banner: str | None,
    website: str | None,
    nip05: str | None,
    lud16: str | None,
    lud06: str | None,
    lei: str | None,
    replace: bool,
    publish_wait: float | None,
    query_timeout: int | None,
    debug: bool,
) -> None:
    """Publish a Nostr kind 0 profile event."""
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    updates = _profile_updates(
        name=name,
        display_name=display_name,
        about=about,
        address=address,
        picture=picture,
        banner=banner,
        website=website,
        nip05=nip05,
        lud16=lud16,
        lud06=lud06,
        lei=lei,
    )
    if not updates:
        raise click.ClickException("No profile fields supplied. Pass at least one profile option to publish.")

    profile_name = profile or get_active_profile_name()
    profile_config = get_profile_config(profile_name)
    resolved_relays = relays or profile_config.get("relays", DEFAULT_RELAYS)
    resolved_publish_wait = publish_wait if publish_wait is not None else profile_config.get("publish_wait", DEFAULT_PUBLISH_WAIT)
    resolved_query_timeout = query_timeout if query_timeout is not None else profile_config.get("query_timeout", DEFAULT_QUERY_TIMEOUT)

    keys = _resolve_publish_key(profile_name, as_user, force)

    async def _publish() -> None:
        current_profile = {} if replace else await _fetch_current_profile(
            relays=resolved_relays,
            pubkey_hex=keys.public_key_hex(),
            query_timeout=resolved_query_timeout,
        )
        merged_profile = dict(current_profile)
        merged_profile.update(updates)
        await _run_publish_profile(
            relays=resolved_relays,
            as_user=keys,
            content=merged_profile,
            publish_wait=resolved_publish_wait,
            query_timeout=resolved_query_timeout,
        )

    asyncio.run(_publish())
