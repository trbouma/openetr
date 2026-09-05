# Nostr Wire Format

The Nostr wire format is OpenETR's initial interoperability binding.

It defines how OpenETR DCR evidence is represented as signed Nostr events,
event kinds, and tags. Nostr supplies event representation, signatures,
references, relay transport, and discovery. OpenETR supplies DCR semantics,
validation rules, graph relationships, and Consequential State derivation.

> Nostr carries the events. OpenETR determines their consequences.

The OpenETR model permits future non-Nostr bindings that preserve equivalent
evidence and state-derivation semantics.

## Key-Based Identifiers

A **Key-Based Identifier (KBI)** identifies public-key verification material
used to verify attributable signed evidence. It does not, by itself, establish
the identity, actor type, authority, role, or recognition of the actor
associated with that key.

In the Nostr binding, the 32-byte public key is the KBI. Its 64-character
lowercase hexadecimal representation is the canonical wire encoding used in
events and relay filters. `npub` is the NIP-19 human-readable encoding of the
same KBI.

## Event Kinds

The current regular-event model uses:

| Kind | Use |
| --- | --- |
| `1415` | Anchor Event |
| `1416` | Control event family |

Legacy prototype events using `31415` and `31416` may exist, but new graph events use regular kinds `1415` and `1416`.

## Core Tags

| Tag | Role |
| --- | --- |
| `o` | Digital Artifact digest. Primary artifact-centric query anchor. |
| `e` | Prior event link for graph traversal. |
| `p` | Action-specific participant. |
| `action` | Control event subtype. |
| `enc` | Encumbrance event referenced by a discharge. |
| `type` | Action-specific subtype. |
| `ref` | External reference or business reference. |

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

## Content Field

The event `content` field is for readable narrative, comments, or unstructured context.

The signed tags are the machine interface.

## Source Specs

- [OpenETR Nostr Wire Format Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [Event Kind Registry](https://github.com/trbouma/openetr/blob/main/docs/specs/EVENT_KIND_REGISTRY.md)
- [Regular Event Kind Migration Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md)
