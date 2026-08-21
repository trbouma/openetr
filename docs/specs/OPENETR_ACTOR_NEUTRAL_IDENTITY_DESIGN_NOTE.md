# OpenETR Actor-Neutral Identity Design Note

This note defines how OpenETR treats human users, software services, autonomous agents, and mixed human-machine workflows at the protocol boundary.

It was prepared after reviewing *Designing Agent IDs*, published by the Singapore AI Safety Hub (SASH) on 31 March 2026.

## Status

Draft design decision.

## Decision

OpenETR does not distinguish between human actors and agent actors in its core identity or control-event model.

At the protocol layer, an actor is represented by a public key. A valid event signature proves that the corresponding private key authorized the event. It does not prove whether the key was operated by:

- a human using a command line or web application;
- a software service following deterministic rules;
- an autonomous or semi-autonomous agent;
- a hardware or managed signing service;
- a human approving an action proposed by an agent;
- a shared organizational workflow.

This actor-neutral treatment is intentional. Human or agent status may matter greatly to an integrating system, regulator, counterparty, or verifier policy, but it is not an intrinsic property of a Nostr public key or OpenETR signature.

## Protocol Claim

For any signed OpenETR event, the core protocol can establish:

```text
the event is cryptographically valid
the event was signed by this public key
the event refers to this digest-identified object
the event participates in this candidate control graph
```

The core protocol cannot establish from the signature alone:

```text
the signer is a natural person
the signer is an AI agent
the signer is a legal person
the signer was authorized by an employer or principal
the signer satisfied KYC or licensing requirements
the signer was supervised by a human
the event should have legal or institutional effect
```

Those are authorization, governance, attribution, and recognition questions.

## Why Actor Type Is Not A Core Field

OpenETR should not require an `actor_type=human` or `actor_type=agent` field in control events.

There are several reasons:

1. A self-declared actor type is not cryptographic proof of who or what operated the key.
2. Many actions are hybrid: an agent proposes, a policy engine checks, a human approves, and a custody service signs.
3. The operator behind a persistent key may change over time without changing the key's cryptographic identity.
4. A mandatory classification could disclose operational or personal information that is unnecessary for control-graph correctness.
5. Different domains and jurisdictions may define `agent`, `automated system`, `operator`, and `human oversight` differently.
6. Control-graph verification should remain stable even as automation and governance models evolve.

An integration may still publish or link an actor-type claim. The claim should be treated as evidence supplied by an identified issuer, not as a fact inferred by the OpenETR protocol.

## Relationship To Agent IDs

The SASH paper describes an Agent ID as a collection of identifiers and metadata that may support authentication, authorization, incident prevention, accountability, and compatibility. It recommends a layered approach because no single existing identity mechanism satisfies every function.

That layered conclusion fits OpenETR well.

| Agent-ID concern | OpenETR contribution | External or policy contribution |
| --- | --- | --- |
| Agent instance identity | A dedicated `npub` may identify a persistent signer or instance | The deployer defines whether a key represents one instance, a pool, or a service |
| Provider identity | A provider may sign an attestation or publish linked evidence | A registry or trust framework recognizes the provider |
| Deployer or principal identity | A deployer may use a separate key or issue a delegation attestation | The host system authenticates the deployer and establishes accountability |
| Authentication | Event signatures authenticate control of the signing key | OIDC, passkeys, enterprise IAM, or other systems authenticate account users |
| Authorization | Events state the action performed on an object | OAuth scopes, mandates, workflow rules, or domain policy decide whether the action was permitted |
| Incident response | Signed events provide durable, object-specific evidence | The provider or deployer supplies monitoring, suspension, escalation, and response processes |
| Compatibility | OpenETR defines a portable event and graph grammar | MCP, REST APIs, CLI JSON, or domain APIs provide interaction surfaces |

OpenETR therefore does not attempt to become a comprehensive Agent ID format. It can carry the stable signer identifier and link to richer identity, authorization, and governance evidence.

## Root And Profile Implications

The root-and-profile model is also actor-neutral.

A root identity or Control Desk Key may be administered by a person, an organization, a custody system, or an automated service. A profile signer or Commitment Profile may represent:

- a person;
- an organizational role;
- a facility or department;
- a service account;
- a software agent;
- a dedicated agent instance;
- a controlled signing workflow.

The root organizes access to independent profile keys. It does not prove the nature of the operator behind them.

Where agent-instance separation is important, an integrator may assign a dedicated profile key to each agent instance or class of agents. Where that granularity is unnecessary, several processes may use one managed operational profile. OpenETR does not prescribe either choice.

## Principal, Operator, And Signer

Integrations should keep three concepts separate:

```text
principal:
  the person or organization on whose authority an action is performed

operator:
  the human, agent, service, or workflow that initiates or executes the action

signer:
  the private-key holder or signing service that produces the event signature
```

These may be the same actor, but they need not be.

For example:

```text
warehouse company (principal)
  -> inventory agent (operator)
  -> managed Commitment Profile key (signer)
  -> signed ISSUE event (OpenETR evidence)
```

The host system should retain or link the evidence needed to explain this relationship when policy requires it.

## Optional Claims And Linked Evidence

An integrating system may express additional actor information through profile metadata, attestations, linked evidence records, registry references, or domain-specific tags.

Examples include claims that:

- a profile is operated by an autonomous agent;
- a deployer controls or supervises an agent instance;
- an agent is authorized only for specified actions or object classes;
- an authorization expires at a stated time;
- a provider supplied the agent software;
- a particular model or tool configuration was used;
- a human approval was obtained before signing;
- an incident-response endpoint is available.

Such claims should identify their issuer and, where appropriate, their validity period, scope, and revocation or supersession mechanism. Sensitive details should normally remain outside public control events, with OpenETR carrying a digest or reference to the evidence.

## Verifier Policy

The generic OpenETR verifier should evaluate cryptographic and graph correctness without treating human-operated signatures as inherently stronger than agent-operated signatures.

A domain or organizational rule book may add safeguards such as:

- warn when the signer is not a known entity;
- require a recognized deployer attestation for an agent-operated profile;
- require bounded authorization for a particular action;
- require fresh authority at the time of action;
- require human approval for high-impact transitions;
- reject, quarantine, or escalate events from suspended agent profiles;
- require incident-response or provider information;
- apply different rules according to risk, domain, or jurisdiction.

These rules enumerate the same signed graph under a particular policy. They do not change whether the underlying signature is valid.

## Integration Guidance

An integration that permits agents to create consequential OpenETR events should:

1. authenticate the accountable account, deployer, or principal;
2. assign the least privilege needed to the agent or workflow;
3. distinguish a proposal from authorization and signing;
4. verify current graph state immediately before a consequential action;
5. protect profile keys through managed custody or constrained signing interfaces;
6. retain or link evidence of delegation, approval, and policy evaluation;
7. support suspension, rotation, incident response, and recovery;
8. disclose agent operation only where the applicable policy requires it.

The OpenETR CLI `--json`, Python component, and REST surfaces can all support agent workflows. Access to those surfaces is not itself authority. The host system remains responsible for deciding which operations an agent may invoke and under what conditions a signer will authorize them.

## Policy Consequence

OpenETR offers equal cryptographic treatment, not equal legal effect.

A human-operated and agent-operated key can produce signatures of the same cryptographic quality. A relying party may nevertheless apply different authorization, assurance, disclosure, supervision, or recognition requirements to those actors.

This preserves a clean boundary:

```text
OpenETR:
  verifies signed control evidence without guessing who or what operated the key

integrating system and verifier policy:
  determine actor classification, authority, safeguards, accountability, and effect
```

## Source Reviewed

Singapore AI Safety Hub (SASH), *Designing Agent IDs*, 31 March 2026, 16 pages. The paper was supplied directly for this review.

## Related Notes

- [Root And Profile Identity Model](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [System Integration Considerations](./SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR Autonomous Systems Governance Review Note](./OPENETR_AUTONOMOUS_SYSTEMS_GOVERNANCE_REVIEW_NOTE.md)
- [OpenETR Organizational Reference Layer Design Note](./OPENETR_ORGANIZATIONAL_REFERENCE_LAYER_DESIGN_NOTE.md)

