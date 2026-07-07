# OpenETR Generic Transfer Model

This note defines a generic Control Layer model for OpenETR.

It is intended to describe control over a transferable electronic record in a way that remains independent of:

- any specific commercial domain
- any specific legal recognition regime
- any specific protocol implementation

OpenETR is not a Recognition Layer system. It does not determine ownership, title, contractual rights, priority, or legal effect. It records authenticated control facts and control transitions for a Controlled Object.

## Purpose

OpenETR is a Control Layer for electronic transferable records.

Its purpose is to maintain an authenticated, verifiable chain of control over a Controlled Object.

It does not determine:

- ownership
- title
- contractual rights
- legal effect

Those matters belong to the Recognition Layer.

## Core Primitives

### Controlled Object

A Controlled Object is a durable electronic record whose control is managed by OpenETR.

The Controlled Object:

- is uniquely identified by the SHA-256 digest of its canonical representation
- is the anchor for all authenticated assertions and Control Events
- is the subject of legal recognition by applicable legal frameworks

### Current Controller

At any point in time, exactly one Participant is the Current Controller.

The Current Controller has the exclusive ability to:

- transfer control
- redeem the Controlled Object
- perform other authorized control actions

This is a Control Layer statement only. It does not by itself determine who owns the underlying asset or what legal consequences follow from control.

### Control Graph

The Control Graph is an immutable graph describing the lifecycle of the Controlled Object.

- nodes represent Participants
- directed edges represent authenticated Control Events
- every event references the Controlled Object
- every event is cryptographically signed by the Participant performing the event

The graph provides the complete provenance of control.

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

Creates the Controlled Object.

An ISSUE event:

- establishes the initial Current Controller
- initializes the Control Graph

### TRANSFER

Transfers exclusive control from the Current Controller to another Participant.

A TRANSFER event:

- changes the Current Controller
- appends a Transfer event to the Control Graph

### ATTEST

Adds an authenticated assertion relating to the Controlled Object.

Examples include:

- custody
- inspection
- quality
- quantity
- certification

Attestations do not change the Current Controller.

### ENCUMBER

Records an authenticated declaration of an encumbrance affecting the Controlled Object.

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

Records that the Current Controller has presented the Controlled Object to the Obligor and requested performance.

### TERMINATE

Records that the Obligor has completed performance and that the Controlled Object has reached the end of its lifecycle.

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

- What is the Controlled Object?
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

That may be operationally acceptable for a narrower environment, but it provides a weaker foundation for independent verification, broad portability, and later dispute resolution.

The same generic model applies regardless of whether the Controlled Object represents:

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
