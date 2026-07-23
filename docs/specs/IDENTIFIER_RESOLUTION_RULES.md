# Identifier Resolution Rules

## Status

Draft, reflecting the current OpenETR CLI and web application behavior.

## Purpose

OpenETR accepts human-friendly identifiers at application and command boundaries, but stores and publishes canonical cryptographic identifiers.

This note defines the expected resolution rules for:

- Controlled Object identifiers;
- participant, party, and entity identifiers;
- profile names;
- aliases;
- known entities.

The goal is to keep user input forgiving while keeping the wire format and stored event data deterministic.

## Core Rule

Human-facing input MAY accept friendly or encoded forms.

Internal state, event tags, query filters, and persisted protocol data SHOULD use canonical hex forms.

In practical terms:

- object references entered by a human may be `nobj` or 64-character hex;
- object digests used internally should be 64-character lowercase hex;
- participant references entered by a human may be a profile name, alias, `npub`, 64-character pubkey hex, or NIP-05 identifier;
- participant pubkeys used internally and in control event tags should be 64-character lowercase hex.

## Controlled Object Resolution

A Controlled Object is identified by the digest of the original record or artifact.

At a human input boundary, an implementation SHOULD accept:

1. `nobj` bech32 object identifier;
2. 64-character hex digest.

After resolution, the implementation MUST normalize the value to a 64-character lowercase hex digest before:

- querying relays;
- publishing `o` tags;
- building control graph state;
- storing local or relay-backed references;
- retrieving associated blobs by digest.

The `nobj` form is a display and input convenience. It is not the canonical stored form.

## Participant Resolution

Participant fields include roles such as:

- transferee;
- current controller;
- secured party or beneficiary;
- releasing party;
- warehouse operator or obligor;
- attestor;
- other action-specific subjects or counterparties.

At a human input boundary, an implementation SHOULD accept:

1. direct `npub`;
2. direct 64-character pubkey hex;
3. relay-backed profile name;
4. relay-backed alias;
5. NIP-05 identifier.

After resolution, the implementation MUST normalize the participant to a 64-character lowercase pubkey hex value before:

- publishing `p` tags;
- comparing signer identity;
- evaluating transfer acceptance;
- evaluating control graph state;
- storing participant references in protocol data.

The `npub`, profile name, alias, and NIP-05 forms are input and display conveniences. They do not change the Nostr event model.

## Recommended Precedence

When a single human-entered participant value could plausibly match more than one category, implementations SHOULD resolve in this order:

1. direct `npub`;
2. direct 64-character pubkey hex;
3. relay-backed profile name;
4. relay-backed alias;
5. NIP-05 identifier.

Direct cryptographic identifiers come first because they are explicit.

Profile names come before aliases because profiles answer a different question:

> Which operational signer identity is organized by this OpenETR root?

Aliases answer:

> What local nickname maps to a pubkey?

NIP-05 comes last because it requires external network resolution and may change outside the OpenETR relay-backed configuration.

## Profiles

A profile is an operational signer identity organized by an OpenETR root.

Resolving a profile name should produce the profile signer's public key.

Profile resolution does not mean:

- the root cryptographically owns the profile key;
- the profile is legally authorized for a role;
- the profile is recognized by a registry, statute, marketplace, or counterparty.

Those questions belong to the recognition layer.

For the root/profile model, see [Root and Profile Identity Model](./ROOT_AND_PROFILE_IDENTITY_MODEL.md).

## Aliases

An alias is a root-managed local nickname for an `npub`.

Resolving an alias should produce the aliased public key.

Alias resolution does not mean:

- the aliased party is trusted;
- the aliased party is legally recognized;
- the alias is globally meaningful;
- another OpenETR root will resolve the same alias the same way.

Aliases are local convenience mappings.

## Known Entities

Known entities are a root-managed familiarity list.

In the current model, known entities are stored as `npub` values rather than named entity records.

Known-entity status can be used by verifier policy to mark a signer or participant as familiar to the current OpenETR environment.

Known-entity status does not by itself resolve a human-entered name. If an implementation wants named entity lookup, the entity should also be represented as an alias, profile, registry record, attestation, or another explicit mapping.

Known-entity status does not prove legal identity, authority, trustworthiness, or recognition.

## NIP-05

NIP-05 identifiers may be accepted as human-friendly participant references.

When a NIP-05 identifier is resolved, the resolved Nostr pubkey should be normalized to 64-character lowercase hex before use in OpenETR event construction or comparison.

Because NIP-05 depends on external web-hosted data, implementations SHOULD treat it as a resolution input, not as final recognition evidence.

A recognition policy may require additional evidence such as:

- profile metadata;
- known-entity status;
- registry authorization;
- TRQP results;
- web-of-trust signals;
- explicit OpenETR attestations;
- domain-specific credentials.

## Resolution Is Not Recognition

Identifier resolution answers:

> Which cryptographic key does this input refer to?

It does not answer:

- Is this party legally who they claim to be?
- Is this party authorized for this role?
- Should this event be recognized as effective?
- Does this party satisfy a trust framework, registry, licensing, or accreditation rule?

OpenETR's control layer can record and verify signed evidence. Recognition depends on the verifier, domain profile, law, contract, registry, attestation, or institutional policy being applied.

## Guard Policy Extension Point

Resolution should happen before guard evaluation.

After object and participant identifiers have been normalized to canonical hex, the control-event publisher may apply guard policy.

The default OpenETR control guard policy evaluates questions such as:

- whether the signer is the current controller for a transfer initiation;
- whether the signer is the intended transferee for a transfer acceptance;
- whether a single active control chain can be resolved;
- whether a supplied prior event resolves back to an origin event;
- whether the target chain is ambiguous.

Implementations may need stricter or domain-specific guard behavior.

For example, a domain profile may require:

- registry recognition before a transfer can be initiated;
- an additional attestation before acceptance;
- a particular profile role for encumbrance or discharge;
- rejection of unknown entities rather than warning-only treatment;
- jurisdiction-specific lifecycle rules.

The component should therefore treat guard evaluation as a swappable policy layer.

The current component exposes a default guard policy through `ControlGuardPolicy` / `DefaultControlGuardPolicy` and allows service-layer publish functions to receive an alternate `guard_policy` implementation.

## Guards Are Not Cryptographic Enforcement

The default guard policy is a baseline application policy.

It helps the reference web app, CLI, and service layer apply the same checks before publishing control events. For example, the baseline policy can require the signer to be the current controller before initiating a transfer or terminating a control graph.

That does not mean the rule is cryptographically enforced across the whole network.

OpenETR events are signed Nostr events. A relay may accept a structurally valid event even if the reference component would have refused to publish it. A different implementation may also apply a different guard policy.

For that reason, guard results should be understood as evidence about the publishing path, not as final recognition.

A downstream verifier should still ask:

- Did the event signature and event id verify?
- Does the event fit the OpenETR wire format and graph shape?
- Which guard assumptions were applied by the publishing or verifying component?
- Are those assumptions sufficient for this verifier's legal, institutional, contractual, or operational context?
- Does a domain registry, trust framework, attestation, or local policy require additional checks?

The guard boundary is therefore:

```text
canonical hex identifiers
  -> baseline or custom guard policy
  -> event construction and publication decision
  -> downstream verifier policy and recognition decision
```

Passing a baseline guard means:

> This implementation found the event publishable under its configured OpenETR guard policy.

It does not mean:

> Every relying party must recognize this event as effective.

Custom guard policies should still preserve the canonical boundary:

```text
friendly input -> resolution -> canonical hex -> guard policy -> event construction
```

This keeps user-facing resolution, guard evaluation, and event serialization as separate concerns.

## Error Handling

If a human-entered identifier cannot be resolved unambiguously, implementations SHOULD fail before publishing an event.

Recommended behavior:

- show the unresolved input;
- state which field failed;
- state the accepted forms;
- avoid silently publishing an event with an unintended participant;
- require an explicit direct `npub` or hex key if named resolution is ambiguous.

## Wire Format Implication

OpenETR events SHOULD NOT store profile names, aliases, or NIP-05 identifiers as the authoritative participant identifier.

The authoritative participant reference in event tags should be the resolved pubkey hex.

Implementations MAY include human-readable references in content or auxiliary tags where useful, but those references should be treated as descriptive evidence rather than the canonical participant key.

## Summary

The resolution rule is:

```text
Object input:
  nobj or 64-character hex
  -> canonical 64-character object digest hex

Participant input:
  npub, 64-character pubkey hex, profile name, alias, or NIP-05
  -> canonical 64-character participant pubkey hex
```

OpenETR should be friendly at the edge and strict inside.

Canonical hex values are what the control graph stores, signs, queries, and verifies.
