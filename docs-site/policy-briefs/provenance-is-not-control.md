# Provenance Is Not Control

Digital trust discussions often place provenance, authenticity, integrity, custody, authority, and control close together.

They are related, but they are not the same thing.

The core distinction is simple once named:

```text
Provenance asks where something came from and what happened to it.
Control asks what consequential state can be derived for the record now.
```

That distinction matters most when the record is not just evidence or content, but something whose value depends on transfer, presentation, redemption, encumbrance, discharge, or exclusive control.

## The Basic Difference

Provenance is about history.

It helps answer:

- who created the asset
- what system created it
- what transformations occurred
- what assertions were attached
- whether the asset still matches a signed provenance claim
- whether the provenance signer is trusted

Control is about state.

It helps answer:

- what the operative record is
- who currently controls it
- how control moved from one participant to another
- whether the record is encumbered
- whether a prior controller has been superseded
- whether the record has been redeemed, discharged, or terminated
- which policy recognizes the resulting state

The compact version is:

```text
Provenance makes history inspectable.
Control makes authority over the record stateful.
```

## Copying Reveals The Distinction

Digital things can be copied.

That is not, by itself, the failure.

The real requirement for transferable records is:

```text
Copying evidence must not copy control.
```

A copy of a bill of lading may reproduce the visible words, signatures, endorsements, and history. But a copy is not the operative bill merely because it looks the same.

The same point applies digitally.

A participant may copy:

- the record bytes
- the metadata
- the provenance statement
- the signatures
- the history
- the evidence bundle

But copying that evidence should not create a new current controller.

Control depends on consequential state derived from validated DCR evidence
under protocol rules. Whether that state is accepted for a legal or institutional
purpose is a separate recognition question.

## C2PA As Provenance Infrastructure

C2PA is a strong model for content provenance.

It can bind signed claims and assertions to an asset. A validator can check whether a manifest belongs with the presented asset and whether protected content still matches the signed claim.

That is exactly what many media and document workflows need.

C2PA is well suited to questions such as:

- Is this provenance authentic for this asset?
- Who or what created this image, video, or document?
- What transformations occurred?
- Which assertions are attached?
- Is the signed manifest still bound to the content?

This is provenance, and it is valuable.

It is not the same as control.

## OpenETR As Control Infrastructure

OpenETR implements the control side of the distinction. It identifies content
as a Digital Artifact by digest. Signed records concerning the artifact form a
DCR spanning its evidenced lifecycle. Validation checks the DCR evidence, and
protocol rules derive consequential state.

Those events can express:

- issuance
- transfer
- acceptance
- attestation
- encumbrance
- discharge
- redemption
- termination

The resulting graph helps answer:

```text
What is this record, and who controls it now?
```

OpenETR can carry provenance-like evidence too, but its distinctive role is
the DCR: a signed, artifact-specific record or graph from which consequential
state can be independently derived.

## Why They Are Complementary

C2PA and OpenETR are not competing solutions.

They are examples of different trust primitives.

The short comparison is:

```text
C2PA provides provenance evidence about content.
OpenETR validates DCR evidence and applies protocol rules to derive
consequential state.
```

Or more sharply:

```text
C2PA makes provenance portable with content.
OpenETR makes evidence portable without making control copyable.
```

Together, they can be stronger than either alone.

For example:

```text
digital trade record
  -> C2PA provenance for content, media, or supporting evidence
  -> OpenETR digest identifying the Digital Artifact
  -> DCR graph for transfer, encumbrance, redemption, or termination
  -> protocol rules deriving consequential state
  -> recognition policy deciding effect
```

C2PA can tell a relying party where the content came from.

OpenETR can tell a relying party which Digital Artifact is involved, what DCR
evidence exists, and what state follows under the protocol rules.

Recognition policy decides what legal, commercial, institutional, or operational effect follows.

## Policy Implications

Policy and technical frameworks should avoid treating provenance as a substitute for control.

A system should not conclude:

```text
This record has authentic provenance, therefore it is controlled.
```

Nor should it conclude:

```text
This artifact has a DCR, therefore all provenance claims are trusted.
```

The better architecture is layered:

```text
Protocol:
  verify hashes, signatures, manifests, events, and references

Control:
  validate DCR evidence and derive candidate state under protocol rules

Recognition:
  decide what effect to give the evidence and state
```

This distinction is especially important for transferable records, including warehouse receipts, bills of lading, promissory notes, bills of exchange, and other instruments where control substitutes for possession.

## Bottom Line

Provenance and control are both essential, but they are different trust primitives.

Provenance explains history.

Control governs state.

C2PA is a strong provenance technology. OpenETR provides DCR evidence and a
state transition rules. The useful policy move is to use each where it
belongs and avoid asking one layer to do the work of the other.

## Related Design Note

- [Provenance And Control Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/PROVENANCE_AND_CONTROL_DESIGN_NOTE.md)

## Related Materials

- [OpenETR And C2PA Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_AND_C2PA_DESIGN_NOTE.md)
- [OpenETR And C2PA Policy Brief](./openetr-and-c2pa.md)
- [OpenETR MLETR And ETDA Mapping Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_MLETR_ETDA_MAPPING_DESIGN_NOTE.md)
