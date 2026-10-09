# Nostr Wire Format

The Nostr wire format is OpenETR's initial interoperability binding.

It defines how OpenETR DCR evidence is represented as signed Nostr events,
event kinds, and tags. Nostr supplies event representation, signatures,
references, relay transport, and discovery. OpenETR supplies DCR semantics,
validation rules, graph relationships, and Consequential State derivation.

> Nostr carries the events. OpenETR determines their consequences.

The OpenETR model permits future non-Nostr bindings that preserve equivalent
evidence and state-derivation semantics.

In OpenETR, the **proof is outside the artifact**. The artifact is identified
by byte identity through the `o` tag, while Anchor Events and Evidence Events
carry the signed proof beside the artifact. A verifier or recognition policy
decides what effect, if any, to give that evidence.
This lets OpenETR remain format agnostic: the same event model can reference
PDFs, images, JSON records, credentials, bundles, media files, and future
artifact formats.

## Key-Based Identifiers

A **Key-Based Identifier (KBI)** identifies public-key verification material
used to verify attributable signed evidence. It does not, by itself, establish
the identity, actor type, authority, role, or recognition of the actor
associated with that key.

In the Nostr binding, the 32-byte public key is the KBI. Its 64-character
lowercase hexadecimal representation is the canonical wire encoding used in
events and relay filters. `npub` is the NIP-19 human-readable encoding of the
same KBI.

## Resource References

A **Resource Identifier** identifies a resource within a defined namespace or
scheme. A **Resource Locator** provides an address through which a resource can
be accessed or resolved. A **Resource Reference** may contain an identifier,
one or more locators, or both; a complete URL may already contain its identifier.

For OpenETR, an Artifact Digest identifies exact artifact bytes, while an Anchor
Event ID identifies a particular signed event concerning those bytes. Blossom
and HTTPS mirrors can supply the artifact; relays and archives can supply its
signed evidence. These are different resources with different identifiers.

The complete QR resolver URL is a Resource Locator. Its Resolution Reference
can directly carry a digest or be mapped to one by a campaign resolver. The
Resolver Profile defines how that interpretation works. Artifact identity can
remain stable while retrieval locations change, provided the bytes still
verify against the digest.

See the [QR Resolver Profile definitions](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_QR_RESOLVER_PROFILE_1_0.md#69-resource-identifier).

## Event Kinds

The current regular-event model uses:

| Kind | Use |
| --- | --- |
| `1415` | Anchor Event |
| `1416` | Evidence Event family |

OpenETR DCR events use regular kinds `1415` and `1416`. Replaceable events
are not part of the DCR wire format.

## Core Tags

| Tag | Role |
| --- | --- |
| `o` | Digital Artifact byte identity digest. Primary artifact-centric query anchor. |
| `e` | Prior event link for graph traversal. |
| `p` | Action-specific participant. |
| `action` | Evidence Event subtype. |
| `enc` | Encumbrance event referenced by a discharge. |
| `type` | Action-specific subtype. |
| `notice_type` | Anchor Publisher position carried by a Publisher Notice. |
| `ref` | External reference or business reference. |
| `blossom` | Optional, repeatable Anchor Event hint identifying a Blossom server origin for artifact retrieval; not assumed relay-indexed. |

## Structured Metadata

OpenETR uses named tags for signed structured metadata that does not need relay indexing.

Examples:

```text
["name", "MLWR001.pdf"]
["size_bytes", "282796"]
["digest_generated_at", "2026-07-10T12:00:00+00:00"]
["domain", "mlwr"]
["document_type", "warehouse_receipt"]
["record_reference", "MLWR001"]
["record_description", "Stored goods described in the receipt"]
```

Implementations should read structured data from tags after retrieving the event. They should not parse the `content` field to recover machine data.

## Blossom Retrieval Hints

An Anchor Event may advertise multiple locations for the same artifact:

```text
["blossom", "https://blossom.example.org"]
["blossom", "https://backup.example.org"]
```

Each tag contains a server origin, not a complete blob URL. The resolver
constructs `<server-origin>/<o-digest>` and verifies the returned bytes against
`o`. The digest identifies the artifact; these optional signed hints only help
locate it. They are read from event tags after relay discovery through `#o`.

When storage is requested, the publication workflow confirms availability
before signing the anchor and advertises the confirmed locations. Storage
requirements are local policy: `any` (default), `half`, `majority`, or `all`.
For N unique target origins, the thresholds are respectively 1, ceil(N/2),
floor(N/2)+1, and N. Failed targets remain in the denominator. An unmet
requirement must be surfaced, not silently treated as successful storage.
These thresholds are not event tags, consensus, or retention guarantees.

Resolvers can combine permitted hints with configured servers. Hints remain
untrusted network destinations even when signed; destination validation,
private-network protection, and bounded retrieval are required. Unusable
hints or unavailable bytes do not by themselves invalidate signed record
evidence. Existing anchors without hints continue to work through configured
storage or other available copies.

An anchor's signed hints cannot be edited without changing its event ID.
Do not silently reissue an anchor to refresh locations; local resolver
configuration can change independently of the DCR.

**Implementation status:** the OpenETR reference app uses Stroma's
`BlossomPool` for opt-in storage and hint-aware retrieval. New anchors advertise
only readback-confirmed origins; older anchors without hints use configured servers.
See the [full hint convention](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md#blossom-retrieval-hints).

## Content Field

The event `content` field is for readable narrative, comments, or unstructured context.

The signed tags are the machine interface.

## Source Specs

- [OpenETR Core Record Ruleset 1.0](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CORE_RECORD_RULESET_1_0.md)
- [OpenETR Nostr Wire Format Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [OpenETR QR Resolver Profile 1.0](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_QR_RESOLVER_PROFILE_1_0.md)
- [Event Kind Registry](https://github.com/trbouma/openetr/blob/main/docs/specs/EVENT_KIND_REGISTRY.md)
- [Regular Event Kind Migration Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md)
