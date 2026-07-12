# Regular Event Kind Migration Design Note

This note discusses a proposed change to the OpenETR control graph wire format:

> Move OpenETR origin and control graph events from addressable / replaceable Nostr event kinds to regular Nostr event kinds.

This is the design note for the migration now reflected in the reference implementation.

## Status

Implemented reference direction.

The reference OpenETR component and CLI now publish new origin/control graph events as regular `kind 1415` and `kind 1416` events. The former `kind 31415` and `kind 31416` assignments are retained in the documentation as legacy prototype kinds.

## Legacy Prototype Model

The earlier OpenETR prototype used:

- `kind 31415` for origin / issue events
- `kind 31416` for later control events

Under NIP-01, event kinds in the `30000 <= kind < 40000` range are addressable by:

```text
kind + pubkey + d tag value
```

Only the latest event for that addressable coordinate is expected to be retained by relays. Older versions may be discarded.

The current prototype therefore uses the `d` tag as an addressable action slot:

```text
origin:
  ["d", "<object_digest>"]
  ["o", "<object_digest>"]

control event:
  ["d", "<object_digest>:<action>"]
  ["o", "<object_digest>"]
  ["action", "<action>"]
```

This worked well for early experimentation because it gave each author/object/action a replaceable slot.

## Problem

The OpenETR control graph is event-id based.

Later control events use `e` tags to reference the exact prior event id being extended or attested.

That creates tension with addressable / replaceable event behavior.

If an origin event is merely rebroadcast unchanged, its event id remains the same and the graph remains linked.

If an origin event is republished as a new addressable event for the same `kind + pubkey + d` coordinate, the new event normally has a different event id because Nostr event ids commit to the serialized event data, including `created_at`, tags, and content.

Under ordinary addressable-event relay behavior, the relay may stop returning the older origin event.

That can orphan later control events:

```text
old origin event id = A
later control event e tag -> A
new replacement origin event id = B
relay stops returning A
=> later control event does not extend B
=> verifier cannot fully traverse the graph unless A is available elsewhere
```

This is a poor fit for the root of a cryptographic control graph.

The same concern applies to any graph node that may later be referenced by `e`.

## Adopted Direction

OpenETR should move the core control graph to regular Nostr events.

Current experimental regular kinds:

| Kind | Purpose | NIP-01 behavior |
| --- | --- | --- |
| `1415` | OpenETR origin / issue event | regular event |
| `1416` | OpenETR control event family | regular event |

These are in the NIP-01 regular-event range:

```text
1000 <= kind < 10000
```

At the time of this design note, `1415` and `1416` do not appear in the Nostr NIPs event-kind registry. They should be treated as experimental OpenETR assignments until an upstream registration decision is made.

The old prototype assignments would become legacy:

| Kind | Status | Notes |
| --- | --- | --- |
| `31415` | legacy prototype | addressable origin event |
| `31416` | legacy prototype | addressable control event family |

## Tag Model After Migration

The tag model can become simpler.

Recommended core tags:

| Tag | Purpose | Relay indexing expectation |
| --- | --- | --- |
| `o` | controlled object digest / object-wide query anchor | indexed |
| `e` | prior event id / graph edge | indexed |
| `p` | participant pubkey where participant lookup matters | indexed |
| `action` | semantic action within the event family | not assumed indexed |

The `o` tag should remain the primary object query anchor.

Example query:

```json
{
  "kinds": [1415, 1416],
  "#o": ["<object_digest>"]
}
```

The `action` tag should carry the event meaning:

```text
["action", "issue"]
["action", "initiate"]
["action", "accept"]
["action", "encumber"]
["action", "discharge"]
["action", "redeem"]
["action", "terminate"]
["action", "attest"]
```

Because `action` does not need relay indexing, it can be a named tag. The verifier can retrieve all events for the object using `#o` and inspect `action` locally.

## Query And Reconstruction Model

The regular-event design assumes that the control graph can be retrieved by object and reconstructed locally.

The `o` tag gives the verifier the candidate event set:

```text
o = find the graph
```

The `e` tag gives the verifier the graph topology inside that event set:

```text
e = walk the graph
```

The `action` tag tells the verifier how to interpret each node:

```text
action = understand each node
```

The selected verifier policy then decides what effect to give the reconstructed graph:

```text
policy = decide effect
```

The verifier flow is therefore:

1. query regular OpenETR event kinds by `#o`
2. collect all candidate origin and control events for the object
3. verify event ids and signatures
4. index retrieved events by event id
5. identify origin candidates
6. follow `e` links to build candidate chains
7. inspect `action` tags and action-specific tags such as `p`, `enc`, `type`, and `ref`
8. apply the selected verifier policy

This means `d` is not required to reconstruct the control graph if every graph event carries `o`, every non-origin graph event carries the necessary `e` link, and every graph event carries enough action metadata to interpret its role.

## Role Of The `d` Tag

If origin and control events become regular events, the `d` tag is no longer needed for core graph semantics.

In the prototype, `d` meant:

```text
origin:
  d = <object_digest>

control:
  d = <object_digest>:<action>
```

That was useful because addressable events use `d` as part of the relay replacement coordinate.

In the proposed regular-event model:

- `o` identifies the object
- `e` links to the prior event
- `action` states the semantic act
- the event id identifies the graph node

Therefore `d` can be removed from new origin/control graph events, or emitted only temporarily for legacy/backward compatibility during migration.

The preferred end state is:

```text
origin event:
  kind 1415
  ["o", "<object_digest>"]
  ["action", "issue"]

control event:
  kind 1416
  ["o", "<object_digest>"]
  ["e", "<prior_event_id>"]
  ["action", "<action>"]
  ...action-specific tags...
```

## Example Event Shapes

### Origin / Issue

```text
kind = 1415
tags:
  ["o", "<object_digest>"]
  ["action", "issue"]
  ["name", "<source_name>"]
  ["digest_generated_at", "<timestamp>"]
  ["size_bytes", "<byte_count>"]
```

### Transfer Initiate

```text
kind = 1416
tags:
  ["o", "<object_digest>"]
  ["e", "<prior_event_id>"]
  ["p", "<transferee_pubkey>"]
  ["action", "initiate"]
```

### Transfer Accept

```text
kind = 1416
tags:
  ["o", "<object_digest>"]
  ["e", "<initiate_event_id_or_prior_control_event_id>"]
  ["action", "accept"]
```

### Encumber

```text
kind = 1416
tags:
  ["o", "<object_digest>"]
  ["e", "<prior_event_id>"]
  ["p", "<beneficiary_or_secured_party_pubkey>"]
  ["action", "encumber"]
  ["type", "<encumbrance_type>"]
  ["ref", "<external_reference>"]
```

### Discharge

```text
kind = 1416
tags:
  ["o", "<object_digest>"]
  ["e", "<prior_event_id>"]
  ["action", "discharge"]
  ["enc", "<encumbrance_event_id>"]
  ["p", "<releasing_party_pubkey>"]
```

## Verifier Policy Implications

Regular events do not prevent duplicate or conflicting events from being published.

That is acceptable.

OpenETR is an open signed-event system. The verifier should enumerate the graph and apply policy.

With regular events:

- duplicate origins remain visible rather than being hidden by relay replacement
- conflicting transfer chains remain visible
- corrections become later signed events or attestations rather than silent rewrites
- missing prior `e` links remain graph-continuity warnings

The generic verifier policy should continue to warn about:

- multiple origins for the same object
- multiple origins by the same issuer for the same object
- competing control chains
- missing prior events referenced by `e`
- policy-specific violations

The important change is that relay replacement should no longer be able to hide a graph root or graph node merely because a newer event was published for the same addressable coordinate.

## Migration Strategy

Recommended implementation plan:

1. Add new constants:
   - `ORIGIN_EVENT_KIND = 1415`
   - `CONTROL_EVENT_KIND = 1416`
   - legacy constants for `31415` and `31416`

2. Update event builders:
   - publish new origin events as `1415`
   - publish new control events as `1416`
   - emit `o`, `e`, `p`, `action`, and action-specific tags
   - stop relying on `d` for graph semantics

3. Update query paths:
   - query current kinds by `#o`
   - optionally query legacy kinds by `#o` during a transition period
   - stop using combined `#d` and `#o` confirmation filters for new graph events

4. Update verifier output:
   - show event kind clearly
   - show whether an event is current-kind or legacy-kind
   - warn on legacy graphs if needed
   - continue warning on multiple origins and broken `e` links

5. Update docs:
   - wire-format spec
   - event kind registry
   - control event minimum shapes
   - CLI walkthrough
   - MLWR profile and webapp domain adapter notes
   - system integration considerations

6. Decide compatibility mode:
   - read-only legacy support
   - dual-query support
   - or clean break because published events are still early prototype data

## Implementation Plan

This section translates the migration strategy into a practical implementation sequence.

The plan assumes a clean current-kind write path using `1415` / `1416`, with optional read-only legacy support for `31415` / `31416` if needed during review or demonstration.

### Phase 1: Centralize Event Kind Constants

Update the OpenETR constants so the regular event kinds are the current defaults.

Likely touchpoints:

- `openetr/config.py`
- `openetr/control.py`
- `openetr/services/issue_etr.py`
- `openetr/services/control_events.py`
- `openetr/services/query_etr.py`
- `openetr/commands/publish.py`
- `openetr/commands/query.py`

Recommended constants:

```python
ORIGIN_EVENT_KIND = 1415
CONTROL_EVENT_KIND = 1416
LEGACY_ORIGIN_EVENT_KIND = 31415
LEGACY_CONTROL_EVENT_KIND = 31416
```

The user-facing default kind should move from `31415` to `1415`.

Any profile/config field named generically as `kind` should be reviewed. If it only means origin kind, either document that clearly or rename internally to `origin_kind` where practical.

### Phase 2: Update Origin Event Publishing

Update origin / issue publishing so new origin events are regular events.

Expected behavior:

- publish `kind = 1415`
- include `["o", "<object_digest>"]`
- include `["action", "issue"]`
- include structured metadata tags such as `name`, `digest_generated_at`, `size_bytes`, `record_reference`, `record_description`, `domain`, and `document_type` where applicable
- stop relying on `["d", "<object_digest>"]` for graph semantics

Open question for implementation:

- either remove `d` immediately from new origin events
- or emit `d` temporarily as a legacy display aid while ensuring no query or graph logic depends on it

Preferred end state:

```text
kind 1415
["o", "<object_digest>"]
["action", "issue"]
```

### Phase 3: Update Control Event Publishing

Update transfer, encumbrance, discharge, redeem, terminate, and attest publishing to use `kind = 1416`.

Expected behavior:

- publish `kind = 1416`
- include `["o", "<object_digest>"]`
- include `["e", "<prior_event_id>"]`
- include `["action", "<action>"]`
- include `p`, `enc`, `type`, and `ref` where required by the action
- stop relying on `["d", "<object_digest>:<action>"]` for graph semantics

The event id is now the graph node identity. The `e` tag is the graph edge. The `action` tag is the semantic classifier.

### Phase 4: Update Query And Verification

Update query services to retrieve by object using `#o`.

Current-kind query:

```json
{
  "kinds": [1415, 1416],
  "#o": ["<object_digest>"]
}
```

Implementation choices:

- query `1415` and `1416` together, then split locally by kind
- or keep separate origin/control queries while using `#o` for both

The verifier should:

1. verify signatures and event ids
2. index retrieved events by event id
3. identify origin candidates from `kind = 1415`
4. identify control candidates from `kind = 1416`
5. reconstruct chains by following `e`
6. inspect `action`
7. apply generic verifier policy

The query path should stop using combined `#d` and `#o` filters for new graph events.

### Phase 5: Handle Legacy Events

Decide whether to support legacy reads.

Recommended default:

- write only `1415` / `1416`
- optionally read `31415` / `31416` in a clearly labeled legacy mode

If legacy read support is kept, query output should label events as:

```text
current-kind
legacy-addressable-kind
```

Legacy events should not be silently mixed into current regular-event chains without a policy annotation.

Possible warning codes:

- `legacy_origin_kind`
- `legacy_control_kind`
- `mixed_kind_chain`

### Phase 6: Update CLI Output And Commands

Update CLI text that mentions `31415`, `31416`, `d`, or replaceable events.

Likely commands:

- `openetr issue-etr`
- `openetr query-etr`
- `openetr transfer initiate`
- `openetr transfer accept`
- `openetr encumber`
- `openetr discharge`
- `openetr redeem`
- `openetr terminate-etr`
- `openetr info`

Expected output changes:

- origin output should show `Kind: 1415`
- control output should show `Kind: 1416`
- query output should emphasize `o`, `e`, and `action`
- display of `d` should be removed, hidden, or labeled as legacy if retained

### Phase 7: Update Web App

The web app should continue calling the shared OpenETR services rather than duplicating wire-format logic.

Expected updates:

- MLWR issue should produce `kind = 1415`
- MLWR transfer/control actions should produce `kind = 1416`
- query result pages should label new kinds correctly
- event data display should emphasize `o`, `e`, `action`, participant, and structured tags
- any text saying `kind 31415`, `kind 31416`, or `d value` should be reviewed

The MLWR domain adapter should remain domain-facing. It should not expose the migration as a user workflow concern beyond event details shown in query/debug output.

### Phase 8: Update Documentation

Update docs after the code behavior is settled.

Required docs:

- `OPENETR_NOSTR_WIRE_FORMAT_SPEC.md`
- `EVENT_KIND_REGISTRY.md`
- `CONTROL_EVENT_MINIMUM_SHAPES.md`
- `OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md`
- `OPENETR_GENERIC_VERIFIER_POLICY.md`
- `OPENETR_MLWR_PROFILE.md`
- `MLWR_WEBAPP_DOMAIN_ADAPTER_DESIGN_NOTE.md`
- `SYSTEM_INTEGRATION_CONSIDERATIONS.md`

Docs should clearly mark `31415` / `31416` as legacy prototype kinds once implementation moves.

### Phase 9: Verification

Minimum verification after implementation:

```bash
.venv/bin/python -m compileall app openetr
.venv/bin/openetr issue-etr examples/MLWR001.pdf
.venv/bin/openetr query-etr examples/MLWR001.pdf
.venv/bin/openetr transfer initiate examples/MLWR001.pdf --transferee <profile-or-npub>
.venv/bin/openetr transfer accept examples/MLWR001.pdf
.venv/bin/openetr query-etr examples/MLWR001.pdf
```

The final query should demonstrate:

- origin event kind `1415`
- control event kind `1416`
- graph retrieval by `#o`
- chain reconstruction by `e`
- action interpretation by `action`
- no dependency on `d`

If web app verification is included:

- run the FastAPI app
- issue a receipt from the MLWR page
- query the receipt
- perform at least one control action
- query again and confirm the result page shows the expected graph state

## Compatibility Considerations

The project is still early.

Existing published `31415` / `31416` events may be treated as prototype events.

Possible approaches:

| Approach | Behavior | Tradeoff |
| --- | --- | --- |
| Clean break | New code only reads/writes `1415` / `1416` | simplest implementation, old demo events ignored |
| Legacy read support | New code writes `1415` / `1416` but can query old `31415` / `31416` | smoother demos, more code paths |
| Dual publish | Publish both old and new kinds | not recommended; creates unnecessary ambiguity |

Given the early stage, a clean break or read-only legacy support is preferable to dual publishing.

## Open Questions

- Should `d` be removed immediately from new graph events, or retained temporarily as a legacy display aid?
- Should all `1416` control actions remain in one event family, or should some actions eventually get separate regular kinds?
- Should OpenETR pursue upstream event-kind registration for `1415` and `1416`?
- Should a correction/supersession event shape be defined for origin metadata errors?
- Should the verifier reject legacy addressable graph events by default or merely label them as legacy?

## Recommendation

Adopt regular event kinds for the OpenETR control graph:

```text
1415 = origin / issue
1416 = control event family
```

Use:

```text
o      = object query anchor
e      = event-id graph edge
p      = participant reference
action = semantic action
```

Do not use addressable / replaceable event behavior for graph nodes that may be referenced by `e`.

Reserve replaceable or addressable event kinds for data that is naturally mutable, such as:

- profile metadata
- relay lists
- aliases
- configuration records
- summaries
- indexes
- derived views

The control graph itself should be made of regular signed events.
