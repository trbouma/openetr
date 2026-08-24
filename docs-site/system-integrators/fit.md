# How OpenETR Fits

OpenETR fits between domain systems.

It is not the system of record for every business fact. It is the signed evidence layer for a controlled record.

## The Integration Shape

Most integrations can be understood as four layers:

```text
Domain system
  users, accounts, documents, workflow, roles, policy

Domain adapter
  maps domain actions into OpenETR event semantics

OpenETR control layer
  digest, origin event, control events, linked evidence, graph

Recognition layer
  legal, registry, institutional, contractual, or verifier decision
```

The domain system remains the place where users work.

OpenETR records the evidence that a verifier may need later, including outside the original system.

## Object-Centric Evidence

OpenETR is object-centric.

It starts with a controlled object:

```text
document, file, JSON artifact, credential, record package
  -> canonical bytes
  -> digest
  -> object id
```

Signed events then attach to that object:

- origin
- transfer
- acceptance
- encumbrance
- discharge
- attestation
- presentation
- redemption
- termination
- linked evidence

This produces a control graph that can be reconstructed from signed events.

The graph is portable because the evidence is tied to the object digest and event signatures, not only to a row in one application database.

## Fit By Domain

| Domain | Host System Owns | OpenETR Adds |
| --- | --- | --- |
| Warehouse receipts | account onboarding, goods records, inventory, facility workflow, financing workflow | signed receipt origin, pledge, release, transfer, redemption, and linked evidence |
| Bills of lading | carrier workflow, shipment data, document presentation, surrender workflow | signed eBL origin, transfer, presentation, surrender, and registry/platform evidence |
| Product passports | product data, supplier portals, compliance workflows | signed lifecycle evidence, component links, attestations, dependency graph |
| Apostille documents | authority workflow, document verification, official records | signed authority evidence and document lifecycle references |
| Trade finance | bank systems, credit policy, payment and settlement | evidence links between controlled records, financing events, pledge status, and discharge |

## What The Verifier Receives

A verifier should be able to receive:

- the controlled object or its digest
- relevant origin and control events
- linked evidence events
- signer/profile references
- domain-adapter interpretation
- verifier-policy output
- warnings for missing, conflicting, or unrecognized evidence

The verifier may receive this as an API response, proof bundle, file package, relay query result, or platform-to-platform exchange.

## Useful Next Pages

- [Integration Patterns](patterns.md)
- [Boundaries And Responsibilities](boundaries.md)
- [Control Layer](../openetr/control-layer.md)
- [Recognition Boundary](../openetr/recognition.md)
