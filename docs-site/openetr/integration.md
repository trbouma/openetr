# Integration Model

OpenETR is intended to integrate with multiple independent systems.

The goal is not to require every participant to use one shared application. The goal is to make the signed control evidence portable.

## Integration Styles

An implementation can use OpenETR by:

- importing the Python component;
- executing the CLI;
- wrapping OpenETR with REST APIs;
- using the demonstration FastAPI app;
- publishing and querying Nostr events directly;
- storing and replaying signed events locally.

## Relay-Backed State

OpenETR state can be relay-backed.

The minimal bootstrap can be as small as:

- root key or a reference to a root key;
- bootstrap/home relay list.

Profiles, profile settings, aliases, contacts, references, and signer material can then be discovered or recovered through relay-backed records, depending on the integration profile.

## No Runtime Dependency On Someone Else's Code

OpenETR's trust anchor is signed event data, not a particular hosted service.

Relays and APIs are useful distribution and integration mechanisms, but a relying party with the signed event set can verify signatures, inspect tags, traverse graph links, and apply policy independently.

This supports:

- public relays;
- private relays;
- local relays;
- local event stores;
- third-party services;
- direct protocol-level integration.

## Existing Account Systems

An existing account-based system can hide root keys and bootstrap relays behind its normal login and tenant model.

In that deployment:

- the host application controls the user experience;
- the Control Desk Key / root manages OpenETR profile configuration;
- profile keys sign operational events;
- verifier policy maps signed evidence to the system's business rules.

## Source Specs

- [System Integration Considerations](https://github.com/trbouma/openetr/blob/main/docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Relay-Backed Configuration Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md)
- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)

