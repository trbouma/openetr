# OpenETR Nostr Wire Format Specification

This document defines the current OpenETR Nostr wire format.

Its purpose is to express the OpenETR protocol model as concrete Nostr events, kinds, and tags so that implementations can:

- publish interoperable OpenETR events
- query and traverse OpenETR control history
- distinguish wire-level validity from later recognition or policy

## Status

Draft.

This is a current working specification for the OpenETR reference direction. It reflects the present `1415` / `1416` regular-event split and current tag conventions. It should not yet be treated as a final permanent registry decision.

The OpenETR reference app implements the optional `blossom` Anchor Event hint
convention using Stroma's `BlossomPool`: opt-in artifact storage precedes signing,
and retrieval combines verified anchor hints with configured servers.
Existing anchors without hints remain compatible.

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

Nostr carries the events. OpenETR determines their consequences. Relays
transport and preserve signed evidence; they do not determine OpenETR
consequential state.

## Key-Based Identifier Mapping

A **Key-Based Identifier (KBI)** is an identifier whose canonical value is
public-key verification material or a deterministic encoding of that material.
A KBI identifies a signing key; it does not, by itself, establish actor
identity, authority, role, or recognition.

In this binding, the 32-byte Nostr public key is the KBI. Its 64-character
lowercase hexadecimal representation is the canonical wire encoding used in
NIP-01 events and relay filters. `npub` is the NIP-19 human-readable encoding
of the same KBI.

## Event Families

The current OpenETR wire format uses two event families:

- `kind 1415` for the Anchor Event
- `kind 1416` for later Evidence Events

Both are regular events. Addressable or replaceable events are not part of the
OpenETR DCR graph.

### Byte Identity

OpenETR uses **byte identity** for the Digital Artifact: the identity of the
artifact is derived from its exact bytes. In this Nostr binding, byte identity
is carried as the 64-character lowercase SHA-256 digest of those bytes.

If the bytes change, the byte identity changes. A visually identical PDF, a
re-encoded image, or a differently serialized data package may therefore be a
different Digital Artifact at the protocol layer. Related artifacts can be
linked by Evidence Events, but they do not share the same `o` value unless
their bytes produce the same digest.

### `1415` Anchor Event

The Anchor Event is the first candidate DCR record concerning a Digital Artifact.

**Digital Controllable Record (DCR)** is the protocol evidence term: it is one
end-verifiable event or a graph of related events concerning the Digital
Artifact identified by the `o` digest. A DCR is not the artifact and does not,
by itself, assert derived or recognized consequential state.

Its current wire-level role is to:

- bind the Digital Artifact byte identity into the OpenETR event graph
- provide the candidate evidence from which an identified ruleset may derive
  initial anchored state
- provide the starting point for Publisher Notice chains and extension graphs

A valid Anchor Event forms a one-record candidate DCR. Evaluation of that DCR
under OpenETR Core Record Ruleset 1.0 establishes initial anchored
Consequential State and brings the identified Digital Artifact into the
OpenETR Digital Original model. The
event does not by itself establish that the candidate is uniquely authoritative
or compel recognition, standing, or legal or operational effect.

A single object digest may have more than one Anchor Event. Different issuers, systems, communities, or recognition contexts may anchor the same object. Verifiers should therefore treat each `1415` event as a candidate anchor and apply the relevant recognition profile to decide which anchor, if any, is authoritative for the purpose at hand.

### `1416` Evidence Event Family

The Evidence Event family extends the DCR with signed evidence of later actions
concerning the same Digital Artifact. Some actions change control; others
contribute evidence from which different Consequential State may be derived.

In the current working model, `1416` is a shared action family rather than a single semantic event type.

The action is carried by the `action` tag.

Current working `1416` actions are:

- `initiate`
- `accept`
- `terminate`
- `attest`
- `notice`
- `encumber`
- `discharge`
- `redeem`

The current reference CLI command mapping is summarized in [OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md](./OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md).
Publisher Notice publication is specified by Core Record Ruleset 1.0 but is not
yet exposed by the reference CLI.

## Core Tag Model

The current OpenETR wire format uses the following core tags.

OpenETR distinguishes between:

- tags used as relay query anchors
- tags used as signed structured event data
- event `content` used as human-readable narrative or unstructured context

Only the first category requires relay indexing support.

Nostr relay filters express tag queries with leading `#` keys, such as `#o`, `#e`, or `#p`.

OpenETR therefore uses short, stable tags such as `o`, `e`, and `p` for object identity, graph traversal, and participant lookup.

OpenETR also uses named tags such as `name`, `size_bytes`, `digest_generated_at`, `domain`, `document_type`, `record_reference`, `record_description`, or `blossom` for structured metadata that does not need to be relay-queryable.

Those named tags are still part of the signed event. They should be read from the event tag list after the event has been retrieved through the core query anchors. Implementations should not need to parse the `content` field to recover structured OpenETR metadata.

The recommended convention is:

- use core single-letter tags for lookup and traversal
- use named tags for signed structured metadata
- use `content` for readable summaries, comments, or other unstructured event data

### `o`

`o` is the Digital Artifact byte identity carried forward across the full DCR history.

In the current model:

- `o = <object_hex>`

The `o` tag carries the SHA-256 digest of the artifact's exact bytes and is the primary object-centric query anchor for both Anchor Events and later Evidence Events.

The `o` tag is a relay-query anchor. It should not be confused with the `1415` Anchor Event, which is a signed event in the control graph.

### `e`

`e` links an Evidence Event to the prior event in the candidate DCR graph.

In the current model, `e` should reference:

- the Anchor Event id for the first later Evidence Event
- the immediately prior control-relevant event for later actions in the chain

This is the primary chain-traversal link.

No separate `origin` or `anchor` tag is required. A verifier identifies the
Anchor Event by following the signed `e` references backward until the chain
terminates at a valid `kind 1415` event carrying the same `o` value. An
implementation may encounter an `origin` tag on early OpenETR events, but it
is non-normative and should not be relied upon for graph reconstruction.

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

`action` distinguishes the semantic subtype within the `1416` Evidence Event family.

Examples:

- `["action", "initiate"]`
- `["action", "accept"]`
- `["action", "terminate"]`
- `["action", "attest"]`
- `["action", "notice"]`
- `["action", "encumber"]`
- `["action", "discharge"]`
- `["action", "redeem"]`

### Other Action-Specific Tags

The current working model may also use action-specific tags where needed.

Examples:

- `["enc", "<encumbrance_event_id_hex>"]` for a discharge event
- `["type", "<subtype>"]` for attestation or encumbrance typing
- `["notice_type", "<publisher_position>"]` for a Publisher Notice
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

Examples for an Anchor Event may include:

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

## Artifact Retrieval

### Blossom Retrieval Hints

An Anchor Event MAY carry zero or more optional `blossom` tags:

```json
["blossom", "https://blossom.example.org"]
```

Each tag has exactly two string elements: the tag name and a Blossom server
origin. Publishers MUST use an absolute HTTPS origin, with no credentials,
non-root path, query, or fragment. A port MAY be specified. Publishers SHOULD
normalize the scheme and hostname to lowercase, omit the default HTTPS port
and trailing slash, and emit at most one tag per normalized origin. Readers
SHOULD accept a root trailing slash and normalize equivalent origins before
deduplicating them. Plain HTTP or private storage may be configured locally,
but is not advertised by this interoperable public-hint convention.

Repeat the tag for multiple locations; do not put a comma-separated server
list in a single tag. The value is a server origin, not a complete blob URL
or another artifact identifier. The candidate blob locator is constructed as
`<server-origin>/<o-digest>`. The `o` tag remains the canonical byte identity.

`blossom` is signed structured metadata, not a relay-query anchor. No
`#blossom` indexing or filtering support is required. Retrieve the Anchor
Event through `#o` and read its tag list, not its `content`.

#### Publication And Confirmation

When an issuance workflow requests Blossom storage, it MUST finish its
storage-confirmation step before constructing the final anchor tags and
signing the Anchor Event. A server MUST be advertised only after a GET
from that origin returns bytes whose SHA-256 matches `o`. This applies both
to new uploads and to copies already available at the server. A successful
PUT response or HEAD response alone is not digest-verified read-back.

For the reference publication workflow, the storage success requirement is
selected locally from the following options, defaulting to `any`:

| Requirement | Confirmed locations required for N unique target origins |
| --- | --- |
| `any` | 1 |
| `half` | `ceil(N / 2)` |
| `majority` | `floor(N / 2) + 1` |
| `all` | N |

An empty target set is an error when storage is requested. Deduplicate the
targets before calculating N; unavailable, rejected, and unconfirmed targets
remain in the denominator. Distinct origins need not be independently operated.
These are availability-confirmation thresholds, not consensus or independent
custodian guarantees. The selected threshold is not a new wire tag and cannot
be inferred from the number of hints in an anchor.

The workflow MUST report whether the requirement was met and the individual
outcomes. If it was not met, it MUST NOT silently proceed with automatic
anchor publication as though storage succeeded. An explicit application
decision may instead proceed without the requested storage assurance; it
must not turn unconfirmed locations into confirmed hints. Issuing an anchor
without requesting Blossom storage remains valid.

After the requirement is met, the workflow SHOULD include every confirmed
location it intends to advertise, not only enough locations to meet the
threshold. Rejected or unconfirmed uploads MUST NOT be represented as
confirmed locations. An upload timeout is ambiguous: the workflow SHOULD
attempt digest-verified retrieval before considering another upload.

A hint is the publisher's signed retrieval suggestion. It is not independent
proof that a read-back occurred, that a server physically retains a copy, or
that the artifact will remain available. Neither the tag nor a server response
establishes ownership, authority, retention, control, recognition, or effect.

#### Resolver Behavior

Resolvers SHOULD combine locally configured servers with permitted hints
from signature- and event-ID-verified candidate anchors carrying the requested
`o` value, then normalize and deduplicate them. Choosing which candidate
anchors and destinations to use remains application policy. No particular
server ordering is implied by tag order.

Resolvers MUST verify the returned bytes against the requested `o` digest
before treating them as the Digital Artifact. The first verified copy is
sufficient for byte retrieval; storage thresholds do not require downloading
a quorum of copies. A missing file, timeout, or digest mismatch at one server
SHOULD allow attempts at other permitted locations.

Signed hints remain untrusted network destinations. Implementations MUST
apply destination policy and resource limits before fetching, including
protection against private-network requests, DNS rebinding, and unsafe
redirects. A resolver may reject redirects altogether. It MUST NOT forward
credentials or upload authorization tokens to hinted retrieval destinations.
Digest verification does not make a file or its declared media type safe to
render; normal content-handling safeguards still apply.

Malformed or disallowed optional hints SHOULD be ignored with a diagnostic;
they do not by themselves invalidate otherwise valid DCR evidence. Failure
to retrieve the artifact MUST be reported separately from failure to retrieve
or verify its Anchor Event and Evidence Events. It is not proof that the
artifact never existed, that the DCR is invalid, or that control changed.

#### Compatibility And Immutability

Anchors without `blossom` tags remain valid and use configured servers,
archives, local copies, or other permitted artifact-retrieval mechanisms.
Older readers may ignore the optional tag. Evidence Events need not repeat
anchor hints; this convention introduces no new action or event kind.

Hints in an existing signed Anchor Event cannot be edited. Adding or changing
a hint changes the event ID and produces a different candidate anchor; it
does not update the old anchor or its linked graph. Implementations MUST NOT
silently reissue an anchor solely to refresh its storage locations. Local
resolver configuration can evolve without changing artifact identity or the
DCR. A future signed locator-update convention would require a separate design.

#### Example Anchor Fields

This fragment omits the standard Nostr author, timestamp, event ID, and
signature fields; it is not a complete signed event:

```json
{
  "kind": 1415,
  "tags": [
    ["o", "72f268d79dc36412a21d046cc2124b9ca02aab3c712eb23e67fd96d86a38e38f"],
    ["action", "issue"],
    ["name", "receipt.pdf"],
    ["blossom", "https://blossom.example.org"],
    ["blossom", "https://backup.example.org"]
  ],
  "content": "Anchored the digital artifact."
}
```

The two locations are hints for the same exact bytes. They do not represent
two artifacts, two anchors, or two votes about consequential state.

## Minimum Event Shapes

The wire-level event structures below define the current minimum working format.

### Anchor Event

- `kind = 1415`
- required tags:
  - `["o", "<object_hex>"]`
  - `["action", "issue"]`
- current implementation structured tags:
  - `["name", "<source_name>"]`
  - `["digest_generated_at", "<iso_8601_timestamp>"]`
  - `["size_bytes", "<decimal_byte_count>"]`
- optional structured tags:
  - `["blossom", "<https_server_origin>"]`, repeated for multiple optional retrieval hints
  - profile or identity tags such as `display_name`, `lei`, or related metadata where a given implementation chooses to include them
  - document metadata tags such as `record_reference` or `record_description`
  - domain tags such as `domain`, `document_type`, `schema`, or `schema_digest`

Recommended `content` convention:

- a short human-readable summary of the anchor or issue event
- no required machine parsing
- structured values are carried in tags

Control meaning:

- creates the first candidate DCR record concerning the Digital Artifact
- establishes the initial anchored control state
- establishes the starting point for later control traversal

Compatibility note:

- the current Nostr binding still uses `["action", "issue"]` on `kind 1415`
- this tag should be read as the current wire action label for anchoring or issuance, not as a claim of universal recognition or external effect

Recognition boundary:

- provides a one-record candidate DCR from which policy validation may produce
  consequential state, without deciding external recognition or effect
- does not, by itself, determine legal authority, ownership, title, mandate, priority, or effect
- may be one of several candidate Anchor Events for the same object digest

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
  - `["e", "<prior_control_event_id_or_anchor_event_id>"]`
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
- targets the specific Anchor Event or evidence event identified by the `e` tag
- does not by itself change the Current Controller

### Publisher Notice

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<anchor_event_id_or_prior_notice_event_id>"]`
  - `["action", "notice"]`
  - `["notice_type", "<publisher_position>"]`
- optional tags:
  - `["severity", "<information_warning_or_critical>"]`
  - `["effective_at", "<publisher_declared_time>"]`
  - `["reason_code", "<structured_reason>"]`
  - `["ref", "<external_reference>"]`
  - `["successor", "<successor_artifact_digest>"]`

State meaning:

- records the Anchor Publisher's signed position concerning the artifact
- must be signed by the Anchor Publisher to qualify under Core Record Ruleset 1.0
- does not erase or replace the Anchor Event
- does not by itself establish external validity, recognition, or effect
- does not by itself change the Current Controller

The normative notice vocabulary and state-derivation rules are defined in
[OPENETR_CORE_RECORD_RULESET_1_0.md](./OPENETR_CORE_RECORD_RULESET_1_0.md).

### Encumber Event

- `kind = 1416`
- required tags:
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_anchor_event_id>"]`
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
  - `["e", "<prior_control_event_id_or_anchor_event_id>"]`
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
  - `["e", "<prior_control_event_id_or_anchor_event_id>"]`
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
2. query Anchor Events using `kind = 1415` and `#o`
3. query evidence events using `kind = 1416` and `#o`
4. group candidate chains by `e` references
5. evaluate those chains under local validity and recognition rules

In current practice, the object digest is commonly queried through the `o` tag across both event families.

The reference `openetr query` command currently derives and displays:

- the candidate Anchor Event or events
- matching `kind 1416` evidence events
- summary control chains from linked `e` references
- lifecycle state
- current controller
- profile information where available
- encumbrance totals, discharged encumbrances, and outstanding encumbrances

The web app query result uses the same query service and should therefore expose the same derived object-state view.

### Retrieval Coverage And EOSE Hints

Relay query completion is not equivalent to global evidence completeness.

Where a relay implements optional NIP-67 EOSE completeness hints, an OpenETR
client should preserve the relay's observations:

| NIP-67 hint | OpenETR retrieval observation |
| --- | --- |
| `finish` | `complete_for_source` |
| `more` | `more_available` |
| `auth` | `authentication_required` |
| no conclusive hint | `unknown_completeness` |

`finish` means only that the relay reports having supplied every matching
stored event for that subscription. It does not prove that another relay,
archive, private repository, or unpublished source contains no additional or
conflicting event.

A client receiving `more` should paginate. A client receiving `auth` may use
NIP-42 authentication where appropriate and authorized. A client that cannot
complete pagination or authentication should preserve the events already
retrieved and report the retrieval limitation instead of silently treating
the result as complete.

OpenETR interoperable DCR evidence should continue to use dedicated event
kinds and semantics. Generic NIP-78 application-data kinds are not a substitute
for kinds `1415`, `1416`, or a future adopted linked-evidence kind.

## Cryptographic Control Chain Verification

The OpenETR control chain is not database state maintained by a single application. It is a graph of signed Nostr events that any verifier can retrieve and independently evaluate.

For a candidate object history, an implementation should verify:

1. the Anchor Event uses `kind = 1415` and carries the expected object identifier in `o`
2. each later evidence event uses `kind = 1416`
3. each event signature is valid for the event author
4. each event id matches the serialized event data under the Nostr event id rules
5. each event has the required minimum tags for its event shape
6. each event in the candidate chain carries the same `o` object identifier
7. each evidence event carries an `e` tag that points to the prior event being relied on
8. action-specific references such as `p`, `enc`, `type`, `notice_type`, and `ref` are present where required by the action or local recognition profile
9. the linked chain can be replayed in order to derive lifecycle state, current controller, and outstanding control conditions

The `e` tag follows the Nostr convention for event references. In OpenETR, it is the primary cryptographic link between control-relevant events:

- for the first later evidence event, `e` should point to the Anchor Event
- for later control-transition events, `e` should point to the immediately prior control-relevant event being extended
- for attestations, `e` should point to the specific event being attested
- for a Publisher Notice, `e` should point to the Anchor Event or immediately prior Publisher Notice
- for discharges, `enc` identifies the encumbrance being discharged, while `e` links the discharge into the current control chain

The chain therefore needs no separate root-pointer tag. A verifier recovers
the candidate Anchor Event by traversing `e` references to `kind 1415` and
must not substitute an unverified `origin` or `anchor` tag for that traversal.

This produces a DCR: an independently verifiable sequence of signed statements
about the same Digital Artifact. A verifier can reject events with invalid
signatures, inconsistent artifact identifiers, missing required tags, or
broken `e` references without relying on the application that originally
displayed the state.

Cryptographic control-chain verification is still not the same thing as legal or operational recognition. After the chain is structurally verified, an implementation must apply the relevant recognition profile, domain adapter, policy rules, and applicable law to decide which structurally valid events are effective for a particular purpose.

## Current Controller Implications

At the wire-format level, events express candidate control history.

The wire format alone does not guarantee:

- singularity
- exclusive control
- final authoritative recognition

Instead, implementations derive candidate controller state by traversing the linked event chain and then applying local recognition rules.

In the current working model:

- the Anchor Event identifies the initial issuer or controller position claimed by that event
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

## Regular-Event Rationale

OpenETR graph links commit to exact event ids. Anchor Events and Evidence Events
therefore use regular event kinds so a later record always references the exact
prior record on which it relies.

Rebroadcasting the exact same signed event preserves its event id. Publishing
different content produces a different event and does not replace or silently
relink the existing graph node. Missing records referenced by `e` shall be
reported as broken graph continuity.

Relay persistence alone is not the source of effect. Relay diversity, archives,
exports, attestations, or local stores may still be needed to preserve a
complete evidence set.

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

External Nostr inputs relevant to retrieval and private application data:

- [NIP-67: EOSE Completeness Hint](https://github.com/nostr-protocol/nips/blob/master/67.md)
- [NIP-78: Arbitrary custom app data](https://github.com/nostr-protocol/nips/blob/master/78.md)

## Summary

The current OpenETR Nostr wire format is defined by:

- `1415` for Anchor Events
- `1416` for later evidence events
- `o` as the object-history anchor
- `e` as the control-chain link
- `action` as the semantic subtype within the evidence-event family
- named non-indexed tags as the convention for signed structured metadata
- optional repeated `blossom` tags as artifact-retrieval hints, without changing byte identity or control semantics
- `content` as human-readable or unstructured event data

This provides a coherent current working format for publishing, querying, and traversing OpenETR control history over Nostr while leaving recognition, standing, mandate, attestation policy, and legal effect to higher layers.
