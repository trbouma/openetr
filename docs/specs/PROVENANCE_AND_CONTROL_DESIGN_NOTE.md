# Provenance And Control Design Note

This note describes a general distinction between provenance and control.

OpenETR is one implementation of this distinction. C2PA is a useful comparison point because it solves a different, complementary problem.

The core insight is:

```text
Provenance and control are separate concepts.
They are often adjacent, but they are not the same thing.
```

## Status

Draft.

## Summary

Provenance asks:

```text
Where did this thing come from, who made assertions about it,
and what happened to it over time?
```

Control asks:

```text
Who can exercise recognized power over this record now,
and how did that control state arise?
```

The difference may seem obvious after it is named, but it is easy to miss because many digital trust systems bundle related ideas together: authenticity, integrity, provenance, custody, authority, entitlement, possession, and control.

The transferable-record problem makes the distinction unavoidable.

For ordinary content, it may be enough to know that an asset is authentic, unaltered, and accompanied by credible provenance.

For a transferable record, that is not enough. The record also needs a stateful control primitive.

The compact statement is:

```text
Provenance makes history inspectable.
Control makes authority over the record stateful.
```

## The Core Distinction

Provenance is about origin and history.

It records or helps verify:

- who created something
- what system created it
- what transformations occurred
- which assertions were attached
- which evidence supports those assertions
- whether the content still matches the signed provenance statement
- whether the provenance signer or trust chain is acceptable

Control is about recognized authority over a record.

It records or helps verify:

- what the record is
- who issued or originated it
- who currently controls it
- which event transferred or changed control
- which prior event was consumed, superseded, or relied on
- whether there are conflicting control branches
- whether encumbrances, holds, redemption, or termination affect control
- which policy recognizes the resulting control state

The two concepts interact, but they answer different questions.

| Question | Provenance | Control |
| --- | --- | --- |
| Where did this asset come from? | Primary concern | Supporting context |
| What happened to this content? | Primary concern | Supporting context |
| Who made this assertion? | Primary concern | Relevant when assertion affects state |
| Has this content changed? | Primary concern | Relevant to object identity |
| What is the operative record? | Not sufficient by itself | Primary concern |
| Who controls the record now? | Not sufficient by itself | Primary concern |
| Can control be transferred? | Not the core problem | Primary concern |
| Can copying evidence copy control? | Not usually the problem | Must be prevented |

## Why The Distinction Gets Blurred

The distinction is often blurred because provenance evidence can be very strong.

A signed provenance record may prove:

- the asset was created by a particular actor
- the asset has not changed relative to a signed claim
- the asset has a verified transformation history
- the asset carries trustworthy metadata

Those are important properties.

But they do not by themselves answer a control question.

For example, a signed history of a bill of lading, warehouse receipt, promissory note, or other transferable record may be authentic and complete. A relying party may still need to know which participant is the current controller and whether a later transfer, pledge, discharge, surrender, or termination changed the recognized state.

In other words:

```text
Authentic history is not the same as current authority.
```

## Copyability Reveals The Difference

Digital copying is not the security failure by itself.

Everything digital can be copied:

- the record bytes
- the visible document
- the metadata
- the provenance statement
- the signatures
- the event history
- the evidence bundle

The necessary property for a transferable record is different:

```text
Copying evidence must not copy control.
```

This is the digital analogue of photocopying a paper bill of lading.

A photocopy may reproduce the words, layout, signatures, and endorsement marks. It may be useful evidence. But the copy-holder does not possess the operative bill merely because they hold a copy.

In a digital system, copies may reproduce the evidence. They should not create a new recognized current controller unless the control graph and recognition policy support that result.

This is the central point:

```text
Provenance can travel with copies.
Control must remain tied to the recognized state of the record.
```

## The Three-Layer Model

The distinction fits a three-layer model.

```text
Protocol:
  Can I verify the hashes, signatures, events, manifests, and references?

Control:
  Who controls this record now under the reconstructed state graph?

Recognition:
  What legal, commercial, institutional, or operational effect follows?
```

Provenance systems are usually strongest at the protocol and evidence-history layers.

Control systems must add a state model.

Recognition systems decide what effect to give the verified evidence and derived control state.

## C2PA As A Provenance Example

C2PA is a strong example of provenance infrastructure.

It binds signed claims and assertions to an asset. A validator can check whether the manifest belongs with the presented asset and whether the protected content still matches the signed claim.

That is exactly the right model for many content authenticity questions:

- Who created this image, video, document, or media asset?
- What transformations occurred?
- Which assertions are attached?
- Is the provenance signature valid?
- Does the protected content still match the signed manifest?

The C2PA question is:

```text
Is this provenance authentic for this asset?
```

C2PA does not need to answer:

```text
Who currently controls this transferable record?
```

That is not a weakness. It is a different problem.

## OpenETR As A Control Example

OpenETR is an implementation of the control side of the distinction.

It treats a record as a digest-identified Controlled Object and associates signed events with that object.

The relevant evidence includes:

- object digest
- origin event
- signed control events
- prior-event references
- participant references
- attestations
- encumbrances
- discharge events
- redemption events
- termination events
- verifier-policy output

The OpenETR question is:

```text
What is this record, and who controls it now?
```

OpenETR can also preserve provenance-style evidence, but its distinctive contribution is the control graph.

That graph lets a verifier reconstruct a candidate state:

```text
issue -> transfer -> encumber -> discharge -> transfer -> redeem -> terminate
```

The graph does not by itself create legal effect. Recognition policy decides what effect follows. But the graph provides the evidence structure needed to ask the control question.

## C2PA And OpenETR Together

C2PA and OpenETR are complementary because provenance and control are complementary.

The compact comparison is:

```text
C2PA makes provenance portable with content.
OpenETR makes evidence portable without making control copyable.
```

Or:

```text
C2PA binds assertions to an asset.
OpenETR binds assertions and control transitions to an identified record.
```

Used together:

- C2PA can describe content origin, transformation, and provenance assertions.
- OpenETR can identify the operative record and preserve its signed control graph.
- Recognition policy can evaluate both.

For example:

```text
warehouse receipt package
  -> C2PA evidence about document generation, inspection media, or supporting artifacts
  -> OpenETR digest identifying the controlled record
  -> OpenETR control graph showing issuance, transfer, encumbrance, discharge, redemption, or termination
  -> verifier policy deciding recognition
```

Neither layer replaces the other.

## Design Implications

Systems that need provenance should preserve provenance explicitly.

Systems that need control should model control explicitly.

A design should avoid saying:

```text
This record has provenance, therefore it is controlled.
```

It should also avoid saying:

```text
This record has a control graph, therefore all provenance assertions are trusted.
```

Better:

```text
Provenance evidence supports history and authenticity.
Control evidence supports state and authority.
Recognition policy decides effect.
```

## Implications For Transferable Records

For transferable records, the provenance/control distinction is not academic.

A transferable-record system must be able to answer:

- What is the operative record?
- Who is the current controller?
- Was control validly transferred?
- Is there a conflicting branch?
- Is the record encumbered?
- Has the record been redeemed or terminated?
- Which evidence supports that state?
- Which policy recognizes the result?

Provenance helps, but it does not replace those questions.

This is why signatures, manifests, credentials, registries, and content provenance are not enough by themselves. They may provide excellent evidence. The record still needs a control primitive if rights, obligations, possession-equivalence, or transferability depend on stateful control.

## Non-Goals

This distinction does not imply that provenance is less important than control.

It also does not imply that every record needs a control graph.

Many assets only need provenance, integrity, authenticity, or attribution.

Many records need lifecycle evidence but not transferable control.

Some records need both.

The purpose of the distinction is to avoid using one concept as an imprecise substitute for the other.

## Open Questions

- What terminology should be used when a system needs provenance, lifecycle state, and control state together?
- Should control graphs include provenance events directly, or should provenance remain linked evidence?
- How should verifiers present provenance validity, graph validity, and recognition status without collapsing them?
- Which document families need control rather than only provenance?
- How should C2PA-style evidence be referenced from a control graph?
- How should transferable-record systems explain copyability without implying that digital records cannot be copied?

## Related Documents

- [OpenETR and C2PA Design Note](./OPENETR_AND_C2PA_DESIGN_NOTE.md)
- [Controllable Records Taxonomy](./CONTROLLABLE_RECORDS_TAXONOMY.md)
- [OpenETR Generic Transfer Model](./OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR MLETR And ETDA Mapping Design Note](./OPENETR_MLETR_ETDA_MAPPING_DESIGN_NOTE.md)
