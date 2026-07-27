# Bills of Lading

Bills of Lading are a major candidate OpenETR domain because they sit close to the core policy problem behind MLETR: making a transferable paper document work as a reliable electronic record.

The goal is not to turn OpenETR into a full carrier platform, maritime data system, or legal recognition engine.

The goal is to support an electronic bill of lading (`eBL`) domain adapter over the general OpenETR control layer.

## Bill Of Lading Use Case

A bill of lading is not just a PDF or a printable form.

In maritime trade, it may perform several functions:

- receipt for goods
- evidence of the contract of carriage
- document of title, where applicable
- control point for transfer, presentation, surrender, and cargo release
- operational reference for carriers, shippers, consignees, banks, ports, and authorities

Those functions are exactly why electronic bills of lading are important in MLETR-style work. The difficult problem is not displaying the document on a screen. The difficult problem is reliable identification, integrity, control, transfer, presentation, surrender, authority, and recognition across systems.

## OpenETR Fit

In an OpenETR eBL domain:

- the eBL artifact or canonical eBL data package is the **Controlled Object**;
- the eBL digest is the stable object identity;
- the issuing profile signs an origin control record;
- transfer, acceptance, encumbrance, presentation, surrender, cancellation, and termination can be represented as signed control or evidence events;
- related maritime data, DCSA messages, registry responses, C2PA-enabled media, or carrier records can be linked as evidence;
- verifier policy decides which graph branch or event is recognized for a relying context.

The compact model is:

```text
bill of lading artifact
  -> SHA-256 digest
  -> OpenETR origin record
  -> signed control and evidence graph
  -> eBL domain adapter interpretation
  -> recognition policy decides effect
```

## Domain Adapter Boundary

The eBL domain adapter should own maritime meaning.

That includes:

- shipper, consignee, notify party, carrier, issuing agent, endorsee, and current controller roles
- vessel, voyage, place of receipt, port of loading, port of discharge, and place of delivery data
- cargo, container, seal, weight, package, dangerous-goods, and temperature fields
- DCSA, UN/CEFACT, UN/LOCODE, ISO 6346, IMO, and related standards mappings
- document lifecycle status
- control status
- amendment and version-management rules
- presentation, surrender, cancellation, and replacement workflows
- cargo-release and regulatory status integration

The OpenETR core should not contain a full maritime schema. It should provide the reusable control fabric.

## Likely Domain Actions

An eBL workspace could map domain actions to OpenETR operations as follows.

| eBL action | OpenETR mapping |
| --- | --- |
| Issue bill of lading | Origin control record |
| Transfer control | `TRANSFER` initiate / accept |
| Record endorsement or instruction | `ATTEST` or profile-specific transfer evidence |
| Record pledge or financing interest | `ENCUMBER` |
| Release financing interest | `DISCHARGE` |
| Present for surrender or delivery | `REDEEM` or eBL-specific presentation profile |
| Complete surrender / return / lifecycle | `TERMINATE` or eBL-specific termination profile |
| Correct or amend | New object or version link plus attestation |
| Cancel | Termination, warning, or non-recognition event depending on policy |
| Link maritime evidence | Linked evidence record |

## Recognition Boundary

OpenETR can show:

- which eBL artifact was identified by digest
- who signed the origin and control events
- how transfer or presentation events are linked
- whether there are competing graph branches or policy warnings
- whether linked evidence points to the same object

OpenETR does not decide:

- whether the eBL satisfies MLETR
- whether a carrier was authorized to issue it
- whether title passed
- whether a transferee is a lawful holder
- whether cargo release is required
- whether a bank, port, court, registry, or carrier must recognize the graph

Those questions belong to MLETR enactments, carrier rules, contracts, registries, courts, banks, ports, authorities, and verifier policy.

## Source Specification

The current design note is:

[OpenETR Electronic Bill of Lading Domain Adapter Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_EBL_DOMAIN_ADAPTER_DESIGN_NOTE.md)

That note defines the recommended architecture in more detail: final artifact versus structured record object models, eBL information domains, status dimensions, action mapping, validation, standards inputs, amendment and versioning, representation boundary, interoperability, non-goals, and roadmap.
