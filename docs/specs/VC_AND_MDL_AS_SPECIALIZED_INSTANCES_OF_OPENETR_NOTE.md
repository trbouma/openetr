# Verifiable Credentials and mDL as Specialized Instances of OpenETR Note

This note explains how claim-centric credential models such as W3C Verifiable Credentials and mobile driver's licenses may be understood as more specific instances of the generalized OpenETR model.

It is intended as a conceptual design note, not as a claim of formal equivalence between standards.

## Status

Draft.

## Core Claim

OpenETR can be understood as a generalized model for:

- signed electronic records
- associated assertions
- restrictions and presentation conditions
- lifecycle events
- recognition of mandate or effect under policy

Under that broader interpretation, a W3C Verifiable Credential or a mobile driver's license can be viewed as a more specific, claim-centric instance of the same general pattern.

This does not mean that OpenETR, W3C VC, and mDL are identical.

It means that VC and mDL fit naturally within a more general OpenETR framing in which:

- there is an identifiable digital record
- claims or assertions are associated with that record
- a relying party evaluates the record under its own policy before relying on it
- technical validity does not by itself determine recognition or effect

This comparison does not imply that one model is better than the other.

Rather, the models serve different purposes and operate at different levels of generality.

## Why OpenETR Is More General

OpenETR is not limited to identity credentials or subject-attribute assertions.

It is a generalized model for electronic records that may involve:

- issuance
- transfer
- attestation
- encumbrance
- discharge
- redemption
- termination
- additional restrictions on presentation, use, or recognition

This allows OpenETR to model a much wider class of records than a typical credential model, including:

- bills of lading
- warehouse receipts
- permits
- certificates
- memberships
- digital entitlements
- other transferable or controlled records

Put simply:

- W3C VC and mDL models focus primarily on signed claims
- OpenETR focuses primarily on controllable records and their lifecycle

That lifecycle may include:

- issuance
- transfer
- restriction or encumbrance
- discharge
- redemption
- termination

OpenETR is therefore not primarily a model for proving subject attributes.

It is a model for signed electronic records that may be issued, controlled, transferred, restricted, redeemed, or terminated and then recognized under the applicable framework.

## W3C Verifiable Credentials as a Specialized Instance

W3C Verifiable Credentials are primarily concerned with signed claims made by an issuer about a subject and later presented by a holder to a verifier.

That makes them narrower and more claim-centric than the full OpenETR model.

Even so, a W3C VC can be understood within the generalized OpenETR framing as follows:

- the credential is the relevant electronic record
- issuance of the credential corresponds to `ISSUE`
- claims, terms of use, evidence, and related issuer statements correspond to associated `ATTEST`-style assertions
- status, suspension, revocation, expiry, or presentation restrictions may be modeled as associated restriction or termination-style events
- verifier reliance corresponds to recognition under policy

Under this interpretation, a VC is a specialized OpenETR-like pattern in which transfer is usually absent or tightly constrained and the central function of the record is the presentation of verifiable claims.

## Mobile Driver's Licenses as a Specialized Instance

A mobile driver's license, or `mDL`, can be understood in a similar way.

An mDL is a digitally issued credential that is:

- created by an issuing authority
- associated with a holder
- presented to a verifier
- evaluated under policy before reliance

In generalized OpenETR terms:

- the mDL record is the relevant electronic record
- issuance by the authority corresponds to `ISSUE`
- the official assertions in the credential correspond to `ATTEST`-style content
- limits on use, status, expiry, suspension, or revocation correspond to associated restrictions or termination-style events
- verifier acceptance corresponds to recognition under policy

Like W3C VCs, mDLs are usually not transferable in the commercial sense.

That makes them a narrower subclass within the broader OpenETR model rather than a complete expression of its transfer-oriented capabilities.

## Key Difference

The key distinction is that:

- W3C VC and mDL models are usually claim-centric
- OpenETR is event-chain-centric and control/evidence-centric

In a VC or mDL system, the primary question is often:

> What claims does this credential make, and should the verifier rely on them?

In OpenETR, the broader question may be:

> What is the object, what events have occurred in its lifecycle, what restrictions or assertions attach to it, and should the resulting evidence chain be recognized?

This is why VC and mDL fit well as specialized instances but do not exhaust the OpenETR model.

OpenETR is also not concerned with the specific substantive validity of the document in the legal or institutional sense.

It is concerned with:

- the existence of the record
- the signed event history associated with it
- the control or presentation conditions attached to it
- the evidence available for later recognition

Whether the document is valid, effective, enforceable, or otherwise entitled to recognition remains a recognition-layer question.

## Practical Value of the Comparison

This comparison is useful because it shows that OpenETR is not limited to shipping or classic documents of title.

It can also support reasoning about:

- identity-like credentials
- presentation rights
- restrictions on use
- non-transferable records
- digitally issued evidence objects more generally

That, in turn, helps position OpenETR as a broad model for signed digital records and their recognition rather than as a narrow transport-only protocol.

## Limits of the Comparison

This note does not claim that:

- every VC is automatically an OpenETR record
- every mDL implementation should be rebuilt using OpenETR
- OpenETR is a substitute for the detailed technical specifications governing VC or mDL ecosystems

The point is conceptual and architectural.

VC and mDL can be understood as narrower, more specific patterns that fit inside a generalized OpenETR way of thinking about digitally issued records, associated assertions, and policy-based recognition.

## Summary

W3C Verifiable Credentials and mobile driver's licenses may be understood as specialized, claim-centric instances of the broader OpenETR model.

OpenETR generalizes beyond them by supporting richer lifecycle events, control logic, restrictions, encumbrances, redemption, and termination across many categories of electronic records.
