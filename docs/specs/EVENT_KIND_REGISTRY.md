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
| `1415` | origin event | working | Initial OpenETR record bringing an object into the scheme | Regular event used for initial issuance/origin flows |
| `1416` | control event family | working | Control-relevant events after origin | Regular event family subtyped by the `action` tag |
| `31415` | legacy origin event | deprecated | Earlier addressable/replaceable origin prototype | Do not use for new OpenETR graph events |
| `31416` | legacy control event family | deprecated | Earlier addressable/replaceable control prototype | Do not use for new OpenETR graph events |

## Current Interpretation

### `1415` Origin Event

The origin event is the initial event by which an object enters the OpenETR scheme.

Current intended role:

- establish the initial OpenETR record
- bind the object identifier into the scheme
- serve as the starting point for later control analysis

### `1416` Control Event Family

The `1416` event family is currently used to express control-relevant actions after origin.

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

This means `1416` is presently being used as a shared control-event family rather than as a single-action kind.

That choice remains working and provisional.

## Related Specifications

- [CANONICAL_ETR_TRANSACTION_SPEC.md](./CANONICAL_ETR_TRANSACTION_SPEC.md)
- [REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md](./REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md)
- [TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md](./TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md)

## Notes

- This registry does not yet define all future OpenETR event kinds.
- Separate event kinds for attestation, encumbrance, discharge, redemption, substitution, cancellation, and revocation are still open design areas.
- New graph events use regular event kinds `1415` and `1416`; the event id is the durable graph node.
- The `o` tag is the object-wide query anchor, the `e` tag links to a prior event, and the named `action` tag identifies the semantic action.
- Termination is currently modeled as `action=terminate` within `1416`, but may later be revisited as a separate kind if implementation experience suggests that is clearer.
- Event kind assignment alone does not determine legal or operational effect; effect depends on the wider OpenETR attestation and recognition model.
