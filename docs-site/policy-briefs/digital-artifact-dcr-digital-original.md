# From Digital Artifact To Digital Original

## The Idea In Plain Language

A digital file can be copied perfectly. That is usually helpful, but it creates
a problem when the file matters.

Imagine a warehouse receipt, birth certificate, inspection report, photograph,
permit, or bill of lading. A copy may display the same information as the file
first issued, but the bytes alone cannot answer:

- Who made a consequential statement about it?
- What has happened to it since then?
- Who, if anyone, can presently act through it?
- Has it been transferred, pledged, revoked, replaced, redeemed, or terminated?
- Which evidence supports the answer?

OpenETR separates this problem into three primitives—the **Digital Artifact**,
the **Digital Controllable Record**, and the **Digital Original**—connected by
one core concept: **Consequential State**.

![OpenETR model showing Digital Artifact, Digital Controllable Record, Consequential State, Digital Original, Recognition and Effect](../assets/images/openetr-model.png)

## 1. The Digital Artifact

The **Digital Artifact** is persistent digital content with a unique content
identity, normally established by a cryptographic digest.

It might be a PDF, image, structured data file, media file, or canonical bundle
of data. OpenETR calculates a cryptographic fingerprint, called a digest, from
the exact bytes. If even one byte changes, the fingerprint changes.

The digest answers a limited but important question:

> Which exact digital content are we talking about?

It does not say who issued the artifact, who controls it, whether it is current,
or whether anyone should trust it. It only gives the content a stable identity.

Several people can hold identical copies with the same digest. They are copies
of the same Digital Artifact, not separate originals.

## 2. The Digital Controllable Record

The **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records containing evidence of consequential
actions concerning the Digital Artifact.

A DCR may be one end-verifiable signed record or a graph of related signed
records. It normally begins with an **Anchor record**, which makes the first
protocol statement about the artifact. Later records may describe events such
as transfer, attestation, encumbrance, discharge, redemption, replacement, or
termination.

The DCR is not the PDF or image. It is the portable record of consequential
statements made about that content.

Each record identifies its signer and links to the relevant artifact and prior
records. A verifier can therefore inspect the evidence without relying solely
on the application or database that originally displayed it.

The word *controllable* does not mean that every DCR is legally transferable or
that OpenETR controls the underlying person, goods, or rights. It means that the
record has a defined protocol lifecycle whose state can be established and
changed through valid signed records.

A DCR is an OpenETR protocol construct. It may satisfy requirements for
recognition as a Controllable Electronic Record, Electronic Transferable
Record, Electronic Trade Document, or another legally recognized record only
where the applicable legal requirements are met.

## Consequential State Is What Follows

Consequential State is state that follows from consequential actions according
to defined protocol rules. It is not a fourth record-like construct and it is
not another name for validation.

Cryptographic and structural validation establishes whether the evidence is
authentic, intact, authorized, correctly linked, and otherwise acceptable under
the protocol. State transition rules then determine what follows. Depending on
the domain, **Consequential State** might indicate:

- the candidate current controller;
- whether the artifact has been issued or activated;
- whether it is encumbered or discharged;
- whether it has been revoked, redeemed, replaced, or terminated; or
- which competing branches or unresolved warnings exist.

Consequential State is not merely a status field stored in one application's
database. Another conforming verifier should be able to obtain the artifact and
DCR, apply the same rules, and independently derive the same result.

> Cryptography validates the evidence. Protocol rules determine what follows.

Actions have consequences. OpenETR represents consequential actions as
end-verifiable events and defines the rules by which those events change
consequential state.

This result is the bridge to the world outside the protocol. A registry,
authority, institution, court, counterparty, or other relying party can decide
to **recognize** the consequential state and give it legal, institutional,
commercial, or operational effect. Recognition does not create another DCR
record. It accepts consequential state for a particular purpose and determines
what follows from accepting it.

## 3. The Digital Original

A **Digital Original** is a Digital Artifact for which consequential state has
been established through a Digital Controllable Record.

This does not make one physical copy of the bytes special. Every exact copy can
be checked against the same digest, DCR, and consequential state. Originality
therefore belongs to the artifact-and-state relationship, not to a particular
device, download, folder, or database row.

In short:

```text
Digital Artifact
  the exact content identified by its fingerprint

Digital Controllable Record
  the signed evidence record or graph spanning the artifact's lifecycle

Consequential State
  what follows according to the rules

Digital Original
  the Digital Artifact with consequential state
```

Or as one continuous pipeline:

```text
content -> Digital Artifact -> Digital Controllable Record

DCR evidence -> validation -> state transition rules -> consequential state
consequential state -> recognition and effect
artifact + established consequential state -> Digital Original
```

## A Simple Example

Suppose a warehouse issues a PDF receipt for stored grain.

1. The PDF's digest identifies the exact **Digital Artifact**.
2. The warehouse signs an Anchor record concerning that artifact.
3. A later signed record transfers control to a buyer.
4. Those linked signed records form the receipt's candidate **DCR** and span
   its evidenced lifecycle.
5. The evidence is validated and OpenETR rules derive the candidate
   current-controller state.
6. The receipt is now a **Digital Original** in the OpenETR sense.
7. A bank, registry, court, or trading partner decides whether to recognize the
   signer, state, and transaction under its own rules.

Emailing another copy of the PDF does not create another receipt or transfer
control. Changing the PDF creates a different artifact with a different digest.
Changing its consequential state requires valid signed evidence, not merely an
edited screen or database field.

## What OpenETR Does Not Claim

OpenETR can validate signed evidence, apply protocol rules, and expose the
resulting consequential state. It does not automatically determine:

- the real-world identity of a signer;
- whether the signer had legal authority;
- whether the underlying statement is factually true;
- whether a law, registry, institution, or counterparty must accept the result;
  or
- what legal or commercial effect follows.

Those are questions of **recognition**. Identity systems, credentials,
registries, contracts, institutional policies, domain rules, and law provide
that surrounding context.

Keeping recognition separate is deliberate. It allows different communities
and institutions to evaluate the same portable evidence under their own
rulebooks without changing the underlying artifact or DCR.

## Significance Of The Model

The model restores something that paper often provided implicitly: a practical
distinction between the information on a document and the consequential record
that people and institutions act upon.

It does so without pretending that digital files cannot be copied and without
making one permanent platform the exclusive authority for state.

The three primitives and the core concept therefore have distinct jobs:

| Term | Plain-language purpose |
| --- | --- |
| Digital Artifact | Identifies the exact content. |
| Digital Controllable Record | Preserves the signed evidence concerning it. |
| Consequential State | Describes what follows when validated evidence is evaluated according to the protocol rules. |
| Digital Original | Describes the artifact once consequential state has been established through its DCR. |

That separation is the core of the OpenETR model.

## Read Next

- [Digital Originality](./digital-originality.md) develops the model in greater depth.
- [Why Control Is Not Recognition](./why-control-is-not-recognition.md) explains the external recognition boundary.
- [Provenance Is Not Control](./provenance-is-not-control.md) distinguishes content history from consequential state.
- [Digital Controllable Record Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md) defines the technical construct.
