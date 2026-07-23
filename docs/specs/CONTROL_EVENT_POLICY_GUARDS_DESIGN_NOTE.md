# Control Event Policy Guards Design Note

This note explains the role of application-side guard policy and recognition rules in the OpenETR control-event flow.

It is not a claim that OpenETR can prevent all invalid or conflicting events from being published.

Instead, it defines why local validation rules still matter and how they can serve as an early expression of the policy that future attestors, verifiers, or relying parties may apply before recognizing or attesting control-relevant events.

An underlying philosophy of the OpenETR protocol is:

> Transact globally, validate locally.

This is a deliberate play on "think globally, act locally."

OpenETR allows parties to publish and exchange control-relevant events in a shared global environment, while leaving validation, attestation, and recognition to the local policy of the party who must decide whether to rely on the resulting chain.

## Status

Draft.

## Purpose

OpenETR is an open event scheme.

That means a participant can still publish events that:

- violate local workflow assumptions
- conflict with earlier events
- reference the wrong object or wrong prior event
- omit information that a stricter implementation would require

The existence of that possibility does not weaken the value of validation rules.

It clarifies their proper role.

Validation rules in the web app, CLI, and shared service layer are useful because they:

- make the expected transaction grammar explicit
- reduce accidental misuse by ordinary operators
- provide a practical reference implementation of OpenETR policy
- create an early executable model of the checks that attestors may later apply before attesting events

The current component has therefore become a working reference implementation of several policy choices across the control-event set, including:

- object-based lookup of control history
- current-controller checks for transfer initiation and termination
- intended-transferee checks for transfer acceptance
- active-chain checks for attestations and auxiliary control events
- reference checks for encumbrance discharge
- warnings for duplicate origin issuance
- visibility of multiple candidate control chains for the same object

## Historical Context

OpenETR can also be understood against the background of global shipping and the historical ethos of the high seas.

Maritime trade developed across jurisdictions long before any single sovereign could govern global trade end to end.

Commerce at sea therefore depended on records, customs, and recognition practices that could travel across ports, carriers, merchants, financiers, and legal systems.

The high seas were not the domain of any one platform or any one legal authority.

What mattered was whether a record, claim, or act would be recognized by the party who needed to rely on it.

In that sense, OpenETR is an attempt to replicate digitally some of the same operating ethos:

- publication in a shared global environment
- movement across institutional and jurisdictional boundaries
- reliance on signed and reviewable evidence
- recognition by the relevant relying party rather than by a single controlling system

Just as maritime trade evolved to function across open waters and multiple jurisdictions, OpenETR is designed to function across an open digital environment where publication is global but recognition remains local.

## Core Distinction

OpenETR does not depend on the network preventing publication.

Instead, OpenETR depends on accountable recognition of valid actions.

The distinction is:

- publication is open
- recognition is conditional
- attestation is accountable

This means the question is not:

> Can an invalid event be published?

It is:

> Under what rules would an identifiable attestor refuse to attest or recognize that event?

Application and service guards are therefore not final enforcement.

They are an executable expression of those rules.

## Baseline Guards And Recognition Context

OpenETR implementations may enforce baseline guards in the web app, CLI, API, or shared service layer.

Those guards are important for consistency and operator safety. They can prevent the reference implementation from publishing obvious mistakes, such as a transfer initiation by a signer that is not the current controller, an acceptance by someone other than the named transferee, or a termination by someone who does not control the active chain according to the component's baseline graph evaluation.

However, these guards are not cryptographic enforcement.

A Nostr relay cannot know every OpenETR recognition context. Another client may publish a structurally valid event that bypasses the reference component. A later verifier may also apply stricter, looser, or domain-specific rules.

The correct model is therefore:

```text
baseline guard passes
  -> event may be published by this implementation
  -> downstream verifier reviews the signed graph
  -> recognition depends on the verifier's selected context
```

The downstream party must still decide whether the guard assumptions are valid for its recognition context.

Examples:

- A warehouse receipt registry may require a recognized warehouse operator profile before treating an origin record as effective.
- A secured lender may refuse recognition of a transfer while a recognized encumbrance remains outstanding.
- A regulator may require an authority or registry attestation even if the baseline OpenETR control graph is structurally clean.
- A private workflow may accept a lighter rule set for operational convenience while marking the result as limited-purpose evidence.

This is why the same guard logic is consolidated into a component: not to make OpenETR closed or permissioned, but to make the baseline behavior consistent, reviewable, testable, and replaceable by implementations with different recognition requirements.

## Event Validity Versus Recognition Rules

Because OpenETR operates in an open environment, anyone may publish an event.

That means OpenETR must distinguish clearly between:

- event validity
- recognition rules

These are not the same thing.

### Event Validity

Event validity concerns cryptographic and structural correctness.

Examples include:

- whether the event signature is valid
- whether the event id is valid
- whether the object identifier is well formed
- whether the required tags are present
- whether referenced prior events exist
- whether the event chain can be traversed

These checks answer questions such as:

- Did this event occur in the claimed form?
- Is it well formed?
- Is it authentically attributable?

They do not answer whether the event should be recognized as effective.

### Recognition Rules

Recognition rules concern the policy conditions under which an event or chain will be treated as effective.

Examples include:

- whether only the recognized current controller may initiate a transfer or terminate a graph
- whether a transfer requires a corresponding accept event
- whether a termination must be recognized as coming from a particular role
- whether an encumbrance blocks later recognition of transfer
- whether a discharge properly references a recognized encumbrance
- whether an attestation comes from a recognized attestor
- whether a signer is a recognized actor for the claimed role

These checks answer questions such as:

- Should this event be treated as effective?
- Does this event satisfy the applicable control or attestation policy?

### Distinction Rationale

OpenETR can authenticate events, but it does not by itself require that every authenticated event be recognized as effective.

That distinction is foundational in a permissionless environment.

The protocol can demonstrate:

- correctness
- attribution
- continuity

But recognition remains a matter of policy.

Accordingly, some rules that may appear in the CLI as publication guards should be understood conceptually as recognition rules rather than as mere syntax checks.

A useful way to describe this is to distinguish between hard guards and soft guards.

- hard guards protect validity
- soft guards govern recognition

Hard guards prevent a transition because the event is not valid enough to publish or process.

Examples include:

- invalid signature
- missing required tag
- malformed object identifier
- unresolvable prior reference

Soft guards do not necessarily prevent a transition from being declared or published. Instead, they operate as policy conditions on the state transition model. They may:

- emit a warning at declaration time
- require operator confirmation
- lead an attestor, assessor, or relying party to refuse recognition later

In OpenETR, policy rules can therefore be understood as soft guards on state transitions. They do not necessarily prevent a transition, but they may influence whether that transition is later recognized as effective.

## Determination of Recognition or Effect

In OpenETR, recognition or legal effect is not determined by the mere existence of a platform record.

It is determined by whether the relevant evidence chain is sufficient under the applicable policy.

That evidence chain may include:

- origin events
- transfer initiate and accept events
- encumbrance, discharge, redemption, and termination events
- event-level or chain-level attestations
- linked evidence records
- actor legitimacy attestations

The important point is that the entire chain exists as signed evidence.

That chain can be evaluated according to:

- cryptographic correctness
- object continuity
- reference integrity
- signer and role legitimacy
- applicable guards or validation rules
- attestation policy

That evidence can also exist outside and independently of any one system.

This follows from the inherent properties of the Nostr protocol: signed events can be published, carried, and later retrieved across multiple independent relays without being bound to a single application database or registry boundary.

That is a fundamental difference from:

- platform databases
- centralized registries
- blockchain systems where the authoritative record is bound to one chain environment

In OpenETR, the crucial unit is the signed event and the linked evidence chain, not custody by one authoritative data store.

This means the decisive question is not simply:

> Was an event published?

It is:

> Does the signed chain satisfy the rules for recognition?

In that sense, OpenETR provides a sound evidentiary basis for the determination of effect.

The protocol carries the signed history.

The determining party applies the rules.

## Validation Rule Rationale

A bypassable rule can still be valuable if it clearly states the expected policy.

In OpenETR, that value appears in four places.

### 1. User Safety

Operators using the CLI or web app should be protected from accidental mistakes such as:

- referencing the wrong prior event
- initiating a transfer from the wrong object history
- publishing a conflicting control event
- accepting a transfer that does not correspond to the expected object or intended counterparty
- discharging the wrong encumbrance
- terminating the wrong active chain

### 2. Policy Clarity

If a rule is implemented in the component, it is no longer merely implied.

It becomes a concrete statement of expected behavior.

That helps make future attestation logic easier to define and review.

### 3. Auditability

A validation rule that is explicit in code and in specifications can be:

- reviewed
- tested
- challenged
- revised

That is stronger than relying on vague operator intuition.

### 4. Attestor Alignment

Attestors do not need to trust that every event on the network is valid.

They need to know what checks they are expected to perform before attesting a control-relevant action.

Baseline component guards provide an early, concrete form of that checklist.

## Validation as Attestor and Verifier Policy

OpenETR should treat control-event validation rules as part of the emerging attestor policy layer.

That does not mean:

- MLETR requires a specific checklist
- every component guard is automatically legally decisive
- a relay or client can define legal effect on its own

It does mean:

- OpenETR can define baseline conditions under which the reference component treats a control event as publishable or cleanly reviewable
- attestors can later rely on those conditions when deciding whether to attest an event
- verifiers and relying parties can compare those conditions against their own recognition context
- the CLI and web app can serve as reference implementations of those conditions

This supports the broader OpenETR position that reliability is attributable to accountable actors applying policy, not to platform behavior alone.

## Actor Legitimacy as a Separate Attestation Layer

OpenETR may also require a separate attestation concerning whether a signer is a legitimate actor for the role being claimed.

This is different from attesting:

- a single transaction event
- a control chain
- a final recognized state

It addresses a different question:

> Is this signer a legitimate actor for this role?

Examples may include:

- whether an issuer is recognized as a legitimate carrier
- whether a signer is recognized as the entitled party
- whether an attestor is recognized as an accepted validating party

This matters because a chain may be structurally sound and still fail recognition if the relevant participants are not recognized as legitimate actors under the applicable policy.

In that sense, OpenETR may require both:

- event or chain validation
- actor legitimacy validation

The first asks whether the control history is valid.

The second asks whether the participants are recognized as appropriate actors within that history.

## Recommended Rule Classes

Not every validation concern needs the same outcome.

OpenETR should classify rules into categories that reflect whether they concern correctness, operator warning, or later recognition.

### Error

The command should block publication or completion because a minimum correctness condition has failed.

Examples:

- a referenced prior event cannot be found
- a control chain cannot be resolved back to a valid origin event
- the object identifier in a referenced event is missing or inconsistent
- an accept event references an event that is not a valid transfer initiate event

### Warning

The command should allow the action but require operator confirmation because the event is publishable but ambiguous, incomplete, or potentially inconsistent with later recognition policy.

Examples:

- a prior event already exists for the same object, action, and signer
- multiple origin events exist for the same object
- a later event may supersede an earlier event but the operator is still choosing to proceed

### Recognition Rule

The component may or may not enforce the condition at publication time, but the condition should be treated as part of recognition, attestation, or assessment policy.

Examples:

- whether the initiating party is the latest recognized controller
- whether a transfer is in conflict with another pending transfer for the same object
- whether the relevant attestor policy recognizes a particular signer or counterparty

This category is especially important because many OpenETR questions are not:

- Can the event be published?

but rather:

- Should the event be recognized as effective?

## Initial Control Event Rules to Formalize

The next practical step is to formalize the first control-event checks directly in the shared component and specs, then expose them consistently through the CLI and web app.

The baseline guard set should cover the control actions currently used by the reference implementation:

- `initiate`
- `accept`
- `encumber`
- `discharge`
- `redeem`
- `terminate`
- `attest`

Transfer remains the clearest example because it changes controller state, but the policy-guard model applies to the whole control-event set.

### Transfer Initiate

Candidate validation rules:

- the supplied prior event must exist
- the supplied prior event must be either:
  - a valid origin event, or
  - a valid control event that can be traversed back to an origin event
- the resulting origin event must belong to the same object being transferred
- the transferee must be a valid counterparty identifier
- a conflicting replaceable initiate event for the same object and signer should trigger a warning
- if the supplied prior event is a `kind 31415` origin event, the signer of the new `kind 31416` event should match the issuer of that origin event
- if the supplied prior event is a `kind 31416` control event, the signer of the new `kind 31416` event should match the current-controller semantics derived from that prior event
- if a subsequent transfer initiate is being published before a corresponding accept event has been observed for the prior transfer event, the component may warn but still allow publication

Current CLI behavior also supports a more object-centric initiation flow:

- the operator may identify the object directly, for example by supplying a digest or file
- the implementation may resolve the active control chain for that object
- the implementation may then choose the current controlling event as the effective prior event

This makes transfer initiation easier in ordinary operation while still preserving the ability to reference a specific prior event in expert workflows.

### Transfer Accept

Candidate validation rules:

- the referenced initiate event must exist
- the referenced event must actually be a transfer initiate event
- the object identifier must be present and valid
- the accept event must point to the intended initiate event
- the signer of the accept event should match the intended transferee identified in the initiate event's `p` tag
- a conflicting replaceable accept event for the same object and signer should trigger a warning or block, depending on policy

### Encumber

Candidate validation rules:

- the object to be encumbered must resolve to an existing origin event
- a single active control chain for that object must be determinable
- the beneficiary or secured party must resolve to a valid participant identifier
- a duplicate encumbrance event for the same object and signer should trigger a warning or block, depending on policy
- domain policy may decide whether only the current controller, a recognized secured party, or another role may publish the encumbrance

### Discharge

Candidate validation rules:

- the object to be discharged must resolve to an existing origin event
- a single active control chain for that object must be determinable
- the referenced encumbrance event must exist
- the referenced encumbrance event must be a control event with `action=encumber`
- the releasing party, if supplied, must resolve to a valid participant identifier
- domain policy may decide whether only the encumbrance beneficiary, current controller, warehouse operator, or another recognized role may discharge the encumbrance

### Redeem

Candidate validation rules:

- the object to be redeemed must resolve to an existing origin event
- a single active control chain for that object must be determinable
- the obligor, warehouse operator, or other action-specific participant must resolve to a valid participant identifier
- domain policy may decide whether redemption affects controller state, lifecycle state, delivery obligations, or only records presentation evidence

### Terminate

Candidate validation rules:

- the object to be terminated must resolve to an existing origin event
- the active control chain for that object must be determinable
- only the current controller of the active chain should be permitted to terminate the ETR
- if the latest control event is already a termination event, a further termination attempt should be blocked
- if more than one active chain for the object is currently controlled by the same signer, termination should be treated as ambiguous unless a more specific policy decides otherwise

### Attest

Candidate validation rules:

- the object or prior event being attested must resolve to an existing OpenETR graph
- if a prior event is supplied, it must be traversable back to an origin event
- the subject, if supplied, must resolve to a valid participant identifier
- the attestation type, if supplied, should be carried in a structured tag
- domain policy may decide which attestors are recognized and what effect their attestations have

## Working Publication Model for Control Events

OpenETR should distinguish between structural invalidity, incomplete acknowledgment, and full attestation validity.

This suggests the following working model for control events:

- a `transfer initiate` event may reference a prior `kind 31416` transfer event even if no corresponding accept event has yet been observed
- the absence of a corresponding accept event should be surfaced as a warning rather than a hard block
- a `transfer accept` event should reference a `kind 31416` initiate event and should be signed by the transferee identified in that initiate event
- an `encumber`, `discharge`, `redeem`, `terminate`, or `attest` event should reference the object graph or a specific prior event according to the action's expected shape
- action-specific participants should be resolved to canonical public-key hex before event construction
- attestors may later require the full initiate-and-accept sequence before recognizing a subsequent transfer as fully valid

Under this model:

- publication remains open
- structural invalidity is still blocked
- incomplete acknowledgment, ambiguity, or policy tension is visible to operators
- attestors retain the ability to require stricter completion rules for recognition

OpenETR therefore permits unilateral transfer initiation.

Whether that initiation is sufficient for recognized transfer of control is a matter for attestation or assessment policy, which may require a corresponding accept event.

This may be useful where an ETR needs to operate in real time, where participants cannot wait for attestors to catch up, or where the parties do not require the added formality of attestation for a particular control step.

OpenETR therefore provides evidence of control-relevant actions.

It does not by itself determine their final legal or operational effect.

Recognition remains a matter for the party applying the relevant assessment or attestation policy.

This also means that more than one candidate control chain may appear for the same object.

OpenETR does not necessarily prevent conflicting or competing control histories from being published.

Instead, it makes those histories visible as signed evidence so that the relevant assessor, attestor, or relying party can decide which chain, if any, should be recognized under the applicable policy.

This preserves a useful distinction between:

- publication rules, which determine whether an event is well-formed enough to be issued
- warning rules, which surface incompleteness or ambiguity without preventing publication
- recognition rules, which determine whether the resulting control graph is sufficient for recognition

## Event-Level and Chain-Level Attestation

OpenETR does not require that every control event be separately attested in order for a later state to be recognized.

An attestor may instead attest a later event, including a termination event, after validating the prior control chain necessary to recognize that event.

This creates two useful attestation patterns:

- event-level attestation, where each origin, initiate, accept, encumber, discharge, redeem, terminate, attest, or linked evidence event is separately attested
- chain-level attestation, where a later event is attested after the relevant earlier events have been reviewed as a chain

Under a chain-level model, an attestation of the later event should be understood as incorporating a claim that the relevant prior chain was examined and found sufficient under the attestor's policy.

This may be especially useful where:

- real-time operations cannot wait for attestation at every step
- parties want a lighter operational flow
- the decisive recognition question arises only at a later state, such as transfer completion or termination

The important design point is that OpenETR leaves this choice to policy.

The protocol can carry the evidence either way.

What matters is that the attestor's claim is clear about whether it is:

- attesting a single event in isolation
- or recognizing a later event on the basis of a validated chain

## Object-Centric Control Evaluation

The current OpenETR component increasingly evaluates control history from the object outward rather than from an operator-supplied prior event alone.

In practice this means:

- determine the object identifier
- query related origin and control events using the object's `o` tag
- identify candidate control chains
- determine the current controller or terminal state from the latest event in a candidate chain
- apply local policy to decide whether a new action should be allowed, warned, or rejected

This approach is particularly useful for:

- current-controller checks
- object-based transfer initiation
- object-based acceptance of pending transfers
- object-based encumbrance, discharge, redemption, attestation, and termination
- detection of multiple candidate control chains for the same object

## Design Principle

OpenETR should not confuse publication with validity.

The more accurate principle is:

> Events may be published openly, but recognition and attestation depend on explicit validation rules.

Baseline component guards are one of the first places those rules become visible and testable.

## Operational Consequence

As the component evolves, control-event validation should be treated as more than user-interface polish.

It is part of the specification effort.

Each new rule should ideally answer three questions:

1. What condition is being checked?
2. Why does that condition matter for valid recognition of the action?
3. Should failure produce an error, a warning, or be treated as a recognition rule?

That keeps implementation and policy aligned.

## Summary

OpenETR validation and recognition rules are valuable even if they do not make invalid publication impossible.

Their real purpose is to:

- reduce operator error
- formalize transaction expectations
- make recognition and attestor policy concrete
- support accountable recognition of control-relevant events

This includes making it explicit that:

- an object may have more than one published origin or control chain
- the protocol may surface those chains rather than suppress them
- policy must decide what to recognize

OpenETR is designed to operate in an open, permissionless environment.

It does not prevent every action at the protocol layer.

Instead, it provides a sound cryptographic basis for recognition by making control-relevant actions signed, attributable, and reviewable.

In this sense, baseline validation is not merely defensive tooling.

It is an early executable form of OpenETR's attestation policy.
