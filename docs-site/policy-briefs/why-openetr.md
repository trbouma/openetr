# Why OpenETR

OpenETR exists because many important records are becoming digital, but the digital systems around them still tend to confuse three separate questions:

- What is the record?
- Who controls it?
- What legal or commercial effect follows from that control?

Those questions are related, but they should not be collapsed into one application, one database, one wallet, one registry, or one legal rulebook.

OpenETR is designed as a thin, open protocol for durable electronic records.
Its control layer identifies a Digital Artifact by cryptographic digest and
records signed lifecycle evidence about that artifact as a Digital
Controllable Record. Validation checks the DCR evidence, and protocol rules
derive consequential state; many different domain systems can then interpret
and recognize that state.

The OpenETR protocol construct is the **Digital Controllable Record**: one
signed end-verifiable record or graph concerning a Digital Artifact. Protocol
rules derive consequential state from validated DCR evidence; the recognition context determines
accepted effect. Electronic transferable records are one important
subclass, but the same control-layer pattern can also support non-transferable
records, credentials, linked evidence, Product Passports, health records,
Apostille documents, and authority-recognized records. See the [Controllable
Records Taxonomy](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROLLABLE_RECORDS_TAXONOMY.md).

This gives OpenETR a precise position in a larger system. A host application
may propose actions, authenticate users, evaluate permissions, obtain
approvals, and control execution. OpenETR makes the resulting statements
portable and independently verifiable, then derives candidate state from that
evidence under explicit rules. A relying party separately decides whether to
recognize the state and act on it.

## The Problem

Digital records are easy to copy.

That is useful for ordinary documents, but it is a problem for records whose value depends on exclusive control, provenance, presentation, transfer, or redemption.

Examples include:

- warehouse receipts
- bills of lading
- promissory notes
- certificates
- product data artifacts
- tickets
- permits
- other electronic transferable records

Many existing systems solve this by making the platform itself the source of truth. A database, registry, wallet provider, document platform, or trade network decides what exists and who can act on it.

That can work inside one closed environment. It becomes harder when records need to move across organizations, jurisdictions, industries, relays, archives, and recognition frameworks.

OpenETR is not intended to compete with or replace existing electronic transferable record systems, warehouse receipt platforms, registries, document services, or trade networks. Its role is more modest and more infrastructural: it can work behind the scenes as a connective control fabric. Existing systems can keep their user interfaces, account models, databases, document formats, and rulebooks while using OpenETR events as cryptographically self-contained evidence that can move between them.

## The OpenETR Approach

OpenETR separates the control problem from the recognition problem.

At the control layer, OpenETR asks:

- What Digital Artifact is the subject of the record?
- Which signed Anchor record began the candidate DCR?
- Which signed records changed or annotated its candidate state?
- Who is the current controller under a selected policy?
- What evidence supports that conclusion?

At the recognition layer, another system asks:

- Is the issuer legally recognized?
- Did the document satisfy the relevant formal requirements?
- Did title pass?
- Is a security right valid or perfected?
- Is the participant authorized under a statute, contract, registry, or institutional rule?
- Should this verifier recognize the event as effective?

This separation is the central rationale of the project.

OpenETR preserves durable signed evidence. Recognition frameworks decide what effect to give that evidence.

## From Action To Consequence

A consequential action passes through several logically different stages:

```text
proposal -> authorization -> commitment -> execution -> evidence -> derived state
```

One system may combine several stages, but they should remain distinguishable.
A request to transfer a receipt is not the transfer. Permission to make the
transfer is not proof that it was made. A signed OpenETR record is durable
evidence of the statement made by its signer; it is not automatic proof of an
external operation, universal authority, or legal effect.

OpenETR therefore distinguishes three boundaries:

1. **Evidence commitment:** a signer creates an immutable, attributable record.
2. **Protocol consequence:** a verifier evaluates that record in its DCR and
   derives consequential state under stated rules.
3. **Operational or legal effect:** a host system, registry, institution,
   counterparty, or applicable law decides whether to act on or recognize that
   state.

Relay acceptance means that an event was stored or forwarded. It is not, by
itself, authorization, execution, consensus, or recognition.

This boundary also makes OpenETR useful inside strongly controlled systems. A
host can evaluate the current DCR immediately before a protected signing or
execution operation, refuse an ineligible action, and publish evidence of the
result. The host supplies the controlled path to execution; OpenETR supplies
portable evidence and independently derivable state. Other systems can later
verify the evidence without depending on the original application runtime.

OpenETR remains useful where no single system controls the whole path. It can
preserve conflicting or policy-inconsistent statements rather than making
authentic signed evidence disappear. A verifier can warn, reject a candidate
transition, or select among branches according to its rule book. Preservation
of evidence and permission to execute are separate concerns.

## Why The Model Extends Beyond Transferable Records

Not every important electronic record is transferable.

Some records need exclusive control and transfer, such as warehouse receipts, bills of lading, or promissory notes. Other records need durable lifecycle evidence without negotiability, such as Product Passports, health records, certificates, Apostille documents, permits, or compliance artifacts. Credentials add another pattern: they may be claim-centric records in their own right, or they may help prove that an actor is authorized to sign an OpenETR event.

The Artifact/DCR/state model gives OpenETR a broader policy vocabulary without
assuming that every record is negotiable or legally controllable.

It lets policymakers and implementers distinguish:

- records where transfer of control may have legal or commercial effect;
- records where control means stewardship, authority, status, or lifecycle accountability;
- credentials and attestations that support recognition of an actor or event;
- linked evidence records that support a Digital Artifact's history;
- registry or authority-recognized records whose effect depends on an external rulebook.

This terminology keeps the layers clean. A **Digital Artifact** is persistent
content identified by digest. A **Digital Controllable Record** is the signed
evidence record or graph concerning that artifact. A **Digital Original** is
the Digital Artifact once consequential state has been established through its
DCR. Legal and policy categories remain recognition
questions.

That framing keeps OpenETR from becoming too narrow. It can remain deeply
relevant to electronic transferable records while also applying the same DCR
evidence and state-transition pattern to other durable electronic records.

## Why An Open Graph

OpenETR treats each Digital Artifact as the subject of one or more candidate
DCR graphs.

The graph may include:

- an Anchor record
- transfer events
- attestation events
- encumbrance and discharge events
- redemption and termination events
- linked evidence records
- profile and participant references
- policy warnings or recognition annotations

This is different from a digital wallet model.

A digital wallet is primarily a credential container. It holds credentials for a person or organization and helps the holder present selected claims to relying parties.

OpenETR is not mainly a container. It is a shared DCR evidence structure about
a Digital Artifact.

The wallet question is:

```text
What credentials does this holder carry?
```

The OpenETR question is:

```text
What happened concerning this Digital Artifact?
```

Wallets can still be important. A wallet credential may prove identity, authority, regulated status, or eligibility. But those credentials support actions in the graph; they do not replace the graph.

## Why Not A Single Registry

A registry can be a recognition authority.

It can decide which issuers are admitted, which transfers it recognizes, which documents are valid, and what disputes or corrections mean inside its rulebook.

OpenETR does not try to replace that role.

Instead, it gives registries, platforms, banks, operators, and relying parties a shared signed evidence substrate.

The same OpenETR graph can be evaluated by:

- a warehouse receipt registry
- a bank
- a buyer
- a warehouse operator
- an insurer
- a regulator
- a court
- a private trade network

Each may apply a different rulebook. The signed evidence remains portable.

Those rulebooks may also reach different conclusions. Signatures and event
links make the evidence attributable and tamper-evident; they do not make one
verifier's policy globally authoritative.

## Why A Behind-The-Scenes Fabric

OpenETR is designed to be embedded, wrapped, or hidden inside existing systems.

A warehouse receipt platform should not have to replace its receipt workflow. A trade finance network should not have to abandon its portal. A registry should not have to give up its rulebook. A document management system should not have to store records in a new proprietary database.

Instead, OpenETR can generate self-contained identifiers and signed events around the record:

- the Digital Artifact is identified by a digest derived from its content;
- signed records concerning it form a candidate DCR;
- each event is signed by the acting profile key;
- event ids are content-derived;
- graph links are carried in signed tags;
- events can be stored on relays, in databases, in archives, in files, or in any system that can preserve the signed event data.

That makes OpenETR more like a fabric than a destination platform.

It can connect existing ETR systems, warehouse receipt systems, registries, verifiers, archives, and domain applications without requiring them to share one runtime or surrender their existing source systems. The important thing is that the control evidence is portable, independently verifiable, and not locked inside one application database.

This is why OpenETR can be useful even when a mature domain system already exists. It gives that system a way to publish and consume durable control evidence that can survive outside the system's own walls.

## Why Nostr

OpenETR uses Nostr-style signed events and relays as a publication and retrieval substrate.

That gives the project:

- portable signed records
- artifact-centric queries by digest
- relay-backed distribution
- independently verifiable event signatures
- simple replication across infrastructure
- a small wire format that does not need to encode every legal rule

Nostr is not the legal authority. It is the wire format and relay layer.

The authority comes from the signers, profiles, attestations, registries, policies, and recognition frameworks that a verifier chooses to trust.

## Why Domain Adapters

Different domains need different language.

A warehouse receipt system should speak in terms of receipts, holders, goods, warehouse operators, liens, presentation, and delivery.

A product passport system should speak in terms of products, components, compliance evidence, lifecycle events, manufacturers, and repair or recycling data.

OpenETR should not force every domain to use the same user-facing vocabulary.

Instead, domain adapters translate local workflows into common OpenETR control operations:

- issue
- transfer
- attest
- encumber
- discharge
- redeem
- terminate
- link evidence

This lets the protocol stay general while the application surfaces stay natural.

## What OpenETR Is Not

OpenETR is not:

- a universal title registry
- a legal recognition engine
- a KYC system
- a complete business workflow or approval engine
- a universal authorization or execution gate
- a global ordering, transaction, or consensus service
- a document storage platform
- a closed trade network
- a wallet-only credential model
- a blockchain smart contract system

It may interoperate with any of those systems.

Its narrower job is to preserve and verify signed control evidence for
digest-identified records and to derive consequential state under explicit
rules. An integrated system may enforce stronger operational controls, but
that claim belongs to the defined integration boundary, not to the existence
of a signed event alone.

## Policy Value

OpenETR is useful because it gives policymakers, registries, platforms, and institutions a clean boundary.

They can adopt digital transferable-record workflows without requiring one platform to own the whole legal, technical, and commercial stack.

The project supports:

- legal neutrality across recognition frameworks
- domain neutrality across record types
- infrastructure portability across relays and archives
- independent verification of signed evidence
- actor neutrality across human, organizational, service, and agent signers
- replayable state derivation from attributable event history
- clean integration with protected authorization and execution boundaries
- policy-specific recognition without protocol fragmentation
- gradual adoption by existing registries and institutions

That is the reason for OpenETR:

```text
Portable evidence.
Consequential state derived by rule.
Execution controlled by the integrating system.
Recognition and effect determined in context.
```

## Source Specifications

- [Controllable Records Taxonomy](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROLLABLE_RECORDS_TAXONOMY.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR Nostr Wire Format](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
