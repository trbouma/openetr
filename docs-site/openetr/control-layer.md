# Control Layer

The OpenETR control layer interprets signed Nostr events under protocol rules
to derive consequential state for a controlled object.

## Controlled Object

A controlled object is identified by a cryptographic digest, normally SHA-256.

The object may be:

- a PDF;
- a JSON artifact;
- a signed document bundle;
- a verifiable credential;
- another canonical electronic record.

OpenETR does not need to parse the object to track its control history. It needs the digest.

## Anchor Event

An Anchor event brings the object into the OpenETR scheme and establishes
candidate consequential state.

It binds:

- object digest;
- issuer profile;
- event kind;
- event id;
- event signature;
- structured metadata tags.

## Control Events

Control events express later control-relevant actions concerning the same object.

Current actions include:

| Action | Meaning |
| --- | --- |
| `initiate` | Initiate a transfer. |
| `accept` | Accept a transfer. |
| `encumber` | Record a pledge, lien, restriction, or other encumbrance. |
| `discharge` | Release a prior encumbrance. |
| `redeem` | Present or redeem the object. |
| `terminate` | Complete or end the active lifecycle. |
| `attest` | Publish an attestation about an object, actor, or context. |

## Graph Reconstruction

The control graph is reconstructed from signed events:

- `o` identifies the controlled object;
- `e` links to a prior event;
- `p` identifies an action-specific participant;
- `action` identifies the control-event subtype;
- action-specific tags such as `enc`, `type`, and `ref` add structured context.

The graph is portable evidence. OpenETR rules derive protocol state from that
evidence. Recognition policy separately decides whether to accept that state
for a purpose and what effect to give it.

```text
signed events -> OpenETR rules -> consequential state -> recognition -> effect
```

Applications may cache and display a projection of the state, but they are not
its sole authority. See [Consequential State](./consequential-state.md).

## Source Specs

- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [Control Event Minimum Shapes](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROL_EVENT_MINIMUM_SHAPES.md)
- [State Transition Note](https://github.com/trbouma/openetr/blob/main/docs/specs/STATE-TRANSITION.md)
- [Consequential State Architecture](https://github.com/trbouma/openetr/blob/main/docs/specs/CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
