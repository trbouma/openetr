"""Select bounded, optional retrieval hints from verified anchor events."""

import logging

from stroma import BlossomPool, Event

logger = logging.getLogger(__name__)


def anchor_blossom_hints(query_context: dict, digest: str) -> list[str]:
    hints = []
    for item in query_context.get("origin_events", []):
        event = item.get("event", {}).get("raw_event")
        if not isinstance(event, Event) or event.kind != 1415:
            continue
        if (not event.is_valid()
                or event.tags.get_tags_value("o") != [digest]
                or event.tags.get_tags_value("action") != ["issue"]):
            continue
        for tag in event.tags:
            if not tag or tag[0] != "blossom":
                continue
            try:
                if len(tag) != 2:
                    raise ValueError("Expected one Blossom origin")
                server = BlossomPool([tag[1]]).servers[0]
            except ValueError:
                logger.warning("Ignoring malformed or disallowed Blossom hint on event %s", event.id)
                continue
            if server not in hints:
                hints.append(server)
            if len(hints) >= 32:
                return hints
    return hints
