# Nostr, DIDs, And Independent Verification

## The Policy Question

Digital identity systems often make three core promises:

1. a globally unique identifier;
2. access to cryptographic verification material; and
3. discovery of services or ways to interact with the identified party.

W3C Decentralized Identifiers provide a general framework for these functions.
OpenETR's initial Nostr binding addresses the same practical needs more
directly when the identifier is intended to identify a signing key.

The important policy question is not which technology has more features. It
is which dependencies are necessary for independently verifiable records.

## A Records-First Decision

OpenETR considered W3C DIDs as a possible identity foundation. Choosing Nostr
as the initial protocol was not a judgment against DIDs. It reflected
OpenETR's decision to begin with records rather than with a general-purpose
identity layer.

```text
DID architecture:
  identify a subject -> resolve keys and services -> verify interactions

OpenETR architecture:
  identify an artifact -> verify signed events -> derive consequential state
```

OpenETR needs to know which key signed an event concerning an exact Digital
Artifact. Whether the key represents a recognized person, organization,
warehouse, bank, authority, service, or agent remains a separate recognition
question.

That boundary gives OpenETR broader applicability. Different industries,
organizations, trust frameworks, and jurisdictions can evaluate the same DCR
evidence without first agreeing on one DID method, credential format,
identity provider, or recognition regime.

Nostr supplies both a signed-event format and a replicable distribution model.
Events can be published to multiple relays, retained in archives, exported as
evidence packages, or stored locally. No relay guarantees permanence, but no
one relay is the exclusive cryptographic authority for an event. Once the
signed evidence is held, verification does not require the original
application, platform, database, service, signer, or publishing relay to remain
available.

> OpenETR selected Nostr as its initial protocol because its key-native,
> independently verifiable, relay-replicable event model provides a small and
> durable foundation for a records-first evidence and state-derivation model.

DIDs remain useful optional inputs wherever an integration needs persistent
subject identity, key rotation, multiple verification methods, credentials,
or service discovery. OpenETR can use that evidence without making it a
prerequisite for validating every control event.

## Two Different Starting Points

A DID is a URI containing a DID method and method-specific identifier. The
method defines how the DID is created, resolved, updated, and deactivated. The
resolved DID document can contain verification methods and service endpoints.
[W3C DID Core](https://www.w3.org/TR/did/)

Nostr starts with a public key. The human-facing `npub` is a bech32 encoding of
that key. A Nostr event includes the author key, signed data, event id, and
signature, so another implementation can verify the event without first
resolving a separate identity document. [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md),
[NIP-19](https://github.com/nostr-protocol/nips/blob/master/19.md)

The distinction can be stated simply:

> A DID resolves to cryptographic identity material. A Nostr public-key
> identifier is cryptographic identity material.

## The Closer Comparison: did:key

The `did:key` method is much closer to Nostr than `did:webvh`. It directly
encodes public-key material together with a key-type identifier. A resolver
expands that material deterministically into a DID document without consulting
DNS, a registry, a hosted file, or a network service.
[did:key Method v0.9](https://w3c-ccg.github.io/did-key-spec/)

The two approaches share important properties:

- the identifier is derived directly from public-key material;
- the public key can be recovered without network retrieval;
- resolution or decoding can occur locally;
- changing the key changes the identifier; and
- rotation, deactivation, recovery, and long-lived continuity require a
  higher-layer mechanism.

The main difference is packaging. `did:key` expands into a DID document with
verification methods and proof-purpose relationships. Nostr places the public
key directly in a signed event format whose kind supplies the protocol context.

```text
did:key:
  encoded key -> deterministic DID document -> verification method

Nostr:
  event pubkey + event data + event id + signature -> direct verification
```

`did:key` supports several encoded key types and provides compatibility with
DID and Verifiable Credential tooling. Nostr is more constrained, but that
constraint makes its event verification path particularly small.

`did:key` also reinforces an OpenETR design concern: a key-native identifier
does not solve long-term key succession. OpenETR should address profile
rotation and compromise recovery explicitly rather than hiding them behind an
identity syntax.

## Where Nostr Is Simpler

For OpenETR's control evidence, the central identity question is narrow:

> Which key signed this event concerning this exact Digital Artifact?

The event itself supplies the material needed to answer that question. A
verifier recomputes the event id and checks the signature against the embedded
author key.

Nostr also uses signed metadata events for discovery. Kind `0` provides
human-facing profile information, while dedicated kinds can carry
machine-facing information. NIP-65, for example, defines kind `10002` for an
author's preferred read and write relays. [NIP-65](https://github.com/nostr-protocol/nips/blob/master/65.md)

This allows identity-related information to remain composed of typed,
independently signed events rather than one large resolved identity document.

## What Nostr Does Not Replace

An `npub` identifies a signing key, not necessarily a stable person,
organization, or service across key rotation.

A DID can identify a subject independently of its current verification keys.
DID methods may support rotation, recovery, deactivation, multiple keys,
multiple controllers, and different proof purposes.

OpenETR should therefore avoid claiming that `npub` replaces every DID use
case. Its narrower claim is stronger:

> OpenETR does not require a general-purpose identity-document resolution
> layer before it can verify who signed an event.

Mapping the signing key to a warehouse, bank, company, person, service, or
agent remains a recognition decision made by the integrating system and its
rule book.

## The did:webvh Trade-Off

`did:webvh` is a sophisticated improvement over plain `did:web`. It adds a
self-certifying identifier, signed and hash-linked DID history, key rotation,
optional pre-rotation, witnesses, portability, and cryptographic agility.
[did:webvh v1.0](https://identity.foundation/didwebvh/v1.0/)

These features reduce dependence on the web host for the integrity of the DID
history. A substituted history must still satisfy the self-certifying
identifier and update-proof rules.

But the normal discovery path still transforms the DID into an HTTPS location:

```text
did:webvh
  -> DID-method-aware resolver
  -> DNS
  -> TLS and HTTPS
  -> hosted did.jsonl history
  -> cryptographic verification
```

The hosting can be static, and a relying party can run its own resolver. Even
so, DNS, HTTPS availability, hosted files, and compatible resolution software
remain part of initial discovery.

This is the critical distinction:

> `did:webvh` reduces trust in the web host's assertions, but it does not
> eliminate the web host from the normal availability path.

Once the complete DID history has been retained, it can be verified without
the original host. Watchers, mirrors, and archives can also improve
availability.

## Nostr Has Availability Dependencies Too

Nostr is not magically independent of infrastructure. A party that does not
already possess an event needs relays, archives, or another evidence source.
Relays can be unavailable or return incomplete results.

The difference is that the public key does not designate one relay as the
canonical authority for cryptographic validity. The same signed event can be
replicated across unrelated relays, exported as an evidence package, stored
locally, and verified wherever it is found.

OpenETR should therefore make a careful claim:

```text
not:
  infrastructure is unnecessary

but:
  no particular application, service, database, platform, domain, or relay
  must remain available once the required signed evidence is held
```

## Implications For OpenETR

OpenETR should:

- keep its Nostr binding key-native;
- verify event signatures without mandatory DID resolution;
- treat profiles and service metadata as signed claims, not automatic
  recognition;
- support DIDs and credentials as optional identity or authority evidence;
- permit a well-defined `did:key` adapter where DID ecosystem compatibility is
  useful, without requiring it for Nostr event verification;
- develop explicit key-succession rules if stable profile continuity across
  rotation is required;
- use dedicated signed event conventions for interoperable capabilities; and
- preserve events in multiple relays, archives, and portable evidence
  packages.

No immediate wire-format change is required.

## Policy Position

DID Core offers a broad, technology-neutral identity framework. `did:webvh`
adds valuable verifiable history and continuity to web-hosted DIDs. These are
appropriate tools where persistent subject identity, key rotation, multiple
verification methods, and DID ecosystem compatibility are required.

`did:key` confirms that the DID model can also be key-native and completely
offline. It is the fairest DID comparison with `npub`. For OpenETR, its primary
additional value would be compatibility with DID-oriented systems, not simpler
or stronger verification of native Nostr events.

OpenETR is solving a narrower problem. It needs independently verifiable
evidence of consequential actions concerning an exact Digital Artifact.
Nostr's direct public-key and signed-event model provides that capability with
fewer resolution layers.

The technologies can coexist:

```text
DID, credential, registry, or account system
  -> identifies or recognizes the actor

Nostr public key and OpenETR event
  -> provide attributable evidence concerning the artifact

OpenETR verifier policy
  -> derives consequential state and evaluates recognition inputs

relying system or law
  -> determines effect
```

The OpenETR choice is therefore not an argument against DIDs. It is an argument
for placing each abstraction only where its additional machinery is needed.

## Read More

- [Detailed technical analysis](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_DIDS_NOSTR_AND_DID_WEBVH_ANALYSIS_NOTE.md)
- [Actor-Neutral Identity](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Managing Digital Identity And OpenETR](./managing-digital-identity-and-openetr.md)
- [OpenETR And Open Trust Layer](./openetr-and-open-trust-layer.md)
