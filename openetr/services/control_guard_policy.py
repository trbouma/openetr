from __future__ import annotations

from typing import Protocol

from monstr.client.client import ClientPool
from monstr.event.event import Event

from openetr.config import DEFAULT_KIND
from openetr.control import ACTION_INITIATE, ACTION_TERMINATE, CONTROL_EVENT_KIND
from openetr.helpers import assert_hex_event_id, assert_hex_object_identifier, assert_hex_pubkey


class ControlEventError(Exception):
    """Raised when a control event cannot be built, resolved, or published."""


def event_tag_value(event: Event, tag_name: str) -> str | None:
    values = event.get_tags_value(tag_name)
    return values[0] if values else None


def split_relays(relays: str) -> list[str]:
    return [relay.strip() for relay in relays.split(",") if relay.strip()]


def control_action_changes_controller(action: str | None) -> bool:
    return action == ACTION_INITIATE


def control_action_terminates(action: str | None) -> bool:
    return action == ACTION_TERMINATE


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


class ControlGuardPolicy(Protocol):
    async def resolve_active_chain_for_controller(
        self,
        relays: str,
        object_digest: str,
        author_pubkey_hex: str,
        query_timeout: int,
        limit: int,
    ) -> tuple[Event, Event]: ...

    async def resolve_pending_initiate_for_transferee(
        self,
        relays: str,
        object_digest: str,
        author_pubkey_hex: str,
        query_timeout: int,
        limit: int,
    ) -> tuple[Event, Event]: ...

    async def resolve_single_active_chain_for_object(
        self,
        relays: str,
        object_digest: str,
        query_timeout: int,
        limit: int,
    ) -> tuple[Event, Event]: ...

    async def resolve_origin_from_prior_event(
        self,
        relays: str,
        prior_event_id_hex: str,
        query_timeout: int,
    ) -> tuple[Event, Event]: ...


class DefaultControlGuardPolicy:
    async def resolve_active_chain_for_controller(
        self,
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
        self,
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
        self,
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

    async def resolve_origin_from_prior_event(
        self,
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


DEFAULT_CONTROL_GUARD_POLICY = DefaultControlGuardPolicy()
