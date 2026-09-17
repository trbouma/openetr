# Verifiable Agent Authority And OpenETR

AI agents are moving from producing recommendations to initiating transactions,
updating records, operating equipment, and acting across organizational
boundaries.

That creates two separate questions:

```text
Was the agent authorized to act?

What verifiable consequence followed from the action?
```

Spherity's proposed M-Trust architecture addresses the first question. OpenETR
addresses the second for consequential actions concerning digital records.

Together, they describe a more complete path from authority to durable digital
consequence.

## Beyond Enterprise Zero Trust

Traditional Zero Trust Architecture evaluates each request to access an
enterprise resource. That remains necessary, but an AI agent may act across
companies, sectors, registries, and jurisdictions.

A receiving organization may need to know:

- which person or organization stands behind the agent;
- who delegated authority to it;
- what task, value, purpose, and time limits apply;
- whether the mandate and credentials remain current;
- whether the AI service and runtime meet required assurance conditions; and
- which policy decision permitted the action.

Spherity's paper [*Beyond Single-Enterprise ZTA: Multi-Trust Architectures for
Authorised Agentic Actors in Open, Cross-Domain
Ecosystems*](https://spherity.github.io/spherity-research/beyond-zero-trust-m-trust-authorised-agentic-actors.html)
proposes an eight-layer architecture for answering those questions.

It combines Business and Agent Wallets, legal-person identity, verifiable
credentials, bounded delegation, AI service assurance, local policy, external
enforcement, registries, and signed action receipts.

Its central idea is **transient cross-domain trust**. Evidence from several
independently governed domains is assembled for one purpose, audience, and time
window. Each source retains authority over its own claims, while the receiving
verifier makes the final authorization decision.

## Authorization Is Not Consequence

A valid identity and mandate can establish that an agent may act. They do not,
by themselves, establish that the action occurred or determine the resulting
state of the affected record.

This is where OpenETR fits.

OpenETR separates:

- the **Digital Artifact**, which identifies the digital thing by digest;
- the **Digital Controllable Record**, which contains end-verifiable evidence
  concerning it;
- the **Consequential State** derived from that evidence under defined rules;
  and
- the **Digital Original**, the digital thing with independently verifiable
  consequential state.

The relationship is straightforward:

```text
identity and delegation
  -> authorization decision
  -> controlled execution
  -> OpenETR consequential evidence
  -> derived consequential state
  -> recognition and real-world effect
```

The authorization architecture decides whether an action may proceed. OpenETR
preserves artifact-specific evidence of what happened and makes the resulting
state independently verifiable.

## A Useful Division Of Responsibility

| Responsibility | Primary mechanism |
| --- | --- |
| Establish the accountable person or organization | Authoritative registers and identity credentials |
| Establish the agent and its mandate | Business Wallet, Agent Wallet, and bounded delegation |
| Decide whether the action is currently permitted | Local verifier and Policy Decision Point |
| Prevent unauthorized execution | Policy Enforcement Point, connector, or gateway |
| Preserve the authorization and execution decision | Signed action receipt |
| Preserve consequential record evidence | OpenETR Digital Controllable Record |
| Derive the record's consequential state | OpenETR state transition rules |
| Decide recognition and effect | Individual, community, institution, authority, contract, or applicable law |

No single component should claim to do all of these jobs.

## Transient Trust, Durable Evidence

Spherity's transient trust decision is deliberately current and
transaction-specific. A credential may expire, a mandate may be revoked, a
policy may change, or a runtime may be suspended.

OpenETR serves a different time horizon. Its signed graph allows a later
verifier to reconstruct the evidence concerning the artifact even when the
original application, wallet session, or agent is no longer available.

```text
transient trust:
  enough current authority to permit one action

durable evidence:
  enough signed, linked evidence to determine what happened
  and derive the resulting record state later
```

The combination is stronger than either layer alone. Durable evidence without
current authorization can preserve an unauthorized act. Current authorization
without durable evidence can leave the resulting record state dependent on the
application that performed the transaction.

## Wallets And Open Graphs

Business and Agent Wallets are controlled containers for credentials, keys,
mandates, and proofs. They present selected evidence to a verifier for a
particular transaction.

OpenETR is an artifact-centric evidence graph. It allows record history and
state to be checked independently of the wallet or application that originally
participated.

The wallet answers:

```text
Who is acting, for whom, and under what current authority?
```

The OpenETR graph answers:

```text
What happened to this digital thing, and what state follows under the rules?
```

The two models are complementary, not competing.

## Signed Action Receipts Need Careful Treatment

Spherity proposes a signed action receipt containing evidence such as the
policy version, status snapshot, evidence references, execution result, and
timestamp.

For OpenETR, that receipt may play one of three roles:

1. It may be linked evidence explaining why an Evidence Event was authorized.
2. It may be operational evidence that does not change the artifact's state.
3. In a domain that defines the receipt itself as the consequential act, it may
   become or be referenced by an Evidence Event.

The domain adapter must make that distinction. Otherwise, systems may either
clutter the state graph with ordinary authorization logs or fail to record an
action that genuinely changes the state of the digital thing.

## Recognition Still Remains Outside

Neither architecture should claim to grant legal or social effect by itself.

OpenETR can establish a Digital Original whose identity and consequential state
can be independently verified. Spherity's architecture can establish evidence
that an agent was authorized under a particular policy and context.

On that basis, an individual, community, institution, authority, contract, or
applicable law can determine whether the digital thing and action should be
recognized and what effect they should have.

This preserves local and institutional sovereignty while allowing the
underlying evidence to remain portable.

## Policy Priorities

Policymakers, standards bodies, and ecosystem operators should:

1. Keep identity, authority, execution, consequential state, and recognition
   as separate claims.
2. Require bounded, current, and purpose-specific delegation for consequential
   agent actions.
3. Bind authorization decisions to the exact artifact, requested action,
   expected prior state, policy version, and validity window.
4. Require non-bypassable enforcement before an agent can sign or commit a
   consequential action.
5. Preserve signed action receipts and link them to the resulting record event.
6. Use commitments, selective disclosure, and controlled evidence stores
   rather than publishing complete identity and mandate packages.
7. Permit each relying party to apply its own recognized issuers, policies, and
   legal context.
8. Require open profiles and conformance tests so one wallet, registry, ledger,
   or platform does not become a permanent dependency.

## A Practical Pilot

A warehouse receipt or bill of lading pilot would provide a useful test.

An agent could propose a transfer, while a Business Wallet establishes the
organization, an Agent Wallet establishes bounded delegation, a local policy
engine checks current authority and record state, and an enforcement point
permits only the approved signature.

OpenETR would then preserve the signed transfer evidence and derive the new
consequential state. The relevant commercial network and applicable law would
determine whether the transfer is recognized and what effect it has.

The pilot should test revoked mandates, changed record state, replay, policy
downgrade, unavailable status services, compromised wallets, and recovery.

## Bottom Line

Spherity's architecture asks whether an agent has current authority to act.

OpenETR asks what end-verifiable evidence records the consequential action and
what state follows under defined rules.

Recognition determines whether that state is accepted and what real-world
effect it has.

The policy opportunity is to connect these layers without collapsing them:

> Verifiable authority should govern whether an agent may act. End-verifiable
> evidence and defined rules should determine the consequential state that
> follows.

## Detailed Analysis

- [OpenETR And Spherity M-Trust Architecture Analysis
  Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_AND_SPHERITY_M_TRUST_ANALYSIS_NOTE.md)

## Sources And Related Materials

- [Spherity research page and reference
  architecture](https://spherity.github.io/spherity-research/beyond-zero-trust-m-trust-authorised-agentic-actors.html#reference-architecture)
- [Spherity full research
  paper](https://spherity.github.io/spherity-research/Spherity-Beyond-Single-Enterprise-ZTA-Multi-Trust-Architectures-for-Authorised-Agentic-Actors.pdf)
- [Agent Identity And OpenETR](./agent-identity-and-openetr.md)
- [Autonomous Systems Governance And OpenETR](./autonomous-systems-governance-and-openetr.md)
- [OpenETR, Trust Frameworks, And Registries](./openetr-trust-frameworks-and-registries.md)

