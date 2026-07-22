# EUDI Wallet And OpenETR Design Note

This note compares the European Digital Identity Wallet, or EUDI Wallet, with OpenETR.

It is a conceptual design note. It does not claim formal equivalence with EUDI Wallet specifications, and it does not propose replacing EUDI Wallet architecture, eIDAS trust services, or wallet-based credential presentation.

## Status

Draft.

## Core Claim

EUDI Wallet and OpenETR solve related but different problems.

- EUDI Wallet is primarily **holder-centric** and **credential-centric**.
- OpenETR is primarily **object-centric** and **control/evidence-centric**.

They should be treated as complementary layers.

The wallet helps answer:

> Who is presenting this identity, attribute, credential, authorization, or mandate?

OpenETR helps answer:

> What happened to this digest-identified controlled object?

## EUDI Wallet Role

The EUDI Wallet ecosystem is designed around wallets, issuers, and relying parties or service providers.

Its focus includes:

- identity and authentication;
- trusted credentials and attestations;
- wallet-mediated presentation;
- selective disclosure;
- user control over shared data;
- interoperability across Member States and relying parties;
- support for electronic signatures and trust-service interactions.

That makes the EUDI Wallet a natural mechanism for proving identity, role, authorization, mandate, or eligibility in a digital transaction.

## OpenETR Role

OpenETR is a general control layer for durable electronic records.

It identifies a record by digest and records signed events about that object.

The OpenETR graph may include:

- an origin control record;
- transfer or control events;
- attestations;
- encumbrance and discharge events;
- redemption and termination events;
- linked evidence records;
- profile and participant references;
- verifier warnings or recognition annotations.

OpenETR is therefore not primarily a holder wallet or credential container. It is an object-centric control and evidence graph for a digest-identified record.

## Architectural Distinction

| Aspect | EUDI Wallet | OpenETR |
| --- | --- | --- |
| Primary orientation | Holder-centric and credential-centric. | Object-centric and lifecycle-centric. |
| Main unit | Wallet Unit and wallet-held credentials. | Controlled Object identified by digest. |
| Main interaction | Presenting credentials or attributes to relying parties. | Publishing and querying signed records about an object. |
| Typical question | What credentials does this holder present? | What signed events exist for this object? |
| Trust focus | Issuers, wallets, relying parties, trust services, credential formats, and presentation protocols. | Profile keys, event signatures, object digests, control graphs, linked evidence records, and verifier policy. |
| Recognition boundary | Relying party decides whether to accept a wallet presentation. | Verifier, registry, authority, or relying party decides what effect to give the OpenETR graph. |

## Complementary Integration Pattern

A practical integration could use EUDI Wallet credentials to authorize OpenETR actions:

```text
EUDI Wallet credential
  -> proves identity, role, mandate, or authorization
  -> OpenETR profile signs a record event
  -> OpenETR graph preserves durable signed evidence
  -> registry / authority / relying party evaluates recognition and effect
```

In this pattern:

- the wallet helps establish who is acting;
- the credential helps show why that actor is authorized;
- the OpenETR profile signs the object-specific action;
- the OpenETR graph records what happened to the digest-identified object;
- a recognition layer decides whether the event has legal, regulatory, or operational effect.

## Product Passport Application

For Digital Product Passports, EUDI Wallet credentials could help an economic operator or authorized representative authenticate to an issuer, registry, customs authority, marketplace, or service provider.

OpenETR could then preserve durable signed evidence of:

- the original Product Passport digest;
- the origin control record for the passport artifact;
- the organization profile key that issued or updated the graph;
- linked evidence records for repair, recall, recycling, audit, inspection, or end-of-life documents;
- durable query links and QR codes;
- verifier output under a selected Product Passport profile.

The EUDI Wallet supports identity, authorization, and presentation. OpenETR supports durable object history.

## Warehouse Receipt Application

For warehouse receipts, EUDI Wallet credentials or wallet-presented attestations could help show that:

- a warehouse operator is licensed or recognized;
- a bank officer is authorized to record a pledge or discharge;
- a holder is entitled to present a receipt;
- a regulator, court officer, or other authority has a right to inspect evidence.

OpenETR would still preserve the receipt digest, origin event, transfer path, encumbrances, discharges, redemption, termination, and verifier warnings.

The wallet credential may support recognition of the signer or actor. It does not replace the object graph.

## Recognition And Effect Boundary

Neither EUDI Wallet presentation nor OpenETR event publication should be treated as automatic legal effect in every context.

For EUDI Wallet, a relying party still decides whether a presented credential satisfies the relevant service, legal, or policy requirement.

For OpenETR, a verifier, registry, authority, court, marketplace, or relying party still decides what effect to give the signed graph.

OpenETR can preserve durable signed evidence that:

- a digest-identified object exists in the graph;
- a recognized profile key signed an event;
- an event links to a prior event or object digest;
- linked evidence records point to supporting artifacts;
- a verifier policy produced warnings, recognition, or non-recognition annotations.

OpenETR does not decide:

- legal identity;
- legal authority;
- credential validity under EUDI rules;
- trust-service compliance;
- wallet conformance;
- statutory effect;
- registry admission;
- final reliance by a verifier.

## Policy Implication

Digital wallets should not be treated as the only trust layer for durable electronic records.

Wallets are essential for identity, credentials, authentication, selective disclosure, and user-controlled presentation. But many important records also need an object-centric history that survives outside any one wallet session, application, registry, platform, or presentation flow.

OpenETR can provide that object-centric control layer.

The result is a cleaner architecture:

```text
Wallets prove who can act.
OpenETR records what happened to the object.
Recognition frameworks decide effect.
```

## Relationship To VC And mDL Note

This note complements [VC_AND_MDL_AS_SPECIALIZED_INSTANCES_OF_OPENETR_NOTE.md](./VC_AND_MDL_AS_SPECIALIZED_INSTANCES_OF_OPENETR_NOTE.md).

That note explains how claim-centric credential models can be viewed as specialized instances of a broader record-and-recognition model. This EUDI Wallet note focuses on the ecosystem distinction between wallet-mediated credential presentation and OpenETR's object-centric control graph.

## Open Questions

- Should OpenETR define a standard way to link wallet-presented credentials to a signed OpenETR event?
- Should a Product Passport profile define recognized EUDI Wallet credential types for issuer, manufacturer, repairer, recycler, auditor, or authority roles?
- Should wallet proof be recorded as an OpenETR attestation, linked evidence record, external reference, or local verifier input?
- How should privacy-sensitive wallet claims be referenced without publishing personal or confidential data to public relays?
- Should OpenETR profiles support short-lived authorization proofs, or only durable organizational profile keys?
- Which recognition rules belong in OpenETR verifier policy and which belong entirely to external EUDI or registry infrastructure?

## Sources

- [European Digital Identity Wallet Architecture and Reference Framework](https://digital-strategy.ec.europa.eu/en/library/european-digital-identity-wallet-architecture-and-reference-framework)
- [EU Digital Identity Wallet Toolbox Process](https://digital-strategy.ec.europa.eu/en/policies/eudi-wallet-toolbox)
- [EUDI Wallet Reference Implementation](https://docs.eudi.dev/latest/)
