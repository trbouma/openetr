# OpenETR Electronic Bill of Lading Domain Adapter Design Note

This note describes how OpenETR can support an electronic bill of lading (`eBL`) workflow without turning the OpenETR core protocol into a maritime data model.

It is informed by the design position that a serious eBL is not merely a PDF representation of a paper bill of lading. It is a controlled maritime data product with structured semantics, validation rules, lifecycle state, authority checks, version history, presentation, surrender, and cross-system interoperability.

The OpenETR design question is:

> Which parts belong in a bill-of-lading domain adapter, and which parts belong in the generic OpenETR control layer?

## Summary

OpenETR should treat an electronic bill of lading as a domain-specific Controlled Object.

The OpenETR core should provide:

- digest-based object identity
- signed origin and control events
- control graph traversal
- transfer, acceptance, encumbrance, discharge, redemption, termination, and attestation primitives
- linked evidence records
- verifier policy warnings
- recognition-layer separation

The eBL domain adapter should provide:

- maritime terminology
- bill-of-lading data semantics
- DCSA, UN/CEFACT, UNECE, IMO, ISO, and carrier-specific mappings
- cargo and container validation
- document lifecycle status
- control status presentation
- regulatory and cargo-release status integration
- amendment and version-management workflows
- user-facing actions such as issue, transfer, present, surrender, cancel, and generate representation

The compact boundary is:

```text
eBL domain adapter:
maritime meaning, validation, roles, statuses, and workflows

OpenETR core:
digest identity, signed control events, graph traversal, and portable evidence

Recognition layer:
legal, registry, carrier, bank, contractual, or institutional effect
```

## Why A Domain Adapter Is Needed

A bill of lading is not just a file format.

The visible document is a representation of a deeper business record involving:

- trade parties
- shipment and routing
- cargo
- containers and transport equipment
- document and commercial information
- lifecycle metadata

These concepts have maritime, commercial, operational, and legal meanings that should not be collapsed into generic text fields or base OpenETR tags.

OpenETR can prove that a particular finalized artifact was identified by digest and that particular profile keys signed events about that artifact. It should not, in the base protocol, decide whether:

- a port code is valid
- a container number satisfies ISO 6346
- dangerous-goods data is complete
- a carrier agent is authorized to issue a bill of lading
- an amendment is permitted in the current document state
- a surrendered bill of lading allows cargo release
- a transferee has legal holder status under the governing law

Those are domain adapter, verifier policy, and recognition-layer questions.

## Layer Mapping

An eBL implementation should keep five layers distinct.

| Layer | Purpose | OpenETR Placement |
| --- | --- | --- |
| Document semantics | Defines the bill-of-lading business concepts and fields. | Domain adapter |
| Reference data | Provides code lists and standards for locations, units, packages, containers, cargo, and parties. | Domain adapter / recognition inputs |
| Business validation | Checks field, cross-field, conditional, state, and authorization rules. | Domain adapter / verifier policy |
| Lifecycle and authority | Tracks issue, amendment, transfer, presentation, surrender, cancellation, and control. | Domain adapter over OpenETR control graph |
| Interoperability | Aligns APIs, messages, statuses, and data structures across systems. | Domain adapter plus OpenETR wire format |

The OpenETR core provides the common control substrate. The eBL adapter supplies the maritime rulebook and vocabulary.

## Controlled Object Model

There are at least two possible object models.

### Final Artifact As Controlled Object

The simplest model treats the finalized bill-of-lading artifact as the Controlled Object.

```text
final eBL artifact
  -> SHA-256 digest
  -> OpenETR origin event
  -> control graph
```

This is appropriate where the relying party needs to verify that the presented artifact is the exact issued, amended, transferred, presented, or surrendered artifact.

The artifact may be:

- a PDF
- a JSON package
- an XML package
- a signed archive
- a wrapped trade-document envelope
- another canonical distribution format

In this model, the eBL data system remains the master data system. OpenETR records control evidence for the finalized artifact.

### Structured Record As Controlled Object

A more integrated model treats a canonical structured record as the Controlled Object.

```text
canonical eBL data package
  -> canonicalization
  -> SHA-256 digest
  -> OpenETR origin event
  -> generated human-readable representations
```

This is appropriate where the authoritative eBL is a structured data product and the PDF or printable view is only a representation.

This model requires stronger canonicalization rules:

- field ordering
- encoding
- numeric precision
- date and time format
- code-list representation
- null and optional-field treatment
- attachment or linked-evidence treatment

Without a stable canonicalization rule, different systems may compute different digests for the same business record.

### Recommended Starting Point

For early OpenETR eBL work, the final artifact model is safer.

It avoids overloading OpenETR with a full maritime canonical data format while still supporting:

- reliable identification
- whole-artifact integrity
- control graph creation
- transfer evidence
- surrender evidence
- verifier reconstruction

A later profile can introduce canonical structured eBL packages once the data model and canonicalization rules are mature.

## eBL Information Domains

The eBL adapter should define structured fields across six domains.

### Trade Parties

The adapter should distinguish organizations from the roles they perform.

Relevant roles may include:

- shipper or consignor
- consignee
- notify party
- carrier
- freight forwarder
- shipping agent
- issuing agent
- endorsee
- authorized representative
- current holder or controller

A single organization may perform multiple roles, but each role can have different authority, notification, validation, and recognition consequences.

### Shipment And Routing

The adapter should model route and shipment concepts separately.

Examples include:

- place of receipt
- port of loading
- port of discharge
- place of delivery
- vessel name
- voyage number
- vessel identifier
- transshipment locations
- mode of transport
- estimated and actual movement timestamps

These fields should use standard location and transport references where possible.

### Cargo

The adapter should separate structured cargo data from free-text commercial descriptions.

Examples include:

- goods description
- cargo classification
- package type
- package count
- gross weight
- net weight
- volume
- marks and numbers
- country of origin
- commodity or harmonized classification
- dangerous-goods data
- temperature or handling requirements

Free text can remain available for commercial description and clauses, but data used for calculation, integration, regulatory review, or validation should be structured.

### Containers And Transport Equipment

For containerized cargo, each container should be a repeating business object.

Examples include:

- container number
- size and type
- equipment category
- seal numbers
- package count
- gross and net weights
- tare weight
- verified gross mass
- dangerous-goods association
- refrigeration settings
- damage or condition status

The adapter should not store multiple containers as one text block merely because a visual document can display them that way.

### Document And Commercial Information

The adapter should model document and commercial fields such as:

- bill-of-lading number
- document type
- issue date
- place of issue
- number of originals, where relevant
- freight-payment terms
- currency and charges
- clauses
- remarks
- signatures or approval references
- issuing party
- contractual references

These fields may affect validation, representation, recognition, and integration.

### Lifecycle Metadata

Lifecycle metadata should be treated as part of the controlled document history, not merely as an application log.

Examples include:

- current document version
- document status
- control status
- regulatory-review status
- cargo-release status
- creation timestamp
- validation timestamp
- issuance timestamp
- amendment history
- transfer history
- presentation history
- surrender event
- cancellation reason
- responsible user and organization
- generated representation history

OpenETR can preserve signed control events, but the domain adapter should decide how those events are displayed in bill-of-lading terms.

## Status Dimensions

The eBL adapter should avoid one overloaded status field.

Recommended status dimensions include:

### Document Lifecycle Status

Examples:

- `DRAFT`
- `VALIDATED`
- `ISSUED`
- `AMENDMENT_PENDING`
- `SUPERSEDED`
- `SURRENDERED`
- `CANCELLED`

### Control Status

Examples:

- `NOT_ASSIGNED`
- `HELD`
- `TRANSFER_PENDING`
- `TRANSFERRED`
- `RETURNED`

### Regulatory Status

Examples:

- `NOT_SUBMITTED`
- `SUBMITTED`
- `UNDER_REVIEW`
- `ACCEPTED`
- `REJECTED`

### Cargo-Release Status

Examples:

- `NOT_ELIGIBLE`
- `PENDING_DOCUMENTS`
- `READY_FOR_RELEASE`
- `RELEASED`
- `BLOCKED`

OpenETR directly helps with control status and control history. The other status dimensions are domain, regulatory, and operational overlays.

## Action Mapping

The eBL adapter should expose business actions, not generic database mutations.

| eBL action | OpenETR mapping |
| --- | --- |
| Create draft | Domain-system action outside OpenETR |
| Validate document | Domain validation / possible attestation |
| Generate representation | Domain-system action, possibly linked evidence |
| Issue bill of lading | OpenETR `ISSUE` / origin event |
| Request amendment | Domain workflow / possible attestation |
| Approve amendment | Domain workflow / possible `ATTEST` |
| Supersede version | Domain versioning plus new object or linked evidence |
| Transfer control | OpenETR `TRANSFER` initiate / accept |
| Record encumbrance | OpenETR `ENCUMBER` |
| Release encumbrance | OpenETR `DISCHARGE` |
| Present for surrender or performance | OpenETR `REDEEM` or eBL-specific presentation profile |
| Accept surrender / complete performance | OpenETR `TERMINATE` or eBL-specific termination profile |
| Cancel document | Domain cancellation plus OpenETR termination or attestation, depending on policy |

The adapter should keep the user-facing language maritime-specific while mapping actions to the generic OpenETR event family.

## Validation Model

The eBL adapter should define validation in several groups.

### Field-Level Validation

Examples:

- date format
- numeric precision
- valid currency code
- valid location code
- valid unit code
- valid package code
- valid container number structure
- valid container size and type
- permitted document-number format

### Cross-Field Validation

Examples:

- gross weight should not be lower than net weight
- document-level totals should reconcile with container-level totals
- freight amount should have an associated currency
- port of loading and port of discharge should be coherent for the route
- dangerous-goods cargo should include required dangerous-goods data
- refrigerated cargo should include temperature requirements

### Conditional Validation

Examples:

- container details are required for containerized cargo
- dangerous-goods fields are required when regulated cargo is declared
- transshipment fields are required for routes with intermediate legs
- freight-payment location is required when the commercial arrangement requires it
- seal details are required where sealed equipment is used

### Authorization Validation

Examples:

- who may issue
- who may approve amendments
- who may transfer control
- who may accept control
- who may request surrender
- who may accept surrender
- who may cancel
- who may view confidential information

Authorization validation may use profile records, EUDI Wallet credentials, trust registries, TRQP, carrier account systems, or other recognition inputs.

### State-Based Validation

Examples:

- drafts may be edited directly
- issued records require controlled amendment
- superseded versions should not be treated as active
- surrendered records should not be transferable again
- cancelled records remain in audit history but should not be recognized as active

Some state-based validation can be represented as OpenETR verifier-policy warnings. Other rules belong in the domain application before an event is signed.

## Standards Inputs

An eBL adapter should align with maritime and trade standards instead of inventing local vocabulary where accepted references exist.

Relevant standards and reference models include:

- UNCITRAL MLETR for transferable-record functional equivalence
- UN Layout Key for trade-document representation
- UN/LOCODE for trade and transport locations
- UNECE Recommendation 20 for units of measure
- UNECE Recommendation 21 for package and cargo codes
- ISO 6346 for freight container identification
- IMO IMDG Code for dangerous goods
- UN/CEFACT Multimodal Transport Reference Data Model
- IMO Compendium on Facilitation and Electronic Business
- DCSA Bill of Lading standards for container-shipping workflows and data exchange

These references should shape the domain adapter, not the OpenETR base protocol.

## Amendment And Versioning

The eBL adapter should preserve amendment history.

Changes after issuance should not silently overwrite the active record.

An amendment workflow should capture:

- requested change
- requesting party
- reason
- previous value
- proposed value
- approving or rejecting party
- decision timestamp
- previous version
- new version
- relationship between superseded and active records
- notifications

OpenETR has two possible implementation patterns.

### New Object Per Material Version

If an amendment changes the artifact bytes or canonical structured record, the amended version may become a new Controlled Object with its own digest.

The relationship between versions can be recorded through linked evidence or attestation events.

This pattern is simple and digest-correct.

### Same Business Record With Version Links

If a profile wants to treat all versions as one business record, the adapter may define a stable business identifier and link each version digest to that identifier.

This requires clear profile rules for:

- active version selection
- supersession
- amendment authority
- version conflict handling
- verifier presentation

OpenETR should not infer these rules from digest equality alone.

## Representation Boundary

The PDF or human-readable view should be treated as a representation unless the profile explicitly defines it as the Controlled Object.

A generated representation should identify:

- document number
- version
- status
- generation timestamp
- verification mechanism
- whether it is draft, issued, copy, superseded, surrendered, or cancelled

Printing or downloading a representation should not create another valid electronic original.

Changing the visual template should not change the underlying maritime record unless the profile defines the artifact itself as authoritative and therefore produces a new digest.

## Interoperability Boundary

An API is not enough for interoperability.

The eBL adapter should define:

- business definitions
- role meanings
- code lists
- lifecycle events
- status meanings
- error meanings
- version behavior
- authorization expectations
- amendment behavior
- surrender behavior
- date and time conventions
- unit conversion rules
- document identifiers

OpenETR contributes a portable signed event format and graph retrieval model, but the domain adapter must make the maritime meaning explicit.

## Non-Goals

The eBL adapter should not make the OpenETR core responsible for:

- a complete bill-of-lading schema
- carrier-specific form rendering
- maritime regulatory reporting
- customs or port-community system integration
- determining legal holder status
- determining title to goods
- deciding cargo-release eligibility
- resolving commercial disputes
- replacing DCSA, UN/CEFACT, IMO, ISO, or UNECE standards

Those matters belong in domain profiles, applications, standards mappings, recognition policies, contracts, registries, and legal frameworks.

## Recommended Roadmap

A practical OpenETR eBL roadmap should proceed in stages.

1. Treat the finalized eBL artifact as an opaque digest-identified Controlled Object.
2. Define an eBL domain adapter that maps issue, transfer, presentation, surrender, cancellation, and amendment language onto OpenETR events.
3. Add structured domain tags for document type, bill-of-lading number, carrier profile, vessel/voyage references, and version identifiers.
4. Add linked evidence support for structured maritime data packages, DCSA messages, carrier records, inspection evidence, and regulatory responses.
5. Define verifier-policy warnings for superseded versions, cancelled records, failed surrender, unknown carrier profiles, unresolved transfer attempts, and inconsistent version links.
6. Develop a canonical structured eBL package profile only after the semantic model and canonicalization rules are stable.

## Bottom Line

The article's useful design position is that an electronic bill of lading should be treated as a controlled maritime data lifecycle, not a PDF-generation exercise.

OpenETR agrees with that position but draws an architectural boundary.

The eBL domain adapter should own maritime semantics, validation, statuses, standards mappings, and user-facing workflows.

OpenETR should own the portable control graph:

```text
digest-identified object
  -> signed origin event
  -> signed control and evidence events
  -> verifier-derived candidate state
  -> recognition policy decides effect
```

This separation lets an eBL system become structured, validated, controlled, and interoperable without requiring the OpenETR core protocol to become a maritime document platform.

