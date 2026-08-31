# Digital Originality

## The Problem

Digital systems make copying effortless. A scanned licence, a PDF certificate,
a warehouse receipt, or a digital form can be duplicated perfectly. The bytes
therefore cannot tell us which copy has continuing operational significance.

Hashing, signing, timestamping, or storing a file can identify it and provide
valuable evidence. None of those acts, by itself, explains what may validly
happen next.

The key distinction is:

> Digital originality is about consequential state, not copy prevention.

**Consequential state** is protocol state that can change what may validly
happen next concerning an identified artifact. It can establish or change a
controller, record a transfer in progress, activate an encumbrance, discharge
a restriction, delegate authority, or terminate an active lifecycle. It is
consequential because relying on it can affect control, authority, rights,
obligations, restrictions, standing, status, or permitted actions.

This is different from ordinary application state. A selected tab, cached
display value, database row, or background-job status may help an application
operate, but it does not become authoritative OpenETR state merely because the
application stores it. Consequential state must be reproducible from portable,
end-verifiable events under identified protocol rules.

## Digital Artifact, Digital Controllable Record, And Digital Original

A **Digital Artifact** is persistent digital content with a unique content
identity established by a cryptographic digest. Byte-for-byte copies with the
same digest represent the same Digital Artifact.

A **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records through which consequential state
concerning a Digital Artifact can be established and transitioned. The DCR is
the signed evidence structure, not the file.

A **Digital Original** is a Digital Artifact for which consequential state has
been established through a DCR under OpenETR protocol rules.

```text
Digital Artifact -> referenced by -> Digital Controllable Record
Digital Controllable Record + protocol rules -> consequential state
Digital Artifact + consequential state -> Digital Original
```

![Digital Artifact to Digital Controllable Record to Digital Original](../assets/images/digital-artifact-to-digital-original.svg)

Creation, scanning, translation, rendering, or transformation may produce a
new Digital Artifact. Novelty alone does not make it a Digital Original.

> Creation produces a Digital Artifact. Consequential state makes that
> artifact a Digital Original.

## The Consequential State Pipeline

Digital originality does not arise from one cryptographic operation or one
institutional decision. It emerges through a sequence of distinct layers.
First, canonical content gives the Digital Artifact a stable identity. One or
more signed events concerning that artifact form a candidate DCR. Those events
provide portable evidence of what actors attempted or asserted. OpenETR rules
validate the DCR against prior state and derive the consequential state that
makes the artifact a Digital Original.

Recognition and effect come afterward. A verifier, institution, community,
contract, or jurisdiction decides whether to accept the actor, graph, or
derived state for a particular purpose. Applicable rules then determine what
practical, institutional, commercial, or legal consequence follows. Keeping
these layers separate prevents content identity, cryptographic validity,
protocol state, authority, and legal effect from being mistaken for one
another.

The pipeline therefore separates six questions that are often blended
together:

| Layer | Question |
| --- | --- |
| Artifact | What persistent content is identified? |
| DCR | Which signed record or record graph concerns the artifact? |
| Consequential state | What state follows under the protocol rules? |
| Recognition | Who accepts that state, and for what purpose? |
| Effect | What external consequence follows? |

The complete relationship is:

```text
Digital Artifact
  -> Digital Controllable Record
  -> OpenETR protocol rules
  -> consequential state and Digital Original
  -> recognition
  -> effect
```

A candidate Anchor is a one-record DCR concerning a Digital Artifact. A valid
Anchor processed under OpenETR rules can establish initial consequential state
and make the artifact a Digital Original. It does not prove that the
signer was uniquely authorized, resolve every competing event, compel a relying
party to recognize the result, or create legal effect on its own.

A provenance claim such as “I created this artifact” is different from an
authority claim such as “I certify this artifact for purpose X.” OpenETR makes
the signer and artifact inspectable. Recognition of the signer's authority is
separate.

## What OpenETR Contributes

OpenETR provides a consequential state layer for Digital Artifacts. Signed events
can describe anchoring, transfer, encumbrance, discharge, redemption, and
termination. Protocol rules determine whether those events are valid in light
of prior state and what state follows.

This lets an independent verifier ask:

- Which object is involved?
- Which events are authentic and structurally valid?
- Which prior state constrains the next transition?
- Who controls the object under the applicable rules?
- Are there unresolved conflicts or active guards?
- Has the lifecycle ended?

The answer can be reconstructed from portable evidence even if the application
that first displayed the record is unavailable.

> System failure need not become state failure.

## Recognition And Effect Remain Contextual

Protocol-valid state is not the same as universally accepted authority.
Recognition may come from a law, contract, institution, community, registry,
or verifier policy. Effect is the consequence that the recognition context
gives the derived state.

The term **recognized Digital Original** can be used when a Digital Original
and its consequential state have been accepted for a stated purpose.

```text
Digital Original + recognition + applicable rules = recognized effect
```

This distinction keeps the protocol useful without asking it to decide who is
a competent issuer, whether a signer is legally authorized, or what every
jurisdiction must accept.

## A Simple Example

A driver's licence can be scanned, hashed, and signed. The scan becomes an
OpenETR Digital Original when valid events about that identified object produce
derivable consequential state under OpenETR rules.

A verifier may then recognize the licensing authority's key and accept that
state for a particular purpose. Only at that point does the verification have
the corresponding institutional or legal effect.

```text
Physical licence
  -> scan and stable digest
  -> Digital Artifact
  -> candidate Digital Controllable Record
  -> valid DCR and protocol rules
  -> Digital Original with consequential state
  -> recognition by a competent verifier
  -> accepted effect
```

The same pattern can apply to warehouse receipts, bills of lading, product
passports, permits, certificates, community records, and archives.

## Multiple Anchors And Conflicts

A Digital Artifact may have multiple anchors or competing event branches.
OpenETR should preserve that evidence rather than silently selecting an
authority. Deterministic protocol rules can reject invalid transitions and
derive candidate states; recognition policy decides which candidate, actor, or
rule set is accepted in a particular context.

Conflict visibility is therefore a feature, not a defect.

## Policy Consequences

Good policy should ask:

- What state variable matters?
- Which events may change it?
- Which signing keys may authorize those events?
- What prior-state constraints apply?
- How can another party derive the same result independently?
- How are conflicts, supersession, and termination handled?
- Who recognizes the result, for what purpose, and with what effect?

This makes the technical boundary explicit while leaving institutional and
legal judgment visible.

## Bottom Line

OpenETR is not a magic originality machine and does not try to prevent copying.
It gives copied digital content a portable, verifiable history from which
consequential state can be independently derived.

A copy can reproduce content. It cannot independently reproduce consequential
state.

The architectural objective is simple:

> Digital Originals should outlive applications.

## Related Design Notes

- [Consequential State Architecture](https://github.com/trbouma/openetr/blob/main/docs/specs/CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [Digital Controllable Record](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
- [Digital Originality, Control, And Standing](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md)
