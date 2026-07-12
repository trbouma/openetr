# OpenETR Layered Architecture Note

This note describes the relationship between:

- the Nostr wire format
- OpenETR as a general control layer
- domain adapters such as the MLWR warehouse receipts surface
- recognition frameworks that give legal or operational effect to the evidence

The short version is:

```text
Domain adapter        MLWR, MLETR, bills of lading, receipts, credentials
OpenETR control       objects, origin events, control events, profiles, state
Nostr wire format     signed events, kinds, tags, relays, event ids
Recognition layer     law, contracts, registry rules, institutional policy
```

OpenETR sits in the middle. It translates domain actions into portable signed control evidence without making every domain share the same user interface, vocabulary, statute, or business process.

## Nostr Wire Format

The Nostr wire format is the publication and retrieval substrate.

At this layer, OpenETR defines:

- event kinds such as `1415` for origin events and `1416` for control events
- core query and traversal tags such as `o`, `e`, and `p`
- signed named tags for structured event data such as `name`, `size_bytes`, `domain`, `document_type`, `record_reference`, or `record_description`
- readable event `content` for narrative context rather than machine parsing
- relay-backed publication and retrieval conventions

This layer answers questions such as:

- what event kind is published?
- which tags identify the object?
- how is the control chain traversed?
- what signed data is present in the event?
- which relays can return the relevant signed events?

It does not decide whether a warehouse receipt is legally valid, whether a transfer is protected, whether goods exist, or whether a registry must recognize an event.

## OpenETR Control Layer

OpenETR is the control layer above the wire format.

It interprets signed events as a control history for a Controlled Object.

At this layer, OpenETR defines:

- Controlled Objects identified by cryptographic digest
- origin events that bring an object into the OpenETR scheme
- control events for transfer, encumbrance, discharge, redemption, termination, and attestation
- profile-backed signing and participant identity
- current-controller derivation from origin and control-event chains
- lifecycle state derived from the signed event history
- guardrails against ambiguous or duplicate actions where appropriate

The control layer is domain-neutral.

It should not need to know whether an object is a warehouse receipt, bill of lading, certificate, credential, or another transferable record. It provides the common machinery for signed control evidence and state evaluation.

In implementation terms, this is the role of the `openetr` Python component, CLI, and shared service layer.

## Domain Adapters

Domain adapters sit above the OpenETR control layer.

A domain adapter presents a workflow in the vocabulary of a particular legal, commercial, or operational setting, then translates those actions into the general OpenETR control model.

The MLWR warehouse receipts webapp is the current example.

It speaks in terms of:

- issue receipt
- query receipt
- current holder / controller
- transfer receipt
- pledge, lien, or restriction
- release encumbrance
- present for delivery
- complete delivery

Under the surface, those actions map to general OpenETR operations:

- issue receipt -> origin event
- transfer receipt -> transfer initiate / accept control events
- pledge or restriction -> encumber control event
- release encumbrance -> discharge control event
- present for delivery -> redeem control event
- complete delivery -> terminate control event

The adapter may add domain-specific signed tags, such as:

- `["domain", "mlwr"]`
- `["document_type", "warehouse_receipt"]`
- `["record_reference", "<receipt_reference_or_other_domain_reference>"]`
- `["record_description", "<goods_description_or_other_domain_description>"]`

These tags make the event intelligible to the domain without changing the core OpenETR control machinery.

This pattern lets OpenETR support multiple domains without hard-coding one legal instrument as the protocol itself.

## Recognition Layer

The recognition layer is above both OpenETR and the domain adapter.

This is where legal, institutional, registry, contractual, or policy rules decide the effect of the signed evidence.

For MLWR, recognition may depend on questions such as:

- was the issuer a legally recognized warehouse operator?
- did the receipt contain the required statutory information?
- was the method reliable under the applicable enactment?
- did the transfer make the transferee a holder or protected holder?
- did an encumbrance create, perfect, or release a security right?
- is delivery required under the receipt, storage agreement, and applicable law?

OpenETR does not answer those questions by itself.

Instead, it provides signed, portable, inspectable evidence that a recognition layer can evaluate.

## Recognition Inputs: TRQP, WoT, Registries, And Attestations

The recognition layer may use many different inputs.

Two important examples are:

- Trust Registry Query Protocol (TRQP);
- Nostr Web of Trust (WoT).

These models complement OpenETR because they mostly answer recognition questions rather than control questions.

OpenETR is focused on control evidence:

- what object exists;
- what event created the origin record;
- which signed events reference the object;
- how control events link through exact `e` references;
- which profile key signed each event;
- what candidate state can be derived from the graph.

TRQP and WoT ask different questions.

TRQP can answer authority and recognition questions such as:

- is this entity authorized by this authority to perform this action on this resource?
- does one authority recognize another authority for this action and resource?
- was the authorization or recognition valid in the relevant context?

Nostr Web of Trust can answer reputational and community-context questions such as:

- is this signer close to a trusted seed set?
- is this profile recognized by a community's social graph?
- does a trusted assertion provider publish a score or classification for this pubkey?
- should this signer, relay, attestor, or graph branch be ranked higher, warned about, or sent for manual review?

Other recognition inputs may include:

- explicit OpenETR attestation events;
- domain registries;
- local allow lists or deny lists;
- contractual network rules;
- statutory or regulatory requirements;
- enterprise account and role systems;
- court, regulator, bank, carrier, warehouse, or platform policies.

The design rule is:

> OpenETR should produce and verify portable control evidence. Recognition inputs decide what effect a verifier gives to that evidence.

This separation keeps OpenETR general.

A verifier can inspect the same signed OpenETR graph under different rule books:

- one verifier may recognize a transition because a TRQP registry says the signer was authorized;
- another may treat the same transition as warning-only because the signer is not known in its WoT graph;
- another may require both formal TRQP authorization and a high-confidence attestation;
- another may accept the graph locally under a private contract or enterprise policy.

Those differences do not fork the OpenETR control model. They are recognition overlays applied to the same signed evidence.

The verifier should therefore present:

- the shared signed control graph;
- structural and cryptographic validity;
- domain interpretation;
- recognition inputs consulted;
- warnings, denials, or confidence scores;
- the final recognized or candidate state under the selected policy.

Related recognition-input notes:

- [OPENETR_TRQP_INTEGRATION_NOTE.md](./OPENETR_TRQP_INTEGRATION_NOTE.md)
- [OPENETR_NOSTR_WEB_OF_TRUST_INTEGRATION_NOTE.md](./OPENETR_NOSTR_WEB_OF_TRUST_INTEGRATION_NOTE.md)
- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)

## Separation Rationale

This layering keeps the project flexible.

The Nostr wire format can remain small and interoperable.

The OpenETR control layer can remain general.

Domain adapters can feel natural to users working in a specific area.

Recognition frameworks can evolve independently, jurisdiction by jurisdiction or institution by institution.

The result is a model where a warehouse receipt system, a bill of lading system, a credential system, or another electronic transferable record system can all use the same signed control substrate without pretending that all domains have the same legal rules.

## Implementation Mapping

Current implementation artifacts roughly map as follows:

| Layer | Implementation artifacts |
| --- | --- |
| Nostr wire format | `OPENETR_NOSTR_WIRE_FORMAT_SPEC.md`, event kinds `1415` and `1416`, event tags, relay queries |
| OpenETR control layer | `openetr` Python package, CLI commands, `openetr.services.issue_etr`, `openetr.services.control_events`, `openetr.services.query_etr` |
| Domain adapters | MLWR Control Desk routes and templates, `MLWR_WEBAPP_DOMAIN_ADAPTER_DESIGN_NOTE.md`, `OPENETR_MLWR_PROFILE.md` |
| Recognition layer | generic verifier policy, MLWR article mapping, policy profiles, attestations, TRQP, WoT, legal or institutional rules outside the base protocol |

The central design rule is:

> Domain adapters translate domain language into OpenETR control operations. OpenETR translates control operations into signed Nostr wire-format events. Recognition layers decide what those events mean in law, policy, or institutional practice.
