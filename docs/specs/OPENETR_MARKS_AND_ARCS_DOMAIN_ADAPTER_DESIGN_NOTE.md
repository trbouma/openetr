# OpenETR Marks And Arcs Domain Adapter Design Note

This note describes a potential OpenETR domain adapter for systems that model work as structured interactions called `Marks` and meaningful graph views called `Arcs`.

The design question is:

> How can a Marks-and-Arcs system use OpenETR control events and control graphs without collapsing collaboration semantics, workflow views, and legal control into one overloaded model?

## Status

Draft.

## Understanding The Problem Domain

Modern collaboration systems produce large volumes of digital traces, but those traces are usually fragmented across tools, channels, repositories, and organizational boundaries.

A decision may begin in a chat message, refer to a document in a drive, depend on an email attachment, receive approval in a workflow tool, and later be cited by an external party. Each interaction may be recorded somewhere, but the complete meaning is difficult to reconstruct.

The common failure modes are:

- interactions are captured as messages or files, not as structured events
- relationships between interactions are implicit, weak, or missing
- evidence is separated from the decisions or actions it supports
- responsibility is difficult to trace across people, systems, and time
- workflow state is confused with legal, operational, or control state
- a later relying party cannot easily verify what happened, who acted, and what object was affected

The Marks-and-Arcs model responds to this by treating each meaningful interaction as a `Mark` and each useful path through those interactions as an `Arc`.

That framing is powerful because it turns collaboration from a pile of messages into a graph of structured meaning. A Mark can say who acted, when they acted, what they acted on, and what evidence was attached. An Arc can show the decision path, document history, workflow timeline, or evidence chain that makes those Marks understandable.

OpenETR addresses a related but narrower problem.

OpenETR is concerned with controllable records: objects whose lifecycle, control, transfer, encumbrance, discharge, redemption, or termination must be represented through signed events and verifiable graphs. It is not a general collaboration substrate. It does not need to model every comment, conversation, document view, or workflow step as a control action.

The adapter is needed because the two models overlap without being identical.

```text
Marks-and-Arcs problem:
  how to structure and navigate the meaning of work

OpenETR problem:
  how to identify controlled objects and verify their control history

Adapter problem:
  how to decide which Marks become evidence, which become Control Events,
  and which Arcs become object-specific Control Graphs
```

Without this boundary, a system may make two opposite mistakes.

It may treat OpenETR too narrowly, using it only as a hash-and-signature layer and losing the richer graph of work that surrounds a controlled record.

It may also treat OpenETR too broadly, assuming that every signed collaboration Mark has control significance or legal recognition.

The design goal is to preserve both strengths:

- Marks and Arcs provide expressive collaboration context
- OpenETR provides portable control evidence and graph verification
- domain and recognition policies decide which actions have legal, operational, or institutional effect

### Channel Context And Durable Context

Many decisions depend on circumstantial context at the time they are made.

For example, the origin context for a document, approval, instruction, or transfer may depend on the fact that it arrived through a particular email thread, chat channel, shared drive, support ticket, project room, or workflow queue. That channel context can be meaningful. It may help explain who was involved, what participants understood, which document version was under discussion, and why a later action appeared authorized.

However, channel context is a weak long-term carrier of control meaning.

Over time:

- chat channels are renamed, archived, exported, or deleted
- email threads fork, lose attachments, or omit later recipients
- workplace identities change when people move roles or organizations
- links rot or point to mutable resources
- message order may not match the effective order of decisions
- access controls may prevent later verifiers from reconstructing the original setting
- the practical meaning of a decision may be diluted as it is copied across tools

This is acceptable for ordinary collaboration history. It is much less acceptable when the question is whether a controlled object was issued, transferred, encumbered, discharged, redeemed, or terminated.

The Marks-and-Arcs adapter should therefore treat channel context as evidence, not as the durable source of control state.

OpenETR gives the adapter a way to lift the control-relevant part of the interaction out of the ephemeral channel. A Mark may still record that an instruction was received through email or chat, but the control-relevant action should be represented as an explicitly signed event linked to the affected Controlled Object. The Arc may still show the originating conversation, but the Control Graph should exist as an object-specific graph that can be verified without depending on the continued existence, naming, ordering, or accessibility of the original channel.

The distinction is:

```text
channel context:
  explains the circumstances around a decision

OpenETR control context:
  preserves the signed, object-specific event graph needed to verify control state
```

This does not make channel evidence irrelevant. It makes it properly situated.

The channel can help explain why a participant acted. The OpenETR Control Graph records what control-relevant action was signed, what object it affected, which prior event it depended on, and how the resulting state can be replayed by a later verifier.

## Summary

A Marks-and-Arcs domain adapter can translate structured collaboration events into OpenETR-compatible signed evidence.

The compact mapping is:

```text
Mark = signed event atom
Arc = selected graph projection over marks
Control Event = mark with control, lifecycle, or authorization semantics
Control Graph = object-specific arc used to verify and replay control state
```

This mapping is useful, but it should be bounded carefully.

All control events can be represented as Marks. Not all Marks should be treated as control events.

All control graphs can be viewed as Arcs. Not all Arcs should be treated as control graphs.

The adapter should therefore distinguish:

- general collaboration evidence
- linked evidence
- domain attestations
- control-relevant actions
- object-specific control graphs
- recognition-policy decisions

OpenETR can make Marks verifiable. It does not make every Mark legally recognized.

## Architectural Boundary

The Marks-and-Arcs adapter sits above the OpenETR control layer.

```text
Marks-and-Arcs domain adapter
  marks, arcs, views, workflow vocabulary, collaboration semantics

OpenETR control layer
  Controlled Objects, signed events, linked evidence, control graphs,
  graph traversal, candidate control state, verifier warnings

Wire format
  event ids, signatures, tags, object references, relays, archives

Recognition layer
  law, contracts, institutional policy, authority lists, trust registries,
  domain rulebooks, relying-party decisions
```

The adapter should translate Marks into signed OpenETR events where useful, and translate OpenETR graph results back into user-facing Arc views.

It should not require the OpenETR core to understand collaboration views, decision threads, timelines, or workplace terminology.

## Domain Model

The adapter assumes two primary domain concepts.

### Marks

A Mark is a structured unit of interaction.

It may represent:

- a comment
- a document upload
- a decision
- an approval
- a request
- a response
- an AI-generated insight
- a human review
- an external-system notification
- a status change
- a control action

At minimum, a Mark should have:

- a stable identifier
- an actor
- a timestamp
- a type
- content or referenced content
- relationship links
- verification metadata

In OpenETR, a Mark is best understood as an event atom. It becomes meaningful when signed, linked to an object or other event, and interpreted under a domain profile.

### Arcs

An Arc is a meaningful graph view over Marks.

It may represent:

- a timeline
- a conversation
- a document history
- a decision path
- a workflow stage
- an evidence trail
- a dependency chain
- an object-specific control history

In OpenETR, an Arc is best understood as a graph projection. It selects events and relationships from the larger event fabric.

Some Arcs are merely useful views. Others have control significance.

## Controlled Object Strategy

The adapter should support three object strategies.

### Artifact Object

A concrete artifact is the Controlled Object.

Examples:

- a finalized document
- a signed PDF
- a structured JSON package
- an evidence bundle
- an exported workflow package

The artifact is canonicalized or finalized, hashed, and identified by digest.

```text
artifact bytes
  -> digest
  -> OpenETR origin event
  -> control and evidence events
  -> object-specific control graph
```

This is the safest starting point because the controlled object is clear.

### Workflow Object

A workflow instance is the Controlled Object.

Examples:

- a budget approval process
- a due diligence review
- a compliance review
- a cargo release workflow
- a policy approval process

The workflow has a stable object identifier and may contain many linked artifacts.

This model is useful where the record of control concerns a process rather than a single file. It requires a clear finalization rule for the workflow object and careful treatment of mutable state.

### Domain Record Object

A structured domain record is the Controlled Object.

Examples:

- an electronic bill of lading record
- a warehouse receipt record
- an Apostille package
- a Product Passport record
- a permit or certificate package

The Marks-and-Arcs adapter may be used as a collaboration layer around another domain adapter. In that case, the domain record adapter defines the Controlled Object, while the Marks-and-Arcs adapter contributes event capture, commentary, evidence, and view construction.

## Mark To OpenETR Mapping

The adapter should map Mark fields to OpenETR event fields and tags.

| Mark Concept | OpenETR Mapping |
| --- | --- |
| Mark identifier | OpenETR event id, or domain `mark_id` tag if the source Mark id must be preserved |
| Actor | event signer, participant tag, profile reference, or authority reference |
| Timestamp | event `created_at` plus optional domain effective time |
| Type | event kind, domain action tag, evidence type, or adapter-specific mark type |
| Content | event content, linked artifact digest, encrypted payload, or external reference |
| Source system | source tag, integration tag, relay metadata, or linked evidence |
| Relationships | event references, object references, participant references, dependency tags |
| Verification | signature validation, profile validation, credential evidence, registry checks |
| Preservation | relay publication, archive pointer, content-addressed storage, retention policy |

The event `content` field should remain human-readable context. Machine interpretation should rely on stable fields, tags, linked artifacts, and adapter-specific schemas.

## Mark Categories

The adapter should classify Marks before deciding how they map to OpenETR.

| Mark Category | OpenETR Treatment |
| --- | --- |
| Informational Mark | Signed evidence event or local-only event |
| Document Mark | Linked evidence, artifact registration, or origin event |
| Decision Mark | Attestation event, policy annotation, or linked evidence |
| Approval Mark | Attestation event or control event, depending on domain semantics |
| AI Insight Mark | Derived evidence with provenance and model metadata |
| System Mark | Integration evidence, timestamp evidence, or relay/archive evidence |
| Control Mark | Control Event such as `ISSUE`, `TRANSFER`, `ENCUMBER`, `DISCHARGE`, `REDEEM`, or `TERMINATE` |

The adapter should not automatically promote every signed Mark into a Control Event.

A Mark should become a Control Event only when it satisfies the domain adapter's control-action rules.

## Control Event Mapping

The adapter should define which Mark types may produce OpenETR control events.

Suggested starting mapping:

| Mark Type | OpenETR Operation | Notes |
| --- | --- | --- |
| Create controlled record | `ISSUE` | Creates the origin or first control event for a Controlled Object. |
| Assign controller | `TRANSFER` | Transfers control to another recognized participant. |
| Accept control | `ACCEPT` or domain acceptance evidence | May be required by verifier policy. |
| Add restriction | `ENCUMBER` | Records a pledge, lock, reservation, lien, hold, or other constraint. |
| Release restriction | `DISCHARGE` | Removes or satisfies a prior encumbrance. |
| Present for fulfillment | `REDEEM` or presentation evidence | Depends on whether the domain treats presentation as control-consuming. |
| Close or cancel record | `TERMINATE` | Ends the control lifecycle for the object. |
| Attach supporting fact | `ATTEST` or linked evidence | Does not usually change control by itself. |

The adapter should require an explicit mapping table for each deployment or domain profile. This avoids treating ordinary workplace approvals as legally effective transfers unless a domain rulebook says so.

## Arc To Control Graph Mapping

The adapter should distinguish Arcs from Control Graphs.

An Arc may be any selected view over Marks:

```text
all marks
  -> timeline arc
  -> conversation arc
  -> document arc
  -> decision arc
  -> evidence arc
  -> dependency arc
  -> control arc
```

A Control Graph is the subset of the event graph that is:

- object-specific
- signed
- linked to a Controlled Object
- ordered or causally related by prior-event references
- interpretable under OpenETR control semantics
- evaluated under a selected verifier policy

The adapter may expose the Control Graph to users as a special Arc, but it should preserve the stronger semantics.

```text
Arc:
  useful graph view

Control Graph:
  object-specific graph view with replay and validation semantics
```

## Relationship Model

Marks become graphable through explicit relationships.

The adapter should support relationship types such as:

- references object
- references event
- replies to
- supersedes
- amends
- approves
- rejects
- depends on
- derived from
- generated from
- attached to
- controls
- transfers to
- encumbers
- discharges

OpenETR should represent these relationships with stable event references, object references, participant references, and domain tags.

The adapter should avoid relying on free-text language such as "this relates to that" when the relationship affects graph interpretation.

## Validation Model

The adapter should define validation in stages.

### Mark Validation

Checks whether the Mark is structurally valid:

- required fields are present
- timestamps are well formed
- content references resolve
- linked artifacts match their digests
- source-system identifiers are syntactically valid
- relationships point to known objects or events

### Signature Validation

Checks whether the Mark or OpenETR event is cryptographically valid:

- event id matches event content
- signature validates against signer key
- profile references resolve
- signer key was active under the selected profile policy
- archive or relay evidence is available where required

### Control Validation

Checks whether a control-relevant Mark can produce or participate in a Control Event:

- the Mark type is mapped to a control operation
- the actor is permitted to perform the operation under the selected policy
- the referenced object exists
- prior control state permits the action
- required acceptance, consent, or countersignature evidence is present
- no unresolved encumbrance or termination blocks the action

### Recognition Validation

Checks whether a relying party should accept the graph:

- applicable law or rulebook is selected
- authority sources are recognized
- organizational identifiers resolve
- registry or trust-framework checks pass
- institutional policy requirements are satisfied
- domain-specific evidence is complete

This final stage is outside OpenETR core. The adapter may assist with recognition inputs, but it should not present cryptographic validity as universal legal effect.

## Status Dimensions

The adapter should avoid one overloaded status label.

It should distinguish:

- Mark capture status
- signature status
- preservation status
- evidence completeness status
- workflow status
- control status
- recognition status
- privacy or disclosure status

For example, an approval Mark may be:

```text
captured: yes
signed: yes
preserved: yes
control_effect: no
recognized_under_policy: not evaluated
```

This is clearer than presenting the Mark as simply "approved."

## Privacy And Storage

Marks may contain sensitive business, personal, legal, or regulated information.

The adapter should not require full Mark content to be published to public relays.

Recommended pattern:

- publish minimal signed metadata
- hash and reference private artifacts
- encrypt sensitive payloads where publication is required
- store private content in controlled repositories
- preserve access-control metadata outside OpenETR when needed
- publish enough information to verify integrity without exposing unnecessary content

The adapter should distinguish between:

- public event metadata
- private Mark content
- private attachments
- participant identifiers
- confidential workflow context
- recognition inputs that may not be public

## AI-Generated Marks

If the source system creates AI-generated Marks, the adapter should treat them as derived evidence, not as authority by default.

An AI-generated Mark should include:

- generation timestamp
- model or tool identifier where appropriate
- source inputs or input digests
- human reviewer, if reviewed
- confidence or limitation metadata where useful
- relationship links to the Marks or artifacts it analyzed

An AI-generated Mark should not become a Control Event unless a domain profile explicitly permits that action and identifies the responsible signer.

In many cases, the legally meaningful event is not:

```text
AI system recommended approval
```

but rather:

```text
authorized human or system adopted the recommendation
```

## Non-Goals

The Marks-and-Arcs adapter should not:

- make OpenETR a general collaboration platform
- make every collaboration event legally effective
- treat every Arc as a control graph
- require all Mark content to be public
- replace domain adapters for bills of lading, warehouse receipts, Apostilles, Product Passports, or other specialized domains
- decide legal recognition in the OpenETR core
- infer actor authority from a signature alone
- collapse workflow status, control status, and recognition status into one field

## Recommended Roadmap

1. Define a minimal Mark schema for OpenETR export.
2. Define required relationship types for graph construction.
3. Define a mapping from Mark categories to OpenETR event treatment.
4. Define an explicit list of Mark types that may become Control Events.
5. Implement object-specific Arc construction for Controlled Objects.
6. Implement Control Graph replay for those object-specific Arcs.
7. Add verifier-policy warnings for Marks that look control-relevant but are not authorized control events.
8. Add privacy profiles for public, private, and encrypted Mark publication.
9. Add optional support for AI-generated derived evidence Marks.

## Open Questions

- Should Marks always be represented as OpenETR events, or should some remain local-only with digest commitments?
- Should a Mark have a stable source-system identifier in addition to the OpenETR event id?
- Which Arc definitions should be persisted as signed objects rather than reconstructed by query?
- Should Control Graphs be named as a special Arc type in user interfaces?
- How should private or encrypted Marks participate in public graph verification?
- What minimum metadata is required for an AI-generated Mark to be useful as evidence?
- Should the adapter define a generic `arc_id`, or should Arcs remain query-derived views?
- How should conflicting Marks be presented when only one branch is recognized under a selected verifier policy?

## References

- [OpenETR Generic Domain Adapter Specification](./OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR Generic Transfer Model](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- [Control Event Minimum Shapes](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Linked Evidence Record Kind Design Note](./LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md)
- [OpenETR Dependency Integrity Design Note](./OPENETR_DEPENDENCY_INTEGRITY_DESIGN_NOTE.md)
