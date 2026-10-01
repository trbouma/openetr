# OpenETR, TradeTrust, And Blockchain-Based Transferability

## Status

Detailed comparative analysis. Last reviewed against the public TradeTrust
documentation on 1 October 2026.

## Purpose

This note compares OpenETR with TradeTrust and, more generally, with
blockchain smart-contract approaches to transferable electronic records.

The comparison is not intended to diminish TradeTrust. TradeTrust is a mature,
open-source digital-trade framework and an important reference implementation
for electronic transferable records. It demonstrates that document integrity,
issuer identification, cross-platform verification, and transferable title
can be assembled into a practical digital utility.

The useful architectural question for OpenETR is:

> What changes when consequential evidence is carried in a portable signed
> record graph and state is independently derived under identified rules,
> rather than maintained as the current state of a blockchain smart contract?

## Executive Assessment

TradeTrust and OpenETR share several goals:

- exact digital content can be cryptographically identified;
- records should be verifiable outside the application that created them;
- cryptographic identifiers must be connected to recognized actors by
  external governance and identity arrangements;
- electronic records should move across otherwise independent systems; and
- technical evidence should support, without pretending to replace, legal
  recognition.

Their principal difference is where consequential state resides.

TradeTrust's transferable-record architecture uses a blockchain token registry
and title-escrow contracts to maintain a shared owner and holder state. The
selected blockchain orders accepted transactions, and smart-contract code
determines which attempted transitions update that state.

OpenETR uses signed Anchor and Evidence Records to form a Digital Controllable
Record (DCR). A verifier validates the evidence graph and applies identified
rules to derive Consequential State. Relays, archives, applications, or local
stores may preserve the evidence, but none of them exclusively owns the
resulting state.

The distinction can be expressed compactly:

```text
TradeTrust transferable record
document identity -> token registry / title escrow -> blockchain state

OpenETR
artifact digest -> signed DCR evidence -> rules -> Consequential State
```

TradeTrust answers:

> What state has this contract accepted on this blockchain?

OpenETR answers:

> What consequential state follows from this validated evidence under these
> identified rules?

Neither question is inherently superior. They express different trust,
governance, infrastructure, and interoperability choices.

## Scope And Documentation Generations

TradeTrust's public documentation currently contains more than one technical
generation. Current introductory material describes TradeTrust as built on the
TrustVC framework and using W3C Verifiable Credentials, Decentralized
Identifiers, cryptographic proofs, and public blockchains. Versioned tutorials
also document the earlier OpenAttestation v2 wrapping, Merkle-proof, Document
Store, Token Registry, and Title Escrow model.

The concepts remain closely related, but they should not be collapsed into one
implementation description:

- current verifiable-document material emphasizes W3C VC data, JSON-LD,
  `did:web`, and cryptographic document proofs;
- current transferable-record schemas identify a token network, token
  registry, and token id;
- the transferable-record implementation continues to use blockchain smart
  contracts for ownership and holdership;
- older OpenAttestation tutorials remain useful for understanding wrapping,
  target hashes, Merkle roots, Document Stores, and earlier issuance paths.

This note therefore distinguishes TradeTrust's enduring architecture from
version-specific implementation details.

## The TradeTrust Model

### Framework and objective

TradeTrust describes itself as an open-source framework and digital utility
for creating, exchanging, verifying, and transferring digital trade records
across platforms. Its three recurring functional concerns are:

- document authenticity and integrity;
- identification of the document source or issuer; and
- ownership and holdership of transferable records.

TradeTrust is specific to digital trade. It provides document schemas,
verification libraries, viewers and renderers, identity conventions, smart
contracts, command-line tooling, and reference workflows.

### Document integrity

Current TradeTrust documentation describes document integrity through W3C
Verifiable Credential proofs associated with a `did:web` verification method.
A verifier retrieves the public verification material, checks the proof, and
confirms that the presented data has not been altered. The model can also
support selective disclosure.

Versioned OpenAttestation flows use wrapped documents, checksums, target
hashes, Merkle roots, and proofs. The exact mechanism differs, but the common
purpose is stable: bind the presented content to cryptographic evidence so
that alteration is detectable.

### Source and identity

TradeTrust uses issuer identity methods such as `did:web`, DNS-DID, or DNS-TXT,
depending on the document type and technical generation. These methods connect
cryptographic verification material or contract addresses to a domain-based
issuer claim.

The cryptography proves possession of the relevant signing or blockchain key.
The identity method and relying context determine what organization is
recognized behind that key or domain.

### Transferability

For transferable records, the TradeTrust document schema includes a
`credentialStatus` entry that identifies:

- the token network and chain id;
- the token-registry contract address; and
- the token id for the record.

The Token Registry is a blockchain smart contract that records transferable
record status. Current TradeTrust guidance describes the registry token as a
soulbound token based loosely on ERC-721 and restricted principally to its
designated Title Escrow contracts. The important point is not the marketing
meaning of NFT. It is that a unique token id connects the digital document to
a programmable, blockchain-maintained state machine.

The Title Escrow model distinguishes:

- **owner** or beneficiary, representing the party with title-related
  ownership; and
- **holder**, representing the party exercising possession-like control of
  the transferable record.

Smart-contract functions support actions such as changing holder, endorsing
ownership, nominating a new owner, accepting an ownership transfer, and
surrendering or returning the record. The blockchain orders transactions and
the contracts reject calls that do not satisfy their current authorization and
state conditions.

### Human presentation

TradeTrust documents are machine-readable data. Decentralized renderers and
compatible viewers turn that data into a human-readable document presentation.
The renderer is separable from the document and may be hosted independently.

This is an important form of portability, but a verifier may still require the
referenced contexts, verification material, renderer, blockchain network,
contract code or interfaces, and related infrastructure for the full
experience.

## The OpenETR Model

### Digital Artifact

OpenETR begins with a Digital Artifact: persistent digital content identified
by a cryptographic digest, normally SHA-256. The artifact may be a PDF, JSON
document, verifiable credential, signed bundle, or another canonical digital
representation.

OpenETR does not need to parse or own the artifact's business content. It needs
an exact, recomputable content identity.

### Digital Controllable Record

A Digital Controllable Record is one signed record or a graph of signed records
concerning the artifact. In the current Nostr binding:

- a regular `kind 1415` Anchor Record introduces a candidate DCR;
- regular `kind 1416` Evidence Records express later actions;
- the `o` tag identifies the artifact by digest;
- `e` tags link records through cryptographic event ids;
- signatures attribute statements to Key-Based Identifiers; and
- action and participant tags carry signed structured semantics.

The DCR is evidence. It is not a mutable status row.

### Consequential State

A verifier validates record identifiers, signatures, artifact consistency,
graph links, minimum record shapes, and transition conditions. It then applies
an identified rule book to derive Consequential State.

Examples include:

- active or terminated;
- current controller;
- transfer pending or accepted;
- encumbrance active or discharged;
- redeemed, surrendered, or changed to another medium; and
- a warning or conflict requiring recognition-layer judgment.

The current implementation uses a Nostr wire format and relay ecosystem, but
the OpenETR model is conceptually separable from any one transport. Signed
records can also be stored in application databases, private relay pools,
archives, evidence packages, or local stores.

### Recognition and effect

OpenETR deliberately separates four questions:

```text
Is the evidence cryptographically and structurally valid?
What Consequential State follows under the selected rules?
Does the relying party recognize that result for this purpose?
What commercial, institutional, or legal effect follows?
```

The first two are protocol and verifier concerns. The last two belong to
domain policy, institutions, agreements, and applicable law.

## Shared Architectural Commitments

### Content integrity is not file custody

Both approaches allow a document to move through ordinary channels while
retaining a means to verify its integrity. Neither requires the business
document itself to be stored as public blockchain state or as relay content.

### A digest connects content to consequential evidence

Both architectures use cryptographic hashing to connect exact content with a
separate control or status mechanism. OpenETR commonly hashes the artifact
bytes directly with SHA-256. TradeTrust's exact calculation depends on the
document generation and may involve a credential proof, checksum, target hash,
or Merkle root.

These values should not be assumed to be interchangeable merely because they
ultimately use SHA-256. Canonicalization, wrapping, selective disclosure, and
Merkle construction can produce different identifiers for apparently similar
content.

### Cryptographic identifiers are not legal identities

A TradeTrust blockchain address, DID verification method, or OpenETR
Key-Based Identifier proves control of verification material. It does not, by
itself, prove that the controller is a particular carrier, bank, warehouse,
government, individual, or autonomous agent.

Both systems require external mechanisms such as onboarding, DNS control,
registries, attestations, contracts, KYC, institutional governance, or law to
recognize the actor and its authority.

### Independent verification is a common objective

TradeTrust documents can be verified by compatible viewers and libraries
outside the issuing platform. OpenETR DCRs can be reconstructed and evaluated
by conforming verifiers outside the application that originated the events.

The systems differ in the dependencies needed to reproduce the answer, not in
the value they place on cross-platform verification.

## Detailed Comparison

| Concern | TradeTrust | OpenETR |
| --- | --- | --- |
| Primary domain | Digital trade documents, especially verifiable and transferable records. | General consequential records with domain adapters, initially including warehouse receipts and bills of lading. |
| Core portable object | Verifiable TradeTrust document plus status references. | Digest-identified Digital Artifact plus its signed DCR evidence. |
| Content integrity | VC proof or version-specific OpenAttestation wrapping and Merkle evidence. | Recomputed artifact digest plus signed record integrity. |
| Issuer/source | DID or DNS-based identity method, document proof, and where applicable a registry contract. | Anchor signer KBI plus optional profiles, attestations, registries, and recognition policy. |
| Transfer representation | Token Registry and Title Escrow contracts maintain owner and holder state. | Signed transition evidence is linked into the DCR; rules derive controller and lifecycle state. |
| State authority | Accepted blockchain and contract state. | Validated evidence plus identified derivation rules. |
| Ordering | Blockchain transaction ordering and contract execution. | Explicit cryptographic links, signed timestamps, and verifier conflict rules; no universal global order is presumed. |
| Invalid attempt | Usually rejected by contract and does not update contract state, though the attempted transaction may remain observable. | Signed statement may remain visible; the verifier excludes it or reports warnings and conflicts. |
| Competing history | Resolved within the selected chain's consensus and contract state. | Preserved as candidate branches or competing anchors and evaluated under policy. |
| Identity primitive | Wallet address, DID verification method, domain binding, and contract roles. | Actor-neutral KBI; current Nostr binding uses a 32-byte public key / `npub`. |
| Recognition | Law, platform rules, issuer identity, governance, and relying-party policy still determine effect. | Explicitly outside the protocol; recognition profiles, institutions, agreements, and law determine effect. |
| Retrieval dependency | Document plus access to relevant DID/DNS resources and, for transferable status, the selected blockchain and contracts. | Artifact plus sufficient signed DCR evidence and the identified rules; evidence may come from relays, archives, applications, or local packages. |
| Common runtime | EVM-compatible network and deployed contract interfaces for the transferable-record model. | No shared execution environment; verifiers reproduce a rules-based result from the evidence. |
| Fees and operations | Gas, wallet custody, contract deployment, network selection, and chain indexing are operational concerns. | Relay/storage policy, event retention, key custody, evidence completeness, and verifier-version governance are operational concerns. |
| Privacy | Business data remains in the document; public token activity and addresses can reveal transaction metadata. Selective disclosure is supported for applicable document formats. | Artifact content can remain off-relay; public events may still expose participants, action types, timing, and graph relationships unless private transport or minimization is used. |
| Upgrades | Contract, schema, library, chain, and identity-method evolution must be governed. | Wire format, action semantics, and rule-book versions must be governed while preserving old evidence. |
| Failure posture | Chain or node access, contract availability, and external identity resources can affect live verification. | Relay failure need not become state failure if a complete evidence package or archive is available; missing evidence remains a verification risk. |

## What Blockchain Adds In TradeTrust

It would be inaccurate to describe the blockchain as merely an expensive place
to store a hash. In TradeTrust's transferable-record model it contributes
substantive properties:

1. **Shared transaction ordering.** Participants use the chain's consensus
   history rather than negotiating their own ordering of concurrent actions.
2. **A common state machine.** Deployed contract code accepts or rejects state
   transitions and exposes a common current owner and holder state.
3. **Atomic authorization checks.** A transition updates state only if the
   caller and current contract conditions satisfy the programmed rules.
4. **A durable transaction history.** Public-chain replication makes accepted
   transactions broadly observable and difficult for one platform to erase.
5. **Established infrastructure.** Wallets, node providers, explorers,
   indexers, contract tooling, and EVM integration are already available.

These properties are valuable when participants accept the selected chain,
contract family, fee model, governance, and meaning of the resulting token
state.

Blockchain does not, by itself:

- prove the truth of the off-chain document data;
- prove the legal identity or authority of a wallet controller;
- guarantee confidentiality;
- determine which law applies;
- ensure that physical goods exist or have moved; or
- guarantee legal recognition of the technical owner or holder state.

Those conclusions still require evidence and institutions outside the chain.

## Blockchain Consensus Versus Relay Replication

The infrastructure models differ at a more fundamental level than where data
is stored. A blockchain is a shared execution and consensus environment. A
relay is a transport and storage service for independently signed records.

In the TradeTrust transferable-record model, participants submit transactions
to a selected blockchain. Validators or other block producers order those
transactions, execute the Token Registry and Title Escrow contracts, and
replicate the resulting contract state. Applications normally wait for block
inclusion and an appropriate degree of finality before treating a transition
as settled.

```text
proposed transaction
  -> blockchain submission
  -> ordering by the network
  -> smart-contract execution
  -> block inclusion and finality
  -> updated owner / holder state
```

In OpenETR, a signer creates a self-contained record. Its event id commits to
the record data and its signature makes the statement attributable. The same
record can then be published to one relay, many relays, a private relay, an
application store, an archive, or a directly exchanged evidence package.

```text
signed OpenETR record
  -> public relay A
  -> public relay B
  -> private institutional relay
  -> application database
  -> local evidence package
```

Replication does not create a new OpenETR record. Byte-identical copies retain
the same event id and signature and can be verified without trusting the
storage provider. A relay acknowledgement means that a relay reports accepting
the record for storage; it is not a consensus vote, a validity judgment, or a
determination of legal effect.

No single common relay is required. Participants need a way to obtain a
sufficiently complete set of signed evidence, not agreement on one storage
operator. They may use overlapping relay pools, exchange event packages
directly, or preserve records in local and institutional archives.

This yields a useful infrastructure principle:

> OpenETR requires common evidence conventions, not common state
> infrastructure.

### Publication and settlement

An OpenETR record is cryptographically complete when it has been signed. A
recipient can validate it immediately after receiving it, without waiting for
miners, validators, block production, transaction confirmation, or network
finality. Publication can therefore avoid blockchain gas fees and confirmation
latency.

That does not mean the resulting Consequential State is globally final. A
verifier may later discover additional valid evidence, a competing branch, a
prior undiscovered encumbrance, or a record that changes the derived state.
OpenETR finality is consequently a policy and evidence-completeness question,
not a property supplied by relay infrastructure.

The distinction is:

```text
record finality
  the signed bytes, event id, and signature are fixed

state finality
  the recognizing party determines whether the evidence set is sufficiently
  complete and the derived result sufficiently settled for its purpose
```

A recognition profile may impose operational safeguards such as querying
several relays, waiting for a stated observation period, requiring both parties
to sign a transfer, consulting an institutional archive, or obtaining an
attestation from an accepted registry. These are disclosed reliance rules,
not hidden consensus assumptions.

### Infrastructure comparison

| Concern | Blockchain and smart contracts | OpenETR relays and evidence stores |
| --- | --- | --- |
| Primary function | Order transactions, execute shared code, and maintain replicated contract state. | Receive, store, replicate, and return independently signed records. |
| Source of authority | Accepted chain history and deployed contract state. | Record signatures, graph relationships, and the verifier's identified rule book. |
| Common infrastructure | Participants converge on a chain, contract addresses, and compatible execution environment. | Participants may use different or overlapping relays and archives if they can obtain the required evidence. |
| Transition admission | Contract execution accepts or rejects the proposed state change. | A relay may accept any well-formed record; the verifier determines whether it contributes to state. |
| Ordering | Consensus supplies a common transaction order within the selected chain. | Cryptographic references express claimed relationships; rule books resolve order, branches, and conflicts. |
| Confirmation | Applications wait for inclusion and an appropriate finality threshold. | A recipient can verify a signed record immediately; reliance may still require evidence-completeness checks. |
| Replication | Nodes reproduce the accepted chain and contract state. | The same signed records can be copied among relays, databases, archives, and evidence packages. |
| Cost | Deployment and transitions may require gas, wallet funding, and chain-specific operations. | No protocol-level gas fee; relay fees, hosting, archival, and operational costs may still apply. |
| Availability dependency | Current status normally requires access to the selected chain through a node or provider. | Any source holding sufficient evidence can support verification; no particular relay must remain available. |
| Conflict treatment | Chain consensus and contract rules select the accepted transition and state. | Conflicting statements may remain visible and are evaluated under verifier and recognition policy. |
| Censorship and admission | Network and contract rules govern transaction admission; public-chain distribution can resist control by one operator. | A relay can refuse or delete records, but signers can publish elsewhere and recipients can retain or exchange exact copies. |
| Local verification | A local node can independently reproduce chain state, but must track the selected blockchain. | A local verifier can evaluate a complete evidence package without a live relay connection. |
| Governance | Chain governance, contract administration, contract upgrades, and network economics matter. | Wire-format governance, rule-book versions, relay policy, evidence retention, and recognition governance matter. |

### Advantages of the blockchain approach

- It supplies one commonly ordered transaction history within the selected
  network.
- Smart contracts enforce transition rules before accepted state changes.
- Participants can query a common current state rather than reconcile
  separately collected evidence sets.
- Public-chain replication can make accepted history difficult for any one
  participant to suppress or rewrite.
- Existing wallets, contract tooling, explorers, node services, and indexers
  support integration and operations.

### Limitations of the blockchain approach

- Participants must accept the selected chain, contract family, addresses,
  fees, finality assumptions, and governance.
- State transitions incur blockchain submission and confirmation latency.
- Deployment and operation introduce wallet funding, gas management,
  contract-administration, and chain-specific expertise.
- Moving to another chain or contract version requires an explicit migration
  and continuity strategy.
- Public transaction history can expose addresses, timing, and commercial
  relationships even when document content remains off-chain.
- Consensus settles contract state, not the legal identity, authority, or
  recognition of the actors behind blockchain addresses.

### Advantages of the relay and signed-evidence approach

- Records can be created and verified without waiting for block production or
  consensus finality.
- The same evidence can be replicated across heterogeneous infrastructure
  without changing its identity.
- No relay, application, database, or archive has to remain the exclusive
  source of the evidence.
- Participants can operate public relays, private relays, local archives, or
  direct evidence exchange according to their confidentiality and resilience
  requirements.
- Verification can continue from a complete local evidence package if all live
  relay services are unavailable.
- Different recognizing parties can apply their own disclosed rule books to
  the same evidence without surrendering authority to one global state
  machine.
- Publication does not require blockchain gas or the deployment of a smart
  contract for each issuer ecosystem.

### Limitations of the relay and signed-evidence approach

- Relays do not supply global ordering, consensus, or conflict settlement.
- A verifier must assess whether its evidence set is sufficiently complete for
  the decision being made.
- Different evidence sets or rule books can produce different results, which
  makes disclosure of the derivation basis essential.
- Relay retention is not guaranteed unless archival and replication policy is
  deliberately implemented.
- Invalid, unauthorized, and conflicting signed statements can be published
  and must be identified by verifier rules.
- Institutions that require one globally enforced current state may prefer a
  common registry or smart-contract model.
- Rule-book governance and versioning become visible institutional
  responsibilities rather than being embedded solely in deployed contract
  code.

The OpenETR approach therefore shifts trust and authority away from a shared
state platform and toward the actors using the ecosystem. Each recognizing
party determines which evidence sources, signers, rule books, and recognition
criteria it accepts. That flexibility is a central design objective, but it
must be matched by transparent verifier output and disciplined evidence
preservation.

## Adoption And Integration Advantages Of A Lighter Protocol

OpenETR's infrastructure model can lower the threshold for adoption because
its cryptographic minimum is small. A participant does not need to join one
platform, operate a public website, maintain a DID document, deploy a smart
contract, fund a blockchain wallet, or adopt a shared identity-resolution
method before it can create and verify OpenETR evidence.

At the protocol level, a participant needs:

1. a signing key;
2. software that creates and verifies the OpenETR wire format;
3. the digest of the Digital Artifact;
4. a way to exchange or retrieve the signed evidence; and
5. an identified rule book appropriate to the relying purpose.

```text
create or select signing key
  -> identify artifact by digest
  -> create and sign record
  -> publish, store, or exchange evidence
  -> verify under an identified rule book
```

Websites, DNS, registries, organizational attestations, KYC services, and
institutional directories may still be valuable for recognition. They are not
mandatory components of the core cryptographic verification path.

### Self-verifying identifiers reduce bootstrap dependencies

An OpenETR Key-Based Identifier directly identifies the verification material
needed to check a signature. In the current Nostr binding, the public key in
hexadecimal or `npub` form can be used without resolving a separate identity
document.

```text
OpenETR KBI
  -> obtain public key directly
  -> verify event id and signature

did:web example
  -> resolve identifier through DNS and HTTPS
  -> retrieve DID document
  -> select verification method
  -> verify proof
```

This does not make OpenETR keys legal identities. It removes a resolution
dependency from cryptographic attribution. Recognition evidence can be added
where the relying party needs to know which organization, person, service, or
agent stands behind the key.

### Existing applications can hide the protocol surface

OpenETR is intended to sit behind existing account-based and domain-specific
applications. Users do not need to handle `nsec` values, event kinds, relay
filters, tags, signatures, or graph traversal.

An existing system can continue to provide:

- user accounts, SSO, passkeys, or multifactor authentication;
- internal roles, permissions, and approval workflows;
- document creation, storage, and delivery;
- customer, counterparty, inventory, shipment, or case records;
- KYC, licensing, and organizational authority checks; and
- the domain vocabulary used by its staff and customers.

The application maps those established controls to OpenETR operations:

```text
Existing application
  user account + authentication
  role and authorization policy
  domain document and workflow
          |
          v
OpenETR integration boundary
  select Commitment Profile
  calculate artifact digest
  create and sign DCR record
  publish to configured evidence stores
  retrieve DCR evidence
  invoke deterministic verifier
          |
          v
Application presentation
  Issue Receipt
  Transfer Control
  Accept Transfer
  Record Encumbrance
  Verify Current State
```

The user sees meaningful business actions. The application protects the key
and performs protocol operations in the background, much as a passkey-enabled
application uses device-held cryptographic material without showing the
private key to the user.

The application's authentication and authorization remain important. If the
application signs an OpenETR record after an unauthorized user action, the
signature can prove which Commitment Profile made the statement but cannot
repair the application's access-control failure.

### Documents do not have to be created by OpenETR

An organization can keep its existing document-generation process. A
warehouse system may continue generating PDF receipts; a carrier may continue
producing bills of lading; a government system may continue issuing its
existing digital forms.

OpenETR can begin after the artifact is finalized:

```text
existing document system
  -> final PDF, JSON, credential, or canonical artifact
  -> SHA-256 digest
  -> OpenETR Anchor Record
```

This reduces migration scope. The first integration does not have to replace
the document-management system, redesign the artifact schema, or move document
content into a new platform. OpenETR introduces a portable consequential
evidence layer beside the existing system.

### Multiple integration surfaces support incremental adoption

An organization can adopt OpenETR at the level that fits its architecture:

| Integration surface | Appropriate use |
| --- | --- |
| Python component | Embed signing, querying, graph reconstruction, and verification in an existing Python service. |
| REST API | Keep OpenETR behind a separately operated service and call it from existing applications. |
| CLI with JSON output | Integrate from shell scripts, batch processes, workflow engines, and agent-operated tools. |
| Wire-format implementation | Implement the signed record format directly in another language or infrastructure stack. |
| Evidence package | Exchange and verify a bounded record set without requiring live access to a particular relay or API. |

This permits a staged adoption path:

1. create evidence records from an existing application;
2. publish redundantly to configured relays or archives;
3. expose verification results to internal users;
4. exchange evidence with selected counterparties;
5. agree on a domain rule book for a pilot; and
6. add institutional or legal recognition arrangements as the use case
   matures.

Participants do not all have to migrate their internal systems at the same
time. One participant may use the Python component, another may call a managed
API, and another may implement the wire format directly. Their common
dependency is the evidence convention, not the application stack.

### Lower coordination burden

Blockchain-based transferable records require participants, directly or
through their service providers, to converge on network support, contract
interfaces, wallet operations, transaction funding, and finality assumptions.
A DID-based issuance model may additionally require agreement on supported
methods and reliable resolution infrastructure.

OpenETR still requires coordination, but over a narrower surface:

- artifact-identification rules;
- signed record shapes and action semantics;
- evidence discovery and retention expectations;
- verifier rule-book identifiers and versions;
- recognized signers and authorities; and
- the legal or institutional effect given to results.

This narrower technical dependency can make bilateral pilots, sector
experiments, and cross-jurisdictional integrations easier to begin. Parties can
first prove that they can exchange and independently verify the same evidence,
then progressively formalize recognition.

### Adoption comparison

| Adoption concern | TradeTrust transferable-record implementation | OpenETR |
| --- | --- | --- |
| End-user website | A platform can hide the technical details; a particular public website is not inherently required. | No website is required by the protocol; existing applications or local tools can create and verify records. |
| Identifier setup | Issuer identity may involve DID or DNS-based configuration; transferable operations use blockchain addresses. | A signing key immediately supplies a self-verifying KBI; richer identity and recognition are optional layers. |
| Shared infrastructure | Requires a supported blockchain, deployed contracts, node access, and compatible contract tooling. | Requires access to sufficient signed evidence, which may be replicated across unrelated relays, archives, or direct packages. |
| Issuance setup | Document protection, identity configuration, token-registry deployment, wallet funding, and blockchain issuance may be involved. | Hash the existing artifact, sign an Anchor Record, and publish or exchange it. |
| User key exposure | A platform can custody wallets and hide blockchain operations from users. | An application can custody Commitment Profile keys and expose only domain actions. |
| Participant migration | Participants need compatible support for the selected TradeTrust document and contract environment. | Participants may use different implementations if they produce and verify the same evidence conventions. |
| Recognition | Identity, authority, reliable method, and legal effect still require governance. | The same concerns remain explicitly external and can be introduced according to domain and jurisdiction. |

TradeTrust can provide an excellent user experience through managed platforms,
and ordinary holders need not personally deploy contracts or operate DID
websites. The OpenETR claim is narrower: those facilities are not required by
the underlying OpenETR verification model. An integrator may use them, replace
them, or omit them according to the recognizing parties' needs.

### Adoption risks that remain

A lighter protocol does not make institutional adoption automatic. OpenETR
implementers must still address:

- secure generation, custody, rotation, recovery, and revocation of signing
  keys;
- authorization controls governing when an application may use a Commitment
  Profile;
- durable evidence replication and retention;
- evidence-completeness checks and relay discovery;
- deterministic, versioned, and testable rule books;
- intelligible warnings and derivation explanations;
- privacy and commercial metadata exposure;
- interoperability testing among independent implementations; and
- the recognition arrangements that connect keys and derived state to real
  institutional or legal effect.

The adoption advantage is therefore not an absence of governance. It is the
ability to begin with a small, implementation-neutral cryptographic core and
add the governance required by each context without first imposing one global
platform, identity method, or state machine on every participant.

## What OpenETR Changes

### Evidence is authoritative; no execution environment is exclusive

OpenETR makes signed DCR evidence and identified rules sufficient to reproduce
the protocol result. A verifier does not need to ask one database, platform,
contract instance, or blockchain for an authoritative mutable status value.

This is the practical meaning of the OpenETR maxim that system failure need
not become state failure. It is not a claim that infrastructure is unnecessary.
The verifier still needs the artifact, a sufficiently complete evidence set,
the rule-book version, and cryptographic software.

### Conflict is represented rather than globally settled

OpenETR does not provide blockchain consensus. Two signers may publish
conflicting events, two candidate anchors may concern the same artifact, or an
unauthorized party may publish a well-formed claim. The evidence remains
visible. A verifier applies structural rules and recognition policy, emits
warnings, and identifies the branch or result it accepts.

This approach is appropriate where different relying parties may legitimately
apply different rules. It is less appropriate where all participants require
one globally enforced current state and do not want to operate a conflict
resolution policy.

### Rules are portable and plural

OpenETR rule books can be implemented by different organizations and compared
against the same evidence. A generic baseline can be supplemented by an MLWR,
MLETR, institutional, contractual, or jurisdiction-specific policy.

The benefit is policy transparency and plurality. The cost is that governance
must specify which rule book, version, evidence-completeness assumptions, and
recognition profile were used.

### The protocol can sit behind ordinary accounts

An enterprise application can authenticate users through SSO, passkeys, local
accounts, or another established mechanism and map permitted actions to
OpenETR Commitment Profiles. The application may hide key custody in the same
way that many systems hide device or wallet keys while exposing meaningful
business roles.

TradeTrust can also be integrated behind ordinary application accounts, but
its transferable-record operations ultimately invoke blockchain accounts and
contract functions. OpenETR's protocol result does not require a blockchain
transaction.

## Comparative Transfer Example

Consider a bill of lading initially controlled by Alice, with Charlie as owner,
that is placed in Bob's holdership and later transferred to a new owner.

### TradeTrust flow

1. The document is created and cryptographically protected.
2. Its transferable-record status identifies a blockchain, Token Registry,
   and token id.
3. The Token Registry and Title Escrow establish the initial owner and holder.
4. The authorized holder calls the applicable change-holder function.
5. The owner may nominate a new owner.
6. The holder endorses the nominated transfer where the contract conditions
   are satisfied.
7. After transaction confirmation, the contract exposes the new owner and
   holder state.
8. Surrender or return is handled through the contract lifecycle.

The verifier checks the document's cryptographic integrity and source, then
reads the identified blockchain and contract state.

### OpenETR flow

1. The artifact bytes are hashed and an issuer signs an Anchor Record.
2. The current controller signs a transfer-initiation Evidence Record naming
   the proposed recipient.
3. The recipient signs an acceptance Evidence Record linked to the relevant
   prior record.
4. Encumbrance, discharge, surrender, redemption, change of medium, or
   termination can be expressed as later signed records.
5. Each Evidence Record identifies the same artifact and links through exact
   cryptographic event ids.
6. A verifier obtains the relevant records, validates the DCR, and applies an
   identified rule book.
7. The verifier reports the derived controller and lifecycle state together
   with warnings, conflicts, and its recognition basis.

OpenETR's generic model does not assume that legal ownership and possession
must always be represented by one `controller` field. A bill-of-lading domain
profile could derive owner, holder, controller, or other domain roles from the
same evidence family where the governing rules require those distinctions.

### The essential contrast

```text
TradeTrust
authorized transaction -> contract execution -> globally shared chain state

OpenETR
attributable statement -> DCR evidence -> policy evaluation -> derived state
```

## Verification At Time Of Performance

TradeTrust reduces reliance on a single trade platform, but transferable-state
verification still normally depends on being able to resolve the relevant
chain and contract state. A local blockchain node can reduce dependence on a
third-party RPC provider, but it does not eliminate dependence on the chosen
blockchain history and contract environment.

OpenETR is designed so that a complete evidence package can be verified
locally. Public or private relays are convenient discovery and replication
infrastructure, not the sole authority. An archive can preserve the artifact,
DCR records, rule-book identifier, and supporting recognition evidence for
later evaluation.

The OpenETR advantage is therefore not "offline by default." It is that live
access to someone else's application, API, relay, or smart contract need not
be a permanent condition of verification once sufficient evidence has been
acquired.

## Privacy And Commercial Confidentiality

Neither architecture makes public infrastructure automatically private.

TradeTrust can keep document contents off-chain, and applicable VC formats can
support selective disclosure. Yet token transactions, contract addresses,
wallet addresses, and timing may be public and linkable.

OpenETR can keep document contents out of public events and use private relays,
restricted evidence packages, encryption, or minimal public tags. Yet public
events can reveal counterparties, action types, timing, and graph shape.

Implementers in either model should perform metadata threat modelling rather
than equating "hash only" or "off-chain document" with confidentiality.

## Legal Recognition

TradeTrust is expressly designed for digital trade and aligns its transferable
record approach with concerns such as integrity, singularity, and exclusive
control under MLETR-style laws. That focus, its legality materials, and its
reference implementation provide a strong adoption story.

OpenETR takes a more general and deliberately narrower protocol position. It
supplies end-verifiable evidence and derivable Consequential State. A domain
profile may map that evidence to MLETR, MLWR, UCC Article 12, or another legal
regime, but the generic protocol does not declare the legal conclusion.

In both systems, legal effect depends on more than cryptographic correctness.
Applicable law, reliable-method analysis, actor authority, system governance,
operational controls, and the facts of the transaction remain relevant.

## Choosing An Architectural Pattern

TradeTrust is a strong fit where:

- the use case is digital trade;
- participants accept a supported blockchain and contract model;
- a shared owner/holder state machine is desirable;
- transaction ordering should be settled by blockchain consensus;
- EVM wallets, contracts, and indexing fit the operating environment; and
- alignment with the TradeTrust ecosystem and reference implementation is
  strategically valuable.

OpenETR is a strong fit where:

- the same evidence must survive across multiple systems and policy contexts;
- participants cannot or do not wish to select one shared blockchain runtime;
- signed claims and conflicts should remain independently inspectable;
- verifiers need to reproduce state locally from portable evidence;
- existing account systems should hide protocol keys behind domain roles;
- several domains or jurisdictions require different rule books; or
- the architecture must remain neutral about recognition and legal effect.

A conventional database remains a strong fit where all participants accept one
operator, cross-platform independent verification is not required, and the
operator's availability and governance are acceptable. OpenETR does not imply
that every workflow needs a public protocol.

## Coexistence And Bridging

The architectures can complement one another:

- an OpenETR Anchor Record can identify a TradeTrust document artifact;
- an OpenETR Evidence Record can attest to a verification result observed from
  a TradeTrust contract at a stated block height;
- a TradeTrust platform can publish OpenETR records as portable evidence for
  cross-system or non-contract actions;
- an OpenETR recognition profile can require current TradeTrust contract state
  before accepting a transition;
- a migration package can preserve relevant contract transactions and
  verification evidence in a DCR-oriented archive; and
- a domain application can support both models while presenting one business
  vocabulary to its users.

Any bridge must state clearly which system is authoritative for each result.
Mirroring state without a declared precedence rule can create two competing
answers rather than interoperability.

## Policy Implications

Public authorities and industry consortia should avoid treating "blockchain"
or "no blockchain" as the policy outcome. They should ask which properties
the use case actually requires:

1. Is one common transaction order necessary, or are attributable records and
   explicit conflict rules sufficient?
2. Must the transition be rejected before publication, or may an invalid claim
   remain visible and be excluded by verifiers?
3. Can all parties accept one chain, contract family, fee model, and upgrade
   process?
4. What evidence must remain verifiable if platforms, RPC services, relays,
   renderers, DNS entries, or vendors disappear?
5. How are cryptographic identifiers mapped to recognized organizations and
   authorized roles?
6. Which rule book determines the state, and how is its version disclosed?
7. Which metadata may become public even when document content remains
   private?
8. What law or institutional policy gives the technical result effect?

Procurement and regulation should specify these functional requirements before
mandating a particular ledger technology.

## Design Takeaway For OpenETR

TradeTrust demonstrates the value of portable document verification, explicit
transfer roles, mature tooling, and a common state machine for digital trade.
OpenETR should learn from those strengths without copying blockchain-specific
assumptions into its core.

The comparison sharpens the OpenETR design claim:

> OpenETR makes consequential evidence portable so that independently operated
> systems can reproduce what follows without giving one application, database,
> service, platform, or blockchain exclusive ownership of the result.

That claim creates corresponding obligations for OpenETR:

- evidence completeness must be assessable;
- graph conflicts must be visible;
- rule books must be identified and versioned;
- verifier output must explain its basis;
- key and profile governance must be operationally credible;
- privacy must be designed rather than assumed; and
- domain profiles must express relevant legal and business distinctions
  without turning the generic protocol into a legal oracle.

## Conclusion

TradeTrust and OpenETR are two serious responses to the same underlying
problem: a consequential digital record should remain verifiable and usable
across systems that do not share one application database.

TradeTrust uses verifiable-document technology plus blockchain smart contracts
to produce a shared transferable-record state. OpenETR uses a digest-identified
artifact, signed DCR evidence, and identified rules to produce reproducible
Consequential State.

TradeTrust makes a blockchain-backed state accessible across compatible
platforms.
OpenETR makes the evidence for deriving state portable across independently
operated systems and policy contexts.

The practical choice is not between modernity and obsolescence, nor between
trust and no trust. It is a choice about where rules execute, how conflicts are
resolved, which infrastructure must remain available, and who is permitted to
determine what follows.

## Sources

- [TradeTrust: What Is TradeTrust](https://www.tradetrust.io/about/what-is-tradetrust/)
- [TradeTrust Documentation](https://documentation.tradetrust.io/)
- [TradeTrust Document Schema](https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/w3c-vc/tradetrust-document-schema)
- [TradeTrust Document Integrity](https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/w3c-vc/verifying-documents/document-integrity/)
- [TradeTrust Transferable Records Overview](https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/transferability/overview/)
- [TradeTrust Title Transfer Example](https://docs.tradetrust.io/docs/4.x/topics/introduction/transferable-records/title-transfer-example/)
- [TradeTrust Token Registry](https://docs.tradetrust.io/docs/4.x/tutorial/transferable-records/token-registry/token-registry-cli/)
- [TradeTrust Document Preview](https://docs.tradetrust.io/docs/introduction/key-components-of-tradetrust/add-ons/document-preview/)
- [TradeTrust Security And Authenticity](https://www.tradetrust.io/solution/security-and-authenticity/)
- [OpenETR Digital Controllable Record Design Note](./DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
- [OpenETR Nostr Wire Format](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [OpenETR Consequential State Architecture](./CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
