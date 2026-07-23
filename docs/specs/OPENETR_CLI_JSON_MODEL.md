# OpenETR CLI JSON Model

This specification describes the JSON output model for the `openetr` command line interface.

The JSON model is intended for machine-readable processes that need to issue, query, verify, or route OpenETR records without parsing human console text.

Examples include:

- workflow engines
- service wrappers
- REST API adapters
- agentic tools
- CI or batch jobs
- document-management systems
- warehouse receipt systems
- trade finance platforms
- verifier and recognition services

## Status

Draft.

This document reflects the current reference CLI direction. The JSON model should be treated as a reference component contract, not as the Nostr protocol wire format itself.

The signed event wire format is specified separately in [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md).

## Design Goal

The CLI JSON model exists so that another process can call `openetr`, inspect a single JSON document, and decide what to do next.

The design goals are:

- emit valid JSON on successful machine-readable command paths
- avoid prompts in JSON mode
- preserve normal shell exit status semantics
- expose signed event evidence without requiring text parsing
- separate command success from verifier-policy warnings
- include enough data for another process to continue a workflow
- avoid leaking private key material

Human-readable output remains the default. JSON mode is opt-in through `--json`.

## Relationship To The Wire Format

OpenETR events are Nostr events.

The Nostr event is the cryptographically signed evidence.

The CLI JSON output is a view over:

- local command inputs
- resolved OpenETR configuration
- signed Nostr events
- relay query results
- derived graph summaries
- warning or guard annotations

The JSON output does not replace the signed event. It is not itself the source of truth.

A verifier should treat JSON output as a convenient evidence package produced by the reference component. Where correctness matters, it should still rely on the included raw event data, event ids, signatures, tags, authors, and policy annotations.

## JSON Invocation

Commands that support machine-readable output expose:

```bash
openetr <command> --json
```

Examples:

```bash
openetr issue examples/mlwr-20260713.pdf --json
openetr query examples/mlwr-20260713.pdf --json
openetr encumber examples/mlwr-20260713.pdf --beneficiary lender --json
openetr transfer initiate examples/mlwr-20260713.pdf --transferee consignee --json
```

JSON mode should not ask an interactive confirmation question. If a guard would normally ask the user what to do, JSON mode should return a structured guard response and exit non-zero unless an explicit override such as `--force` is supplied.

## Response Envelope

Every JSON-capable command should emit one top-level JSON object.

The common top-level fields are:

| Field | Meaning |
| --- | --- |
| `ok` | Boolean command result. `true` means the command completed its requested operation. `false` means the command was blocked, rejected, or failed in a structured way. |
| `command` | CLI command surface that produced the response, such as `issue`, `query`, `issue-etr`, or `query-etr`. |
| `reason` | Machine-readable reason code when `ok` is `false`. |
| `warning` | Human-readable warning summary for a guard or policy warning. |
| `warnings` | Array of structured warning objects when the command succeeds but has policy or graph annotations. |
| `digest` | Hex object digest where applicable. |
| `object_id` | Bech32 OpenETR object identifier where applicable. |
| `digest_source` or `source` | Source file path when the command was invoked with a local file. |
| `relays` | Relay list used by the command. |

The envelope is intentionally simple so shell, service, and agent callers can branch on `ok`, `reason`, and `warnings[].code`.

## Exit Status

JSON mode preserves shell semantics.

Recommended behavior:

- exit `0` when `ok` is `true`
- exit non-zero when `ok` is `false`
- do not rely on warning presence alone to set a non-zero exit status

Warnings mean the command completed but discovered information a verifier or policy should inspect.

For example, `query --json` may return `ok: true` while also reporting multiple origin events in `warnings`.

## Structured Guard Responses

A guard is a command-level condition that blocks or asks for confirmation before continuing.

In human mode, a guard may print a warning and prompt.

In JSON mode, a guard should return structured JSON and avoid prompting.

Example duplicate origin guard:

```json
{
  "ok": false,
  "command": "issue",
  "reason": "duplicate_origin_event",
  "digest": "2976895f610a8e928249f365827c2fd385d2c7d71da0e4d3bf47845f8dcbdd20",
  "object_id": "nobj199mgjhmpp28f9qjf7djcylp06wza937hrkswf5alg7z9lrwtm5sqyenss3",
  "existing": {
    "count": 1,
    "same_author": true,
    "latest_event_id": "e8f9858243640ece19fb346de346d30ed1d8e6c835a04a20a480f7e295f69a73",
    "latest_issuer_npub": "npub1..."
  },
  "hint": "Re-run with --force to publish another origin event for this object."
}
```

A machine process can then decide whether to stop, query the existing record, route to human review, or intentionally re-run with `--force`.

## Successful Publish Responses

A successful publish command should include:

- `ok: true`
- `event_id`
- `kind`
- `pubkey` and `pubkey_hex`
- `object_id` and `digest` where applicable
- signed event `tags`
- event `content`
- raw signed `event`
- relay acknowledgement information when available
- post-publish query or verification information when available

Example shape:

```json
{
  "ok": true,
  "command": "issue",
  "event_id": "c70f3d7b8b3d3283b423e68d88fba49750c8795bfd13bd084ec31370e7de8e46",
  "kind": 1415,
  "object_id": "nobj199mgjhmpp28f9qjf7djcylp06wza937hrkswf5alg7z9lrwtm5sqyenss3",
  "digest": "2976895f610a8e928249f365827c2fd385d2c7d71da0e4d3bf47845f8dcbdd20",
  "verification": {
    "matched_object_filter": true,
    "exact_event_returned": true
  }
}
```

Relay acknowledgement data may be absent even when the event is successfully retrievable. A post-publish query that returns the exact event is often the stronger evidence for caller workflows.

## Query Responses

`query --json` returns an object-centric view of the OpenETR graph. `query-etr --json` remains available as a compatibility alias.

The top-level response identifies the command, object digest, object id, relays, and source. The `result` object contains the graph view.

Important `result` fields include:

| Field | Meaning |
| --- | --- |
| `origin_kind` | Origin event kind, currently `1415`. |
| `control_event_kind` | Control event kind, currently `1416`. |
| `relay_filter` | Origin event query filter. |
| `transfer_filter` | Control event query filter. |
| `count` | Number of origin events returned for the object query. |
| `origin_event_count` | Explicit count of origin events found. |
| `initial_event` | Selected origin event used as the initial event for the displayed candidate state. |
| `origin_events` | All origin events returned for the object. |
| `transfer_groups` | Control event groups linked by `e` references. |
| `summary_control_chains` | Human-readable chain summaries for compact display. |
| `lifecycle_state` | Candidate lifecycle state derived by the reference component. |
| `current_controller` | Candidate current controller derived by the reference component. |
| `encumbrance_summary` | Counts of encumbrance, discharged, and outstanding encumbrance events. |
| `outstanding_encumbrances` | Structured outstanding encumbrance items. |
| `warnings` | Structured warning annotations. |

The query result is deliberately evidentiary. It should not be treated as a final legal conclusion by itself.

## Event Views

Where the JSON response includes an event view, the current model includes:

| Field | Meaning |
| --- | --- |
| `event_role` | `origin` for kind `1415`; `control` for kind `1416`. |
| `action` | Value of the `action` tag when present. |
| `action_label` | Display label, such as `origin issue`, `transfer initiate`, or `encumber`. |
| `action_marker` | Compact graph marker, such as `++`, `->`, `+$`, or `-$`. |
| `id` | Event id hex. |
| `event_ref` | Bech32 event reference. |
| `kind` | Nostr event kind. |
| `author_hex` | Signer pubkey hex. |
| `author_npub` | Signer pubkey as npub. |
| `created_at` | Display timestamp. |
| `o_values` | Object tag values. |
| `d_values` | Legacy `d` values, if present. |
| `prior_event_id` | Prior event id from the `e` tag, if present. |
| `subject_npub` | Participant from the `p` tag, if present. |
| `structured_tags` | Non-core structured tags as name/value views. |
| `raw_event` | Raw signed Nostr event data. |

The `raw_event` field is important. It preserves the signed evidence so another process can independently inspect or verify event ids, pubkeys, signatures, content, and tags.

## Warnings

Warnings are structured annotations. They are not necessarily command failures.

Each warning should include:

| Field | Meaning |
| --- | --- |
| `code` | Stable machine-readable warning code. |
| `severity` | Usually `warning`; future values may include `info` or `error`. |
| `message` | Human-readable explanation. |
| Additional fields | Warning-specific data. |

Example:

```json
{
  "code": "multiple_origin_events",
  "severity": "warning",
  "origin_event_count": 2,
  "event_ids": [
    "e8f9858243640ece19fb346de346d30ed1d8e6c835a04a20a480f7e295f69a73",
    "c70f3d7b8b3d3283b423e68d88fba49750c8795bfd13bd084ec31370e7de8e46"
  ],
  "selected_initial_event_id": "e8f9858243640ece19fb346de346d30ed1d8e6c835a04a20a480f7e295f69a73",
  "selection_basis": "earliest origin event by created_at/id"
}
```

A verifier policy should inspect warnings and decide what recognition effect to give them.

This aligns with [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md): policy issues should normally be surfaced as annotations rather than hiding signed evidence.

## Policy And Recognition

JSON output can say:

- what signed evidence was found
- what the reference component derived as candidate state
- what warnings were detected
- which event was selected as the initial basis for a candidate view

JSON output should not claim final legal effect by itself.

Recognition remains a policy concern.

For example, a downstream verifier may decide that `multiple_origin_events` is:

- acceptable but logged
- warning-only
- a reason to require human review
- a reason to select a newer origin event
- a reason to refuse recognition
- resolved by an external registry, trust framework, or domain rule

OpenETR's JSON model makes that decision inspectable. It does not force one policy result on every organization.

## Privacy And Secret Handling

JSON output must not include private signing keys, root `nsec` values, profile signer secrets, recovery phrases, or other secret key material.

The JSON model may include:

- public `npub` values
- public key hex values
- event ids
- event signatures
- event content
- event tags
- profile metadata already published as Nostr kind `0` metadata

This is sufficient for machine-readable workflows without exposing local root or profile secrets.

## Agent-Friendly Use

An agent or service wrapper should generally:

1. run an `openetr` command with `--json`
2. parse stdout as JSON
3. check process exit status
4. check `ok`
5. branch on `reason` if `ok` is false
6. inspect `warnings` even when `ok` is true
7. use `raw_event` and event ids for evidence and audit trails
8. apply local or domain-specific verifier policy before assigning recognition effect

For example:

- `ok=false` and `reason=duplicate_origin_event`: stop or route to review unless the workflow intentionally permits `--force`
- `ok=true` and `warnings[].code=multiple_origin_events`: continue only if the selected verifier policy recognizes one origin basis
- `ok=true` and `verification.exact_event_returned=true`: treat the publish as relay-query verified for workflow purposes

## Compatibility Notes

The JSON model may evolve as the component matures.

Consumers should prefer stable fields:

- `ok`
- `command`
- `reason`
- `warnings[].code`
- `event_id`
- `object_id`
- `digest`
- `result.initial_event.id`
- `result.origin_events`
- `result.transfer_groups`
- `result.current_controller`
- `result.lifecycle_state`
- `raw_event`

Consumers should tolerate additional fields.

Consumers should not depend on object key ordering, display-only chain labels, or exact human-readable message text when a stable code is available.

## Non-Goals

The JSON model does not:

- replace the Nostr wire format
- define legal effect
- define final recognition policy
- require any particular relay service
- expose private keys
- guarantee that every organization will derive the same recognized state

It is a machine-readable interface to the OpenETR reference component and its current evidence model.
