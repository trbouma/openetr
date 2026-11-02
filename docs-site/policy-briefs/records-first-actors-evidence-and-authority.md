# Records First: Actors, Evidence, And Authority

**Policy brief · 1 November 2026 · Non-normative**

## Executive Summary

Digital systems commonly organize trust around accounts and application
databases. A record is identified by a location inside a service, and its meaning
depends on what that service currently reports. This is convenient, but can make
identity, evidence and authority difficult to separate from the platform.

A records-first approach starts elsewhere: public keys identify cryptographic
actors, content digests identify particular Digital Artifacts, and signed events
express assertions connecting them. Applications help people create, find and
interpret evidence. An identified ruleset determines its consequential state;
relying parties decide whether to recognize that result for their purpose.

> Cryptography establishes verifiable bindings. It does not, by itself, establish
> truth, legitimacy or authority.

This brief explains that model and the role delegation could play within it.
It does not introduce a new event kind, amend OpenETR Core Record Ruleset 1.0,
or claim that general-purpose delegation is implemented. Delegation examples
below are proposals requiring explicit extension rules and security analysis.

## Actors, Actions, And Records

The model has a simple grammatical analogy:

```text
Actor → signed assertion of an action → identified record
```

A public key identifies the cryptographic actor. A SHA-256 digest identifies the
exact artifact bytes, subject to the hash function's security assumptions. A
signed event binds an assertion to its signer and the referenced object.

In linguistic terms, the actor resembles the agent and the record resembles the
patient or theme. The analogy is not literal: observing or endorsing an immutable
artifact does not modify it. What changes is the body of evidence concerning it
and, where applicable, the state derived under a ruleset.

Three identities must remain distinct:

| Identity | What it identifies | What it does not establish alone |
| --- | --- | --- |
| Actor public key | A cryptographic signing identity | A particular human, organization, trustworthy program or permission |
| Artifact digest | Particular bytes independently of their location | Truth, ownership, availability or continuity across edits |
| Evidence-event identifier | A particular assertion under its event format | Authority or the assertion's consequential validity |

An artifact digest is not automatically the identifier of an Anchor Event or
an entire Evidence Graph. The applicable wire format defines event identifiers
and signature commitments. Systems must not assume that every event identifier
commits to its signature bytes.

Changing artifact bytes produces a different digest. A stable business record
spanning versions therefore needs explicit relationships between those versions,
not an assumption that content addressing supplies continuity automatically.

## Applications Mediate; They Do Not Supply Universal Authority

An application may identify a person, authenticate a session and control access
to its own services. Those responsibilities do not make it the universal source
of identity or authority for every record it handles.

Bindings between a key and a person, organization or role can be supplied by
attestations and other evidence. Each relying party determines which bindings
are adequate for the decision at hand. Some interactions may require strong
institutional identification; others may need only continuity of key control.
The model moves identification to the boundary where it is needed, rather than
making a global identity provider a prerequisite for every assertion.

This is not an argument that lawful authorities or institutional mandates cease
to matter. It makes their role explicit: a registry, employer or public authority
may be authoritative for a defined question without becoming authoritative for
every relationship in the system.

OakGate illustrates the distinction. Its user login, wallet custody, service
identity and record-selection conventions serve different purposes. OakGate's
paths and sharing-label suffixes are application conventions, not OpenETR
authority rules. A recognizable handle or shortened fingerprint helps selection;
it does not prove provenance or grant access.

Custody also matters. An application holding a user's private key has practical
power to act with it. Portable evidence does not remove that power. Recovery,
export, departure and transparent custody arrangements remain necessary to
reduce dependence on the application.

## Delegation As Evidence

Delegation adds a relationship between actors:

> Actor A authorizes Actor B to perform action X concerning record R, subject
> to conditions C.

The grant and its exercise are distinct assertions. A signs the grant; B signs
an action referring to the grant on which it relies. The grant can itself be a
content-addressed artifact with signed evidence identifying the grantor. An
extension must specify the encoding and references so that the exact grant and
its signed evidence can be verified without ambiguity.

A proposed grant would need to identify:

- the grantor and delegate keys;
- permitted actions and precisely bounded objects or object classes;
- validity periods, intended audience and operational limits;
- whether further delegation is allowed, and how scope can only narrow;
- withdrawal, expiry and key-compromise handling;
- the rules under which the grant is interpreted.

Verification must start with a recognized source of authority. A signature from
A cannot establish that A was entitled to grant the power. A verifier must check
the authority chain, scope, conditions and relevant withdrawal evidence. Cyclic
or unsupported chains do not manufacture authority.

Authority to submit or sign an action is not necessarily transfer of control
over a record. Neither automatically grants access to encrypted contents or
permission to disclose them. Extensions must distinguish these powers.

Withdrawal adds evidence rather than erasing the grant. Whether it affects
earlier acts, how time is established, and what to do when withdrawal evidence
is unavailable must be specified. A missing withdrawal in an incomplete query
is not proof of continuing authority. Application replay controls and durable
verification of historical actions are separate requirements.

## Service Identity And Component Authority

The same model can apply to services. A stable service key could delegate a
narrow role to a replaceable component key—for example, issuing observation
receipts but not transferring control or spending funds.

This separates enduring identity from operational credentials. It also separates
operator commissioning, component delegation, runtime authentication and action
authorization. None is interchangeable with software certification or evidence
that a machine is uncompromised.

Such a design could complement workload-identity infrastructure. It should not
be described as equivalent to workload attestation merely because it uses signed
keys and grants. Credential issuance, isolation, rotation, revocation and
compromise recovery still need engineering and testing.

## Practical Usefulness

**Portable records.** A verifier can compare retrieved bytes with a known digest
without treating their current storage URL as their identity. Independent
verification still requires access to the necessary artifact and evidence.

**Cross-organization workflows.** Institutions can exchange records and signed
assertions without sharing one application database. Different recognition
policies remain possible and should be visible rather than concealed.

**Scoped service operation.** Explicit delegations could let a component act
within a limited role without possessing a service's root signing key.

**Independent observation.** A relay witness can provide separate evidence about
an observed signed event. Trust in the observer and its clock remains explicit;
witnessing does not certify the truth of the subject assertion.

**Historical reconstruction.** Corrections, withdrawals and superseding assertions
can remain inspectable alongside earlier evidence. This improves auditability
without making every authentic assertion valid or currently effective.

## Boundaries And Risks

Content addressing does not ensure storage or retrieval. Portable evidence
packages, replication and evidence-completeness reporting remain important.
Signatures do not prevent a compromised key from making new assertions, and
append-only retention does not make those assertions legitimate.

Digests and public relationships can reveal correlations; hashing predictable
content is not confidentiality. Sensitive artifacts and grants need appropriate
encryption, disclosure controls and retention policies. Preserving history must
not be presented as a universal obligation to publish personal information.

Rulesets can disagree, evidence can be incomplete, and legal recognition can
differ across jurisdictions. A defensible result identifies its rules, evidence
and uncertainty rather than implying universal acceptance.

## Implications For OpenETR

OpenETR Core Record Ruleset 1.0 supplies the anchor-and-publisher-notice baseline.
Transfer, delegated action and other consequential operations require applicable
extension rules; they are not implied by the presence of a signed event.

The next research step is a bounded delegation design with worked examples and
negative tests: unauthorized grantors, scope escalation, prohibited onward
delegation, expired grants, replay, key rotation, conflicting withdrawals and
unavailable evidence. Any normative proposal should define semantics before
assigning event kinds or presenting interoperability claims.

The guiding principle is:

> Keys identify actors. Digests identify artifacts. Signed evidence expresses
> assertions and proposed authority relationships. Rules determine consequential
> state; relying parties determine recognition.

## Related Reading

- [Policy Guards And Cryptographic Evidence](policy-guards-and-cryptographic-evidence.md)
- [Verifiable Agent Authority And OpenETR](verifiable-agent-authority-and-openetr.md)
- [Application Managed Keys And OpenETR](application-managed-keys-and-openetr.md)
- [Relays As Accountable Witnesses](relays-as-accountable-witnesses.md)
- [Preserving OpenETR Evidence](preserving-openetr-evidence.md)
- [Consequential State](../openetr/consequential-state.md)
