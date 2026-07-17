# Control Layer

The OpenETR control layer interprets signed Nostr events as a control history for a controlled object.

## Controlled Object

A controlled object is identified by a cryptographic digest, normally SHA-256.

The object may be:

- a PDF;
- a JSON artifact;
- a signed document bundle;
- a verifiable credential;
- another canonical electronic record.

OpenETR does not need to parse the object to track its control history. It needs the digest.

## Origin Event

An origin event brings the object into the OpenETR scheme.

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

The graph is evidence. Verifier policy decides what effect to give the evidence.

## Source Specs

- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [Control Event Minimum Shapes](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROL_EVENT_MINIMUM_SHAPES.md)
- [State Transition Note](https://github.com/trbouma/openetr/blob/main/docs/specs/STATE-TRANSITION.md)

