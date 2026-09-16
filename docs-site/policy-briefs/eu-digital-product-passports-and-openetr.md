# EU Digital Product Passports And OpenETR

The European Union is turning product information into shared digital
infrastructure.

Digital Product Passports will connect products, components, and materials to
structured information about identity, sustainability, conformity, repair,
reuse, recycling, and other lifecycle concerns. Consumers, businesses,
repairers, recyclers, customs officials, and market-surveillance authorities
will see different information according to their roles.

OpenETR can complement this programme by making the evidence behind important
passport states independently verifiable across applications and providers.

This brief reflects the EU legal and implementation position reviewed on 16
September 2026.

## The EU Is Building A Regulatory System

The Digital Product Passport is not simply a QR code or a product webpage.

The [Ecodesign for Sustainable Products Regulation, Regulation (EU)
2024/1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj/eng), establishes a
horizontal DPP framework. Product-specific delegated acts then determine which
products require a passport, what information must be included, whether the
passport applies at model, batch, or item level, and who may access or update
the data.

Separate legislation also applies the DPP model to sectors such as batteries,
construction products, toys, and detergents.

The EU framework requires DPPs to use persistent identifiers, data carriers,
open standards, interoperable formats, machine-readable data, differentiated
access, security, privacy, and lifecycle availability without vendor lock-in.

It is therefore better understood as a regulated product-information ecosystem
than as a document format.

## A Central Registry With Decentralized Data

The EU's architecture deliberately combines central and decentralized
elements.

The [EU DPP Registry became operational on 20 July
2026](https://single-market-economy.ec.europa.eu/news/digital-product-passport-registry-now-live-2026-07-20_en).
It stores identifiers, registration data, selected metadata, semantic models,
status, and information needed for customs and enforcement.

The detailed passport data remains under the responsibility of the economic
operator. It may be hosted by the operator or a DPP service provider.

```text
EU Registry:
  identity, registration, indexing, semantics, status, enforcement

Economic operator or DPP provider:
  detailed passport data and lifecycle availability
```

This design avoids one giant product database, but it creates a need for strong
links among identifiers, passport versions, operators, providers, and evidence.

## Registration Is Not Compliance

[Commission Implementing Regulation (EU)
2026/1778](https://eur-lex.europa.eu/eli/reg_impl/2026/1778/oj) defines the
Registry's operation.

The Registry can verify actor identity, required structure, semantic
conformity, granularity, identifiers, commodity codes, and service-provider
backup links. It can then issue a sealed proof of registration containing the
verified economic operator, a Commission timestamp, and a hash of the relevant
DPP version.

Those checks are important, but the Regulation makes a careful distinction:
automated Registry verification is not proof that the product complies with
every applicable rule. Substantive compliance remains a matter for economic
operators and market-surveillance authorities.

That distinction should be preserved in every DPP interface.

```text
registered does not necessarily mean compliant
signed does not necessarily mean true
available does not necessarily mean current
current does not necessarily mean recognized for every purpose
```

Each proof proves only what it proves.

## The Rollout Has Begun

The first mandatory deadline is close. Under the [Batteries
Regulation](https://eur-lex.europa.eu/eli/reg/2023/1542/oj), specified electric
vehicle, light-means-of-transport, and industrial batteries placed on the
market or put into service must have battery passports from 18 February 2027.

The EU's 2025-2030 working plan identifies an indicative sequence for further
product measures:

| Period | Priority areas |
| --- | --- |
| 2026 | Iron and steel |
| 2026-2029 | Energy-related products |
| 2027 | Textiles, tyres, and aluminium |
| 2028 | Furniture |
| 2029 | Mattresses and ICT products |

The exact obligation and compliance date for each product depends on the
applicable delegated act or sector legislation. ESPR delegated acts provide at
least an 18-month transition period for economic operators.

## Standards Now Matter

In July 2026, the Commission published references to six harmonized DPP
standards covering:

- data exchange protocols;
- unique identifiers;
- data carriers;
- data storage, archiving, and persistence;
- lifecycle-management and search APIs; and
- system interoperability.

These standards matter because conformity with the cited standards can support
a presumption of conformity with the ESPR requirements they cover.

A DPP project should not claim regulatory interoperability merely because it
has a REST API, a QR code, a blockchain entry, or a signed JSON document. It
must map its implementation to the applicable legal requirements and
harmonized standards.

## Where OpenETR Fits

OpenETR does not create a compliant DPP by itself.

It does not decide:

- which products require a passport;
- which data is mandatory;
- which identifier scheme applies;
- who qualifies as a verified economic operator;
- which actors may access restricted information;
- whether a product complies with EU law; or
- whether customs or market-surveillance authorities should accept it.

OpenETR can provide a complementary evidence layer.

For a Product Passport integration:

- a canonical passport version can be a **Digital Artifact** identified by its
  digest;
- signed records concerning that version can form a **Digital Controllable
  Record**;
- Registry proofs, conformity documents, repair records, recalls, and
  end-of-life evidence can be linked without silently rewriting earlier
  evidence;
- defined rules can derive **Consequential State**; and
- the passport version can be treated as a **Digital Original** whose identity
  and consequential state can be independently verified.

The applicable EU rules and authorities still determine recognition and
regulatory effect.

## Product Identity And Passport Identity Are Different

A trustworthy implementation must keep several identifiers distinct:

```text
product identifier
Registry registration identifier
passport endpoint
passport version hash
OpenETR event identifier
signer key
```

The persistent product identifier identifies the regulated product, batch, or
model. The passport-version hash identifies exact digital content. The Registry
identifier proves registration in the EU system. An OpenETR event identifies a
signed statement concerning the artifact.

Collapsing these into one identifier would make the evidence less precise.

## A Passport Is Usually A Living Dataset

A DPP may change through correction, repair, refurbishment, recall,
remanufacture, repurposing, recycling, or a change in responsible operator.

That creates a versioning problem. If passport content changes, its digest must
also change. A useful OpenETR profile would preserve:

- the exact canonical snapshot;
- its digest;
- the applicable schema and semantic version;
- its product and Registry identifiers;
- the actor that signed the update;
- its relationship to the prior version; and
- the evidence supporting the change.

The objective is not to freeze the DPP. It is to make change attributable and
reconstructable.

## Product Graphs And Control Graphs

The DPP may contain a rich product graph connecting components, materials,
suppliers, certificates, repairs, and other passports.

OpenETR provides a narrower graph of consequential evidence concerning an
exact digital artifact.

```text
product graph:
  describes the product and its relationships

OpenETR graph:
  preserves signed evidence of consequential actions
  and supports rules-based state derivation
```

OpenETR can sit within a wider DPP evidence architecture without trying to
replace the product data model.

## A Practical Battery Pilot

Batteries are the strongest near-term pilot because the legal deadline is
fixed and the lifecycle is consequential.

A pilot could test:

1. item-level battery and passport identifiers;
2. canonical passport snapshots and version hashes;
3. EU Registry registration and sealed proof capture;
4. public, restricted, and committed evidence;
5. repair, repurposing, second-life, and recycling records;
6. responsible economic-operator and value-chain-actor identity;
7. recall, supersession, and end-of-life state; and
8. continuity when a provider or endpoint changes.

The pilot should integrate with the EU Registry and applicable standards. It
should not create a parallel compliance universe.

## Policy Priorities

Policymakers and implementers should preserve seven principles.

1. **Keep registration and compliance separate.** A valid registration proves
   registration, not every underlying product claim.
2. **Keep product and passport identifiers separate.** Product continuity and
   content-version integrity are different concerns.
3. **Make lifecycle changes attributable.** Later actors should add signed
   evidence rather than silently rewrite history.
4. **Avoid provider dependence.** Evidence and version history should survive
   changes in hosting, software, and responsible operators.
5. **Use graduated access.** Public verification must coexist with trade-secret,
   personal-data, and security protections.
6. **Show the basis for state.** Applications should expose the evidence and
   rules behind consequential conclusions.
7. **Preserve authority boundaries.** OpenETR, DPP providers, and the Registry
   should not claim the compliance or recognition powers assigned to economic
   operators and public authorities.

## Bottom Line

The EU is creating an interoperable DPP ecosystem for product identity,
lifecycle information, circularity, customs, and market surveillance.

OpenETR can complement that system by preserving exact passport versions and
signed lifecycle evidence in a form that remains independently verifiable
across applications.

The relationship is:

```text
EU regulation defines the obligation and effect.
The DPP carries regulated product information.
The Registry indexes and verifies registration.
OpenETR can preserve the evidence behind consequential passport state.
```

This is not a substitute for EU compliance. It is a way to make the evidence
supporting important DPP states more durable, portable, and explainable.

## Detailed Analysis

- [EU Digital Product Passports And OpenETR Regulatory Analysis
  Note](https://github.com/trbouma/openetr/blob/main/docs/specs/EU_DIGITAL_PRODUCT_PASSPORT_REGULATORY_ANALYSIS_NOTE.md)

## Related Materials

- [Product Passports Domain](../product-passports.md)
- [Product Passport Requirements Mapping](../product-passport-requirements.md)
- [European Commission DPP
  portal](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport_en)
- [EU DPP Registry](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport/dpp-registry_en)
- [Ecodesign Working Plan
  2025-2030](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025DC0187)
