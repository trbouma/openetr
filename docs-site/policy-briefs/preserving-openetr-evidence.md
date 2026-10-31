# Preserving OpenETR Evidence While Allowing State to Change

*Policy brief | 31 October 2026*

## Policy proposition

An actor who publishes a consequential assertion should not be able to erase the shared evidentiary history simply by asking its storage provider to delete it. Corrections, withdrawals, and reversals should be expressed through additional attributable evidence and evaluated under explicit rules.

OpenETR should support this principle through a specialized, opt-in evidence-relay policy, portable evidence packages, and verification that reports gaps and conflicts. It should not require every Nostr relay to retain every regular event indefinitely.

This is a proposal for deployment and interoperability work, not a new legal retention obligation or an amendment to the current OpenETR ruleset.

## Three separate questions

A digital signature can establish that an assertion was signed by a particular key. It does not establish that the assertion is correct, that its author had authority, or that it remains effective.

Historical availability asks whether the evidence can still be obtained. Consequential validity asks what follows from it under the applicable rules. These questions need separate answers: an authentic assertion can remain available even after a correction, withdrawal, or permitted reversal changes its effect.

OpenETR's [Core Record Ruleset](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CORE_RECORD_RULESET_1_0.md) already makes this distinction for non-transferable records. An anchor remains historical evidence when its publisher issues a subsequent notice. A withdrawal changes the publisher's stated position; it does not erase the fact of publication. Broader transfer and control arrangements require their own rules.

## Why storage behavior matters

Consider a publisher that anchors a product document and later warns users not to rely on it. If the warning disappears from a relay, a reader may see the original anchor alone. The reader must not mistake that incomplete view for proof that no warning exists.

An evidence relay that retains both events makes reconstruction more reliable. The verifier still needs to explain which evidence it evaluated and what may be missing. No single relay, replication arrangement, or internally consistent evidence package guarantees that every relevant event has been discovered.

Replacement presents a related risk. A mutable address may expose only the latest version of a record. That is useful for contact details or discovery indexes, but insufficient as the only record of a consequential history. Historical assertions need exact signed references and independently retrievable evidence.

## A bounded retention policy

The proposed relay policy would retain admitted regular events despite ordinary author deletion requests, while preserving replacement and deletion behavior for mutable event classes. Ephemeral events would remain outside retained history. Corrections and retractions would be additional signed assertions rather than destructive edits.

Operators would publish admission rules, retention periods, removal exceptions, and export arrangements. They would retain administrative removal powers for legal, privacy, security, and operational reasons. Such removal affects availability; it does not by itself reverse an OpenETR consequence.

This separation also limits operator authority. Hosting evidence does not authorize the operator to determine ownership, standing, or the effect of a transaction. Those conclusions depend on the identified rules and recognition policies.

## Privacy and accountability

A blanket rule for all regular Nostr events would also capture private communications and other sensitive material. A dedicated evidence service is a more appropriate starting point than a universal prohibition on deletion.

Applications should minimize public personal data, separate artifacts from their public evidence where appropriate, and make retention expectations clear before publication. Hashing is not a general privacy guarantee: predictable underlying data can sometimes be identified from its digest. Encryption likewise does not guarantee eventual erasure of all copies or indefinite confidentiality.

Local hiding, access restrictions, and administrative removal can serve legitimate purposes. They must not be presented as proof that all copies have disappeared. Participants also need practical export and recovery arrangements rather than an unsupported promise of permanence.

## Protocol and cryptographic implications

The proposed behavior is not the current general deletion rule in [NIP-09](https://github.com/nostr-protocol/nips/blob/master/09.md). A future amendment would need to define its scope, target classification, compatibility with mutable records, policy discovery, and the distinction between acknowledging a deletion request and carrying it out. Specialized deployments can evaluate the policy first, with their differences disclosed.

Post-quantum signatures are a separate avenue for protecting long-lived evidence. The proposed Stroma and Spurline integration could support experiments with ML-DSA-44 anchors, but a new signature format requires an explicit OpenETR interoperability profile. It does not automatically establish authority or make evidence permanently available. Storage resilience and cryptographic resilience should be tested independently.

## Recommended next steps

1. Pilot the disclosed evidence-retention policy on a controlled relay, including deletion-before-arrival and mixed-target tests.
2. Test OpenETR reconstruction with missing, restored, conflicting, and administratively removed evidence.
3. Define portable evidence and observation records that preserve the inputs to an evaluation without claiming global completeness.
4. Consult relay and client implementers before proposing NIP-09 changes; preserve privacy-sensitive use cases.
5. Evaluate post-quantum anchor profiles separately from retention and current normative rules.

The objective is durable, independently verifiable evidence with rule-governed changes in effect—not an unchangeable view of the world. Evidence may be contradicted or superseded while remaining available for accountability.

## Supporting design

The [OpenETR Evidence Retention and Deletion design note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_EVIDENCE_RETENTION_AND_DELETION_DESIGN_NOTE.md) sets out verifier behavior, policy boundaries, possible NIP-09 changes, and proposed tests. Companion Spurline proposals cover [append-only evidence retention](https://github.com/trbouma/spurline/blob/main/docs/append-only-evidence-policy.md) and [post-quantum anchor events](https://github.com/trbouma/spurline/blob/main/docs/post-quantum-anchor-events.md).
