# OpenETR Generic Transfer Model

This note defines how OpenETR's control layer supports transfer of control
over a Digital Artifact by preserving DCR evidence and applying state
transition rules.

It is intended to describe control over a transferable electronic record in a way that remains independent of:

- any specific commercial domain
- any specific legal recognition regime
- any specific protocol implementation

OpenETR is not a Recognition Layer system. It does not itself provide
ownership, title, contractual rights, priority, mandate, or legal effect. It
preserves a Digital Controllable Record concerning a Digital Artifact and
supports validation of that DCR under an applicable policy. Consequential
state is the result of that validation.

## Purpose

OpenETR provides a control layer for electronic transferable records.

Its purpose is to make the DCR evidence, validation policy, and resulting
consequential state concerning a Digital Artifact independently verifiable.

It does not determine:

- ownership
- title
- contractual rights
- mandate
- legal effect

Those matters belong to the Recognition Layer.

## Core Primitives

### Digital Artifact

A **Digital Artifact** is persistent digital content uniquely identified by the
SHA-256 digest of its canonical representation.

The Digital Artifact:

- is uniquely identified by the SHA-256 digest of its canonical representation;
- is the common subject referenced by candidate assertions and Control Events;
- may have incomplete, invalid, competing, ambiguous, or terminated event
  history; and
- becomes a Digital Original when validation of its DCR under an applicable
  policy establishes consequential state.

### Digital Controllable Record

A **Digital Controllable Record (DCR)** is one end-verifiable record or a graph
of related end-verifiable records concerning the Digital Artifact. The DCR is
the control evidence structure, not the artifact itself.

### Current Controller

For a valid, complete, unambiguous, and active candidate graph, an applicable
validation policy may produce exactly one Participant as the Current
Controller. A Digital Artifact does not necessarily have a resulting Current Controller: the relevant
event set may be absent, incomplete, invalid, conflicting, or terminated.

The Current Controller has the exclusive ability to:

- transfer control
- redeem the Digital Artifact
- perform other authorized control actions

This is a Control Layer statement only. It does not by itself determine who owns the underlying asset or what legal consequences follow from control.

### Control Graph

The Control Graph is the control-event portion of the DCR concerning the
lifecycle of the Digital Artifact.

- nodes represent Participants
- directed edges represent authenticated Control Events
- every event references the Digital Artifact
- every event is cryptographically signed by the Participant performing the event

The graph provides evidence that a stated policy can validate to produce
consequential state. A particular retrieved graph may be incomplete or may
compete with another candidate graph.

### Participants

A Participant is any identified entity capable of creating authenticated Control Events.

A Participant may assume one or more Control Roles:

- Issuer
- Current Controller
- Transferor
- Transferee
- Attestor
- Obligor
- Redeemer
- Relying Party

These are Control Roles only.

Commercial or institutional roles such as:

- exporter
- buyer
- warehouse operator
- bank
- producer

exist outside the model.

## Generic Control Events

### ISSUE

Creates the first DCR record concerning a Digital Artifact. Validation of that
one-record DCR under the applicable policy may establish initial consequential
state.

An ISSUE event:

- establishes the initial Current Controller
- initializes the Control Graph

### TRANSFER

Transfers exclusive control from the Current Controller to another Participant.

A TRANSFER event:

- changes the Current Controller
- appends a Transfer event to the Control Graph

### ATTEST

Adds an authenticated assertion relating to the Digital Artifact.

Examples include:

- custody
- inspection
- quality
- quantity
- certification

Attestations do not change the Current Controller.

### ENCUMBER

Records an authenticated declaration of an encumbrance affecting the Digital Artifact.

Examples include:

- pledge
- security right
- lien
- restriction

OpenETR records the declaration but does not determine:

- legal validity
- perfection
- priority
- legal effect

### DISCHARGE

Records the authenticated release or satisfaction of a previously declared encumbrance.

### REDEEM

Records that the Current Controller has presented the Digital Artifact to the Obligor and requested performance.

### TERMINATE

Records that the Obligor has completed performance and that the Digital Artifact has reached the end of its OpenETR lifecycle.

No further control events may occur after termination.

## Endorsement and Indorsement

OpenETR does not define endorsement or indorsement as a separate universal Control Event type.

Instead, where relevant, endorsement or indorsement is expressed as an attestation associated with an underlying OpenETR event, with its legal or commercial characterization determined by the applicable recognition framework.

In the generic model:

- if the relevant action changes the Current Controller, it is modeled as `TRANSFER`
- if the relevant action adds authenticated meaning, authority, approval, instruction, limitation, or another assertion without itself changing control, it is modeled as `ATTEST`

Whether those events amount to an endorsement or indorsement is determined outside the Control Layer by the relevant Recognition Layer, contractual framework, or governing law.

## Generic State Model

```text
PRE-ISSUANCE
      |
      | ISSUE
      v
ACTIVE
      |
      |-- ATTEST
      |-- TRANSFER
      |-- ENCUMBER
      |-- DISCHARGE
      |
      v
ACTIVE
      |
      |-- REDEEM
      v
REDEMPTION PENDING
      |
      |-- TERMINATE
      v
TERMINATED
```

`ATTEST`, `TRANSFER`, `ENCUMBER`, and `DISCHARGE` may occur multiple times throughout the `ACTIVE` state.

## Architectural Boundary

OpenETR records authenticated facts.

It answers:

- What is the Digital Artifact and what DCR concerns it?
- Who is the Current Controller?
- Who made which authenticated assertions?
- How has control evolved?

It does not answer:

- Who owns the underlying asset?
- Has title passed?
- Is a security right legally perfected?
- Which party has priority?
- What contractual rights exist?

Those questions are determined by the applicable Recognition Layer, for example:

- MLWR
- MLETR
- UCC Article 12
- contract law
- other governing legal frameworks

## Design Principle

OpenETR provides authenticated evidence of control.

Commercial relationships and legal consequences remain outside the Control Layer.

Some implementation profiles may choose to recognize certain effects, especially transfers among a small and otherwise trusted set of counterparties, without separate third-party attestation at the time of transfer.

Where that occurs, recognition arises from the participants' own trust relationship and agreed policy rather than from the stronger OpenETR model of independently attestable evidence.

In such a simplified local-recognition profile, ordinary transfers may be recognized without separate attestation, although a specific attestation may still be used where the parties want to attach additional meaning, instruction, endorsement, or indorsement to a particular event.

That may be operationally acceptable for a narrower environment, but it provides a weaker foundation for independent verification, broad portability, and later dispute resolution.

As the model scales outward, parties may increasingly require attestation in order to rely on actions taken by participants with whom they do not share the same direct trust relationship.

In some settings, attestation may additionally be required for legal effect, institutional acceptance, or official recognition.

OpenETR should therefore be understood as supporting a spectrum from simplified local recognition, to selective event-level attestation, to fuller attested models designed for broader reliance and recognition.

The same generic model applies regardless of whether the Digital Artifact represents:

- a warehouse receipt
- a bill of lading
- a promissory note
- a certificate
- a ticket
- a digital asset entitlement
- another transferable record

## Interpretation

This model is intended to be protocol-neutral and recognition-neutral.

It is compatible with the broader three-layer framing in which:

- the Protocol Layer establishes correctness
- the Control Layer establishes authenticated control relationships
- the Recognition Layer assigns legal, commercial, institutional, or social effect

Under that framing, OpenETR belongs to the Control Layer. It preserves a durable, signed, and reviewable history of control without collapsing control into either protocol mechanics or legal recognition.
