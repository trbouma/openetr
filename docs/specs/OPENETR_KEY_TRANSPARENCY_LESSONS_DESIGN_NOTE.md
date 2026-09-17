# Key Transparency Lessons For OpenETR Design Note

## Status

Draft research and architecture note, 7 September 2026.

## Purpose

This note considers architectural lessons from the IETF Key Transparency
work and Signal's Automatic Key Verification deployment. It identifies useful
distinctions for OpenETR without incorporating a Key Transparency service,
Merkle-tree construction, directory, auditor network, or monitoring protocol
into the OpenETR core.

The central conclusion is:

> Independent verification does not require eliminating trusted actors. It
> requires limiting the proposition that each actor and each piece of evidence
> is trusted to establish.

This is consistent with the OpenETR discipline:

> Each proof proves only what it proves.

## Sources

This analysis uses:

- [IETF Key Transparency Protocol, draft-ietf-keytrans-protocol-05](https://datatracker.ietf.org/doc/html/draft-ietf-keytrans-protocol-05)
- [IETF Key Transparency Architecture, draft-ietf-keytrans-architecture-07](https://datatracker.ietf.org/doc/html/draft-ietf-keytrans-architecture-07)
- [Signal, "Introducing Automatic Key Verification"](https://signal.org/blog/automatic-key-verification/)

The IETF documents are Internet-Drafts and may change before publication.
OpenETR should therefore adopt the architectural distinctions described here,
not depend on draft-specific data structures or algorithms.

## Different Problems, Related Discipline

Key Transparency maintains verifiable, versioned mappings between labels and
cryptographic values. Its combined searchable tree and append-only log support
lookup, inclusion, consistency, auditing, and monitoring. These mechanisms are
designed to make interference, concealed updates, and inconsistent views
detectable under stated deployment assumptions.

Signal applies this pattern to mappings between public account identifiers and
encryption keys. Signal explicitly limits the resulting proposition: Key
Transparency can show that participants receive a consistent key association;
it does not establish the real-world identity of the account holder or prove
that an account has not been fully taken over.

OpenETR addresses a broader and different problem:

```text
Digital Artifact
  + DCR Evidence
  + Defined Rules
  -> Consequential State
```

The shared discipline is derivation from verifiable evidence. The systems
should not otherwise be conflated.

| Key Transparency | OpenETR |
| --- | --- |
| Maintains a versioned label-to-value mapping. | Preserves DCR evidence concerning a digest-identified artifact. |
| Uses a Transparency Log as an authoritative service under explicit auditing or monitoring assumptions. | Permits evidence to be obtained from relays, repositories, archives, bundles, or local stores without making one source authoritative. |
| Proves inclusion and consistency relative to tree heads. | Verifies event authenticity, graph relationships, and state transitions relative to an evidence set and rule set. |
| Detects inconsistent directory views under deployment-specific assumptions. | Preserves competing evidence and reports when available evidence does not support a unique state. |
| Does not establish the identity behind the account. | Leaves actor identity, authority, recognition, and effect contextual. |

OpenETR is not a transparency log. A Key Transparency proof may become linked
or stapled evidence used by an OpenETR verifier, but it does not become an
OpenETR control primitive.

## Separate Functions

OpenETR specifications and verifier output should keep the following functions
separate:

| Function | Question |
| --- | --- |
| Create | What signed evidence was produced? |
| Verify | Does the supplied evidence satisfy the identified cryptographic, structural, and transition rules? |
| Audit | Do observations or commitments support a conclusion that an evidence source maintained a consistent history? |
| Monitor | Does an evolving history remain consistent with prior observations or an affected participant's expectations? |
| Recognize | What external significance does a relying party give to the evidence or derived state? |

These functions may be performed by one implementation, but their conclusions
remain distinct. Verification of an event does not prove population-wide
observation. Agreement among auditors does not prove actor intent. Monitoring
does not determine legal effect. Recognition does not rewrite the underlying
evidence.

## Evidence Taxonomy

The following evidence categories establish different propositions:

| Evidence category | Proposition it may support | Proposition it does not establish by itself |
| --- | --- | --- |
| Event authenticity | A particular key signed the exact event. | Authority, intent, recognition, or unique state. |
| Observation or inclusion | A witness, repository, or log observed or included identified evidence. | Global completeness or transition validity. |
| Historical continuity | A later observed history extends an identified earlier history under the proof system used. | Correctness of every included action or legal continuity. |
| Temporal evidence | Evidence existed no later than, or was observed at, a supported time bound. | Authority, truth, or state validity. |
| Coverage evidence | An identified source or observation process covered a stated population, query, or interval. | Absence of evidence outside that scope. |
| Audit attestation | An auditor performed a stated procedure and signed its result. | Control, actor intent, universal consistency, or recognition. |
| Monitoring evidence | An observer compared evolving evidence with prior observations or expectations. | That an unexpected event is unauthorized or legally ineffective. |
| Recognition evidence | An authority or relying party accepted an actor, action, or state for a stated purpose. | Universal recognition or cryptographic validity. |

Profiles may require particular categories. The generic protocol need not
define a new event kind or action for every category.

## Equivocation And Divergent Observation

Valid signatures do not imply a single globally observed Evidence Graph.
Different evidence sources may omit events, return stale results, or present
different subsets. Authentic events may also form competing branches:

```text
                 transfer -> B
                /
Anchor --------+
                \
                 transfer -> C
```

Both transfers may be authentic signed statements. Defined rules determine
whether either contributes to Consequential State. If the evidence and rules
do not support a unique result, the verifier should report ambiguity rather
than manufacture certainty.

Relevant verifier findings may include:

- conflicting evidence;
- insufficient evidence;
- history divergence;
- unresolved candidate states; and
- evidence completeness unknown.

These are findings or dimension-specific outcomes, not necessarily new core
protocol enums. A conforming result should identify the evidence set, sources,
rules, and evaluation parameters on which the conclusion depends.

## Historical State Derivation

Historical reconstruction is a first-class verification capability. Where
sufficient evidence is available, a verifier should support semantics
equivalent to:

```text
derive_state(evidence_set, rule_set)
derive_state(evidence_set, rule_set, at_event=E)
```

The second operation derives the state for a candidate graph path ending at
event `E`. It is not automatically a statement about globally authoritative
state at the event's declared timestamp.

A historical-state result should identify:

- the terminal event or graph cut used;
- the ancestor records included in the derivation;
- the evidence sources and retrieval scope;
- the rule identifier and version;
- competing or related evidence present in the supplied evidence set;
- unresolved links or missing evidence; and
- the resulting state and warnings.

Historical state is therefore evidence-set-relative, rule-set-relative, and
path-relative. Signed event timestamps alone do not create a trusted total
order. Temporal Proofs or other accepted external evidence may add time
assurance as a separate result dimension.

This capability supports audit, litigation, regulatory review, secured
lending, historical-controller analysis, and termination or redemption
disputes without depending on an originating application's historical
database.

## Independent Witnesses And Auditors

An OpenETR attestation can carry evidence about an event, graph observation,
audit procedure, or external proof. An attestor may act as a witness or
auditor without becoming:

- the controller of the Digital Artifact;
- the author of the underlying event;
- the source of Consequential State;
- a canonical registry;
- a recognition authority; or
- proof of global completeness.

The attestation should identify the subject event, graph commitment, evidence
bundle, or observation to which it applies and describe the procedure or claim
being attested. A verifier then decides what proposition the attestation
supports under the applicable rules.

An attestation may have recognition significance when an external rule book
recognizes the attestor for a stated purpose. That recognition is additional
to, and does not arise merely from, the valid attestation signature.

## Monitoring As A Surrounding Service

Monitoring should not become a universal OpenETR action or another core centre
of concern. It is a service or evidence property surrounding the Evidence
Graph.

A history can be internally verifiable without proving that every signed
change was intended. A compromised signing key may produce a cryptographically
authentic transfer. Observation, audit, and agreement among evidence sources
do not establish that the controller intended that transfer. Monitoring can
help an interested party detect and challenge an unexpected event, but the
applicable rules and recognition context determine its consequence.

A domain or organizational profile may require monitoring, witness
attestations, source comparison, or response windows. The generic OpenETR
protocol does not.

## Resolve For Discovery; Staple For Evidence

External systems may help discover current key bindings, authority, status,
or service information. Historical verification should not depend solely on
the current response of an external directory.

Where practical, an evidence bundle should preserve or reference the external
evidence relevant when an event was evaluated. Examples include:

- controller-to-key binding evidence;
- identity or authority attestations;
- recognition credentials;
- authorization evidence;
- Key Transparency inclusion or consistency proofs;
- PKI certificates or certificate-status evidence;
- DID historical state;
- EUDI attestations;
- Temporal Proofs; and
- witness or audit attestations.

Stapled evidence remains subject to its own validation rules, expiry,
revocation model, privacy constraints, and recognition policy. Presence in a
DCR does not cause it to prove more than its native evidence model supports.

## Specification Direction

OpenETR should:

1. distinguish creation, verification, auditing, monitoring, recognition, and
   effect;
2. expose multidimensional verifier results;
3. preserve authentic but conflicting evidence;
4. report divergent source observations and unknown completeness;
5. support historical state derivation at an identified graph point;
6. allow attestations to describe witness and audit evidence without changing
   controller state by default;
7. permit external key-history and continuity evidence to be linked or
   stapled; and
8. keep all conclusions scoped to their evidence, sources, procedures, rules,
   and recognition context.

These refinements do not require a new OpenETR event kind or core action.

## Non-Goals

This design does not turn OpenETR into:

- a Key Transparency service;
- a transparency log;
- a blockchain;
- a global event-ordering or consensus system;
- an identity directory;
- a key-management protocol;
- a mandatory monitoring service; or
- an auditor governance framework.

OpenETR remains responsible for a narrower proposition:

> Given a Digital Artifact, DCR evidence, and defined rules, derive
> Consequential State independently.

Other systems may strengthen the evidence used in that derivation.

## Related OpenETR Specifications

- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Consequential State Architecture Design Note](./CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [OpenETR Generic Transfer Model](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- [Evidence Event Minimum Shapes](./CONTROL_EVENT_MINIMUM_SHAPES.md)
- [Linked Evidence Record Kind Design Note](./LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md)
- [OpenETR Draft National Standard](./OPENETR_DRAFT_NATIONAL_STANDARD.md)

