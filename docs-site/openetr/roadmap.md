# OpenETR Roadmap

OpenETR's next phase keeps the state-transition protocol small while making
verification scope and uncertainty more explicit.

> Each proof proves only what it proves.

## Immediate Priorities

1. Align the primary documentation with regular event kinds `1415` and `1416`
   and the current Consequential State model.
2. Define machine-readable verifier dimensions for integrity, authenticity,
   graph continuity, transition validity, consequential state, retrieval
   coverage, evidence sufficiency, recognition, and external effect.
3. Preserve per-relay retrieval observations and report unknown completeness
   instead of assuming that no additional evidence exists.

## Next Design Work

- define generic associated evidence for authorization, execution, Temporal
  Proof, identity, and system reliability;
- keep stable intent identity separate from individual execution attempts;
- add representation-neutral recognition adapters, including SD-JWT VC;
- keep credential validity separate from issuer authority; and
- continue the warehouse-receipt pilot, including change of medium and the
  China electronic-document mapping.

## Monitored Work

OpenETR is monitoring SCITT temporal proofs, Vaara receipts, NIP-67, NIP-78,
SD-JWT VC, MLETR and MLWR implementation, national electronic-document regimes,
and UCC Article 12. Draft external schemas are design inputs, not automatic
OpenETR dependencies.

## Boundaries

The roadmap does not make Temporal Proof mandatory, infer global completeness
from one relay, put KYC into the base protocol, or treat protocol validity as
system reliability or legal effect.

Read the complete [project roadmap](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_ROADMAP.md).

