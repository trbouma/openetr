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

## Digital Object And Digital Original

A **Digital Object** has uniquely and stably identifiable content.

A **Digital Original** is a Digital Object for which consequential state can be
derived from valid, end-verifiable events under OpenETR protocol rules.

```text
Digital Object + end-verifiable events + protocol rules = Digital Original
```

Consequential state may describe the current controller, lifecycle status,
active guards, prior transitions, or another result that matters to what may
validly happen next. An application may display or cache that state, but it is
not the sole authority for it.

## The Consequential State Pipeline

OpenETR separates five questions that are often blended together:

| Layer | Question |
| --- | --- |
| Object | What content is identified? |
| Events | What signed actions occurred? |
| Consequential state | What state follows under the protocol rules? |
| Recognition | Who accepts that state, and for what purpose? |
| Effect | What external consequence follows? |

The relationship is:

```text
event -> protocol rules -> consequential state -> recognition -> effect
```

A valid Anchor can establish candidate consequential state and bring a Digital
Object into the OpenETR Digital Original model. It does not prove that the
signer was uniquely authorized, resolve every competing event, compel a relying
party to recognize the result, or create legal effect on its own.

## What OpenETR Contributes

OpenETR provides a consequential state layer for digital objects. Signed events
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
  -> Digital Object
  -> valid events and protocol rules
  -> Digital Original with consequential state
  -> recognition by a competent verifier
  -> accepted effect
```

The same pattern can apply to warehouse receipts, bills of lading, product
passports, permits, certificates, community records, and archives.

## Multiple Anchors And Conflicts

A Digital Object may have multiple anchors or competing event branches.
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

The architectural objective is simple:

> Digital Originals should outlive applications.

## Related Design Notes

- [Consequential State Architecture](https://github.com/trbouma/openetr/blob/main/docs/specs/CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [Digital Originality, Control, And Standing](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md)
