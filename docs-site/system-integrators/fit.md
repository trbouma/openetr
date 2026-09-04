# How OpenETR Fits

OpenETR fits between domain systems.

It is not the system of record for every business fact. It is the signed evidence layer for a controlled record.

It can be used before an operation, to provide current DCR state to a host
policy decision, and after an operation, to publish portable evidence of the
result. The host remains responsible for controlling the operation itself.

## The Integration Shape

Most integrations can be understood as four layers:

```text
Domain system
  users, accounts, documents, workflow, roles, policy

Domain adapter
  maps domain actions into OpenETR event semantics

OpenETR control layer
  artifact digest, Anchor record, control records, linked evidence, graph

Recognition layer
  legal, registry, institutional, contractual, or verifier decision
```

The domain system remains the place where users work.

OpenETR records the evidence that a verifier may need later, including outside the original system.

## Proposal, Commitment, And Evidence

An integration should distinguish what was requested, what was permitted, what
was committed, what was executed, and what evidence was published. These may
occur in one transaction, but they are not the same fact.

For a consequential operation, a strong integration pattern is:

```text
host receives a proposal
  -> authenticates the human, service, or agent
  -> evaluates domain policy and current authoritative inputs
  -> queries and verifies the relevant OpenETR DCR
  -> rechecks material conditions at the protected operation
  -> commits or refuses the operation
  -> publishes signed OpenETR evidence of the outcome
  -> independently verifies the resulting DCR state
```

The protected operation might be signing an Anchor, updating a registry,
releasing goods, accepting a transfer, or invoking another system. Each
integration must identify the operation it actually controls.

OpenETR does not claim that publishing an event controls every external path.
It can support that assurance when the host protects its signer or execution
boundary and prevents equivalent ungoverned operations within the declared
scope. The claim should remain bounded to that scope.

## Three Boundaries

| Boundary | Meaning | Primary Responsibility |
| --- | --- | --- |
| Evidence commitment | A key signs an immutable OpenETR statement. | OpenETR signer and wire implementation |
| Protocol consequence | A verifier evaluates DCR evidence and derives consequential state under stated rules. | OpenETR verifier policy |
| Operational or legal effect | A system acts on the state, or a rule book recognizes it. | Host system, registry, institution, contract, or applicable law |

Relay storage sits between publication and retrieval. It does not collapse
these boundaries or make the relay an authority.

## Object-Centric Evidence

OpenETR is object-centric.

It starts with a Digital Artifact:

```text
document, file, JSON artifact, credential, record package
  -> canonical bytes
  -> digest
  -> object id
```

Signed events then attach to that object:

- anchor
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
| Warehouse receipts | account onboarding, goods records, inventory, facility workflow, financing workflow | signed receipt Anchor records, pledge, release, transfer, redemption, and linked evidence |
| Bills of lading | carrier workflow, shipment data, document presentation, surrender workflow | signed eBL Anchor records, transfer, presentation, surrender, and registry/platform evidence |
| Product passports | product data, supplier portals, compliance workflows | signed lifecycle evidence, component links, attestations, dependency graph |
| Apostille documents | authority workflow, document verification, official records | signed authority evidence and document lifecycle references |
| Trade finance | bank systems, credit policy, payment and settlement | evidence links between controlled records, financing events, pledge status, and discharge |

## What The Verifier Receives

A verifier should be able to receive:

- the Digital Artifact or its digest
- relevant Anchor and control records
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
