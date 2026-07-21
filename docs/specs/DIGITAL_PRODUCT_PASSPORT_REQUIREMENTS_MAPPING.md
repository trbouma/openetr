# Product Passport Requirements Mapping

This document is a working recognition and effect traceability matrix for Digital Product Passport capabilities in OpenETR.

It is based on a project-oriented interpretation of Digital Product Passport requirements supplied for review. It is not a restatement of legislation and does not assert that OpenETR satisfies any EU Digital Product Passport obligation by itself.

The matrix is intentionally about **recognition and effect**. Those questions are technically outside the base OpenETR protocol, but they can be closely mapped to protocol evidence.

OpenETR should be treated as a signed evidence, digest identity, retrieval, and control-graph layer. It can show what was identified, signed, linked, retrieved, updated, attested, or queried. Product regulation, delegated acts, registry rules, access-control policy, market-surveillance practice, and relying-party decisions decide what legal, regulatory, or operational effect follows.

## Mapping Table

| Source area | Requirement group | Short summary | Project mapping / evidence |
| --- | --- | --- | --- |
| EU DPP system requirements | Product Identification | Every regulated product needs a globally unique, stable identifier that can be reached through a physical or electronic data carrier. | TBD |
| EU DPP system requirements | Digital Product Passport | Each regulated product needs a retrievable Digital Product Passport containing the information required for its product category. | TBD |
| EU DPP system requirements | Data Accessibility | Authorized parties need electronic access, role-sensitive access levels, public/restricted separation, and machine-to-machine access. | TBD |
| EU DPP system requirements | Lifecycle Support | Passport information must support lifecycle updates and preserve continuity through manufacture, sale, repair, refurbishment, remanufacture, and end-of-life. | TBD |
| EU DPP system requirements | Data Integrity | Passport information must be protected from unauthorized modification, verifiable against alteration, and traceable across updates. | TBD |
| EU DPP system requirements | Data Persistence | Passport information must remain available for the required retention period and not depend on a single market participant remaining active. | TBD |
| EU DPP system requirements | Interoperability | Systems need open interfaces, independent implementation interoperability, and standardized data formats. | TBD |
| EU DPP system requirements | Searchability | Authorized users must be able to locate passport information by product identifier, with automated discovery where required. | TBD |
| EU DPP system requirements | Information Management | Systems must distinguish mandatory and optional data, support structured machine-readable data, and allow updates without invalidating unrelated information. | TBD |
| EU DPP system requirements | Security | Systems must authenticate authorized modifiers, protect confidential information, and prevent unauthorized disclosure of restricted data. | TBD |
| EU DPP system requirements | Governance | Systems must record information sources, attribute information to responsible economic operators, and support regulatory inspection. | TBD |
| EU DPP system requirements | Auditability | Systems must maintain an audit trail of significant passport events that can reconstruct passport history. | TBD |
| DPP registry requirements | Registry Service | A registry should maintain unique registrations and enough metadata to locate and identify passports, without necessarily storing passport content. | TBD |
| DPP registry requirements | Passport Registration | Authorized economic operators must be able to register passports, while unauthorized or duplicate registrations are rejected. | TBD |
| DPP registry requirements | Passport Discovery | The registry must locate a passport from its unique identifier and return the current endpoint through automated, machine-readable lookup. | TBD |
| DPP registry requirements | Economic Operator Management | The registry must maintain authenticated economic operator identities, associate registrations with responsible operators, and track operator status. | TBD |
| DPP registry requirements | Authentication | Registry users and API clients must be authenticated through secure mechanisms. | TBD |
| DPP registry requirements | Authorization | Role-based authorization must support roles such as economic operator, competent authority, customs authority, Commission administrator, and national administrator. | TBD |
| DPP registry requirements | Access Control | The registry must separate public, restricted, and administrative information and enforce access to each class. | TBD |
| DPP registry requirements | API Services | Programmatic APIs must support registration, lookup, updates, validation, status queries, documentation, and interoperability with external DPP systems. | TBD |
| DPP registry requirements | Registry Metadata | Each registration must maintain metadata such as passport identifier, product identifier, economic operator, endpoint, status, and timestamps. | TBD |
| DPP registry requirements | Availability | The registry must provide appropriate continuous availability, fault recovery, and preservation across failures. | TBD |
| DPP registry requirements | Audit | The registry must record registrations, updates, authentication events, and administrative actions in tamper-evident records. | TBD |
| DPP registry requirements | Security | Registry data, communications, credentials, and monitoring must be protected against unauthorized access or modification. | TBD |
| DPP registry requirements | Data Quality | Submitted registration data must be validated, malformed registrations rejected, and inconsistencies detected. | TBD |
| DPP registry requirements | Administration | Authorized administrators must be able to approve, suspend, revoke, configure, and monitor, with administrative actions audited. | TBD |
| DPP registry requirements | Interoperability | The registry must interoperate with independent DPP providers, support standardized identifiers and interfaces, and avoid requiring registry-hosted passports. | TBD |
| DPP registry requirements | Data Persistence | Registry records and historical registration information must remain available for the required retention period. | TBD |
| DPP registry requirements | Compliance | The system must support competent-authority inspection, customs verification, and regulatory reporting. | TBD |
| DPP registry requirements | Error Handling | The system must return standardized errors, detect unavailable passport endpoints, and report invalid registrations. | TBD |

## Mapping Guidance

Use the final column to point to concrete project artifacts, not broad claims. Useful entries should name:

- the relevant OpenETR route, command, service, template, or event shape;
- the signed event evidence that is produced or queried;
- the OpenETR profile, role, or external party expected to sign or attest;
- the identifier, digest, endpoint, registry, or storage behavior being relied on;
- the access-control, validation, persistence, or recognition rule being applied;
- any remaining legal, delegated-act, registry, or institutional dependency.

Examples of useful evidence references may include:

- `/digital-product-passports`
- `/etr/{digest}`
- `/etr/{digest}/qr`
- `/warehouse-receipts/query`
- `openetr issue-etr`
- `openetr query-etr`
- `openetr/services/control_events.py`
- `openetr/services/query_etr.py`
- `app/templates/digital_product_passports.html`
- `app/templates/query_etr_result.html`
- `docs-site/product-passports.md`

## Review Notes

This table is intentionally not complete yet. The next step is to review each requirement group and decide whether OpenETR:

- already has usable implementation evidence;
- needs a Product Passport domain profile;
- needs a registry or discovery integration;
- needs access-control or role modeling;
- should treat the requirement as outside the base protocol and leave it to the recognition layer.
