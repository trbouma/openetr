# OpenETR, W3C DIDs, Nostr, And did:webvh Analysis Note

## Status

Research and architecture note, 4 September 2026.

This note compares the identity properties commonly attributed to W3C
Decentralized Identifiers with the narrower public-key and signed-event model
used by Nostr and OpenETR. It gives particular attention to `did:webvh` and its
dependencies on DNS, HTTPS, DID resolution, and hosted DID logs.

The purpose is not to establish that one technology is universally superior.
It is to determine which abstractions OpenETR actually needs to produce
independently verifiable records.

## Sources

Primary sources used in this analysis include:

- [W3C Decentralized Identifiers v1.0](https://www.w3.org/TR/did/)
- [did:key Method v0.9](https://w3c-ccg.github.io/did-key-spec/)
- [did:webvh DID Method v1.0](https://identity.foundation/didwebvh/v1.0/)
- [NIP-01: Basic protocol flow description](https://github.com/nostr-protocol/nips/blob/master/01.md)
- [NIP-19: bech32-encoded entities](https://github.com/nostr-protocol/nips/blob/master/19.md)
- [NIP-65: Relay List Metadata](https://github.com/nostr-protocol/nips/blob/master/65.md)

## Executive Assessment

The three DID claims considered here have direct Nostr counterparts:

1. a globally unique identifier;
2. cryptographic verification material; and
3. service or interaction endpoints.

Nostr addresses these functions with fewer layers when the subject of the
identifier is the signing key itself:

```text
public key
  -> signed event
  -> relay-backed metadata and protocol events
```

DID Core addresses a broader problem:

```text
DID
  -> DID method
  -> method-specific resolution
  -> DID document
  -> verification methods, relationships, and services
```

The principal OpenETR conclusion is:

> A DID resolves to cryptographic identity material. A Nostr public-key
> identifier is cryptographic identity material.

That narrower construction is valuable for OpenETR because the protocol needs
to verify attributable signed evidence. It does not need every signing key to
become a technology-neutral, key-rotatable identifier for an arbitrary subject.

The closest DID comparison is `did:key`, not `did:webvh`. Like an `npub`, a
`did:key` identifier directly encodes public-key material and can be resolved
locally without DNS, a registry, a network request, or a hosted DID document.
It confirms that a key-native identifier can satisfy many DID goals with very
little infrastructure.

The trade-off is real. DIDs can separate the persistent subject identifier
from its current keys and can express multiple verification methods,
controllers, services, rotation, recovery, and deactivation. A Nostr `npub`
identifies one public key. If the key changes, the identifier changes unless a
separate signed succession or recognition mechanism establishes continuity.

## Why OpenETR Selected Nostr As Its Initial Protocol

OpenETR considered W3C DIDs as a possible identity foundation. The decision to
use Nostr as the initial protocol was not a rejection of DIDs. It followed from
a different starting point and a deliberate scope boundary.

DID architecture begins with an identifier for a subject and defines how that
identifier resolves to verification methods, relationships, services, and
other subject-associated information. This is valuable where a system needs a
general identity layer, persistent subject identity, key rotation, multiple
proof purposes, service discovery, or compatibility with Verifiable
Credentials and DID-based ecosystems.

OpenETR begins with the record:

```text
exact Digital Artifact
  -> attributable signed events concerning it
  -> Digital Controllable Record
  -> state-transition rules
  -> Consequential State
```

For that records-first model, the minimum identity requirement is narrower. A
verifier needs to determine which key signed a particular event. Whether that
key represents a recognized person, organization, warehouse, bank, authority,
service, or agent is important, but it is a separate recognition question.

Leaving recognition outside the base protocol was an explicit design choice.
It allows the same OpenETR evidence to be used across domains, organizations,
trust frameworks, and legal jurisdictions without requiring them to adopt one
identity method, credential format, registry, or definition of authority.

Nostr fits this boundary particularly well because it combines:

- key-native signer identification;
- a compact, deterministic signed-event format;
- event ids that commit to the complete signed event data;
- typed events and structured tags;
- object and prior-event references;
- publication to multiple independent relays;
- replication into archives and local event stores; and
- verification without contacting the original application or signer.

The relay architecture is important to OpenETR's durability objective. A DID
method can define durable identifiers and verifiable identity history, but DID
Core deliberately leaves persistence, resolution, replication, and
availability to each method and its underlying verifiable data registry.
Nostr gives the initial OpenETR implementation a shared event-distribution
model in addition to a signature model.

No relay guarantees permanence or complete retrieval. The advantage is that
no one relay is the exclusive authority for a valid event. An exact signed
event can be served by several relays, stored in an archive, exported in an
evidence package, or verified locally. Once the required evidence is held, the
original OpenETR application, service, database, platform, and publishing
relay need not be running at the time of verification.

This produced the following design decision:

> OpenETR uses Nostr as its initial protocol because a key-native,
> independently verifiable, relay-replicable event model is the smallest
> architecture that supports its records-first control layer. DIDs remain
> valuable optional inputs for identity, authority, service discovery, and
> recognition where an integration requires them.

The choice also preserves technology neutrality at the OpenETR model level.
Nostr is the initial normative wire binding, not a claim that consequential
state can only be represented through Nostr. Another binding can interoperate
if it preserves equivalent artifact identity, attributable signed evidence,
event identity, graph linkage, transition semantics, and independent
verification.

## Claim 1: Global Uniqueness

### DID Model

DID Core defines a DID as a URI containing:

- the `did` URI scheme;
- a DID method name; and
- a method-specific identifier.

The method determines how identifiers are created, resolved, updated, and
deactivated. The method is therefore not decorative syntax. It identifies the
rules and infrastructure needed to interpret the method-specific identifier.

A DID may identify a person, organization, software agent, thing, data model,
or abstract subject. The DID subject need not be the key or the controller.

### Nostr Model

NIP-01 represents an event author with a 32-byte public key. NIP-19 defines
`npub` as the human-facing bech32 encoding of that public key. The core event
and relay filters use the underlying hexadecimal or binary key, not the
display encoding.

The key is probabilistically unique within the cryptographic keyspace. No
registration authority, DID method namespace, or method-specific creation
procedure is required to allocate it.

For OpenETR, this is usually enough. The protocol question is:

> Which public key signed this event?

It is not automatically:

> Which persistent real-world subject does this identifier denote across all
> future key changes?

### Qualification

An `npub` should not be described as a complete replacement for every DID use
case. It identifies a key directly, while a DID can identify a subject and
resolve to changing verification material.

OpenETR should state the difference positively:

- `npub` is a compact identifier for a Nostr signing key;
- a Commitment Profile associates operational meaning with a signing key;
- a host system or recognition policy maps that key to a person,
  organization, role, facility, service, or agent; and
- key succession or rotation requires explicit evidence and policy rather
  than being assumed from the identifier.

## Claim 2: Public-Key Infrastructure

### DID Documents

A DID document can contain verification methods and verification
relationships. It can say which cryptographic material is associated with
authentication, assertion, key agreement, capability invocation, or
delegation.

Calling this a public-key infrastructure is understandable but broad. The DID
document describes cryptographic material and authorized relationships. A
verifier must still:

1. recognize the DID method;
2. perform method-specific resolution;
3. validate the resolved DID document and method result;
4. select the relevant verification method and relationship; and
5. verify the proof using that material.

The assurance obtained depends on the DID method and its trust, availability,
freshness, and resolution properties.

### Nostr Events

A Nostr event contains the author public key, timestamp, kind, tags, content,
event id, and signature. NIP-01 defines the event id as the SHA-256 digest of
the serialized event data and the signature as a signature over that event id.

Verification is direct:

```text
receive event
  -> recompute event id
  -> compare event id
  -> verify signature against event pubkey
```

No DID document or method-specific resolver is needed to prove that the holder
of the corresponding private key authorized the event.

This does not prove ownership of an identity in the legal or social sense. It
proves control of the private key for the purpose of creating that signature.
Recognition remains separate.

### OpenETR Consequence

Nostr is attractive to OpenETR because the signed event is already an
independently verifiable evidence object. The verifier does not need to
retrieve a separate identity document before checking event authenticity.

OpenETR should continue to distinguish:

```text
signature validity:
  this key signed this event

profile meaning:
  this key claims or is presented as representing this role

actor recognition:
  this verifier accepts the mapping for this purpose

authority:
  this actor was permitted to perform this action
```

## did:key: The Closest DID Comparison

### Deterministic And Registry-Free

The `did:key` method is a non-registry DID method. Its method-specific
identifier contains a Multibase encoding of a Multicodec key-type identifier
and the raw public-key bytes. A resolver expands those bytes deterministically
into a DID document.

The resolution path is local:

```text
did:key identifier
  -> decode Multibase
  -> decode Multicodec key type
  -> validate public-key bytes
  -> generate deterministic DID document
```

No authoritative registry, DNS lookup, HTTPS request, hosted file, or third-
party resolver service is required. A relying party still needs compatible
`did:key`, Multibase, Multicodec, DID document, and cryptographic software, but
it can run that software locally.

The current `did:key` document is a W3C Credentials Community Group work item,
not the W3C DID Core Recommendation itself. Its current specification describes
version 0.9.

### Similarity To `npub`

Both identifiers are deterministic encodings of public-key material:

```text
did:key:
  DID prefix + method + Multibase(Multicodec(key type, public key bytes))

npub:
  bech32 display encoding of a Nostr public key
```

Neither requires network retrieval to recover the public key. Neither has
intrinsic key rotation, recovery, update, or deactivation. In both cases, a
new key produces a new identifier and continuity must be established at a
higher layer.

`did:key` is more cryptographically descriptive because the identifier carries
a Multicodec key type and can represent several supported key families. An
`npub` is more constrained: in the Nostr context, the encoding means a Nostr
public key used under the NIP-01 signature rules.

### Remaining Difference

`did:key` deterministically generates a DID document containing verification
methods and verification relationships such as authentication, assertion,
capability invocation, capability delegation, and, for some key types, key
agreement.

Nostr does not generate that intermediate document. The event kind and the
Nostr protocol define how the public key is being used for the event. The
event carries the author key, signed payload, event id, and signature together.

For OpenETR event verification, the Nostr path remains shorter:

```text
did:key evidence path:
  decode identifier -> generate DID document -> select verification method
  -> interpret proof suite -> verify external signed object

Nostr evidence path:
  recompute event id -> verify event signature against event pubkey
```

This is a difference in packaging and protocol scope, not a fundamental
difference in cryptographic decentralization.

### Limitations Shared With Nostr Keys

The `did:key` specification explicitly does not support update or deactivation
and cautions against long-lived use without strong key protection. A
compromised key cannot be replaced while retaining the same identifier.

That is substantially the same continuity issue faced by a bare Nostr public
key. OpenETR's root-and-profile organization can manage operational keys, but
long-lived succession, compromise recovery, revocation, and historical
recognition still require explicit signed evidence and verifier policy.

### Service Discovery

Because a `did:key` document is generated entirely from the identifier, it
cannot provide independently updated service endpoints without introducing a
higher-layer convention or another external record. This makes it less suited
than an updateable DID method for mutable service discovery.

Nostr addresses mutable discovery separately through signed replaceable
events such as kind `0` metadata and kind `10002` relay lists. This separation
lets the public-key identifier remain stable while metadata changes, although
retrieving current metadata still depends on relays or retained events.

## Claim 3: Service Endpoints

### DID Services

DID Core permits a DID document to contain service entries with an identifier,
type, and service endpoint. This gives DID-aware systems a common document
location for discovering ways to interact with the DID subject.

The endpoint is still a claim in a resolved DID document. The relying party
must decide whether the service type is understood, whether the endpoint is
appropriate, and what security or recognition policy applies.

### Nostr Metadata

NIP-01 defines kind `0` as replaceable user metadata signed by the profile key.
Its content includes conventional human-facing fields and may contain
additional metadata fields.

Kind `0` can therefore advertise contact or interaction information by
convention. However, OpenETR should not turn kind `0` into an unbounded DID
document substitute. Machine-interoperable capabilities are clearer when
expressed through dedicated event kinds and NIPs.

NIP-65 provides an example. Kind `10002` publishes the author's preferred read
and write relays as a signed replaceable event.

A Nostr-native discovery model can therefore be composed:

```text
public key
  -> kind 0: human-facing profile metadata
  -> kind 10002: relay discovery
  -> dedicated kinds: protocol capabilities or service conventions
  -> OpenETR kinds: DCR evidence
```

This model keeps each claim typed and independently signed instead of placing
all identity, key, and service information in one resolved document.

### Qualification

Nostr still has a discovery problem. A client must know which relay or relay
pool to query, obtain relevant metadata, and assess freshness and retrieval
coverage. The simplification is not that retrieval disappears. It is that
cryptographic verification of an event does not depend on trusting the relay
or resolving a separate identity method.

## did:webvh: What It Adds

`did:webvh` improves substantially on plain `did:web`. Version 1.0 provides:

- a self-certifying identifier derived from the initial DID log entry;
- a cryptographically linked history of DID document versions;
- signed update proofs;
- key rotation and optional pre-rotation;
- optional witnesses;
- optional portability to another web location;
- cryptographic agility; and
- optional watcher locations and historical verification.

These are meaningful capabilities. In particular, the self-certifying
identifier and signed update history reduce the ability of a compromised web
host or DNS route to substitute a different valid identity history.

`did:webvh` solves a richer continuity problem than a bare Nostr public key.
That strength should be recognized rather than dismissed.

## did:webvh: What It Still Depends On

The normal `did:webvh` resolution process transforms the DID's domain and path
into an HTTPS location and retrieves a `did.jsonl` DID log. The specification
identifies the DNS-resolved host as the target system.

The ordinary retrieval path is therefore:

```text
did:webvh identifier
  -> method-aware resolver
  -> DNS resolution
  -> TLS and HTTPS availability
  -> hosted did.jsonl
  -> SCID, history, update-key, proof, and witness verification
  -> current DID document
```

The host need not run a specialized identity application continuously. Static
HTTPS hosting can publish the files, and a relying party can run its own
resolver. Nevertheless, DNS, TLS, hosting, and compatible resolver software
remain part of normal initial discovery.

The cryptographic history changes the nature of that dependency:

- DNS and HTTPS are not sufficient authority for the integrity of the DID
  history;
- a substituted history must still satisfy the embedded SCID and update-proof
  rules;
- the host can still deny availability;
- a host may be able to present an older valid history unless the verifier has
  stronger freshness evidence; and
- long-term operation benefits from retained logs, watchers, mirrors, or
  archives.

Once a verifier possesses the required DID log and verification material, it
can verify the history independently. This resembles OpenETR's ability to
verify a retained signed evidence package without contacting its original
publisher.

## Nostr: What It Still Depends On

Nostr also has operational dependencies.

A verifier that does not already possess an event needs:

- one or more relay locations;
- reachable relay or archive infrastructure;
- query and pagination support;
- any required relay authentication; and
- sufficient retrieval coverage for the selected policy.

Relays can omit, delete, withhold, or fail to return events. Multiple relays,
archives, local evidence packages, and explicit retrieval-status reporting are
therefore important.

The architectural difference is that no one relay is identified by the public
key as the canonical authority for the event's cryptographic validity. The
same signed event can be replicated across unrelated relays or stored locally.
Any exact copy verifies to the same event id and signature.

## Comparative Model

| Property | DID Core | `did:key` | `did:webvh` | Nostr / OpenETR |
| --- | --- | --- | --- | --- |
| identifier subject | arbitrary subject | key-derived DID subject | arbitrary DID subject | signing public key |
| global namespace | method plus method-specific id | method plus encoded key type and bytes | `webvh`, SCID, domain, path | 32-byte public-key space |
| human-facing form | DID URI | DID URI | DID URI | `npub` display encoding |
| signature verification | method-defined resolution | deterministic local DID document | verify DID log, then select method | verify event against embedded author key |
| key rotation | method-defined | not supported | verifiable history and pre-rotation | new key creates new identifier; continuity requires evidence |
| multiple keys and purposes | DID document relationships | deterministic relationships | DID document relationships | separate keys, profiles, and event conventions |
| service discovery | DID document services | no mutable service document | DID services and linked paths | kind `0`, kind `10002`, and dedicated events |
| normal discovery dependency | method-specific | held identifier and local software | DNS, HTTPS, hosted DID log | relay or evidence-source discovery |
| content integrity | method-dependent | identifier-derived key material | SCID, linked history, update proofs | event id and signature |
| replication | method-dependent | identifier itself is sufficient | watchers, mirrors, retained logs | multiple relays, archives, local event stores |
| offline verification | depends on held method data | yes | possible with retained history | possible with exact retained events |
| legal identity or authority | external recognition | external recognition | external recognition | external recognition |

## Availability Is Not Integrity

The comparison is clearest when availability and integrity are separated.

`did:webvh` uses DNS and HTTPS to locate its normal authoritative publication
path, but cryptographically verifies the retrieved history. Nostr uses relays
to locate and replicate signed events, but cryptographically verifies each
event independently of the relay.

Neither system makes unavailable evidence available through cryptography.
Neither a valid DID history nor a valid Nostr event proves that the associated
actor is legally recognized or authorized for a particular action.

OpenETR should report these questions independently:

- was the evidence retrieved?
- from which sources?
- is its cryptographic integrity valid?
- is the evidence current and sufficient under the policy?
- is the signer recognized for the claimed role?
- was the signer authorized for this action?

## Implications For The OpenETR Identity Model

### Keep Nostr Key-Native

The normative Nostr binding should continue to use the event author's public
key as the cryptographic signer identifier. It should not require DID
resolution before validating an OpenETR event.

### Keep Recognition External

A kind `0` profile, DID document, credential, NIP-05 identifier, Contact, or
Reference can provide identity and discovery evidence. None should be treated
as automatic authority to issue or control a Digital Artifact.

### Preserve DID Interoperability

OpenETR should be able to reference a DID or DID-derived credential as
associated identity, role, authority, or recognition evidence. This permits
integration with DID-based systems without making one DID method part of the
control grammar.

Where a relying ecosystem requires a DID representation for an OpenETR signer,
`did:key` may be a straightforward adapter because it is derived from key
material without network resolution. The exact conversion is not merely a
textual prefix change: it must specify the compatible key encoding, key type,
and proof conventions, including the difference between Nostr's public-key
representation and the compressed secp256k1 representation listed by the
current `did:key` specification.

### Specify Key Succession Deliberately

The Control Desk Key and Commitment Profile model organizes keys for an
application context, but it should not be described as automatically providing
the stable subject identity, rotation history, recovery, or deactivation model
of `did:webvh`.

If long-lived profile continuity across key changes becomes a requirement,
OpenETR should define explicit signed succession evidence and verifier policy.
That design can borrow lessons from DID methods without importing DID Core as
a prerequisite for event verification.

### Use Typed Discovery Events

Kind `0` should remain primarily human-facing profile metadata. Standard
machine-facing endpoints and capabilities should use dedicated signed event
conventions where interoperability matters.

### Preserve Evidence Locally

OpenETR's strongest availability claim is not that relays never fail. It is
that signed evidence can be replicated, exported, archived, and verified
without the original application or publisher being available at the time of
performance.

## Recommended Position

OpenETR should describe its identity choice as a deliberate narrowing:

> DIDs provide a technology-neutral framework for resolving identifiers into
> documents containing keys and services. Nostr begins with the signing key
> itself and uses independently signed, relay-backed events to associate
> discoverable information with it.

For OpenETR, the Nostr model provides a simpler cryptographic path from signer
to event evidence. DID systems remain useful recognition and integration
inputs where persistent subject identifiers, key rotation, multiple
verification methods, or DID ecosystem compatibility are required.

`did:key` occupies the closest middle ground. It demonstrates that DID syntax
can wrap a public key without a registry or network resolver. For native
OpenETR event verification, that wrapper adds ecosystem compatibility but does
not add cryptographic assurance beyond possession of the correct key and
verification of the signed event.

No immediate OpenETR wire-format change is required. Future work should focus
on:

1. explicit key-succession and profile-continuity requirements;
2. typed service and capability discovery conventions;
3. DID and credential references as associated recognition evidence;
4. relay discovery, retrieval coverage, and portable evidence packages; and
5. verifier output that separates cryptographic validity, availability,
   freshness, identity recognition, authority, and effect.

## Related OpenETR Documents

- [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md](./OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [OPENETR_AND_MANAGING_DIGITAL_IDENTITY_REVIEW_NOTE.md](./OPENETR_AND_MANAGING_DIGITAL_IDENTITY_REVIEW_NOTE.md)
- [OPENETR_AND_OPEN_TRUST_LAYER_REVIEW_NOTE.md](./OPENETR_AND_OPEN_TRUST_LAYER_REVIEW_NOTE.md)
- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md](./RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md)
- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)
