# OpenETR Overview

OpenETR is a protocol for deriving consequential state from end-verifiable
evidence concerning durable electronic records.

If this is your first encounter with OpenETR, start with one practical
question: **how can another party determine what happened to a digital record
without having to trust the application displaying it?** OpenETR answers by
keeping the identifiable content, the signed evidence, the derived state, and
external recognition separate.

![OpenETR model showing Digital Artifact, Digital Controllable Record, Consequential State, Digital Original, Recognition and Effect](../assets/images/openetr-model.png)

It is not limited to warehouse receipts. The Warehouse Receipts workspace is the first focused domain adapter, and the Product Passports workspace is the next domain surface. The underlying OpenETR model is intended to support Digital Artifacts such as bills of lading, certificates, credentials, secured finance records, product data artifacts, and other electronic transferable records.

The model can be read from left to right:

```text
Digital Artifact -> Digital Controllable Record -> Consequential State -> Digital Original

Consequential State -> Recognition -> Effect
```

OpenETR calls the identifiable content a **Digital Artifact**. It calls the
signed evidence a **Digital Controllable Record (DCR)**. A DCR may be one
independently verifiable signed record or a graph of related records containing
evidence of consequential actions. Consequential state is what follows when
validated evidence is evaluated according to defined protocol rules. A Digital
Artifact for which consequential state has been established through a DCR is a
**Digital Original**.

> Cryptography validates the evidence. Protocol rules determine what follows.

The DCR is not the file, and the word “controllable” does not automatically
give it legal status. Legal recognition remains a separate question.

For a complete worked example, see the [English Gutenberg reconstruction in
the Digital Originality
brief](../policy-briefs/digital-originality.md#concrete-example-an-english-gutenberg-reconstruction).

## How The Implementation Fits

```text
Domain adapters       Warehouse Receipts, Product Passports, bills of lading, credentials
OpenETR protocol      DCR evidence, state transition rules, consequential state
Nostr event substrate signed events, kinds, tags, relays, event ids
Outside the protocol  recognition by law, contracts, registries, and institutions
```

OpenETR sits in the middle. It turns domain actions, document identities, control assertions, and evidence links into signed protocol evidence without forcing every domain to share the same user interface, vocabulary, statute, or business process.

## What OpenETR Provides

OpenETR defines:

- digest-addressed Digital Artifacts;
- Digital Controllable Records made of signed end-verifiable events;
- state transition rules for deriving state from DCR evidence;
- Anchor records that begin candidate DCRs;
- control events for transfer, encumbrance, discharge, redemption, termination, and attestation;
- linked evidence records for supporting documents and lifecycle evidence;
- profile-backed signing;
- object-centric relay queries;
- control graph traversal;
- verifier policy warnings;
- CLI, JSON, Python component, and webapp integration surfaces.

## What OpenETR Does Not Decide

OpenETR does not, by itself, decide:

- legal title;
- protected-holder status;
- warehouse licensing;
- KYC status;
- registry recognition;
- statutory effect;
- priority among competing claims.

Those are recognition questions. OpenETR preserves durable signed evidence and
derives consequential state according to defined protocol rules. Recognition
outside the protocol determines the effect given to that state.

## Source Specs

- [Controllable Records Taxonomy](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROLLABLE_RECORDS_TAXONOMY.md)
- [Digital Controllable Record](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
