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

In plain language, the important question is not “which physical file is the
one true copy?” It is “what verifiable history and current state concern this
exact content?” A copy can reproduce the content, but it cannot create a valid
issuance, transfer, discharge, or termination event.

**Consequential State** is the result of validating a Digital Controllable
Record—or its graph of related records—in relation to an identified policy. It
matters because accepting that result can change what may validly happen next
concerning the artifact. It can establish or change a controller, record a
transfer in progress, activate an encumbrance, discharge a restriction,
delegate authority, or terminate an active lifecycle. It is consequential
because recognition of it can affect control, authority, rights, obligations,
restrictions, standing, status, or permitted actions.

This is different from ordinary application state. A selected tab, cached
display value, database row, or background-job status may help an application
operate, but it does not become authoritative OpenETR state merely because the
application stores it. Consequential State must be reproducible by validating
portable, end-verifiable DCR evidence under the same identified policy.

An **end-verifiable event** is a signed record that a recipient can verify
independently, without calling the application that originally produced it.

## A First Example

Consider a warehouse receipt stored as a PDF:

1. A digest identifies the exact PDF content. That content is the **Digital
   Artifact**.
2. A warehouse signs an Anchor record concerning the PDF. Later signed records
   may transfer it, encumber it, discharge the encumbrance, or terminate its
   lifecycle. Together those records are the **Digital Controllable Record**.
3. An applicable policy validates the DCR as a whole and produces the current
   **Consequential State**.
4. The PDF, now associated with established consequential state, is a
   **Digital Original** in the OpenETR technical sense.
5. A bank, registry, court, or trading partner decides whether to recognize
   that state and what legal or commercial effect follows.

The PDF may be copied many times. Those copies represent the same
digest-identified artifact; they do not independently reproduce its signed
history or state.

## Digital Artifact, Digital Controllable Record, And Digital Original

A **Digital Artifact** is persistent digital content with a unique content
identity established by a cryptographic digest. Byte-for-byte copies with the
same digest represent the same Digital Artifact.

A **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records through which consequential state
concerning a Digital Artifact can be established and transitioned. The DCR is
the signed evidence structure, not the file.

The name is easiest to understand as **the controllable record concerning the
artifact**, rather than as a description of the artifact itself.

A **Digital Original** is a Digital Artifact for which Consequential State has
been established by validating its DCR under an applicable policy.

```text
Digital Artifact -> referenced by -> Digital Controllable Record
Digital Controllable Record + applicable policy -> validation
validation result -> Consequential State
Digital Artifact + established Consequential State -> Digital Original
```

![Digital Artifact to Digital Controllable Record to Digital Original](../assets/images/digital-artifact-to-digital-original.svg)

Creation, scanning, translation, rendering, or transformation may produce a
new Digital Artifact. Novelty alone does not make it a Digital Original.

> Creation produces a Digital Artifact. Consequential state makes that
> artifact a Digital Original.

## Concrete Example: An English Gutenberg Reconstruction

Consider a digitized page from the Gutenberg Bible. The Bible was printed in
Latin in Mainz in the mid-fifteenth century, and digitized page images are now
available through institutions including the [Library of
Congress](https://www.loc.gov/item/2021666734/).

Suppose an editor translates the Latin text into English and renders the
translation using typography and layout intended to preserve the visual
character of the source page. The resulting image is new. Gutenberg never
printed this English page. It is neither a scan of an existing physical page
nor merely another copy of the source image.

Once finalized, the new content is put into canonical form and assigned a
cryptographic digest:

```text
Original Gutenberg page
          |
          | translate and render
          v
   New digital content
          |
          | canonicalize and digest
          v
   DIGITAL ARTIFACT
```

The digest establishes the content identity of the new artifact. The image may
be novel and may be the first representation of its kind, but novelty alone
does not make it an OpenETR Digital Original.

Now suppose a scholar, library, archive, publisher, or other institution
examines the artifact and signs this statement:

> This Digital Artifact is an English reconstruction of the identified
> Gutenberg Bible page, prepared to represent the content and visual
> experience of that source page.

The signed end-verifiable record references the artifact's digest. It becomes
the first record in a candidate DCR:

```text
DIGITAL ARTIFACT
digest: abc123...
        |
        | referenced by
        v
SIGNED RECORD
        |
        v
DIGITAL CONTROLLABLE RECORD
```

The DCR may initially contain only that Anchor record. It may later grow into
a graph containing attestations, control transfers, restrictions, superseding
versions, or termination records.

An applicable policy validates the DCR as a whole and produces Consequential
State concerning the artifact. A simplified projection might show:

```text
artifact       = abc123...
lifecycle      = active
controller     = <controller key>
anchor signer  = <signing key>
source         = <identified Gutenberg page>
designation    = English reconstruction
evidence       = <basis event ids>
```

This state is not authoritative merely because an application stored it in a
database. Another conforming application can obtain the artifact and DCR,
verify the signatures and references, apply the same validation policy, and
reproduce the applicable Consequential State.

Once Consequential State has been established by validating the DCR under an
applicable policy, the artifact is an OpenETR Digital Original in the technical
sense:

```text
NEW DIGITAL CONTENT
        |
        v
DIGITAL ARTIFACT
uniquely identifiable content
        |
        v
DIGITAL CONTROLLABLE RECORD
signed end-verifiable evidence spanning the lifecycle
        |
        | validate the DCR as a whole
        | against an applicable policy
        v
CONSEQUENTIAL STATE (validation result)
        |
        v
DIGITAL ORIGINAL
```

The signature proves which key made the statement, what artifact the statement
concerns, and what was said. It does not prove that the signer is a recognized
Gutenberg authority. A university might recognize a particular scholar; a
national library might recognize its curator; another institution might apply
a different recognition policy.

```text
Digital Original
      |
      | signer and state accepted for a purpose?
      v
RECOGNITION
      |
      v
EFFECT
```

The resulting English image can still be copied freely. Byte-identical copies
have the same digest and represent the same Digital Artifact:

```text
Copy A --+
Copy B --+-- same digest --> DIGITAL ARTIFACT abc123...
Copy C --+
```

Making another copy does not create another DCR, controller, or consequential
history. OpenETR does not make the information scarce; it makes the
consequential history surrounding its content identity independently
verifiable.

The distinction can therefore be summarized precisely:

> The translated page is created as a new Digital Artifact. Validation of its
> DCR under an applicable policy establishes Consequential State and makes it a
> Digital Original. Recognition determines whether that result is accepted as
> authoritative and what effect it receives for a particular purpose.

## The Consequential State Pipeline

Digital originality does not arise from one cryptographic operation or one
institutional decision. Canonical content first gives the Digital Artifact a
stable identity. One or more signed records concerning that artifact form a
candidate DCR spanning its evidenced lifecycle. Those records provide portable
evidence of what actors attempted or asserted. The DCR is then evaluated as a
whole under an applicable policy by the **Consequential State Machine
(CSM)**. Consequential State is the result of that CSM validation; it is not
another record or container beside the DCR.

The DCR records the consequential actions. The CSM determines their
consequences.

Recognition and effect follow from that result. A verifier, institution,
community, contract, or jurisdiction decides whether to accept the signer,
DCR, and Consequential State for a particular purpose and what practical,
institutional, commercial, or legal consequence follows. Keeping these layers
separate prevents content identity, cryptographic validity, policy validation,
authority, and external effect from being mistaken for one another.

The pipeline therefore separates five questions that are often blended
together:

| Layer | Question |
| --- | --- |
| Artifact | What persistent content is identified? |
| DCR | Which signed record or record graph concerns the artifact? |
| CSM validation and Consequential State | What state results when the DCR is evaluated under the identified policy? |
| Recognition | Who accepts that state, and for what purpose? |
| Effect | What external consequence follows? |

The complete relationship is:

```text
Digital Artifact
  -> Digital Controllable Record
  -> CSM validation of the DCR under an applicable policy
  -> Consequential State and Digital Original
  -> recognition of that state
  -> effect
```

A candidate Anchor is a one-record DCR concerning a Digital Artifact. A valid
Anchor evaluated under an applicable policy can establish initial
Consequential State and make the artifact a Digital Original. It does not prove that the
signer was uniquely authorized, resolve every competing event, compel a relying
party to recognize the result, or create legal effect on its own.

A provenance claim such as “I created this artifact” is different from an
authority claim such as “I certify this artifact for purpose X.” OpenETR makes
the signer and artifact inspectable. Recognition of the signer's authority is
separate.

## What OpenETR Contributes

OpenETR provides a Consequential State layer for Digital Artifacts. Signed
records can describe anchoring, transfer, encumbrance, discharge, redemption,
and termination. The CSM applies an applicable policy to determine whether the
DCR is valid in light of prior state and what result follows.

This lets an independent verifier ask:

- Which Digital Artifact is involved?
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
OpenETR Digital Original when its DCR is validated under an applicable policy
and produces Consequential State.

A verifier may then recognize the licensing authority's key and accept that
state for a particular purpose. Only at that point does the verification have
the corresponding institutional or legal effect.

```text
Physical licence
  -> scan and stable digest
  -> Digital Artifact
  -> candidate Digital Controllable Record
  -> DCR validation under an applicable policy
  -> Digital Original with consequential state
  -> recognition by a competent verifier
  -> accepted effect
```

The same pattern can apply to warehouse receipts, bills of lading, product
passports, permits, certificates, community records, and archives.

## Multiple Anchors And Conflicts

A Digital Artifact may have multiple anchors or competing event branches.
OpenETR should preserve that evidence rather than silently selecting an
authority. A stated validation policy can reject invalid transitions and
produce candidate Consequential State; recognition determines which result,
actor, or policy is accepted in a particular context.

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
