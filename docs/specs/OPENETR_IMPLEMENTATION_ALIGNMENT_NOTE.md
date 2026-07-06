# OpenETR Implementation Alignment Note

This note maps the generic OpenETR Control Layer model to the current OpenETR Nostr event implementation.

It is intended as a short bridge between:

- [OPENETR_GENERIC_TRANSFER_MODEL.md](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- the current OpenETR implementation in `/Users/trbouma/projects/etrix/openetr`

## Purpose

The generic model describes OpenETR at the level of Control Layer concepts.

The current implementation expresses those concepts through specific Nostr event kinds, tags, command flows, and query logic.

This note identifies:

- where the current implementation already aligns
- where the implementation is more specific than the generic model
- where the generic model is ahead of the current implementation

## Current Event Mapping

The current implementation uses the following working event family:

- `kind 31415`
  - origin event
  - currently corresponds to `ISSUE`
- `kind 31416`
  - control-event family
  - currently used for:
    - `action=initiate`
    - `action=accept`
    - `action=terminate`

At the implementation level, the mapping is therefore:

- `ISSUE` -> `31415`
- `TRANSFER` -> `31416` with `action=initiate` and optionally `action=accept`
- `TERMINATE` -> `31416` with `action=terminate`

## Current Controlled Object Model

The current implementation aligns well with the generic Controlled Object concept.

The Controlled Object is:

- identified by the SHA-256 digest of the canonical file or record
- carried through the event family using the object digest
- referenced in event tags

In current practice:

- the origin event uses:
  - `d = <object_digest>`
  - `o = <object_digest>`
- control events use:
  - `o = <object_digest>`
  - `d = <object_digest>:<action>`

This means the object itself is already the anchor for control assertions and lifecycle events.

## Current Controller Semantics

The generic model states that exactly one Participant is the Current Controller at any point in time.

The current implementation is aligned with that statement as a recognition goal, but not yet as a protocol-level guarantee.

Today, the implementation:

- computes the current controller by traversing the observable control chain
- uses guards to require that the next transfer or termination event be authored by the current controller position
- supports warnings and ambiguity handling where multiple candidate chains exist

However, the current implementation still operates in an open relay environment where:

- multiple origin events may exist for the same object
- multiple candidate control chains may exist
- recognition policy is still required to determine which chain is authoritative

Accordingly, the current implementation should be understood as:

- exposing candidate control histories
- applying guards for valid publication behavior
- leaving final authoritative recognition to policy, attestation, or assessment

## Transfer Model Alignment

The generic model defines a single abstract `TRANSFER` event.

The current implementation is more specific.

It models transfer using two related control events:

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

The generic model defines `TERMINATE` as the event through which the Obligor completes performance and the Controlled Object reaches the end of its lifecycle.

The current implementation is not yet fully aligned with that formulation.

Today, `terminate-etr` is effectively modeled as:

- a controller-driven termination event
- authored by the current controller of the active chain

So while termination already exists in the event family, its present semantics are closer to:

- controller-declared termination

rather than:

- obligor-confirmed completion of performance

This is a meaningful conceptual gap between the generic model and the live implementation.

## Event Types Not Yet Implemented

The generic model includes the following control events:

- `ATTEST`
- `ENCUMBER`
- `DISCHARGE`
- `REDEEM`

These are not yet implemented in the current OpenETR Nostr event family.

At present, the live implementation covers:

- `ISSUE`
- `TRANSFER`
- `TERMINATE`

with transfer refined into:

- initiate
- accept

## Overall Conclusion

The current OpenETR implementation is directionally aligned with the generic Control Layer model.

It already demonstrates:

- a digest-identified Controlled Object
- a signed control-event family
- a traversable control graph
- explicit current-controller logic
- transfer and termination semantics within a shared control-event family

However, the generic model is now ahead of the live implementation in several respects:

- it expresses transfer more abstractly than the current initiate/accept implementation
- it assumes a cleaner single-current-controller model than the open relay environment guarantees by itself
- it defines termination in obligor/performance terms that the current controller-driven implementation does not yet enforce
- it includes `ATTEST`, `ENCUMBER`, `DISCHARGE`, and `REDEEM`, which are not yet implemented

The practical interpretation is therefore:

- the current implementation is a working subset of the generic OpenETR model
- the generic model provides the broader architectural target
- further work is required to bring the Nostr event implementation into fuller semantic alignment
