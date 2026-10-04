# OpenETR Core Record Ruleset 1.0

## Status

Draft specification for review and implementation.

Ruleset identifier:

```text
openetr:core-record:1.0
```

This document defines the minimum OpenETR ruleset for deriving Consequential
State concerning a digest-identified Digital Artifact. It is intentionally
limited to artifact anchoring and later notices from the Anchor Publisher.

The ruleset is suitable as a complete foundation for non-transferable records.
Future rulesets may extend it for transferable records without changing the
meaning of an Anchor Event or Publisher Notice defined here.

## 1. Purpose

The purpose of this ruleset is to answer two narrow questions:

1. Does the supplied evidence establish that a signing key anchored this exact
   Digital Artifact?
2. What is that Anchor Publisher's current signed position concerning the
   artifact, if a qualifying Publisher Notice is available?

The ruleset derives those answers from end-verifiable signed evidence. It does
not require the application that created or displayed the evidence to remain
available.

## 2. Conformance Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document indicate normative requirements.

An implementation claiming conformance with this ruleset SHALL identify the
ruleset as `openetr:core-record:1.0` in machine-readable results.

## 3. Architectural Position

This ruleset is not the OpenETR protocol and is not a recognition policy.

```text
OpenETR protocol
  -> defines the evidence structure and verification semantics

Nostr wire-format binding
  -> represents the evidence as signed events

Core Record Ruleset 1.0
  -> evaluates supplied evidence
  -> derives anchored state and publisher position

Recognition policy
  -> determines whether a relying party accepts that state
  -> determines what external effect follows
```

The verifier applies this ruleset to an evidence set. The protocol does not make
an artifact legally valid, authoritative, approved, enforceable, or recognized
merely because qualifying evidence exists.

## 4. Scope

This ruleset defines:

- Digital Artifact identification using SHA-256;
- validation of a candidate Anchor Event;
- derivation of anchored Consequential State;
- validation of Publisher Notices;
- construction of Publisher Notice chains;
- derivation of the Anchor Publisher's current stated position;
- treatment of multiple anchors, competing notices, and missing evidence;
- minimum machine-readable output; and
- evidence, timestamp, recognition, and presentation boundaries.

## 5. Out Of Scope

This ruleset does not derive or determine:

- Current Controller;
- transferability;
- transfer initiation or acceptance;
- possession, ownership, title, or holder status;
- encumbrances, security interests, priority, or discharge;
- redemption, surrender, or termination;
- authority of the Anchor Publisher;
- legal, institutional, contractual, or regulatory validity;
- global uniqueness of an Anchor Event;
- globally complete event retrieval;
- trusted publication time;
- global event ordering;
- witnessed observation;
- consensus or finality; or
- external recognition or effect.

The absence of an evaluated concept SHALL NOT be represented as a positive
finding about that concept.

## 6. Terms

### 6.1 Digital Artifact

Persistent digital content identified in this ruleset by the SHA-256 digest of
its exact bytes.

### 6.2 Anchor Event

A regular Nostr event of kind `1415` that begins a candidate Digital
Controllable Record concerning a Digital Artifact.

### 6.3 Anchor Publisher

The Key-Based Identifier corresponding to the public key that signed the Anchor
Event.

The term identifies the signing key. It does not, by itself, establish the
identity, actor type, authority, role, or recognition of the actor associated
with that key.

### 6.4 Publisher Notice

A regular Nostr Evidence Event of kind `1416`, signed by the Anchor Publisher,
that states the publisher's position concerning the anchored Digital Artifact.

### 6.5 Publisher Notice Chain

An ordered path beginning with an Anchor Event and extended by zero or more
qualifying Publisher Notices linked through exact `e` references.

### 6.6 Publisher Position

The position expressed by the terminal qualifying Publisher Notice on a unique
Publisher Notice Chain.

Publisher Position is derived state about what the Anchor Publisher has stated.
It is not an independent determination that the artifact is valid, invalid,
safe, unsafe, binding, or ineffective.

### 6.7 Candidate DCR

The Anchor Event and any related evidence records evaluated together as one
candidate Digital Controllable Record.

### 6.8 Evidence Set

The exact collection of signed records supplied to or retrieved by the
verifier, together with the declared retrieval scope and sources.

## 7. Digital Artifact Identification

The artifact identifier SHALL be:

```text
SHA-256(exact artifact bytes)
```

The canonical representation SHALL be 64 lowercase hexadecimal characters.

Byte-identical copies having the same digest SHALL be treated as the same
Digital Artifact. Copying the bytes SHALL NOT be interpreted as creating a new
Anchor Event, DCR, Publisher Position, or independently recognized state.

An implementation MAY evaluate a supplied digest without possessing the
artifact bytes. Its result SHALL indicate whether the digest was computed from
locally supplied bytes or accepted as an input assertion.

## 8. Anchor Event

### 8.1 Minimum Shape

A conforming Anchor Event SHALL:

- use regular event kind `1415`;
- carry exactly one `o` tag containing the artifact digest;
- carry exactly one `action` tag with value `issue`;
- contain a valid Nostr event identifier;
- contain a valid signature for its author public key; and
- identify its author using the Nostr public-key field.

Example:

```json
{
  "kind": 1415,
  "pubkey": "<anchor-publisher-hex-pubkey>",
  "created_at": 0,
  "tags": [
    ["o", "<artifact-sha256-hex>"],
    ["action", "issue"]
  ],
  "content": "Anchored record"
}
```

The `created_at` value above is illustrative. Section 15 defines its limited
meaning.

### 8.2 Optional Data

An Anchor Event MAY include signed named tags such as:

- `name`;
- `size_bytes`;
- `digest_generated_at`;
- `domain`;
- `document_type`;
- `record_reference`;
- `record_description`;
- `schema`; and
- `schema_digest`.

Required machine-readable semantics SHALL be carried in event fields or tags.
The verifier SHALL NOT parse `content` to recover the artifact identifier,
action, signer, or graph relationship.

### 8.3 Anchor Validation

For each candidate Anchor Event, a conforming verifier SHALL:

1. recompute and validate the event identifier;
2. validate the event signature;
3. confirm `kind=1415`;
4. confirm `action=issue`;
5. confirm that `o` is a valid SHA-256 hexadecimal digest;
6. confirm that `o` equals the artifact digest under evaluation; and
7. identify the Anchor Publisher from the event author.

A failure in steps 1 through 6 SHALL prevent that event from establishing
`anchored` state under this ruleset.

### 8.4 Anchor Consequence

A valid Anchor Event SHALL produce:

```text
anchor_state = anchored
```

This is Consequential State under this ruleset. It means that the supplied
evidence proves that the Anchor Publisher signed an anchoring statement
concerning the identified Digital Artifact.

Because the artifact has Consequential State established through a DCR, it is a
Digital Original under this ruleset. Whether a relying party recognizes that
Digital Original as authoritative for any purpose remains external.

It SHALL NOT be interpreted as proving:

- that the publisher was authorized to issue the artifact;
- that the artifact is substantively correct;
- that the artifact remains suitable for use;
- that the Anchor Event is globally unique; or
- that any relying party recognizes the artifact.

## 9. Publisher Notice

### 9.1 Purpose

A Publisher Notice allows the Anchor Publisher to add a later signed statement
concerning the artifact without deleting, replacing, or mutating the Anchor
Event.

The historical fact represented by the Anchor Event remains verifiable after a
notice is published.

### 9.2 Minimum Shape

A conforming Publisher Notice SHALL:

- use regular event kind `1416`;
- be signed by the same public key as the Anchor Event;
- carry exactly one `o` tag equal to the anchored artifact digest;
- carry exactly one `e` tag referencing the Anchor Event or immediately prior
  Publisher Notice;
- carry exactly one `action` tag with value `notice`;
- carry exactly one `notice_type` tag;
- contain a valid Nostr event identifier; and
- contain a valid signature.

Example:

```json
{
  "kind": 1416,
  "pubkey": "<same-anchor-publisher-hex-pubkey>",
  "created_at": 0,
  "tags": [
    ["o", "<same-artifact-sha256-hex>"],
    ["e", "<anchor-or-prior-notice-event-id>"],
    ["action", "notice"],
    ["notice_type", "do_not_use"],
    ["severity", "warning"]
  ],
  "content": "This record has been withdrawn and should not be relied upon."
}
```

### 9.3 Notice Types

Core Record Ruleset 1.0 defines the following `notice_type` values:

| Value | Publisher statement |
| --- | --- |
| `information` | Supplies additional information without expressing caution. |
| `caution` | Advises the relying party to exercise caution. |
| `do_not_use` | Advises that the artifact should not be used or relied upon. |
| `withdrawn` | Withdraws the publisher's own prior anchoring assertion or support. |
| `superseded` | States that another artifact or record has superseded this artifact. |
| `corrected` | States that the artifact is subject to correction or has a corrected successor. |
| `other` | Carries a publisher position not represented by another core value. |

These values classify the publisher's statement. They SHALL NOT be presented as
independent findings of fact or universal effect.

An extension MAY define additional namespaced notice types. A core verifier that
does not understand an extension SHALL preserve and report the signed notice,
but SHALL set its derived Publisher Position to `unsupported_notice_type`
unless another applicable ruleset defines its semantics.

### 9.4 Optional Notice Data

A Publisher Notice MAY include:

- `severity`, such as `information`, `warning`, or `critical`;
- `effective_at`, expressing the publisher's claimed effective time;
- `reason_code`, expressing a structured reason;
- `ref`, identifying an external reference;
- `successor`, identifying a claimed successor artifact digest; and
- human-readable `content`.

`severity` and `effective_at` are publisher assertions. They do not establish
independent severity or trusted time.

A `superseded` or `corrected` notice SHOULD identify the successor or
correction through `successor`, `ref`, or another defined structured tag.

### 9.5 Notice Validation

For each candidate Publisher Notice, a conforming verifier SHALL:

1. recompute and validate the event identifier;
2. validate the event signature;
3. confirm `kind=1416`;
4. confirm `action=notice`;
5. confirm that its author equals the Anchor Publisher;
6. confirm that `o` equals the anchored artifact digest;
7. resolve the exact event identified by `e`;
8. confirm that the referenced event is the Anchor Event or a qualifying
   Publisher Notice in the same candidate DCR;
9. confirm that the notice does not create a graph cycle; and
10. validate `notice_type` according to Section 9.3.

A notice that fails one or more requirements SHALL remain visible as supplied
evidence but SHALL NOT determine Publisher Position under this ruleset.

## 10. Publisher Notice Graph

### 10.1 Chain Construction

The first qualifying Publisher Notice in a chain SHALL reference the Anchor
Event.

A later Publisher Notice that updates the publisher's position SHALL reference
the immediately prior qualifying Publisher Notice.

Graph order SHALL be determined by exact `e` relationships, not by
`created_at`.

Repeated copies of an event having the same event identifier SHALL be
deduplicated for state derivation while preserving source-observation
information where available.

### 10.2 Terminal Notice

A terminal notice is a qualifying Publisher Notice that is not referenced as
the predecessor of another qualifying Publisher Notice in the supplied Evidence
Set.

If exactly one terminal notice exists, its supported `notice_type` SHALL
determine `publisher_position`.

If no qualifying Publisher Notice exists:

```text
publisher_position = no_notice_found
```

`no_notice_found` SHALL NOT be interpreted as `valid`, `approved`,
`current`, `safe_to_use`, or any equivalent positive conclusion.

### 10.3 Competing Notice Branches

If more than one terminal qualifying Publisher Notice exists for the same
Anchor Event:

```text
publisher_position = conflicting_notices
```

The verifier SHALL:

- preserve every branch;
- identify each terminal notice;
- avoid selecting a branch based only on `created_at`;
- issue a structured conflict finding; and
- avoid presenting any one Publisher Position as uniquely current.

### 10.4 Missing Notice Predecessor

A notice whose `e` reference cannot be resolved SHALL be reported as an
incomplete notice chain.

It SHALL NOT be silently attached to the Anchor Event or another notice.

## 11. Multiple Candidate Anchors

More than one valid Anchor Event MAY exist for the same Digital Artifact.

Each Anchor Event SHALL begin a separate candidate DCR, even where two Anchor
Events have the same author.

Publisher Notices SHALL be evaluated only within the candidate DCR rooted at
the Anchor Event reached through their `e` links.

A verifier SHALL NOT:

- merge separate candidate anchors;
- select the latest anchor by timestamp as universally authoritative;
- treat one anchor as replacing another without a defined rule; or
- infer that multiple anchors make otherwise authentic evidence disappear.

Where more than one valid candidate Anchor Event is present, the aggregate
result SHALL report `multiple_candidate_anchors` and return each candidate
evaluation separately.

## 12. Derived State Model

### 12.1 Candidate State

For each candidate Anchor Event, the ruleset SHALL derive:

- `anchor_state`;
- `anchor_event_id`;
- `anchor_publisher`;
- `publisher_position`;
- the qualifying Publisher Notice chain or branches;
- non-qualifying evidence;
- structured findings; and
- evidence-source and retrieval information where available.

### 12.2 Anchor State Vocabulary

The following values are defined:

| Value | Meaning |
| --- | --- |
| `anchored` | A candidate Anchor Event satisfies this ruleset. |
| `invalid_anchor_evidence` | A supplied candidate fails cryptographic or structural validation. |
| `not_anchored` | No qualifying Anchor Event was found in the supplied Evidence Set. |
| `unverifiable` | Required evidence or cryptographic verification capability was unavailable. |

### 12.3 Publisher Position Vocabulary

The following values are defined:

- `no_notice_found`;
- each supported `notice_type`;
- `conflicting_notices`;
- `incomplete_notice_chain`;
- `unsupported_notice_type`; and
- `unverifiable`.

### 12.4 State Independence

`anchor_state` and `publisher_position` SHALL remain separate dimensions.

A `withdrawn` or `do_not_use` Publisher Position SHALL NOT change the
historical Anchor Event into an invalid signature or erase `anchor_state`.

Example:

```text
anchor_state       = anchored
publisher_position = withdrawn
```

## 13. Verification Procedure

A conforming verifier SHALL perform the following procedure:

1. determine or accept the artifact digest;
2. record whether the digest was computed or supplied;
3. accept or retrieve candidate `1415` Anchor Events by `o`;
4. validate each candidate Anchor Event independently;
5. create one candidate DCR for each valid Anchor Event;
6. accept or retrieve candidate `1416` Publisher Notices by `o`;
7. validate each notice against the candidate anchor it reaches through `e`;
8. construct qualifying notice chains;
9. identify terminal notices, branches, missing predecessors, and conflicts;
10. derive candidate state according to Section 12;
11. preserve non-qualifying signed evidence and explain why it did not affect
    state;
12. identify the ruleset and version applied; and
13. report retrieval scope, evidence sources, and known completeness
    limitations.

The procedure SHALL be deterministic for the same artifact identifier, Evidence
Set, ruleset version, and evaluation parameters.

## 14. Evidence Findings

A verifier SHOULD use stable finding codes. Core codes include:

| Code | Condition |
| --- | --- |
| `anchor_not_found` | No qualifying Anchor Event was supplied or retrieved. |
| `invalid_event_id` | Event identifier validation failed. |
| `invalid_signature` | Signature validation failed. |
| `artifact_mismatch` | The `o` value does not match the evaluated artifact. |
| `invalid_anchor_action` | A kind `1415` candidate does not declare `issue`. |
| `notice_signer_mismatch` | Notice author differs from the Anchor Publisher. |
| `notice_parent_missing` | The event referenced by `e` is unavailable. |
| `notice_parent_invalid` | The referenced event is not a qualifying parent. |
| `notice_cycle` | Notice graph traversal detected a cycle. |
| `unsupported_notice_type` | No applicable rules define the notice type. |
| `conflicting_notices` | More than one terminal qualifying notice exists. |
| `multiple_candidate_anchors` | More than one valid Anchor Event exists. |
| `retrieval_incomplete` | Retrieval limitations may have omitted evidence. |
| `timestamp_not_independently_verified` | No accepted external time evidence was evaluated. |

Findings SHALL distinguish cryptographic invalidity, structural
non-conformance, incomplete evidence, conflict, and external recognition.

## 15. Time And Observation

Nostr `created_at` is declared by the event signer.

Core Record Ruleset 1.0 SHALL NOT treat `created_at` as independent proof of:

- publication time;
- first observation;
- ordering between competing branches;
- existence before a legal or operational deadline; or
- global availability.

The verifier MAY display signer-declared time, but it SHOULD label that value
accordingly.

Witness records, trusted timestamps, relay observation receipts, transparency
logs, and other external time evidence are outside this ruleset.

## 16. Retrieval And Completeness

OpenETR evidence may be obtained from public relays, private relays, local
relays, archives, files, databases, bundles, or direct exchange.

A valid signature proves attribution to a key for the signed event. It does not
prove that the verifier has received every relevant event.

A verifier SHALL identify, where available:

- evidence sources queried;
- relay filters or equivalent retrieval parameters;
- retrieval start and end time;
- pagination or authentication limitations;
- timeouts or source failures; and
- whether the result is based on a supplied bundle rather than discovery.

The verifier SHALL represent its result as relative to the supplied or retrieved
Evidence Set.

## 17. Recognition And Effect

This ruleset derives Consequential State from protocol evidence. Recognition
remains external.

A relying party MAY use a recognition policy to determine:

- whether the Anchor Publisher is known or authorized;
- whether the artifact type is accepted;
- whether a Publisher Notice has institutional or legal effect;
- whether another authority may override or supplement the publisher's
  position;
- whether additional evidence is required; and
- what action should follow.

A conforming presentation SHALL distinguish:

```text
Ruleset result:
  The Anchor Publisher signed a do_not_use notice.

Recognition result:
  This relying party accepts that notice for the stated purpose.

Effect:
  The relying application blocks operational use of the artifact.
```

The second and third conclusions do not follow from this ruleset alone.

## 18. Presentation Requirements

User-facing software SHALL describe Publisher Position as an attributable
statement.

Preferred:

> The Anchor Publisher states that this artifact should not be used.

Not conforming without additional recognized evidence:

> This artifact is invalid.

User-facing software SHOULD display:

- the artifact digest;
- Anchor Event identifier;
- Anchor Publisher;
- anchor signature status;
- Publisher Position;
- terminal Publisher Notice identifier;
- signer-declared timestamp with an appropriate label;
- conflicts and incomplete-chain warnings;
- ruleset identifier and version; and
- recognition status separately, if recognition was evaluated.

## 19. Machine-Readable Result

A conforming JSON result SHOULD follow this minimum structure:

```json
{
  "ruleset": {
    "id": "openetr:core-record:1.0",
    "version": "1.0"
  },
  "artifact": {
    "digest_algorithm": "sha256",
    "digest": "<artifact-sha256-hex>",
    "digest_source": "computed"
  },
  "aggregate_state": "anchored",
  "candidates": [
    {
      "anchor_state": "anchored",
      "anchor_event_id": "<event-id>",
      "anchor_publisher": "<hex-pubkey>",
      "publisher_position": "do_not_use",
      "terminal_notice_event_ids": ["<event-id>"],
      "notice_event_ids": ["<event-id>"],
      "findings": []
    }
  ],
  "retrieval": {
    "sources": ["<evidence-source>"],
    "complete": null
  },
  "findings": [
    {
      "code": "timestamp_not_independently_verified",
      "severity": "information"
    }
  ]
}
```

`retrieval.complete` SHOULD be `null` where completeness cannot be established.
It SHALL NOT default to `true` merely because one or more relays returned
events.

The result SHOULD include or permit export of the exact raw signed events used
for derivation.

## 20. Conformance Classes

### 20.1 Conforming Publisher

A conforming publisher SHALL:

- construct Anchor Events according to Section 8;
- construct Publisher Notices according to Section 9;
- sign the exact event data;
- use regular events;
- preserve structured semantics in tags; and
- avoid representing signer-declared time as independently verified time.

### 20.2 Conforming Verifier

A conforming verifier SHALL:

- implement the procedure in Section 13;
- validate event identifiers and signatures;
- evaluate candidate anchors separately;
- follow exact `e` links;
- avoid timestamp-based branch selection;
- preserve conflicting and non-qualifying evidence;
- produce the state dimensions in Section 12;
- identify this ruleset and version; and
- preserve the boundary between ruleset output, recognition, and effect.

### 20.3 Conforming Application

A conforming application SHALL:

- avoid presenting application database state as the sole authority;
- permit the evidence supporting displayed state to be inspected or exported;
- label Publisher Position as the publisher's statement;
- avoid treating `no_notice_found` as affirmative validity; and
- avoid implying that this ruleset determines transfer, ownership, or legal
  effect.

## 21. Required Test Vectors

An implementation test suite SHALL cover at least:

1. one valid Anchor Event;
2. no Anchor Event;
3. an Anchor Event with an invalid signature;
4. an Anchor Event with an incorrect event identifier;
5. an Anchor Event whose `o` value does not match the artifact;
6. multiple valid candidate Anchor Events;
7. one valid Publisher Notice referencing the Anchor Event;
8. a sequence of Publisher Notices linked through `e`;
9. a notice signed by a key other than the Anchor Publisher;
10. a notice with a missing predecessor;
11. a notice with an unsupported notice type;
12. competing terminal notice branches;
13. duplicate observations of the same signed event;
14. misleading or backdated `created_at` values;
15. incomplete relay retrieval; and
16. a `withdrawn` notice that leaves `anchor_state=anchored`.

Test vectors SHOULD include the artifact bytes or digest, complete event JSON,
expected state, and expected finding codes.

## 22. Privacy And Security Considerations

### 22.1 Public correlation

Artifact digests, publisher keys, tags, and notice content may be publicly
correlatable when published to public relays.

Implementations SHOULD avoid publishing unnecessary personal, confidential, or
sensitive information.

### 22.2 Guessable artifacts

A digest does not conceal low-entropy or guessable content. A party possessing
candidate content can hash it and compare the result.

### 22.3 Key compromise

A valid signature establishes use of the corresponding private key. It does not
establish that the key was uncompromised, properly authorized, or operated by
the expected actor.

Compromise, recovery, and key-rotation rules are outside this ruleset.

### 22.4 Availability

Regular event status does not guarantee indefinite retention by every relay.
Publishers and relying parties SHOULD preserve evidence according to their
availability and retention requirements.

### 22.5 Harmful or misleading notices

The Anchor Publisher can publish misleading, contradictory, or malicious
notices. This ruleset preserves and attributes those statements; it does not
guarantee their truth.

## 23. Extension And Versioning Rules

An extension SHALL NOT change the meaning of a conforming Core 1.0 Anchor Event
or Publisher Notice while claiming Core 1.0 compatibility.

An extension that assigns new consequences SHALL:

- use a distinct ruleset identifier and version;
- define required event shapes;
- define signer and graph relationships;
- define state variables and transitions;
- define conflict and missing-evidence handling;
- identify its dependency on Core Record Ruleset 1.0; and
- keep external recognition and effect explicit.

Unknown events SHALL remain visible as evidence. They SHALL have no state
consequence under Core Record Ruleset 1.0 unless this document defines one.

## 24. Transferable Record Considerations

This section is non-normative.

A future transferable-record ruleset may extend a candidate DCR with:

- Current Controller;
- transfer initiation;
- transfer acceptance;
- pending and completed transfer state;
- witnesses;
- independent timestamp or observation evidence;
- ordering and concurrency rules; and
- higher-assurance conflict handling.

The future ruleset should depend on Core Record Ruleset 1.0:

```text
Core Record Ruleset 1.0
  anchor_state
  publisher_position
        |
        +-- Transferable Record Ruleset
              transfer_state
              current_controller
```

The Anchor Publisher and Current Controller are separate roles. A Publisher
Notice SHALL NOT transfer control, and a transfer SHALL NOT silently change the
identity of the Anchor Publisher.

A future transferable-record ruleset SHALL define whether and how a Publisher
Position affects transfer-state derivation. Core Record Ruleset 1.0 assigns no
transfer consequence to a Publisher Notice.

A higher-assurance transferable-record ruleset may require witness or
observation evidence to address retrospective publication, concurrent branches,
or disputed ordering. Those mechanisms are deliberately excluded from Core
Record Ruleset 1.0.

## 25. Relationship To Other OpenETR Documents

This ruleset should be read with:

- [OpenETR Draft National Standard](./OPENETR_DRAFT_NATIONAL_STANDARD.md);
- [Digital Controllable Record Design Note](./DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md);
- [OpenETR Nostr Wire Format Specification](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md);
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md);
- [Event Kind Registry](./EVENT_KIND_REGISTRY.md); and
- [Regular Event Kind Decision Note](./REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md).

Where terminology differs, the canonical definitions in the Draft National
Standard apply unless this ruleset supplies a narrower definition for its own
state derivation.

## 26. Summary

Core Record Ruleset 1.0 establishes a deliberately small foundation:

```text
Digital Artifact
  + valid Anchor Event
  -> anchored Consequential State

anchored artifact
  + qualifying Publisher Notice chain
  -> current Publisher Position
```

The ruleset preserves what was signed, identifies who signed it, follows exact
graph relationships, exposes conflicts, and derives reproducible state. It does
not decide who must trust that state or what external effect it receives.
