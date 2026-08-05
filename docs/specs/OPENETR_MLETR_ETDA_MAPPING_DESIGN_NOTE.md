# OpenETR MLETR And ETDA Mapping Design Note

This note analyzes how the UNCITRAL Model Law on Electronic Transferable Records (`MLETR`) and the United Kingdom Electronic Trade Documents Act 2023 (`ETDA`) can map to OpenETR.

It is informed by Alan Davidson's comparative paper on MLETR and ETDA, which argues that MLETR offers the better template for international harmonization while ETDA provides a narrower domestic digitization model with some divergent terminology and structure.

## Status

Draft.

## Purpose

OpenETR is intended to provide a portable control and evidence layer for digest-identified controllable records.

MLETR and ETDA are legal instruments that make certain electronic records or documents capable of performing functions traditionally associated with paper transferable documents or instruments.

The design question is:

> How should OpenETR generate technical evidence that can be evaluated under MLETR-style and ETDA-style legal frameworks without becoming specific to either statute?

The short answer is:

```text
OpenETR provides signed object identity, integrity, control, transfer,
and lifecycle evidence.

MLETR, ETDA, contracts, registries, courts, and relying parties decide
whether that evidence satisfies the applicable legal gateway.
```

## Understanding The Problem Domain

Paper transferable documents and instruments work because possession of the paper object carries legal and commercial significance.

Examples include:

- bills of lading
- warehouse receipts
- bills of exchange
- promissory notes
- ship's delivery orders
- mate's receipts
- marine insurance policies
- cargo insurance certificates

These instruments may allow a holder to claim performance of an obligation, transfer the right to performance, or exercise rights associated with goods, payment, finance, or transport.

The legal problem is that electronic information does not naturally behave like paper.

Paper has a physical scarcity property. One can ask who possesses the paper document. Electronic information can be copied, synchronized, exported, forwarded, screenshotted, or stored in multiple systems. The functional-equivalence problem is therefore not simply:

```text
Can a document be electronic?
```

It is:

```text
Can an electronic method perform the legal functions that paper possession,
delivery, integrity, endorsement, and replacement performed?
```

MLETR and ETDA answer that problem in different but related ways.

OpenETR should not attempt to enact either answer. It should preserve the technical evidence that those legal answers require.

## Core Mapping

The compact mapping is:

| Legal Function | MLETR Framing | ETDA Framing | OpenETR Evidence |
| --- | --- | --- | --- |
| Identify the relevant electronic record | Identify `the` electronic transferable record | Identify the document so it can be distinguished from copies | Controlled Object digest and origin event |
| Preserve integrity | Complete and unaltered except authorized or normal technical changes | Protection against unauthorized alteration | Digest, canonicalization profile, signed event graph, linked evidence |
| Establish control | Exclusive control by a person | Not possible for more than one person to exercise control at one time | Current-controller derivation from signed control graph |
| Identify controller | Identify person in control | Allow person able to exercise control to demonstrate that ability | signer profile, participant tags, recognition inputs, verifier policy |
| Transfer control | Transfer of control over the electronic record | Transfer deprives prior controller unless also transferee | transfer event linked to prior control state |
| Replace paper/electronic medium | Reliable change of medium; old form made inoperative | conversion statement; old form ceases to have effect | change-of-medium events, termination/reissuance, linked conversion evidence |
| Endorsement | Information required for endorsement included and signed | inferred through control, use, transfer, or disposal | endorsement as attestation, transfer metadata, or domain control event |
| Reliability | reliable method, function-specific, with ex post safety clause | reliable system, document-system oriented | verifier policy over OpenETR method, infrastructure, and achieved function |

OpenETR is not itself the MLETR or ETDA compliance layer.

It is the evidence layer that can help a domain adapter answer:

- Which electronic record is being evaluated?
- What artifact or package does it identify?
- Has the artifact remained unchanged?
- Which control events exist?
- Who signed them?
- Which participant appears to be the current controller?
- Was a transfer linked to the previous control state?
- Was the previous controller deprived of control under the evaluated policy?
- Which method, system, registry, or operational rules support reliability?
- Which warnings or unresolved conditions remain?

## MLETR Orientation

MLETR is structured as a model law for broad international adoption.

For OpenETR, its most important design signals are:

- technology neutrality
- functional equivalence
- international harmonization
- preservation of substantive law
- focus on transferable records rather than platform-specific systems
- reliable methods for specific legal functions
- explicit treatment of exclusive control
- lifecycle language from creation until effect or validity ends
- change-of-medium provisions
- non-discrimination for foreign electronic transferable records

OpenETR aligns well with that orientation because it is protocol-level infrastructure rather than a closed platform.

An OpenETR implementation can support MLETR-style analysis by producing evidence for:

- identification of the electronic transferable record
- integrity of the record and authorized changes
- control from creation through termination
- exclusive control by a person or recognized participant
- transfer of control
- identification of the person in control
- linked endorsements and attestations
- change of medium from paper to electronic or electronic to paper
- verifier-policy analysis of reliability

The OpenETR core should stay neutral about the substantive rights attached to the document. A bill of lading, warehouse receipt, promissory note, or insurance certificate may have different legal consequences in different jurisdictions. OpenETR should expose the control graph. Domain law decides the effect.

## ETDA Orientation

ETDA is national legislation. It is aimed at making certain electronic trade documents capable of possession, indorsement, and transfer under UK law.

For OpenETR, its most important design signals are:

- gateway criteria for an electronic trade document
- a narrower definition of eligible paper trade documents
- emphasis on documents commonly used in at least one part of the United Kingdom in trade, transport, or financing
- a reliable system rather than a reliable method
- ability to distinguish the document from copies
- protection against unauthorized alteration
- prevention of concurrent control by more than one person
- ability of the controller to demonstrate control
- transfer that deprives the previous controller of control
- conversion between paper and electronic forms

OpenETR can support ETDA-style analysis by presenting the control graph as evidence that a reliable system or method:

- identifies the document
- distinguishes the operative controlled object from non-operative copies or representations
- protects the document through digest integrity and signed event history
- represents only one recognized controller at a time under the selected policy
- lets a controller demonstrate control by presenting the signed graph
- records transfer events that supersede prior control
- records conversion statements and lifecycle effects

OpenETR should not hard-code ETDA's narrower statutory scope into the core.

Instead, an ETDA recognition profile or domain adapter can ask:

```text
Does this Controlled Object fall within ETDA Section 1?
Does the selected OpenETR deployment satisfy the reliable-system gateway?
Does the control graph support possession, indorsement, transfer, and conversion?
```

## Design Boundary

The key boundary is:

```text
OpenETR:
  technical evidence of object identity, integrity, control, transfer,
  lifecycle, signatures, linked evidence, and graph continuity

Domain adapter:
  document family, vocabulary, schemas, roles, workflow actions,
  statuses, domain validation, and presentation

Recognition profile:
  MLETR, ETDA, local enactment, contract, registry rulebook,
  institutional policy, or court-facing legal analysis
```

OpenETR should avoid two mistakes.

First, it should not treat a valid signature or digest as legal control by itself.

Second, it should not restrict the core to one statute's language, such as ETDA's `electronic trade document` terminology or MLETR's `electronic transferable record` terminology.

The core concept should remain broader:

```text
Controlled Object + signed control graph + recognition context
```

## Electronic Record And Controlled Object

MLETR uses the concept of an electronic record that becomes the electronic transferable record.

ETDA refers to information in electronic form that, together with logically associated information, constitutes an electronic trade document.

OpenETR should map both to a Controlled Object.

The Controlled Object may be:

- a final artifact
- a canonical structured record
- a document package
- a signed bundle
- a record plus logically associated metadata
- a change-of-medium package

The adapter must define what is hashed.

For early implementations, the safest strategy remains:

```text
final artifact or canonical package
  -> digest
  -> origin event
  -> control graph
```

Where the legal framework treats logically associated information as part of the document, the adapter should include that information in the canonical package or link it explicitly as required evidence.

## Copies, Originals, And Operative Records

The comparison paper highlights ambiguity in ETDA's use of `copies` for electronic documents.

OpenETR should avoid building a copy/original metaphysics into the core.

Instead, it should distinguish:

- the digest-identified Controlled Object
- non-operative representations
- replicas of the same bytes
- exported views
- linked evidence
- multiple legally recognized originals where the domain permits them
- replacement or termination events that make a prior object inoperative

An exact byte copy of a Controlled Object should not create a new operative object merely because it is stored somewhere else.

The operative question is whether the presented artifact is linked to a recognized control graph and whether the selected policy treats that graph as effective.

## Integrity

Integrity maps cleanly to OpenETR, but the adapter must be precise.

OpenETR can provide:

- digest identity
- signature validation
- event immutability
- prior-event references
- linked evidence digests
- canonicalization warnings
- authorized-change events
- replacement and termination events

OpenETR should distinguish:

- artifact integrity
- event integrity
- graph integrity
- lifecycle integrity
- recognition integrity

For MLETR-style analysis, integrity includes authorized changes and normal technical changes that arise through communication, storage, or display.

For ETDA-style analysis, integrity includes protection against unauthorized alteration and measures supporting system reliability.

The domain adapter should state which changes create:

- a new Controlled Object
- an authorized amendment event
- a linked evidence update
- a non-operative representation
- a verifier warning
- termination and replacement

## Control

Control is the center of the mapping.

MLETR asks whether a reliable method establishes exclusive control and identifies the person in control.

ETDA asks whether a reliable system secures that more than one person cannot exercise control at the same time and allows the person able to exercise control to demonstrate that ability.

OpenETR can model this as:

```text
origin event
  -> transfer or control event
  -> optional acceptance event
  -> optional encumbrance/discharge events
  -> current-controller derivation
  -> verifier-policy result
```

The OpenETR control graph is not merely a list of signatures.

It should show:

- which object is controlled
- who issued or originated the object
- who was recognized as controller at each step
- which event transferred or changed control
- which prior event was consumed or superseded
- whether there are conflicting branches
- whether encumbrances, holds, or terminations affect control
- which policy was used to derive the candidate current controller

OpenETR should use `exclusive control` as the conceptual north star even when supporting an ETDA profile that phrases the gateway differently.

This preserves interoperability with MLETR-style jurisdictions and avoids reducing control to platform possession.

## Transfer

Transfer should be represented as an explicit Control Event.

A transfer event should normally include:

- object digest
- transferor or prior controller reference
- transferee reference
- prior control event reference
- transfer intent
- timestamp
- signer profile
- optional acceptance or countersignature evidence
- optional endorsement metadata
- policy or domain tags

For MLETR, the transfer event supports the functional equivalence of transfer of possession through transfer of control.

For ETDA, the transfer event should also support evidence that the previous controller was deprived of the ability to exercise control unless they are also a transferee.

OpenETR cannot guarantee deprivation in a physical or metaphysical sense. It can provide evidence that the recognized control graph no longer treats the previous controller as current controller under the selected policy.

That distinction should be explicit:

```text
OpenETR deprivation evidence:
  the graph no longer recognizes the transferor as current controller

Legal deprivation conclusion:
  the selected ETDA or domain recognition policy treats that evidence as sufficient
```

## Reliability

The article's MLETR/ETDA comparison is especially important for reliability.

MLETR frames reliability as a method that is appropriate for the function being performed and also includes an ex post safety clause where the method is proven in fact to have fulfilled the function.

ETDA frames reliability around a system and lists factors that may be taken into account when determining whether the system is reliable.

OpenETR should support both views by producing method-level and system-level evidence.

### Method-Level Evidence

Method-level evidence concerns the function performed in a particular transaction.

Examples:

- digest identified the record
- signature bound the event to a signer
- transfer event referenced the prior control event
- current-controller derivation produced one recognized controller
- linked evidence matched its digest
- archived event was retrievable
- replacement event terminated the prior medium

This aligns strongly with MLETR.

### System-Level Evidence

System-level evidence concerns the operating environment.

Examples:

- operational rules
- relay policy
- profile governance
- hardware or software security claims
- audit results
- supervisory, accreditation, or voluntary-scheme assessments
- industry standards
- retention and recovery practices
- access-control model

This aligns strongly with ETDA.

OpenETR should allow a verifier policy to evaluate both:

```text
transaction evidence:
  did the method work for this object and this event?

system evidence:
  does the surrounding operating environment support reliability?
```

## Change Of Medium

Both MLETR and ETDA address conversion between paper and electronic forms.

OpenETR should represent change of medium as a specific lifecycle pattern, not as an informal note.

Potential events include:

- `CONVERT_FROM_PAPER`
- `CONVERT_TO_PAPER`
- `TERMINATE_PRIOR_MEDIUM`
- `ISSUE_REPLACEMENT`
- `ATTEST_CONVERSION_STATEMENT`

The linked evidence should include:

- image or scan of the prior paper document if appropriate
- conversion statement
- authority or custodian attestation
- prior object reference if electronic
- new object digest
- termination or inoperative-state evidence for the old medium

The adapter should support MLETR's concern that the prior form becomes inoperative and ceases to have effect or validity, and ETDA's concern that the old form ceases to have effect while rights and liabilities continue in relation to the new form.

## Endorsement

MLETR expressly addresses endorsement.

ETDA appears to rely on the ability of a person in control to use, transfer, indorse, or otherwise dispose of the document, rather than providing the same specific endorsement provision.

OpenETR should model endorsement explicitly where the domain requires it.

An endorsement may be:

- metadata on a transfer event
- a separate signed attestation
- a domain-specific control event
- a linked representation attached to the record

The adapter should define:

- required endorsement information
- required signer
- relationship to transfer
- whether endorsement changes control
- whether endorsement is merely evidentiary
- how endorsements appear in human-readable views

## Party Autonomy

Both MLETR and ETDA preserve some room for parties to vary or exclude certain effects.

OpenETR should not hide this from verifiers.

The adapter should support:

- contract references
- governing-law tags
- opt-out indicators
- rulebook identifiers
- platform terms
- party autonomy evidence
- warnings where an action appears valid cryptographically but may be excluded contractually

Party autonomy should be recognition context, not core protocol truth.

## Foreign Records And Interoperability

MLETR contains an explicit non-discrimination principle for records issued or used abroad.

ETDA does not contain the same express provision and is more domestically scoped.

This difference matters for OpenETR because OpenETR is intended to support portable evidence across platforms and jurisdictions.

The OpenETR core should therefore remain jurisdiction-neutral.

Jurisdiction-specific adapters may evaluate whether a given Controlled Object is recognized under:

- MLETR enactment
- ETDA
- local trade law
- contractual choice of law
- registry rulebook
- institutional policy
- court or agency practice

But the base graph should remain inspectable even when the recognition result differs by jurisdiction.

## Domain Adapter Implications

An MLETR/ETDA-aware domain adapter should define the following.

### Scope

The adapter should state which document family is covered:

- bill of lading
- warehouse receipt
- bill of exchange
- promissory note
- insurance certificate
- delivery order
- other transferable document or instrument

### Eligibility

The adapter should test whether the object falls within the selected framework:

- MLETR transferable document or instrument
- ETDA paper trade document / electronic trade document
- local enactment of MLETR
- contract or platform rulebook
- institutional recognition policy

### Object Strategy

The adapter should specify:

- final artifact as object
- canonical structured record as object
- package as object
- logically associated information
- treatment of non-operative representations
- treatment of multiple originals

### Control Actions

The adapter should map domain actions to OpenETR operations:

| Domain Action | OpenETR Operation |
| --- | --- |
| issue electronic record | `ISSUE` |
| transfer control | `TRANSFER` |
| accept control | acceptance evidence or domain event |
| endorse | `ATTEST` or transfer metadata |
| pledge or restrict | `ENCUMBER` |
| release pledge or restriction | `DISCHARGE` |
| present for performance | `REDEEM` or presentation evidence |
| convert paper to electronic | change-of-medium profile |
| convert electronic to paper | change-of-medium profile |
| cancel or complete lifecycle | `TERMINATE` |

### Reliability Evidence

The adapter should expose both:

- function-specific evidence that a method worked
- system-level evidence that the operating environment is reliable

### Recognition Result

The adapter should present recognition as a policy-dependent result:

```text
cryptographically valid:
  yes / no

control graph structurally valid:
  yes / no / warnings

recognized under selected framework:
  MLETR profile / ETDA profile / local law / contract / registry / not evaluated
```

## Recommended OpenETR Position

OpenETR should treat MLETR as the stronger default alignment target for international trade because it is model-law based, technology-neutral, and designed for harmonization.

OpenETR should also support ETDA because English law and UK-based trade practice are commercially important.

The implementation stance should be:

```text
Build the core around generic controllable records and MLETR-compatible
functional evidence.

Implement ETDA as a recognition profile and domain-adapter policy,
not as the default vocabulary of the core.
```

This lets OpenETR serve both:

- MLETR-style international harmonization
- ETDA-style UK recognition

without becoming trapped in either legal vocabulary.

## Non-Goals

OpenETR should not:

- decide whether a document is legally valid under MLETR or ETDA
- replace national enactment of MLETR
- replace ETDA reliable-system analysis
- decide substantive rights under bills of lading, warehouse receipts, bills of exchange, or promissory notes
- guarantee legal possession merely because an event is signed
- hard-code one jurisdiction's statutory scope into the core
- treat every electronic copy as a new operative original
- infer reliable-system status from cryptography alone
- collapse technical control into legal recognition

## Recommended Roadmap

1. Define an MLETR recognition profile over existing OpenETR control events.
2. Define an ETDA recognition profile over existing OpenETR control events.
3. Add structured verifier output that separates cryptographic validity, control-graph validity, and recognition result.
4. Extend change-of-medium profiles for paper-to-electronic and electronic-to-paper conversion.
5. Define endorsement handling for bills of lading and other documents where endorsement matters.
6. Add reliability evidence fields for method-level and system-level assessment.
7. Add policy warnings for multiple originals, non-operative copies, missing prior-event references, unresolved encumbrances, and unsupported jurisdiction claims.
8. Publish domain-specific mappings for bills of lading and warehouse receipts.

## Open Questions

- Should OpenETR define a generic `recognized_framework` field for verifier output?
- Should reliability evidence be represented as linked evidence or as a dedicated event type?
- How should OpenETR represent multiple legally recognized originals where substantive law permits them?
- Should transfer always require acceptance evidence, or should that remain domain-specific?
- Should ETDA reliable-system evidence be attached to every object, every profile, or the deployment as a whole?
- How should a verifier distinguish between byte copies, exported views, replicas, and operative records?
- What is the minimum change-of-medium event shape required for MLETR and ETDA profiles?
- Should endorsement be an `ATTEST` event, a transfer attribute, or a domain-specific event?

## Related Policy Brief

- [OpenETR, MLETR, And ETDA](../../docs-site/policy-briefs/openetr-mletr-and-etda.md)

## References

- Alan Davidson, `Comparison and Application of the Model Law of Electronic Transferable Records and the Electronic Trade Documents Act 2023 (UK)`, 2026.
- [OpenETR Generic Domain Adapter Specification](./OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR Generic Transfer Model](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Control Event Minimum Shapes](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [MLWR Change Of Medium Profile](./MLWR_CHANGE_OF_MEDIUM_PROFILE.md)
- [OpenETR Electronic Bill of Lading Domain Adapter Design Note](./OPENETR_EBL_DOMAIN_ADAPTER_DESIGN_NOTE.md)
