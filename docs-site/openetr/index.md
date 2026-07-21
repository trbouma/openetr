# OpenETR Overview

OpenETR is a control layer for portable electronic records.

It is not limited to warehouse receipts. The Warehouse Receipts workspace is the first focused domain adapter, and the Product Passports workspace is the next domain surface. The underlying OpenETR model is intended to support other controlled objects such as bills of lading, certificates, credentials, secured finance records, product data artifacts, and other electronic transferable records.

## Layered Model

```text
Domain adapter         Warehouse Receipts, Product Passports, bills of lading, credentials
OpenETR control layer  controlled objects, control records, linked evidence records, profiles, state
Nostr wire format      signed events, kinds, tags, relays, event ids
Recognition layer      law, contracts, registry rules, institutional policy
```

OpenETR sits in the middle. It turns domain actions, document identities, control assertions, and evidence links into signed protocol evidence without forcing every domain to share the same user interface, vocabulary, statute, or business process.

## What OpenETR Provides

OpenETR defines:

- digest-addressed controlled objects;
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

- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
