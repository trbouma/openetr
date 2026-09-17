# Evidence And State

The OpenETR protocol layer evaluates end-verifiable evidence concerning a
Digital Artifact. Signed records form a DCR; cryptographic and structural checks
validate that evidence; defined rules determine what Consequential State
follows. Control is one possible subject of that state, not the name for every
event or every consequence.

## Digital Artifact And Digital Controllable Record

A **Digital Artifact** is the persistent content identified by cryptographic
digest, normally SHA-256. A **Digital Controllable Record (DCR)** is one signed,
end-verifiable record or a graph of related records concerning that artifact.

The DCR carries evidence. Its presence does not, by itself, establish that the
events are valid, that consequential state or a current controller can be
derived, or that the artifact is recognized.

The object may be:

- a PDF;
- a JSON artifact;
- a signed document bundle;
- a verifiable credential;
- another canonical electronic record.

OpenETR does not need to parse the object to track its control history. It needs the digest.

When validation of the DCR under an applicable policy establishes
consequential state for the Digital Artifact, it becomes a **Digital Original**
in the technical OpenETR sense.

## Anchor Event

An Anchor event forms a one-record candidate DCR. Validation of that DCR under
an applicable policy may establish candidate consequential state.

It binds:

- object digest;
- issuer profile;
- event kind;
- event id;
- event signature;
- structured metadata tags.

## Evidence Events

Evidence Events express later signed actions concerning the same Digital
Artifact. Some actions change control, while attestations and other evidence may
support different state or no state change at all.

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

The Evidence Graph is reconstructed from signed events:

- `o` identifies the Digital Artifact by digest;
- `e` links to a prior event;
- `p` identifies an action-specific participant;
- `action` identifies the Evidence Event subtype;
- action-specific tags such as `enc`, `type`, and `ref` add structured context.

The Control Graph is the portion of that Evidence Graph concerned specifically
with control transitions. The graph is portable evidence. Cryptographic and
structural checks validate the DCR as a whole, and defined rules determine what
Consequential State follows.
Recognition separately decides whether to accept that result for a purpose and
what effect to give it.

```text
validated DCR evidence -> defined rules -> Consequential State
Consequential State -> recognition -> effect
```

Nostr carries the events. OpenETR determines their consequences.

Applications may cache and display a projection of the state, but they do not
own it. See [Consequential State](./consequential-state.md).

## Source Specs

- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [Evidence Event Minimum Shapes](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROL_EVENT_MINIMUM_SHAPES.md)
- [State Transition Note](https://github.com/trbouma/openetr/blob/main/docs/specs/STATE-TRANSITION.md)
- [Consequential State Architecture](https://github.com/trbouma/openetr/blob/main/docs/specs/CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [Digital Controllable Record](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
