# OpenETR Dependency Integrity Design Note

This note describes how OpenETR can model dependency integrity across related controllable records.

It is motivated by a recurring digital trade problem:

> It is not enough to know that one electronic transferable record is authentic, singular, and controlled. A verifier may also need to know how changes to that record affect other records, obligations, rights, claims, and evidence in the same trade transaction.

## Status

Draft.

## Summary

OpenETR already models a single Controlled Object as a digest-identified artifact with a signed control graph.

Dependency integrity extends that model across objects.

Instead of asking only:

```text
What is the current recognized state of this object?
```

a dependency-aware verifier also asks:

```text
What other objects, claims, obligations, or evidence items depend on this object?
Does a change in this object create a warning, revalidation need, or recognition effect elsewhere?
```

This does not mean OpenETR becomes a full legal-state engine.

The design boundary remains:

```text
OpenETR records signed object and dependency evidence.
Domain adapters interpret dependency meaning.
Recognition policy decides effect.
```

## Core Problem

Trade records rarely stand alone.

Examples:

- a bill of lading may support a financing arrangement
- a warehouse receipt may serve as collateral
- an insurance policy may rely on inventory represented by a receipt
- a certificate of origin may support customs declarations or tariff treatment
- a delivery confirmation may trigger a payment obligation
- an inspection report may support release, acceptance, or compliance status
- an Apostille package may support downstream recognition by a court, university, agency, or counterparty

If one record changes, dependent records may need review.

OpenETR should not decide every legal consequence of that change. But it can make dependencies explicit enough that verifiers, attestors, and domain applications do not have to rely on memory, manual reconciliation, or platform-specific hidden state.

## Definitions

### Primary Object

The **Primary Object** is the Controlled Object currently being evaluated.

Example:

```text
warehouse receipt digest
```

### Dependent Object

A **Dependent Object** is another digest-identified object whose recognition, value, state, workflow, or verifier treatment may depend on the Primary Object.

Examples:

- financing agreement
- pledge record
- insurance certificate
- customs declaration
- certificate of origin
- delivery instruction
- payment obligation

### Dependency Edge

A **Dependency Edge** is a signed event or linked evidence record that asserts a relationship between two objects.

Examples:

- `finances`
- `secures`
- `relies_on`
- `supports`
- `blocks_release_until`
- `requires_discharge_of`
- `supersedes`
- `satisfies`
- `invalidates_if_revoked`
- `triggers_review_of`

### Dependency Graph

The **Dependency Graph** is the linked set of dependency edges among Controlled Objects, evidence artifacts, and recognized external references.

It is not a replacement for each object's own control graph.

It is an overlay:

```text
object control graph
  + linked evidence graph
  + cross-object dependency edges
  -> dependency graph evaluated by policy
```

### Dependency Integrity

**Dependency Integrity** is the ability to determine whether a change in one recognized object or event affects the recognition, workflow, or risk status of another object.

It does not mean OpenETR automatically computes all legal consequences.

It means OpenETR can preserve enough signed relationship evidence for policy-aware systems to detect and explain the dependency.

## Relationship To Existing OpenETR Concepts

Dependency integrity builds on existing OpenETR primitives.

| Existing Concept | Dependency Integrity Use |
| --- | --- |
| Controlled Object | Each related record remains separately digest-identified. |
| Control Graph | Each object retains its own origin and control history. |
| Linked Evidence Record | Supporting artifacts can be associated with one or more objects. |
| Attestation | A signer can assert a relationship, dependency, warning, or status. |
| Encumbrance | A dependent financing or security relationship can affect recognition of transfer, redemption, or termination. |
| Verifier Policy | Policy decides whether a dependency creates warning, block, revalidation, or no effect. |
| Domain Adapter | Domain-specific language explains what a dependency means. |

Dependency integrity should not collapse these concepts into one global state machine.

OpenETR should preserve separable object graphs and add explicit edges between them.

## Candidate Dependency Event Model

There are two plausible implementation patterns.

### Pattern 1: Linked Evidence Dependency Records

Use the proposed linked evidence event kind to express cross-object relationships.

Example shape:

```json
{
  "kind": 1417,
  "tags": [
    ["o", "<primary_object_digest>"],
    ["linked_digest", "<dependent_object_digest>"],
    ["evidence_type", "dependency"],
    ["dependency_type", "secures"],
    ["dependency_direction", "primary_to_dependent"],
    ["domain", "trade_finance"],
    ["policy", "<policy_id>"]
  ],
  "content": ""
}
```

This works well when the dependency is evidence about a relationship but does not itself change control state.

### Pattern 2: Attestation Dependency Records

Use an attestation-style control event to assert a dependency.

Example shape:

```json
{
  "kind": 1416,
  "tags": [
    ["o", "<primary_object_digest>"],
    ["action", "attest"],
    ["attestation_type", "dependency"],
    ["dependent_object", "<dependent_object_digest>"],
    ["dependency_type", "blocks_release_until"],
    ["policy", "<policy_id>"]
  ],
  "content": "Financing pledge must be discharged before release recognition."
}
```

This may be appropriate where the dependency assertion itself is a control-relevant attestation by a recognized party.

### Current Recommendation

Treat dependency edges as linked evidence by default, and use `ATTEST` only where the assertion is meant to carry authority or recognition weight.

The distinction is:

```text
linked evidence:
there is a relationship worth inspecting

attestation:
a signer asserts a relationship that may affect recognition
```

## Suggested Tags

Potential dependency tags:

- `["dependency_type", "<type>"]`
- `["dependent_object", "<digest>"]`
- `["dependency_direction", "primary_to_dependent" | "dependent_to_primary" | "bidirectional"]`
- `["dependency_policy", "<policy_id>"]`
- `["dependency_effect", "warning" | "revalidate" | "block" | "notify" | "informational"]`
- `["trigger_action", "transfer" | "encumber" | "discharge" | "redeem" | "terminate" | "revoke" | "replace" | "cancel"]`
- `["required_state", "<state_or_condition>"]`
- `["related_event", "<event_id>"]`
- `["relationship_reference", "<external_reference>"]`
- `["valid_from", "<iso8601_or_unix_time>"]`
- `["valid_until", "<iso8601_or_unix_time>"]`

Potential dependency types:

- `relies_on`
- `supports`
- `secures`
- `pledges`
- `insures`
- `references`
- `supersedes`
- `replaces`
- `satisfies`
- `blocks_transfer_until`
- `blocks_release_until`
- `requires_discharge_of`
- `requires_revalidation_if_changed`
- `invalidates_if_revoked`
- `triggers_notice_to`

These should remain profile-controlled vocabularies. The base protocol should not try to define every trade relationship.

## Example: Warehouse Receipt, Financing, And Insurance

A warehouse receipt represents stored goods.

The receipt is also used as:

- collateral for a secured loan
- evidence for an insurance policy

The dependency graph may look like:

```text
warehouse receipt object
  -> secures financing agreement object
  -> supports insurance certificate object
```

If the receipt is redeemed and terminated, a verifier may need to warn that:

- the financing agreement may require discharge or update
- the insurance evidence may no longer support the same risk assumption
- a surrender or release action may be non-recognized while a pledge remains active

OpenETR should not decide the legal result automatically.

It should preserve the dependency edges and let a selected policy say:

```text
receipt termination while recognized pledge remains outstanding:
recognition_effect = policy_warning | block | manual_review
```

## Example: Bill Of Lading And Trade Finance

An electronic bill of lading may support:

- a letter of credit
- a payment undertaking
- a financing pledge
- an insurance policy
- customs or port release workflow

A transfer of control to a financier may affect the commercial state of related records.

The eBL domain adapter can show:

- the bill-of-lading control graph
- the financing dependency edge
- the current recognized controller
- whether an encumbrance blocks later surrender or delivery recognition
- which policy produced the warning or block

The domain adapter should speak in maritime and finance terms. OpenETR should provide the digest-linked evidence graph.

## Example: Certificate Of Origin And Customs Declaration

A certificate of origin may support:

- preferential tariff treatment
- customs declaration data
- documentary credit presentation
- buyer compliance evidence

If the certificate is revoked, corrected, or superseded, dependent records may need revalidation.

A dependency edge may state:

```text
customs declaration relies_on certificate of origin
dependency_effect = revalidate
trigger_action = revoke | replace | correct
```

The verifier can then flag that the customs declaration should not be evaluated as if the certificate were unchanged.

## Verification Behavior

A dependency-aware verifier should proceed in stages.

1. Verify the Primary Object graph.
2. Retrieve linked evidence and dependency records for the Primary Object.
3. Identify dependent objects referenced by digest or external id.
4. Retrieve dependent object graphs where available.
5. Evaluate dependency edges under the selected policy.
6. Annotate warnings, revalidation needs, blocks, or informational links.
7. Present technical evidence separately from recognition effect.

The verifier should make the difference clear:

```text
The dependency exists as signed evidence.
The policy outcome is this verifier's recognition decision.
```

## Policy Outcomes

Dependency policy may produce several outcomes.

| Outcome | Meaning |
| --- | --- |
| `informational` | Relationship is displayed but does not affect recognition. |
| `notify` | A related party or workflow should be notified. |
| `revalidate` | A dependent object should be checked again before reliance. |
| `warning` | Recognition may proceed with visible risk annotation. |
| `manual_review` | A human or authority must evaluate the dependency. |
| `block` | The selected policy refuses recognition while the dependency condition remains unresolved. |

These outcomes are recognition-policy effects, not base event validity.

## Domain Adapter Responsibilities

A domain adapter using dependency integrity should define:

- dependency types it recognizes
- dependency tags it requires
- which actions trigger dependency checks
- what policy outcomes are possible
- which actors may assert dependency edges
- which actors may discharge or resolve dependency conditions
- whether dependencies are displayed as warnings, blockers, notices, or audit facts
- how external references are resolved
- how privacy-sensitive relationships are protected

Examples:

- an MLWR adapter may require pledge discharge before delivery recognition
- an eBL adapter may warn on surrender while financing dependency is active
- a Product Passport adapter may revalidate compliance status when a component certificate is revoked
- an Apostille adapter may require manual review when an e-Register verification result changes

## Recognition Boundary

Dependency integrity must not become a hidden legal engine.

OpenETR can show:

- signed dependency assertions
- related object digests
- referenced events
- dependency types
- policy identifiers
- verifier warnings and outcomes

OpenETR does not decide:

- whether a financing agreement is enforceable
- whether title passed
- whether insurance coverage changed
- whether customs treatment is legally invalid
- whether a court or authority must accept the dependency result
- whether every affected system has been notified

Those effects belong to contracts, law, registries, institutions, courts, authorities, and verifier policy.

## Privacy And Commercial Sensitivity

Dependency graphs may reveal sensitive commercial relationships.

Examples:

- financing arrangements
- pledges
- insurance coverage
- buyer or supplier relationships
- customs strategies
- bank counterparties
- shipment chains

OpenETR implementations should avoid publishing unnecessary commercial dependency details to public relays.

Possible mitigations:

- publish dependency digests without full document contents
- use private or permissioned relays
- encrypt or access-control referenced artifacts
- use policy identifiers rather than full contract terms
- publish coarse dependency types where sufficient
- use verifier-held evidence for sensitive relationship details
- separate public integrity evidence from private recognition evidence

Dependency integrity should improve auditability without making sensitive trade graphs casually public.

## Relationship To Singularity

Singularity asks:

```text
Which control state is authoritative for this transferable record?
```

Dependency integrity asks:

```text
What else depends on that authoritative state?
```

The two concepts are complementary.

Singularity is object-centric. Dependency integrity is graph-of-objects-centric.

OpenETR should support both without collapsing them:

```text
single-object control graph
  -> candidate current controller
  -> recognition policy

cross-object dependency graph
  -> dependency warnings or effects
  -> recognition policy
```

## Non-Goals

This design does not require OpenETR to:

- model every commercial relationship in trade
- compute complete legal state
- enforce all downstream effects automatically
- replace ERP, banking, customs, insurance, or logistics systems
- expose private trade dependencies publicly
- define one universal dependency vocabulary for all domains
- guarantee notification to all affected systems
- decide legal consequences of dependency changes

## Recommended Roadmap

1. Treat dependency integrity as a verifier-policy and domain-adapter feature first.
2. Model dependency edges using linked evidence records where possible.
3. Use attestation events for dependency assertions made by recognized authorities or counterparties.
4. Define small domain-specific dependency vocabularies for MLWR, eBL, Product Passports, and Apostille workflows.
5. Add verifier warnings for unresolved dependencies, active encumbrances, stale linked evidence, superseded objects, and revoked supporting records.
6. Add privacy guidance before encouraging broad publication of dependency graphs.
7. Revisit whether a dedicated dependency event kind is needed after linked evidence usage is better understood.

## Open Questions

- Should dependency edges use `1417` linked evidence, `1416 action=attest`, or a future dedicated event kind?
- Should dependency edges be queryable by both primary object and dependent object?
- Should there be a standard `dependency_type` vocabulary or only domain-profile vocabularies?
- How should dependency edges be revoked, expired, corrected, or superseded?
- How should encrypted or permissioned dependency evidence be represented?
- How should verifiers prevent dependency graphs from creating false certainty about legal effect?
- Should some dependency checks become baseline verifier warnings in the generic policy?

## References

- [LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md](./LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md)
- [OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md](./OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [CONTROL_EVENT_POLICY_GUARDS_DESIGN_NOTE.md](./CONTROL_EVENT_POLICY_GUARDS_DESIGN_NOTE.md)
- Verifiable.Trade, "Can Digital Trade Achieve True Singularity without creating new third party dependencies?"

