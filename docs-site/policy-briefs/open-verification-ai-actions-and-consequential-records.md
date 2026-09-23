# Open Verification For AI Actions And Consequential Digital Records

AI agents can now interpret information, call tools, move data, and initiate
actions across organizational systems. The policy question is no longer only
whether an agent appears capable or whether its operator says it followed the
rules. It is whether another party can verify what happened and determine what
consequence should follow for the digital thing involved.

The Advanced AI Society's draft Proof-of-Control standard and OpenETR address
different parts of that problem.

Proof-of-Control seeks openly verifiable evidence that an agent acted within
defined controls. OpenETR preserves artifact-specific evidence and derives the
consequential state of a digital thing according to defined rules.

Together, they support a more complete chain from authority, through action,
to consequence.

## The Problem

Agentic systems create a new version of a familiar evidence problem. The
system that performs an action is often also the system that reports what it
did.

An agent or its operator may provide logs, explanations, dashboards, and audit
exports. These can be useful, but an external party may still have to trust
that:

- every relevant action was recorded;
- the log was not rewritten;
- the executed request matched the approved request;
- the agent did not use an unmonitored path;
- the stated policy was actually enforced; and
- the claimed result corresponds to the digital record at issue.

Signing an application log improves integrity after signing. It does not, by
itself, prove that the log is complete or that it faithfully represents what
happened.

## What Proof-of-Control Contributes

The OpenVerification initiative proposes that evidence should be generated at
the point where an agent invokes a tool or causes an effect. Its draft
Proof-of-Control model emphasizes evidence that is contemporaneous,
tamper-evident, transparent about residual trust, and independently
verifiable.

Its strongest pattern places an interception mechanism between the agent and
the affected system. The mechanism evaluates the action, binds the approved
request to the request that executes, produces evidence as part of execution,
and refuses the action if required evidence cannot be generated.

The draft grades evidence using four tiers:

| Tier | Meaning |
| --- | --- |
| 1 | The operator asserts that a control held. |
| 2 | A third party or auditor attests to it. |
| 3 | An outsider can verify the evidence using published material. |
| 4 | Valid evidence and controls gate the action, so it cannot proceed otherwise. |

The proposed standard calls Tiers 3 and 4 Proof-of-Control. The tier model
remains draft and should be applied to specific claims, not used as a general
label for an entire system.

Proof-of-Control also maintains an essential boundary. It can provide evidence
that an agent stayed within the controls it was given. It does not establish
that the controls were good, that the model's output was correct, or that the
action should have legal effect.

## What OpenETR Contributes

OpenETR begins with the digital thing rather than the agent.

It separates:

- the **Digital Artifact**, identified by a digest;
- the **Digital Controllable Record**, containing end-verifiable evidence of
  consequential actions;
- the **Consequential State** derived from that evidence according to defined
  rules; and
- the **Digital Original**, the digital thing with independently verifiable
  consequences.

Recognition and effect remain outside the protocol. An individual, community,
institution, authority, contract, or applicable law determines whether the
digital thing and its derived state should be recognized and what real-world
effect they should have.

OpenETR therefore answers a question that agent execution evidence does not:

> What follows for this particular digital thing under the applicable rules?

## Two Different Meanings Of Control

The shared word **control** can obscure the relationship.

Proof-of-Control is mainly concerned with execution controls: whether an agent
stayed within permissions, policies, and an enforced action boundary.

OpenETR may represent controller state for transferable records, but its
broader concern is consequential state. Issuance, revocation, discharge,
attestation, and termination can be consequential even when no controller
changes.

The distinction is:

```text
Proof-of-Control:
  Was the agent action within its controls?

OpenETR:
  What consequence follows for the digital thing?
```

Neither answer implies the other.

## Connecting Action To Consequence

A practical integration would work as follows:

1. A host system authenticates the responsible principal and gives an agent a
   bounded delegation.
2. A Proof-of-Control mechanism intercepts the proposed action and evaluates
   it against the current policy and authority.
3. The approval is bound to the exact artifact digest, action, expected prior
   record state, policy version, target, and validity window.
4. The affected system accepts only the approved, action-bound request.
5. The execution mechanism creates evidence of what was evaluated and what
   occurred.
6. If the action is consequential for the artifact, an OpenETR domain adapter
   creates an Evidence Event linked to that execution evidence.
7. OpenETR rules derive the resulting consequential state.
8. The relevant relying party determines recognition and real-world effect.

This creates a chain that is stronger than either an agent log or an
application state field:

```text
bounded authority
  -> verifiable agent action
  -> artifact-specific evidence
  -> defined state transition rules
  -> consequential state
  -> recognition and effect
```

## Proof-of-Control Evidence Is Not Automatically A Record Event

Most agent actions should not become part of a digital thing's permanent
record. A retrieval, formatting step, internal policy check, or unsuccessful
proposal may be operationally relevant without changing the artifact's state.

Proof-of-Control evidence can therefore be:

- a separately verifiable evidence artifact;
- supporting evidence linked by digest to an OpenETR event; or
- evidence of the consequential action represented by an OpenETR event.

The applicable domain rules must decide which role it plays.

## A Warehouse Receipt Example

Suppose an AI agent is instructed to transfer a digital warehouse receipt
after payment.

The receipt is identified as a Digital Artifact. Its DCR identifies the current
controller and any guards on transfer. The agent receives a transaction-bounded
delegation. A Proof-of-Control gateway checks the delegation, counterparty,
value, payment evidence, policy, and current DCR head before allowing the
managed signer to sign the transfer.

The resulting OpenETR event links the receipt, prior event, transferee, and a
commitment to the execution evidence. OpenETR rules derive the new
consequential state. The warehouse system, counterparties, federation, and
applicable law determine whether the transfer is recognized and what effect it
has.

The agent's compliance evidence does not become the receipt. The receipt's
valid state does not prove that every agent action was monitored. The two
evidence layers support different decisions.

## Policy Priorities

Policymakers, standards bodies, procurement teams, and system operators should:

1. **Separate authority, execution, consequence, and recognition.** Each is a
   distinct claim with different evidence and decision-makers.
2. **Require claim-specific evidence.** Avoid assigning one assurance tier to
   a whole product when only particular actions or controls have been tested.
3. **Bind approval to the exact digital thing.** Agent authority should name
   the artifact digest, action, expected prior state, target, policy, and
   validity window.
4. **Test bypass paths.** A signed log is insufficient when an agent can reach
   tools, credentials, or signers outside the evidenced path.
5. **Require independently usable verification material.** Schemas, canonical
   formats, algorithm identifiers, rules, trust assumptions, and test vectors
   should be available to outside verifiers.
6. **Make completeness claims explicit.** Verifying presented evidence is not
   the same as proving that no action or event is missing.
7. **Protect sensitive traces.** Use digests, commitments, selective
   disclosure, and controlled evidence stores instead of publishing complete
   agent histories.
8. **Retain human and institutional judgment.** Verifiable compliance with a
   policy does not prove that the policy was adequate or that the outcome was
   fair, lawful, or correct.
9. **Keep recognition local.** Common evidence can support interoperable
   assessment without requiring every jurisdiction or institution to reach the
   same decision.
10. **Pilot the combined pattern.** Transferable records provide a strong test
    because authority, execution, evidence, state, and real-world effect can be
    examined separately.

## Implications For OpenETR

OpenVerification does not require a new OpenETR primitive. The useful work is
at the integration boundary.

OpenETR should develop a linked-evidence profile that binds Proof-of-Control
evidence to an artifact digest, OpenETR action, prior event, resulting event,
and ruleset. Verifier output should report execution-evidence status separately
from event validity, graph continuity, consequential state, identity and
authority evidence, recognition, and effect.

High-assurance profiles should also describe their completeness boundary,
equivocation protections, time source, evidence retention, and non-bypassable
signing path.

## Bottom Line

Proof-of-Control and OpenETR solve adjacent problems.

Proof-of-Control can help establish that an AI agent acted within defined
controls and that another party can verify the evidence. OpenETR can bind a
consequential action to a particular digital thing and derive the state that
follows according to defined rules.

Recognition remains the final question: should that state be accepted, and
what real-world effect should it have?

The policy opportunity is to connect the layers without confusing them:

> Agent actions should be evidenced at execution. Consequences for digital
> things should be derived from end-verifiable evidence and defined rules.

## Detailed Analysis

- [OpenVerification Proof-of-Control And OpenETR Analysis
  Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_AND_OPENVERIFICATION_PROOF_OF_CONTROL_ANALYSIS_NOTE.md)

## Sources And Related Materials

- [OpenVerification use-case repository](https://github.com/AAI-Society/openverification)
- [Proof-of-Control standard repository](https://github.com/AAI-Society/ov-poc-standard)
- [Advanced AI Society announcement](https://advancedaisociety.org/announcements/joins-linux-foundation-open-verification-ecosystem)
- [Agentic AI And Consequential Evidence](./agentic-ai-and-consequential-evidence.md)
- [Verifiable Agent Authority And OpenETR](./verifiable-agent-authority-and-openetr.md)
- [OpenETR, Trust Frameworks, And Registries](./openetr-trust-frameworks-and-registries.md)

