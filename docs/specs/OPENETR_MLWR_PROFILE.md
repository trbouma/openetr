# OpenETR MLWR Profile Design Note

This note sketches an OpenETR profile for warehouse receipts under UNCITRAL-UNIDROIT Model Law on Warehouse Receipts (MLWR) style regimes.

It is a starting design note, not a final legal or implementation specification.

## Status

Draft.

This note reflects the current OpenETR generalized Control Layer, Nostr wire format, and CLI behavior.

## Purpose

The purpose of this profile is to connect OpenETR's generic control model to warehouse receipt workflows.

The MLWR profile should answer:

- how a warehouse receipt is represented as a Controlled Object
- which warehouse receipt roles map to OpenETR participants and profiles
- which OpenETR control records correspond to receipt issuance evidence, transfer, encumbrance, discharge, redemption, and termination
- what evidence OpenETR can provide to a recognition framework
- which questions remain outside OpenETR and must be answered by MLWR-style law, local enactment, contract, registry rules, or institutional policy

The first product focus is the warehouse operator issuance workflow described in [MLWR_WAREHOUSE_OPERATOR_ISSUANCE_USE_CASE.md](./MLWR_WAREHOUSE_OPERATOR_ISSUANCE_USE_CASE.md).

That use case deliberately treats the warehouse receipt as an opaque artifact. OpenETR commits to the receipt by digest and records the signed control graph for that digest. It does not need to parse or validate the receipt contents in order to provide control evidence.

Terminology matters here because the warehouse receipt may itself be a record. In this profile:

- the **warehouse receipt document** is the Controlled Object;
- an **OpenETR control record** is a signed origin or control event about that object;
- the **OpenETR control graph** is the linked set of control records for that object.

OpenETR does not replace the MLWR or any local warehouse receipt law.

OpenETR provides a signed, inspectable, protocol-neutral evidence layer that an MLWR-style recognition framework can evaluate.

## Legal And Architectural Boundary

OpenETR belongs to the Control Layer.

It records authenticated control facts and control-relevant assertions.

It does not by itself determine:

- whether a warehouse receipt is legally valid
- whether the goods described by the receipt exist or conform
- whether a warehouse operator is licensed, bonded, or otherwise authorized
- whether a holder is protected under an applicable law
- whether a pledge or security right is perfected
- priority among competing claims
- warehouse liability or defenses
- legal title to goods
- final legal effect of transfer, pledge, discharge, redemption, or termination

Those questions belong to the Recognition Layer.

In this profile, the Recognition Layer may include:

- the enacted warehouse receipt law
- MLWR-based local legislation
- warehouse licensing rules
- registry or platform rules
- secured transactions law
- contract terms
- institutional policy
- attestation or certification requirements

## Profile Scope

This profile is intended to support electronic warehouse receipt workflows including:

- creation of an initial OpenETR control record for a warehouse receipt
- identification of the warehouse operator and initial depositor or holder
- transfer of control over the receipt
- declaration of pledges, liens, restrictions, or other encumbrances
- discharge or release of encumbrances
- presentation for delivery or performance
- termination after delivery, cancellation, or other lifecycle completion

It is not intended to define a complete warehouse receipt data schema.

The receipt document itself may be a PDF, JSON document, signed document bundle, verifiable credential, or another canonical representation. OpenETR identifies it by digest and carries the control-event history around that digest.

## Roles

The MLWR profile maps warehouse receipt actors into OpenETR participant roles.

### Warehouse Operator

The warehouse operator is the party that issues the receipt and is obligated, subject to the applicable law and receipt terms, with respect to the stored goods.

In OpenETR, the warehouse operator will commonly be represented by a profile signer.

The warehouse operator may act as:

- issuer
- obligor
- attestor of custody or receipt terms
- terminating party after delivery or cancellation

### Depositor

The depositor is the party that deposits goods or on whose behalf goods are stored.

The depositor may be the initial controller, but this is a profile choice rather than a universal rule.

Some workflows may issue the receipt directly to the depositor. Others may issue from the warehouse operator as initial controller and then transfer to the depositor.

### Holder Or Current Controller

The holder or current controller is the participant that controls the electronic warehouse receipt under the evaluated OpenETR control chain.

This role is evidence-relevant, but OpenETR does not by itself decide whether the holder has protected-holder status or any equivalent legal status.

### Transferee

The transferee is the participant to whom control is being transferred.

In OpenETR, transfer is represented by a control-event chain involving `initiate` and, where the profile requires it, `accept`.

### Secured Party Or Pledgee

The secured party or pledgee is the beneficiary of an encumbrance, pledge, security right, lien, or similar claim affecting the receipt.

In OpenETR, this party is represented by the `p` tag on an `encumber` event.

### Releasing Party

The releasing party is the participant associated with the release, satisfaction, or discharge of a previously declared encumbrance.

In OpenETR, this party may be represented by the `p` tag on a `discharge` event.

Recognition policy must decide who is entitled to discharge a particular encumbrance.

### Attestor Or Recognition Authority

An attestor may be a warehouse registry, auditor, inspection service, licensing authority, financing platform, trusted counterparty, or other participant that publishes accountable assertions about the receipt, parties, goods, chain, or event.

Attestation does not change control by itself.

It supplies evidence that may be required for recognition under a particular MLWR implementation or institutional workflow.

## Event Mapping

The current OpenETR implementation uses:

- `kind 31415` for origin events
- `kind 31416` for control-relevant events

The MLWR profile maps warehouse receipt actions onto that event family as follows.

| Warehouse receipt action | OpenETR event | Current CLI surface | Control effect |
| --- | --- | --- | --- |
| Create initial control record for receipt | `kind 31415` origin | `openetr issue-etr <receipt-file>` | establishes origin and initial controller evidence for the receipt digest |
| Initiate transfer | `31416`, `action=initiate` | `openetr transfer initiate <receipt-file> --transferee <profile>` | candidate transfer toward transferee |
| Accept transfer | `31416`, `action=accept` | `openetr transfer accept <receipt-file>` | acceptance evidence; recognition depends on policy |
| Attest fact or event | `31416`, `action=attest` | `openetr attest <receipt-file>` | no controller change |
| Declare pledge, lien, or restriction | `31416`, `action=encumber` | `openetr encumber <receipt-file> --beneficiary <profile>` | no controller change |
| Release pledge, lien, or restriction | `31416`, `action=discharge` | `openetr discharge <receipt-file> --encumbrance-event <event>` | no controller change |
| Present for delivery | `31416`, `action=redeem` | `openetr redeem <receipt-file> --obligor <profile>` | redemption-pending state |
| End lifecycle | `31416`, `action=terminate` | `openetr terminate-etr <receipt-file>` | terminated lifecycle state |

## Initial Control Record

The warehouse receipt may be issued by an external warehouse system, document system, or legal process. OpenETR begins when a profile publishes an origin control record for the receipt document digest.

The receipt document is hashed, and the resulting digest is used as the OpenETR object identifier.

Minimum current wire shape:

- `kind = 31415`
- `d = <object_hex>`
- `o = <object_hex>`
- author = issuing profile signer

In an MLWR profile, policy should specify:

- whether the warehouse operator must be the signer of the initial control record
- whether the initial controller is the warehouse operator, depositor, or another party
- whether the receipt must include structured warehouse receipt fields
- whether a warehouse operator profile must include a legal name, address, license, registry id, or other credentials
- whether receipt issuance or control-record creation requires an attestation by a registry, platform, or public authority

OpenETR can prove that a particular profile signed the origin control record for a particular receipt digest. It cannot by itself prove that the signer was legally authorized to issue warehouse receipts, or that the receipt itself was validly issued under applicable law.

## Transfer Of Control

Transfer is represented by the current OpenETR transfer action family.

The initiating party publishes:

- `kind = 31416`
- `action = initiate`
- `p = <transferee_pubkey_hex>`
- `o = <object_hex>`
- `e = <prior_event_id>`

The transferee may then publish:

- `kind = 31416`
- `action = accept`
- `o = <object_hex>`
- `e = <initiate_event_id_or_prior_event_id>`

The MLWR profile should specify when transfer is recognized as effective.

Possible recognition rules include:

- unilateral transfer initiation is enough among trusted parties
- transfer requires transferee acceptance
- transfer requires warehouse operator acknowledgement
- transfer requires registry attestation
- transfer is blocked or flagged while outstanding encumbrances exist
- transfer is recognized only if the transferor is the current controller under the accepted chain

OpenETR can provide the signed chain. The MLWR profile decides which chain is legally or institutionally recognized.

## Encumbrance And Pledge

Warehouse receipts are commonly used in secured finance.

The MLWR profile should treat pledge, lien, and security-right evidence as first-class control-relevant assertions without assuming that publication alone creates or perfects the right.

An encumbrance event currently uses:

- `kind = 31416`
- `action = encumber`
- `p = <beneficiary_or_secured_party_pubkey_hex>`
- optional `type`, such as `pledge`, `lien`, or `restriction`
- optional `ref`, such as a financing agreement, loan id, registry reference, or business reference

The query service derives outstanding encumbrances by finding `encumber` events that have not been matched by a later `discharge` event referencing the encumbrance event id.

Recognition policy should specify:

- who may create a recognized encumbrance
- whether the current controller must sign the encumbrance
- whether the secured party must accept or attest the encumbrance
- whether warehouse operator acknowledgement is required
- whether registration in a separate secured transactions registry is required
- whether an encumbrance restricts later transfer, redemption, or termination
- how priority is determined among multiple encumbrances

OpenETR can show that an encumbrance was declared, by whom, in favor of whom, and whether a matching discharge event exists. It does not decide perfection, priority, or enforceability.

## Discharge

Discharge records release or satisfaction of a particular encumbrance.

The discharge event should identify the encumbrance being discharged:

- `kind = 31416`
- `action = discharge`
- `enc = <encumbrance_event_id_hex>`
- optional `p = <releasing_party_pubkey_hex>`
- optional `ref = <release_reference>`

The MLWR profile should specify:

- who is entitled to discharge an encumbrance
- whether the secured party must sign the discharge
- whether the current controller, warehouse operator, registry, or financing platform must also attest
- whether partial discharge is allowed
- whether discharge requires reference to an external satisfaction or settlement record

For the current implementation, `openetr query-etr` can report total, discharged, and outstanding encumbrances.

## Redemption And Delivery

Redemption represents presentation of the warehouse receipt for delivery of goods or other performance by the warehouse operator.

The current event shape is:

- `kind = 31416`
- `action = redeem`
- `p = <obligor_pubkey_hex>`
- optional `ref = <presentation_or_claim_reference>`

For warehouse receipts, the obligor will commonly be the warehouse operator.

The MLWR profile should specify:

- who may redeem
- whether the redeemer must be the current controller
- whether outstanding encumbrances block redemption
- whether warehouse operator acknowledgement is required
- whether redemption creates a redemption-pending state before final delivery
- what evidence is required before termination

OpenETR can record presentation. It does not by itself compel delivery or decide whether the presenter is legally entitled to the goods.

## Termination

Termination records that the OpenETR lifecycle for the warehouse receipt has ended.

In an MLWR profile, termination may correspond to:

- delivery of goods
- cancellation of the receipt
- replacement or substitution under a recognized procedure
- expiry or invalidation under applicable law
- a court, registry, or warehouse-directed termination process

The current event shape is:

- `kind = 31416`
- `action = terminate`
- `o = <object_hex>`
- `e = <prior_event_id>`

Recognition policy should specify who may terminate and what evidence is required.

## Attestation

Attestation is likely central to a robust MLWR profile.

Attestation can attach accountable evidence to the receipt or to a specific event.

Possible attestations include:

- warehouse operator identity or authorization
- receipt issuance approval
- goods inspection
- quantity or quality certification
- insurance status
- warehouse custody confirmation
- registry acknowledgement
- transfer recognition
- encumbrance acknowledgement
- discharge acknowledgement
- redemption acceptance
- delivery completion

The current attestation shape is:

- `kind = 31416`
- `action = attest`
- `e = <specific_event_id_being_attested>`
- optional `type = <attestation_type>`
- optional `p = <subject_pubkey_hex>`
- optional `ref = <external_reference>`

The MLWR profile should define attestation types and which are required for each recognition context.

## Suggested MLWR Recognition Rules

This section is intentionally preliminary.

A practical MLWR profile may eventually define rule sets such as:

### Minimal Demonstration Profile

- warehouse operator issues the receipt
- current controller may transfer
- transferee acceptance completes transfer
- encumbrances are visible but do not automatically block transfer or redemption
- discharge is recognized if signed by the encumbrance beneficiary or releasing party
- redemption places the receipt into redemption-pending state
- warehouse operator termination ends the lifecycle

### Registry-Backed Profile

- warehouse operator issuance requires registry attestation
- transfer requires registry or warehouse acknowledgement
- encumbrance requires secured-party acceptance or registry notice
- discharge requires secured-party signature and registry acknowledgement
- redemption requires current controller presentation and warehouse acknowledgement
- termination requires warehouse operator signature and registry attestation

### Secured-Finance Profile

- encumbrances block transfer, redemption, or termination unless discharged or expressly consented to
- secured-party acceptance is required for recognized pledge creation
- priority is determined by registry time, attestation time, or another policy rule
- partial discharge and subordination require explicit event types or structured references

These rule sets are not part of the base OpenETR wire format. They are recognition profiles built on top of the signed event evidence.

## Example Lifecycle

One MLWR-style lifecycle may look like:

1. Warehouse operator creates a profile.
2. Warehouse operator publishes a profile with legal name, address, and optional registry identifiers.
3. Warehouse operator creates the initial OpenETR control record for the already-issued receipt:

   ```bash
   openetr issue-etr examples/MLWR001.pdf
   ```

4. Warehouse transfers control to the depositor or exporter:

   ```bash
   openetr transfer initiate examples/MLWR001.pdf --transferee exporter
   openetr profile use exporter
   openetr transfer accept examples/MLWR001.pdf
   ```

5. Exporter pledges the receipt to a bank:

   ```bash
   openetr encumber examples/MLWR001.pdf \
     --beneficiary bank \
     --type pledge \
     --ref loan-MLWR001-001
   ```

6. Bank releases the pledge after payment or settlement:

   ```bash
   openetr discharge examples/MLWR001.pdf \
     --encumbrance-event <encumbrance_event_id_or_nevent> \
     --releasing-party bank \
     --ref release-MLWR001-001
   ```

7. Current controller presents the receipt to the warehouse operator:

   ```bash
   openetr redeem examples/MLWR001.pdf --obligor warehouse --ref delivery-request-MLWR001
   ```

8. Warehouse operator completes delivery and terminates the receipt lifecycle:

   ```bash
   openetr profile use warehouse
   openetr terminate-etr examples/MLWR001.pdf
   ```

9. Anyone with access to the relevant relays can query the history:

   ```bash
   openetr query-etr examples/MLWR001.pdf
   ```

The query result should show the origin control record, later control records, lifecycle state, current controller, profile metadata, and outstanding encumbrance state.

## Open Questions

The MLWR profile still needs answers to several design questions:

- What minimum structured fields should a warehouse receipt contain?
- Should OpenETR define a canonical receipt JSON format, or remain document-format neutral?
- Which actor should be the initial controller after issuance?
- Is transfer initiation alone ever enough, or should acceptance always be required?
- When should warehouse operator acknowledgement be required?
- When should registry attestation be required?
- What event shape should represent amendment, replacement, cancellation, or split receipts?
- How should partial delivery be modeled?
- How should fungible bulk goods, commingled goods, or warehouse substitutions be represented?
- How should priority among multiple encumbrances be represented or referenced?
- Should encumbrance acceptance be a separate event or an attestation attached to the encumbrance event?
- Should redemption require discharge of all outstanding encumbrances?
- What is the minimum profile metadata for warehouse operators and secured parties?

## Related Specifications

- [OPENETR_GENERIC_TRANSFER_MODEL.md](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- [CANONICAL_ETR_TRANSACTION_SPEC.md](./CANONICAL_ETR_TRANSACTION_SPEC.md)
- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [CONTROL_EVENT_MINIMUM_SHAPES.md](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md](./OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md)
- [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)

## Summary

The MLWR profile should treat OpenETR as a signed evidence layer for warehouse receipt control.

OpenETR can identify the receipt, publish and query the control history, expose the current controller under a chosen recognition profile, and report encumbrance, discharge, redemption, and termination evidence.

The MLWR or local enactment remains responsible for legal validity, protected-holder status, warehouse obligations, pledge effect, priority, enforcement, and final recognition.
