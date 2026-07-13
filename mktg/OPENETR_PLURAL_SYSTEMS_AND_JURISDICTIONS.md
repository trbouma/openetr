# OpenETR Across Systems and Jurisdictions

OpenETR is designed for a world where transferable records do not live inside one system, one institution, or one legal jurisdiction.

Trade, logistics, finance, and storage workflows cross organizational boundaries. A single warehouse receipt, bill of lading, or other transferable record may be relevant to many parties:

- warehouse operators;
- carriers;
- exporters and importers;
- banks and secured lenders;
- buyers and sellers;
- insurers;
- registries;
- auditors;
- courts and arbitral forums;
- regulators and public authorities;
- technology platforms and service providers.

Each party may use different software. Each jurisdiction may apply different legal rules. Each institution may require its own recognition policy.

OpenETR is built for that plurality.

## The Core Idea

OpenETR separates the signed evidence of control from the legal or institutional recognition of that evidence.

That separation lets many systems inspect the same control graph while applying different rule books.

One system may use OpenETR events inside a warehouse platform. Another may integrate them into a bank workflow. A third may verify them through a registry. A fourth may archive them for dispute resolution. They do not all need to run the same application or rely on the same hosted service at time of performance.

The common substrate is the signed event graph.

## Plural Systems

OpenETR is not intended to replace existing systems.

It is intended to connect them through portable evidence.

An organization can integrate OpenETR in several ways:

- through the installable Python component;
- through the command-line interface;
- through REST APIs exposed by an application or service;
- through a hosted platform;
- through direct protocol-level handling of OpenETR wire-format events;
- through relay-backed event retrieval;
- through local event storage and verification.

This means OpenETR can sit behind an existing account-based system, inside a new workflow application, or alongside a registry or document-management system.

The system that creates, displays, or stores the record does not have to be the same system that later verifies it.

## Plural Legal Jurisdictions

OpenETR does not assume one universal legal rule.

That is deliberate.

Electronic transferable records, warehouse receipts, secured finance records, and trade documents are recognized through legal frameworks such as:

- the UNCITRAL Model Law on Electronic Transferable Records;
- the UNCITRAL-UNIDROIT Model Law on Warehouse Receipts;
- UCC Article 12 and related commercial law;
- national warehouse receipt legislation;
- secured transactions law;
- registry rules;
- platform rules;
- contract terms;
- court or arbitral orders;
- institutional policies.

OpenETR provides evidence that these frameworks can evaluate. It does not replace them.

A verifier in one jurisdiction may treat a transfer as effective. A verifier in another may require additional registry attestation. A bank may require a known-entity policy. A court may examine the same signed graph as evidence but apply its own legal conclusions.

This is expected. OpenETR is designed so that different legal systems can reason over the same event evidence without requiring identical recognition outcomes.

## Recognition Is Local and Accountable

OpenETR makes recognition explicit.

The event graph can show:

- the record digest;
- the origin event;
- the issuer;
- the current controller under the graph;
- transfers;
- encumbrances;
- discharges;
- redemptions;
- terminations;
- medium changes;
- attestations;
- external references;
- signer profiles;
- known entities;
- verifier warnings.

But the recognition decision belongs to the relying system.

That system should be able to say:

- which policy it applied;
- which signers it recognized;
- which attestations it required;
- which warnings it accepted or rejected;
- which graph branch it treated as effective;
- which legal or institutional framework controlled the result.

This makes recognition accountable rather than hidden inside a platform's database state.

## Relays, Local Stores, and Independence

OpenETR events can be relay-backed, but relay-backed does not mean relay-dependent.

Relays provide distribution, discovery, indexing, and availability. They are useful infrastructure. But the signed events are the durable evidence.

A relying party can:

- retrieve events from public relays;
- mirror events to private relays;
- archive events locally;
- exchange event bundles directly;
- verify signatures and graph links without trusting the original application;
- apply its own policy to the same event set.

The core philosophy is that there should be no requirement to rely on someone else's running code at time of performance.

If the relevant signed events and policy are available, the record history can be inspected.

## Identity Across Systems

OpenETR's root-and-profile model is designed to integrate with existing identity environments.

A root key can organize operational profile keys. A profile can represent an acting role, office, business unit, system account, warehouse operator, exporter, bank desk, or service component.

Existing platforms can hide this behind their own user accounts and permission systems. A user may log in with a familiar enterprise account, while the system signs OpenETR events using the appropriate operational profile.

OpenETR also supports aliases, known entities, NIP-05 identifiers, and external recognition inputs such as trust registries or web-of-trust signals.

The result is flexible:

- systems can use their own account model;
- OpenETR can still produce portable signer evidence;
- verifiers can decide which keys and profiles they recognize.

## Domain Adapters

OpenETR's control layer is general.

Domain adapters translate that general model into domain language.

For warehouse receipts, the MLWR adapter can speak in terms of:

- warehouse operator;
- depositor;
- holder;
- transferee;
- secured party;
- receipt reference;
- goods description;
- storage agreement;
- change of medium;
- delivery and termination.

Underneath, these map to generic OpenETR objects, profiles, signed events, actions, tags, and verifier policies.

This pattern allows OpenETR to support many domains without making each domain its own isolated protocol.

## What OpenETR Does Not Claim

OpenETR does not claim that publication of an event automatically creates legal effect everywhere.

It does not decide by itself:

- whether a warehouse operator is licensed;
- whether a depositor had authority;
- whether a transfer creates protected-holder status;
- whether an encumbrance has priority;
- whether a paper receipt was legally made inoperative;
- whether a document satisfies all statutory content requirements;
- whether a court or registry must recognize a state transition.

Those are recognition questions.

OpenETR makes the evidence available for those questions.

## Positioning Statement

OpenETR is built for plural systems and plural legal jurisdictions.

It provides a portable, signed control graph that many systems can issue, store, relay, inspect, and verify. It lets each legal jurisdiction, registry, institution, or relying platform apply its own recognition policy to the same underlying evidence.

This makes OpenETR especially useful where records cross organizational and legal boundaries, and where no single platform should be assumed to be the permanent source of truth.

## Short Form

OpenETR gives many systems a shared evidence layer without forcing one recognition authority.

