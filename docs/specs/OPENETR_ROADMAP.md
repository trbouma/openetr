# OpenETR Roadmap

This document is the canonical project-level roadmap for the OpenETR protocol,
reference component, integration surfaces, and domain work.

## Status

Draft, 4 September 2026.

The roadmap identifies priorities rather than normative protocol requirements.
Detailed requirements remain in the applicable specifications and design
notes.

## Governing Direction

OpenETR is an open protocol for deriving consequential state from
end-verifiable evidence concerning exact Digital Artifacts, independently of
the applications, organizations, and legal regimes that use or recognize that
state.

The governing verification discipline is:

> Each proof proves only what it proves.

The project shall keep the state-transition core narrow while making evidence
scope, uncertainty, recognition, and external effect explicit.

## Phase 0: Documentation Alignment

Priority: immediate.

- keep the README, documentation site, draft standard, wire format, and
  implementation vocabulary aligned;
- use regular event kinds `1415` and `1416` for new graph events;
- reserve **Anchor Event** for the OpenETR graph primitive;
- use **Temporal Proof** for external timestamp or ledger evidence;
- maintain one project-level roadmap and link domain roadmaps to it; and
- distinguish current behavior, proposed behavior, and monitored external work.

Completion evidence:

- strict documentation build passes;
- specification index and documentation navigation expose this roadmap; and
- stale current-state references are removed from primary documentation.

## Phase 1: Generic Verifier Result Model

Priority: highest implementation priority.

Define and implement independent result dimensions for:

- artifact integrity;
- event authenticity and structural validity;
- graph continuity;
- transition validity;
- consequential state;
- retrieval coverage;
- evidence sufficiency;
- optional temporal proof;
- actor and authority recognition;
- system reliability evidence; and
- external recognition and effect.

Adopt a stable outcome vocabulary capable of expressing `valid`, `invalid`,
`unverifiable`, `absent`, `not_evaluated`, and `not_applicable`.

The CLI JSON model, service APIs, Python component, and web application should
use compatible result structures. Command success shall remain separate from
verification and recognition outcomes.

## Phase 2: Retrieval Coverage And Graph Evidence

Priority: high.

- preserve per-relay or per-repository retrieval observations;
- support NIP-67 `finish`, `more`, and `auth` hints where the relay client makes
  them available;
- support appropriate NIP-42 authentication flows without treating private
  relay access as a protocol requirement;
- paginate when additional matching events are reported;
- report unknown retrieval completeness instead of assuming completeness;
- distinguish source retrieval coverage from graph continuity and policy
  sufficiency; and
- test conflicting branches, unavailable parents, source disagreement, and
  authenticated evidence retrieval.

## Phase 3: Generic Associated Evidence

Priority: design before implementation.

Complete the design of a generic associated-evidence interface and determine
whether proposed kind `1417` should be adopted.

Candidate evidence purposes include:

- authorization;
- execution;
- temporal proof;
- identity, role, or accreditation;
- system reliability and audit; and
- domain-specific supporting evidence.

The model should preserve stable intent identity separately from individual
execution attempts. Associated evidence shall not silently become a control
transition or recognition decision.

## Phase 4: Recognition Adapters

Priority: incremental.

- define a representation-neutral interface for identity, role, authority, and
  recognition evidence;
- add SD-JWT VC as a candidate adapter;
- retain support for TRQP, Web of Trust, attestations, References, and host
  account or registry evidence;
- report credential cryptographic validity separately from issuer recognition
  for purpose; and
- allow organizational and jurisdictional rule books to combine recognition
  inputs without changing the base control grammar.

## Phase 5: Warehouse Receipt Pilots

Priority: primary domain focus.

- complete the Model Law on Warehouse Receipts mapping and operating rule book;
- keep the Control Desk workflow focused on warehouse issuance and control
  actions;
- evaluate change of medium, depositor request, surrender, redemption,
  termination, and encumbrance behavior;
- create a China electronic warehouse-receipt regulatory mapping;
- test whether singular consequential state can support a legal uniqueness
  analysis while identical artifact copies remain possible; and
- obtain jurisdiction-specific legal review before making compliance claims.

## Phase 6: Additional Domain And Legal Profiles

Priority: after the verifier result model stabilizes.

- maintain UCC Article 12 as an external legal profile and keep Digital
  Controllable Record distinct from statutory Controllable Electronic Record;
- continue bills of lading, Product Passport, apostille, and other domain
  mappings;
- document the evidence each profile requires and the conclusions it is
  permitted to draw; and
- avoid adding domain semantics to the generic control grammar unless they are
  demonstrably cross-domain.

## Monitored Work

The project should monitor, test against, and learn from external work without
prematurely making it a normative dependency.

Current monitored inputs include:

- the individual SCITT Bitcoin temporal-proof Internet-Draft;
- the individual Vaara Receipt Internet-Draft;
- optional draft NIP-67 and NIP-78 behavior;
- SD-JWT VC as it proceeds through the IETF standards process;
- national electronic-document regimes, including China Order No. 22;
- MLETR and MLWR implementation developments; and
- UCC Article 12 enactment and implementation.

External draft version numbers and status should be checked before publication
of any conformance claim.

## Deliberate Non-Goals

The roadmap does not call for OpenETR to:

- turn optional Temporal Proof into a condition of DCR validity;
- claim global evidence completeness from one relay result;
- make KYC or one credential format part of the base protocol;
- import an autonomous-agent authorization framework into control events;
- make system-reliability or legal-effect determinations without an identified
  policy and supporting evidence; or
- replace host-system authentication, authorization, document storage, or
  jurisdiction-specific compliance controls.

## Related Documents

- [OPENETR_DRAFT_NATIONAL_STANDARD.md](./OPENETR_DRAFT_NATIONAL_STANDARD.md)
- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OPENETR_CLI_JSON_MODEL.md](./OPENETR_CLI_JSON_MODEL.md)
- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md](./LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md)
- [OPENETR_CHINA_ELECTRONIC_WAREHOUSE_RECEIPTS_REVIEW_NOTE.md](./OPENETR_CHINA_ELECTRONIC_WAREHOUSE_RECEIPTS_REVIEW_NOTE.md)

