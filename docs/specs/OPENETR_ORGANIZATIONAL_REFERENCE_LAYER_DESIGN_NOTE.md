# OpenETR Organizational Reference Layer Design Note

This note describes how organizational reference layers such as LEI, proto-LEI, local business registries, and related identifier mapping systems can support OpenETR verification.

It is motivated by a practical identity problem:

> OpenETR profile keys can prove which key signed an event, but a verifier often also needs to know which real-world organization that key represents.

## Status

Draft.

## Summary

OpenETR profile keys are cryptographic actors.

They answer:

```text
Which key signed this OpenETR event?
```

An organizational reference layer helps answer:

```text
Which legal entity, organization, branch, authority, or operating unit does this signer represent?
```

The two layers should remain distinct.

```text
OpenETR profile key:
cryptographic event signer

Organizational reference layer:
real-world entity resolution and identifier mapping

Recognition policy:
decision about whether that entity is accepted for the action and domain
```

This means proto-LEI, LEI, and other organizational identifiers should be treated as recognition inputs, not as mandatory OpenETR wire-format dependencies.

## Core Problem

Digital trade relies on many organizational identifiers:

- company registration numbers
- tax identifiers
- VAT numbers
- customs identifiers
- banking identifiers
- procurement identifiers
- platform account ids
- industry registry ids
- LEIs
- proto-LEIs
- DIDs
- domain-specific profile identifiers

Each identifier may be valid in its own context. But a verifier often needs to know whether several identifiers refer to the same organization.

Examples:

- a warehouse operator profile signs an OpenETR origin record
- a bank profile records an encumbrance
- a carrier profile issues an eBL origin event
- a Competent Authority profile attaches Apostille evidence
- a manufacturer profile issues a Product Passport record
- an AI agent signs through an organizational workflow

The OpenETR event signature proves that a key signed the event. It does not, by itself, prove that the key is controlled by the claimed legal entity or that the entity is recognized for the action.

That mapping belongs to organizational reference and recognition layers.

## Design Boundary

OpenETR should preserve a clean boundary.

```text
OpenETR control layer
  object digests, signed events, profile keys, control graphs

Organizational reference layer
  LEI, proto-LEI, business registry ids, local authority ids,
  entity-status data, identifier mappings, entity relationships

Recognition layer
  domain policy, legal authority, registry admission,
  KYC/AML, trust framework rules, relying-party decisions
```

OpenETR should not require one global identifier system.

Instead, it should allow domain adapters and verifier policies to consult reference layers where organizational identity matters.

## proto-LEI And LEI Role

The LEI provides a globally standardized identifier for legal entities where coverage exists.

The proto-LEI concept extends the same general idea toward broader coverage by linking authoritative local registry data into a global reference layer. In that model, the proto-LEI is not meant to replace local registries or the LEI. It acts as a bridge across fragmented identifiers and can later support upgrade or alignment with formal LEI records.

For OpenETR, the useful role is:

```text
profile signer npub
  -> organizational reference claim
  -> proto-LEI / LEI / local registry data
  -> verifier checks authority and status
  -> recognition policy outcome
```

This helps a verifier decide whether a signer should be treated as:

- a recognized warehouse operator
- a recognized carrier
- a bank or secured lender
- a manufacturer or importer
- a Competent Authority
- a registry operator
- a verifier, auditor, or attestor
- a legally existing counterparty

## Relationship To Root And Profile Identity

OpenETR root/profile identity remains operational.

The root organizes an OpenETR environment. Profiles sign operational events.

An organizational reference layer does not change that cryptographic model.

It adds recognition context:

```text
root admin key
  -> manages local OpenETR environment

profile signer key
  -> signs OpenETR event

organizational reference
  -> helps identify the legal entity or organization behind the profile

recognition policy
  -> decides whether that organization is authorized for the action
```

A profile may publish or be associated with multiple identifiers:

- `npub`
- NIP-05 identifier
- DID
- LEI
- proto-LEI
- local company number
- tax id
- registry id
- platform account id

These should be treated as claims or references until verified under policy.

## Suggested Profile Metadata

OpenETR profiles may include organizational reference metadata.

Possible signed profile tags:

- `["lei", "<lei>"]`
- `["proto_lei", "<proto_lei>"]`
- `["company_registry", "<registry_identifier>"]`
- `["company_number", "<local_company_number>"]`
- `["tax_id", "<tax_identifier>"]`
- `["vat_id", "<vat_identifier>"]`
- `["jurisdiction", "<jurisdiction>"]`
- `["legal_name", "<legal_name>"]`
- `["organization_role", "<role>"]`
- `["authority_reference", "<authority_or_registry_reference>"]`

These tags should not be treated as self-validating.

A verifier should ask:

- Did the profile sign this metadata?
- Does an external reference layer confirm the mapping?
- Was the entity active at the relevant time?
- Is the entity recognized for this domain and action?
- Does the selected policy accept this identifier source?

## Event-Level References

Some OpenETR events may also include organizational references where useful.

Potential event tags:

- `["actor_lei", "<lei>"]`
- `["actor_proto_lei", "<proto_lei>"]`
- `["actor_registry_id", "<registry_id>"]`
- `["actor_role", "<domain_role>"]`
- `["authority_reference", "<authority_or_registry_reference>"]`
- `["identity_policy", "<policy_id>"]`

Event-level references should be used carefully.

The signer identity is still the event `pubkey`. Organizational references help a verifier map that pubkey into the recognition context, but they do not replace signature verification.

## Verification Flow

A verifier using an organizational reference layer could follow this sequence.

1. Verify the OpenETR event signature.
2. Identify the event signer profile key.
3. Retrieve profile metadata, local aliases, known-entity records, or signed profile attestations.
4. Extract organizational references such as LEI, proto-LEI, local registry id, or DID.
5. Query or consult an organizational reference layer.
6. Resolve whether the references map to the same legal entity.
7. Check status, jurisdiction, role, and time validity where available.
8. Apply domain policy to determine whether the organization is recognized for the action.
9. Annotate the OpenETR graph with recognition outcome.

The verifier should present:

```text
signature_valid = true
signer_npub = <npub>
organization_reference = <proto_lei_or_lei>
organization_status = active | inactive | unknown | conflicting
domain_authorization = recognized | not_recognized | warning | unavailable
recognition_effect = accepted | warning | manual_review | blocked
```

## Relationship To TRQP

TRQP can be used to query whether an entity is authorized or recognized for an action and resource.

An organizational reference layer can help determine the `entity_id` used in that query.

Example:

```text
OpenETR signer npub
  -> profile metadata includes proto-LEI
  -> verifier resolves proto-LEI to organization
  -> TRQP asks whether organization may issue warehouse receipts
  -> verifier annotates OpenETR event
```

The split is:

- organizational reference layer: who is the entity?
- TRQP or trust registry: is the entity authorized for this action/resource?
- OpenETR: what did the profile key sign about this object?
- verifier policy: what effect follows?

## Relationship To EUDI Wallet And Credentials

Wallet credentials can also support organizational identity and mandate.

For example, a wallet-presented credential may prove that a person or agent is authorized to act for an organization identified by LEI or proto-LEI.

OpenETR can use this as recognition evidence:

```text
wallet credential
  -> proves representative mandate
  -> references organization identifier
  -> OpenETR profile signs object event
  -> verifier checks organization and mandate
```

The credential should not replace the object graph. It helps recognize the actor.

## Domain Adapter Examples

### Warehouse Receipts

An MLWR adapter may require:

- warehouse operator profile key
- organization identifier
- registry recognition as warehouse operator
- authority valid at issuance time

The OpenETR origin event proves the profile signed the receipt origin. The organizational reference layer helps determine whether the profile maps to the recognized warehouse operator.

### Bills Of Lading

An eBL adapter may use organizational references for:

- carrier
- issuing agent
- shipper
- consignee
- bank
- insurer
- port or customs authority

This helps avoid platform-local identity silos when an eBL circulates across systems.

### Apostille Documents

An Apostille adapter may use organizational references for:

- Competent Authority
- notary or certifying official
- e-Register operator
- receiving institution

The reference layer can support authority discovery, but official recognition still depends on Apostille Convention rules, Competent Authority practice, and verifier policy.

### Product Passports

A Product Passport adapter may use organizational references for:

- manufacturer
- importer
- repairer
- recycler
- auditor
- marketplace
- regulator

The reference layer helps link lifecycle evidence to recognized organizations.

## Non-Goals

This design does not require OpenETR to:

- mandate LEI or proto-LEI for all profiles
- replace local business registers
- operate an organizational identity registry
- decide legal existence of an entity
- decide beneficial ownership or control
- perform KYC, AML, sanctions, or onboarding checks
- guarantee that a self-declared identifier is accurate
- collapse signer identity into legal identity
- make organizational recognition a base protocol requirement

## Risks And Caveats

### False Certainty

A matching identifier does not necessarily prove authority for a specific action.

An organization may exist and still not be authorized to issue a particular record, transfer a particular asset, or act in a particular role.

### Time Sensitivity

Entity status changes.

An organization may be dissolved, merged, renamed, suspended, or replaced. Verification should consider the time of the OpenETR event and the time of reliance.

### Branches And Operating Units

Legal entities, branches, subsidiaries, departments, agents, and delegated signers may not map one-to-one.

Domain policy must decide whether the relevant actor is:

- the legal entity
- a branch
- an authorized representative
- a subsidiary
- a platform account
- an automated agent

### Privacy And Commercial Sensitivity

Some organizational relationships may be commercially sensitive.

OpenETR should not require all mappings, ownership structures, or authority chains to be published on public relays.

## Recommended Roadmap

1. Keep OpenETR profile keys as the primary cryptographic actors.
2. Add optional profile metadata fields for LEI, proto-LEI, local registry id, jurisdiction, and legal name.
3. Treat organizational references as verifier-policy inputs, not automatic truth.
4. Define domain-specific identity requirements in domain adapter specs.
5. Allow TRQP, trust registries, EUDI Wallet credentials, known entities, and local registries to use organizational references.
6. Add verifier annotations for resolved, unresolved, conflicting, inactive, or unrecognized organizational references.
7. Avoid making any single organizational reference system mandatory in the base OpenETR protocol.

## Open Questions

- Which profile metadata tags should become standard OpenETR conventions?
- Should organizational reference claims be stored in profile records, event tags, linked evidence, or all three?
- How should time-specific entity status be represented in verifier output?
- Should OpenETR define a standard `organization_reference` object model?
- How should conflicting identifiers be displayed to verifiers?
- Should a domain adapter be able to require LEI or proto-LEI for certain roles?
- How should automated agents acting for organizations be represented?

## References

- [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [OPENETR_TRQP_INTEGRATION_NOTE.md](./OPENETR_TRQP_INTEGRATION_NOTE.md)
- [EUDI_WALLET_AND_OPENETR_DESIGN_NOTE.md](./EUDI_WALLET_AND_OPENETR_DESIGN_NOTE.md)
- Verifiable.Trade, "From Fragmented Identifiers to a Global Reference Layer: The Case for the proto-LEI"

