# OpenETR And Managing Digital Identity Review Note

## Status

Draft policy and architecture analysis, 2026-09-03.

## Source

This note reviews the UK National Audit Office (NAO) report [*Managing digital
identity*](https://www.nao.org.uk/insights/managing-digital-identity/), published
2 September 2026 as HC 586, Session 2026-27.

The report draws lessons from UK initiatives and international experience. It
does not evaluate a particular identity programme. OpenETR uses those lessons
as architectural and delivery guidance, not as an endorsement by the NAO.

## Executive Assessment

The report is directly relevant to OpenETR's identity boundary, even though
the two subjects are different.

The report is primarily concerned with person-centric digital identity:
identification, authentication, credentials, wallets, public services, trust
frameworks, record matching, privacy, adoption, and value for money.

OpenETR is primarily concerned with object-centric evidence: identifying an
exact Digital Artifact, recording attributable consequential actions in a
Digital Controllable Record (DCR), and deriving Consequential State under
stated rules.

The relationship is complementary:

```text
digital identity and host account
  -> establish and authenticate the actor
  -> present credentials, attributes, roles, or mandates

OpenETR Commitment Profile
  -> signs an object-specific consequential statement
  -> contributes evidence to the Digital Artifact's DCR

verifier and recognition policy
  -> evaluates identity, authority, DCR evidence, and applicable rules
  -> determines whether to rely on the state and what effect it receives
```

The report strongly supports OpenETR's decision not to infer real-world
identity or authority from a public key. It also exposes areas where OpenETR's
integration guidance should become more precise, particularly delegated
authority, contextual identifiers, privacy, revocation, account matching,
accessibility, recovery, and assurance levels.

No immediate change to OpenETR event kinds or core Nostr wire format is
required.

## 1. The Report's Identity Model

The report separates three basic functions:

| Function | Question |
| --- | --- |
| Identification | Who is the person or organization? |
| Authentication | Is the presenter the legitimate controller of that identity? |
| Credential or attribute proof | What trusted fact can the presenter prove? |

It also distinguishes three systems problems that are often mistakenly
collapsed:

| Problem | Question |
| --- | --- |
| Verification | Has the claimed identity been established to the required assurance? |
| Matching | Which record in this system belongs to that identity? |
| Linking | Which records in different systems refer to the same identity? |

These distinctions are important because identity proof does not automatically
repair inconsistent data, resolve duplicate accounts, or connect legacy
records. A credential can be valid while the relying system still matches it
to the wrong customer record.

The report further treats digital identity as an ecosystem rather than one
product. Government, private providers, identity services, attribute services,
wallets, orchestration services, component providers, standards bodies,
regulators, and relying parties may all perform different functions.

## 2. Mapping To OpenETR

### 2.1 Functional mapping

| Digital identity concern | OpenETR concept | Boundary |
| --- | --- | --- |
| Digital identifier | Commitment Profile `npub` | Identifies a signing key, not automatically a person or legal entity. |
| Authentication | Event signature | Proves control of the private key for that event. |
| Host login | Account session, passkey, IAM, or other authentication | Belongs to the integrating application. |
| Identity proofing | KYC, registry, wallet, credential, or identity provider | External to the base protocol. |
| Attribute proof | Credential, attestation, or linked evidence | May be referenced by OpenETR and evaluated under policy. |
| Holder service or wallet | Wallet or credential store | Complements OpenETR; a DCR is not a personal wallet. |
| Delegated authority | Mandate, approval, account role, or delegation evidence | Must connect principal, operator, signer, scope, and time. |
| Record matching | Mapping from account or organization record to `npub` | Host-system responsibility. |
| Cross-system identity linking | Registry, trust framework, pairwise mapping, or attestation | Recognition concern requiring an explicit policy basis. |
| Trust framework | TRQP, DVS-style framework, registry, accreditation, or local policy | Determines which identity evidence is accepted. |
| Identity assurance level | Risk-based verifier requirement | May vary by action, domain, and consequence. |
| Credential revocation | Status or revocation service | Must be checked when current validity matters. |
| Consequential record history | Digital Controllable Record | OpenETR's principal contribution. |

### 2.2 What an OpenETR signature establishes

For a valid event, OpenETR can establish that:

- a particular public key signed the exact event;
- the event concerns a digest-identified Digital Artifact;
- the event contains particular signed tags and content;
- its event references participate in a candidate DCR graph; and
- stated protocol rules produce a particular candidate Consequential State.

The signature does not establish that:

- the key belongs to the named person or organization;
- the operator passed an identity-proofing process;
- the host authenticated the correct account holder;
- the operator was authorized to use the Commitment Profile;
- a delegation or approval was current and in scope;
- profile claims match records in another system;
- a credential issuer is recognized;
- a signed assertion is factually true; or
- the event has legal, regulatory, institutional, or commercial effect.

This is the same separation OpenETR applies to human, organizational, service,
and agent-operated keys.

## 3. Verification, Matching, Linking, And Recognition

The report's separation of verification, matching, and linking provides a
useful extension to OpenETR's layered model.

### 3.1 Cryptographic verification

OpenETR first verifies the event itself:

```text
event bytes -> event ID -> signature -> signer npub
```

This is deterministic and portable.

### 3.2 Host-system matching

The host must associate the signer or operator with the correct internal
record:

```text
authenticated account
  -> organization, facility, employee, service, or agent record
  -> permitted Commitment Profile
```

That association may be wrong, stale, duplicated, or incomplete even when the
OpenETR signature is valid.

### 3.3 Cross-system linking

A verifier may need to decide whether several identifiers represent the same
actor:

```text
npub
  <-> host account ID
  <-> company registration number
  <-> LEI or local registry identifier
  <-> wallet subject or credential identifier
  <-> NIP-05 address
```

OpenETR should not silently equate these identifiers. A registry response,
attestation, credential, contractual mapping, or other evidence should support
the link, and policy should say which source is authoritative.

### 3.4 Recognition

Recognition asks whether the verified and matched actor is acceptable for the
specific action. A verifier might require a licensed warehouse operator for an
Anchor, a recognized bank for an encumbrance, or a duly authorized officer for
a discharge.

The same identity may be recognized for one action and not another. Recognition
is contextual, not a permanent property of an `npub`.

## 4. Delegated Authority

The report identifies delegated authority as essential and notes that identity
systems built only for individual account holders can fail where employees,
professional agents, carers, businesses, or other representatives must act for
someone else.

This is especially relevant to OpenETR. A consequential action may involve:

```text
principal
  the person or organization on whose authority the action is taken

operator
  the human, service, workflow, or agent initiating the action

signer
  the Commitment Profile or signing service producing the event signature

approver
  a person or system supplying a required approval
```

These roles may be combined, but an integration should not assume they are the
same.

### 4.1 Minimum delegation questions

A high-assurance integration should be able to determine:

- who granted the authority;
- to whom it was granted;
- which Commitment Profile may be used;
- which actions and object classes are permitted;
- whether the authority is limited to a tenant, facility, jurisdiction, or
  counterparty;
- when it begins and expires;
- whether it is single-use or reusable;
- whether further delegation is permitted;
- how it is suspended or revoked;
- whether required approval was obtained; and
- whether the authority remained current at the protected signing or execution
  boundary.

### 4.2 OpenETR placement

The base protocol should not require one delegation technology. Evidence may
come from:

- host IAM and role assignments;
- wallet-presented credentials;
- signed attestations;
- trust-registry queries;
- contractual mandates;
- professional or corporate registries;
- authorization services; or
- local policy records.

OpenETR can link or commit to that evidence. The host controls access to the
signer, and the verifier decides whether the delegation is sufficient.

## 5. Identifier Privacy And Correlation

The report warns that using one personal identifier across many services can
increase security and privacy consequences. It describes tokenization and
sector-specific identifiers as possible mitigations.

The OpenETR equivalent risk is reuse of one public key across unrelated
domains, transactions, customers, or jurisdictions. Public events can make
activity correlation easy even when the underlying documents remain private.

### 5.1 Existing mitigation

OpenETR's independent Commitment Profiles already provide the right primitive:

- the Control Desk Key can remain an administrative and recovery key;
- separate Commitment Profiles can be used for operational contexts;
- profiles need not be cryptographically derived from one public root;
- domain systems can map their own account and tenancy boundaries to profiles;
  and
- private organizational relationships need not be published as protocol
  facts.

### 5.2 Recommended guidance

OpenETR should recommend that production integrations:

- do not use the Control Desk Key for ordinary operational signing;
- consider separate Commitment Profiles by organization, role, domain,
  facility, tenant, or risk boundary;
- avoid publishing unnecessary personal or organizational metadata;
- treat cross-profile and cross-system linking as explicit recognition
  evidence;
- account for correlation through event timing, relay choice, tags, and object
  references;
- define secure key rotation and continuity evidence; and
- retain sensitive mappings in appropriately protected host systems.

This is contextual separation, not anonymity. A relying party may still need a
strong, accountable mapping to a legal person or organization.

## 6. Wallets And Verifiable Credentials

The report expects phone-based wallets and verifiable credentials to play an
increasing role. It also emphasizes that a credential requires supporting
infrastructure so a verifier can check issuer, integrity, and validity rather
than relying on visual presentation.

OpenETR and wallets remain complementary:

```text
wallet or credential system
  proves identity, attribute, role, eligibility, or mandate

OpenETR
  records the signed action concerning the Digital Artifact
  and derives its DCR state

relying party
  evaluates both under its policy
```

A wallet presentation may support recognition of a Commitment Profile without
becoming part of the public DCR. Depending on privacy and replay requirements,
the integration may retain:

- the presentation locally;
- a digest commitment to the presentation;
- a minimal signed attestation;
- a status or registry reference; or
- no durable identity evidence beyond an internal audit record.

The design must also specify how expiry and revocation are checked. A
credential that was once valid is not necessarily current authority for a new
consequential action.

## 7. Assurance Levels And Proportionality

The report notes that identity systems use different assurance levels because
not every service presents the same risk. OpenETR should apply the same
principle at the recognition and integration layers.

Examples:

| OpenETR action | Possible assurance posture |
| --- | --- |
| Query a public DCR | No user identity required. |
| Publish non-consequential linked evidence | Authenticated signer and basic policy checks. |
| Create a warehouse receipt Anchor | Recognized warehouse Commitment Profile and protected signer access. |
| Transfer control | Current-controller verification, authenticated operator, target binding, and fresh authorization. |
| Record or discharge an encumbrance | Recognized secured party or authorized operator, referenced encumbrance, and current authority. |
| Redeem or terminate a record | Strong authentication, lifecycle checks, and domain-specific approvals. |

These are profile and policy decisions, not different signature algorithms.

## 8. Public And Private Roles

The report finds multiple viable international delivery models: state-led,
co-regulated, and plural-provider ecosystems operating under shared rules.

OpenETR is compatible with all three:

- a government or registry can operate an authoritative domain profile;
- accredited private providers can supply identity or verification services;
- multiple providers can issue or verify evidence under a shared framework;
- a private network can apply contractual recognition rules; and
- independent verifiers can apply different policies to the same DCR evidence.

The OpenETR protocol should not require one institutional model. Its role is to
make the object-specific evidence portable enough for each model to use.

Known entities, Contacts, and References must also remain carefully bounded:

- a **Contact** is an addressable counterparty;
- a **Reference** is a source of identity, authority, assurance, or recognition
  context;
- a local known-entity record expresses familiarity under local policy; and
- none of these labels is universal certification.

## 9. Delivery And Adoption Lessons

The report's delivery findings are highly relevant to OpenETR as a project.

### 9.1 Start with outcomes and processes

Technology should follow a clear use case, process boundary, data model, and
integration plan. OpenETR's warehouse-operator workflow is therefore a sound
starting point: issue a receipt artifact, create its Anchor, and establish its
initial DCR state.

### 9.2 Identity is not the whole integration

Adding identity proof does not solve document storage, data quality, record
matching, workflow, authorization, or legal effect. OpenETR integrations should
map all of those responsibilities rather than treating a recognized `npub` as
the complete solution.

### 9.3 Build on existing providers and standards

OpenETR should consume recognized identity and credential systems rather than
reimplementing them. This includes passkeys, enterprise IAM, wallets,
verifiable credentials, trust registries, and regulated identity providers.

### 9.4 Make the user benefit visible

Users should see receipt, holder, pledge, release, presentation, and delivery
workflows. They should not be required to understand private keys, relay
queries, or identity-framework plumbing.

### 9.5 Plan for recovery and inclusion

A key-based system needs practical recovery, assisted operation, accessibility,
and non-digital alternatives where the domain requires them. The Control Desk
Key recovery model must not become the only way a person can obtain help or
exercise a legal right.

### 9.6 Define accountability

An integration should identify responsibility for:

- identity proofing;
- account authentication;
- profile-key custody;
- role and delegation management;
- verifier policy;
- credential and registry availability;
- incorrect matching;
- security incidents;
- disputed actions;
- recovery and redress; and
- operational and legal effect.

## 10. Warehouse Receipt Example

A warehouse receipt implementation illustrates the full separation:

```text
warehouse employee authenticates to host system
  -> host matches employee to warehouse and role records
  -> credential or registry confirms warehouse status where required
  -> host policy authorizes use of warehouse Commitment Profile
  -> Commitment Profile signs Anchor for exact receipt digest
  -> OpenETR verifies event and reconstructs DCR
  -> MLWR or local verifier evaluates identity and control evidence
  -> relying party determines recognition and effect
```

For a later discharge:

```text
bank officer authenticates
  -> host matches officer to bank account and delegated role
  -> current mandate and credential status are checked
  -> bank Commitment Profile signs discharge referencing encumbrance
  -> OpenETR derives candidate unencumbered state
  -> warehouse, transferee, registry, or court applies its rule book
```

At no point does the `npub` alone establish that the signer is a licensed
warehouse, bank, employee, or authorized agent.

## 11. Design Consequences

### 11.1 No immediate wire-format change

The report does not justify adding personal identity fields to core OpenETR
events. Doing so could create false assurance, unnecessary disclosure, and
cross-context correlation.

### 11.2 Strengthen existing documentation

OpenETR documentation should explicitly distinguish:

- identification;
- authentication;
- credentials and attributes;
- authorization and delegation;
- signer attribution;
- record matching;
- cross-system identity linking;
- verifier recognition; and
- operational or legal effect.

### 11.3 Develop a delegated-authority profile

A future design note should define a technology-neutral evidence model for:

- principal, operator, signer, and approver;
- scope and target binding;
- issue, activation, expiry, suspension, and revocation;
- single-use and further-delegation constraints;
- current-status checking; and
- privacy-preserving references to external authorization evidence.

This should be optional and domain-driven rather than mandatory for every
OpenETR event.

### 11.4 Add contextual-profile privacy guidance

The root-and-profile identity note should explain when separate Commitment
Profiles reduce correlation and why the Control Desk Key should normally
remain out of public operational history.

### 11.5 Make recognition evidence observable

Machine-readable verifier output should identify, where policy permits:

- which identity or authority evidence was consulted;
- the evidence source and status time;
- issuer or registry recognition;
- assurance level;
- matching basis;
- warnings or unresolved conflicts; and
- whether the evidence affected protocol state, recognized state, or only a
  user-facing risk decision.

### 11.6 Preserve actor neutrality

The report is person-centric, but OpenETR should remain actor-neutral. The same
cryptographic model can support people, organizations, services, and agents.
Integrating systems determine what additional identity, supervision, or
accountability evidence each actor class requires.

## 12. Policy Conclusions

The report reinforces five OpenETR policy positions.

1. **A cryptographic identifier is not a complete identity.** It must be placed
   in an institutional, organizational, and assurance context.
2. **Authentication is not authorization.** Control of a key does not establish
   permission to perform every consequential action.
3. **Credentials are recognition inputs.** Their issuers, validity, status, and
   applicability still need to be evaluated.
4. **Identity reuse does not solve record integration.** Matching and linking
   remain separate responsibilities.
5. **OpenETR should complement identity infrastructure.** It should use
   identity evidence to support object-specific actions rather than becoming a
   general identity platform.

The resulting architecture can be summarized as:

```text
identity systems establish who may be acting
host systems authenticate, match, authorize, and control signer access
OpenETR records attributable consequential evidence about the artifact
verifier policies derive state and evaluate recognition inputs
relying systems and law determine effect
```

This is a strong fit with OpenETR's layered architecture. The report does not
call for a broader identity protocol inside OpenETR; it calls for clearer
integration boundaries around the identity systems OpenETR will encounter.

## Related OpenETR Documents

- [Root And Profile Identity Model](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Actor-Neutral Identity Design Note](./OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [EUDI Wallet And OpenETR](./EUDI_WALLET_AND_OPENETR_DESIGN_NOTE.md)
- [Organizational Reference Layer](./OPENETR_ORGANIZATIONAL_REFERENCE_LAYER_DESIGN_NOTE.md)
- [TRQP Integration Note](./OPENETR_TRQP_INTEGRATION_NOTE.md)
- [Nostr Web Of Trust Integration Note](./OPENETR_NOSTR_WEB_OF_TRUST_INTEGRATION_NOTE.md)
- [Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [System Integration Considerations](./SYSTEM_INTEGRATION_CONSIDERATIONS.md)

