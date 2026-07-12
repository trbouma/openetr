# OpenETR and TradeTrust Comparison

This note compares OpenETR's signed control-graph approach with the blockchain smart-contract approach used by TradeTrust and the OpenAttestation Document Store ecosystem.

The purpose is not to criticize TradeTrust. TradeTrust is an important production-oriented reference point for digital trade documents. The useful question for OpenETR is different:

> What changes when control evidence is represented as a portable signed event graph rather than as state managed by a blockchain smart contract?

## TradeTrust In Brief

TradeTrust describes itself as a framework for trade digitalisation that uses blockchain and cryptographic technologies to let trading partners create, exchange, verify digitised documents, and transfer ownership of title documents across digital platforms.

The OpenAttestation Document Store smart contracts are used with the OpenAttestation framework to issue and verify documents on blockchains. The Document Store supports issuance and revocation. The Transferable Document Store supports documents that have an owner and are transferable, with each transferable document represented as an ERC-721 non-fungible token.

In that model, the blockchain smart contract is a central part of the document state mechanism.

## OpenETR In Brief

OpenETR uses a different center of gravity.

OpenETR's core object is a signed control graph:

- an origin event introduces the controlled object
- later control events express transfer, encumbrance, discharge, redemption, termination, or attestation
- Nostr event ids, signatures, and tags provide cryptographic correctness
- relays provide publication and retrieval
- verifiers reconstruct the graph and apply their own recognition policy

OpenETR does not require a smart contract to maintain the authoritative state of the record.

The signed event graph is the shared evidence. Effect remains a policy and recognition question.

## Shared Starting Point: Document Digests

Despite the different state models, both approaches start from the same basic cryptographic move: the issued document is identified by a digest of its bytes.

For a PDF-based receipt, bill of lading, or other issued record, the document bytes can be hashed with SHA-256 to produce a stable content identifier. That digest lets later verifiers check whether the presented PDF is the same document that was issued.

TradeTrust / OpenAttestation uses document roots, target hashes, and Merkle proofs in its document model. The Document Store records issuance and revocation of those hashes or roots, and a verifier checks whether the presented document corresponds to the issued hash evidence.

OpenETR uses the document digest as the controlled object identifier. The current implementation derives the object id from `sha256(<document bytes>)`, carries that object through the `d` and `o` tags, and includes signed structured metadata such as the source name, generation time, and byte size.

The important contrast is therefore not whether document hashing is used. Both models use hashing. The contrast is what happens after the digest exists:

- TradeTrust anchors document state in a blockchain smart contract.
- OpenETR anchors control evidence in a signed event graph that can be retrieved from relays or local stores.

## Transferable Records: Token Registry Versus Control Graph

TradeTrust's transferable-record model uses the document digest as the bridge from the off-chain document to on-chain transfer state.

According to the TradeTrust documentation, Transferable Records consist of two smart contracts:

- a Token Registry
- a Title Escrow

The Token Registry is deployed by the transferable-record issuer, such as a land title registry or shipping line. It replaces the simpler Document Store contract used for non-transferable verification. Its identity is bound to the issuer using DNS.

The Token Registry stores the ownership state of transferable records using a mapping:

```text
document ID -> smart contract address
```

In that model:

- the `document ID`, also called the `token ID`, is the target hash and Merkle root of the individual TradeTrust document
- the mapped smart contract address is the Title Escrow contract for that document
- an unissued document maps to the zero address
- an issued document maps to a Title Escrow contract address
- a returned document maps back to the Token Registry address

This means the issued document is anchored into the smart-contract system through its digest-backed token id.

The Title Escrow then handles the transferable-record roles. TradeTrust distinguishes legal ownership from physical-style possession by modeling:

- an Owner
- a Holder

The Title Escrow holds the token and enforces the rules for changes in token status. The current holder can transfer holdership. The owner can change ownership where the applicable owner/holder conditions are satisfied. Return to issuer is also handled through the Title Escrow lifecycle.

The TradeTrust flow can therefore be summarized as:

```text
issued document
  -> target hash / Merkle root
  -> document ID / token ID
  -> Token Registry mapping
  -> Title Escrow contract
  -> owner / holder state
```

OpenETR uses the same kind of digest foundation, but does not create an ERC-721-style token or Title Escrow contract.

The OpenETR flow is:

```text
issued document
  -> SHA-256 digest
  -> controlled object id
  -> origin event
  -> linked control events
  -> verifier-derived state
```

At the OpenETR layer:

- the origin event introduces the digest-identified object
- transfer, acceptance, encumbrance, discharge, redemption, termination, and attestation are expressed as signed control events
- `e` tags link events into the control graph
- `p`, `enc`, `action`, and related tags express participants and action semantics
- verifiers reconstruct the candidate state and then apply recognition policy

So the compact contrast is:

```text
TradeTrust:
document digest -> token id -> smart contract state

OpenETR:
document digest -> object id -> signed control graph
```

TradeTrust is more concrete and prescriptive for transferable title documents. It provides a smart-contract state machine with owner and holder roles. OpenETR is more general and policy-driven. It provides cryptographic control evidence that can be interpreted by multiple domain adapters, including MLWR warehouse receipts, MLETR bills of lading, credentials, secured-finance records, and other control-relevant electronic records.

## Comparative Example: Transfer Of A Bill Of Lading

Consider an electronic bill of lading issued by a shipping line to a shipper, then transferred to a bank or consignee.

### TradeTrust-style flow

In a TradeTrust-style transferable-record flow:

1. The electronic bill of lading document is wrapped and hashed.
2. The document's target hash / Merkle root becomes the `document ID` or `token ID`.
3. The issuer's Token Registry records the document as issued by mapping that token ID to a Title Escrow contract.
4. The Title Escrow holds the token and stores the current Owner and Holder.
5. A holdership transfer changes the Holder field.
6. An endorsement or owner transfer changes the Owner field, subject to the Title Escrow rules.
7. The endorsement chain can display the transaction history and current owner / holder wallet addresses.
8. When the document is returned to the issuer, the Token Registry and Title Escrow lifecycle reflect that returned state.

The state path is:

```text
bill of lading PDF / wrapped document
  -> target hash / Merkle root
  -> token ID
  -> Token Registry
  -> Title Escrow
  -> Owner / Holder state
```

The smart contracts are doing important work. They provide the state machine for the transferable record and enforce the permitted transitions for owner, holder, endorsement, and return.

### OpenETR-style flow

In an OpenETR-style flow:

1. The bill of lading PDF is hashed with SHA-256.
2. The digest becomes the OpenETR controlled object id.
3. The issuing profile signs a `kind 31415` origin event carrying the object id in `d` and `o`.
4. The current controller signs a `kind 31416` transfer initiation event.
5. The transferee signs a `kind 31416` transfer acceptance event.
6. Later actions such as encumbrance, discharge, redemption, attestation, or termination are signed as additional `kind 31416` control events.
7. Each control event carries the same `o` object id and uses `e` to link to the prior event being relied on.
8. A verifier reconstructs the control graph and applies its accepted recognition policy to decide which events have effect.

The state path is:

```text
bill of lading PDF
  -> SHA-256 digest
  -> object id
  -> origin event
  -> transfer / accept / other control events
  -> verifier-derived controller and lifecycle state
```

The OpenETR events are doing a different kind of work. They provide signed, portable evidence of control-relevant actions. The effective owner, holder, controller, or protected party status is then determined by the relevant domain adapter and recognition policy.

### Side-by-side interpretation

| Step | TradeTrust | OpenETR |
| --- | --- | --- |
| Document identity | Target hash / Merkle root becomes token ID. | SHA-256 digest becomes object id. |
| Issuance | Token Registry maps token ID to Title Escrow. | Origin event introduces the object. |
| Transfer state | Title Escrow stores Owner and Holder. | Control graph records transfer and acceptance events. |
| Transition enforcement | Smart contract logic enforces allowed state changes. | Verifier policy determines which signed events are recognized as effective. |
| Current state query | Read Token Registry / Title Escrow state and endorsement chain. | Retrieve events by object id and replay the linked control graph. |
| Identity | Wallet addresses act as technical identifiers for owner / holder roles. | Profile `npub` keys act as technical identifiers for signers / participants. |
| Legal mapping | Platform, registry, issuer, contract, and law map wallet roles to legal actors and effect. | Root/profile systems, attestations, domain adapters, and law map profile keys to legal actors and effect. |

This example shows the shared conceptual pattern:

```text
document identity -> cryptographic control representation -> recognized transfer effect
```

The difference is where the control representation lives.

TradeTrust places it in a smart-contract token and Title Escrow model. OpenETR places it in a signed event graph that can be replicated through relays or local stores and evaluated by any verifier.

## Architectural Contrast

| Topic | TradeTrust / OpenAttestation Document Store | OpenETR |
| --- | --- | --- |
| State anchor | Blockchain smart contract state. | Signed Nostr event graph. |
| Document identity | Document roots, target hashes, and Merkle proofs bind the presented document to issued hash evidence. | A SHA-256 digest of the issued document bytes becomes the controlled object identifier. |
| Issuance model | Document Store smart contract records issuance and revocation of document roots or target hashes. | Origin event records issuance of the digest-identified controlled object by a profile signer. |
| Transfer model | Transferable documents are represented as ERC-721 NFTs with an owner. | Transfer is expressed as signed control events linked into the object graph. |
| Runtime dependency | Verification and transfer rely on the relevant blockchain network, contract address, and contract state. | Verification relies on retrieved signed events; events can be served by public relays, private relays, archives, or local storage. |
| Execution model | Smart-contract functions update on-chain state. | Local OpenETR software publishes signed events and independently derives candidate state. |
| Identity model | Blockchain addresses and smart-contract roles such as admin, issuer, or revoker. | Root-and-profile identity, where existing systems authenticate users and map them to operational profile signers. |
| Portability | Portable across systems that understand the TradeTrust/OpenAttestation contract model and supported chains. | Portable across systems that can retrieve and verify the OpenETR wire format. |
| Recognition | Legal or operational effect still depends on applicable law, platform rules, and relying-party policy. | Legal or operational effect still depends on applicable law, domain adapter, and verifier recognition policy. |

## The Main Difference

TradeTrust uses blockchain contracts as part of the authoritative technical state layer.

OpenETR uses signed events as the authoritative evidence layer and leaves state derivation to verifiers.

That difference matters because a smart contract answers a state question inside a particular execution environment:

> What does this deployed contract currently say?

OpenETR asks a slightly different question:

> What signed control history exists for this object, and what effect does the verifier's policy give to that history?

The TradeTrust approach is stronger when participants want a common smart-contract state machine and are willing to depend on the selected blockchain network and contract deployment.

The OpenETR approach is stronger when participants want a cryptographic evidence layer that can be replicated, archived, served locally, or retrieved from multiple relay sources without making legal or operational effect depend on one running contract at time of performance.

## Smart Contract State Versus Control Graph Evidence

In a smart-contract model, the contract is not just evidence that something happened. It is also the program that accepts or rejects state transitions.

That can be very useful:

- the contract has a single state view
- supported transitions can be enforced at publication time
- standard token interfaces can be reused
- existing blockchain infrastructure can provide availability, indexing, wallets, and transaction history

It also introduces design commitments:

- the relevant chain must be available and acceptable to the parties
- the contract must be deployed, administered, and upgraded or replaced where needed
- gas, account, wallet, and chain-specific integration concerns become part of the workflow
- state semantics are tied to the contract's code and supported interfaces

OpenETR deliberately avoids making a smart contract the required state machine.

Instead:

- any profile can sign an event
- relays can carry the signed evidence
- any verifier can reject malformed, unsigned, inconsistent, or broken-chain events
- recognition policy decides which structurally valid events have effect

This makes OpenETR less like a token contract and more like a portable signed evidence protocol for control-relevant actions.

## Identity and Integration

TradeTrust-style integrations naturally align with blockchain accounts and smart-contract permissions. The Document Store uses roles such as default admin, issuer, and revoker to control who can call key contract functions.

In that respect, OpenETR profiles are similar to blockchain wallet addresses. Both are cryptographic identifiers that can sign or authorize actions in the technical system. A blockchain address does not, by itself, prove that the address belongs to a particular carrier, bank, warehouse operator, or individual. Likewise, an OpenETR `npub` does not, by itself, prove the legal identity, authority, licensing status, or organizational role of the signer.

The mapping from cryptographic identifier to real-world or legal entity is therefore performed by the systems and policies that use the platform.

In a TradeTrust-style deployment, that mapping may be supported by platform onboarding, issuer registries, smart-contract role assignment, wallet custody arrangements, or institutional processes around who controls a blockchain account.

In OpenETR, the corresponding mapping may be supported by root-managed profiles, relay-backed profile metadata, enterprise account systems, registry attestations, contractual onboarding, or domain-specific recognition profiles.

OpenETR is designed to sit behind ordinary account-based systems.

An enterprise system can authenticate a user with SSO, local account credentials, or another existing method. It can then use OpenETR's root-and-profile model to select the operational signing profile that will sign the event.

That means the OpenETR signing layer can be hidden behind familiar application workflows:

- the human signs in to the enterprise system
- the system maps the user to an allowed OpenETR profile
- the profile signs the OpenETR event
- the event is published to relays or stored locally
- later verifiers evaluate the signed control graph under their own policy

The result is not weaker cryptography. It is a different integration philosophy: the blockchain account is not the primary application account, and the smart contract is not required to be the primary state authority.

## Domain Adapters

TradeTrust is closely associated with digital trade documents and title-document workflows.

OpenETR is trying to keep the protocol layer more general. The OpenETR control graph can be interpreted by domain adapters such as:

- MLWR warehouse receipts
- MLETR electronic bills of lading
- credentials and certificates
- secured-finance records
- bearer-style presentation and redemption workflows

The domain adapter supplies domain vocabulary and UI. The OpenETR layer supplies common control events. The recognition layer supplies legal or operational effect.

This separation lets a warehouse receipt workflow look like a warehouse receipt workflow while still using the same generic control-event family as other domains.

## Complementary, Not Mutually Exclusive

OpenETR and TradeTrust should not be understood as mutually exclusive.

A future implementation could bridge them.

For example:

- an OpenETR origin event could reference a TradeTrust document or contract address
- an OpenETR attestation could record that a TradeTrust verification result was observed
- a TradeTrust-enabled platform could publish OpenETR control events for additional off-chain or cross-system evidence
- an OpenETR recognition profile could require confirmation from a TradeTrust smart contract before treating an event as effective

The important distinction is where each architecture places the shared source of technical truth.

TradeTrust places more of that truth in smart-contract state.

OpenETR places it in a cryptographically verifiable event graph, with recognition determined by the verifier's accepted policy.

## Design Takeaway For OpenETR

The TradeTrust comparison helps sharpen OpenETR's design claim:

> OpenETR is not trying to replace every registry, smart contract, or platform. It is trying to define a portable control-evidence layer that can be independently verified and then recognized by whatever policy the verifier accepts.

This keeps the protocol useful in environments where:

- parties cannot agree on one blockchain
- participants need to integrate with existing account systems
- records need to be verifiable from local archives or relay-backed event stores
- different jurisdictions or institutions apply different recognition rules
- the same control evidence may need to support several domain adapters

In short: TradeTrust shows the value of a blockchain-backed document state model. OpenETR explores the complementary value of a signed-event control graph that can travel across systems without requiring a shared smart-contract runtime.

## Sources

- TradeTrust, "What is TradeTrust", https://www.tradetrust.io/
- TradeTrust, "Transferable Records", https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/transferability/overview/
- TradeTrust, "Title Escrow", https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/transferability/title-transfer/
- TradeTrust, "Title Transfer Example", https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/transferability/title-transfer-example/
- TradeTrust, "Endorsement Chain", https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/transferability/endorsement-chain/
- OpenAttestation Document Store README, https://github.com/Open-Attestation/document-store/blob/master/README.md
