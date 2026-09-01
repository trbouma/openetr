# Integration Model

OpenETR is intended to integrate with multiple independent systems.

The goal is not to require every participant to use one shared application. The goal is to make the signed control evidence portable.

OpenETR is not intended to replace existing ETR platforms, warehouse receipt
systems, registries, document services, or trade networks. It is intended to
work behind the scenes as a connective evidence layer: self-generated object
identifiers, signed control events, state transition rules, and graph links
can be stored anywhere the signed event data is preserved, while existing
systems keep their own user interfaces, databases, workflows, and rulebooks.

## Integration Styles

An implementation can use OpenETR by:

- importing the Python component;
- executing the CLI;
- wrapping OpenETR with REST APIs;
- using the demonstration FastAPI app;
- publishing and querying Nostr events directly;
- storing and replaying signed events locally.

## Suggested Integration Milestones

Integrators do not need to adopt every OpenETR surface at once. A practical integration can move through a few clear milestones.

| Milestone | Integration Question | OpenETR Concern |
| --- | --- | --- |
| Map domain terminology | What does the domain call the issuer, holder, controller, pledgee, secured party, receipt, record, or action? | Map domain words to OpenETR concepts such as Digital Artifact, Anchor record, control record, DCR, Commitment Profile, Acting Profile, contact, reference, and verifier policy. |
| Separate control from document movement | How do documents move today, and where should control evidence live? | Use OpenETR as the signed control layer while allowing PDFs, files, records, registry entries, or business documents to move through existing channels. |
| Define the host-system boundary | Which existing or new system owns users, accounts, workflow, documents, and policy? | Treat OpenETR as portable signed evidence underneath the host system rather than as the host system's application database. |
| Define authentication and recognition | How are users authenticated and recognized in the relevant domain or jurisdiction? | Let the host system, domain adapter, registry, KYC provider, trust framework, or verifier policy decide whether an actor is recognized for a particular role. |
| Choose an integration surface | Should the system embed OpenETR, call a service, execute the CLI, or implement the protocol directly? | Use the Python component, REST APIs, CLI `--json`, or direct wire-format integration according to the system architecture. |
| Choose a wire format strategy | Is the Nostr event format sufficient, or does the integrator need another transport or storage format? | Nostr is the initial OpenETR wire format, but the control model is portable. An integrator may choose another event, message, storage, or transport protocol if it preserves equivalent signed control evidence. |

The first milestone is often conceptual rather than technical. OpenETR becomes
easier to integrate once the domain-specific language is mapped to Digital
Artifacts, DCR evidence, state transition rules, and recognition policy. For
example, a warehouse receipt system may use warehouse operator, depositor,
holder, secured party, and receipt state, while OpenETR represents those
concerns through profiles, contacts, references, object ids, signed events,
and verifier output.

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

Both approaches should use the same OpenETR control-layer behavior underneath:
DCR evidence, state transition rules, and consequential-state derivation.

## Relay-Backed State

OpenETR state can be relay-backed.

The minimal bootstrap can be as small as:

- root key or a reference to a root key;
- bootstrap/home relay list.

Profiles, profile settings, aliases, contacts, references, and signer material can then be discovered or recovered through relay-backed records, depending on the integration profile.

## Stateless App Boundary

The strongest integration pattern is a stateless or mostly stateless host application.

In this pattern, the host application keeps its own product database, account model, document store, workflow state, and recognition policy. OpenETR provides the portable control evidence.

The host application may store very little OpenETR-specific local state:

- a Control Desk Key, root key, or reference to a managed key;
- bootstrap or home relays;
- optional cache/index data for performance.

Everything important for OpenETR control can be reconstructed from signed events:

- Commitment Profiles and profile configuration;
- Anchor records;
- control events;
- graph links;
- signer attribution;
- verifier warnings.

This means OpenETR can be added behind an existing application boundary without making OpenETR the application database.

## Passkey-Style Key Custody

OpenETR can be integrated in a way that feels similar to passkeys.

With passkeys, a device or platform keeps a private key on behalf of a user. The user normally does not see or handle the private key directly. The user sees meaningful application concepts such as accounts, devices, approvals, and sign-in prompts.

OpenETR can use the same product pattern.

For example, a warehouse receipt system may hide the Control Desk Key from the end user. The user signs in to the warehouse system as usual. The system then uses the Control Desk Key behind the scenes to discover and manage the OpenETR environment.

The user sees domain concepts:

- warehouse operator;
- facility;
- issuing Commitment Profile;
- Acting Profile;
- depositor;
- holder;
- secured party;
- receipt state.

The user does not need to see:

- root `nsec` material;
- relay bootstrap records;
- encrypted signer storage;
- low-level Nostr event construction.

The host application may expose Commitment Profiles, contacts, references, and receipt actions while hiding key custody and relay mechanics.

This does not change the cryptographic model. Commitment Profile keys still sign operational events, and relying parties still verify signed event data. The host app improves the user experience by managing key custody and presenting only meaningful domain controls.

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
- the Control Desk Key / root manages OpenETR Commitment Profile configuration;
- Commitment Profile keys sign operational events;
- verifier policy maps signed evidence to the system's business rules.

The OpenETR boundary should be clear:

| Existing application responsibility | OpenETR responsibility |
| --- | --- |
| User login and account recovery | Signed event construction |
| Product UI and workflow | Artifact identifiers and graph links |
| Document storage | Anchor and control-event publication |
| User permissions and roles | Commitment Profile-backed event attribution |
| Business policy and recognition | Verifier inputs and warnings |
| Caches and local indexes | Portable wire-format evidence |

This lets OpenETR provide portable evidence underneath the application rather
than acting as a competing product surface or owner of consequential state.

## Source Specs

- [System Integration Considerations](https://github.com/trbouma/openetr/blob/main/docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Multi-Modality Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/MULTI_MODALITY_ARCHITECTURE_NOTE.md)
- [Relay-Backed Configuration Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md)
- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
