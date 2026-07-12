from __future__ import annotations

from functools import lru_cache
from importlib.resources import files
from random import choice

import yaml


OPENETR_TRIVIA_PATH = files("openetr").joinpath("openetr_trivia.yaml")


@lru_cache(maxsize=1)
def load_openetr_trivia_facts() -> tuple[str, ...]:
    with OPENETR_TRIVIA_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    facts = tuple(str(fact) for fact in data.get("facts", []) if fact)
    if not facts:
        raise RuntimeError("No OpenETR trivia facts were found in the packaged data file.")

    return facts


def random_openetr_trivia_fact() -> str:
    return choice(load_openetr_trivia_facts())
