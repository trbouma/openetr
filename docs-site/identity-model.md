# Identity Model

The Warehouse Receipts workspace uses business terms over the OpenETR root/profile identity model.

## Vocabulary

| Control Desk Term | OpenETR Technical Term |
| --- | --- |
| Warehouse Receipts workspace | MLWR operating surface / domain workspace |
| Control Desk Key | Root admin identity |
| Commitment Profile | Operational signer identity the desk can act as |
| Contact | External party the desk can address or transact with |
| Reference | External recognition, assurance, registry, KYC, assessment, audit, attestation, or policy source |
| Receipt control record | Signed OpenETR origin or control event |

## What The Categories Mean

| Category | Question Answered |
| --- | --- |
| Commitment Profile | Can this control desk act as this identity? |
| Acting Profile | Which Commitment Profile is currently selected to sign? |
| Contact | Can this control desk refer to this external party by a convenient name? |
| Reference | Can this desk or verifier consult this source for recognition context? |

Commitment Profiles are organized by the Control Desk Key.

The term **Commitment Profile** is the user-facing name for an operational OpenETR profile that can make signed commitments. The selected Commitment Profile is shown in the app as the **Acting Profile**.

Contacts are addressable but not controllable.

References are sources of recognition or assurance evidence. They are not automatically parties to a receipt transaction.

## Important Cryptographic Boundary

Commitment Profile keys are ordinary independent Nostr keypairs.

They are not cryptographically derived from the Control Desk Key. The Control Desk Key organizes access to Commitment Profiles and relay-backed configuration; operational events are signed by the selected Commitment Profile signer.

## Human And Agent Actors

OpenETR does not assign different protocol identities to humans and software agents.

A valid event signature proves that a particular key signed the event. It does not reveal whether the key was operated by a person, an agent, a service, a managed signer, or a workflow in which an agent proposed an action and a human approved it.

A Commitment Profile can therefore represent a person, organizational role, facility, service account, software agent, or controlled workflow. The host system remains responsible for authenticating users, constraining agent permissions, protecting signer keys, and retaining evidence of delegation or approval. Verifier policies and recognition systems decide whether those safeguards are sufficient for a particular domain or jurisdiction.

OpenETR may carry or link claims about an agent, provider, deployer, permission scope, or human approval. These are attributable evidence, not facts inferred from the key itself.

## Integration Pattern

This model is useful for existing systems:

- the host system can keep its normal account login;
- the Control Desk Key can be hidden behind that account context;
- Commitment Profiles can represent operational roles or facilities;
- contacts and references can be managed as business configuration;
- OpenETR events remain cryptographically signed and independently verifiable.

## Source Notes

- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Actor-Neutral Identity Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [System Integration Considerations](https://github.com/trbouma/openetr/blob/main/docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Relay-Backed Configuration Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md)
