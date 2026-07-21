# Product Passport Requirements Mapping

The Product Passport requirements mapping tracks how OpenETR evidence could be recognized under, or given effect by, Digital Product Passport requirements.

The mapping is intentionally about **recognition and effect**. Those questions are technically outside the base OpenETR protocol, but they are closely mapped to protocol evidence such as product artifact digests, signed control records, durable links, QR-code retrieval, original-record storage, attestations, and verifier policy output.

OpenETR can show what was identified, signed, linked, retrieved, updated, attested, or queried. Product regulation, delegated acts, registry rules, access-control policy, market-surveillance practice, marketplaces, and relying parties decide what legal, regulatory, or operational effect follows.

## How To Read The Mapping

The mapping distinguishes between:

| Category | Meaning |
| --- | --- |
| Protocol evidence | OpenETR provides digest identity, signed control records, retrieval, or verification evidence relevant to the requirement. |
| Supported by domain adapter | The Product Passports workspace can present DPP-specific language, fields, and workflows over the generic OpenETR model. |
| Registry / integration dependency | The requirement needs registry, discovery, API, identity, storage, or access-control integration outside the base control graph. |
| Recognition / compliance effect | OpenETR can provide evidence, but legal, regulatory, or operational effect depends on policy, delegated acts, authorities, or relying parties. |
| Gap / design note | More design work is needed before the requirement can be treated as supported. |

## Current Focus

The current strongest coverage is around:

- product passport artifact identity by digest;
- initial Product Passport control-record evidence;
- durable link and QR-code access to the control graph;
- optional retrieval of the original controlled object where storage is configured;
- basic domain metadata for product name, product id, manufacturer, batch or lot, and description;
- recognition-boundary documentation.

Some requirements need deeper product-domain policy or registry design. Those are intentionally tracked as gaps rather than hidden.

## Source Mapping

The working table is maintained in:

- [Digital Product Passport Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_PRODUCT_PASSPORT_REQUIREMENTS_MAPPING.md)

Related overview:

- [Product Passports Overview](product-passports.md)
