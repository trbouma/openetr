# OpenETR

## Everything Digital Needs Consequential State

Not every digital file needs consequential state. But whenever people,
institutions, or machines rely on something digital to determine what may or
must happen next, its state becomes consequential.

A warehouse receipt may be active, transferred, encumbered, redeemed, or
terminated. A health record may be final, corrected, superseded, or withdrawn.
An academic record may be issued and later amended. An Apostille may have been
verified against an official register at a particular time. In each case, the
content matters because something follows from it.

OpenETR provides a general way for any digest-identifiable **Digital Artifact**
to become a **Digital Original**. Signed, linked records concerning the
artifact form a **Digital Controllable Record (DCR)**. When that evidence is
validated and evaluated under defined rules, it produces **Consequential
State**.

```text
Digital Artifact
  + Digital Controllable Record
  + Defined Rules
  -> Consequential State
  -> Digital Original
```

The transformation does not make the file uncopyable. It makes the artifact's
consequential history independently verifiable. Identical copies remain the
same digest-identified artifact; copying the bytes does not independently copy
or change its Consequential State.

> Content makes an artifact identifiable. Consequential State makes it an
> original.

Explore the possibilities in your domain:
[Digital Trade](policy-briefs/digital-trade-needs-consequential-state.md) |
[Warehouse Receipts](policy-briefs/warehouse-receipts-need-consequential-state.md) |
[Human Rights](policy-briefs/human-rights-need-consequential-state.md) |
[Health Records](policy-briefs/health-records-need-consequential-state.md) |
[Academic Records](policy-briefs/academic-records-need-consequential-state.md) |
[Apostille Records](policy-briefs/apostille-records-need-consequential-state.md)

## The Application Should Show Its Work

Most digital systems answer consequential questions with an application
assertion: the website says who controls the record, the registry says which
status is current, or the platform says that an obligation has been discharged.
The assertion may be correct, but the application rarely exposes the evidence
and rules that produced it.

OpenETR changes that relationship:

```text
Artifact + Portable Evidence + Defined Rules
  -> independently reproducible Consequential State
  -> application projection
```

Applications and databases remain useful. They can store records, authenticate
users, enforce permissions, coordinate workflows, index evidence, and present
the resulting state. They should not have to be the exclusive reason that
state is believed.

An end-verifiable signed record carries enough evidence for another
implementation to verify its attribution and integrity and determine which
artifact and prior records it concerns. Given the same sufficient DCR evidence,
rules, and evaluation parameters, another conforming implementation should be
able to reproduce the same protocol state without depending on the original
website, service, or database.

This is how OpenETR seeks to **make consequences portable**. It turns
Consequential State from an application assertion into an independently
reproducible result.

The protocol result does not compel universal agreement. A person,
institution, community, contract, authority, or applicable law still decides
whether to recognize the evidence and state for a particular purpose and what
effect to give them.

```text
Consequential State -> Recognition -> Effect
```

> Let the application display the answer. Let the artifact, evidence, and rules
> explain why that answer follows.

## Three Primitives. One Core Concept.

The OpenETR model is deliberately simple. The diagram below shows how three
primitives and one core concept fit together, with recognition and effect
remaining outside the protocol.

<figure class="openetr-model-figure openetr-model-figure--marquee">
  <img src="assets/images/openetr-model.png" alt="OpenETR model showing Digital Artifact, Digital Controllable Record, Consequential State, Digital Original, Recognition and Effect">
  <figcaption>
    Recognition and effect remain outside the protocol.
  </figcaption>
</figure>

## The Problem, Restated

**Copies Are Not the Problem.** Digital content can be copied perfectly, and
that is often useful. The harder problem is determining what constitutes the
Digital Original and what verifiable evidence establishes its consequential
state.

The file alone cannot tell us who made a consequential statement about it,
what has happened to it, or which state should now be relied upon.

This matters for warehouse receipts, bills of lading, permits, certificates,
product passports, health records, photographs, and many other records that
people and institutions act upon.

OpenETR addresses the problem without making one application, database,
registry, or wallet the exclusive authority for state. It identifies the exact
content, preserves end-verifiable evidence concerning it, and applies defined
protocol rules so another conforming system can derive the same state.

Applications may maintain projections of consequential state, but those
projections are not the authority. Applications derive consequential state;
they do not own it.

## Concrete Examples

Once the problem is understood as consequential state rather than copy
prevention, familiar examples become simple.

**Health records.** The problem is not whether a lab report can be copied. It
is whether this exact report is current, who signed it, and what verified
history shows that it was corrected, superseded, or withdrawn.

**Warehouse receipts.** The problem is not whether the receipt PDF can be
copied. It is whether the receipt remains active, who controls it, and whether
it has been transferred, encumbered, redeemed, or terminated.

> A copy reproduces content. It does not reproduce or change consequential
> state.

## Four Questions

These questions extend, in spirit, the [Law Commission of England and Wales's
recognition](https://lawcom.gov.uk/project/digital-assets/) that some digital
assets may exist beyond the traditional personal-property categories of things
in possession and things in action. The [Property (Digital Assets etc) Act
2025](https://www.legislation.gov.uk/ukpga/2025/29) now confirms that a digital
or electronic thing is not excluded from personal-property rights merely
because it is neither. In that spirit, OpenETR uses **digital things** as a
broader protocol description, not as the legal name of the third category or a
claim that every Digital Artifact is property.

**What is the digital thing?** The **Digital Artifact**, identified by a digest.

**What happened concerning it?** The **Digital Controllable Record**, containing
evidence signed by actors.

**What follows?** **Consequential State**, derived according to defined rules.

**What has the digital thing become?** A **Digital Original**, the thing with
consequential state.

The final question sits outside the protocol: **so what?** People,
institutions, systems, and law recognize consequential state and determine what
effect it receives.

> Consequential state should be derived from end-verifiable evidence according
> to defined rules, not merely asserted by applications, databases or
> blockchains.

> Each proof proves only what it proves.

## Three Primitives And One Core Concept

### Digital Artifact

The **Digital Artifact** is persistent digital content with a unique content
identity, normally established by a cryptographic digest. It may be a document,
image, credential, record, data structure, or other identifiable content. It is
the subject of consequential actions.

### Digital Controllable Record

The **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records containing evidence of consequential
actions concerning a Digital Artifact. It may contain an Anchor and later
records such as transfer, encumbrance, discharge, relinquishment, attestation,
redemption, or termination.

The DCR is not the file. It is the portable record of consequential statements
made about the file.

### Consequential State

**Consequential State** is state that follows from consequential actions
according to defined protocol rules. It is not another record or container and
it is not “the validation.” Validation asks whether evidence is authentic,
intact, authorized, and acceptable under the protocol. Consequential State is
what follows when the relevant evidence is evaluated according to the rules.

For example, the resulting state may identify a controller, show that an
artifact is active or encumbered, identify a secured party, or show that its
lifecycle has ended.

> Cryptography validates the evidence. Protocol rules determine what follows.

### Digital Original

A **Digital Original** is a Digital Artifact for which consequential state has
been established through a Digital Controllable Record.

Originality does not belong to one physical copy. Identical copies represent
the same artifact and can be checked against the same DCR and state.

> A copy can reproduce the content. It cannot independently reproduce the
> consequential state.

The complete path is:

```text
Digital Artifact -> Digital Controllable Record -> Consequential State -> Digital Original

Consequential State -> Recognition -> Effect
```

## A Simple Example

A warehouse issues a PDF receipt for stored grain. Its fingerprint identifies
the Digital Artifact. The warehouse signs an Anchor record, and a later signed
record transfers control to a buyer. Those records form the candidate DCR.
Cryptography validates the evidence, and OpenETR rules derive the candidate
current-controller state.

Emailing another copy of the PDF does not transfer the receipt. Editing the PDF
creates a different artifact. Changing its consequential state requires valid
signed evidence.

A bank, registry, court, or trading partner then decides whether to recognize
the signers and resulting state. OpenETR preserves the evidence and derives
protocol state; it does not claim that cryptography alone creates ownership or
other legal or commercial effect.

## Relationship To Mainstay

OpenETR is an adjacent member of the Mainstay product family, not a service in
the default Mainstay runtime bundle. Mainstay applications can preserve and
present artifacts and evidence; OpenETR defines how consequential state is
derived from qualifying evidence. Operators, institutions, communities, and
recognition frameworks remain responsible for policy and effect.

The shared emphasis is practical continuity with clear boundaries: records and
evidence remain understandable across applications and changing conditions,
while cooperation does not require every participant to surrender local
stewardship.

## Start Here

| Area | Purpose |
| --- | --- |
| [OpenETR Axioms](openetr/axioms.md) | Start with the ten foundational propositions and five maxims that define the OpenETR model and its boundaries. |
| [The Core Model](policy-briefs/digital-artifact-dcr-digital-original.md) | Read how Digital Artifacts, DCR evidence, protocol rules, consequential state, and Digital Originals fit together. |
| [Digital Originality](policy-briefs/digital-originality.md) | Explore consequential state and the model through detailed examples. |
| [OpenETR Overview](openetr/index.md) | Continue into the architecture, wire format, implementation surfaces, and recognition boundary. |
| [OpenETR Roadmap](openetr/roadmap.md) | See the prioritized work for verifier results, retrieval coverage, associated evidence, recognition adapters, and domain pilots. |
| [Warehouse Receipts](getting-started.md) | Work with warehouse receipt documents using MLWR-style terminology over OpenETR DCR evidence and state transition rules. |
| [Product Passports](product-passports.md) | Start modelling Product Passport control records for product data, compliance evidence, and lifecycle attestations. |
| [Health Records](health-records.md) | Placeholder for future health-record Evidence Graph workflows, with privacy and consent concerns called out early. |
| [Apostille Documents](apostille-documents.md) | Placeholder for future apostille and legalization document verification workflows. |

## Live App

| Page | Purpose |
| --- | --- |
| [`https://openetr.org/`](https://openetr.org/) | OpenETR Control Desk app with query-only upload flow |
| [`https://openetr.org/warehouse-receipts`](https://openetr.org/warehouse-receipts) | Warehouse Receipts workspace |
| [`https://openetr.org/digital-product-passports`](https://openetr.org/digital-product-passports) | Product Passports workspace |
| [`https://openetr.org/openetr`](https://openetr.org/openetr) | Advanced OpenETR console |
| [`https://openetr.org/docs`](https://openetr.org/docs) | FastAPI-generated API docs |

## Core Vocabulary

| Term | Meaning |
| --- | --- |
| Digital Artifact | Persistent digital content with a unique content identity, normally established by a cryptographic digest. |
| Digital Controllable Record | A single end-verifiable record or graph of related end-verifiable records containing evidence of consequential actions concerning a Digital Artifact. |
| Consequential State | State that follows from consequential actions according to defined protocol rules. |
| Control Record | A signed OpenETR lifecycle record within a DCR. |
| Linked Evidence Record | A signed record that associates another document, artifact, or evidence item with a Digital Artifact without necessarily transferring control. |
| Control Graph | The linked control-event portion of a DCR. |
| Evidence Graph | The broader DCR graph, including Anchor, control, and linked-evidence records. |
| Digital Original | A Digital Artifact for which consequential state has been established through a Digital Controllable Record. |
| Domain Workspace | A user-facing adapter that speaks domain language while using the same OpenETR DCR evidence and state transition rules underneath. |
| Recognition Layer | Law, registry policy, institutional rules, verifier policy, or contracts that decide whether consequential state is accepted and what effect it receives. |

## Core Thesis

OpenETR does not try to become each domain's system of record, registry, legal authority, or compliance engine.

Instead, it preserves durable evidence from which consequential state can be
derived:

```text
real-world object, product, document, or record
  -> canonical file or data artifact
  -> Digital Artifact identified by digest
  -> Digital Controllable Record containing an Anchor and later records
  -> evidence is validated and protocol rules derive consequential state
  -> Digital Original
  -> durable query link and QR code
  -> verifier / registry / authority / relying party decides effect
```

The artifact content can stay with the operator, manufacturer, registry,
platform, or storage service. OpenETR preserves its cryptographic identity and
portable DCR evidence.

OpenETR does not decide universal effect. It preserves durable signed evidence
and derives consequential state according to defined protocol rules.
Recognition outside the protocol determines what legal, institutional,
commercial, or operational effect that state receives.

The same boundary applies to execution. A signed record is attributable
evidence of a statement concerning the Digital Artifact; it is not automatic
proof that an outside operation was authorized or performed. An integrating
system can place OpenETR verification before a protected signing or execution
operation, refuse an ineligible action, and publish evidence of the outcome.
OpenETR makes that evidence portable and the resulting state independently
derivable; the integrating system controls the operation within its own scope.

```text
signing commits evidence
protocol rules derive consequential state
integrating systems control operations
recognition frameworks determine effect
```

## Documentation Tracks

| Track | Audience | Starting Point |
| --- | --- | --- |
| OpenETR | Implementers, protocol reviewers, system integrators | [OpenETR Overview](openetr/index.md) |
| Warehouse Receipts | Warehouse operators, MLWR reviewers, domain integrators | [Warehouse Receipts Overview](getting-started.md) |
| Product Passports | Product, compliance, lifecycle, and supply-chain integrators | [Product Passports Overview](product-passports.md) |
| Health Records | Health data, consent, privacy, and clinical workflow integrators | [Health Records Overview](health-records.md) |
| Apostille Documents | Notarial, legalization, authority, and document verification integrators | [Apostille Documents Overview](apostille-documents.md) |

## Source Specifications

Key source documents:

- [GitHub repository](https://github.com/trbouma/openetr)
- [Specification index](https://github.com/trbouma/openetr/blob/main/docs/specs/INDEX.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OpenETR Nostr Wire Format](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [OpenETR MLWR Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_MLWR_PROFILE.md)
- [MLWR Article Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_ARTICLE_REQUIREMENTS_MAPPING.md)
- [Digital Product Passport Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_PRODUCT_PASSPORT_REQUIREMENTS_MAPPING.md)
