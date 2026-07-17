# MLWR Control Desk

The **MLWR Control Desk** is the warehouse receipt operating surface for OpenETR.

It gives warehouse operators and their counterparties a domain-specific way to issue, query, and manage warehouse receipt control records while keeping the underlying OpenETR protocol general.

## What This Site Covers

This documentation focuses on the MLWR domain adapter:

- how a warehouse receipt document is committed by SHA-256 digest;
- how the webapp translates warehouse receipt actions into OpenETR events;
- how the Control Desk Key, profiles, contacts, and references fit together;
- how verifier policy reads the signed control graph;
- how this work maps to the Model Law on Warehouse Receipts.

The protocol details remain in the OpenETR specs. This site is the domain guide that sits above them.

## Core Thesis

OpenETR does not try to become the warehouse receipt system of record.

Instead, it provides a thin signed control layer:

```text
warehouse receipt document
  -> SHA-256 digest
  -> signed OpenETR origin event
  -> signed control events
  -> verifier policy / recognition layer
```

The receipt content stays with the warehouse operator or integrated system. OpenETR records the cryptographic object identity and the control-relevant event graph.

## Current Product Surface

The demo webapp now opens directly to the MLWR Control Desk:

| Page | Purpose |
| --- | --- |
| `/` | MLWR Control Desk landing page |
| `/openetr` | General OpenETR console |
| `/overview` | OpenETR overview and diagrams |
| `/experimental` | Bitcoin/Taproot/Silent Payments experiments |
| `/docs` | FastAPI-generated API docs |

## Source Specifications

Key source documents:

- [MLWR Webapp Domain Adapter Design Note](https://github.com/trbouma/etrix/blob/main/docs/specs/MLWR_WEBAPP_DOMAIN_ADAPTER_DESIGN_NOTE.md)
- [MLWR Warehouse Operator Issuance Use Case](https://github.com/trbouma/etrix/blob/main/docs/specs/MLWR_WAREHOUSE_OPERATOR_ISSUANCE_USE_CASE.md)
- [OpenETR MLWR Profile](https://github.com/trbouma/etrix/blob/main/docs/specs/OPENETR_MLWR_PROFILE.md)
- [OpenETR Nostr Wire Format](https://github.com/trbouma/etrix/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [MLWR Article Requirements Mapping](https://github.com/trbouma/etrix/blob/main/docs/specs/MLWR_ARTICLE_REQUIREMENTS_MAPPING.md)

