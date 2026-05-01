# Event Kind Registry

This document is the working registry for OpenETR event kinds.

Its purpose is to provide one canonical place to track:

- event kind numbers
- event kind names
- current status
- intended purpose
- related specifications
- implementation notes

This registry is a draft and may change as the OpenETR model evolves.

## Status Values

Suggested status values:

- `working` for active experimental assignments
- `draft` for proposed but not yet adopted assignments
- `reserved` for intentionally held future assignments
- `deprecated` for assignments that should no longer be used

## Registry

| Kind | Name | Status | Purpose | Notes |
|------|------|--------|---------|-------|
| `31415` | origin event | working | Initial OpenETR record bringing an object into the scheme | Currently used for initial issuance/origin flows |
| `31416` | control event family | working | Control-relevant events after origin | Currently subtyped by `action=initiate`, `action=accept`, and `action=terminate` |

## Current Interpretation

### `31415` Origin Event

The origin event is the initial event by which an object enters the OpenETR scheme.

Current intended role:

- establish the initial OpenETR record
- bind the object identifier into the scheme
- serve as the starting point for later control analysis

### `31416` Control Event Family

The `31416` event family is currently used to express control-relevant actions after origin.

Current intended role:

- represent transfer initiation after origin
- represent transfer acceptance
- represent termination
- support later exclusive-controller determination
- separate control movement from initial origin

Current working action subtypes:

- `action=initiate`
- `action=accept`
- `action=terminate`

This means `31416` is presently being used as a shared control-event family rather than as a single-action kind.

That choice remains working and provisional.

## Related Specifications

- [CANONICAL_ETR_TRANSACTION_SPEC.md](./CANONICAL_ETR_TRANSACTION_SPEC.md)
- [TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md](./TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md)

## Notes

- This registry does not yet define all future OpenETR event kinds.
- Endorsement, substitution, cancellation, revocation, and attestation kinds are still open design areas.
- Termination is currently modeled as `action=terminate` within `31416`, but may later be revisited as a separate kind if implementation experience suggests that is clearer.
- Event kind assignment alone does not determine legal or operational effect; effect depends on the wider OpenETR attestation and recognition model.
