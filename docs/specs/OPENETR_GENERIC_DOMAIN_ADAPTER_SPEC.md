# OpenETR Generic Domain Adapter Specification

This specification defines the generic role of a domain adapter in OpenETR.

It is intended to make clear what OpenETR does, what a domain adapter does, and what remains outside both in the Recognition Layer.

## Status

Draft.

## Purpose

OpenETR is a general control layer for durable electronic records.

Different domains need different language, data models, validation rules, roles, workflows, and recognition frameworks. A warehouse receipt system should speak warehouse-receipt language. A bill-of-lading system should speak maritime transport language. An Apostille workflow should speak Competent Authority and e-Register language. A Product Passport workflow should speak product, lifecycle, compliance, and evidence language.

The domain adapter is the boundary object between those domain workflows and the generic OpenETR control layer.

The design goal is:

```text
Domain adapters make OpenETR useful in a specific domain
without making the OpenETR core specific to that domain.
```

## Layer Model

OpenETR systems should keep four layers distinct.

```text
Domain adapter
  domain vocabulary, workflows, validation, UI/API, rulebook-specific state

OpenETR control layer
  Controlled Objects, control records, control graphs, profile signing,
  transfer/attest/encumber/discharge/redeem/terminate primitives

Wire format
  signed events, kinds, tags, relays, event ids, object queries

Recognition layer
  law, contracts, registries, trust frameworks, institutional policy,
  competent authorities, relying-party decisions
```

The domain adapter sits above OpenETR. It translates domain actions into OpenETR operations and translates OpenETR graph results back into domain language.

## What OpenETR Core Does

The OpenETR core provides generic control and evidence infrastructure.

It defines:

- digest-identified Controlled Objects
- origin records
- control records
- linked evidence records
- signed event publication and retrieval
- object-centric graph queries
- control graph traversal
- profile-backed signing
- participant references
- generic lifecycle events
- verifier policy warnings
- candidate state derivation

OpenETR core answers questions such as:

- What object digest is being referenced?
- Which signed events exist for that object?
- Which profile key signed each event?
- How do events link through prior-event references?
- What candidate control graph can be reconstructed?
- What generic control state can be derived under a selected policy?
- What warnings arise from structural or baseline-policy checks?

OpenETR core should remain domain-neutral.

It should not need to know whether the object is a warehouse receipt, bill of lading, Apostille package, Product Passport, health record, certificate, credential, permit, or another controllable record.

## What OpenETR Core Does Not Do

OpenETR core does not decide:

- legal title
- ownership
- contractual rights
- priority
- protected-holder status
- KYC or AML sufficiency
- regulatory compliance
- public-authority competence
- document-content sufficiency
- cargo-release eligibility
- medical consent validity
- Product Passport regulatory completeness
- Apostille recognition
- whether a relying party must accept a record

It also should not contain:

- complete domain schemas
- jurisdiction-specific legal rules
- carrier-specific bill-of-lading forms
- warehouse-specific receipt templates
- healthcare data models
- Apostille e-Register policy
- product-category delegated-act rules
- local registry account models

Those concerns belong to domain adapters, recognition profiles, external systems, or relying-party policy.

## What A Domain Adapter Does

A domain adapter presents OpenETR in domain language.

It is responsible for:

- domain vocabulary
- user-facing workflows
- domain API actions
- domain data schemas
- domain-specific validation
- domain-specific status labels
- role mapping
- profile selection and actor mapping
- domain event tags
- linked evidence conventions
- warning presentation
- recognition-input selection
- integration with external systems
- human-readable rendering

The adapter should make a domain workflow feel natural while keeping the underlying control evidence portable.

Examples:

- an MLWR adapter maps "pledge receipt" to `ENCUMBER`
- an eBL adapter maps "surrender bill of lading" to `REDEEM` or an eBL presentation profile
- an Apostille adapter maps "attach e-Register reference" to linked evidence
- a Product Passport adapter maps "attach repair evidence" to linked evidence or `ATTEST`

## What A Domain Adapter Does Not Do

A domain adapter does not, by itself, create legal effect.

It should not claim that a signed event automatically satisfies:

- MLETR
- MLWR
- Apostille Convention recognition
- Product Passport regulation
- healthcare consent law
- secured-transactions law
- customs or port rules
- bank policy
- registry rules
- court or agency acceptance

The adapter may implement local policy checks, but those checks are not the same as universal recognition.

The adapter may say:

```text
Under this selected verifier policy, this graph is recognized.
```

It should not say:

```text
OpenETR itself makes this legally effective everywhere.
```

## Generic Adapter Responsibilities

Every domain adapter should define the following.

### Domain Scope

The adapter should state:

- record types covered
- record types excluded
- applicable domain vocabulary
- intended users
- intended relying parties
- relevant external standards or rulebooks
- recognition assumptions

### Controlled Object Strategy

The adapter should define what is hashed.

Possible strategies include:

- final artifact as Controlled Object
- canonical structured record as Controlled Object
- package or bundle as Controlled Object
- public document as Controlled Object with linked evidence
- evidence artifact as linked object

The adapter must specify:

- canonicalization rules, if any
- package finalization rules
- digest algorithm
- whether transformations create new objects
- how versions are related
- how generated representations are treated

### Domain Roles

The adapter should map domain roles to OpenETR participant roles.

Examples:

- warehouse operator -> issuer / obligor / attestor
- receipt holder -> current controller
- carrier -> issuer / obligor
- shipper -> transferor or participant
- consignee -> transferee or relying party
- Competent Authority -> recognized attestor or authority source
- manufacturer -> issuer or attestor
- repairer -> linked-evidence attestor

This mapping should not imply legal authority by itself. Authority must be established by recognition inputs or policy.

### Domain Actions

The adapter should map domain actions to OpenETR operations.

Generic operations include:

- `ISSUE`
- `TRANSFER`
- `ATTEST`
- `ENCUMBER`
- `DISCHARGE`
- `REDEEM`
- `TERMINATE`
- linked evidence creation
- verifier annotation

The adapter should define whether each domain action:

- publishes an OpenETR event
- creates linked evidence
- runs local validation only
- consults recognition inputs
- updates only the domain system
- produces a human-readable representation

### Domain Event Tags

The adapter should define signed tags needed for domain interpretation.

Common generic tags include:

- `["domain", "<domain_id>"]`
- `["document_type", "<type>"]`
- `["record_reference", "<domain_reference>"]`
- `["record_description", "<short_description>"]`
- `["jurisdiction", "<jurisdiction>"]`
- `["version", "<profile_or_record_version>"]`

Domain-specific tags should be stable, documented, and machine-readable.

The event `content` field should remain human-readable context. It should not be the primary machine interface for domain data.

### Domain Validation

The adapter should define validation rules.

Categories may include:

- field-level validation
- cross-field validation
- conditional validation
- state-based validation
- authorization validation
- external-reference validation
- schema validation
- canonicalization validation
- linked-evidence validation

Validation may occur:

- before event publication
- during graph verification
- during recognition-policy evaluation
- during external-system integration

The adapter should distinguish each stage.

### Status Dimensions

The adapter should avoid one overloaded status field.

It should define separate status dimensions where the domain requires them.

Examples:

- document lifecycle status
- control status
- regulatory status
- cargo-release status
- registry verification status
- recognition status
- evidence completeness status
- privacy or access status

OpenETR may derive generic control state. The adapter decides how to present domain state.

### Linked Evidence Model

The adapter should define which artifacts are linked evidence rather than the main Controlled Object.

Examples:

- inspection reports
- registry responses
- e-Register lookups
- repair records
- certificates
- translations
- shipment data packages
- C2PA-enabled media
- authority credentials
- verifier reports

Linked evidence should remain digest-addressed and independently verifiable where possible.

### Recognition Inputs

The adapter should identify relevant recognition inputs.

Examples:

- trust registries
- Competent Authority lists
- domain registries
- local allow lists
- KYC providers
- EUDI Wallet credentials
- Verifiable Credentials
- Nostr Web of Trust signals
- TRQP responses
- contracts
- statute or regulation
- institutional policy

The adapter should treat these inputs as recognition context, not base OpenETR truth.

### Privacy And Storage

The adapter should define what may safely be published.

It should distinguish:

- public event metadata
- private document bytes
- sensitive personal data
- regulated data
- commercial data
- storage location
- relay policy
- retention policy
- redaction rules

OpenETR should not require sensitive content to be published on public relays. Digest-linked evidence can be useful even when the underlying bytes remain in controlled storage.

## Generic Domain Adapter Template

A domain adapter specification should use this structure unless there is a reason to deviate:

1. Status
2. Purpose
3. Architectural boundary
4. Domain model
5. Controlled Object strategy
6. Domain roles
7. Domain actions and OpenETR mapping
8. Suggested event tags
9. Validation model
10. Status dimensions
11. Linked evidence model
12. Recognition inputs
13. Privacy and storage
14. Non-goals
15. Recommended roadmap
16. Open questions
17. References

## Adapter Categories

OpenETR can support different categories of domain adapter.

### Transferable-Record Adapters

These adapters use control transfer as a central workflow.

Examples:

- warehouse receipts
- bills of lading
- promissory notes

They commonly map domain actions to `ISSUE`, `TRANSFER`, `ENCUMBER`, `DISCHARGE`, `REDEEM`, and `TERMINATE`.

### Non-Transferable Controllable-Record Adapters

These adapters focus on issuance, status, authority, evidence, verification, and lifecycle, but may not require transfer of control.

Examples:

- Apostille documents
- Product Passports
- certificates
- permits
- health-record packages

They commonly use `ISSUE`, `ATTEST`, linked evidence, warning, replacement, revocation, and verifier-policy annotations.

### Evidence-Graph Adapters

These adapters focus on associating many evidence artifacts with a primary object.

Examples:

- Product Passport lifecycle evidence
- compliance evidence
- repair history
- audit records
- inspection media

They commonly rely on linked evidence records and attestation events.

### Credential-Supported Adapters

These adapters use credentials or wallets as authority inputs.

Examples:

- EUDI Wallet-supported authority proof
- Verifiable Credential-backed role proof
- mDL or identity-backed signer recognition

The credential may be the Controlled Object, linked evidence, or a recognition input.

## Validation Versus Recognition

Domain adapters should distinguish validation from recognition.

Validation asks:

- Is the data complete?
- Is the event structurally sound?
- Is the action allowed by the local workflow?
- Does the record satisfy the adapter's schema?
- Are required references present?

Recognition asks:

- Will this verifier rely on the event?
- Does the signer have authority?
- Does a law, registry, or institution accept the evidence?
- Is the action legally or commercially effective?
- Does the record satisfy the governing rulebook?

A domain adapter may implement both validation and recognition-policy evaluation, but it should label them separately.

## Publication Versus Recognition

OpenETR is an open signed-event system.

The fact that an event can be published does not mean that every verifier must recognize it.

Domain adapters should preserve this distinction:

```text
event exists
  -> signature and structure can be verified
  -> graph can be traversed
  -> adapter can interpret domain meaning
  -> recognition policy decides effect
```

This is the practical meaning of:

```text
Transact globally, validate locally.
```

## Non-Goals

A generic domain adapter specification should not:

- redefine the OpenETR core wire format
- put domain-specific legal rules into the base protocol
- imply that all domains are transferable records
- require public storage of sensitive documents
- replace official registries or authorities
- claim universal legal effect
- hide policy differences behind cryptographic validity
- make `content` parsing part of the machine contract

## Conformance Expectations

A domain adapter is conformant with this generic specification if it:

- identifies its Controlled Object strategy
- maps domain actions to OpenETR operations
- documents its domain tags
- documents its validation stages
- separates technical verification from recognition
- identifies relevant recognition inputs
- defines privacy and storage expectations
- states non-goals and recognition limits
- preserves OpenETR core event semantics

## Existing And Candidate Adapters

Current or candidate adapters include:

- MLWR warehouse receipts
- electronic bills of lading
- Apostille documents
- Product Passports
- health records
- credentials and attestations
- C2PA-linked media evidence
- secured finance records

Each should be documented as a domain-specific profile or adapter specification that refers back to this generic boundary.

## Bottom Line

The domain adapter is where OpenETR becomes useful to a real domain.

It is also where OpenETR avoids becoming trapped inside one domain.

The core rule is:

```text
OpenETR records portable signed control and evidence facts.
Domain adapters translate those facts into domain workflows.
Recognition layers decide legal, regulatory, institutional, or commercial effect.
```

