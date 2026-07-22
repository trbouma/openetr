# Why Control Is Not Recognition

OpenETR separates two questions that digital-record systems often collapse:

- Who controls this record?
- What effect should that control have?

Those questions are related, but they are not the same.

OpenETR provides a general control layer for durable electronic records. It identifies a record by digest and preserves signed evidence about the record's lifecycle. Recognition frameworks decide what legal, regulatory, commercial, or operational effect to give that evidence.

## The Control Question

Control is an evidence question.

At the control layer, OpenETR can ask:

- What object digest is being referenced?
- Which signed origin record brought the object into the graph?
- Which signed control records reference the same object?
- How do later records link to prior records?
- Which profile key signed each record?
- What candidate controller or lifecycle state can be derived from the graph?
- Which linked evidence records point back to the object?

These questions can be answered by inspecting cryptographic evidence.

The result is not a hidden database state. It is a signed control graph that can be queried, replayed, and independently verified.

## The Recognition Question

Recognition is an effect question.

At the recognition layer, a verifier, registry, authority, court, platform, or relying party asks:

- Is this signer legally authorized?
- Is this issuer recognized for this domain?
- Does this profile key map to a known organization or role?
- Does the record satisfy the required legal or policy form?
- Does a registry accept this event?
- Does a statute give effect to this control transition?
- Should an encumbrance, discharge, redemption, or termination be accepted?

These questions cannot be answered by signatures alone.

They depend on law, contracts, institutional rules, trust registries, onboarding, authority records, verifier policy, and the facts of the particular domain.

## Why The Difference Matters

If control and recognition are collapsed, the system has to pretend that one platform, database, wallet, registry, or smart contract decides everything.

That creates brittle systems.

It can make the technical operator appear to decide legal effect. It can hide policy disagreements. It can make one registry or platform the only practical place where the record exists. It can also make it harder for courts, regulators, banks, insurers, marketplaces, and trading partners to apply their own rules to the same evidence.

OpenETR takes a different approach:

```text
Publish signed control evidence.
Verify the graph.
Apply recognition policy separately.
```

This lets the same evidence graph be evaluated by different relying parties without changing the underlying record.

## What OpenETR Can Prove

OpenETR can provide durable signed evidence that:

- a specific file, document, or data artifact has a particular digest;
- a profile key signed an origin record for that digest;
- later events reference the same object;
- events link to prior events;
- a transfer, attestation, encumbrance, discharge, redemption, termination, or linked evidence record was published;
- the event signatures and ids verify;
- the event graph can be reconstructed from relays, mirrors, exports, or local records.

That is powerful.

It gives verifiers a shared factual substrate.

## What OpenETR Does Not Prove By Itself

OpenETR does not, by itself, prove:

- that a signer is legally licensed;
- that a signer had organizational authority;
- that a warehouse receipt, Product Passport, Apostille, or other document satisfies all formal requirements;
- that title passed;
- that a security right was perfected;
- that a Product Passport satisfies an applicable delegated act;
- that a Competent Authority must accept an attestation;
- that a court, regulator, registry, bank, or marketplace must recognize the event.

Those are recognition conclusions.

OpenETR can preserve the evidence needed to reach them, but it should not claim to decide them inside the base protocol.

## Policy Layers Are Not Protocol Forks

Different organizations can apply different recognition rules to the same signed graph.

A warehouse receipt registry may require a licensed warehouse operator profile. A bank may require KYC and encumbrance disclosure. A customs authority may require a specific Product Passport registry response. A marketplace may accept only certain manufacturers or repairer attestations.

Those differences should be expected.

They do not require different OpenETR protocols. They require different verifier policies over the same evidence substrate.

A good verifier should show:

- the signed evidence;
- the baseline graph structure;
- the selected rule book;
- warnings or policy failures;
- the resulting candidate or recognized state.

The evidence remains visible even when a policy refuses recognition.

## Examples

### Warehouse Receipts

OpenETR can show that a warehouse receipt digest was issued, transferred, pledged, discharged, presented, or terminated by particular profile keys.

Warehouse receipt law, registry rules, storage agreements, courts, and verifier policy decide whether those actions are legally effective.

### Product Passports

OpenETR can show the original Product Passport digest, the issuer profile, linked lifecycle evidence, and verifier warnings.

Product regulation, delegated acts, registries, market-surveillance authorities, customs authorities, marketplaces, and relying parties decide whether the passport information is sufficient and recognized.

### Apostille Documents

OpenETR can show a document bundle digest, authority attestations, registry references, and verification history.

The Apostille Convention framework, Competent Authorities, e-Registers, courts, agencies, and relying institutions decide the legal recognition of the Apostille.

### Digital Wallets

A wallet credential can help show who is acting or what authorization they hold.

OpenETR records what happened to the object.

The relying party decides whether the wallet credential and OpenETR graph together satisfy the applicable policy.

## The Policy Value

Separating control from recognition gives policymakers and institutions a cleaner design space.

They can:

- adopt durable electronic records without requiring one central platform;
- preserve independently verifiable signed evidence;
- let registries and authorities apply domain-specific rules;
- allow different sectors to reuse the same control layer;
- support policy-specific recognition without fragmenting the protocol;
- make disputes easier to inspect because the evidence remains visible.

The core principle is:

```text
Control is what the signed graph shows.
Recognition is what a rule book does with it.
```

OpenETR should remain disciplined about that boundary.

## Source Specifications

- [Recognition Boundary](../openetr/recognition.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OpenETR MLWR Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_MLWR_PROFILE.md)
- [Digital Product Passport Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_PRODUCT_PASSPORT_REQUIREMENTS_MAPPING.md)
