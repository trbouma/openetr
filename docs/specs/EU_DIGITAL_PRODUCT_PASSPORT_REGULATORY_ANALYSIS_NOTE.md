# EU Digital Product Passports And OpenETR Regulatory Analysis Note

This note reviews the European Union's emerging Digital Product Passport (DPP)
regime and analyzes where OpenETR can complement it.

The EU is not creating one universal product database or one identical passport
for every product. It is establishing a common horizontal architecture, then
using product-specific delegated acts and sector legislation to determine which
products require a DPP, what data it contains, whether it applies at model,
batch, or item level, who may access which data, and when the obligation takes
effect.

OpenETR does not replace that regime. It can provide an additional
artifact-centric evidence layer for identifying exact passport versions,
preserving signed lifecycle evidence, and deriving consequential state under
defined rules without making one application or DPP provider the exclusive
source of that state.

## Status

Draft regulatory analysis, current to 16 September 2026.

This note is an architectural and policy analysis, not legal advice. Economic
operators must evaluate the legislation and delegated acts applicable to their
products and roles.

## Executive Assessment

The EU DPP regime is moving from framework legislation into operational
infrastructure.

As of the date of this note:

- Regulation (EU) 2024/1781, the Ecodesign for Sustainable Products Regulation
  (ESPR), supplies the horizontal DPP framework.
- The EU DPP Registry became operational on 20 July 2026.
- Commission Implementing Regulation (EU) 2026/1778 defines registry operation,
  identity verification, registration, versioning, semantics, logging,
  retention, and responsibilities.
- Commission Implementing Decision (EU) 2026/1736 publishes references to six
  harmonized DPP standards.
- The first mandatory sector deadline is 18 February 2027 for specified
  batteries under Regulation (EU) 2023/1542.
- Product-specific requirements for iron and steel, textiles, tyres, aluminium,
  furniture, mattresses, and other priority groups are being introduced
  progressively.
- Separate Union legislation extends the DPP architecture to batteries,
  construction products, toys, detergents and end-user surfactants, and other
  regulated product classes.

The EU architecture has three important characteristics.

First, it is **federated rather than fully centralized**. The Commission's
Registry indexes passports, identifiers, metadata, status, semantic models, and
enforcement information. The detailed DPP data remains the responsibility of
the economic operator and may be hosted by that operator or a DPP service
provider.

Second, it separates **registration and structural verification from
substantive compliance**. The Registry can verify identity, syntax, semantic
conformity, granularity, required fields, identifiers, commodity codes, and
backup links. Those checks do not prove that the product complies with all
applicable law. Market surveillance authorities retain the substantive
compliance role.

Third, it requires **interoperability without vendor lock-in**. DPP data is to
use open standards and interoperable formats, with standardized identifiers,
data carriers, exchange protocols, storage, APIs, and lifecycle management.

OpenETR aligns strongly with those architectural choices, but only in a bounded
role:

```text
EU DPP regime:
  defines regulated content, actors, identifiers, access, registration,
  sector obligations, supervision, and legal effect

OpenETR:
  identifies exact DPP artifacts by digest, preserves end-verifiable
  lifecycle evidence, and derives protocol state under defined rules
```

The best fit is an independent evidence overlay, not a competing DPP registry
or alternative compliance system.

## Primary Sources

- [Regulation (EU) 2024/1781, the Ecodesign for Sustainable Products
  Regulation](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng)
- [Commission Implementing Regulation (EU) 2026/1778 on the DPP
  Registry](https://eur-lex.europa.eu/eli/reg_impl/2026/1778/oj)
- [Commission Implementing Decision (EU) 2026/1736 on harmonized DPP
  standards](https://eur-lex.europa.eu/eli/dec_impl/2026/1736/oj)
- [Ecodesign for Sustainable Products and Energy Labelling Working Plan
  2025-2030](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025DC0187)
- [Regulation (EU) 2023/1542 concerning batteries and waste
  batteries](https://eur-lex.europa.eu/eli/reg/2023/1542/oj)
- [Regulation (EU) 2024/3110 concerning construction
  products](https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng)
- [European Commission DPP implementation
  portal](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport_en)
- [European Commission DPP Registry
  overview](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport/dpp-registry_en)

## The Regulatory Structure

### The ESPR Is A Framework Regulation

The ESPR establishes the legal architecture for ecodesign requirements and
DPPs. It does not immediately require a DPP for every physical product.

Under Article 9, a product can be placed on the market or put into service only
with a DPP when an applicable delegated act adopted under the ESPR requires
one. The delegated act must specify the product group and the relevant DPP
requirements.

Those product-specific rules can determine:

- which data from Annex III must be included;
- the required data carrier and its placement;
- whether the passport is created at model, batch, or item level;
- how customers can access it before purchase, including distance sales;
- which actors may access which data;
- who may introduce or update information;
- the period for which the passport must remain available; and
- the relationship to other product information systems.

This means there is no single universal DPP content checklist. A compliant DPP
must satisfy the horizontal system requirements and the specific requirements
applicable to that product.

### Horizontal Requirements

Articles 10 and 11 of the ESPR establish essential DPP requirements. In
summary, a DPP must:

- connect a persistent unique product identifier to a data carrier;
- use a data carrier physically present on the product, packaging, or
  accompanying documentation, as specified by the applicable act;
- use applicable standards for identifiers and data carriers;
- use open standards and interoperable formats;
- be machine-readable, structured, searchable, and transferable where
  appropriate;
- operate through an open interoperable exchange network without vendor
  lock-in;
- apply at the required model, batch, or item level;
- enforce role-appropriate access rights;
- be interoperable technically, semantically, and organizationally;
- remain accessible free of charge to entitled actors;
- preserve authenticity, reliability, and integrity;
- meet security and privacy requirements;
- remain available for the required period, including after the responsible
  operator ceases activity; and
- have a backup copy available through a DPP service provider when placed on
  the market.

Customer personal data may not be stored in the DPP without explicit consent.
Commercial confidentiality, intellectual property, and differentiated access
remain important constraints.

### Annex III Data Categories

Annex III provides the menu from which product-specific delegated acts select
required data. It includes categories such as:

- product and passport identifiers;
- Global Trade Item Number or equivalent identifiers;
- commodity codes where relevant;
- compliance documentation;
- manuals, instructions, warnings, and safety information;
- manufacturer, importer, and responsible economic-operator information;
- unique operator and facility identifiers;
- information required by the relevant ecodesign rules; and
- references needed to make data accessible and interoperable.

The applicable delegated act, not Annex III alone, determines what is mandatory
for a particular product group.

## The EU DPP Registry

Article 13 of the ESPR requires a Commission-operated DPP Registry. The
Registry became operational on 20 July 2026, and Implementing Regulation (EU)
2026/1778 supplies its operating rules.

The Registry is not intended to hold all detailed product information. It acts
as a common EU index and enforcement layer while detailed passport data remains
decentralized.

Its components include:

- a secure user interface;
- a registration and query API;
- a verification platform;
- unique registration identifier generation;
- storage for identifiers and customs commodity codes;
- a list of verified DPP service providers;
- a semantic repository;
- an audit log system; and
- identification and authorization schemes for users.

### Verified Actors

Only verified economic operators can register DPPs. Verified value-chain
actors, such as repairers, refurbishers, remanufacturers, and recyclers, may
perform actions where the applicable legislation permits them.

The Registry regulation uses eIDAS mechanisms for identity evidence. Depending
on actor type and establishment, these can include:

- qualified electronic signatures;
- qualified electronic seals;
- high-assurance electronic identification; and
- electronic or qualified electronic attestations of attributes.

Verified status lasts only until the relevant identification means expires and
in any event no longer than three years without renewed verification.

This is an important boundary for OpenETR. An OpenETR signature proves control
of a protocol key. It does not replace the Registry's legal-person verification
or establish that the signer is an authorized economic operator.

### Registration

A DPP is registered at the model, batch, or item level required by the
applicable law. Where several Union rules apply at different levels, the
Registry requires registration at the most granular level.

Registration can occur through the Registry user interface or API. The
Registry performs automated checks for:

- semantic conformity;
- required data and structural coherence;
- the required granularity level;
- commodity-code validity where relevant; and
- the DPP service-provider backup link where relevant.

After successful verification, the Registry generates a unique persistent
registration identifier.

The verified economic operator remains responsible for the accuracy,
completeness, and currency of submitted information, even when a third party
performs registration activities on its behalf.

### Registration Is Not A Compliance Determination

Implementing Regulation 2026/1778 expressly separates automated Registry checks
from substantive compliance. Automated checks do not prove that the product
complies with all applicable Union rules. Market surveillance authorities
remain responsible for substantive assessment.

This resembles OpenETR's own proof boundary:

```text
Registry proof:
  the DPP was registered and passed specified registry checks

OpenETR proof:
  signed evidence concerning an exact artifact satisfies specified protocol rules

Neither proof alone:
  establishes every underlying product fact or compels legal recognition
```

### Proof Of Registration And Versioning

The Registry can issue a downloadable proof of registration. It includes:

- the unique product identifier;
- the commodity code where relevant;
- the verified economic operator;
- a Commission-timestamped registration date and time; and
- a hash of the DPP version covered by the proof.

The proof is protected by a qualified electronic seal and Commission time
stamp. The Registry also supports versioning and timestamps each update.

This is directly relevant to OpenETR. The EU architecture itself distinguishes:

- the persistent product identifier;
- the Registry's registration identifier;
- a specific version of the DPP; and
- the cryptographic hash of that version.

OpenETR can preserve and link those distinct identifiers without pretending
that any one of them replaces the others.

### Semantic Repository

The Registry regulation establishes an authoritative, machine-readable
semantic repository. It contains:

- product-group data models;
- semantic definitions and controlled vocabularies;
- attribute and role meanings;
- version and provenance metadata;
- multilingual labels;
- typed links among DPPs and underlying evidence; and
- publicly documented, free APIs.

OpenETR should consume these product-specific semantics through domain adapters.
It should not invent a competing universal DPP vocabulary.

## Harmonized Standards

Commission Implementing Decision (EU) 2026/1736 publishes references to six
harmonized standards:

| Standard | Subject |
| --- | --- |
| EN 18216:2026 | Data exchange protocols |
| EN 18219:2026 | Unique identifiers |
| EN 18220:2026 | Data carriers |
| EN 18221:2026 | Data storage, archiving, and persistence |
| EN 18222:2026 | APIs for lifecycle management and searchability |
| EN 18223:2026 | System interoperability |

Under Article 41(2) of the ESPR, conformity with cited harmonized standards or
the relevant parts of them supports a presumption of conformity with the
essential requirements those standards cover.

OpenETR interoperability work must therefore map to these standards rather
than merely claim that Nostr events or digest links are interoperable in the
regulatory sense.

The Commission's implementation timeline indicated that two additional DPP
standards were expected in September 2026. This note does not treat those
references as published until an Official Journal decision confirms them.

## Product Rollout

### ESPR Working Plan 2025-2030

The Commission's first ESPR working plan prioritizes product groups and gives
an indicative schedule for product-specific work:

| Indicative year | Product groups |
| --- | --- |
| 2026 | Iron and steel |
| 2026-2029 | Energy-related products |
| 2027 | Textiles, tyres, and aluminium |
| 2028 | Furniture |
| 2029 | Mattresses and ICT products |

These dates concern the development or adoption of product-specific measures,
not a single immediate compliance date for every operator. The Commission
states that ESPR delegated acts provide economic operators with a transition
period of at least 18 months.

### Batteries

The Batteries Regulation provides the first concrete mandatory DPP deadline.
From 18 February 2027, each of the following placed on the market or put into
service must have a battery passport:

- a light means of transport battery;
- an industrial battery with capacity greater than 2 kWh; and
- an electric vehicle battery.

The passport combines model-level and individual-battery information,
including information resulting from use. It applies differentiated access
for the public, authorities and notified bodies, and actors with a legitimate
interest such as repairers, remanufacturers, second-life operators, recyclers,
or parties acting for a purchaser.

The battery passport is therefore a particularly strong OpenETR pilot domain:
it has an item-specific lifecycle, changing operational data, differentiated
access, repair and repurposing evidence, and a near-term legal deadline.

### Construction Products

Regulation (EU) 2024/3110 requires a construction DPP system to be compatible
with and based on the ESPR DPP architecture while preserving interoperability
with Building Information Modelling.

The construction DPP can include declarations of performance and conformity,
technical documentation, instructions, safety information, labels, unique
identifiers, and documents required under other Union law. It also requires
access controls, update rights, availability, integrity, security, and privacy.

### Other Sector Legislation

Implementing Regulation 2026/1778 makes the Registry available for DPPs required
under:

- ESPR delegated acts;
- the Batteries Regulation;
- the Construction Products Regulation;
- Regulation (EU) 2025/2509 concerning toys;
- Regulation (EU) 2026/405 concerning detergents and end-user surfactants; and
- future Union legislation that requires a DPP and registration in the ESPR
  Registry.

The Commission's DPP portal also identifies packaging, critical raw materials,
and other product legislation as part of the broader DPP landscape. Each act
must be read on its own terms.

## The EU Architecture In Plain Language

The EU model can be summarized as follows:

```text
physical product, batch, or model
  -> persistent product identifier
  -> physical or electronic data carrier
  -> decentralized DPP data held by operator or service provider
  -> EU Registry entry and unique registration identifier
  -> role-based access for consumers, value-chain actors, and authorities
  -> market surveillance, customs, and sector-specific legal effect
```

The Registry is authoritative for registration and its own records. The
economic operator remains responsible for detailed DPP content. Competent
authorities remain responsible for enforcement. Product-specific law defines
the required facts and access rights.

## OpenETR's Potential Role

OpenETR can add an independently verifiable evidence path alongside the
regulated DPP architecture.

```text
DPP version or evidence artifact
  -> digest-identified Digital Artifact
  -> signed DCR evidence
  -> defined state transition rules
  -> independently reproducible Consequential State
```

This can help answer questions such as:

- Which exact DPP version was registered or relied upon?
- Which economic operator, repairer, auditor, or recycler signed a lifecycle
  statement?
- Which signed evidence superseded an earlier passport version?
- Was a recall, repair, remanufacturing, or end-of-life record linked to the
  correct product and passport version?
- What evidence produced the state displayed by an application?
- Can a verifier reconstruct that evidence if the original provider is no
  longer available?

### Product Identity Is Not Passport Identity

An integration must keep several identifiers separate:

| Identifier | Function |
| --- | --- |
| Product identifier | Identifies the regulated model, batch, or item |
| DPP Registry identifier | Identifies the Registry registration |
| DPP endpoint | Locates current passport data |
| DPP version hash | Identifies the exact passport content version |
| OpenETR event id | Identifies a signed evidence record |
| OpenETR signer key | Identifies the cryptographic signer |

OpenETR's artifact digest should normally identify an immutable DPP version or
supporting evidence artifact. It should not be used as a substitute for the
persistent product identifier.

### A Dynamic DPP Is Not One Immutable File

Many DPP implementations will expose a changing dataset or API response rather
than one permanent file. OpenETR therefore needs a canonicalization and
versioning rule.

A robust profile should:

1. define the canonical serialization of a DPP snapshot;
2. compute a digest over that exact snapshot;
3. preserve the applicable schema and semantic-repository version;
4. bind the snapshot to the product and Registry identifiers;
5. link successor snapshots without erasing prior evidence; and
6. distinguish correction, supplementation, supersession, and status change.

Without canonicalization, two systems may serialize equivalent data
differently and produce different digests. Without version semantics, a digest
can prove content integrity but not which version is current.

### DPP Content And The DCR Are Different Graphs

A DPP may contain a rich product graph: components, materials, suppliers,
certificates, carbon data, repair information, and links to other passports.

An OpenETR DCR is a graph of end-verifiable evidence concerning a
digest-identified Digital Artifact. It should include or link the records that
matter for the artifact's consequential state under an applicable profile.

The product graph and the DCR may overlap, but they are not identical:

```text
DPP product graph:
  what is known or asserted about the product and its lifecycle

OpenETR DCR:
  which signed evidence concerns an exact DPP artifact,
  and what state follows under defined rules
```

OpenETR can act as a consequential-state subgraph within the broader DPP
evidence environment.

## Regulatory Mapping

| EU requirement or function | OpenETR contribution | Boundary |
| --- | --- | --- |
| Persistent product identifier | Signed linkage between identifier and exact artifact digest | OpenETR does not issue or govern the regulated identifier |
| Model, batch, or item granularity | Records the asserted granularity and parent identifiers | Applicable law and Registry determine valid granularity |
| Data carrier | Can bind QR or resolver evidence to a digest | Must conform to applicable standards and delegated act |
| Open, interoperable exchange | Portable signed events and independent verification | Regulatory interoperability requires the EN standards and DPP profiles |
| Accurate, complete, current data | Preserves signed version and update evidence | Economic operator remains legally responsible |
| Integrity and authenticity | Digest and signature verification | Signatures do not prove underlying product claims are true |
| Lifecycle updates | Linked evidence and explicit successor relationships | Product-specific rules determine who may update what |
| Access rights | Public commitments and integrity checks for disclosed data | OpenETR public relays are not a confidential-data access-control system |
| Registry registration | Links Registry identifier and sealed proof to passport version | OpenETR cannot replace mandatory Registry registration |
| Proof of registration | Preserves the sealed proof and version hash as linked evidence | Proof confirms registration, not substantive product compliance |
| Semantic conformity | Links the snapshot to schema and vocabulary versions | Registry and semantic repository define official semantics |
| Availability and persistence | Relay and storage replication can reduce dependence on one provider | Regulatory retention and availability require managed services and governance |
| Auditability | Signed event history and evidence graph | Completeness depends on required-event rules and operational capture |
| Market surveillance | Reconstructable evidence package | Authorities decide compliance and enforcement |

## Consequential State For A Product Passport

OpenETR should be careful not to turn every DPP claim into protocol state.

Possible protocol states might include:

- the currently referenced passport version;
- whether a version has been superseded;
- whether a signed recall, withdrawal, repair, or end-of-life notice is linked;
- which recognized profile issued a particular lifecycle statement;
- whether required linked evidence is present under a selected profile; and
- whether the passport evidence graph is complete enough for a particular
  verifier policy.

OpenETR should not assert that a product is legally compliant merely because:

- a DPP exists;
- the DPP was registered;
- its content hash matches;
- a signer is known; or
- the graph is structurally valid.

Substantive product compliance remains a recognition and enforcement decision.

## Recommended Event Treatment

Not every DPP lifecycle action should be a control-state transition.

| DPP occurrence | Suggested OpenETR treatment |
| --- | --- |
| Initial canonical DPP version | Anchor Record or linked-artifact evidence |
| EU Registry proof | Linked evidence |
| Corrected or superseding DPP version | Explicit successor or supersession record |
| Repair or maintenance record | Linked evidence, unless profile defines a state transition |
| Conformity certificate | Linked attestation evidence |
| Recall or withdrawal notice | Consequential record under a domain profile |
| Remanufacture or repurpose event | Linked evidence plus state transition where rules require it |
| Recycling or end-of-life evidence | Linked evidence and possible terminal state |
| Change in responsible operator | Registry-linked transition evidence; legal effect remains external |

The Product Passport domain adapter should define these mappings explicitly.

## Privacy And Confidentiality

The EU regime uses differentiated access. Some data is public, some is limited
to authorities, and some is available only to actors with a legitimate
interest.

OpenETR must not publish restricted DPP data to public relays by default.

Preferred patterns include:

- public digests and non-sensitive metadata;
- commitments to restricted evidence;
- encrypted or controlled storage;
- role-authorized retrieval outside the public graph;
- selective disclosure where supported;
- signed disclosure receipts; and
- verifier results that distinguish missing access from invalid evidence.

The aim is independent verification of permitted claims, not universal public
disclosure.

## Dependency And Continuity

The ESPR explicitly rejects vendor lock-in and requires passport availability
even after an operator ceases activity. It also requires a backup copy through
a DPP service provider.

OpenETR can contribute to continuity by preserving:

- exact passport-version digests;
- signed actor statements;
- Registry proofs and timestamps;
- successor and supersession relationships;
- storage and resolver references; and
- exportable evidence graphs.

This does not remove every dependency. Verifiers may still depend on:

- the EU Registry;
- the Commission semantic repository;
- recognized economic-operator identity;
- DPP service providers;
- issuer and credential status systems;
- controlled storage for restricted data; and
- competent-authority decisions.

The design goal should be to make each dependency explicit and to preserve
enough evidence that failure of one application does not erase the record's
history.

## Recommended OpenETR Work

### 1. Update The Product Passport Profile

Define a profile covering:

- product, Registry, endpoint, artifact, and event identifiers;
- model, batch, and item granularity;
- canonical DPP snapshot serialization;
- semantic model and schema versions;
- version succession and correction;
- recognized actor roles;
- public, restricted, and committed evidence;
- retention and resolver expectations; and
- state derivation rules.

### 2. Add Registry Integration

Support capture and verification of:

- Registry registration identifiers;
- sealed proofs of registration;
- Commission timestamps;
- DPP version hashes;
- Registry status and operator identity evidence; and
- semantic-repository references.

### 3. Build Against The Harmonized Standards

Map OpenETR functions to EN 18216, EN 18219, EN 18220, EN 18221, EN 18222,
and EN 18223. Record where OpenETR conforms, where an adapter is required, and
where the function remains external.

### 4. Pilot Batteries First

Use the 18 February 2027 battery deadline as the primary implementation target.
Test:

- item-level product identity;
- canonical passport snapshots;
- Registry enrollment and proof capture;
- public and restricted data separation;
- repair, repurposing, and recycling evidence;
- signer and economic-operator identity binding;
- supersession and end-of-life transitions; and
- continuity after a provider or endpoint change.

### 5. Preserve The Recognition Boundary

Every verifier result should distinguish:

```text
content integrity
signer attribution
DCR validity
derived protocol state
Registry status
semantic conformity
substantive regulatory compliance
recognition and effect
```

No single green check should collapse these claims.

## Policy Implications

The EU DPP programme is not merely a labeling initiative. It is creating shared
digital infrastructure for product identity, lifecycle information, market
access, customs, surveillance, repair, reuse, and circularity.

Its long-term legitimacy will depend on several policy choices:

1. **Interoperability must remain practical.** Open standards and APIs must
   prevent nominal interoperability from becoming provider dependence.
2. **Registration must not be confused with compliance.** Structural checks
   and sealed proofs should state exactly what they establish.
3. **Economic operators must remain accountable for claims.** Outsourcing to a
   DPP service provider should not outsource responsibility.
4. **Evidence should survive systems.** Passport history should remain
   intelligible when operators, providers, endpoints, or software change.
5. **Access should be graduated.** Public transparency should not expose trade
   secrets, personal data, or security-sensitive information.
6. **Lifecycle claims need attribution.** Repairers, recyclers, auditors, and
   authorities should be able to make attributable statements without silently
   rewriting earlier evidence.
7. **Authorities need reconstructable evidence.** Market surveillance should
   be able to see why a displayed status follows, not only the status itself.

OpenETR can support these goals by making the evidence behind consequential DPP
states portable and independently verifiable.

## Bottom Line

The EU is building a regulated DPP ecosystem with:

- product-specific legal obligations;
- standardized identifiers and data carriers;
- decentralized passport data;
- a central EU Registry and semantic repository;
- verified economic operators and value-chain actors;
- differentiated access;
- lifecycle versioning and audit; and
- customs and market-surveillance enforcement.

OpenETR should not compete with those functions.

Its role is to help an exact DPP version or supporting record become a Digital
Artifact with a durable DCR, so that defined rules can derive consequential
state from end-verifiable evidence rather than relying only on the application
currently displaying the passport.

The EU regime determines what information is required, who is responsible,
which registrations and standards apply, and what regulatory effect follows.
OpenETR can help the evidence remain understandable and verifiable across the
systems that implement those obligations.

## Policy Brief

- [EU Digital Product Passports And
  OpenETR](https://trbouma.github.io/openetr/policy-briefs/eu-digital-product-passports-and-openetr/)

## Related OpenETR Materials

- [Product Passport Requirements Mapping](./DIGITAL_PRODUCT_PASSPORT_REQUIREMENTS_MAPPING.md)
- [OpenETR Generic Domain Adapter Specification](./OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [Digital Controllable Record Design Note](./DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
- [Linked Evidence Record Kind Design Note](./LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md)
- [OpenETR Dependency Integrity Design Note](./OPENETR_DEPENDENCY_INTEGRITY_DESIGN_NOTE.md)
- [OpenETR Organizational Reference Layer Design Note](./OPENETR_ORGANIZATIONAL_REFERENCE_LAYER_DESIGN_NOTE.md)
