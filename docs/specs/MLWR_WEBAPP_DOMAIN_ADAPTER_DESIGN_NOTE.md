# MLWR Webapp Domain Adapter Design Note

This note documents the current warehouse receipts webapp work and how it relates to the generalized OpenETR component.

It is intended to explain the implementation boundary created by the new MLWR Control Desk:

- the webapp speaks warehouse receipt language
- the OpenETR component remains generic
- domain actions are translated into general OpenETR issue, query, and control-event service calls

## Status

Draft, reflecting the current FastAPI webapp and `openetr.services` implementation.

## Purpose

The warehouse receipts page is a domain adapter for MLWR-style workflows.

It should feel like a warehouse receipt control desk to the user, while avoiding warehouse-specific protocol logic inside the OpenETR core.

This lets OpenETR support MLWR-style usage without hard-coding MLWR as the only use case.

The same pattern can later support other domain adapters, such as:

- electronic bills of lading
- promissory notes
- certificates
- bearer-style presentation records
- secured finance records

## Architectural Boundary

The design follows a three-part split.

### Domain Web Surface

The FastAPI webapp presents domain concepts:

- warehouse receipt
- warehouse operator
- holder / current controller
- secured party
- pledge or lien
- release
- presentation for delivery
- completed delivery

These terms are used in routes, page headings, form labels, and result sections.

### OpenETR Service Layer

The webapp calls generic OpenETR service functions.

Current services include:

- `publish_issue_etr`
- `build_query_etr_result`
- `publish_transfer_initiate_event`
- `publish_transfer_accept_event`
- `publish_auxiliary_control_event`

The control-event publishing functions live in:

```text
openetr/services/control_events.py
```

The service layer works in terms of:

- object digests
- Nostr pubkeys
- origin events
- control events
- action tags
- participant tags
- relay publication and verification

It should not depend on warehouse receipt terminology.

### OpenETR Wire Model

The services publish and query the generalized OpenETR Nostr wire format:

- `kind 31415` for origin events
- `kind 31416` for control-relevant events
- named structured tags such as `name`, `digest_generated_at`, and `size_bytes` for origin-event metadata
- MLWR domain tags such as `domain=mlwr`, `document_type=warehouse_receipt`, `receipt_reference`, and `goods_description`
- `action` tags for control-event subtype
- `o` for object identity
- `d` for replaceable action slot
- `e` for prior event linkage
- `p` for action-specific participant
- `enc` for discharge of a specific encumbrance
- `type` and `ref` for additional action metadata

The MLWR adapter treats signed event tags as the structured data interface.

The event `content` field is used for a short human-readable narrative, such as `Issued warehouse receipt MLWR001`, and should not be parsed to recover receipt reference, goods description, file name, or byte size.

This mirrors the general OpenETR convention: relay-query anchors and graph links live in core tags; domain and document data live in named signed tags; `content` remains readable context.

## Current Web Routes

The warehouse receipts surface is rooted at:

```text
GET /warehouse-receipts
```

The current route set is:

| Route | Domain action | OpenETR service mapping |
| --- | --- | --- |
| `GET /warehouse-receipts` | show MLWR Control Desk | renders domain page |
| `POST /warehouse-receipts/query` | query receipt state | `build_query_etr_result` |
| `POST /warehouse-receipts/issue` | issue receipt | `publish_issue_etr` then `build_query_etr_result` |
| `POST /warehouse-receipts/transfer/initiate` | initiate receipt transfer | `publish_transfer_initiate_event` |
| `POST /warehouse-receipts/transfer/accept` | accept receipt transfer | `publish_transfer_accept_event` |
| `POST /warehouse-receipts/encumber` | record pledge, lien, or restriction | `publish_auxiliary_control_event(action=encumber)` |
| `POST /warehouse-receipts/discharge` | release pledge, lien, or restriction | `publish_auxiliary_control_event(action=discharge)` |
| `POST /warehouse-receipts/redeem` | present for delivery | `publish_auxiliary_control_event(action=redeem)` |
| `POST /warehouse-receipts/terminate` | complete delivery / lifecycle | `publish_auxiliary_control_event(action=terminate)` |

## Templates

The current warehouse receipt templates are:

```text
app/templates/warehouse_receipts.html
app/templates/warehouse_receipt_result.html
```

`warehouse_receipts.html` provides the domain dashboard.

It includes:

- page framing as the `MLWR Control Desk`
- read-only query flow
- receipt issuance flow
- profile selection
- domain role summary
- recognition boundary explanation

`warehouse_receipt_result.html` renders the generic OpenETR query result as warehouse receipt state.

It includes:

- receipt digest and object id
- receipt origin / issuance
- current holder / controller
- pledges, liens, and restrictions
- outstanding encumbrance summary
- receipt control history
- action forms for transfer, acceptance, pledge, release, presentation, and completion
- underlying OpenETR query filters for auditability

## Profile Selection

The MLWR page includes profile selection because warehouse receipt workflows are role-driven.

A user may need to act as:

- warehouse operator
- exporter
- depositor
- bank
- secured party
- holder
- registry or attestor

The page reuses the existing relay-backed profile/session model.

Profile switching posts to the existing route:

```text
POST /profiles/use
```

This means the MLWR page does not create a separate identity system.

The currently selected profile determines the signer used for publish actions.

## Domain-To-Action Mapping

The MLWR page maps receipt-domain actions to generic OpenETR actions as follows.

### Issue Receipt

Domain language:

- issue warehouse receipt

OpenETR mapping:

- `kind = 31415`
- origin event
- object digest from uploaded receipt file
- signed by selected profile

Current service:

```text
publish_issue_etr
```

### Transfer Receipt

Domain language:

- transfer receipt to another holder

OpenETR mapping:

- `kind = 31416`
- `action = initiate`
- `p = transferee_pubkey`

Current service:

```text
publish_transfer_initiate_event
```

### Accept Transfer

Domain language:

- accept receipt transfer

OpenETR mapping:

- `kind = 31416`
- `action = accept`
- references pending initiate event

Current service:

```text
publish_transfer_accept_event
```

### Record Pledge Or Lien

Domain language:

- record pledge
- record lien
- record restriction

OpenETR mapping:

- `kind = 31416`
- `action = encumber`
- `p = secured_party_pubkey`
- optional `type`
- optional `ref`

Current service:

```text
publish_auxiliary_control_event(action=encumber)
```

### Release Pledge Or Lien

Domain language:

- release pledge
- discharge lien
- release restriction

OpenETR mapping:

- `kind = 31416`
- `action = discharge`
- `enc = encumbrance_event_id`
- optional `p = releasing_party_pubkey`
- optional `ref`

Current service:

```text
publish_auxiliary_control_event(action=discharge)
```

### Present For Delivery

Domain language:

- present receipt for delivery

OpenETR mapping:

- `kind = 31416`
- `action = redeem`
- `p = warehouse_operator_or_obligor_pubkey`
- optional `ref`

Current service:

```text
publish_auxiliary_control_event(action=redeem)
```

### Complete Delivery

Domain language:

- complete delivery
- end receipt lifecycle

OpenETR mapping:

- `kind = 31416`
- `action = terminate`
- optional signed `ref` tag

Current service:

```text
publish_auxiliary_control_event(action=terminate)
```

## Control Event Service

The new `openetr.services.control_events` module extracts reusable control-event publishing behavior out of the webapp.

Its responsibilities include:

- finding origin events for an object
- finding control events for an object
- resolving an active chain
- resolving a pending transfer initiation
- resolving a prior event back to an origin event
- building `kind 31416` control events
- signing with the provided signer key
- publishing to configured relays
- verifying publication by exact event id or replaceable slot
- returning structured publish results to adapters

The service raises `ControlEventError` for service-level failures.

This avoids making the service depend on CLI-specific `click.ClickException` behavior.

## Result Rendering

The MLWR result page does not create a separate state engine.

It reuses the generic query result from:

```text
build_query_etr_result
```

The result is rendered into warehouse receipt terms:

- origin event -> warehouse receipt origin / issuance
- current controller -> current holder / controller
- encumbrance summary -> pledges, liens, and restrictions
- redeem event -> presentation for delivery
- terminate event -> completed delivery / lifecycle end

This keeps the state calculation centralized while allowing the UI to be domain-native.

## Recognition Boundary

The MLWR webapp is a domain adapter, not a legal recognition engine.

It can show signed evidence that a receipt was issued, transferred, encumbered, discharged, presented, or terminated.

It does not decide:

- warehouse operator legal authority
- legal validity of the receipt
- protected-holder status
- legal effect of transfer
- pledge perfection
- priority among claims
- warehouse liability
- delivery entitlement

Those remain MLWR/local law, registry, contractual, institutional, or attestation-policy questions.

## Design Principles

The current implementation follows these principles.

### Domain Outside, General Inside

Domain language belongs in the webapp route and template layer.

OpenETR services should remain general enough to support multiple recognition profiles.

### Shared Core

The webapp should call the same service-layer workflows that CLI, agent CLI, and future APIs can call.

Where command logic exists only inside CLI functions, it should be promoted into a service before being reused by the webapp.

### Hypermedia Web Flow

The MLWR Control Desk should remain a hypermedia application rather than becoming a separate client-side app.

The preferred pattern is:

- render receipt state and available actions in HTML
- expose actions as ordinary forms and links
- use htmx for targeted swaps, loading indicators, and small interaction improvements
- keep custom client-side JavaScript to a minimum
- let the server return the next receipt or page representation after each action

This keeps the webapp aligned with a HATEOAS philosophy: the current page should tell the user which actions are available, and each action should produce the next server-rendered representation of the OpenETR state.

### Profile-Aware Signing

The active profile determines the signer.

Profile selection is therefore part of the domain workflow because a user may need to act as different warehouse receipt participants.

### Query After Publish

After a domain action publishes a control event, the webapp refreshes the receipt state using the same query service.

This makes the result page evidence-oriented rather than merely showing a form submission success.

## Current Limitations

The current implementation is intentionally practical and early.

Known limitations include:

- the warehouse receipt data model is still document-format neutral
- action forms operate from a known object digest and signed origin-event tags rather than a full structured receipt schema
- attestation forms are not yet exposed directly on the MLWR page
- amendment, cancellation, split receipts, partial delivery, substitution, and bulk goods are not yet modeled as first-class domain actions
- recognition profiles are not yet machine-enforced beyond current OpenETR chain and action checks
- the CLI still contains some older inline control-event publishing logic that should eventually call the same service layer

## Next Steps

Useful next implementation steps:

1. Add MLWR-specific attestation forms.
2. Add richer structured receipt metadata tags or optional schema-backed fields.
3. Add domain result sections for discharged claims, redemption events, and termination events.
4. Refactor CLI control commands to call `openetr.services.control_events`.
5. Add policy profiles for minimal demo, registry-backed, and secured-finance recognition modes.
6. Add tests for route registration, template rendering, and service event construction.
7. Add examples using `examples/MLWR001.pdf` and the warehouse/exporter/bank profile flow.

## Related Documents

- [OPENETR_MLWR_PROFILE.md](./OPENETR_MLWR_PROFILE.md)
- [OPENETR_GENERIC_TRANSFER_MODEL.md](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [CONTROL_EVENT_MINIMUM_SHAPES.md](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md](./OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md)
- [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [MULTI_MODALITY_ARCHITECTURE_NOTE.md](./MULTI_MODALITY_ARCHITECTURE_NOTE.md)

## Summary

The MLWR Control Desk establishes a domain-adapter pattern for OpenETR.

Users see warehouse receipt workflows. The system publishes and queries generalized OpenETR events.

That keeps the protocol portable while making the application surface intelligible to people working with warehouse receipts.
