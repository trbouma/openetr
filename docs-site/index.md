# OpenETR

Many important records are becoming digital, but the institutions around them still need something that paper used to provide almost by accident: a way to distinguish the operative record from a copy, a way to know who can act on it, and a way to preserve evidence of what happened to it over time.

That problem appears in many domains:

- a warehouse receipt may support financing against stored goods
- a bill of lading may control rights to goods in transit
- a promissory note or bill of exchange may be transferred or discharged
- a product passport may depend on lifecycle and compliance evidence
- an apostille or certificate may need durable authority evidence
- a health record may need continuity, consent, and trustworthy provenance

Digital records are easy to copy. That is useful for sharing information, but it creates a problem when a record's value depends on control, presentation, transfer, pledge, release, redemption, or recognition by another party.

Many systems solve this by making one platform, registry, wallet, or database the source of truth. That can work inside one environment. It becomes harder when records need to move across organizations, legal frameworks, industries, financing arrangements, archives, and software systems.

**OpenETR** is a general control layer for durable electronic records.

<figure class="openetr-home-figure">
  <img src="assets/images/global-relay-race-zach-lucero-unsplash.jpg" alt="Runner carrying a relay baton on a track field">
  <figcaption>
    OpenETR is intended to be part of a global relay race: each system can carry the record forward while preserving signed evidence of the handoff.
    Photo by <a href="https://unsplash.com/@zlucerophoto?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Zach Lucero</a> on <a href="https://unsplash.com/photos/woman-running-on-field-x_x3RPpDbII?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>.
  </figcaption>
</figure>

It identifies a document, file, or data artifact by cryptographic digest.
Signed Anchor, Control, and linked-evidence events concerning that Digital
Artifact form a candidate **Digital Controllable Record (DCR)**. OpenETR
validates that evidence and derives consequential state; domain-specific
workflows decide how to interpret and recognize it.

OpenETR does not try to become every domain's registry, legal authority, KYC system, wallet, storage service, or compliance engine. It preserves portable signed evidence that those systems can evaluate.

The basic idea is:

```text
record or artifact
  -> digest-identified Digital Artifact
  -> Digital Controllable Record made of candidate events
  -> valid DCR and protocol rules
  -> consequential state and Digital Original
  -> domain adapter interprets the graph
  -> recognition layer decides effect
```

This is why OpenETR is described as a control layer. It records durable evidence about the lifecycle of an object without pretending that cryptography alone decides legal or commercial effect.

## Start Here

| Area | Purpose |
| --- | --- |
| [OpenETR Overview](openetr/index.md) | Learn the general control model, wire format, implementation surfaces, and recognition boundary. |
| [Warehouse Receipts](getting-started.md) | Work with warehouse receipt documents using MLWR-style terminology over the OpenETR control layer. |
| [Product Passports](product-passports.md) | Start modelling Product Passport control records for product data, compliance evidence, and lifecycle attestations. |
| [Health Records](health-records.md) | Placeholder for future health-record control graph workflows, with privacy and consent concerns called out early. |
| [Apostille Documents](apostille-documents.md) | Placeholder for future apostille and legalization document verification workflows. |

## Live App

| Page | Purpose |
| --- | --- |
| [`https://openetr.org/`](https://openetr.org/) | OpenETR Control Desk app with query-only upload flow |
| [`https://openetr.org/warehouse-receipts`](https://openetr.org/warehouse-receipts) | Warehouse Receipts workspace |
| [`https://openetr.org/digital-product-passports`](https://openetr.org/digital-product-passports) | Product Passports workspace |
| [`https://openetr.org/openetr`](https://openetr.org/openetr) | Advanced OpenETR console |
| [`https://openetr.org/docs`](https://openetr.org/docs) | FastAPI-generated API docs |

## Core Vocabulary

| Term | Meaning |
| --- | --- |
| Digital Artifact | Persistent content, such as a document or data artifact, identified by digest. |
| Digital Controllable Record | One end-verifiable record or a graph of related records concerning a Digital Artifact. |
| Control Record | A signed OpenETR origin or control event within a DCR. |
| Linked Evidence Record | A signed record that associates another document, artifact, or evidence item with a Digital Artifact without necessarily transferring control. |
| Control Graph | The linked control-event portion of a DCR. |
| Evidence Graph | The broader DCR graph, including origin, control, and linked-evidence records. |
| Domain Workspace | A user-facing adapter that speaks domain language while using the same OpenETR control layer underneath. |
| Recognition Layer | Law, registry policy, institutional rules, verifier policy, or contracts that decide legal or operational effect. |

## Core Thesis

OpenETR does not try to become each domain's system of record, registry, legal authority, or compliance engine.

Instead, it provides a thin signed control layer that produces durable evidence:

```text
real-world object, product, document, or record
  -> canonical file or data artifact
  -> SHA-256 digest
  -> signed OpenETR origin control record
  -> signed control records and linked evidence records
  -> durable query link and QR code
  -> verifier / registry / authority / relying party decides effect
```

The object content can stay with the operator, manufacturer, registry, platform, or storage service. OpenETR records the cryptographic object identity and the signed evidence graph.

OpenETR does not decide effect. It preserves durable signed evidence that a recognition layer can evaluate.

## Documentation Tracks

| Track | Audience | Starting Point |
| --- | --- | --- |
| OpenETR | Implementers, protocol reviewers, system integrators | [OpenETR Overview](openetr/index.md) |
| Warehouse Receipts | Warehouse operators, MLWR reviewers, domain integrators | [Warehouse Receipts Overview](getting-started.md) |
| Product Passports | Product, compliance, lifecycle, and supply-chain integrators | [Product Passports Overview](product-passports.md) |
| Health Records | Health data, consent, privacy, and clinical workflow integrators | [Health Records Overview](health-records.md) |
| Apostille Documents | Notarial, legalization, authority, and document verification integrators | [Apostille Documents Overview](apostille-documents.md) |

## Source Specifications

Key source documents:

- [GitHub repository](https://github.com/trbouma/openetr)
- [Specification index](https://github.com/trbouma/openetr/blob/main/docs/specs/INDEX.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OpenETR Nostr Wire Format](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [OpenETR MLWR Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_MLWR_PROFILE.md)
- [MLWR Article Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_ARTICLE_REQUIREMENTS_MAPPING.md)
- [Digital Product Passport Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_PRODUCT_PASSPORT_REQUIREMENTS_MAPPING.md)
