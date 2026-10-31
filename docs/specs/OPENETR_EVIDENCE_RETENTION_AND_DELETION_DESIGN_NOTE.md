# OpenETR Evidence Retention and Deletion

*Design note | 31 October 2026 | Proposed guidance, non-normative*

## Purpose and scope

OpenETR needs historical evidence to remain independently verifiable even when its consequential effect changes. A dedicated evidence relay can support that objective by declining author deletion requests for regular events. It cannot guarantee permanent availability, complete discovery, or the validity of the assertions it retains.

This note proposes deployment guidance and tests. It does not amend NIP-09, change the OpenETR wire format, or introduce new Core Record Ruleset result codes. Post-quantum signatures remain a separate, experimental profile question.

## Existing OpenETR foundation

The [Core Record Ruleset 1.0](./OPENETR_CORE_RECORD_RULESET_1_0.md) already separates an Anchor Event from the Anchor Publisher's subsequent position. Section 9 preserves the anchor when notices are published; Section 10 preserves competing notice branches and reports missing predecessors; Sections 13 and 14 require retrieval limitations and distinct findings to be reported.

Kinds 1415 and 1416 are regular events in the [Nostr wire format](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md). Their event identifiers reference particular signed assertions, rather than a mutable address whose latest value stands in for history.

The core ruleset concerns non-transferable records. Transfer, relinquishment, discharge, and control reversal require their own applicable rulesets; they are not additional meanings conferred on core Publisher Notices by this proposal.

## Deletion, replacement, and consequential change

| Operation | What changes | What it does not establish |
| --- | --- | --- |
| Relay deletion or suppression | Evidence returned by that relay | That the assertion never existed or has no effect |
| Replacement at a logical address | The version exposed as current at that address | Preservation of earlier versions |
| OpenETR notice or permitted successor | The conclusion derived under an identified ruleset | Erasure of the preceding signed assertion |
| Administrative removal | Availability under operator policy | An authorized OpenETR reversal |

NIP-09 deletion requests are signed requests for removal or suppression, not cryptographic revocation of the referenced signature. A retained deletion request may be relevant evidence of an author's wishes, but is not automatically a qualifying Publisher Notice. A verifier must not translate it into `withdrawn`, `superseded`, or a control transition without an applicable rule explicitly defining that effect.

Mutable indexes and summaries may aid discovery. They should not be the sole evidence supporting a historical conclusion.

## Proposed dedicated evidence relay policy

An opt-in deployment would publish its admission rules, retention period, removal exceptions, and export arrangements before accepting evidence under this policy.

| Event class | Proposed treatment |
| --- | --- |
| Regular | Retain admitted events without honoring ordinary author deletion requests |
| Replaceable | Preserve ordinary replacement and deletion semantics |
| Addressable | Preserve ordinary replacement and deletion semantics |
| Ephemeral | Do not retain; deletion is unnecessary |
| Undefined or unsupported | Apply an explicit admission policy; do not infer durable treatment |

This boundary applies regardless of signature algorithm. It does not require accepting every event, retaining evidence forever, or disabling administrative removal for privacy, legal, security, or operational reasons. Sensitive messages should not be routed to an evidence relay merely because they are regular events.

Deletion processing needs per-target classification. A request's kind hints are not authoritative evidence of the target's class. Mixed requests can affect mutable targets while leaving regular evidence available. Requests received before their targets must not establish blanket tombstones that later suppress protected regular events. Retaining a deletion request and acknowledging its publication must not imply that every referenced event was removed.

Changing deployment policy requires an explicit migration plan for existing tombstones, retained evidence, and client expectations. An append-only setting cannot recover evidence already lost.

The [Spurline append-only design note](https://github.com/trbouma/spurline/blob/main/docs/append-only-evidence-policy.md) describes the companion relay proposal. This is not a claim that the policy is already deployed.

## Verifier behavior and evidence packages

A verifier evaluates the supplied and retrieved evidence under the declared ruleset. It should retain the original signed events, exact references, ruleset version, and source observations needed to reproduce that evaluation. Observation timestamps are not automatically trusted timestamps for the underlying assertions.

For the core ruleset, existing behavior remains applicable:

- A qualifying anchor remains an anchor when a qualifying withdrawal or correction notice is found.
- No qualifying notice yields `no_notice_found`, not approval or a completeness guarantee.
- Competing terminal notices yield `conflicting_notices`; the latest timestamp does not choose the winner.
- An unresolved predecessor produces `notice_parent_missing`; retrieval limitations can produce `retrieval_incomplete`.
- Evidence missing from one relay may be supplied from another source and independently validated. Its absence alone cannot prove nonexistence.

Portable evidence packages should include the relevant signed graph, artifact or digest binding, evaluation parameters, and known gaps. A package can be internally consistent yet omit an undiscovered competing branch. Replication and agreement among several relays improve availability but do not prove global completeness or consensus.

For broader control rulesets, reversals need explicit authorized successor or compensating evidence. Deleting a transfer must never silently restore the preceding controller. The precise transition rules belong in those rulesets, not in the storage policy.

## Walkthrough

A publisher anchors a product document with event A. It later publishes notice B, referencing A, stating `do_not_use`. Under the core ruleset, A remains historically anchored and B determines the publisher position if it is the unique qualifying terminal notice.

The publisher then asks a relay to delete A and B. The proposed evidence relay retains both. A different relay may stop returning them. A verifier supplied with A and B still evaluates their signatures and relationships normally; a verifier retrieving only A reports its limited evidence scope rather than claiming that no caution exists anywhere.

If a subsequent notice C references B but B is unavailable, the verifier reports the missing predecessor. It does not attach C directly to A. If two qualifying branches remain, it reports the conflict rather than resolving it by timestamp or relay popularity.

## Possible NIP-09 changes

Current [NIP-09](https://github.com/nostr-protocol/nips/blob/master/09.md) does not generally exempt regular events from author deletion requests. A specialized policy must be disclosed as such, rather than presented as the existing universal rule. [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md) supplies the event classifications, but does not itself guarantee historical retention.

A future amendment would need to specify:

1. Whether restricted deletion is universal or an advertised optional relay policy. The initial recommendation is the latter.
2. Eligibility of exact `e` targets and preservation of address-target `a` cutoff behavior for mutable records.
3. Treatment of mixed targets, missing targets, untrusted kind hints, and requests arriving before targets.
4. How acknowledgments distinguish storing a request from acting on it, without implying a new response format already exists.
5. How clients discover the policy, retain local hiding controls, and explain that remote copies may persist.
6. Administrative removal boundaries, policy migration, and the continued distinction between removing evidence and undoing an application consequence.

Any new discovery field or response extension requires a separately specified interoperable format. OpenETR verification should not depend on adoption of this amendment.

## Post-quantum anchors

The [Spurline post-quantum proposal](https://github.com/trbouma/spurline/blob/main/docs/post-quantum-anchor-events.md) explores ML-DSA-44 through Stroma for anchor-style evidence. Retention and cryptographic longevity are complementary: a strong signature cannot recover a missing event, and retention cannot repair a compromised signature scheme.

OpenETR should define an explicit experimental profile before accepting such events: algorithm identification, canonical signing input, event identifier construction, supported kinds, key binding and rotation, verifier capability reporting, and downgrade behavior. Existing Nostr signature validation must not be silently widened. An unsupported algorithm must not be reported as verified.

ML-KEM concerns key establishment, not event signatures. Neither PQ signatures nor a link to an existing classical identity establish authority, trusted time, or legal recognition by themselves. Migration of long-lived evidence needs its own policy for prior keys, compromise, and independently supported time claims.

## Proposed validation work

| Scenario | Required observation for the proposed policy |
| --- | --- |
| Delete regular anchor or notice, before or after arrival | Evidence remains available under retention policy |
| Delete mutable records and replace versions | Mutable semantics remain intact |
| Mixed deletion targets | Each target gets its appropriate treatment |
| Anchor followed by withdrawal | Anchor authenticity remains distinct from publisher position |
| Missing predecessor or competing notices | Existing gap or conflict findings are preserved |
| Operator removes an event | Availability changes without inventing a state reversal |
| Restore evidence from a portable package | Same evidence and evaluation inputs give the same result |
| Unknown PQ profile | No false signature-verification success or silent downgrade |

Implementation should begin with relay-policy and verifier fixtures, followed by documented deployment tests. Any subsequent normative change should be reviewed and versioned separately.

## Covering policy brief

See [Preserving OpenETR Evidence While Allowing State to Change](../../docs-site/policy-briefs/preserving-openetr-evidence.md).
