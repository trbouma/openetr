# OpenETR, TradeTrust, And Blockchains

## Policy Proposition

**The policy choice is not simply blockchain or no blockchain. It is a choice
about where consequential state is maintained, how it can be verified, and
who is entitled to determine what follows.**

TradeTrust and OpenETR both seek to make consequential digital records usable
across otherwise independent systems. They share important foundations:
cryptographic integrity, portable verification, key-based attribution, and a
separation between digital content and the infrastructure that records actions
concerning it.

They take different routes.

TradeTrust's transferable-record architecture places owner and holder state in
a blockchain Token Registry and Title Escrow model. OpenETR places signed
evidence in a Digital Controllable Record and lets identified rules derive
Consequential State.

```text
TradeTrust
verifiable document + tokenized status + smart-contract state

OpenETR
digest-identified artifact + signed DCR evidence + derivation rules
```

This is not a contest between a cryptographic system and a non-cryptographic
one. Both use cryptography. The difference is whether a shared blockchain
execution environment maintains the accepted current state or whether any
conforming verifier can reproduce the state from portable evidence.

## TradeTrust's Contribution

TradeTrust is an open-source digital utility for trade documents. Its current
framework combines verifiable-document technologies, issuer identification,
human-readable rendering, and blockchain-backed transferability.

For a transferable record, the document identifies a blockchain network,
Token Registry, and token id. Title Escrow contracts distinguish owner and
holder roles and enforce permitted transitions. The blockchain supplies a
shared order for accepted transactions and a common state visible to
participants using that chain and contract model.

This architecture offers real benefits:

- one common owner and holder state;
- contract-enforced transition rules;
- blockchain ordering of competing transactions;
- mature wallet, node, explorer, and indexing infrastructure; and
- a focused reference model for digital trade and MLETR-style transferability.

TradeTrust also reduces dependence on any one trade platform. Compatible
software can verify the document and inspect its transferable status.

## The OpenETR Alternative

OpenETR begins with a Digital Artifact identified by digest. Signed Anchor and
Evidence Records concerning that artifact form a Digital Controllable Record.
A verifier validates the evidence and applies an identified rule book to
derive Consequential State.

OpenETR does not require a blockchain, token, or smart contract to maintain the
authoritative current state. Its evidence may be replicated through public or
private relays, stored by applications, archived, or carried in a local
evidence package.

The design objective is:

> No application, database, service, platform, or blockchain should have to
> exclusively own the evidence from which consequential state is derived.

This makes OpenETR attractive where participants cannot agree on one chain,
where several jurisdictions or institutions apply different policies, or
where a record must remain verifiable after the original service disappears.

## Key Insight: A Lower Threshold For Adoption

OpenETR requires common evidence conventions rather than common identity,
application, or state infrastructure. At the protocol level, a participant
needs a signing key, the artifact digest, compatible signing and verification
software, access to the relevant evidence, and an identified rule book.

It does not require every participant to:

- operate a public website or control a DNS domain;
- create and maintain a DID document;
- use the same issuance platform;
- deploy a smart contract;
- fund a blockchain wallet or wait for transaction finality; or
- connect to one common relay.

The same signed record can be replicated through several public or private
relays, retained by applications and archives, or exchanged as an evidence
package without changing its event id or signature. Relays provide discovery,
transport, and storage; they do not determine the resulting state.

Existing applications can hide the protocol behind familiar business actions.
A warehouse, carrier, bank, or government system can preserve its accounts,
authentication, permissions, documents, and approval workflows while handling
Commitment Profile keys, artifact hashing, record signing, relay publication,
graph traversal, and deterministic verification in the background.

```text
Existing application
  Issue Receipt | Transfer Control | Accept | Verify
          |
          v
OpenETR integration
  digest | sign | publish | retrieve | evaluate
```

Participants also do not need identical internal implementations. One may
embed the OpenETR Python component, another may call a REST service, and
another may use the CLI, an agent-facing JSON interface, or a direct wire-format
implementation. Interoperability rests on the signed evidence and disclosed
rules rather than on shared application code.

TradeTrust platforms can likewise hide wallets, DIDs, contracts, and network
operations from ordinary users. The OpenETR distinction is at the architectural
minimum: those facilities are optional recognition or integration choices,
not mandatory elements of the verification path.

This lighter technical entry point can support incremental adoption. Parties
can first exchange and independently verify evidence, then add the identity,
authority, retention, privacy, and legal-recognition arrangements required by
their domain and jurisdiction. It lowers coordination costs; it does not remove
the need for secure key custody, durable evidence preservation, versioned rule
books, or institutional governance.

## The Blockchain Question

A blockchain contributes more than hash storage. In the TradeTrust model it
provides transaction ordering, shared execution, and a common contract state.
Those properties are useful when participants accept the selected network,
contracts, fees, governance, and wallet model.

They also create dependencies:

- the selected blockchain and contract history must remain available;
- participants need compatible wallets, node access, and transaction funding;
- contract and chain upgrades require governance;
- public transaction metadata may reveal commercial relationships; and
- the contract's technical state still needs legal and institutional
  recognition.

OpenETR removes the common execution environment, not the need for rules or
infrastructure. Its verifiers need a sufficiently complete evidence set and an
identified rule-book version. Conflicts are preserved and reported rather
than globally settled by blockchain consensus.

The trade-off is therefore:

| Common smart-contract state | Independently reproducible state |
| --- | --- |
| Blockchain orders accepted transactions. | Cryptographic links and policy evaluate evidence. |
| Contract rejects unauthorized transitions before state changes. | Invalid or conflicting claims remain visible and are excluded or warned about. |
| Participants converge on one chain and contract result. | Relying parties may apply different rule books to the same evidence. |
| Live status normally depends on chain and contract access. | A complete evidence package can be evaluated locally. |

## Identity And Recognition

Neither a blockchain wallet address nor an OpenETR Key-Based Identifier is a
legal identity by itself. Each proves control of cryptographic verification
material.

TradeTrust uses mechanisms including DIDs, DNS bindings, platform onboarding,
and smart-contract roles to support issuer and participant recognition.
OpenETR uses profiles, attestations, registries, enterprise accounts, and
domain recognition policies around its actor-neutral keys.

In both architectures, institutions and law must still answer:

- Which organization or person controls this key?
- Was that actor authorized for this action?
- Is the technical method reliable for this purpose?
- What legal or commercial effect follows?

Cryptographic certainty about a key is not the same as legal certainty about
an actor or transaction.

## Integrity And Privacy

Both systems can keep the substantive business document outside public
infrastructure and use a cryptographic commitment to bind it to status or
control evidence.

That does not make either system automatically confidential. TradeTrust token
transactions may reveal wallet relationships and timing. Public OpenETR events
may reveal participants, actions, timing, and graph structure. Implementers
must minimize metadata, select appropriate public or private infrastructure,
and preserve confidential content separately.

## Policy Guidance

Governments, standards bodies, and industry consortia should specify the
required properties before selecting the technology:

1. Determine whether the use case needs one globally ordered state or can use
   attributable evidence with explicit conflict rules.
2. Require verifiers to disclose the document identity, evidence sources,
   rule-book version, warnings, and recognition basis behind any status result.
3. Keep cryptographic attribution separate from KYC, authority, licensing, and
   legal recognition.
4. Test whether records remain verifiable when the original platform,
   renderer, API, node provider, relay, or vendor is unavailable.
5. Assess public metadata exposure, not only whether document content is kept
   off-chain or off-relay.
6. Avoid mandating a ledger technology where a functional requirement would
   permit more than one conforming architecture.
7. Preserve paths for bridging: a verifier may use TradeTrust contract state as
   recognition evidence for an OpenETR result, or a TradeTrust platform may
   publish portable OpenETR evidence for cross-system use.

## Complementary Roles

TradeTrust is especially compelling where participants want a common,
contract-enforced owner and holder state for digital trade records and can
adopt its blockchain environment.

OpenETR is especially compelling where the evidence and resulting state must
remain portable across systems, domains, jurisdictions, and verifier policies
without requiring one shared smart-contract runtime.

The two can coexist. A bridge may identify a TradeTrust document as the OpenETR
Digital Artifact, record a contract observation as signed evidence, or make
current contract status a condition in an OpenETR recognition profile. Any
bridge must declare which system is authoritative for each result and how
disagreement is handled.

## Policy Conclusion

TradeTrust demonstrates how a blockchain-backed state machine can support
portable digital-trade documents. OpenETR asks whether portability can extend
one layer deeper: to the signed evidence and rules from which consequential
state is reproduced.

The policy value of OpenETR is not opposition to blockchain. It is
infrastructure plurality. Blockchain state, platform databases, registries,
and attestations may all contribute evidence, while no one service must have
exclusive custody of what a consequential record means.

## Further Reading

- [Detailed OpenETR, TradeTrust, And Blockchain Analysis](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_AND_TRADETRUST_COMPARISON.md)
- [TradeTrust: What Is TradeTrust](https://www.tradetrust.io/about/what-is-tradetrust/)
- [TradeTrust Documentation](https://documentation.tradetrust.io/)
- [TradeTrust Transferable Records](https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/transferability/overview/)
- [TradeTrust Document Integrity](https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/w3c-vc/verifying-documents/document-integrity/)
- [OpenETR Consequential State](../openetr/consequential-state.md)
- [OpenETR Recognition Boundary](../openetr/recognition.md)
