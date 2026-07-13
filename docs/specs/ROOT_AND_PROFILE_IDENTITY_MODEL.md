# Root and Profile Identity Model

This note describes how OpenETR organizes independent Nostr identities into a root-and-profile operating model.

It is intended to clarify the distinction between:

- cryptographic identity at the Nostr layer
- role assignment inside the OpenETR component
- operational signing authority for ETR events

## Status

Draft, reflecting the current OpenETR relay-backed configuration model and CLI behavior.

## Core Principle

Every OpenETR root or profile identity is an ordinary Nostr keypair.

At the Nostr layer:

- each `nsec` / `npub` pair is cryptographically independent
- there is no native parent-child relationship between keys
- one key does not derive authority from another key merely because OpenETR labels it as a profile
- relays see signed events from ordinary Nostr pubkeys

OpenETR adds an application-level organization model on top of those independent identities.

The root-and-profile model is therefore role-based, not key-type-based.

## Roles

A Nostr keypair may serve in one or more OpenETR roles.

### Root Admin Identity

The root admin identity is the key used by the OpenETR component to manage an OpenETR environment.

Its responsibilities may include:

- discovering relay-backed configuration
- publishing and updating configuration records
- managing the profile index
- managing aliases
- recovering profile configuration on another machine
- encrypting, decrypting, or otherwise accessing profile signer material where the implementation supports that

The root identity is administrative. It is not automatically the signer of operational ETR events.

### Profile Signer Identity

A profile signer identity is the key used to act as a named OpenETR profile.

Profile signers may publish operational events such as:

- ETR origin or issue events
- transfer initiate events
- transfer accept events
- attestation events
- encumbrance events
- discharge events
- redemption events
- termination events
- profile metadata

When a command publishes an ETR event, the event is signed by the active profile signer unless a command explicitly overrides the signer.

### Same Key, Different Roles

The same Nostr keypair may be used as both:

- the root admin identity
- an operational profile signer

This is allowed because the distinction is a role assignment made by OpenETR, not a different cryptographic key type.

For example, a solo or demonstration environment may use the root key as a profile signer for convenience.

However, using the same key for both roles weakens separation between administration and operational authorship.

In production-like usage, the recommended pattern is usually:

- root admin key for configuration, recovery, and profile management
- separate profile signer keys for day-to-day ETR event publication

## Component-Level Organization

OpenETR may organize multiple independent profile signers under a single root identity.

This means the root identity has operational knowledge of, or access to, the profile set through OpenETR's relay-backed configuration model.

It does not mean that profile public keys are cryptographically subordinate to the root public key.

The relationship is created by the OpenETR component through signed, relay-backed configuration and profile-secret management.

In practical terms:

- root controls the OpenETR environment
- profiles act within OpenETR workflows
- each profile remains an independent Nostr identity

## Profiles, Aliases, And Known Entities

OpenETR uses several root-managed lists of `npub` values, but they do different jobs.

The practical distinction is:

> Profiles are who this root can act as.  
> Aliases are what this root calls other `npub`s.  
> Known entities are which `npub`s this root is prepared to treat as familiar for baseline verifier warnings.

| Concept | Purpose | Effect |
| --- | --- | --- |
| Profile | Operational signer identity organized by the root | Can sign OpenETR events when selected as the active profile |
| Alias | Human-friendly nickname for an `npub` | Makes commands and displays easier; does not itself imply trust |
| Known entity | Root-managed familiarity list for external or internal `npub`s | Suppresses or changes unknown-entity verifier warnings depending on policy |

Profiles are delegated or organized operational identities.

For example, `warehouse`, `carrier`, `exporter`, or `bank` may be profiles. When a profile is active, OpenETR commands sign operational events with that profile's signer key.

Aliases are convenience labels.

For example, `consignee` may be an alias for a counterparty `npub`. The alias helps the user avoid pasting long bech32 identifiers. It does not mean the counterparty is authorized, trusted, or recognized.

Known entities are verifier-policy inputs.

They work like an SSH known-hosts file. If a signer or participant appears in the signed OpenETR graph but is not in the root's `known_entities` record, a baseline verifier can warn that the entity is unfamiliar to this OpenETR environment. The event may still be cryptographically valid.

The same `npub` may appear in more than one category.

For example:

- a profile signer may also have an alias;
- a counterparty alias may also be added as a known entity;
- a profile signer may be added to known entities so the verifier treats it as familiar in another context.

The categories should not be collapsed. They answer different questions:

- **Can I act as this identity?** Profile.
- **What short name do I use for this identity?** Alias.
- **Should this identity be treated as familiar during verification?** Known entity.

## Model Flexibility

The root-and-profile model is powerful because the root organizes access to identities without pretending to create their cryptographic authority.

At the Nostr layer, a profile key can exist independently before it is known to any OpenETR root. It may have its own public profile, history, counterparties, and operational reputation.

OpenETR can later add that profile signer to a root-managed environment by storing the profile configuration and encrypted signer material under the root's relay-backed configuration.

This means:

- a profile can be created inside one OpenETR environment and later imported into another;
- an existing external Nostr identity can become an OpenETR operational profile;
- one administrative root can organize many operational profiles;
- the same operational profile may be known to more than one administrative context where the signer secret has intentionally been shared;
- existing systems can map their own account, tenant, role, or custody model onto OpenETR profiles.

The important principle is:

> OpenETR does not pretend the root creates the identity. The root organizes access to identities.

That makes the model suitable for integration with existing systems while preserving independent signer attribution at the event layer.

## CLI Semantics

The current CLI reflects this distinction through separate commands.

### `openetr whoami`

`whoami` answers:

> Which profile signer am I currently acting as?

It shows the active profile and its resolved signer pubkey.

This is the identity used by ordinary operational commands unless overridden.

Examples include:

- `openetr issue-etr`
- `openetr transfer initiate`
- `openetr transfer accept`
- `openetr attest`
- `openetr encumber`
- `openetr discharge`
- `openetr redeem`
- `openetr terminate-etr`

### `openetr root`

`root` answers:

> Which root admin identity controls this OpenETR environment, and which profiles are organized under it?

It shows the root admin pubkey, home relays, the profile set, and the active acting profile.

By default it should not expose secret keys.

If a command provides an explicit secret-display option, such as `--nsec`, that output should be treated as sensitive recovery material.

## Authority Boundaries

The root identity's authority is administrative within the OpenETR component.

It does not automatically determine legal authority, title, mandate, or recognition.

Similarly, a profile signer can create signed operational events, but whether those events are recognized as effective depends on the relevant OpenETR policy, attestation model, institutional rules, or legal framework.

This note is therefore about OpenETR component organization, not about legal effect.

## Summary

OpenETR profiles are ordinary independent Nostr identities organized by the OpenETR component under a root administrative identity.

The root may also be a profile, but root and profile are roles, not different cryptographic key classes.

The practical distinction is:

- `root`: the identity that manages and recovers the OpenETR environment
- `profile`: the identity that signs operational events
- `whoami`: the active profile signer
- `root`: the administrative identity and profile set
