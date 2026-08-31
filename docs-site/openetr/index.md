# OpenETR Overview

OpenETR is a general control layer for durable electronic records.

It is not limited to warehouse receipts. The Warehouse Receipts workspace is the first focused domain adapter, and the Product Passports workspace is the next domain surface. The underlying OpenETR model is intended to support Digital Artifacts such as bills of lading, certificates, credentials, secured finance records, product data artifacts, and other electronic transferable records.

The protocol construct is the **Digital Controllable Record (DCR)**: one
end-verifiable record or a graph of related records concerning a Digital
Artifact. Valid DCR evidence and protocol rules derive consequential state and
make the artifact a Digital Original. This protocol term is not automatically
synonymous with a legally recognized controllable electronic record.

## Layered Model

```text
Domain adapter         Warehouse Receipts, Product Passports, bills of lading, credentials
OpenETR control layer  Digital Artifacts, DCRs, profiles, derived state
Nostr wire format      signed events, kinds, tags, relays, event ids
Recognition layer      law, contracts, registry rules, institutional policy
```

OpenETR sits in the middle. It turns domain actions, document identities, control assertions, and evidence links into signed protocol evidence without forcing every domain to share the same user interface, vocabulary, statute, or business process.

## What OpenETR Provides

OpenETR defines:

- digest-addressed Digital Artifacts;
- Digital Controllable Records made of signed end-verifiable events;
- origin events that bring objects into the scheme;
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

Those are recognition questions. OpenETR provides the control layer and produces durable signed evidence that a recognition layer can evaluate.

## Source Specs

- [Controllable Records Taxonomy](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROLLABLE_RECORDS_TAXONOMY.md)
- [Digital Controllable Record](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
