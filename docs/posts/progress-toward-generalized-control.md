---
title: Progress Toward Generalized Control
eyebrow: Project Update
description: A progress update on the OpenETR protocol, CLI, web app, and the move toward a generalized control layer for multiple legal frameworks.
---

OpenETR has moved from a narrow proof of concept toward a more general protocol shape: a control layer for electronic records that can be interpreted under different legal and institutional frameworks.

That distinction matters. OpenETR is not trying to be a statute, registry, court, or private rulebook. It is trying to provide the signed, inspectable evidence from which those systems can decide whether a record, transfer, encumbrance, discharge, or presentation should be recognized.

The latest implementation work makes that boundary much clearer.

## What changed

The current reference implementation now has a working event family for the core lifecycle of a controlled electronic record.

At the wire level, the model is built around two Nostr event families:

- `kind 31415` for the origin or issue event
- `kind 31416` for later control-relevant events

The `31416` family is no longer treated as only a transfer event. It is now a broader control-event family with explicit action subtypes:

- `initiate`
- `accept`
- `terminate`
- `attest`
- `encumber`
- `discharge`
- `redeem`

That gives the protocol enough vocabulary to represent more of the actual lifecycle of a trade or title-related record.

A record can now be issued, transferred, encumbered, discharged, presented for redemption, and terminated, while preserving a signed event history that can be queried later.

## CLI and web app progress

The CLI now exposes those actions directly.

For example, a profile can issue a warehouse receipt or bill of lading from a local document:

```bash
openetr issue-etr examples/MLWR001.pdf
```

The current controller can initiate a transfer:

```bash
openetr transfer initiate examples/MLWR001.pdf --transferee exporter
```

The transferee can accept:

```bash
openetr profile use exporter
openetr transfer accept examples/MLWR001.pdf
```

The record can also carry encumbrance evidence:

```bash
openetr encumber examples/MLWR001.pdf \
  --beneficiary lender \
  --type pledge \
  --ref encumbrance-MLWR001-001
```

And that encumbrance can later be discharged by reference to the encumbrance event:

```bash
openetr discharge examples/MLWR001.pdf \
  --encumbrance-event <encumbrance_event_id_or_nevent> \
  --releasing-party lender \
  --ref discharge-MLWR001-001
```

The query surface has also become more useful. `openetr query-etr` now shows the origin event, matching control events, lifecycle state, current controller, social profile information where available, and an encumbrance summary.

That means a user can ask a practical question such as:

> Are there any outstanding encumbrances on this record?

and receive a state-oriented answer derived from the signed event history.

The web app uses the same query service, so the browser-based query view can expose the same control state and outstanding encumbrance information.

## Root and profiles

The implementation also now distinguishes between a root administrative identity and operational profile signer identities.

At the Nostr layer, each `nsec` / `npub` pair remains independent. OpenETR does not make profile keys cryptographically subordinate to a root key.

Instead, the root identity organizes the OpenETR environment at the component level, while profiles act as operational signers. A carrier, warehouse, exporter, consignee, bank, or other actor can each be represented by its own profile signer.

This has two useful consequences:

- the signing identity for a record action is explicit
- the component can still help users manage multiple operational roles from one environment

The CLI reflects that distinction:

- `openetr whoami` shows who the user is currently acting as
- `openetr root` shows the administrative root and the profile set it controls

The root may also be a profile, but root and profile are roles rather than different cryptographic key classes.

## The important generalization

The most important design progress is not just that more commands exist. It is that the model has been generalized.

OpenETR is now framed as a Control Layer rather than a single-purpose legal instrument.

The Control Layer answers questions such as:

- What is the controlled object?
- Who signed the origin event?
- Who is the current controller under the evaluated chain?
- What transfer, attestation, encumbrance, discharge, redemption, or termination events exist?
- Which events are linked to which prior events?
- What evidence is available for later recognition?

It deliberately does not answer final legal questions such as:

- Who owns the underlying asset?
- Has title passed?
- Is a security right perfected?
- Which party has priority?
- What legal effect follows in a particular jurisdiction?

Those questions belong to the Recognition Layer.

This separation is what lets the same protocol structure be useful across multiple legal frameworks instead of being locked to one statute, one registry, or one asset class.

## Why this helps with legislation

Different legal frameworks emphasize related but not identical concepts.

MLETR-style regimes focus on reliable methods for identifying an electronic transferable record, preserving integrity, establishing control, and identifying the person in control.

Warehouse receipt frameworks, including MLWR-inspired approaches, care about issuance, transfer, warehouse obligations, protected-holder analysis, security rights, and dealings in receipts.

UCC Article 12 is built around control-oriented treatment of certain electronic records and digital assets.

Digital-asset private-law frameworks such as the UNIDROIT DAPL Principles focus on control, transfer, custody, security rights, and proprietary consequences.

These frameworks are not the same. OpenETR should not pretend they are.

But they all need reliable evidence about electronic records and control-relevant actions. That is the common technical substrate OpenETR can provide.

The generalized model lets an implementation say:

- here is the record identifier
- here is the signed origin event
- here is the signed control history
- here are the parties who acted
- here are the encumbrances and discharges asserted against the record
- here is the redemption or termination state
- here is the evidence a recognition framework can evaluate

The legal framework then decides what effect, if any, follows.

That keeps the protocol modest but useful. It avoids collapsing technical publication into legal effect, while still giving legal and institutional systems better evidence to work with.

## Why the current event family matters

The move from a narrow transfer event to a broader `31416` control-event family is a practical part of that generalization.

A transferable record is rarely only transferred. It may be inspected, pledged, restricted, released, presented, redeemed, or terminated. Some of those actions change control. Some do not. Some may matter only under a particular policy or legal regime.

By carrying the action in an `action` tag, OpenETR can keep the object history queryable while still distinguishing the meaning of each event.

The `o` tag anchors the event to the object. The `d` tag provides the replaceable action slot. The `e` tag links the event into the control graph. Action-specific tags such as `p`, `enc`, `type`, and `ref` add the participants and business references needed by the relevant workflow.

That is enough structure for a reference implementation to publish and query meaningful state today, while leaving room for stricter schemas, policy profiles, and recognition rules later.

## Where this leaves the project

The current work gives OpenETR a clearer bridge between specs and implementation:

- a Nostr wire format for origin and control events
- a minimum shape for implemented control actions
- a CLI walkthrough that maps commands to event shapes
- a root/profile model for operational identities
- query output that derives lifecycle state, controller state, and encumbrance state
- a web query surface that uses the same state evaluation service

The next important work is not to claim legal effect by fiat. It is to keep making the evidence model sharper.

That means improving validation rules, policy profiles, attestation flows, and examples for particular recognition settings such as electronic bills of lading, warehouse receipts, secured finance, and bearer-style redemption.

OpenETR is becoming less about one document type and more about a portable way to express control over electronic records.

That is the useful direction: a small, inspectable protocol layer that lets different legal systems and institutions recognize the evidence they are prepared to recognize, without forcing every record back into a single platform boundary.

