# OpenETR

**OpenETR** is a general control layer for durable electronic records.

It treats a document, file, or product data artifact as a **Controlled Object** identified by digest. Signed OpenETR origin records, control records, and linked evidence records for that digest form a control and evidence graph that can be queried, verified, and interpreted by domain-specific workflows.

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
| Controlled Object | The document, file, Product Passport artifact, warehouse receipt, or other record identified by digest. |
| Control Record | A signed OpenETR origin or control event about a Controlled Object. |
| Linked Evidence Record | A signed record that associates another document, artifact, or evidence item with a Controlled Object without necessarily transferring control. |
| Control Graph | The linked set of origin records and control records for one Controlled Object. |
| Evidence Graph | The broader linked set of origin records, control records, and linked evidence records for one Controlled Object. |
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
