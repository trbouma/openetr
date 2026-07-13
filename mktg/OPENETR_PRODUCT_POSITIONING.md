# OpenETR Product Positioning

OpenETR is an open control layer for transferable records.

Its core thesis is simple:

> A transferable record should be controlled by an open, verifiable graph of signed events, while legal recognition remains a policy decision made by the systems and institutions that rely on that graph.

In shorter form:

> OpenETR separates control evidence from legal recognition.

## The Problem

Transferable records are not just documents. They carry operational and legal state.

A system needs to answer questions such as:

- What record exists?
- Who issued it?
- Who controls it now?
- Was it transferred?
- Are there claims, encumbrances, discharges, redemptions, terminations, or medium changes?
- Which signatures, references, and events support that state?
- Which legal or institutional rule book recognizes that state?

Many existing systems collapse these questions into one platform, registry, smart contract, or database. That can work within a closed environment, but it creates dependency on a particular operator at the time performance is needed.

OpenETR takes a different approach.

## The OpenETR Approach

OpenETR makes the evidence open and portable.

It represents a transferable record as a controlled object surrounded by a graph of signed events. Those events can record issuance, transfer, encumbrance, discharge, redemption, termination, change of medium, attestations, and other control-relevant actions.

The graph can be retrieved from relays, mirrored, archived, exported, or verified locally. If a relying party has the signed events and the applicable policy, it can independently inspect the evidence.

OpenETR does not require every participant to trust the same app, database, smart contract, or hosted service as the final source of truth.

Instead, it gives everyone a common evidence substrate.

## Control Evidence vs Legal Recognition

OpenETR deliberately separates two layers.

The signed event graph answers evidence questions:

- What was issued?
- Which file, document, or record digest identifies the object?
- Which key signed the origin event?
- Which events link to prior events?
- Who appears to be the current controller under the graph?
- Which claims, releases, presentations, or terminations were declared?
- Are the signatures, links, object identifiers, and state transitions verifiable?

The recognition layer answers legal and institutional questions:

- Is this signer authorized?
- Is this warehouse operator licensed?
- Is this transfer legally effective?
- Is this holder protected?
- Does this encumbrance have priority?
- Is this paper or electronic medium currently operative?
- Should this event produce legal effect under MLWR, MLETR, UCC Article 12, a registry rule, a contract, or a court order?

That separation is not a limitation. It is the product's main design choice.

OpenETR makes control portable and recognition accountable.

## How OpenETR Is Different

### Compared With Registry Systems

A registry system often says:

> Our database is authoritative.

OpenETR says:

> The signed event graph is portable evidence. A registry may recognize it, attest it, index it, or add policy, but the evidence can still be verified outside that registry.

This allows registries to remain important without making them the only place where the record can be understood.

### Compared With Smart Contract Systems

A smart contract system often says:

> State changes according to this on-chain program.

OpenETR says:

> State is reconstructed from signed events, and different verifiers can apply different legal or institutional rule books.

This matters for legal instruments because legal effect often depends on facts outside code: authority, notice, good faith, protected-holder status, local law, court orders, registries, sanctions, fraud, insolvency, and institutional rules.

OpenETR can still integrate with blockchain systems where useful, but it does not make a smart contract the only source of meaning.

### Compared With Closed Platforms

A closed platform often says:

> Use our app or API to know the current state.

OpenETR says:

> If you have the signed events, you can verify the graph yourself.

The platform can provide workflow, user experience, hosting, indexing, policy, and support. But the evidence does not have to disappear when a service changes, fails, or is replaced.

### Compared With Document Signing

A document-signing system proves that a document was signed.

OpenETR goes further. It tracks a control and lifecycle graph around the record:

- issuance;
- transfer;
- encumbrance;
- discharge;
- redemption;
- termination;
- change of medium;
- attestations;
- verifier warnings and recognition outcomes.

The document remains important, but the product is about the record's control state, not just the signature on a static file.

### Compared With Pure Nostr Identity or Messaging

Nostr provides open signed events and relay distribution.

OpenETR builds a control model on top:

- controlled object digests;
- origin events;
- control-event chains;
- action semantics;
- graph verification;
- root-and-profile identity;
- aliases and known entities;
- domain adapters such as MLWR;
- verifier policies that distinguish evidence from recognition.

OpenETR uses open signed-event infrastructure, but it is not merely a messaging or social identity system.

## Market Need

Transferable records live across organizations.

A warehouse operator, bank, carrier, buyer, seller, insurer, registry, court, platform, and auditor may all need to inspect the same record from different systems and under different policies.

OpenETR is designed for that reality.

It does not force all parties into one database. It does not ask legal recognition to be reduced to code. It does not hide the record inside a single application.

Instead, OpenETR provides:

- portable signed evidence;
- independently verifiable control history;
- flexible identity through root-and-profile keys;
- relay-backed records that can also be stored and verified locally;
- domain adapters for legal and commercial contexts;
- policy-based recognition for institutions, registries, and verifiers.

## Positioning Statement

OpenETR is an open, signed-event control layer for transferable records.

It lets organizations issue, transfer, encumber, discharge, redeem, terminate, and change the medium of records using a portable event graph that can be independently verified.

Unlike closed platforms, registry-only systems, or smart-contract-only approaches, OpenETR separates the evidence of control from the legal or institutional recognition of that evidence.

That makes it especially well suited for domains where records cross organizational, legal, and technical boundaries: warehouse receipts, bills of lading, negotiable instruments, secured finance records, and other electronic transferable records.

## Short Form

OpenETR makes control portable and recognition accountable.
