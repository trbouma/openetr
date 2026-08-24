# Boundaries And Responsibilities

OpenETR works best when the integration boundary is explicit.

The host system should keep the responsibilities it already understands. OpenETR should provide portable signed evidence around the controlled record.

## Responsibility Split

| Host System Responsibility | OpenETR Responsibility |
| --- | --- |
| user login and account recovery | signed event construction |
| KYC, onboarding, and legal identity binding | profile-backed event attribution |
| document storage and rendering | object digest and event links |
| domain workflow and permissions | origin, control, and linked evidence events |
| business policy and approvals | verifier-policy inputs and warnings |
| registry, bank, or platform rulebook | portable evidence for recognition decisions |
| operational audit logs | independently verifiable object graph |

This boundary keeps OpenETR from becoming a hidden replacement for the host application.

## What OpenETR Does Not Do

OpenETR does not:

- perform KYC
- create user accounts
- decide legal title
- decide protected-holder status
- license warehouse operators
- certify carriers, banks, or authorities
- store every underlying document
- replace a registry
- replace a trade platform
- replace a wallet or credential system
- guarantee that physical goods exist

OpenETR can link to evidence from those systems. It should not pretend to be those systems.

## Reliable Systems And Correctness Protocol

An existing domain platform may be a reliable system.

It may manage:

- account creation
- identity checks
- role assignment
- document generation
- operational approval
- warehouse or carrier workflow
- registry admission
- customer support and dispute handling

OpenETR is a correctness protocol between and beneath those systems.

It helps preserve signed evidence that an action occurred against a particular controlled object.

The distinction is:

```text
reliable system:
  decides who can use the system and what workflow may run

OpenETR:
  records portable signed evidence of object control and lifecycle events
```

## Recognition Is External

OpenETR verification can show that:

- an event signature is valid
- the event references a controlled object digest
- the event links to a prior event
- the graph has a candidate current controller
- linked evidence exists
- warnings are present

It cannot decide, by itself, that a court, registry, bank, regulator, carrier, or warehouse must recognize the event.

Recognition depends on:

- law
- contracts
- registry rules
- platform rulebooks
- institutional policy
- domain adapter rules
- KYC or account evidence
- authority credentials
- verifier risk appetite

Read:

- [Recognition Boundary](../openetr/recognition.md)
- [Why Control Is Not Recognition](../policy-briefs/why-control-is-not-recognition.md)
- [Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)

## Key Custody Boundary

The host application may manage key custody in a passkey-style pattern.

Users may see ordinary product concepts:

- organization account
- facility
- operator
- bank
- receipt
- holder
- secured party
- action approval

They do not need to see raw root keys, relay configuration, or low-level event construction.

Even when the host application hides the cryptographic mechanics, the signed event data should remain independently verifiable.

Read:

- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [System Integration Considerations](https://github.com/trbouma/openetr/blob/main/docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)

## Evidence Boundary

OpenETR can link to outside evidence without ingesting everything.

Examples:

- LEI or organizational identity credentials
- KYC or account attestations
- warehouse inspection reports
- inventory records
- carrier registry references
- customs approvals
- bank financing documents
- platform registry status
- payment receipts

The linked evidence may be public, private, encrypted, off-platform, or available only to authorized verifiers.

OpenETR should record enough structured reference material for a verifier to know that the evidence exists and how it relates to the controlled object.
