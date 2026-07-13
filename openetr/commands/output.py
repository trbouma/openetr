import json
from datetime import datetime
from pathlib import Path
from typing import Any

import click
from monstr.event.event import Event


def to_jsonable(value: Any) -> Any:
    if isinstance(value, Event):
        return to_jsonable(value.data())
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if hasattr(value, "tags") and isinstance(value.tags, list):
        return to_jsonable(value.tags)
    return value


def emit_json(payload: Any) -> None:
    click.echo(json.dumps(to_jsonable(payload), indent=2, sort_keys=True))
