# Integration Model

OpenETR is intended to integrate with multiple independent systems.

The goal is not to require every participant to use one shared application. The goal is to make the signed control evidence portable.

OpenETR is not intended to replace existing ETR platforms, warehouse receipt systems, registries, document services, or trade networks. It is intended to work behind the scenes as a connective control fabric: self-generated object identifiers, signed control events, and graph links can be stored anywhere the signed event data is preserved, while existing systems keep their own user interfaces, databases, workflows, and rulebooks.

## Integration Styles

An implementation can use OpenETR by:

- importing the Python component;
- executing the CLI;
- wrapping OpenETR with REST APIs;
- using the demonstration FastAPI app;
- publishing and querying Nostr events directly;
- storing and replaying signed events locally.

## One Component, Multiple Modes

The reference implementation is intended to support both humans and agents.

```text
Human web UI
Agent REST/API calls
Human CLI
Agent CLI with --json
        ↓
shared OpenETR component
        ↓
identifier resolution
baseline or custom policy guards
event publication / query
structured verifier output
```

The web app provides human-facing pages and forms, while its REST APIs provide a machine-facing service boundary.

The CLI provides human-readable terminal output by default, while `--json` provides a machine-facing mode for agents, scripts, CI jobs, and automation.

All of these modes should route through the same OpenETR component and service layer so that object identifiers, participant resolution, guard policy, event construction, and verifier output remain consistent.

## Embedded Or Service Integration

An application can integrate OpenETR in either of two primary ways:

- embed the `openetr` component directly in its own runtime;
- call REST APIs exposed by a running OpenETR instance.

Embedded integration is useful when the host application wants OpenETR behavior inside its own process, account model, workflow, signing, logging, or deployment boundary.

REST integration is useful when the host application is not Python-based, wants an HTTP service boundary, or wants to share a running OpenETR service across several applications.

Both approaches should use the same OpenETR control-layer behavior underneath.

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
- [Multi-Modality Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/MULTI_MODALITY_ARCHITECTURE_NOTE.md)
- [Relay-Backed Configuration Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md)
- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
