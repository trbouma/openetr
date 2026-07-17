# Identity Model

The MLWR Control Desk uses business terms over the OpenETR root/profile identity model.

## Vocabulary

| Control Desk Term | OpenETR Technical Term |
| --- | --- |
| Control Desk | MLWR operating surface / workspace |
| Control Desk Key | Root admin identity |
| Profile | Operational signer identity the desk can act as |
| Contact | External party the desk can address or transact with |
| Reference | External recognition, assurance, registry, KYC, assessment, audit, attestation, or policy source |
| Receipt control record | Signed OpenETR origin or control event |

## What The Categories Mean

| Category | Question Answered |
| --- | --- |
| Profile | Can this control desk act as this identity? |
| Contact | Can this control desk refer to this external party by a convenient name? |
| Reference | Can this desk or verifier consult this source for recognition context? |

Profiles are controlled by the Control Desk Key.

Contacts are addressable but not controllable.

References are sources of recognition or assurance evidence. They are not automatically parties to a receipt transaction.

## Important Cryptographic Boundary

Profile keys are ordinary independent Nostr keypairs.

They are not cryptographically derived from the Control Desk Key. The Control Desk Key organizes access to profiles and relay-backed configuration; operational events are signed by the selected profile signer.

## Integration Pattern

This model is useful for existing systems:

- the host system can keep its normal account login;
- the Control Desk Key can be hidden behind that account context;
- profiles can represent operational roles or facilities;
- contacts and references can be managed as business configuration;
- OpenETR events remain cryptographically signed and independently verifiable.

## Source Notes

- [Root And Profile Identity Model](https://github.com/trbouma/etrix/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [System Integration Considerations](https://github.com/trbouma/etrix/blob/main/docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Relay-Backed Configuration Design Note](https://github.com/trbouma/etrix/blob/main/docs/specs/RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md)

