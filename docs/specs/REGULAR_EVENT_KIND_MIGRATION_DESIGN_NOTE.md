# Regular Event Kind Decision Note

## Status

Implemented.

OpenETR Anchor Events and Evidence Events use regular Nostr event kinds:

| Kind | Purpose |
| --- | --- |
| `1415` | Anchor Event beginning a candidate DCR |
| `1416` | Evidence Event extending or relating to a candidate DCR |

The reference component, CLI, web application, and current specifications use
only these kinds for DCR graphs.

## Decision

OpenETR DCR graph nodes shall be regular events. They shall not use addressable
or replaceable event semantics.

The current graph grammar uses:

| Element | Purpose |
| --- | --- |
| `o` | Digital Artifact digest and object-centric query anchor |
| `e` | exact prior-event reference and graph edge |
| `p` | participant key where participant lookup is required |
| `action` | semantic subtype |

The `d` tag is not part of the current DCR graph grammar.

## Rationale

Every `e` link commits to an exact prior event id. A graph node must remain the
same signed record whenever another record references it. Replaceable semantics
are incompatible with that requirement because a newer event at the same
addressable coordinate would have a different event id and could cause a relay
to stop returning the referenced record.

Regular events preserve the intended model:

1. an Anchor Event begins a candidate DCR;
2. each later Evidence Event identifies the same Digital Artifact through `o`;
3. each graph edge identifies an exact prior record through `e`;
4. a verifier validates the supplied Evidence Graph;
5. defined rules derive Consequential State; and
6. recognition determines what external effect follows.

## Retrieval And Preservation

Regular event status does not guarantee indefinite availability from every
relay. Implementations should use relay diversity, local stores, archives,
exports, or other preservation arrangements appropriate to the domain.

A verifier shall report a missing record referenced by `e` as incomplete or
broken graph continuity. It shall not silently substitute another event.

## Configuration Events

This decision applies to DCR evidence. OpenETR may still use replaceable or
addressable events for information that is naturally mutable, including:

- profile metadata;
- relay lists;
- configuration records;
- summaries;
- indexes; and
- derived views.

Those records do not become DCR graph nodes merely because they are used by an
OpenETR implementation.

## Implementation Consequences

- publishers emit only kinds `1415` and `1416` for DCR evidence;
- object retrieval queries `#o`;
- graph traversal follows exact `e` references;
- event builders do not produce a `d` action slot;
- verifier policy does not include legacy-kind compatibility; and
- documentation and user interfaces describe only the regular-event model.

## Related Documents

- [OpenETR Nostr Wire Format Specification](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [Event Kind Registry](./EVENT_KIND_REGISTRY.md)
- [Evidence Event Minimum Shapes](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR Draft National Standard](./OPENETR_DRAFT_NATIONAL_STANDARD.md)
