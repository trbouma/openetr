# Agentic AI Needs Consequential Evidence

The United Nations [*Co-Chairs' Summary of the inaugural Global Dialogue on
Artificial Intelligence Governance*](https://www.un.org/global-dialogue-ai-governance/sites/default/files/2026-09/ai_dialogue_co-chairs_summary.pdf)
describes an international policy conversation increasingly concerned with
verifiability, traceability, interoperability, evidence, accountability, and
agentic AI.

The report does not discuss or endorse OpenETR. It is also a summary of themes
observed by the Co-Chairs, not a negotiated outcome or consensus position. It
nevertheless provides an important external signal: as AI systems become more
capable of taking consequential actions, governance will need evidence that can
be evaluated beyond the application in which an action occurred.

OpenETR offers a useful architectural response:

> AI may infer what a digital artifact means. Consequential action should rest
> on independently verifiable evidence, identified rules, and an explicit
> recognition decision.

## Policy Context

The UN summary identifies several themes that are directly relevant to this
problem.

First, participants described interoperability, rather than complete
harmonization, as a realistic objective for connecting different national and
regional governance approaches. The report points to common technical
foundations, shared definitions, comparable classifications, open benchmarks,
and mutual recognition of testing and audit protocols.

Second, it presents verifiability as a basis for trust. Participants called for
independent testing, disclosure across the AI value chain, incident reporting,
and exchanges of evidence.

Third, it identifies increasingly autonomous and agentic AI as a particular
accountability challenge. The proposed elements of accountability include
transparency and traceability, documentation of agent chains, an identifiable
and empowered human decision-maker, clear liability, remedies, and audit
capacity.

Fourth, the report calls for practical and interoperable tools that can move AI
governance from principles toward implementation.

These themes do not prescribe a technical architecture. They do, however,
expose the need for one.

## The Hard Problem Has Moved

The article [*The Machine Can Read the Document. But Should It Believe
It?*](https://trbouma.substack.com/p/the-machine-can-read-the-document)
provides the complementary technical insight.

AI is rapidly reducing the cost of interpreting unfamiliar or weakly
structured documents. An agent can often understand an invoice, warehouse
receipt, purchase order, certificate, image, or handwritten note without every
participant first adopting the same application or schema.

But a fraudulent invoice may be just as intelligible as a genuine one.
Comprehension does not establish:

- who issued the artifact;
- whether the issuer or another actor was authorized;
- which consequential actions occurred;
- whether an authorization was revoked or superseded;
- what current state follows from the evidence; or
- whether another party should act on that state.

The policy problem therefore moves from making artifacts machine-readable to
establishing reliable grounds for action.

## From Agent Logs To End-Verifiable Evidence

Documenting an agent chain is useful, but an application log remains an
assertion made and controlled by that application. A relying party may be
unable to verify the log without privileged access to the originating system,
its database, and its interpretation of current state.

For consequential actions, stronger documentation should be:

- attributable to identifiable signing keys;
- bound to the exact Digital Artifact or object concerned;
- cryptographically linked to relevant prior evidence;
- independently retrievable where disclosure policy permits;
- evaluated under identified and versioned rules; and
- capable of producing a reproducible state assessment outside the originating
  application.

OpenETR calls the resulting evidence structure a **Digital Controllable Record
(DCR)**. The DCR does not make every signed assertion true or effective. It
provides portable evidence from which a verifier can determine what follows
under a selected rule book.

```text
AI interpretation
  -> proposes what the artifact means

Digital Artifact
  -> identifies the exact content by digest

DCR evidence
  -> records attributable consequential statements and relationships

Defined rules
  -> validate the evidence and derive Consequential State

Recognition
  -> determines whether a relying party accepts that result

Effect
  -> determines what action or external consequence follows
```

This division lets AI perform the interpretation at which it is increasingly
capable without allowing inference alone to manufacture authority or current
state.

## A Consequential Evidence Layer For Agentic Systems

Consider an AI agent presented with a purchase order for $47,500.

The agent may accurately infer the supplier, amount, goods, delivery terms, and
requested payment. Those are semantic conclusions. Before approving payment,
the relevant system may need to determine:

1. Did the identified organization issue this exact purchase order?
2. Which key signed the approval evidence?
3. What identity, role, or mandate is associated with that key?
4. Was the approval within the applicable monetary and temporal limits?
5. Was the authority later revoked or the purchase order superseded?
6. What current authorization state follows under the selected rules?
7. Does the paying organization recognize that evidence and state for this
   transaction?

OpenETR can provide the object-specific evidence and state-derivation layer. It
does not perform KYC, assign organizational responsibility, determine legal
liability, or compel payment. Those remain responsibilities of identity
systems, host applications, governance frameworks, contracts, law, and relying
parties.

## Actor-Neutral Evidence, Human-Centred Accountability

The UN report emphasizes meaningful human oversight, an empowered human
decision-maker, liability, remedies, and audit capacity. OpenETR does not
replace any of these requirements.

At the protocol layer, a **Key-Based Identifier** identifies verification
material. It does not establish whether the key was operated by a person,
organization, service, device, or autonomous agent. This actor-neutral model is
useful because real workflows frequently combine all of them: an agent proposes
an action, a policy engine tests it, a human approves it, and a managed signing
service applies the signature.

The integrating system and recognition policy must preserve the additional
evidence needed to identify:

- the accountable principal;
- the agent, operator, or service involved;
- the authority or mandate under which it acted;
- the human approval or override path, where required;
- applicable limits, expiry, suspension, and revocation;
- the responsible provider or deployer; and
- available review, appeal, and remedy processes.

Cryptographic attribution strengthens accountability evidence. It does not
decide where accountability or liability ultimately rests.

## Interoperability Without Harmonized Recognition

The report's emphasis on interoperability among differing governance regimes
aligns closely with OpenETR's recognition boundary.

Participants do not need one shared application, database, identity provider,
or legal conclusion. They can instead agree on enough common evidence and
verification conventions to evaluate the same signed records. Each
jurisdiction, institution, or counterparty can then apply its own recognition
policy.

```text
shared artifact identity
  + portable attributable evidence
  + reproducible verification rules
  = interoperable assessment

local law, policy, contract, or institutional mandate
  = recognition and effect
```

The central policy proposition is:

> Interoperable evidence does not require harmonized recognition.

This approach supports international cooperation while respecting differences
in law, institutional authority, risk tolerance, and local context.

## Policy Recommendations

1. **Distinguish interpretation from evidence.** AI-generated semantic
   conclusions should not be treated as proof of issuance, authority,
   authorization, control, revocation, or current state.
2. **Require stronger evidence for consequential action.** Assurance should
   increase when an agent can transfer value, exercise authority, alter rights,
   or trigger legal or operational consequences.
3. **Make agent-chain evidence object-specific.** Accountability records should
   identify the exact artifact or transaction concerned and link to relevant
   prior evidence.
4. **Prefer portable evidence over application-only logs.** Another authorized
   implementation should be able to verify the evidence without requiring the
   originating application to remain available.
5. **Identify the rule book.** A state conclusion should disclose the rules,
   policy version, evidence scope, and verification time on which it depends.
6. **Report verification dimensions separately.** Artifact integrity, signature
   validity, graph continuity, authorization, evidence sufficiency, actor
   recognition, and external effect should not collapse into one `trusted`
   Boolean.
7. **Preserve recognition plurality.** Common technical evidence should support,
   not displace, jurisdictional and institutional authority.
8. **Retain human accountability mechanisms.** End-verifiable evidence should
   complement human oversight, audit, appeal, remedy, and liability frameworks.

## Implications For OpenETR

The report does not require a new OpenETR primitive or a special class of
AI-authored event. The existing actor-neutral model already permits people,
organizations, services, and agents to participate through signing keys while
leaving identity, authority, accountability, and recognition to the applicable
context.

The immediate OpenETR priorities are therefore to:

- develop agentic-system examples using the existing DCR model;
- improve representation of authorization, delegation, revocation, execution,
  and linked evidence;
- expose verifier results in machine-readable, dimension-specific form;
- document how external identity and agent-governance systems supply
  recognition evidence; and
- demonstrate independent state reconstruction across two separately operated
  systems.

The idea can be summarized without diminishing either AI or institutional
judgment:

> Inference interprets. Evidence supports claims. Rules determine what follows.
> Recognition gives effect.

AI is making digital artifacts broadly intelligible. OpenETR is concerned with
making consequential actions concerning those artifacts independently
verifiable.

## Related Material

- [OpenETR Axioms](../openetr/axioms.md)
- [Agent Identity And OpenETR](./agent-identity-and-openetr.md)
- [Autonomous Systems Governance And OpenETR](./autonomous-systems-governance-and-openetr.md)
- [Policy Guards And Cryptographic Evidence](./policy-guards-and-cryptographic-evidence.md)
- [Recognition Boundary](../openetr/recognition.md)
- [The Machine Can Read the Document. But Should It Believe It?](https://trbouma.substack.com/p/the-machine-can-read-the-document)
- [UN Global Dialogue on AI Governance](https://www.un.org/global-dialogue-ai-governance/en)

