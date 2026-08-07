# MLWR Warehouse Receipt Pilot Boundary Notes

This note captures pilot-design boundaries for using OpenETR with a warehouse receipt system.

It is based on the position that OpenETR is a correctness protocol for portable control evidence, not the reliable system, identity provider, KYC provider, account system, warehouse management system, registry, or federation operator.

## Status

Pilot note.

## Purpose

A warehouse receipt pilot needs a clean boundary between:

- the system that operates the warehouse receipt service
- the legal and operational identity controls around user accounts
- the OpenETR protocol events that record control-relevant facts
- the federation arrangements among participating system operators
- the attestation and recognition policies that give evidence practical effect

The compact model is:

```text
Reliable system:
  accounts, KYC, authorization, custody, document generation,
  operational controls, user experience, federation agreements

OpenETR correctness protocol:
  digest-identified objects, signed origin/control events,
  profile keys, control graphs, linked evidence, verifier output

Recognition layer:
  MLWR-style law, contracts, registry rules, platform rules,
  institutional policy, attestation requirements, relying-party decisions
```

OpenETR should exist between systems as portable evidence. It should not absorb the duties of those systems.

## Reliable System Versus Correctness Protocol

The pilot should distinguish a `reliable system` from a `correctness protocol`.

A reliable system is the operational environment that creates, manages, and governs warehouse receipt activity.

It may include:

- user accounts
- KYC and legal-identity onboarding
- role assignment
- warehouse operator authorization
- customer onboarding
- document generation
- warehouse management integration
- storage and access control for receipt content
- audit and compliance controls
- operational security
- business workflow
- support and dispute handling
- federation agreements with other operators

OpenETR is narrower.

It provides a correctness protocol for signed evidence about a controlled object.

It can answer:

- Which receipt artifact or package is identified by digest?
- Which profile key signed the origin event?
- Which control events refer to the same object?
- Which prior events are linked into the control graph?
- Which participant keys are named?
- Which attestations or linked evidence exist?
- What candidate control state can be derived under a selected verifier policy?
- What warnings arise from the graph?

It should not answer by itself:

- Was the user properly KYC'd?
- Is this account legally tied to the named person or organization?
- Is the warehouse operator licensed?
- Is the signer authorized under the pilot rulebook?
- Does this receipt satisfy statutory content requirements?
- Do federation partners recognize this account, key, receipt, or event?
- Is an attestation legally sufficient?

Those are reliable-system, domain-adapter, federation, and recognition questions.

## KYC And Account Boundary

OpenETR should not perform KYC.

KYC belongs to the host warehouse receipt system or to an integrated identity/compliance provider chosen by that system.

For the pilot, the host system should be responsible for:

- creating a user account
- tying that account to a legal person or legal entity
- performing or relying on KYC, KYB, AML, sanctions, or registry checks where required
- assigning account roles and permissions
- recording account lifecycle events
- deciding whether a user may issue, transfer, accept, encumber, discharge, redeem, or terminate a receipt
- maintaining the business record that links account identity to operational authority

OpenETR only sees the keys and signed events that the system permits to act.

The distinction is:

```text
account identity:
  who the system says the user or organization is

OpenETR key identity:
  which key signed the control event

recognition policy:
  whether the account-to-key binding and system controls are sufficient
```

## Account-Controlled Key Creation

In the pilot, account context may provide the secure environment used to generate or protect OpenETR keys.

The system may:

- create a root admin identity for the account
- create one or more operational profile keys
- protect signer material using account security controls
- store encrypted profile signer material
- require multi-factor authentication for sensitive actions
- separate administrative key access from operational signing access
- maintain logs tying key creation and use to the account

This does not mean OpenETR performs account management.

It means the reliable system creates an accountable operating environment in which OpenETR keys are generated, stored, selected, and used.

OpenETR's root/profile model remains:

```text
root admin identity:
  organizes the OpenETR environment and profile set

profile signer identity:
  signs operational OpenETR events

host account:
  provides the legal, operational, and security context around those keys
```

## Accountability Chain

Ultimate accountability in the pilot depends on linking the OpenETR key material to the host-system account.

The useful chain is:

```text
legal identity
  -> host-system account
  -> account roles and permissions
  -> root admin identity
  -> operational profile key
  -> signed OpenETR event
  -> warehouse receipt control graph
```

OpenETR can prove that a profile key signed an event.

The host system must be able to prove, or at least evidence under its rulebook, that:

- the account was tied to a legal identity
- the account was allowed to control the root or profile
- the profile key was created, imported, or activated under that account
- the signing action was authorized under the account's role and workflow
- any required internal approval, dual control, or attestation was satisfied

This account-to-key accountability record may be private to the host system, exposed through a registry, or provided as linked evidence.

OpenETR should not require private account records to be public. It should allow references, attestations, or verifier-policy hooks that make the relationship auditable when needed.

## Profiles And Roles

Pilot systems should avoid treating one account as always equivalent to one OpenETR signer.

A single account may control multiple profiles.

Examples:

- warehouse operator root
- facility issuer profile
- inventory-control profile
- finance-office profile
- system automation profile
- emergency recovery profile

Likewise, one legal entity may operate multiple accounts or facilities.

The pilot should define:

- which profiles may issue receipts
- which profiles may transfer control
- which profiles may attest facts
- which profiles may declare encumbrances
- which profiles may discharge encumbrances
- which profiles may redeem or terminate receipts
- whether profile use requires human approval or system automation

OpenETR records which key signed. The reliable system records why that key was allowed to sign.

## Federation Boundary

Federation is an arrangement among system operators.

OpenETR can provide portable signed control evidence that travels between systems, but it does not automatically create a federation.

Federation may require agreement on:

- participant onboarding
- KYC or KYB standards
- legal identity assurance
- account-to-key binding requirements
- profile naming or metadata conventions
- relay or archive infrastructure
- receipt document formats
- accepted domain tags
- attestation requirements
- verifier policies
- dispute resolution
- suspension, revocation, or emergency handling
- data sharing and privacy rules

The OpenETR graph can move between participants.

Recognition of that graph is a federation-policy decision.

```text
OpenETR portability:
  another system can inspect the signed object/control graph

Federation recognition:
  another system agrees to rely on that graph under shared rules
```

The pilot should therefore document federation rules separately from the OpenETR wire format.

## Attestation Boundary

Attestation fits naturally in OpenETR.

An attestation can be represented as a signed event or linked evidence about:

- the warehouse operator
- the account-to-key binding
- the receipt artifact
- goods custody
- inspection results
- insurance
- financing
- encumbrance status
- release or discharge
- registry status
- legal identity assurance
- system reliability
- federation membership

But the responsibility for requiring and evaluating attestations remains outside the OpenETR core.

The host system, federation rulebook, registry, or verifier policy should decide:

- which attestations are required
- who may issue them
- when they must be refreshed
- whether they are public or private
- whether missing attestations produce warnings or hard failures
- whether an attestation changes control or only supports recognition

OpenETR should record and retrieve attestation evidence. It should not decide universal attestation sufficiency.

## Pilot Event Responsibilities

The pilot should classify responsibilities this way.

| Responsibility | Reliable System | OpenETR | Recognition / Federation |
| --- | --- | --- | --- |
| User account creation | yes | no | may set requirements |
| KYC / KYB | yes | no | may require evidence |
| Legal identity binding | yes | no | evaluates sufficiency |
| Root/profile key generation context | yes | stores/signs through keys | evaluates controls |
| Receipt document creation | yes | hashes artifact | evaluates content |
| Origin event | authorizes action | signs/publishes event | evaluates signer authority |
| Transfer event | authorizes workflow | signs/publishes event | evaluates legal effect |
| Encumbrance/discharge | authorizes workflow | signs/publishes event | evaluates priority/effect |
| Attestation | requires and obtains | records signed evidence | evaluates sufficiency |
| Federation membership | negotiates and enforces | provides portable graph | recognizes participants |
| Verifier warnings | supplies policy inputs | computes graph warnings | decides effect |

## Pilot Design Principles

The pilot should use the following principles.

### Keep OpenETR Narrow

OpenETR should be responsible for correctness of the portable control graph:

- object digest correctness
- event signature correctness
- prior-event linkage
- graph reconstruction
- candidate state derivation
- signed evidence retrieval

### Keep The Host System Accountable

The host system should remain responsible for:

- legal identity
- account security
- KYC
- authorization
- operational controls
- document content
- business process
- private data custody

### Make Bindings Explicit

The pilot should explicitly record or reference:

- account-to-root binding
- account-to-profile binding
- profile-to-role binding
- receipt-to-origin binding
- transfer-to-prior-event binding
- attestation-to-object or attestation-to-event binding

These bindings may be public OpenETR events, private host-system records, registry records, or linked evidence, depending on the sensitivity of the data.

### Separate Cryptographic Validity From Recognition

A valid OpenETR signature means the key signed the event.

It does not automatically mean:

- the signer was KYC'd
- the signer was authorized
- the warehouse receipt is valid
- the goods exist
- the federation must accept the event
- a court must recognize the transfer

Those conclusions require recognition policy.

## Pilot Minimum Viable Architecture

A practical pilot can start with:

```text
warehouse receipt system
  -> account and KYC layer
  -> account-managed OpenETR root/profile keys
  -> receipt artifact or package
  -> OpenETR origin event
  -> OpenETR control events
  -> optional attestations and linked evidence
  -> verifier policy for pilot recognition
```

The first pilot does not need to solve every federation or recognition question.

It should demonstrate that:

- a warehouse receipt artifact can be digest-identified
- an account-authorized profile can sign an origin event
- later control events can link to the same object
- account-to-key accountability can be evidenced by the host system
- required attestations can attach to the graph
- another verifier can inspect the graph without being inside the original system
- recognition decisions remain policy-dependent

## Open Questions For The Pilot

- Which legal identity assurance level is required for warehouse operators?
- Which account roles may create root keys or profile keys?
- Should profile signer material be generated client-side, server-side, or in managed custody?
- How will the host system evidence account-to-key binding?
- Which profile types are needed for the first pilot?
- Which attestation types are mandatory for issuance?
- Which attestation types are mandatory for transfer, encumbrance, discharge, redemption, or termination?
- Which events must be public, private, or encrypted?
- Which relays or archives will participating operators use?
- What federation rulebook, if any, will pilot operators adopt?
- What happens when a profile key is compromised, rotated, suspended, or retired?
- What verifier output should distinguish cryptographic validity, reliable-system assurance, attestation sufficiency, and legal recognition?

## Related Documents

- [MLWR Warehouse Operator Issuance Use Case](./MLWR_WAREHOUSE_OPERATOR_ISSUANCE_USE_CASE.md)
- [OpenETR MLWR Profile Design Note](./OPENETR_MLWR_PROFILE.md)
- [Root And Profile Identity Model](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [System Integration Considerations](./SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [OpenETR MLETR And ETDA Mapping Design Note](./OPENETR_MLETR_ETDA_MAPPING_DESIGN_NOTE.md)
