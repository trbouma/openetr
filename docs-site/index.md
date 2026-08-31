# OpenETR

**OpenETR helps people know that an important digital record is the one they
intend to rely on, what has happened to it, and what state it is in—even when
they cannot depend on the application that created it.**

It does this by giving the underlying Digital Artifact a durable,
independently verifiable basis for state.

A digital file can be copied perfectly. That is useful, but the file alone
cannot tell us who made a consequential statement about it, what has happened
to it, or which state should now be relied upon.

This matters for warehouse receipts, bills of lading, permits, certificates,
product passports, health records, photographs, and many other records that
people and institutions act upon.

OpenETR addresses the problem without making one application, database,
registry, or wallet the permanent source of truth. It identifies the exact
content, preserves signed evidence concerning it, and applies a Consequential
State Machine so another conforming system can derive the same state.

<figure class="openetr-model-figure">
  <img src="assets/images/digital-artifact-to-digital-original.svg" alt="The OpenETR model showing a Digital Artifact, its Digital Controllable Record, policy validation producing consequential state, a Digital Original, and recognition and effect">
  <figcaption>
    The OpenETR model separates content, signed evidence, derived state, and external recognition.
  </figcaption>
</figure>

## Three Constructs And One Decisive Evaluation

### Digital Artifact

The **Digital Artifact** is the exact content: a PDF, image, data file, media
file, or canonical data package. A cryptographic fingerprint identifies its
bytes. An altered file has a different fingerprint.

### Digital Controllable Record

The **Digital Controllable Record (DCR)** is the signed evidence concerning
that artifact. It may be one end-verifiable record or a graph containing an
Anchor and later lifecycle records such as transfer, encumbrance, discharge,
attestation, redemption, or termination.

The DCR is not the file. It is the portable record of consequential statements
made about the file.

### Consequential State Through The CSM

Consequential State is not another record or container. It is the result of
validating a DCR—or its graph of related records—in relation to an applicable
policy through the OpenETR **Consequential State Machine (CSM)**. The result
says what state has been established: for example, who the candidate current
controller is, whether the artifact is encumbered, or whether its active
lifecycle has ended.

The DCR records the consequential actions. The CSM determines their
consequences.

Consequential State is what an external authority, registry, institution, or
relying party can recognize and give practical effect. Recognition does not
add another event to the DCR. It accepts the result of policy validation for a
particular purpose and determines what legal, institutional, commercial, or
operational effect follows.

### Digital Original

A **Digital Original** is the Digital Artifact once consequential state has
been established by validating its DCR under an applicable policy.

Originality does not belong to one physical copy. Identical copies represent
the same artifact and can be checked against the same DCR and state.

The complete path is:

```text
content -> Digital Artifact
        -> Digital Controllable Record spanning its signed lifecycle

DCR + applicable policy -> CSM validation -> consequential state
consequential state -> recognition and effect
artifact + established consequential state -> Digital Original
```

## A Simple Example

A warehouse issues a PDF receipt for stored grain. Its fingerprint identifies
the Digital Artifact. The warehouse signs an Anchor record, and a later signed
record transfers control to a buyer. Those records form the candidate DCR.
OpenETR validates the evidence and derives the candidate current-controller
state.

Emailing another copy of the PDF does not transfer the receipt. Editing the PDF
creates a different artifact. Changing its consequential state requires valid
signed evidence.

A bank, registry, court, or trading partner then decides whether to recognize
the signers and resulting state. OpenETR preserves the evidence and derives
protocol state; it does not claim that cryptography alone creates legal or
commercial effect.

## Start Here

| Area | Purpose |
| --- | --- |
| [The Core Model](policy-briefs/digital-artifact-dcr-digital-original.md) | Read how Digital Artifacts, DCRs, policy validation, consequential state, and Digital Originals fit together. |
| [Digital Originality](policy-briefs/digital-originality.md) | Explore consequential state and the model through detailed examples. |
| [OpenETR Overview](openetr/index.md) | Continue into the architecture, wire format, implementation surfaces, and recognition boundary. |
| [Warehouse Receipts](getting-started.md) | Work with warehouse receipt documents using MLWR-style terminology over the OpenETR control layer. |
| [Product Passports](product-passports.md) | Start modelling Product Passport control records for product data, compliance evidence, and lifecycle attestations. |
| [Health Records](health-records.md) | Placeholder for future health-record control graph workflows, with privacy and consent concerns called out early. |
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
| Digital Artifact | Persistent content, such as a document or data artifact, identified by digest. |
| Digital Controllable Record | One end-verifiable record or a graph of related records concerning a Digital Artifact. |
| Consequential State | The result of validating a DCR or DCR graph in relation to an applicable policy; it is the state that may be recognized and given effect. |
| Control Record | A signed OpenETR lifecycle record within a DCR. |
| Linked Evidence Record | A signed record that associates another document, artifact, or evidence item with a Digital Artifact without necessarily transferring control. |
| Control Graph | The linked control-event portion of a DCR. |
| Evidence Graph | The broader DCR graph, including Anchor, control, and linked-evidence records. |
| Digital Original | A Digital Artifact for which Consequential State has been established by validating its DCR under an applicable policy. |
| Domain Workspace | A user-facing adapter that speaks domain language while using the same OpenETR control layer underneath. |
| Recognition Layer | Law, registry policy, institutional rules, verifier policy, or contracts that decide whether consequential state is accepted and what effect it receives. |

## Core Thesis

OpenETR does not try to become each domain's system of record, registry, legal authority, or compliance engine.

Instead, it provides a thin signed control layer that produces durable evidence:

```text
real-world object, product, document, or record
  -> canonical file or data artifact
  -> Digital Artifact identified by digest
  -> Digital Controllable Record containing an Anchor and later records
  -> validation of the DCR under an applicable policy produces consequential state
  -> Digital Original
  -> durable query link and QR code
  -> verifier / registry / authority / relying party decides effect
```

The artifact content can stay with the operator, manufacturer, registry,
platform, or storage service. OpenETR preserves its cryptographic identity and
portable DCR evidence.

OpenETR does not decide universal effect. It preserves durable signed evidence,
supports policy validation of the DCR, and exposes consequential state that a
recognition layer can accept and give effect.

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
