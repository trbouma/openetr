# OpenETR Nostr Wire Format Specification

This document defines the current OpenETR Nostr wire format.

Its purpose is to express the OpenETR control model as concrete Nostr events, kinds, and tags so that implementations can:

- publish interoperable OpenETR events
- query and traverse OpenETR control history
- distinguish wire-level validity from later recognition or policy

## Status

Draft.

This is a current working specification for the OpenETR reference direction. It reflects the present `1415` / `1416` regular-event split and current tag conventions. It should not yet be treated as a final permanent registry decision.

## Scope

This specification defines:

- current event-kind assignments
- the meaning of the core OpenETR tags
- minimum wire-level event shapes
- object-history query and traversal expectations
- the distinction between wire format and recognition

This specification does not by itself determine:

- ownership
- title
- mandate
- legal effect
- priority
- recognition policy

Those remain outside the wire format and are determined by the applicable OpenETR policy, attestation, and recognition framework.

## Event Families

The current OpenETR wire format uses two event families:

- `kind 1415` for the origin event
- `kind 1416` for later control events
- legacy prototype `kind 31415` / `kind 31416` events may exist, but new OpenETR graph events use regular kinds `1415` / `1416`

### `1415` Origin Event

The origin event is the event by which a Controlled Object first enters the OpenETR scheme.

Its current wire-level role is to:

- bind the object digest into the OpenETR event graph
- express initial issuance or origin
- provide the starting point for later control traversal

### `1416` Control Event Family

The control-event family is used for later control-relevant actions concerning the same Controlled Object.

In the current working model, `1416` is a shared action family rather than a single semantic event type.

The action is carried by the `action` tag.

Current working `1416` actions are:

- `initiate`
- `accept`
- `terminate`
- `attest`
- `encumber`
- `discharge`
- `redeem`

The current reference CLI command mapping is summarized in [OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md](./OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md).

## Core Tag Model

The current OpenETR wire format uses the following core tags.

OpenETR distinguishes between:

- tags used as relay query anchors
- tags used as signed structured event data
- event `content` used as human-readable narrative or unstructured context

Only the first category requires relay indexing support.

Nostr relay filters express tag queries with leading `#` keys, such as `#o`, `#e`, or `#p`.

OpenETR therefore uses short, stable tags such as `o`, `e`, and `p` for object identity, graph traversal, and participant lookup.

OpenETR also uses named tags such as `name`, `size_bytes`, `digest_generated_at`, `domain`, `document_type`, `record_reference`, or `record_description` for structured metadata that does not need to be relay-queryable.

Those named tags are still part of the signed event. They should be read from the event tag list after the event has been retrieved through the core query anchors. Implementations should not need to parse the `content` field to recover structured OpenETR metadata.

The recommended convention is:

- use core single-letter tags for lookup and traversal
- use named tags for signed structured metadata
- use `content` for readable summaries, comments, or other unstructured event data

### `d`

`d` is not required for new regular OpenETR graph events.

Earlier prototype events used `d` as the addressable / replaceable slot:

- origin event: `d = <object_hex>`
- control event: `d = <object_hex>:<action>`

Readers may display `d` when inspecting legacy events, but new graph reconstruction should not rely on it.

### `o`

`o` is the Controlled Object identifier carried forward across the full object history.

In the current model:

- `o = <object_hex>`

The `o` tag is the primary object-centric query anchor for both origin and later control events.

### `e`

`e` links a control event to the prior event in the control graph.

In the current model, `e` should reference:

- the origin event id for the first later control event
- the immediately prior control-relevant event for later actions in the chain

This is the primary chain-traversal link.

### `p`

`p` identifies another participant relevant to the event.

Examples in the current model:

- transfer initiate: the transferee pubkey
- transfer accept: the accepted transfer counterparty where the implementation includes it
- encumber: the beneficiary or secured party
- redeem: the obligor
- attest: an optional subject or referenced participant

The exact semantics of `p` are action-dependent.

### `action`

`action` distinguishes the semantic subtype within the `1416` control-event family.

Examples:

- `["action", "initiate"]`
- `["action", "accept"]`
- `["action", "terminate"]`
- `["action", "attest"]`
- `["action", "encumber"]`
- `["action", "discharge"]`
- `["action", "redeem"]`

### Other Action-Specific Tags

The current working model may also use action-specific tags where needed.

Examples:

- `["enc", "<encumbrance_event_id_hex>"]` for a discharge event
- `["type", "<subtype>"]` for attestation or encumbrance typing
- `["ref", "<external_reference>"]` for external linkage

Current reference CLI usage:

| Tag | Used by | Meaning |
| --- | --- | --- |
| `enc` | `openetr discharge` | event id of the encumbrance being discharged |
| `type` | `openetr attest`, `openetr encumber` | action-specific subtype such as attestation type or encumbrance type |
| `ref` | `openetr attest`, `openetr encumber`, `openetr discharge`, `openetr redeem` | external reference or business reference |

These tags are part of the working wire convention. Their legal or operational effect depends on the applicable recognition profile.

### Named Structured Metadata Tags

Named metadata tags may be used when an implementation wants to carry signed structured data without requiring relay-level filtering on that data.

Examples for an origin event may include:

- `["name", "MLWR001.pdf"]`
- `["digest_generated_at", "2026-07-10T12:00:00+00:00"]`
- `["size_bytes", "282796"]`
- `["record_reference", "MLWR001"]`
- `["record_description", "Stored goods described in the receipt"]`

Examples for domain or policy context may include:

- `["domain", "mlwr"]`
- `["document_type", "warehouse_receipt"]`
- `["schema", "<schema_identifier_or_uri>"]`
- `["schema_digest", "<schema_digest_hex>"]`

These tags are:

- signed by the event author
- available to any verifier that retrieves the event
- useful for structured display, validation, policy mapping, and domain adapters
- not assumed to be relay-indexed unless an implementation explicitly chooses and tests relay support

Implementations should treat these named tags as structured event data.

The `content` field should not be the primary machine interface for such data. It is reserved for readable narrative, comments, or unstructured context that helps a person understand the event after the structured tags have been read.

## Minimum Event Shapes

The wire-level event structures below define the current minimum working format.

### Origin / Issue Event

- `kind = 1415`
- required tags:
  - `["o", "<object_hex>"]`
  - `["action", "issue"]`
- current implementation structured tags:
  - `["name", "<source_name>"]`
  - `["digest_generated_at", "<iso_8601_timestamp>"]`
  - `["size_bytes", "<decimal_byte_count>"]`
- optional structured tags:
  - `["action", "issue"]`
  - profile or identity tags such as `display_name`, `lei`, or related metadata where a given implementation chooses to include them
  - document metadata tags such as `record_reference` or `record_description`
  - domain tags such as `domain`, `document_type`, `schema`, or `schema_digest`

Recommended `content` convention:

- a short human-readable summary of the issue event
- no required machine parsing
- structured values are carried in tags

Control meaning:

- introduces the Controlled Object into the OpenETR scheme
- establishes the starting point for later control traversal

### Transfer Initiate Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<prior_event_id_hex>"]`
  - `["p", "<transferee_pubkey_hex>"]`
  - `["action", "initiate"]`

Control meaning:

- declares an intended transfer of control
- does not by itself settle whether the transfer is recognized as effective

### Transfer Accept Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<initiate_event_id_hex_or_prior_control_event_id_hex>"]`
  - `["action", "accept"]`
- recommended tags:
  - `["p", "<transferor_or_related_counterparty_pubkey_hex>"]`

Control meaning:

- records acceptance of a transfer
- may be required by policy before a transfer is recognized as effective

### Terminate Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "terminate"]`

Control meaning:

- records termination of the active OpenETR lifecycle for the object
- prevents later control transitions if the event is recognized as effective

### Attest Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<specific_event_id_being_attested>"]`
  - `["action", "attest"]`
- optional tags:
  - `["type", "<attestation_type>"]`
  - `["p", "<subject_pubkey_hex>"]`
  - `["ref", "<external_reference>"]`

Control meaning:

- records an authenticated assertion relating to the object or a control-relevant event
- targets the specific origin or control event identified by the `e` tag
- does not by itself change the Current Controller

### Encumber Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "encumber"]`
  - `["p", "<beneficiary_or_secured_party_pubkey_hex>"]`
- optional tags:
  - `["type", "<encumbrance_type>"]`
  - `["ref", "<external_reference>"]`

Control meaning:

- records a claimed encumbrance affecting the object
- does not by itself change the Current Controller

### Discharge Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "discharge"]`
  - `["enc", "<encumbrance_event_id_hex>"]`
- optional tags:
  - `["p", "<beneficiary_or_releasing_party_pubkey_hex>"]`
  - `["ref", "<external_reference>"]`

Control meaning:

- records release or satisfaction of a previously claimed encumbrance
- does not by itself change the Current Controller

### Redeem Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "redeem"]`
  - `["p", "<obligor_pubkey_hex>"]`
- optional tags:
  - `["ref", "<presentation_or_claim_reference>"]`

Control meaning:

- records presentation of the object to the obligor for performance
- does not by itself terminate the object

## Query and Traversal Model

OpenETR wire-level evaluation is object-centric first.

Implementations should generally:

1. determine the object digest
2. query origin events using `kind = 1415` and `#o`
3. query control events using `kind = 1416` and `#o`
4. group candidate chains by `e` references
5. evaluate those chains under local validity and recognition rules

In current practice, the object digest is commonly queried through the `o` tag across both event families.

The reference `openetr query` command currently derives and displays:

- the initial origin event
- matching `kind 1416` control events
- summary control chains from linked `e` references
- lifecycle state
- current controller
- profile information where available
- encumbrance totals, discharged encumbrances, and outstanding encumbrances

The web app query result uses the same query service and should therefore expose the same derived object-state view.

## Cryptographic Control Chain Verification

The OpenETR control chain is not database state maintained by a single application. It is a graph of signed Nostr events that any verifier can retrieve and independently evaluate.

For a candidate object history, an implementation should verify:

1. the origin event uses `kind = 1415` and carries the expected object identifier in `o`
2. each later control event uses `kind = 1416`
3. each event signature is valid for the event author
4. each event id matches the serialized event data under the Nostr event id rules
5. each event has the required minimum tags for its event shape
6. each event in the candidate chain carries the same `o` object identifier
7. each control event carries an `e` tag that points to the prior event being relied on
8. action-specific references such as `p`, `enc`, `type`, and `ref` are present where required by the action or local recognition profile
9. the linked chain can be replayed in order to derive lifecycle state, current controller, and outstanding control conditions

The `e` tag follows the Nostr convention for event references. In OpenETR, it is the primary cryptographic link between control-relevant events:

- for the first later control event, `e` should point to the origin event
- for later control-transition events, `e` should point to the immediately prior control-relevant event being extended
- for attestations, `e` should point to the specific event being attested
- for discharges, `enc` identifies the encumbrance being discharged, while `e` links the discharge into the current control chain

This produces an independently verifiable sequence of signed statements about the same controlled object. A verifier can reject events with invalid signatures, inconsistent object identifiers, missing required tags, or broken `e` references without relying on the application that originally displayed the state.

Cryptographic control-chain verification is still not the same thing as legal or operational recognition. After the chain is structurally verified, an implementation must apply the relevant recognition profile, domain adapter, policy rules, and applicable law to decide which structurally valid events are effective for a particular purpose.

## Current Controller Implications

At the wire-format level, events express candidate control history.

The wire format alone does not guarantee:

- singularity
- exclusive control
- final authoritative recognition

Instead, implementations derive candidate controller state by traversing the linked event chain and then applying local recognition rules.

In the current working model:

- the origin event identifies the initial issuer or controller position
- a recognized transfer initiate and transfer accept pair may move control
- a recognized termination event ends the active control lifecycle
- attestation, encumbrance, discharge, and redeem events do not by themselves change the Current Controller

## Validity and Recognition

This wire format separates structural validity from recognition.

Wire-level validity concerns questions such as:

- does the event use the correct kind
- are the required tags present
- is the object identifier well formed
- is the event signature valid
- is the referenced prior event structurally coherent
- where structured metadata is required by a profile, is it present in tags rather than only embedded in `content`

Recognition concerns questions such as:

- whether the signer was entitled to publish the action
- whether a transfer accept is required
- whether a transfer without attestation is sufficient in a narrow trusted-counterparty profile
- whether a termination should be recognized as effective
- whether actor legitimacy requirements have been satisfied

This wire format does not itself provide mandate or effect.

It provides the event structure and evidence from which mandate or effect may later be recognized under the applicable framework.

An event may therefore be:

- valid but not recognized
- recognized only under a specific policy profile
- invalid and therefore not capable of recognition

## Legacy Replaceable-Event Rationale

The earlier prototype model assumed that OpenETR graph events could be published as Nostr addressable / replaceable events within their author and `d` slot.

That is now treated as a legacy design stage. New OpenETR graph events use regular event kinds `1415` and `1416`.

The reason for the migration is important:

- relay persistence alone is not the source of effect
- graph continuity should be based on exact event ids
- a verifier should not silently relink old control events to a newer replacement event
- archives, attestations, local event stores, or relay diversity may still matter for evidentiary completeness

This means the wire format should be understood as the event grammar for OpenETR publication and traversal, not as a guarantee of effect by publication alone.

### Replacement And Control Graph Continuity

OpenETR control chains use event ids as graph links.

This creates a tension with Nostr replaceable-event behavior.

If an origin event is merely rebroadcast unchanged, it has the same event id and the control graph remains linked.

If the same author republishes the origin as a new replaceable event for the same `kind` and `d` coordinate, the new event normally has a different event id because the Nostr event id commits to the serialized event data, including fields such as `created_at`, tags, and content.

For example:

```text
same pubkey
same kind 31415
same d tag / object slot
new created_at or changed tags/content
=> different event id
```

Under ordinary replaceable-event relay behavior, the relay may stop returning the older origin event for that author/kind/`d` coordinate and return only the newer replacement.

That can break later control-chain traversal:

```text
old origin event id = A
later control event e tag -> A
new replacement origin event id = B
relay stops returning A
=> later control event does not extend B
=> verifier cannot fully traverse the chain unless A is available from another source
```

For this reason, the reference implementation moved origin and control graph events to regular event kinds.

A verifier should not silently relink old control events to the newer origin. The `e` tag points to a specific event id, not merely to the latest replaceable coordinate.

Recommended policy treatment:

- rebroadcasting the exact same event is safe because the event id is unchanged
- republishing an origin after dependent control events exist should produce a strong warning or policy failure
- missing prior events referenced by `e` should be reported as broken graph continuity
- archives, attestations, or local event stores may be needed to verify older graph links when relays have replaced earlier events
- domain policies may require origin immutability once the first control event is recognized

## Relationship to Other Specifications

This specification is intended to consolidate the wire-level aspects of the current model.

Related documents include:

- [OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md](./OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md)
- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [CANONICAL_ETR_TRANSACTION_SPEC.md](./CANONICAL_ETR_TRANSACTION_SPEC.md)
- [EVENT_KIND_REGISTRY.md](./EVENT_KIND_REGISTRY.md)
- [CONTROL_EVENT_MINIMUM_SHAPES.md](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [OPENETR_IMPLEMENTATION_ALIGNMENT_NOTE.md](./OPENETR_IMPLEMENTATION_ALIGNMENT_NOTE.md)
- [TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md](./TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md)

## Summary

The current OpenETR Nostr wire format is defined by:

- `1415` for origin
- `1416` for later control events
- `o` as the object-history anchor
- `e` as the control-chain link
- `action` as the semantic subtype within the control-event family
- named non-indexed tags as the convention for signed structured metadata
- `content` as human-readable or unstructured event data

This provides a coherent current working format for publishing, querying, and traversing OpenETR control history over Nostr while leaving recognition, mandate, attestation policy, and legal effect to higher layers.
