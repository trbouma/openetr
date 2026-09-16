# OpenETR And Spherity M-Trust Architecture Analysis Note

This note reviews Spherity's paper *Beyond Single-Enterprise ZTA: Multi-Trust
Architectures for Authorised Agentic Actors in Open, Cross-Domain Ecosystems*
and its reference architecture for verifiable agentic networks.

The paper addresses a problem that sits immediately before many OpenETR
actions: how a relying system determines whether an AI agent is currently
authorized to perform a particular action across organizational, sectoral, or
jurisdictional boundaries.

OpenETR addresses a different but adjacent problem: how evidence of a
consequential action concerning a Digital Artifact can remain end-verifiable,
and how defined rules derive consequential state from that evidence.

The two approaches are complementary. Spherity's architecture can help answer
whether an action should be permitted. OpenETR can help preserve what happened
to the record and what state follows from it.

## Status

Draft analysis note.

## Sources Reviewed

- Dr. Carsten Stöcker, [*Beyond Single-Enterprise ZTA: Multi-Trust
  Architectures for Authorised Agentic Actors in Open, Cross-Domain
  Ecosystems*](https://spherity.github.io/spherity-research/beyond-zero-trust-m-trust-authorised-agentic-actors.html),
  Spherity GmbH, 16 September 2026.
- [Full research
  paper](https://spherity.github.io/spherity-research/Spherity-Beyond-Single-Enterprise-ZTA-Multi-Trust-Architectures-for-Authorised-Agentic-Actors.pdf).
- Spherity's [reference architecture for verifiable agentic
  networks](https://spherity.github.io/spherity-research/beyond-zero-trust-m-trust-authorised-agentic-actors.html#reference-architecture).

The paper is an architectural and standards-gap analysis. Its eight-layer
reference architecture is a proposal by the author, not an adopted standard or
evidence of deployed interoperability. The paper makes that limitation clear.

## Executive Assessment

Spherity extends the Zero Trust question from:

```text
May this subject access this enterprise resource now?
```

to a cross-domain agentic question:

```text
May this agent perform this specific action, for this principal,
for this purpose, within this scope, under current conditions?
```

Its proposed answer combines:

- legal-person and representative identity;
- Business and Agent Wallets;
- verifiable credentials and decentralized identifiers;
- a current, bounded Power of Attorney or other delegation;
- AI service, testing, runtime, and attestation evidence;
- source-domain trust registries and credential status;
- a local Policy Decision Point (PDP);
- a Policy Enforcement Point (PEP); and
- a signed action receipt after execution.

OpenETR should not duplicate those functions. It should accept their outputs as
authorization and recognition inputs where a domain requires them.

The most useful integration is:

```text
Spherity-aligned authority architecture
  establishes identity, mandate, current assurance, and permission
  ->
domain system and PEP
  execute the bounded action
  ->
OpenETR domain adapter
  records artifact-specific consequential evidence
  ->
OpenETR state transition rules
  derive consequential state
  ->
individual, community, institution, authority, or applicable law
  determines recognition and effect
```

This division avoids two category errors:

1. A valid mandate does not prove that a requested record transition actually
   occurred or determine the record's resulting state.
2. A valid OpenETR signature or graph does not prove that the signer had legal
   or organizational authority to act.

## The Paper's Core Contribution

The paper begins with GSMA Greater China's proposed M-Trust model. It describes
three dimensions:

- **Multi-party trust** combines evidence, endorsements, evaluators, and risk
  inputs from more than one party.
- **Agentic intent-aware trust** evaluates the proposed task, purpose, context,
  scope, and risk rather than authenticating an agent in the abstract.
- **Cross-domain trust** allows evidence to move among independently governed
  trust domains while each receiving verifier retains its own decision
  authority.

Spherity identifies a gap between this technical model and legally attributable
B2B or B2G action. It therefore adds legal-person identity, organizational
representation, Business Wallets, verifiable delegation, AI Service Passports,
current status, local policy enforcement, and signed action receipts.

The result is an eight-layer reference architecture designed to produce
**transient cross-domain trust**. The trust is transient because it is composed
for one transaction, purpose, audience, and time window. Source domains retain
authority over their claims, and the receiving verifier retains sovereignty
over the authorization decision.

That is a strong match for OpenETR's recognition boundary. OpenETR does not need
one global identity root or one universal recognition decision. Different
verifiers can evaluate the same end-verifiable evidence using different trusted
issuers, status sources, rule books, and legal contexts.

## The Core Relationship

The architectures focus on different objects.

| Question | Spherity M-Trust architecture | OpenETR |
| --- | --- | --- |
| Primary subject | Agent, principal, mandate, service, and requested action | Digest-identified Digital Artifact and its DCR |
| Primary decision | Is this action currently authorized? | What consequential state follows from valid evidence under defined rules? |
| Time orientation | Transaction-time and continuously evaluated | Lifecycle evidence and reproducible state derivation |
| Main evidence | Identity, credentials, delegation, status, runtime assurance, policy decision | Signed Anchor and Control Events, prior-event links, linked evidence |
| Enforcement | PDP, PEP, connector, gateway, or controlled system | Host system and domain adapter gate publication and effect |
| Durable output | Signed action receipt and audit trail | Digital Controllable Record and derived consequential state |
| Final authority | Local relying verifier | Recognition remains with the relevant person, community, institution, authority, or law |

The connecting point is a consequential action concerning a Digital Artifact.

An authorization decision is an input to that action. It is not automatically
the action itself. An action receipt is evidence of execution. It is not
automatically an OpenETR Control Event or proof of a particular consequential
state.

The applicable domain adapter must determine the mapping.

## A Terminology Trap: Two Meanings Of Control

Spherity uses **control plane** primarily for organizational identity,
delegation, authorization, policy decision, and enforcement. It asks who may do
what under current conditions.

OpenETR uses **control layer** for artifact-centric evidence and state
transitions. It asks what has happened to a Digital Artifact and what state
follows under the rules.

These meanings are related but not interchangeable.

```text
Spherity control plane:
  authority to perform an action

OpenETR control layer:
  consequential evidence and state concerning an artifact
```

Integration documents should qualify the term rather than simply saying
"control." Useful labels are:

- **authority control plane** for identity, mandate, PDP, and PEP functions;
- **record control layer** for OpenETR DCR evidence and state derivation.

This distinction also protects OpenETR's boundary. OpenETR does not become an
identity wallet, access-management platform, or universal policy engine merely
because both architectures discuss control.

## Mapping The Eight Layers

### 1. Governance And Trust

Spherity includes law, rule books, reciprocal recognition, issuer
accreditation, trust registries, and semantic governance.

For OpenETR, these are recognition and domain-policy inputs. They may determine:

- which issuers or profile keys are accepted;
- which actions require a particular role or licence;
- which domain adapter and transition rules apply;
- whether an action has contractual, institutional, or legal effect; and
- which jurisdiction's rules govern the record.

OpenETR should reference these inputs without embedding one governance regime in
the base protocol.

### 2. Organizational Identity

Spherity proposes Business Wallets containing register-backed legal-person,
representation, role, licence, and vLEI evidence.

OpenETR remains actor-neutral. A protocol signature establishes that a key
signed an event. It does not establish that the key belongs to a legal person,
that the operator held a corporate role, or that a representation right was
current.

Organizational credentials can therefore be:

- checked by the host system before permitting a signature;
- summarized in the authorization decision receipt;
- linked as evidence by digest or privacy-preserving reference; and
- evaluated again by a verifier when the recognition context requires it.

### 3. Agent Identity And Delegation

Spherity connects an Agent Wallet or workload identity to a task-bounded Power
of Attorney or capability.

This complements OpenETR's distinction among principal, operator, and signer:

```text
principal:
  the person or organization on whose authority the action is performed

operator:
  the agent, service, person, or workflow that initiates or executes it

signer:
  the key or signing service that signs the OpenETR event
```

The three may be different. A verifier should not infer their relationship from
the event signature alone.

### 4. AI Service Assurance

The AI Service Passport, testing, evaluation, verification and validation
(TEVV), incident status, runtime controls, and monitoring describe the system
that operates the agent.

These are important authorization inputs for high-impact actions, but they are
not intrinsic properties of a Digital Artifact or its DCR. OpenETR can link to
a versioned assurance snapshot when a domain requires proof of the system state
under which an action occurred.

### 5. Data And Product Evidence

This is the closest architectural overlap. Spherity proposes verifiable
evidence graphs for product, provenance, conformity, testing, and operational
claims. OpenETR provides an artifact-centric DCR: one end-verifiable record or a
graph of records concerning a digest-identified Digital Artifact.

The graphs should not be collapsed without a profile. A broad evidence graph
may contain many claims and relationships that do not change OpenETR
consequential state. A DCR includes only the records that the applicable
OpenETR rules evaluate for that artifact, together with linked evidence needed
by policy.

OpenETR can therefore serve as a consequential-state subgraph within a wider
industrial evidence graph.

### 6. Decision And Enforcement

Spherity's PDP evaluates identity, mandate, source-domain evidence, purpose,
runtime context, and local policy. Its PEP prevents execution unless the
decision permits it.

OpenETR benefits when that enforcement occurs before a consequential event is
signed or published.

```text
weak integration:
  agent acts -> system logs an OpenETR event later

strong integration:
  agent proposes -> PDP authorizes -> PEP constrains execution
  -> OpenETR event is signed at commitment -> domain system gives effect
```

The OpenETR verifier may later evaluate linked authority evidence, but it is not
a substitute for non-bypassable transaction-time enforcement.

### 7. Registry And Cryptographic Resilience

Spherity includes VDRs, trust registries, credential status, DIDs, optional
distributed ledgers, trusted execution, remote attestation, cryptographic
agility, and post-quantum migration.

OpenETR's Nostr relays distribute signed events. Relays do not replace issuer
registries, credential status services, legal-entity registers, or trust lists.
Conversely, those registries do not replace the OpenETR event graph.

Both architectures require algorithm agility and durable verification. A
complete migration plan must cover event signatures, credentials, identifiers,
status evidence, timestamps, transport, archived evidence, and any long-lived
integrity commitments.

### 8. Accountability Evidence

Spherity's signed action receipt is the most direct integration artifact. It
can preserve:

- the requested action and purpose;
- principal, agent, and workload references;
- the applicable mandate and scope;
- credential and status references;
- the policy version and decision;
- relevant runtime or assurance evidence;
- the enforcement result;
- a timestamp and transaction identifier; and
- the execution result.

OpenETR should treat the receipt according to its function:

| Receipt function | OpenETR treatment |
| --- | --- |
| Proves why an action was authorized | Linked evidence |
| Proves execution details without changing artifact state | Linked evidence |
| Is itself the domain-defined consequential act | Candidate Control Event or payload referenced by one |
| Supports later recognition but contains sensitive data | Private evidence with a digest, commitment, or controlled reference in the DCR |

Calling every action receipt a Control Event would overload the state graph.
Calling every receipt mere logging would lose the cases where the receipt is
the authoritative expression of a consequential act. The domain adapter must
make the distinction explicit.

## Canonical End-To-End Transaction

A combined transaction should proceed as follows.

1. An agent proposes a specific action concerning a digest-identified Digital
   Artifact.
2. The gateway identifies the required legal-person, representative, agent,
   delegation, role, assurance, and domain evidence.
3. Business and Agent Wallets present the required credentials and mandate.
4. The local verifier resolves issuer authority, credential status, semantic
   profiles, runtime evidence, and the current OpenETR graph state.
5. The PDP evaluates the request under current policy and produces a bounded,
   time-specific authorization decision.
6. The PEP permits only the authorized capability.
7. At the point of commitment, the designated signer creates the appropriate
   OpenETR event for the Digital Artifact.
8. The gateway produces a signed action receipt that binds the authorization
   decision, execution result, and OpenETR event identifier.
9. The event and non-sensitive evidence are published; sensitive evidence is
   retained privately with verifiable references or commitments.
10. OpenETR validation checks the DCR evidence, and defined transition rules
    derive consequential state.
11. A relying person, community, institution, authority, or applicable law
    determines whether to recognize the state and what effect it should have.

This sequence preserves four separate decisions:

```text
proposal      what the agent requests
authorization whether the request may proceed
consequence   what state follows from the signed evidence
recognition   whether and how that state is accepted or given effect
```

## Binding Authorization To Consequence

The main integration risk is a time-of-check to time-of-use gap. An agent may be
authorized against one record state but sign an event after the record,
mandate, credential status, policy, or runtime condition has changed.

A robust transaction should bind the authorization decision to:

- the artifact digest;
- the proposed OpenETR action;
- the expected prior event or graph head;
- the principal, operator, and signer references;
- the mandate identifier, scope, audience, and expiry;
- the verifier and policy version;
- the relevant credential-status snapshot;
- the assurance or runtime snapshot where required;
- the request and transaction identifiers;
- the maximum authorization-to-signing interval; and
- the resulting OpenETR event identifier and execution result.

If the expected graph head or another material input changes, the system should
re-authorize rather than reuse the prior decision.

## Transient Trust And Durable Consequential State

The paper's **transient cross-domain trust** is intentionally short-lived. It
answers whether evidence from several source domains is acceptable for one
decision now.

OpenETR's DCR is intended to remain verifiable after that transaction context
has passed. This is a valuable division:

```text
transient trust:
  enough current authority and assurance to permit one action

durable evidence:
  enough signed, linked evidence to reconstruct the consequential record state
  after the original application, session, or trust decision is unavailable
```

Durability does not mean that every upstream credential remains valid forever.
The record should preserve what was checked, by whom, under which policy, and at
what time. A later verifier can then distinguish historical authorization from
current authority.

## Wallets And Graphs

Business and Agent Wallets are primarily controlled containers and presentation
agents for credentials, keys, mandates, and proofs. Their contents may be
selectively disclosed for a particular transaction.

OpenETR is an open evidence graph concerning an artifact. It is designed so
that a verifier can reconstruct signed lifecycle evidence without depending on
the wallet or application that participated in the original transaction.

The relationship is:

```text
wallet:
  presents current identity, role, delegation, and assurance evidence

OpenETR graph:
  preserves artifact-specific evidence of consequential actions and state
```

Neither replaces the other.

## Verifier Sovereignty And Recognition

Spherity's verifier-sovereign model aligns with OpenETR's separation of
protocol correctness from recognition.

An OpenETR verifier can establish that:

- an event is correctly signed;
- the event concerns a particular artifact digest;
- the event links to the expected prior evidence;
- the DCR satisfies the applicable structural rules; and
- defined transition rules produce a candidate consequential state.

The Spherity-aligned authority layer can provide evidence that:

- the principal and representative were identified;
- the agent held a current, bounded mandate;
- required credentials and service assurances were current;
- the local policy permitted the action; and
- the PEP executed the permitted operation.

The relying context still decides whether those issuers, rules, decisions, and
events are recognized and what real-world effect follows.

## Privacy And Selective Disclosure

The combined architecture can expose sensitive organizational, personal,
commercial, and runtime information if implemented naively.

OpenETR public events should not contain complete wallet presentations,
identity documents, Powers of Attorney, policy inputs, or runtime telemetry.
Integrations should prefer:

- minimal public actor and object references;
- hashes or commitments to authorization packages;
- encrypted or access-controlled evidence stores;
- purpose-bound presentation records;
- selective-disclosure credentials where appropriate;
- explicit retention and deletion policies for off-graph evidence; and
- verifier output that distinguishes unavailable evidence from invalid
  evidence.

The objective is end-verifiability, not indiscriminate publication.

## Failure And Revocation Semantics

The architectures also cover different kinds of revocation.

| Change | Primary response |
| --- | --- |
| Credential or mandate revoked before action | PDP denies; no consequential event should be signed |
| Agent or runtime compromised during execution | PEP blocks or quarantines; incident process records outcome |
| Authorization later found defective | Link corrective or dispute evidence; recognition policy determines effect |
| OpenETR signing key compromised | Apply profile rotation, warnings, and domain recovery rules |
| Record transition itself reversed | Use an explicit compensating or permitted successor transition, not deletion of history |
| Trust-domain issuer loses recognition | Later verifiers reevaluate recognition without rewriting signed historical evidence |

Revoking authority does not erase an action that already occurred. Equally, a
durable event does not guarantee continuing recognition. The graph should
preserve history while policies evaluate current and historical effect.

## OpenETR Design Consequences

The Spherity architecture does not require a new OpenETR core primitive.

The existing model is sufficient:

- **Digital Artifact** identifies the thing by digest.
- **Digital Controllable Record** contains end-verifiable evidence concerning
  it.
- **Consequential State** is derived from that evidence according to defined
  rules.
- **Digital Original** is the artifact with independently verifiable
  consequential state.
- **Recognition and effect** remain outside the protocol.

The integration does suggest several profile and implementation requirements.

### Domain Adapter Requirements

A domain adapter intended for agentic action should define:

1. which proposed actions can produce OpenETR Control Events;
2. which authority credentials and mandates are required for each action;
3. which current graph state must be included in the authorization request;
4. what constitutes the point of commitment;
5. how the action receipt binds to the OpenETR event;
6. which evidence is public, private, committed, or merely referenced;
7. how expiry, revocation, suspension, dispute, and recovery are handled; and
8. which recognition rules determine real-world effect.

### Linked Evidence Profile

A future linked-evidence profile could define neutral fields for:

- evidence type;
- evidence digest and media type;
- issuer or decision-maker reference;
- subject artifact and proposed action;
- policy identifier and version;
- decision time and validity window;
- expected prior OpenETR event;
- action receipt and resulting event references; and
- disclosure and retrieval method.

The profile should not require one wallet, DID method, VC proof format, trust
registry, or PDP product.

### Verifier Output

Verifier output should keep separate results for:

```text
cryptographic validity
DCR structural validity
state derivation
authority evidence
authorization decision
recognition decision
```

A single green check would hide materially different claims.

## Example: Agent Transfers A Warehouse Receipt

Consider an enterprise agent instructed to transfer a warehouse receipt after
payment.

```text
1. The receipt is a digest-identified Digital Artifact.
2. Its current DCR shows the transferor as controller and no blocking guard.
3. The agent proposes TRANSFER to the named transferee.
4. The Business Wallet proves the transferor organization and representative.
5. The Agent Wallet presents a current, transaction-bounded delegation.
6. The PDP checks mandate, value limit, counterparty, current DCR state,
   payment evidence, credential status, and policy.
7. The PEP permits the managed signer to sign only the approved TRANSFER.
8. The OpenETR event references the receipt, prior event, and transferee.
9. The signed action receipt binds the policy decision to the event id.
10. OpenETR rules derive the new consequential state.
11. The warehouse system, federation, counterparties, and applicable law
    determine recognition and effect.
```

The Business Wallet does not become the warehouse receipt. The authorization
receipt does not become the whole DCR. OpenETR does not perform company KYC or
decide whether the transfer has legal effect. Each component stays within its
proper boundary.

## Policy And Standards Implications

The paper's strongest policy contribution is the insistence that cross-domain
agent authority be portable, bounded, current, and locally evaluated. OpenETR
adds a complementary requirement:

> Consequential state should be derived from end-verifiable evidence according
> to defined rules, not merely asserted by applications, databases or
> blockchains.

Together, the principles imply that standards work should distinguish:

- identity from authority;
- authority from execution;
- execution evidence from consequential state;
- consequential state from recognition and effect;
- transient authorization context from durable record evidence; and
- credential containers from artifact-centric evidence graphs.

Standards bodies should profile the interfaces among these layers rather than
forcing them into one universal wallet, registry, ledger, or application.

## Recommended OpenETR Work

1. Add an agentic-action integration profile to the generic domain-adapter
   specification.
2. Define a linked authorization-decision and action-receipt evidence profile.
3. Require artifact digest, proposed action, expected prior event, policy
   version, and validity window in high-assurance authorization bindings.
4. Add verifier output fields that distinguish authority evidence from DCR and
   state validity.
5. Test stale mandate, changed graph head, replay, policy downgrade, wallet
   compromise, signer compromise, and unavailable status-service scenarios.
6. Pilot the pattern with a warehouse receipt or bill of lading transaction in
   which an agent proposes but cannot independently bypass authorization and
   signing controls.
7. Keep the core protocol actor-neutral and technology-neutral.

## Bottom Line

Spherity's architecture and OpenETR occupy adjacent parts of a trustworthy
execution chain.

```text
Spherity M-Trust architecture:
  Can this agent perform this action now?

OpenETR:
  What end-verifiable evidence records the consequential action,
  and what state follows under defined rules?

Recognition context:
  Should that state be accepted, and what real-world effect should it have?
```

The important opportunity is not to merge the architectures. It is to bind
their decisions and evidence precisely at the point of consequential action.
That creates a path from verifiable authority, through controlled execution,
to durable and independently verifiable consequential state.

## Policy Brief

- [Verifiable Agent Authority And
  OpenETR](https://trbouma.github.io/openetr/policy-briefs/verifiable-agent-authority-and-openetr/)

## Related OpenETR Notes

- [OpenETR Actor-Neutral Identity Design Note](./OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [OpenETR Autonomous Systems Governance Review Note](./OPENETR_AUTONOMOUS_SYSTEMS_GOVERNANCE_REVIEW_NOTE.md)
- [OpenETR Layered Architecture Note](./OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [Digital Controllable Record Design Note](./DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
- [Linked Evidence Record Kind Design Note](./LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md)
- [OpenETR Generic Domain Adapter Specification](./OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
