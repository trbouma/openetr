---
title: A Clear Boundary Between Control And Recognition
date: 2026-07-12
eyebrow: Project Update
description: How OpenETR keeps the control graph separate from recognition inputs such as TRQP, Nostr Web of Trust, attestations, and institutional policy.
---

One of the most important design boundaries in OpenETR is the line between **control** and **recognition**.

OpenETR is focused on control evidence. It creates a signed, inspectable graph of events around a controlled object. A verifier can ask:

- what object is this about?
- which event created the origin record?
- which signed events reference the object?
- how do the events link through exact prior-event references?
- which profile signed each event?
- what candidate lifecycle or controller state can be derived from the graph?

That is already a powerful substrate. But it is not the whole story.

The fact that a key signed an event does not, by itself, answer every legal, institutional, or commercial question. It does not prove that the signer was a recognized warehouse operator, that a secured lender's release should be accepted, that an attestor is credible, or that a particular jurisdiction or trading network should give effect to the event.

Those are recognition questions.

## The Control Layer

At the OpenETR layer, the primary job is to produce portable evidence.

The current Nostr wire format uses regular event kinds:

- `1415` for origin events
- `1416` for control events

The graph is object-centric:

- `o` finds the object graph
- `e` walks exact prior-event links
- `action` tells the verifier what the node is trying to do

That gives us a durable way to represent issuance, transfer, encumbrance, discharge, redemption, termination, and attestation without forcing every domain to use the same application or legal vocabulary.

OpenETR should be strict about structural facts:

- event ids must verify
- signatures must verify
- object tags must be coherent
- graph links must be traversable
- action-specific tags must be present where required

But after the graph has been verified, the next question is different:

> What effect should this verifier give to this signed evidence?

## The Recognition Layer

Recognition is where policy enters.

A recognition layer may consider:

- law
- contracts
- registry rules
- domain-specific requirements
- enterprise account roles
- local allow lists or deny lists
- attestations
- trust registry responses
- Web of Trust signals

This means two verifiers may inspect the same OpenETR graph and reach different policy conclusions.

One verifier may recognize a transfer because the signer is authorized in a trust registry. Another may treat the same event as warning-only because the signer is outside its community trust graph. A third may require a domain attestation before accepting the state as final.

That is not a protocol failure. It is the expected result of keeping evidence and recognition separate.

## TRQP As Formal Recognition Input

The Trust Registry Query Protocol (TRQP) fits naturally at the recognition layer.

TRQP can answer questions such as:

- is this entity authorized by this authority to perform this action on this resource?
- does this authority recognize another authority for this action and resource?
- was the authorization valid in the relevant context?

In OpenETR terms, a verifier might inspect an `action=issue` event and ask a TRQP registry whether the signing profile is recognized as a warehouse operator for electronic warehouse receipts.

TRQP does not replace the OpenETR event. It does not become the control graph.

Instead, it helps answer whether a structurally valid event should be recognized under a particular governance framework.

## Web Of Trust As Community Recognition Input

Nostr Web of Trust answers a different kind of recognition question.

It can help a verifier understand whether a signer, attestor, relay, or assertion provider is trusted from a particular viewpoint.

That may involve:

- NIP-02 follow lists
- trusted seed sets
- relay hints
- local reputation policy
- NIP-85-style trusted assertions
- community-maintained trust graphs

This is not the same as formal authority. A high Web of Trust score does not prove legal authority, and a low score does not make a signature invalid.

But WoT can be useful for:

- warning about unfamiliar signers
- ranking competing origin events
- selecting trusted assertion providers
- surfacing known attestors
- reducing spam in open publication environments
- helping communities apply their own recognition lens

Again, the OpenETR graph remains the evidence. WoT is an input to the verifier's recognition policy.

## Attestations And Other Inputs

OpenETR itself can also carry recognition-relevant evidence through attestation events.

An `action=attest` event may say that a party has inspected goods, witnessed custody, confirmed a fact, or endorsed some state of the graph. That attestation is itself signed evidence. Whether it is enough for recognition depends on the policy being applied.

This gives OpenETR a useful pattern:

1. Build the signed graph.
2. Verify the graph.
3. Collect recognition inputs.
4. Apply a selected rule book.
5. Show both the evidence and the recognition result.

The verifier should not hide structurally valid evidence just because recognition fails. It should show the signed event and explain the policy outcome.

## Design Significance

This boundary lets OpenETR stay general.

The control layer does not need to become a warehouse registry, court, bank, trade platform, Web of Trust provider, or trust registry. It only needs to provide a durable, portable, verifiable event graph.

Recognition systems can then compete, specialize, and evolve:

- MLWR policies can evaluate warehouse receipts.
- Trade platforms can evaluate bills of lading.
- Banks can apply secured-lending rules.
- Regulators can apply statutory frameworks.
- TRQP registries can answer formal authorization questions.
- WoT systems can provide community trust and reputation signals.

All of them can work from the same underlying OpenETR evidence.

That is the point of the boundary: OpenETR keeps control portable, while recognition remains flexible enough for real legal, commercial, and institutional diversity.

