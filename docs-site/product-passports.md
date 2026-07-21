# Product Passports

The **Product Passports** workspace is a domain adapter over the general OpenETR control layer.

It is for product data artifacts, compliance evidence, manufacturing metadata, lifecycle attestations, and related product records. It is not about personal identity passports.

## What A Product Passport Is In OpenETR

In this domain:

- the Product Passport file or data artifact is the **Controlled Object**;
- the Product Passport digest is the stable object identity;
- each signed OpenETR origin or control event is a **control record** for that Product Passport;
- the linked set of control records is the Product Passport **control graph**.

The Product Passport itself may be a PDF, image, JSON document, data bundle, credential, registry export, or another canonical artifact. OpenETR does not need to parse it before it can identify the artifact by digest and record control-relevant evidence.

## Requirements Mapping

A working Digital Product Passport requirements overview is available at [Product Passport Requirements Mapping](product-passport-requirements.md).

The mapping is intentionally incomplete so each requirement can be reviewed before project evidence, gaps, and recognition-boundary notes are filled in.

## Current App Surface

The live Product Passports workspace is:

[`https://openetr.org/digital-product-passports`](https://openetr.org/digital-product-passports)

The current page supports two starting workflows.

| Workflow | Purpose |
| --- | --- |
| Query Product Passport Control | Upload a Product Passport file and query the OpenETR control graph associated with its digest. |
| Create Product Passport Control Record | Publish the initial OpenETR control record for a Product Passport document using the selected profile signer. |

## Product Passport Metadata

The first Product Passport control-record flow can carry basic signed metadata:

| Field | OpenETR Tag |
| --- | --- |
| Product name | `product_name` |
| Product id | `product_id` and `record_reference` |
| Manufacturer or issuer | `manufacturer` |
| Batch or lot | `batch_or_lot` |
| Description | `record_description` |
| Domain | `domain=digital_product_passport` |
| Document type | `document_type=product_passport` |

These tags are early domain-adapter metadata. They make the control record easier to inspect without turning OpenETR into a complete Product Passport schema or compliance engine.

## Likely Future Control Records

Product Passport workflows will likely need domain-specific profiles and verifier policies for:

- manufacturer or importer attestations;
- material provenance;
- repair, refurbishment, and resale history;
- sustainability and compliance claims;
- recall, restriction, or safety notices;
- recycling, recovery, or end-of-life events;
- registry, auditor, or marketplace recognition.

OpenETR can provide the signed graph and digest linkage. Domain policy decides which claims are trusted, which actors are recognized, and what legal or operational effect follows.

## Relationship To Warehouse Receipts

Product Passports and Warehouse Receipts should use the same underlying OpenETR vocabulary:

| Shared OpenETR Concept | Warehouse Receipts | Product Passports |
| --- | --- | --- |
| Controlled Object | Receipt document | Product Passport artifact |
| Origin control record | Initial receipt control evidence | Initial Product Passport control evidence |
| Control graph | Receipt control history | Product Passport control history |
| Recognition layer | MLWR law, registry rules, warehouse policy | Product regulation, compliance policy, registry rules, marketplace policy |

This is the domain-adapter pattern: each workspace speaks its own language, but the signed control layer stays general.
