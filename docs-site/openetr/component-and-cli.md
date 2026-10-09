# Component And CLI

OpenETR is designed to be usable through multiple implementation surfaces.

## Installable Python Component

The `openetr` package is an installable Python component.

It contains the reusable control, query, publish, profile, relay, and verifier-oriented logic.

The FastAPI demonstration app is intentionally separate from the packaged component.

## Stroma Transport

OpenETR now uses Stroma throughout the component, CLI, and web app. Monstr is
deprecated and removed as a runtime dependency; there is no Monstr fallback or
compatibility client in OpenETR. Stroma's native `RelayPool` queries the selected
relays, validates returned signatures and event IDs, and deduplicates events by
ID. OpenETR applies operation deadlines and its own graph/ruleset evaluation.

Publication is awaited and requires at least one relay acknowledgement. That
acknowledgement is not consensus, durable-retention assurance, or legal recognition.
Read-back verification remains separate, including the existing any/majority/all
verification modes. A publication timeout is reported as unconfirmed because a
relay may have stored the event even if its acknowledgement was lost. Query the
event ID before retrying. A query failure must not be interpreted as proof that
no record exists.

Wire kinds, tags, canonical event IDs, signatures, nsec/npub identifiers, salted
configuration addresses, and NIP-44 v2 encrypted profiles remain unchanged.
Existing records do not need to be republished. Code that imports OpenETR services
and passes event/key objects should now use `stroma.Event` and `stroma.Keys`.
Raw wire timestamps remain Unix integers; projected display timestamps remain
date/time values, rendered in UTC.

Use Python 3.11-3.13 and Poetry 2.2 or newer. The Stroma Git revision is pinned
in `pyproject.toml` and the lockfile. Git is required when installing from source;
the Docker builder includes it. The experimental Bitcoin helpers retain an
explicit `secp256k1` dependency, separate from Stroma's Nostr signing implementation.

The legacy `--ssl-disable-verify` option is retained only to provide an explicit
unsupported-option error. Stroma connections verify TLS certificates; the flag
is never silently ignored. Development relays may still use `ws://` where
appropriate.

Migration regression checks use synthetic keys and local WebSocket relays, not
production identities or live record publication:

```sh
poetry run pip install -r app/requirements.txt
poetry run python -m unittest discover -s tests -v
```

## CLI Surface

The `openetr` CLI is the human and automation command surface.

Common commands include:

```sh
openetr issue examples/mlwr-20260713.pdf
openetr query examples/mlwr-20260713.pdf
openetr transfer initiate examples/mlwr-20260713.pdf --transferee consignee
openetr encumber examples/mlwr-20260713.pdf --beneficiary lender
openetr discharge examples/mlwr-20260713.pdf --encumbrance-event <event-id>
```

The CLI is intended to work well from a shell, including workflows where inputs and outputs are piped or consumed by agents.

## JSON Mode

Machine-readable callers can use `--json`:

```sh
openetr issue examples/mlwr-20260713.pdf --json
openetr query examples/mlwr-20260713.pdf --json
```

JSON mode is a component contract for automation. It does not replace the signed Nostr event. It packages command inputs, relay results, signed event data, derived graph state, warnings, and guard results into one JSON object.

## Webapp And API Surface

The demonstration FastAPI app calls the same underlying OpenETR component and services.

An integrator may:

- use the demo app directly;
- adapt its REST-style routes;
- import the Python component;
- run the CLI from an automation environment;
- integrate directly at the Nostr wire-format layer.

## Source Specs

- [OpenETR CLI JSON Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CLI_JSON_MODEL.md)
- [OpenETR CLI Implementation Walkthrough](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md)
- [Multi-Modality Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/MULTI_MODALITY_ARCHITECTURE_NOTE.md)
