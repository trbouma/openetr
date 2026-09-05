# Warehouse Receipt Pilot Notes

These pilot notes describe how OpenETR should fit into a warehouse receipt system.

The key boundary is:

```text
The warehouse receipt system is the reliable system.
OpenETR is the correctness protocol between systems.
```

OpenETR should provide portable signed DCR evidence and derive Consequential
State under defined rules. It should not replace the account system, KYC
process, warehouse management system, registry, federation arrangement, or
recognition policy.

## Reliable System Boundary

The reliable system is responsible for the operational environment around the warehouse receipt.

That includes:

- user accounts
- KYC, KYB, AML, sanctions, or registry checks
- legal identity binding
- account roles and permissions
- warehouse operator onboarding
- document generation
- receipt content and storage
- operational authorization
- account security
- business workflow
- audit and compliance records

OpenETR is responsible for the signed DCR evidence and state derivation:

- receipt digest
- Anchor Event
- profile signer
- control events
- prior-event links
- attestations and linked evidence
- Evidence Graph reconstruction
- verifier warnings

## KYC And Accounts

OpenETR does not do KYC.

The host system creates an account tied to a legal identity and decides which account may perform which warehouse receipt actions.

The useful accountability chain is:

```text
legal identity
  -> host-system account
  -> account roles and permissions
  -> OpenETR root/admin identity
  -> operational profile key
  -> signed OpenETR event
  -> warehouse receipt Evidence Graph
```

OpenETR can show that a profile key signed an event. The host system must evidence why that key was associated with a legal account and allowed to act.

## Keys And Profiles

The account context may provide the secure environment for creating and protecting OpenETR keys.

The root/admin identity organizes the OpenETR environment. Operational profile keys sign receipt events.

A pilot may use profiles for:

- warehouse operator
- facility issuer
- finance office
- inventory-control role
- system automation
- emergency recovery

OpenETR records which key signed. The host system records why that key was authorized.

## Federation

Federation is an arrangement between system operators.

OpenETR makes the Evidence Graph portable. It does not make other systems
recognize the graph or its derived state automatically.

Federation rules may need to cover:

- onboarding standards
- account-to-key binding requirements
- accepted profile metadata
- relay or archive infrastructure
- attestation requirements
- verifier policy
- suspension or revocation handling
- dispute resolution
- privacy and data sharing

## Attestation

Attestation fits naturally in OpenETR, but the responsibility for requiring and evaluating attestations remains with the system, federation, registry, or verifier policy.

Attestations may cover:

- warehouse operator status
- account-to-key binding
- receipt artifact
- goods custody
- inspection results
- encumbrance status
- discharge or release
- registry status
- federation membership
- system reliability

OpenETR records signed attestation evidence. Recognition policy decides whether the evidence is sufficient.

## Pilot Goal

The first pilot should demonstrate that:

- a warehouse receipt artifact can be digest-identified
- an account-authorized profile can sign an Anchor Event
- later control events can link to the same object
- account-to-key accountability can be evidenced by the host system
- required attestations can attach to the graph
- a verifier can inspect the graph outside the original system
- recognition decisions remain policy-dependent

## Detailed Design Note

- [MLWR Warehouse Receipt Pilot Boundary Notes](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_WAREHOUSE_RECEIPT_PILOT_BOUNDARY_NOTES.md)
