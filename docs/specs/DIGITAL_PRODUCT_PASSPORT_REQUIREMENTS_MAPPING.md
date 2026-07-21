# Product Passport Requirements Mapping

This document is a working recognition and effect traceability matrix for Digital Product Passport capabilities in OpenETR.

It is based on a project-oriented interpretation of Digital Product Passport requirements supplied for review. It is not a restatement of legislation and does not assert that OpenETR satisfies any EU Digital Product Passport obligation by itself.

The matrix is intentionally about **recognition and effect**. Those questions are technically outside the base OpenETR protocol, but they can be closely mapped to protocol evidence.

OpenETR should be treated as a signed evidence, digest identity, retrieval, and control-graph layer. It can show what was identified, signed, linked, retrieved, updated, attested, or queried. Product regulation, delegated acts, registry rules, access-control policy, market-surveillance practice, and relying-party decisions decide what legal, regulatory, or operational effect follows.

## Mapping Table

| ID | Source area | Requirement group | Short summary | Project mapping / evidence |
| --- | --- | --- | --- | --- |
| DPP-SYS-01 | EU DPP system requirements | Product Identification | Every regulated product needs a globally unique, stable identifier that can be reached through a physical or electronic data carrier. | Outside the base OpenETR protocol. Product identifier assignment, uniqueness, lifecycle stability, and data-carrier attachment are the responsibility of the organization or economic operator that issues the Product Passport, subject to the applicable product rules. OpenETR can preserve evidence that an issuer asserted a `product_id` or related identifier in the Product Passport control record, and can link that assertion to the passport artifact digest, QR code, durable URL, and control graph. Recognition depends on whether the issuer and identifier scheme are accepted by the relevant registry, authority, marketplace, or relying party. |
| DPP-SYS-02 | EU DPP system requirements | Digital Product Passport | Each regulated product needs a retrievable Digital Product Passport containing the information required for its product category. | Partially supported as protocol evidence. The original Product Passport record, such as a PDF, image, JSON document, data bundle, credential, or registry export, is treated as the Controlled Object. Its bytes produce the digest that identifies the passport artifact in OpenETR. Issuing the passport through the Product Passports workspace creates a corresponding signed origin control record for that digest, with optional domain metadata such as `product_id`, `product_name`, `manufacturer`, `batch_or_lot`, and `record_description`. OpenETR can also retrieve and render the original controlled record when configured storage contains the matching digest. The completeness of passport content required by a delegated act remains outside the base protocol and must be handled by the issuer, schema, registry, authority, or verifier policy. |
| DPP-SYS-03 | EU DPP system requirements | Data Accessibility | Authorized parties need electronic access, role-sensitive access levels, public/restricted separation, and machine-to-machine access. | Supported as profile-scoped protocol evidence, with access-policy limits outside the base protocol. In an OpenETR Product Passport profile, the authorized party is the organization that controls the recognized profile control key for that passport issuer. Only Product Passport control records issued by that organization profile should be recognized as authoritative for that issuer's passport. OpenETR can expose the signed control graph electronically and support machine-readable retrieval by digest or durable URL, but it does not itself decide public versus restricted passport content. Public/restricted access levels, API authorization, and confidential data disclosure rules must be enforced by the issuing organization, storage service, registry, or verifier policy. |
| DPP-SYS-04 | EU DPP system requirements | Lifecycle Support | Passport information must support lifecycle updates and preserve continuity through manufacture, sale, repair, refurbishment, remanufacture, and end-of-life. | Supported as linked evidence around the Product Passport graph, with lifecycle semantics defined by a Product Passport profile. The original Product Passport record can remain the primary Controlled Object, while later original records, such as repair reports, refurbishment certificates, remanufacturing records, resale attestations, recall notices, recycling records, or end-of-life documents, can be associated through signed linked evidence records. Those records can point to their own digests and back to the original passport digest, preserving continuity across lifecycle events without rewriting the original passport artifact or treating every lifecycle update as a transfer of control. Recognition depends on whether the issuer profile, evidence type, linked document class, and lifecycle rule are accepted by the relevant delegated act, registry, authority, marketplace, or verifier policy. |
| DPP-SYS-05 | EU DPP system requirements | Data Integrity | Passport information must be protected from unauthorized modification, verifiable against alteration, and traceable across updates. | Strongly supported as protocol evidence. OpenETR identifies the Product Passport artifact by digest, so any change to the original record produces a different object identity. Origin, control, and future linked evidence records are signed by OpenETR profile keys, giving verifiers cryptographic evidence of who asserted each record and whether the event signature is valid. Updates can be represented as additional signed records linked to the passport digest or to prior events, making the update path traceable without silently modifying earlier records. OpenETR does not prevent an external storage system from changing its own content, but digest verification reveals whether retrieved content still matches the recorded artifact. Recognition depends on accepted profile keys, verifier policy, storage integrity, and any domain-specific rule for whether an update is valid, superseding, or merely supporting evidence. |
| DPP-SYS-06 | EU DPP system requirements | Data Persistence | Passport information must remain available for the required retention period and not depend on a single market participant remaining active. | TBD |
| DPP-SYS-07 | EU DPP system requirements | Interoperability | Systems need open interfaces, independent implementation interoperability, and standardized data formats. | TBD |
| DPP-SYS-08 | EU DPP system requirements | Searchability | Authorized users must be able to locate passport information by product identifier, with automated discovery where required. | TBD |
| DPP-SYS-09 | EU DPP system requirements | Information Management | Systems must distinguish mandatory and optional data, support structured machine-readable data, and allow updates without invalidating unrelated information. | TBD |
| DPP-SYS-10 | EU DPP system requirements | Security | Systems must authenticate authorized modifiers, protect confidential information, and prevent unauthorized disclosure of restricted data. | TBD |
| DPP-SYS-11 | EU DPP system requirements | Governance | Systems must record information sources, attribute information to responsible economic operators, and support regulatory inspection. | TBD |
| DPP-SYS-12 | EU DPP system requirements | Auditability | Systems must maintain an audit trail of significant passport events that can reconstruct passport history. | TBD |
| DPP-REG-01 | DPP registry requirements | Registry Service | A registry should maintain unique registrations and enough metadata to locate and identify passports, without necessarily storing passport content. | TBD |
| DPP-REG-02 | DPP registry requirements | Passport Registration | Authorized economic operators must be able to register passports, while unauthorized or duplicate registrations are rejected. | TBD |
| DPP-REG-03 | DPP registry requirements | Passport Discovery | The registry must locate a passport from its unique identifier and return the current endpoint through automated, machine-readable lookup. | TBD |
| DPP-REG-04 | DPP registry requirements | Economic Operator Management | The registry must maintain authenticated economic operator identities, associate registrations with responsible operators, and track operator status. | TBD |
| DPP-REG-05 | DPP registry requirements | Authentication | Registry users and API clients must be authenticated through secure mechanisms. | TBD |
| DPP-REG-06 | DPP registry requirements | Authorization | Role-based authorization must support roles such as economic operator, competent authority, customs authority, Commission administrator, and national administrator. | TBD |
| DPP-REG-07 | DPP registry requirements | Access Control | The registry must separate public, restricted, and administrative information and enforce access to each class. | TBD |
| DPP-REG-08 | DPP registry requirements | API Services | Programmatic APIs must support registration, lookup, updates, validation, status queries, documentation, and interoperability with external DPP systems. | TBD |
| DPP-REG-09 | DPP registry requirements | Registry Metadata | Each registration must maintain metadata such as passport identifier, product identifier, economic operator, endpoint, status, and timestamps. | TBD |
| DPP-REG-10 | DPP registry requirements | Availability | The registry must provide appropriate continuous availability, fault recovery, and preservation across failures. | TBD |
| DPP-REG-11 | DPP registry requirements | Audit | The registry must record registrations, updates, authentication events, and administrative actions in tamper-evident records. | TBD |
| DPP-REG-12 | DPP registry requirements | Security | Registry data, communications, credentials, and monitoring must be protected against unauthorized access or modification. | TBD |
| DPP-REG-13 | DPP registry requirements | Data Quality | Submitted registration data must be validated, malformed registrations rejected, and inconsistencies detected. | TBD |
| DPP-REG-14 | DPP registry requirements | Administration | Authorized administrators must be able to approve, suspend, revoke, configure, and monitor, with administrative actions audited. | TBD |
| DPP-REG-15 | DPP registry requirements | Interoperability | The registry must interoperate with independent DPP providers, support standardized identifiers and interfaces, and avoid requiring registry-hosted passports. | TBD |
| DPP-REG-16 | DPP registry requirements | Data Persistence | Registry records and historical registration information must remain available for the required retention period. | TBD |
| DPP-REG-17 | DPP registry requirements | Compliance | The system must support competent-authority inspection, customs verification, and regulatory reporting. | TBD |
| DPP-REG-18 | DPP registry requirements | Error Handling | The system must return standardized errors, detect unavailable passport endpoints, and report invalid registrations. | TBD |

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
- `docs/specs/LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md`

## Review Notes

This table is intentionally not complete yet. The next step is to review each requirement group and decide whether OpenETR:

- already has usable implementation evidence;
- needs a Product Passport domain profile;
- needs a registry or discovery integration;
- needs access-control or role modeling;
- should treat the requirement as outside the base protocol and leave it to the recognition layer.
