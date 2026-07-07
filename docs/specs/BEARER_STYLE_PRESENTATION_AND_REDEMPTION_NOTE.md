# Bearer-Style Presentation and Redemption Note

This note describes a possible OpenETR recognition profile in which a Controlled Object may be treated in a bearer-like or presenter-entitled manner.

It is intentionally short and exploratory.

## Status

Draft.

## Purpose

OpenETR is capable of recording:

- a Controlled Object
- the control history of that object
- attestations associated with the object or specific lifecycle events

This creates the possibility that an attestation could carry additional meaning or instruction to the effect that redemption should be available to the valid presenter of the object and its recognized evidence chain, rather than only to a specifically named controller.

This note does not say that OpenETR itself creates bearer status as a matter of law.

It says only that OpenETR can carry the evidence from which a recognition framework might choose to recognize a bearer-like redemption model.

## Core Idea

A party could:

1. issue a PDF or other electronic record into OpenETR as a Controlled Object
2. associate an attestation with that object or a relevant event
3. have that attestation carry additional instruction or endorsement-like meaning
4. rely on a recognition framework that treats the object as redeemable by a valid presenter

In that model, the practical basis for redemption is not merely possession of a file.

It is presentation of:

- the Controlled Object
- the relevant OpenETR event chain
- the associated attestation or indorsement-like instruction
- any other evidence required by the relying party's policy

## Relationship to Endorsement and Indorsement

Under the revised OpenETR model, endorsement or indorsement is not a standalone control-event primitive.

Instead, where relevant, it may be expressed as an attestation associated with an underlying OpenETR event.

In a bearer-style profile, that attestation could carry additional instruction to the effect that:

- the object is payable to bearer
- the object is redeemable by presenter
- the object may be presented without naming a further transferee

Whether such an attestation has that effect is determined by the applicable recognition framework, contract, and governing law.

## Redemption Logic

In this profile, redemption would be recognized based on presentation of a valid evidence set rather than only on a named current-controller relationship.

That evidence set may include:

- the object identifier
- the origin event
- the relevant control history
- any associated attestation carrying bearer-style or presenter-entitled meaning
- any redeem event
- any termination event once performance is complete

The practical redemption question becomes:

> Has the presenter shown a recognized evidence chain that entitles presentation and performance for this object?

## Double Redemption Risk

If a bearer-style or presenter-entitled profile is used, the redeemer must manage double-redemption risk explicitly.

One straightforward operational approach is:

- identify the object by its canonical object id
- recognize only the first valid redemption for that object id
- record that redemption and later termination against the same object id
- refuse later redemption attempts for the same object once redemption or termination has already been recognized

In that sense, the object id functions as the practical anti-double-redemption anchor.

## Important Distinction

This model is different from a strict named-controller model.

In the strict named-controller model:

- entitlement follows the recognized control chain to the current controller

In a bearer-style presentation model:

- entitlement may instead follow presentation of a recognized evidence chain plus a bearer-style or presenter-entitled attestation

That is a meaningful policy shift.

It should therefore be treated as a distinct recognition profile rather than as an automatic implication of ordinary transfer logic.

## Scope of OpenETR

OpenETR can provide the evidence.

It does not itself provide mandate or effect.

It does not itself decide:

- whether a given object should be treated as bearer-like
- whether a presenter is legally entitled to redemption
- whether an indorsement-like attestation is sufficient
- what legal effect follows from presentation

Those remain recognition-layer questions.

## Summary

OpenETR could support a bearer-style or presenter-entitled redemption profile by expressing the relevant instruction as an attestation associated with an underlying event or object.

The obligor or redeemer could then manage double redemption by recognizing only the first valid redemption for the object id and recording redemption or termination against that same object.

Whether that profile should be recognized, and on what terms, remains outside the protocol itself.
