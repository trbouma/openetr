# EUDI Wallet And OpenETR

The European Digital Identity Wallet and OpenETR solve related but different problems.

The EUDI Wallet is centered on identity, credentials, user control, selective disclosure, authentication, and presentation to relying parties. OpenETR is centered on durable electronic records, control events, linked evidence, and recognition of effect under domain policy.

They should be seen as complementary layers, not competing architectures.

## The EUDI Wallet Question

The EUDI Wallet asks:

```text
Who is presenting this identity, attribute, credential, or authorization?
```

In the EUDI ecosystem, wallets help citizens, residents, and businesses hold and present identity data, certificates, and other digital documents. The broader architecture coordinates wallet providers, issuers, and service providers around common specifications, interoperability, privacy, and user control.

That is a powerful model for:

- proving identity;
- presenting attributes;
- authenticating to public or private services;
- selectively disclosing information;
- carrying official or trusted credentials;
- supporting electronic signatures and trust services.

## The OpenETR Question

OpenETR asks a different question:

```text
What happened to this controlled object?
```

OpenETR identifies a record by digest and records signed events about that record.

The graph may include:

- an origin control record;
- transfer or control events;
- attestations;
- encumbrance and discharge events;
- redemption and termination events;
- linked evidence records;
- profile and participant references;
- verifier warnings or recognition annotations.

OpenETR is therefore object-centric. The central unit is not the holder's wallet; it is the durable electronic record and the signed control/evidence graph around that record.

## Why This Distinction Matters

Many digital trust systems need both identity and object history.

For example:

- a warehouse operator may need to prove it is authorized to issue a receipt;
- a manufacturer may need to prove it is the recognized issuer of a Product Passport;
- a repairer may need to prove it is allowed to attach a lifecycle evidence record;
- a bank may need to prove authority to record an encumbrance or discharge;
- a regulator may need to inspect who signed which record and when.

An EUDI Wallet or wallet-held credential can help answer the identity and authorization question.

OpenETR helps answer the object-history question.

## Complementary Roles

| Function | EUDI Wallet | OpenETR |
| --- | --- | --- |
| Primary focus | Identity, credentials, authentication, selective disclosure, presentation. | Durable records, control records, linked evidence, object history, recognition inputs. |
| Main unit | Wallet holder and wallet-held credentials. | Controlled Object identified by digest. |
| Main question | What credentials does this person or organization present? | What signed events exist for this object? |
| Technical center | Wallet, issuer, verifier, service provider interactions. | Digest, signed events, control graph, evidence graph, verifier policy. |
| Recognition boundary | Relying party decides whether to accept a presented credential. | Verifier, registry, authority, or relying party decides what effect to give the signed graph. |

## How They Can Work Together

A practical integration could look like this:

```text
EUDI Wallet credential
  -> proves identity, role, mandate, or authorization
  -> OpenETR profile signs a record event
  -> OpenETR graph preserves durable signed evidence
  -> registry / authority / relying party evaluates effect
```

In that model, the wallet is not replaced.

The wallet helps establish who is acting, what credential they hold, and what authority they can present. OpenETR then records what that actor did to a particular digest-identified record.

## Product Passport Example

For Product Passports, an EUDI Wallet could help an economic operator or representative authenticate to an issuer, registry, customs authority, marketplace, or service provider.

OpenETR could then record:

- the original Product Passport digest;
- the origin control record for that passport artifact;
- the recognized organization profile key that issued it;
- linked evidence records for repair, recall, recycling, audit, or end-of-life documents;
- durable query links and QR codes;
- verifier output about whether the graph satisfies a selected Product Passport policy.

The wallet supports identity and presentation. OpenETR supports durable object history.

## Warehouse Receipt Example

For warehouse receipts, wallet-held credentials could help prove that:

- a warehouse operator is licensed or recognized;
- a bank officer is authorized to record a pledge or discharge;
- a holder is entitled to present a receipt;
- a regulator or court officer has authority to inspect a record.

OpenETR would still preserve the receipt digest, origin event, transfer path, encumbrances, discharges, redemption, termination, and verifier warnings.

The legal effect of the graph remains a recognition-layer question.

## Policy Implication

Policymakers should avoid treating digital wallets as the only trust layer for durable electronic records.

Wallets are essential for identity, credentials, and user-controlled presentation. But many important records also need an object-centric history that survives outside any one wallet session, application, registry, or platform.

OpenETR offers that object-centric control layer.

It lets identity systems, registries, institutions, and authorities evaluate durable signed evidence without requiring every domain to collapse into a single wallet model.

## What OpenETR Should Not Claim

OpenETR should not claim to be:

- an EUDI Wallet;
- a replacement for EUDI Wallet specifications;
- an identity wallet for citizens or businesses;
- a selective-disclosure credential system;
- a trust service provider;
- a legal recognition engine.

Instead, OpenETR should claim the narrower role:

```text
A general control layer for durable electronic records.
```

It preserves durable signed evidence about digest-identified records so that wallets, registries, authorities, and relying parties can evaluate recognition and effect.

## Sources

- [EUDI Wallet And OpenETR Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/EUDI_WALLET_AND_OPENETR_DESIGN_NOTE.md)
- [European Digital Identity Wallet Architecture and Reference Framework](https://digital-strategy.ec.europa.eu/en/library/european-digital-identity-wallet-architecture-and-reference-framework)
- [EU Digital Identity Wallet Toolbox Process](https://digital-strategy.ec.europa.eu/en/policies/eudi-wallet-toolbox)
- [EUDI Wallet Reference Implementation](https://docs.eudi.dev/latest/)
- [Verifiable Credentials and mDL as Specialized Instances of OpenETR](https://github.com/trbouma/openetr/blob/main/docs/specs/VC_AND_MDL_AS_SPECIALIZED_INSTANCES_OF_OPENETR_NOTE.md)
