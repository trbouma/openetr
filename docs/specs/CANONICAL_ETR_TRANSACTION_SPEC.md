# Canonical ETR Transaction Specification

This draft defines a canonical interaction model for OpenETR transactions.

For a simplified visual companion, see [CANONICAL_ETR_TRANSACTION_INFOGRAPHIC.md](./CANONICAL_ETR_TRANSACTION_INFOGRAPHIC.md).

It focuses on control-relevant actions and the minimum attestable structure required for an OpenETR scheme to express:

- issuance
- transfer
- attestation
- encumbrance
- discharge
- termination
- revocation of incomplete actions

The purpose of this note is not to prescribe one legal implementation for all use cases. It is to define a canonical transaction grammar that can be:

- independently attested
- independently recognized
- evaluated under explicit policy
- aligned with MLETR-style reliability requirements without relying on platform trust

## Status

Draft.

## Purpose

OpenETR treats legal effect as the result of attested actions rather than as the product of a platform or registry asserting state.

That means the canonical question is not:

> What does the system say happened?

It is:

> Which actions were declared, accepted where required, attested by accountable parties, and recognized under policy?

This specification defines the minimal matrix for answering that question.

## Core Principle

All control-relevant actions must be independently attested.

Legal effect arises only when all required actions are:

- performed
- attested
- recognized

In this model, attestation applies to each action, not merely to the final outcome.

At the same time, OpenETR does not require that every event be separately attested in every implementation profile.

An attestor may instead attest a later event, including a termination event, provided that the attestation reflects validation of the prior control chain necessary to recognize that later event.

This means OpenETR can support both:

- event-level attestation, where each control-relevant action is attested as it occurs
- chain-level attestation, where a later event is attested after the relevant prior chain has been validated

The decisive question is therefore not only whether an event was directly attested, but what the attestor is claiming to have validated and recognized.

This canonical model is intentionally strong.

In some limited operational contexts involving a small and otherwise trusted set of counterparties, the parties may choose to recognize the effect of a transfer without separate third-party attestation.

In that case, recognition arises from the parties' own agreed policy and trust relationship rather than from the fuller OpenETR attestation model.

Such a profile may be operationally sufficient for that narrower context, but it provides a weaker basis for independent verification, portability, and later dispute resolution.

## Canonical Interaction Matrix

| Lifecycle | Declare (Initiator) | Accept (Counterparty) |
|-----------|----------------------|------------------------|
| Issue | Declare Issue -> Attest(Declare) | — |
| Transfer | Declare Transfer -> Attest(Declare) | Accept Transfer -> Attest(Accept) |
| Attest | Declare Attestation -> Attest(Declare) | — |
| Encumber | Declare Encumbrance -> Attest(Declare) | — |
| Discharge | Declare Discharge -> Attest(Declare) | — |
| Terminate | Declare Termination (Release / Cancel / Substitute) -> Attest(Declare) | — |

In this matrix:

- `declare` means to publish the substantive control action or assertion being made
- `accept` means to publish the counterparty's acceptance where the lifecycle requires it
- `attest` means for an identifiable attestor to publish accountable recognition, witness, validation, or policy-backed support for the relevant declared or accepted action

## Foundational Rule

Effect exists only when all required actions are attested and recognized.

Therefore:

- Issue requires `Declare + Attest`
- Transfer requires `Declare + Accept + Attest(Declare) + Attest(Accept)`
- Attest requires `Declare + Attest`
- Encumber requires `Declare + Attest`
- Discharge requires `Declare + Attest`
- Terminate requires `Declare + Attest`

Recognition is external to raw event publication. An event may exist on relays and still lack effect if the required action set has not been completed or if the attestors are not recognized under policy.

## Terms

### Object

The electronic transferable record or the canonical object identifier to which a transaction applies.

### Controller

The party capable of exercising control over the object at a given moment.

### Initiator

The party that publishes the substantive control-relevant action or assertion.

### Counterparty

The party whose acceptance is required for the action to become effective.

### Attestor

An identifiable signing party whose attestation anchors accountable recognition, witness, validation, or policy-backed support for a specific declared or accepted action.

### Recognition

The policy act of treating an attested action set as effective for the relevant legal or operational context.

## Endorsement and Indorsement

OpenETR does not treat endorsement or indorsement as a standalone universal protocol primitive.

Instead, where relevant, OpenETR expresses endorsement or indorsement as an attestation associated with an underlying OpenETR event, with its legal or commercial characterization determined by the applicable recognition framework.

At the Control Layer, the relevant questions are:

- who signed
- what was declared
- which object was referenced
- whether control changed
- what assertions were made
- whether the resulting chain is recognized under policy

In the revised model:

- actions that change control are typically modeled as `TRANSFER`
- actions that add authenticated meaning, approval, instruction, limitation, or related assertions without themselves changing control are typically modeled as `ATTEST`

Whether a particular combination of `TRANSFER`, `ATTEST`, and related recognized events constitutes an endorsement or indorsement for legal or commercial purposes is determined by the applicable Recognition Layer.

## Event Validity and Recognition

Because OpenETR operates in an open environment, the protocol must distinguish between:

- event validity
- recognition

These are related, but they are not the same thing.

### Event Validity

Event validity concerns cryptographic and structural correctness.

Examples include:

- whether the event signature is valid
- whether the event id is valid
- whether the object identifier is well formed
- whether required tags are present
- whether referenced prior events exist
- whether the event chain is structurally traversable

These checks answer questions such as:

- Did this event occur in the claimed form?
- Is it well formed?
- Is it authentically attributable?

They do not determine whether the event should be treated as effective.

### Recognition

Recognition concerns the policy conditions under which an event or chain is treated as effective.

Examples include:

- whether the relevant controller was entitled to perform the action
- whether a transfer requires a corresponding accept event
- whether an encumbrance or discharge requires additional supporting conditions under policy
- whether a signer is recognized as a legitimate actor for the claimed role
- whether an attestation or chain is sufficient under the applicable policy

These checks answer questions such as:

- Should this event be treated as effective?
- Does this event satisfy the conditions for recognition?

### Consequence

An event may therefore be:

- valid but not recognized
- recognized only under a particular policy profile
- invalid and therefore incapable of recognition

This distinction is essential in OpenETR because anyone may publish an event, but not every published event deserves recognition as effective.

A useful way to express this distinction is to separate hard guards from soft guards.

- hard guards protect validity
- soft guards govern recognition

Hard guards prevent a transition because the event fails minimum validity requirements.

Soft guards do not necessarily prevent publication. Instead, they operate as policy conditions on the state transition model. They may:

- emit a warning at declaration time
- require confirmation by an operator or workflow
- lead a later evaluator to refuse recognition

In this sense, policy operates as a soft guard on state transitions. It does not necessarily prevent a declaration from being made, but it influences whether the resulting transition is later recognized as effective.

## Determination of Legal Effect and Recognition

In OpenETR, the determination of legal effect or operational recognition does not arise from a platform simply asserting state.

Instead, it arises from evaluation of the signed evidence chain.

That evidence chain may include:

- the origin event
- later control events
- any accept or terminate events
- any event-level or chain-level attestations
- any actor legitimacy attestations relevant to the participants

The determining party may therefore ask:

> Does the full signed chain satisfy the applicable validation rules and cryptographic checks for recognition?

### Signed Evidence Chain

The full control history exists as linked signed events.

Those events can be evaluated for:

- cryptographic correctness
- continuity of references
- consistency of object identity
- role and signer legitimacy
- compliance with the applicable guards or policy rules

This evidence does not need to remain inside any one platform, database, registry, or single operational system.

Because OpenETR is built on the Nostr protocol, the signed events can exist across multiple independent relays while remaining portable, attributable, and verifiable.

That is a fundamental difference from models in which the authoritative record is inseparable from one database, one registry operator, or one blockchain environment.

In OpenETR, the evidence chain can persist outside and independently of any one system because the relevant unit is the signed event itself rather than the custody of a single data store.

OpenETR now applies the same general design direction to its CLI administration layer as well: operational configuration is increasingly represented by relay-backed signed records rather than being treated as machine-local state alone.

### Recognition Basis

Legal effect or operational recognition may therefore be based on whether:

- the relevant events are cryptographically valid
- the event chain is coherent and complete enough for the use case
- the participants are recognized as legitimate actors where policy requires that
- the applicable guards or rules have been satisfied
- the relevant attestation claims, if any, are themselves valid and recognized

### Consequence

OpenETR therefore provides a basis for recognition by making the relevant chain available as inspectable, signed evidence.

The protocol does not itself declare final effect.

It enables the determining party to validate the chain according to:

- cryptographic correctness
- explicit guards and rules
- attestation policy
- recognition policy

This means OpenETR should not be understood as saying:

> Publication equals effect.

It should instead be understood as saying:

> Publication provides evidence. Recognition determines effect.

## Actor Legitimacy Attestation

OpenETR may also require a distinct form of attestation concerning the legitimacy of the participating actors themselves.

This is different from attestation of a transaction event or of a control chain.

It addresses questions such as:

- who this signer is
- whether the signer is a legitimate actor for the role being claimed
- whether the signer is recognized for purposes such as issuance, transfer, custody, attestation, encumbrance, discharge, redemption, or termination

This creates a useful distinction between:

- actor legitimacy attestation
- transaction attestation
- chain-level attestation

### Purpose

An event chain may be structurally valid and cryptographically well-formed while still depending on whether the participants are recognized as legitimate actors for the relevant role.

Examples may include:

- whether an issuer is recognized as a legitimate carrier
- whether a controller is recognized as the entitled party
- whether an attestor is recognized as an accepted validator under policy

### Consequence

Recognition of a control event may therefore depend not only on the event chain itself, but also on whether the relevant signers have been independently attested as legitimate actors for the roles they claim to perform.

### Working Interpretation

In a fuller OpenETR model, actor legitimacy attestation may bind an `npub` to one or more recognized identities, roles, or organizational attributes, such as:

- legal name
- role
- jurisdiction
- LEI
- policy reference
- attestation period or validity interval

This is a separate layer from attesting whether a given transaction event or control chain should be recognized.

## Canonical Action Types

### 1. Issue

Issue is the initial declaration that an object is being brought into effective circulation under the scheme.

Required actions:

- declare issue
- attest the declaration

No counterparty acceptance is required for issue in the canonical model.

Issue becomes effective only when the declaration is both:

- attested
- recognized

### 2. Transfer

Transfer is the movement of control from one controller to another.

Required actions:

- declare transfer by the initiating side
- accept transfer by the receiving side
- attest the declaration
- attest the acceptance

Transfer becomes effective only when all four action components are recognized.

### 3. Attest

Attestation is an authenticated assertion relating to the object or to a control-relevant event in its lifecycle.

Examples may include:

- custody
- inspection
- quality
- quantity
- certification

Required actions:

- declare attestation
- attest the declaration

No counterparty acceptance is required in the canonical model, although an application profile may add additional conditions for recognition.

Attestation does not by itself change the current controller.

### 4. Encumber

Encumbrance is an authenticated declaration that the object is subject to a claimed restriction, pledge, lien, security right, or similar burden relevant to recognition.

Required actions:

- declare encumbrance
- attest the declaration

No counterparty acceptance is required in the canonical minimum model, although an application profile may impose additional recognition conditions or require supporting evidence.

Encumbrance does not by itself change the current controller.

### 5. Discharge

Discharge is an authenticated declaration that a previously claimed encumbrance has been released, satisfied, or otherwise brought to an end.

Required actions:

- declare discharge
- attest the declaration

No counterparty acceptance is required in the canonical minimum model, although an application profile may impose additional recognition conditions or require linkage to the encumbrance being discharged.

Discharge does not by itself change the current controller.

### 6. Terminate

Termination ends or supersedes the current effective state of an object within the scheme.

Canonical termination forms include:

- release
- cancel
- substitute

Required actions:

- declare termination
- attest the declaration

No counterparty acceptance is required in the canonical model, although an application profile may impose one.

## Working Event Kind Allocation

For the current OpenETR reference direction, canonical transaction families are split across distinct event kinds.

The working registry for these assignments is maintained in [EVENT_KIND_REGISTRY.md](./EVENT_KIND_REGISTRY.md).

Working allocation:

- `31415` = origin event
- `31416` = control transfer event

### Origin Event

The origin event is the event by which an object first enters the OpenETR scheme.

It is intended to represent:

- initial issuance
- initial declaration of the object within the scheme
- the first effective control-relevant state for that object

In the current working model, origin events are published as:

- `kind = 31415`

### Control Transfer Event

The control transfer event is the event by which control moves after origin.

It is intended to represent:

- transfer of control from one controller to another
- later control transitions in the object lifecycle

In the current working model, control transfer events are published as:

- `kind = 31416`

### Working `31416` Action Family

Within the current working model, `kind 31416` is treated as a control-event family rather than as a single undifferentiated action.

The action distinction is currently expressed through the `action` tag:

- `action=initiate`
- `action=accept`
- `action=terminate`

This means that:

- transfer initiation
- transfer acceptance
- termination

are presently modeled as distinct actions within the same `31416` event family rather than as separate event kinds.

This is a working design choice, not yet a final registry decision.

### Working Tag Conventions

The current reference implementation also uses a working split between:

- `o` as the object identifier carried forward across the full object history
- `d` as the replaceable slot identifier for the specific action being expressed

Current working examples:

- origin event:
  - `d = <object_hex>`
  - `o = <object_hex>`
- transfer initiate:
  - `d = <object_hex>:initiate`
  - `o = <object_hex>`
- transfer accept:
  - `d = <object_hex>:accept`
  - `o = <object_hex>`
- terminate:
  - `d = <object_hex>:terminate`
  - `o = <object_hex>`

This keeps the full chain object-centric while allowing replaceable slots to distinguish action types for the same object.

### Why Split Kinds

This split is useful because it distinguishes:

- the event that brings an object into the scheme
- the events that subsequently move control over that object

That separation improves:

- query clarity
- lifecycle reasoning
- validation logic
- traversal of control history

It also allows an implementation to identify the initial OpenETR record without inferring it only from timestamps or event ordering within a single mixed event family.

### Current Scope

This specification currently treats the following as the working minimum:

- issue/origin mapped to `31415`
- control transfer mapped to `31416`

Attestation, termination, substitution, cancellation, encumbrance, discharge, redemption, and revocation may later receive their own event kinds or remain subtyped within broader event families depending on implementation experience.

This allocation should therefore be treated as:

- current working convention
- not yet a final permanent registry decision

## Query Implications

Under this split-kind model:

- initial-record discovery should query origin events
- control-history traversal should query control transfer events
- full object-state evaluation will typically need both event families

In practice that means an implementation may need to:

1. query the object's origin event using `kind = 31415`
2. query subsequent control transfer events using `kind = 31416`
3. evaluate the attested action chain across both families

In the current reference flow, object-history evaluation is therefore object-centric first.

That is, implementations commonly:

1. determine the object identifier
2. query origin and control events by the object's `o` tag
3. derive candidate control chains from linked `e` references
4. apply local policy to determine which chain, if any, is recognized

This helps support:

- current-controller determination
- termination guards
- ambiguity detection where more than one candidate control chain exists for the same object

This is consistent with the broader OpenETR design goal of making lifecycle semantics explicit rather than collapsing all control-relevant actions into one undifferentiated event stream.

## Replaceable Events and Attested Binding Effect

OpenETR does not require raw transaction events to be permanently preserved at the relay layer in order for them to matter.

The current design direction assumes that canonical transaction events may be published as Nostr replaceable events.

That means there may be nothing at the relay layer alone to prevent an author from:

- replacing the event
- deleting the event from a particular relay's retained view
- making the event difficult to recover later from ordinary relay queries

This is not treated as a fatal flaw in the scheme.

### Core Distinction

OpenETR distinguishes between:

- the transaction event
- the attestation event

The transaction event expresses the underlying control-relevant act.

The attestation event expresses the accountable statement that the act was witnessed, evaluated under policy, and recognized for effect.

In this model, binding effect does not arise from the relay persistence of the underlying transaction event alone.

Binding effect arises when an identifiable attestor issues an attestation referencing that transaction event and thereby assumes accountability for having witnessed and evaluated it.

### Consequence

An event may later be replaced, removed, or become unavailable from common relay views, while an attestation concerning it still remains the binding evidence that the event existed and satisfied policy at the relevant time.

The attestation therefore functions as:

- witnessed evidence
- policy-bearing evidence
- accountability-bearing evidence

### Trust Anchor

The trust anchor in OpenETR is not platform behavior.

It is the accountable use of protocol by recognized attestors.

This means the scheme does not ultimately rely on the proposition:

> the platform preserved the event, therefore the effect is trustworthy

Instead, it relies on the proposition:

> the attestor is accountable for having witnessed and evaluated the event under policy

### Why This Matters

This distinction allows OpenETR to avoid making legal or operational effect depend entirely on:

- relay retention
- platform immutability claims
- centralized registry persistence

It places the decisive weight on identifiable actors who can be reviewed, challenged, and held accountable.

### Persistence as Evidence

Persistence is still valuable.

An event that remains queryable across relays is useful evidence.

However, persistence is not treated as the ultimate source of effect.

The decisive source of effect is attested witness combined with recognition under policy.

### Specification Implication

Future OpenETR specifications should therefore distinguish clearly between:

- transaction-event semantics
- event-level attestation semantics
- chain-level attestation semantics
- recognition of final effect after validation of the relevant prior chain
- attestation-event semantics
- recognition rules

Transaction events may remain replaceable.

Attestation events are the layer at which witnessed reliability and accountable effect are anchored.

## Revocation

Revocation is not a lifecycle transition in the same sense as issue, transfer, attest, or terminate.

Revocation applies only to actions that are:

- declared
- optionally accepted
- not yet fully attested

That means revocation is a control on incomplete action sets.

Revocation itself must be:

- declared
- attested

Revocation must not be used to unwind a transaction that has already become effective under the canonical rule unless a separate correction, dispute, rescission, or termination policy expressly permits it.

## Action Completion Model

A transaction is not evaluated as a monolithic event. It is evaluated as an action set.

The minimum evaluation steps are:

1. Identify the intended lifecycle action.
2. Determine the required action components for that lifecycle.
3. Determine whether each required component exists.
4. Determine whether each required component is attested.
5. Determine whether the attestors are recognized under policy.
6. Determine whether the action set is internally consistent and refers to the same object and transaction context.
7. Conclude effect only if the complete required set is present, attested, and recognized.

## Reliable Method Under MLETR

MLETR requires a reliable method to:

- identify the record
- preserve integrity
- establish exclusive control
- identify the person in control

MLETR deliberately does not prescribe one implementation.

OpenETR therefore does not claim that attestation is required by MLETR as such.

Instead, OpenETR uses attestation as the mechanism by which reliability is achieved and evidenced.

### OpenETR formulation

OpenETR satisfies the reliable-method requirement by making reliability attributable to identifiable attestors (`npubs`) who apply defined policies, rather than to a platform or system as a whole.

### Consequences

This means:

- identifiability is anchored in public keys
- accountability is anchored in signatures attributable to specific attestors
- integrity is anchored in the event and attestation chain
- exclusive control is expressed by recognizing only properly attested control transitions as effective

## Actor-Based Reliability

This specification rejects platform-based reliability as the canonical trust model.

It does not assume:

- the platform is reliable because it is certified
- the registry is reliable because it is centralized
- the application is reliable because it controls the database

Instead, it adopts actor-based reliability:

- each control-relevant action is attributable
- each attestor is identifiable
- each attestor is accountable for the application of policy
- each attestation can be independently reviewed

### Canonical rule

Every control-relevant action must be attested by an identifiable party whose public key anchors accountability for the application of policy.

## Why This Is Stronger Than Platform Trust

### 1. Granular accountability

The relevant question becomes:

> Who attested this specific action?

instead of:

> Which system was supposed to manage it?

### 2. Composability

Different policies and attestors may coexist.

The scheme can support:

- multiple attestors
- different recognition rules
- layered validation
- selective acceptance by different relying parties

### 3. Auditability

Each attestation is:

- signed
- attributable
- reviewable
- separable from platform claims

### 4. Legal alignment

Legal systems ultimately hold actors and entities accountable, not software abstractions.

This model aligns the technical structure with that practical legal reality.

## Transaction Recognition

Recognition is out of scope for the raw event layer and in scope for policy.

An implementation profile must specify:

- which attestors are recognized
- which policies they are expected to apply
- whether one or multiple attestations are required for a given action
- how conflicts are resolved
- how disputes, rescissions, and substitutions are handled

This specification only defines the canonical minimum:

- no effect without a fully attested required action set

## Minimum Data Expectations

This specification does not yet define a final wire format, but each canonical transaction should be able to express at least:

- the object identifier
- the lifecycle type
- the action type
- the initiating party
- the counterparty where applicable
- the attestor identity
- the policy context or policy reference
- the relationship to prior actions where applicable
- the signature covering the action

## Canonical Validation Rules

An OpenETR transaction action should be considered canonically valid only if:

- the object is clearly identified
- the action type is clearly identified
- the signer is identifiable
- the attestation is cryptographically valid
- the action is internally consistent with its referenced object and counterpart actions
- the action satisfies the lifecycle’s required interaction pattern

An OpenETR transaction becomes canonically effective only if:

- all required actions are present
- all required actions are attested
- the relevant attestors are recognized

## Transaction Families

This specification is intended to support transaction families such as:

- canonical issue transactions
- canonical transfer transactions
- canonical attestation transactions
- canonical encumbrance transactions
- canonical discharge transactions
- canonical termination transactions
- canonical revocation transactions for incomplete action sets

Future companion specifications may define:

- a canonical event schema
- a canonical attestor schema
- policy reference formats
- dispute and rescission handling
- transaction grouping and correlation identifiers

## Non-Goals

This draft does not yet define:

- a complete JSON schema
- a final Nostr event-kind assignment
- jurisdiction-specific legal effect rules
- substantive commercial law rules for title, negotiability, or legal effect
- a universal recognition policy

## Summary

The central move in this specification is simple:

Reliability is not treated as a property of systems.
It is treated as a property of accountable actors applying policy.

OpenETR makes that accountability explicit through attestation.

That allows the scheme to express control-relevant transactions in a way that is:

- independently verifiable
- policy-aware
- portable across infrastructures
- aligned with the technology-neutral logic of MLETR
