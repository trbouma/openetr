# Component And CLI

OpenETR is designed to be usable through multiple implementation surfaces.

## Installable Python Component

The `openetr` package is an installable Python component.

It contains the reusable control, query, publish, profile, relay, and verifier-oriented logic.

The FastAPI demonstration app is intentionally separate from the packaged component.

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
