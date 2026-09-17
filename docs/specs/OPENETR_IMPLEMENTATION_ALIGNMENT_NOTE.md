# OpenETR Implementation Alignment Note

This note maps the generic OpenETR Protocol Layer model to the current OpenETR Nostr event implementation.

It is intended as a short bridge between:

- [OPENETR_GENERIC_TRANSFER_MODEL.md](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- the current OpenETR implementation in `/Users/trbouma/projects/etrix/openetr`

## Purpose

The generic model describes OpenETR at the level of Protocol Layer concepts.

The current implementation expresses those concepts through specific Nostr event kinds, tags, command flows, and query logic.

This note identifies:

- where the current implementation already aligns
- where the implementation is more specific than the generic model
- where the generic model is ahead of the current implementation

## Current Event Mapping

The current implementation uses the following working event family:

- `kind 1415`
  - Anchor Event
  - currently corresponds to `ISSUE`
- `kind 1416`
  - evidence-event family
  - currently used for:
    - `action=initiate`
    - `action=accept`
    - `action=terminate`
    - `action=attest`
    - `action=encumber`
    - `action=discharge`
    - `action=redeem`

At the implementation level, the mapping is therefore:

- `ISSUE` -> `1415`
- `TRANSFER` -> `1416` with `action=initiate` and optionally `action=accept`
- `TERMINATE` -> `1416` with `action=terminate`
- `ATTEST` -> `1416` with `action=attest`
- `ENCUMBER` -> `1416` with `action=encumber`
- `DISCHARGE` -> `1416` with `action=discharge`
- `REDEEM` -> `1416` with `action=redeem`

## Current Digital Artifact Model

The current implementation aligns well with the generic Digital Artifact concept.

The Digital Artifact is:

- identified by the SHA-256 digest of the canonical file or record
- carried through the event family using the object digest
- referenced in event tags

In current practice:

- the Anchor Event uses:
  - `o = <object_digest>`
- evidence events use:
  - `o = <object_digest>`
  - `e = <prior_event_id>`
  - `action = <action_name>`

The `d` tag may appear on legacy prototype events, but it is not required for
new regular graph events.

This means the object itself is already the anchor for control assertions and lifecycle events.

## Current Controller Semantics

The generic model states that exactly one Participant is the Current Controller at any point in time.

The current implementation is aligned with that statement as a recognition goal, but not yet as a protocol-level guarantee.

Today, the implementation:

- computes the current controller by traversing the observable control chain
- uses guards to require that the next transfer or termination event be authored by the current controller position
- supports warnings and ambiguity handling where multiple candidate chains exist

However, the current implementation still operates in an open relay environment where:

- multiple Anchor Events may exist for the same object
- multiple candidate control chains may exist
- recognition policy is still required to determine which chain is authoritative

Accordingly, the current implementation should be understood as:

- exposing candidate control histories
- applying guards for valid publication behavior
- leaving final authoritative recognition to policy, attestation, or assessment

## Transfer Model Alignment

The generic model defines a single abstract `TRANSFER` event.

The current implementation is more specific.

It models transfer using two related evidence events:

- `transfer initiate`
- `transfer accept`

This means the current implementation treats transfer as a small lifecycle rather than as a single atomic control transition.

That is consistent with the broader OpenETR design direction in which:

- unilateral initiation may occur
- acceptance may later confirm the transfer
- an attestor or assessor may determine whether initiation alone is sufficient for recognition

The generic model therefore remains accurate at a high level, but the implementation currently refines `TRANSFER` into:

- an initiation step
- an optional acceptance step

## Termination Model Alignment

The generic model defines `TERMINATE` as the event through which the Obligor completes performance and the Digital Artifact reaches the end of its lifecycle.

The current implementation is not yet fully aligned with that formulation.

Today, `terminate-etr` is effectively modeled as:

- a controller-driven termination event
- authored by the current controller of the active chain

So while termination already exists in the event family, its present semantics are closer to:

- controller-declared termination

rather than:

- obligor-confirmed completion of performance

This is a meaningful conceptual gap between the generic model and the live implementation.

## Implemented Action Set

The implementation supports the following Evidence Event actions:

- `ATTEST`
- `ENCUMBER`
- `DISCHARGE`
- `REDEEM`

Together with `initiate`, `accept`, and `terminate`, these actions use the shared
`1416` Evidence Event family. Their existence as signed events does not itself
establish a state change. Defined rules determine the Consequential State that
follows.

## Overall Conclusion

The current OpenETR implementation is directionally aligned with the generic Protocol Layer model.

It already demonstrates:

- a digest-identified Digital Artifact
- a signed evidence-event family
- a traversable control graph
- explicit current-controller logic
- transfer and termination semantics within a shared evidence-event family

However, the generic model is now ahead of the live implementation in several respects:

- it expresses transfer more abstractly than the current initiate/accept implementation
- it assumes a cleaner single-current-controller model than the open relay environment guarantees by itself
- it defines termination in obligor/performance terms that the current controller-driven implementation does not yet enforce
- termination remains controller-declared in the current implementation rather
  than necessarily proving obligor-confirmed performance

The practical interpretation is therefore:

- the current implementation is a working subset of the generic OpenETR model
- the generic model provides the broader architectural target
- further work is required to bring the Nostr event implementation into fuller semantic alignment
