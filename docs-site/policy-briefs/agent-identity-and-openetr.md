# Agent Identity And OpenETR

AI agents are beginning to perform actions that matter outside a chat window. They can call services, initiate transactions, update records, and participate in workflows that affect people and organizations.

The Singapore AI Safety Hub paper *Designing Agent IDs* asks what information services need in order to know who an agent is, who instructed it, what it may do, and how incidents should be handled. Its central finding is that no single identity system answers all of those questions. Agent identity will require layers for authentication, authorization, structured interaction, registries, governance, and domain-specific rules.

OpenETR fits that layered model, but it draws a firm protocol boundary.

For each record lifecycle, OpenETR distinguishes the exact **Digital Artifact**
from the **Digital Controllable Record (DCR)** made up of signed evidence about
that artifact. Protocol rules evaluate the DCR to derive consequential state.
Identity and governance systems then help a relying party decide whether to
recognize the signer, its authority, and the resulting state.

## The OpenETR Position

OpenETR does not distinguish between a human actor and an agent actor at the protocol layer.

An OpenETR event is signed by a cryptographic key. Verification proves that the corresponding key authorized the event. It does not reveal whether the key was operated by a person, an AI agent, a service account, a managed signing service, or a workflow combining all of them.

That is not a missing feature. It is a deliberate separation of concerns.

```text
OpenETR verifies:
  which key signed which event about which record

The integrating system decides:
  who or what operated the key, whether it was authorized,
  what safeguards applied, and what effect the event should have
```

## Why The Distinction Belongs Outside The Core

A mandatory label such as `human` or `agent` would be easy to assert but difficult to prove. It would also hide the reality of modern workflows.

An agent may propose an action, a policy engine may test it, a human may approve it, and a custody service may apply the signature. Which one is the actor?

The useful answer depends on the question being asked:

- For cryptographic correctness, the signer key matters.
- For authorization, the mandate and scope matter.
- For accountability, the principal and deployer matter.
- For incident response, the provider, operator, model, and runtime may matter.
- For legal effect, the applicable law and recognition policy matter.

Trying to compress all of these into one protocol-level actor label would make the evidence less precise, not more.

## How Agent IDs Can Complement OpenETR

OpenETR can carry or link the evidence needed by an Agent ID framework without becoming that framework.

| Policy need | OpenETR role | Complementary system role |
| --- | --- | --- |
| Persistent actor reference | Event signer `npub` | Identity provider or registry maps the key to an agent, provider, deployer, or legal entity |
| Authentication | Signature proves control of the signing key | OIDC, passkeys, or enterprise IAM authenticates the account or principal |
| Authorization | Event records the action performed | OAuth, mandates, workflow policy, or domain rules define permitted actions |
| Accountability | A DCR preserves durable signed action evidence | Governance processes assign responsibility and retain operational logs |
| Incident response | Events identify affected objects and signer history | Providers and deployers supply monitoring, suspension, escalation, and remediation |
| Recognition | Verifiers can evaluate linked evidence | Trust frameworks, registries, counterparties, and law decide effect |

An integration may use a dedicated OpenETR profile key for an agent instance. It may instead use a managed organizational profile shared by a constrained workflow. OpenETR supports both because profile keys identify signers, not biological or computational categories.

## The Root-And-Profile Model

OpenETR's root-and-profile identity model maps naturally to agent-enabled systems.

The root identity, presented in the warehouse receipt application as the **Control Desk Key**, organizes operational signer profiles. A **Commitment Profile** signs record events. Either key may be operated through a human interface, an automated service, an agent, or managed custody.

The model separates administrative organization from operational authorship, but it does not claim that a profile is human or automated.

Where policy requires more information, the system can link claims about:

- the accountable principal or deployer;
- the agent provider or instance;
- bounded permissions and expiry;
- human approval;
- model or tool configuration;
- monitoring and incident-response contacts;
- suspension or revocation status.

Those claims remain independently attributable evidence. A verifier can require, ignore, or warn about them according to its rule book.

## Policy Implications

The SASH paper highlights security, interoperability, privacy, distributed infrastructure, and risk-proportionate requirements. OpenETR contributes to those goals in a narrow but useful way.

Its signed, portable events avoid dependence on one identity vendor or application session. Its public-key identifiers can be resolved against different registries and assurance systems. Its policy boundary allows high-risk sectors to require stronger agent identity and authorization without imposing those requirements on every use case.

The resulting policy position is:

1. Do not infer human or agent status from an OpenETR key.
2. Do not treat a signature as proof of legal identity, delegation, or permission.
3. Permit actor, provider, deployer, and authorization claims as linked evidence.
4. Let domain and organizational policies decide which claims are required.
5. Apply additional safeguards at the point where an agent can cause a consequential record action.
6. Preserve the same cryptographic verification rules for human-operated and agent-operated keys.

## A Useful Boundary

The Agent ID paper is about making agents identifiable, governable, and interoperable.

OpenETR is about making record actions signed, object-specific, linked, and independently verifiable.

These concerns complement one another:

```text
Agent identity and governance:
  who or what is acting, for whom, under what authority and safeguards

OpenETR control layer:
  what DCR evidence exists for which digest-identified artifact,
  and what consequential state follows under the protocol rules

Recognition policy:
  whether that actor and action should be accepted in context
```

This boundary lets OpenETR support both people and agents without making the control protocol dependent on a single model of agency, identity, or regulation.

## Source And Detailed Design

- Singapore AI Safety Hub (SASH), *Designing Agent IDs*, 31 March 2026. Supplied directly for review.
- [OpenETR Actor-Neutral Identity Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Autonomous Systems Governance And OpenETR](./autonomous-systems-governance-and-openetr.md)
