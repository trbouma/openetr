# OpenETR As Fabric

OpenETR is best understood as infrastructure fabric, not as the finished clothing for any one domain.

That distinction matters.

A fabric can be cut, layered, reinforced, dyed, lined, and tailored into many different garments. The same underlying material can become workwear, formalwear, sportswear, medical textiles, protective equipment, or industrial coverings. The fabric matters enormously, but it is not the final product by itself.

OpenETR plays a similar role for durable electronic records.

It supplies a reusable control-and-evidence material:

- digest-based Digital Artifact identity
- signed events
- Digital Controllable Records (DCRs)
- reproducible DCR validation under identified policies
- linked evidence
- profile-backed attribution
- artifact-centric retrieval
- verifier-policy warnings
- portable proof that can move across systems

Domain adapters turn that material into something domain-specific.

## The Clothing Analogy

The clothing industry changed when new fibers and technical fabrics made it possible to design garments with properties that older materials could not provide as easily.

Synthetic fibers, blends, membranes, elastic materials, and engineered textiles did not eliminate tailoring, fashion, uniforms, safety standards, or cultural meaning. They expanded what clothing could do.

The same material science could support:

- lightweight travel clothing
- flame-resistant workwear
- waterproof shells
- medical garments
- athletic compression wear
- everyday durable clothing
- specialized protective equipment

The fiber was not the whole garment. It was the enabling substrate.

OpenETR should be seen the same way.

It is not a warehouse receipt application, a bill-of-lading platform, an Apostille registry, a Product Passport database, or a health-record portal.

It is the control fabric from which those domain systems can build portable, verifiable record workflows.

## Fabric Versus Garment

The distinction can be summarized simply:

```text
OpenETR is the fabric.
Domain adapters are the clothing.
Recognition frameworks decide where the clothing is acceptable.
```

Or, more technically:

```text
OpenETR:
common artifact, DCR, and state-derivation substrate

Domain adapter:
domain vocabulary, workflows, validation, roles, statuses, and presentation

Recognition layer:
law, registry policy, institutional rules, contracts, and relying-party decisions
```

This avoids two mistakes.

The first mistake is expecting the fabric to already be a finished garment.

OpenETR does not, by itself, provide every field, rule, screen, template, registry check, legal requirement, or business process for each domain.

The second mistake is making every garment out of a completely unrelated material.

If every domain invents its own closed control mechanism, then records become trapped inside platforms. Verification becomes bespoke. Transfer and evidence histories become hard to compare. Long-term portability suffers.

## What The Fabric Provides

Good fabric has reliable properties.

OpenETR's reusable properties are:

- a Digital Artifact can be identified by digest
- signed events can be independently verified
- DCR graphs can be reconstructed from portable signed records
- DCR evidence can be validated and explicit protocol rules can derive consequential state
- linked evidence can be attached without becoming the main object
- profile keys can attribute actions
- different verifiers can apply different recognition policies to the same evidence

These properties are useful across domains.

A warehouse receipt, bill of lading, Apostille package, Product Passport, health-record package, C2PA-linked media artifact, or certificate may have different domain meaning, but all can benefit from portable signed evidence about an identified object.

## What The Fabric Does Not Provide

Fabric does not decide whether an outfit is appropriate for court, surgery, a factory floor, a wedding, or a mountain expedition.

OpenETR likewise does not decide:

- whether a warehouse operator is licensed
- whether a bill of lading satisfies maritime or carrier requirements
- whether an Apostille is recognized by a receiving institution
- whether a Product Passport satisfies a delegated regulation
- whether a health-record disclosure has valid consent
- whether a security right is perfected
- whether a credential issuer is trusted

Those are domain and recognition questions.

OpenETR gives the Digital Artifact a durable DCR evidence structure and derives
its consequential state. It does not decide every rule that gives that state
legal, institutional, or commercial effect.

## Domain Adapter Role

Domain adapters are the tailoring layer.

They take the OpenETR fabric and shape it for a particular use case.

Examples:

| Domain | Adapter Clothing |
| --- | --- |
| Warehouse receipts | Receipt issuance, holder language, pledge, release, presentation, delivery |
| Bills of lading | Carrier, shipper, consignee, voyage, surrender, transfer, DCSA-aligned data |
| Apostille documents | Competent Authority, e-Apostille, e-Register, verification, replacement |
| Product Passports | Product identity, lifecycle evidence, compliance, repair, recycling |
| Health records | Consent, access policy, clinical evidence, privacy-preserving sharing |
| C2PA media evidence | Provenance manifest plus final-artifact integrity evidence |

The adapter makes OpenETR intelligible to people in the domain. It also keeps the OpenETR core from becoming overloaded with domain-specific rules.

## Policy Implications

Policymakers and institutions often face a hard choice between two bad options:

- mandate a single platform for a domain
- allow every platform to define its own closed evidence model

OpenETR offers a third path.

It can provide a shared control fabric while allowing domain systems to remain different.

That means:

- a registry can keep its own rulebook
- a carrier can keep its bill-of-lading workflow
- a warehouse can keep its receipt system
- a government authority can keep its official register
- a manufacturer can keep its product data system
- a verifier can apply its own recognition policy

The shared layer is not the business application. It is the signed evidence material that lets those applications interoperate more cleanly.

## The Practical Rule

The practical rule for OpenETR design is:

```text
Do not sew the whole wardrobe into the fabric.
Do not make every domain weave its own fabric.
```

OpenETR should remain a stable control substrate.

Domain adapters should remain domain-specific.

Recognition frameworks should remain explicit.

## Source Specifications

- [OpenETR Generic Domain Adapter Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [Controllable Records Taxonomy](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROLLABLE_RECORDS_TAXONOMY.md)
