# OpenETR Generic Verifier Policy

This note documents the generic verifier policy used by the current OpenETR component and the direction for future verifier-policy work.

The core rule is:

> A verifier policy enumerates the control graph according to its rules. A policy violation should normally produce a warning or non-recognition annotation, not make the signed event disappear.

OpenETR is an open signed-event system. Parties may publish events that are structurally valid but policy-questionable. The generic verifier should therefore distinguish between:

- events that cannot be verified or traversed at all
- events that can be verified as signed evidence but break a policy rule
- events that are recognized as effective under the verifier's selected policy

## Baseline Policy

The generic verifier policy is the baseline policy for all OpenETR evaluations.

Every OpenETR domain should start from the same generic sequence:

1. retrieve the object graph
2. verify cryptographic and structural correctness
3. enumerate candidate chains
4. annotate policy issues
5. derive candidate or recognized state according to the selected policy
6. present the evidence and policy outcome separately

Domain policies are overlays on this baseline.

A domain policy may add:

- additional safeguards
- stricter recognition requirements
- domain-specific actor rules
- required structured tags or schemas
- additional attestation requirements
- explicit exemptions from a generic warning condition
- alternative treatment of a warning within that domain

A domain policy should not replace the baseline enumeration behavior. Even where a domain policy refuses recognition, the verifier should still show the signed evidence and explain the policy reason.

## Current Component Behavior

The current `openetr` query service is intentionally object-wide.

For a document digest / object id, it:

1. queries origin events using `kind = 31415` and `#o`
2. queries control events using `kind = 31416` and `#o`
3. groups candidate control events by `e` references
4. builds summary control chains
5. derives a candidate lifecycle state
6. derives a candidate current controller
7. summarizes encumbrances, discharges, and outstanding encumbrances
8. includes profile metadata where available
9. reports warning conditions such as multiple origin events for the same object

This behavior is deliberately exploratory and evidentiary. It does not ask the relay or the first application that displays the record to decide final effect.

Instead, the component gives the verifier a structured view of the available signed evidence.

## Hard Verification Errors

Some failures prevent a verifier from treating an event as usable OpenETR evidence.

Examples include:

- malformed object identifiers supplied to the query command
- malformed public keys supplied as filter inputs
- invalid event signatures
- invalid event ids
- missing required event shape tags
- events whose required object identity cannot be determined
- control events that cannot be associated with the queried object

These are structural or cryptographic problems. A verifier may reject those events from the candidate graph because they do not satisfy the minimum requirements for OpenETR event evidence.

In implementation terms, these failures may raise errors, cause the event to be excluded, or mark the event as structurally invalid.

## Policy Warnings

Other conditions may break a policy rule but still leave the event as signed evidence.

These should generally be represented as warnings or policy annotations.

Examples include:

- more than one origin event exists for the same object digest
- a control event is signed by someone other than the expected current controller
- a transfer initiation has no corresponding acceptance event
- a transfer acceptance appears without a recognized initiation
- an encumbrance exists before or during a transfer
- a discharge references an encumbrance that the verifier does not recognize
- a termination appears while an encumbrance remains outstanding
- multiple candidate chains compete for recognition
- a participant profile is missing or does not satisfy the verifier's actor policy
- an event is structurally valid but lacks an attestation required by the selected policy

These conditions are not the same as invalid signatures or malformed events.

The event happened in the cryptographic sense: a key signed a statement, relays carried it, and the event can be retrieved. The question is whether a verifier's policy treats that statement as effective.

For that reason, the generic policy should not erase the event or treat the whole graph as failed. It should enumerate the graph and mark the relevant issue.

## Warning Semantics

A warning means:

> This event or transition is visible in the signed control graph, but the selected verifier policy has not accepted it as cleanly effective.

A warning should include, where practical:

- the rule that was triggered
- the event or transition that triggered it
- whether the issue affects controller state, lifecycle state, encumbrance state, or only display confidence
- whether the policy ignored the event, accepted it with warning, or left multiple candidate states unresolved

Warnings should be machine-readable as well as human-readable where the component exposes structured output.

Recommended fields for future structured verifier output include:

| Field | Meaning |
| --- | --- |
| `code` | Stable warning code such as `multiple_origin_events` or `unexpected_controller` |
| `severity` | Suggested severity such as `info`, `warning`, or `policy_blocked` |
| `event_id` | Event that triggered the warning, if applicable |
| `prior_event_id` | Prior event involved in the transition, if applicable |
| `action` | Control action involved, if applicable |
| `message` | Human-readable explanation |
| `recognition_effect` | How the selected policy treated the event or transition |

## Enumeration Before Recognition

The verifier should first enumerate the available graph before applying recognition effects.

The sequence is:

1. retrieve candidate origin and control events for the object
2. verify structural and cryptographic requirements
3. group events by `o` and `e` references
4. construct candidate chains
5. apply the selected verifier policy to those chains
6. annotate policy breaks as warnings
7. derive recognized or candidate state from the policy result
8. present both the evidence and the policy outcome

This lets the verifier answer two separate questions:

> What signed evidence exists?

and:

> What does this verifier's policy recognize as effective?

Both answers matter.

## Current Generic Policy

The current generic policy is intentionally minimal.

It treats the graph as object-centric evidence and derives practical state for demonstration and integration purposes:

- the first origin event is used as the initial origin basis
- multiple origin events are reported as a warning condition
- control events are grouped and summarized through `e` references
- controller state is derived from controller-changing actions
- lifecycle state is derived from lifecycle-changing actions
- encumbrance state is derived by matching `encumber` and `discharge` events
- profile metadata is displayed where available but missing profile metadata does not erase the signed event

This is not a final legal recognition profile.

It is a generic component policy for making the signed graph legible.

Domain adapters and recognition profiles may apply stricter rules.

## Domain-Specific Policy Profiles

A domain-specific policy profile applies on top of the generic verifier policy.

It may decide that a warning has stronger consequences within that domain.

For example, an MLWR warehouse receipt profile may decide:

- only a recognized warehouse operator may issue a receipt
- protected-holder status requires additional conditions
- transfer while an encumbrance is outstanding is not recognized
- delivery completion requires a warehouse-operator termination event
- particular structured tags or receipt fields are mandatory

It may also decide that a generic warning should be exempted or softened in a particular domain context.

For example:

- a closed trusted-counterparty profile may recognize transfer initiation without a separate acceptance event
- a warehouse receipt profile may allow a transfer while an encumbrance is outstanding but mark the encumbrance prominently
- a registry-backed profile may treat a registry attestation as curing a missing profile metadata warning
- a bearer-style redemption profile may recognize presentation by a valid presenter rather than ordinary controller transfer history

Those rules should still be reported as policy outcomes over the graph.

The underlying signed events remain evidence. The policy decides whether they are recognized.

## Implementation Guidance

OpenETR implementations should prefer this behavior:

- raise errors for malformed inputs or structurally unusable events
- warn for policy-rule breaks in otherwise signed and retrievable events
- keep policy warnings visible in CLI and web outputs
- expose policy warnings in structured API responses where possible
- avoid collapsing warning-free display into legal effect
- avoid treating every policy breach as a publication failure

This supports the OpenETR principle:

> Publish signed evidence openly. Verify structure cryptographically. Recognize effect under policy.

## Relationship To Other Notes

This note complements:

- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [TRANSFER_VALIDATION_GUARDS_DESIGN_NOTE.md](./TRANSFER_VALIDATION_GUARDS_DESIGN_NOTE.md)
- [CONTROL_EVENT_MINIMUM_SHAPES.md](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [OPENETR_LAYERED_ARCHITECTURE_NOTE.md](./OPENETR_LAYERED_ARCHITECTURE_NOTE.md)

The wire-format spec defines the event grammar. The validation-guards note explains hard and soft guards. This note defines how a generic verifier should enumerate and annotate the control graph under policy.
