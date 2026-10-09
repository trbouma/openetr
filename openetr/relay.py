"""OpenETR operation deadlines around Stroma's native relay pool."""

import asyncio

from stroma import Event, PublishResult, RelayError, RelayPool


async def query_events(pool: RelayPool, filters: dict) -> list[Event]:
    try:
        return await asyncio.wait_for(pool.query(filters), timeout=pool.timeout)
    except TimeoutError as exc:
        raise RelayError("Relay query timed out; the available evidence may be incomplete.") from exc


async def publish_event(pool: RelayPool, event: Event) -> list[PublishResult]:
    try:
        return await asyncio.wait_for(pool.publish(event), timeout=pool.timeout)
    except (TimeoutError, RelayError) as exc:
        raise RelayError(
            "Publication was not confirmed by a relay. The event may have been stored; "
            f"query event {event.id} before retrying."
        ) from exc
