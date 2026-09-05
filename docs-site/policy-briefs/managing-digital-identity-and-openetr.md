# Managing Digital Identity And OpenETR

The UK National Audit Office report [*Managing digital
identity*](https://www.nao.org.uk/insights/managing-digital-identity/) draws
together lessons from digital identity initiatives in the UK and other
countries. Its findings are relevant to OpenETR because every signed record has
an actor, but they also show why OpenETR should not become a general-purpose
identity system.

Digital identity and OpenETR answer different questions:

```text
Digital identity:
  Who is this actor, is the presenter authentic, and what can they prove?

OpenETR:
  What signed evidence exists concerning this exact Digital Artifact,
  and what Consequential State follows under stated rules?
```

The two layers are complementary.

## Identity Is More Than A Key

OpenETR represents a signer with a public key, normally displayed as an
`npub`. A valid event signature proves that the corresponding private key
authorized the event. It does not prove that the key belongs to the person,
business, warehouse, bank, service, or agent named in a profile.

An integrating system may rely on additional evidence:

- an authenticated account;
- an identity-proofing service;
- a wallet-held credential;
- KYC or organizational onboarding;
- a professional or business registry;
- a trust-registry response;
- an attestation from a recognized authority; or
- a contractual mandate or delegation.

OpenETR can link to that evidence. The applicable verifier or recognition
policy decides whether it is sufficient.

## Five Questions, Not One

The report usefully distinguishes identity verification from matching and
cross-system linking. For OpenETR, five questions should remain separate:

1. **Was the OpenETR event signed correctly?**
2. **Which real-world actor does the signing key represent?**
3. **Which account or organizational record corresponds to that actor?**
4. **Was the actor authorized for this action at this time?**
5. **Will the relying party recognize the action and resulting state?**

A system can answer the first question perfectly and still answer one of the
others incorrectly. Cryptographic verification does not repair poor source
data, duplicated accounts, stale role assignments, or mistaken identity
matching.

## Delegation Is Central

Many important actions are performed on behalf of someone else. Employees act
for companies, professional agents act for clients, services act for account
holders, and software agents operate under organizational policies.

OpenETR integrations should distinguish:

| Role | Meaning |
| --- | --- |
| Principal | Person or organization on whose authority the action is taken. |
| Operator | Human, service, workflow, or agent initiating the action. |
| Signer | Commitment Profile or signing service creating the OpenETR signature. |
| Approver | Actor or system supplying any required approval. |

Those roles may be performed by one actor, but they should not be assumed to
be identical.

A high-assurance system may need evidence of delegation scope, permitted
actions, target, start time, expiry, revocation, further delegation, and current
authority at the point of signing or execution.

The OpenETR protocol does not mandate one delegation technology. The host
system controls signer access, identity and authorization systems provide the
supporting evidence, and verifier policy determines whether that evidence is
acceptable.

## Commitment Profiles And Privacy

The report highlights the privacy and security risks of reusing one identifier
across many services. The equivalent OpenETR risk is using one `npub` in every
domain and transaction, making otherwise separate activity easy to correlate.

OpenETR's root-and-profile model provides a practical response:

- keep the Control Desk Key for administration and recovery;
- use separate Commitment Profiles for operational signing;
- consider different profiles for different organizations, facilities, roles,
  tenants, domains, or risk contexts;
- publish only the metadata needed by the intended verifier; and
- make cross-profile identity linking an explicit recognition decision.

Separate profiles do not create anonymity. They let an integrating system
limit unnecessary correlation while retaining accountable mappings where law
or policy requires them.

## Wallets And Credentials Complement The DCR

Digital wallets and verifiable credentials are holder-centric. They help a
person or organization present identity, attributes, eligibility, roles, or
mandates.

OpenETR is object-centric. It creates a DCR containing signed evidence about a
digest-identified Digital Artifact and derives Consequential State from that
evidence.

Together, they can support a complete interaction:

```text
wallet credential establishes identity, role, or mandate
  -> host system authenticates and authorizes the operator
  -> Commitment Profile signs an OpenETR record
  -> DCR evidence is validated and consequential state is derived
  -> relying party applies its recognition policy
```

A credential must still be checked for issuer recognition, integrity, status,
expiry, and applicability. A credential that was valid in the past is not
automatically current authority for a new action.

## A Warehouse Receipt Example

When a warehouse employee issues a receipt, several layers are involved:

```text
employee account and authentication
  -> matching to the correct warehouse and role
  -> warehouse licence or registry evidence
  -> authorization to use a warehouse Commitment Profile
  -> signed Anchor for the exact receipt digest
  -> DCR reconstruction and consequential-state derivation
  -> recognition under MLWR, local law, registry rules, or contract
```

OpenETR handles the object-specific signed DCR evidence and derives
Consequential State. It does not
perform employee onboarding, license the warehouse, or decide the legal effect
of the receipt.

This division lets the warehouse system hide keys and relay mechanics behind a
normal account experience while preserving evidence that another system can
verify independently.

## Delivery Lessons

The report's broader programme lessons also apply to OpenETR adoption:

- start with a clear use case and measurable user benefit;
- understand existing processes and legacy integration before adding
  technology;
- build on existing identity providers, wallets, standards, and trust
  frameworks;
- define public, private, and provider responsibilities explicitly;
- design privacy, security, recovery, accessibility, and redress from the
  beginning;
- use risk-proportionate assurance rather than one identity requirement for
  every action; and
- explain clearly what the technology does and does not establish.

This supports OpenETR's warehouse-first approach. A complete operator workflow
is a better proof point than a claim to solve digital identity generally.

## The OpenETR Position

The report reinforces a concise identity boundary:

```text
Identity systems establish who may be acting.
Host systems authenticate, match, authorize, and control signer access.
OpenETR records attributable consequential evidence about the artifact.
Verifier policies evaluate the DCR and recognition inputs.
Relying systems and law determine effect.
```

No immediate OpenETR wire-format change is needed. The priority is clearer
integration guidance around contextual profiles, delegated authority,
credential status, privacy, matching, and recognition.

## Read More

- [Detailed OpenETR analysis](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_AND_MANAGING_DIGITAL_IDENTITY_REVIEW_NOTE.md)
- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Actor-Neutral Identity Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [EUDI Wallet And OpenETR](./eudi-wallet-and-openetr.md)
- [OpenETR, Trust Frameworks, And Registries](./openetr-trust-frameworks-and-registries.md)
