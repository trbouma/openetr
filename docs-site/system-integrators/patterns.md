# Integration Patterns

OpenETR can be integrated gradually.

An integrator does not need to adopt every surface at once.

## Pattern 1: Behind-The-Scenes Control Layer

The host application keeps its existing interface and workflow.

OpenETR runs behind the scenes when the application performs control-relevant actions:

- issue a record
- transfer control
- accept control
- pledge or encumber a record
- release an encumbrance
- attach evidence
- present or redeem a record
- terminate a record lifecycle

This pattern is the best starting point for most enterprise or domain systems.

## Pattern 2: REST Service Boundary

The host system calls an OpenETR service over HTTP.

Use this when:

- the host system is not Python-based
- multiple systems need a shared OpenETR service
- teams want a clear deployment and security boundary
- APIs are easier to govern than embedded library calls

Read:

- [Integration Model](../openetr/integration.md)
- [Component And CLI](../openetr/component-and-cli.md)

## Pattern 3: Embedded Component

The host application imports OpenETR functionality directly.

Use this when:

- the application wants OpenETR behavior inside its own process
- signing and workflow must be tightly controlled
- the host team wants fewer moving parts
- local event storage or direct relay publication is preferred

The same control model should apply whether OpenETR is embedded or exposed through a service.

## Pattern 4: Proof Bundle Exchange

The host system exports a bundle containing the evidence needed by another party.

A bundle may include:

- object digest
- origin event
- relevant control events
- linked evidence records
- signer/profile metadata
- verifier-policy output
- external registry or platform references

This is useful for system-to-system handoff, bank review, regulatory inspection, litigation support, and offline verification.

## Pattern 5: Relay-Backed Publication

The host system publishes signed OpenETR events to relays.

Relays make the evidence discoverable by object digest and event links.

The host system may still keep its own database, but verifiers can reconstruct the OpenETR graph from signed events rather than depending only on the host application's private state.

Read:

- [Nostr Wire Format](../openetr/wire-format.md)
- [Relay-Backed Configuration Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/RELAY_BACKED_CONFIGURATION_DESIGN_NOTE.md)

## Pattern 6: Domain Adapter

A domain adapter translates business actions into OpenETR control events.

For example:

| Domain Action | OpenETR Pattern |
| --- | --- |
| issue warehouse receipt | origin event |
| pledge receipt to bank | encumbrance event |
| release pledge | discharge event |
| transfer eBL | transfer and acceptance events |
| surrender eBL | redemption or termination event |
| attach inspection report | linked evidence event |

Read:

- [Generic Domain Adapter Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [Warehouse Receipt Pilot Boundary Notes](../warehouse-receipt-pilot.md)
- [Bills of Lading](../bills-of-lading.md)

## Implementation Checklist

- identify the controlled object and canonicalization rule
- decide where content is stored
- define which actions require OpenETR events
- map domain actors to OpenETR profile signers
- define key custody and account binding
- choose embedded, service, relay, or bundle integration
- define verifier policy and warnings
- define how recognition inputs are linked
- test graph reconstruction from signed events alone
