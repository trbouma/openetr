# Control Event Minimum Shapes

This note defines minimum event shapes for additional OpenETR control events within the current Nostr event family.

It is intended to extend the current OpenETR working model in which:

- `kind 31415` represents the origin or issue event
- `kind 31416` represents the control-event family

The goal is to define a minimal, internally consistent event shape for the current working `31416` action family:

- `INITIATE`
- `ACCEPT`
- `TERMINATE`
- `ATTEST`
- `ENCUMBER`
- `DISCHARGE`
- `REDEEM`

These definitions are intentionally minimal. They are not intended to settle the full legal, operational, or attestation semantics of the events. They define only the minimum Nostr event structure required to express them in the current OpenETR model.

## Shared Control-Event Pattern

Each of the events in this note is a `kind 31416` event.

They follow the same general pattern:

- `o` identifies the Controlled Object
- `e` links the event to the current control chain
- `action` identifies the event type
- `d` provides the replaceable addressing slot for that author, object, and action

Unless explicitly stated otherwise, these events do not change the Current Controller.

The reference implementation centralizes these actions and labels in `openetr/control.py`.

## Implementation Mapping

The current CLI maps these action shapes as follows:

| CLI command | Event kind | `action` | Participant tag |
| --- | --- | --- | --- |
| `openetr transfer initiate` | `31416` | `initiate` | `p` = transferee |
| `openetr transfer accept` | `31416` | `accept` | optional `p` = counterparty |
| `openetr terminate-etr` | `31416` | `terminate` | none |
| `openetr attest` | `31416` | `attest` | optional `p` = subject |
| `openetr encumber` | `31416` | `encumber` | `p` = beneficiary |
| `openetr discharge` | `31416` | `discharge` | optional `p` = releasing party |
| `openetr redeem` | `31416` | `redeem` | `p` = obligor |

`openetr query-etr` consumes the same event family to derive lifecycle state, current controller, control chains, and encumbrance state.

## INITIATE

### Purpose

`INITIATE` records a transfer initiation from the current controller toward a transferee.

The event identifies the intended transferee but does not, by itself, settle every recognition question outside the wire layer.

### Minimum Shape

- `kind = 31416`
- required tags:
  - `["d", "<object_hex>:initiate"]`
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "initiate"]`
  - `["p", "<transferee_pubkey_hex>"]`

### Control Effect

- candidate transfer of Current Controller to the transferee
- recognized effect depends on the implementation's control-chain and recognition rules

## ACCEPT

### Purpose

`ACCEPT` records acceptance of a transfer or control transition by the receiving party.

### Minimum Shape

- `kind = 31416`
- required tags:
  - `["d", "<object_hex>:accept"]`
  - `["o", "<object_hex>"]`
  - `["e", "<initiate_event_id_or_prior_control_event_id>"]`
  - `["action", "accept"]`

### Optional Tags

- `["p", "<transferor_or_related_counterparty_pubkey_hex>"]`

### Control Effect

- no independent controller change at the protocol layer
- may be required by policy or implementation logic before a transfer is treated as complete

## TERMINATE

### Purpose

`TERMINATE` records termination of the active OpenETR lifecycle for the Controlled Object.

### Minimum Shape

- `kind = 31416`
- required tags:
  - `["d", "<object_hex>:terminate"]`
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "terminate"]`

### Control Effect

- terminates the active lifecycle if recognized as effective
- later control events should not be treated as effective after recognized termination

## ATTEST

### Purpose

`ATTEST` records an authenticated assertion relating to the Controlled Object.

The attestation should reference the specific prior event being attested.

That means the `e` tag should point to the concrete origin or control event whose declaration, occurrence, or effect is being attested, rather than merely to the latest event in the chain in general.

Examples may include:

- custody
- inspection
- quality
- quantity
- certification

An attestation does not change the Current Controller.

### Minimum Shape

- `kind = 31416`
- required tags:
  - `["d", "<object_hex>:attest"]`
  - `["o", "<object_hex>"]`
  - `["e", "<specific_event_id_being_attested>"]`
  - `["action", "attest"]`

### Optional Tags

- `["type", "<attestation_type>"]`
- `["p", "<subject_pubkey_hex>"]`
- `["ref", "<external_reference>"]`

### Control Effect

- no change to Current Controller

## ENCUMBER

### Purpose

`ENCUMBER` records an authenticated declaration of an encumbrance affecting the Controlled Object.

Examples may include:

- pledge
- security right
- lien
- restriction

OpenETR records the declaration but does not determine legal validity, perfection, priority, or legal effect.

### Minimum Shape

- `kind = 31416`
- required tags:
  - `["d", "<object_hex>:encumber"]`
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "encumber"]`
  - `["p", "<beneficiary_or_secured_party_pubkey_hex>"]`

### Optional Tags

- `["type", "<encumbrance_type>"]`
- `["ref", "<external_reference>"]`

### Control Effect

- no change to Current Controller at the protocol layer

## DISCHARGE

### Purpose

`DISCHARGE` records the authenticated release or satisfaction of a previously declared encumbrance.

This event should identify the encumbrance event being discharged.

### Minimum Shape

- `kind = 31416`
- required tags:
  - `["d", "<object_hex>:discharge"]`
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "discharge"]`
  - `["enc", "<encumbrance_event_id_hex>"]`

### Optional Tags

- `["p", "<beneficiary_or_releasing_party_pubkey_hex>"]`
- `["ref", "<external_reference>"]`

### Control Effect

- no change to Current Controller

## REDEEM

### Purpose

`REDEEM` records that the Current Controller has presented the Controlled Object to the Obligor and requested performance.

`REDEEM` does not itself terminate the Controlled Object.

### Minimum Shape

- `kind = 31416`
- required tags:
  - `["d", "<object_hex>:redeem"]`
  - `["o", "<object_hex>"]`
  - `["e", "<prior_control_event_id_or_origin_event_id>"]`
  - `["action", "redeem"]`
  - `["p", "<obligor_pubkey_hex>"]`

### Optional Tags

- `["ref", "<presentation_or_claim_reference>"]`

### Control Effect

- conceptually moves the Controlled Object into a redemption-pending state
- does not itself terminate the object
- does not by itself change the Current Controller unless a later policy layer says otherwise

## Minimum `d` Tag Convention

The minimum convention in this note is:

- `initiate` -> `<object_hex>:initiate`
- `accept` -> `<object_hex>:accept`
- `terminate` -> `<object_hex>:terminate`
- `attest` -> `<object_hex>:attest`
- `encumber` -> `<object_hex>:encumber`
- `discharge` -> `<object_hex>:discharge`
- `redeem` -> `<object_hex>:redeem`

This provides one replaceable slot per:

- author
- object
- action

That is sufficient for a minimum working model.

However, this may later prove too coarse for event types that commonly occur multiple times for the same author and object.

Examples:

- multiple attestations by the same participant
- multiple encumbrances affecting the same object
- multiple discharge actions against distinct encumbrances

Accordingly, later refinements may choose to make `d` more specific while keeping the minimum shape otherwise intact.

## Summary

The minimum required tags for each event are:

- `INITIATE`
  - `d`, `o`, `e`, `action`, `p`
- `ACCEPT`
  - `d`, `o`, `e`, `action`
- `TERMINATE`
  - `d`, `o`, `e`, `action`
- `ATTEST`
  - `d`, `o`, `e`, `action`
- `ENCUMBER`
  - `d`, `o`, `e`, `action`, `p`
- `DISCHARGE`
  - `d`, `o`, `e`, `action`, `enc`
- `REDEEM`
  - `d`, `o`, `e`, `action`, `p`

These definitions provide a minimum event grammar for extending the existing OpenETR control-event family without changing the current `31415` / `31416` architectural split.
