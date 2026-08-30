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
| `1415` | Anchor Event | working | Initial signed event establishing an anchored control state for an object | Regular event used as the starting point for a candidate control graph |
| `1416` | control event family | working | Control-relevant events after an Anchor Event | Regular event family subtyped by the `action` tag |
| `31415` | legacy origin event | deprecated | Earlier addressable/replaceable origin prototype | Do not use for new OpenETR graph events |
| `31416` | legacy control event family | deprecated | Earlier addressable/replaceable control prototype | Do not use for new OpenETR graph events |

## Current Interpretation

### `1415` Anchor Event

The Anchor Event is the initial event by which an object enters an OpenETR control graph.

Current intended role:

- establish the initial anchored control state
- bind the object identifier into the scheme
- serve as the starting point for later control analysis

An Anchor Event is the wire-level starting point for a candidate control graph.
When valid under the applicable OpenETR rules, it establishes initial
consequential state and brings the identified Digital Object into the Digital
Original model. The registry does not decide which candidate graph is
authoritative, whether it is recognized, or what external effect follows.

A single object digest may have more than one Anchor Event. The registry does not require global uniqueness of `kind 1415` events per object digest; verifiers must evaluate candidate anchors under the relevant recognition profile.

### `1416` Control Event Family

The `1416` event family is currently used to express control-relevant actions after an Anchor Event.

Current intended role:

- represent transfer initiation after anchoring
- represent transfer acceptance
- represent termination
- represent attestations
- represent encumbrances
- represent discharges
- represent redemption or presentation events
- support later exclusive-controller determination
- separate later control movement from initial anchoring

Current working action subtypes:

- `action=initiate`
- `action=accept`
- `action=terminate`
- `action=attest`
- `action=encumber`
- `action=discharge`
- `action=redeem`

This means `1416` is presently being used as a shared control-event family rather than as a single-action kind.

That choice remains working and provisional.

## Related Specifications

- [CANONICAL_ETR_TRANSACTION_SPEC.md](./CANONICAL_ETR_TRANSACTION_SPEC.md)
- [REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md](./REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md)
- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [CONTROL_EVENT_MINIMUM_SHAPES.md](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md](./DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md)
- [TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md](./TITLE_TRANSFER_AUTHORITY_REPLACEABLE_EVENT_SPEC.md)

## Notes

- This registry does not yet define all future OpenETR event kinds.
- Separate event kinds for attestation, encumbrance, discharge, redemption, substitution, cancellation, and revocation remain open design areas, but the current working model represents several of these as `1416` actions.
- New graph events use regular event kinds `1415` and `1416`; the event id is the durable graph node.
- The `o` tag is the object-wide query anchor, the `e` tag links to a prior event, and the named `action` tag identifies the semantic action.
- Termination is currently modeled as `action=terminate` within `1416`, but may later be revisited as a separate kind if implementation experience suggests that is clearer.
- Event kind assignment alone does not determine legal or operational effect; effect depends on the wider OpenETR attestation, recognition, standing, and domain-policy model.
