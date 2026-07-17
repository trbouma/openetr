# MLWR Warehouse Operator Issuance Use Case

This note documents the focused warehouse operator use case for OpenETR in an MLWR-style environment.

The goal is to make the first warehouse receipt workflow as simple as possible:

> A warehouse operator issues a warehouse receipt, OpenETR commits to that receipt by digest, and OpenETR control records track later control-relevant actions.

## Status

Design note.

This note is intentionally narrower than a full MLWR profile. It describes the minimum useful workflow for a warehouse operator and the associated design boundaries.

## Product Focus

The primary user is a warehouse operator.

The primary job is:

1. create or obtain a warehouse receipt document;
2. issue an OpenETR origin event for that receipt;
3. create later control records when control-relevant actions occur;
4. let verifiers inspect the signed event graph and apply their own recognition policy.

The receipt may be:

- a PDF;
- an exported record from a warehouse management system;
- a signed document bundle;
- a JSON document;
- a verifiable credential;
- another canonical file or artifact.

OpenETR does not need to parse the receipt contents for this core use case.

## Thin-Waist Model

The warehouse operator profile should use OpenETR as a thin control layer:

```text
warehouse receipt document
  -> SHA-256 digest
  -> OpenETR origin event signed by warehouse operator profile
  -> later OpenETR control events
  -> verifier policy / recognition layer
```

The important protocol facts are:

- which digest identifies the receipt;
- which profile signed the origin event;
- which control events refer to the same digest through `o`;
- how control events link through `e`;
- which participants are named in action-specific tags such as `p`;
- which verifier policy recognizes the resulting graph.

This keeps the warehouse operator workflow small, auditable, and automatable.

## Out Of Scope: Receipt Contents

For this use case, OpenETR should not attempt to understand the detailed contents of the warehouse receipt.

Out of scope for the base OpenETR protocol:

- goods description validation;
- quantity or weight validation;
- grade, quality, or inspection validation;
- warehouse terms and conditions;
- receipt form compliance;
- local statutory content requirements;
- warehouse licensing or bonding requirements;
- KYC or AML checks;
- whether the warehouse actually holds the goods;
- whether the receipt has legal effect under a particular enactment.

Those issues may be essential to a real warehouse receipt system, but they belong to the domain system, legal framework, registry, attestor, or verifier policy.

OpenETR's base responsibility is narrower:

> Bind the warehouse receipt artifact to a digest and make the control history signed, retrievable, and inspectable.

## In Scope: Digest And Control Records

The minimum OpenETR issuance evidence is:

- receipt digest;
- origin event id;
- issuer profile public key;
- event signature;
- object tag `o`;
- action tag `action=issue`;
- optional signed metadata tags such as `name`, `size_bytes`, and `digest_generated_at`.

The minimum control evidence is:

- control event id;
- event kind;
- signer public key;
- object tag `o`;
- prior-event link `e`, where applicable;
- action tag;
- participant tag `p`, where applicable;
- action-specific tags such as `enc`, `type`, or `ref`;
- event signature.

The warehouse receipt file itself can remain wherever the warehouse operator or integrated system keeps it.

The verifier only needs the file when it wants to recompute the digest and confirm that the presented artifact matches the OpenETR object id.

## Warehouse Operator Profile

The warehouse operator is expected to act through an OpenETR profile.

In a simple deployment, the operator may use one profile for all issuance.

In a larger system, separate profiles may represent:

- a warehouse facility;
- a tenant;
- a regional office;
- an authorized issuance role;
- a system signer operated by a warehouse management platform.

OpenETR does not by itself decide whether the profile is legally authorized to issue warehouse receipts.

That is a recognition question.

Recognition inputs may include:

- a published profile;
- root-managed `known_entities`;
- KYC or onboarding status in the host system;
- a registry or licensing check;
- TRQP;
- Web of Trust;
- an OpenETR attestation event;
- a contractual network rule book.

## Control Desk Model

For the warehouse receipt application, the user-facing metaphor is the **Control Desk**.

The Control Desk is the workspace where the warehouse operator issues receipts, manages operating identities, addresses external parties, and consults reference sources.

The **Control Desk Key** is the administrative key behind that workspace. Technically, it is the OpenETR root admin identity.

The Control Desk Key is responsible for organizing the OpenETR environment used by the warehouse receipt application. It may manage:

- available warehouse receipt profiles;
- active profile selection;
- contacts for counterparties and other external parties;
- references for recognition sources;
- relay-backed configuration;
- recovery of profile configuration;
- encrypted profile signer material, where supported by the implementation.

The settled vocabulary is:

| Warehouse receipt application term | OpenETR technical term |
| --- | --- |
| Control Desk | MLWR / warehouse receipt operating surface |
| Control Desk Key | Root admin identity |
| Profile | Operational profile signer identity the desk can act as |
| Contact | External party the desk can address or transact with |
| Reference | External recognition, assurance, registry, KYC, assessment, audit, attestation, or policy source |
| Receipt control record | Signed OpenETR origin or control event |

These categories answer different questions:

| Category | Question answered |
| --- | --- |
| Profile | Can this control desk act as this identity? |
| Contact | Can this control desk refer to this external party by a convenient name? |
| Reference | Can this control desk or verifier consult this external source for recognition context? |

A contact is addressable, not controllable. Adding a party as a contact does not mean the Control Desk can sign as that party.

A reference is a source of recognition or assurance evidence. It is not necessarily a party to a receipt transaction, and its presence does not automatically make an event effective. Verifier policy decides how a reference is used.

The Control Desk Key should not be misunderstood as a cryptographic parent key.

Profile keys remain ordinary, independent Nostr keypairs. They are not derived from the Control Desk Key and do not become cryptographically subordinate to it.

The Control Desk Key organizes access to the profile set. Profile keys sign the operational events.

This distinction lets the warehouse receipt application speak in operational terms while preserving the technical OpenETR root/profile model:

```text
Control Desk = workspace / operating surface
Control Desk Key = root/admin identity for the workspace
Profile = identity the desk can act as
Contact = external party the desk can address
Reference = external source the desk or verifier may rely on
Receipt Control Record = signed OpenETR event
```

## Issuance Workflow

The minimal CLI workflow is:

```bash
openetr profile use warehouse
openetr issue-etr examples/mlwr-20260713.pdf
openetr query-etr examples/mlwr-20260713.pdf
```

For automation, the JSON surface can be used:

```bash
openetr issue-etr examples/mlwr-20260713.pdf --json
openetr query-etr examples/mlwr-20260713.pdf --json
```

Expected behavior:

- `issue-etr` hashes the receipt file;
- the active warehouse profile signs an origin event;
- the origin event carries the object digest in `o`;
- the query command reconstructs the object view from origin and control events;
- the result exposes candidate lifecycle and controller state;
- warnings are emitted for policy-relevant issues such as duplicate origin events.

The command should not require OpenETR to read or validate the receipt body.

## Control Record Workflow

After issuance, the warehouse operator or other recognized participants may publish control records.

Common actions include:

| Warehouse receipt action | OpenETR action | Example command |
| --- | --- | --- |
| Transfer control | `initiate` / `accept` | `openetr transfer initiate <receipt-file> --transferee <profile>` |
| Record pledge, lien, or restriction | `encumber` | `openetr encumber <receipt-file> --beneficiary <profile>` |
| Release pledge, lien, or restriction | `discharge` | `openetr discharge <receipt-file> --encumbrance-event <event-id>` |
| Present for delivery | `redeem` | `openetr redeem <receipt-file> --obligor <profile>` |
| Complete delivery or cancel lifecycle | `terminate` | `openetr terminate-etr <receipt-file>` |

These commands create control records about the same digest.

They do not need to parse the warehouse receipt contents.

## Event Data Convention

OpenETR should keep structured protocol and domain data in signed event tags where possible.

For this use case:

- `o` identifies the receipt digest;
- `action` identifies the origin or control action;
- `e` links to the prior event in the control graph;
- `p` identifies an action-specific participant where applicable;
- named tags such as `name`, `size_bytes`, and `digest_generated_at` describe the issued artifact;
- additional domain tags may be used by a warehouse receipt adapter where needed.

The event `content` field should be treated as readable narrative or unstructured context.

Callers should not be required to parse `content` to recover structured receipt data.

## Recognition Boundary

The warehouse operator issuance use case depends on the same boundary as the wider OpenETR model:

```text
OpenETR authenticates signed control evidence.
Domain systems recognize actors and receipt validity.
Verifier policy decides whether the evidence is sufficient.
```

Examples of recognition questions:

- Is the issuer a licensed warehouse operator?
- Does the receipt satisfy local statutory content requirements?
- Is the signer recognized by the platform, registry, or relying party?
- Does the current controller satisfy the applicable holder or entitlement rules?
- Does a transfer require acceptance?
- Does an outstanding encumbrance block transfer or only require disclosure?
- Is KYC required for this actor or transaction?

OpenETR should make the signed evidence visible. It should not hard-code one answer to these recognition questions into the base protocol.

## Practical Value

This use case gives OpenETR a practical starting point.

The warehouse operator does not need to adopt a new all-encompassing warehouse receipt platform. It can keep using its existing document generation, warehouse management, customer, and compliance systems.

OpenETR adds a narrow capability:

- digest the receipt artifact;
- sign issuance;
- publish retrievable control evidence;
- allow later control records to attach to the same object;
- expose the graph to verifiers and integrating systems.

That narrow capability is enough to demonstrate electronic control without turning OpenETR into a warehouse receipt content management system.

## Design Decision

For the current MLWR focus:

```text
Prioritize the warehouse operator issuance workflow.
Treat the warehouse receipt as an opaque artifact committed by SHA-256 digest.
Use OpenETR events to record issuance and control history.
Leave receipt content validation and legal recognition to domain systems and verifier policies.
```

This keeps the first product path simple, testable, and aligned with the generalized OpenETR control layer.

## Related Documents

Use these documents to follow the model from the warehouse operator use case into the underlying OpenETR design.

| Topic | Document |
| --- | --- |
| Broader MLWR profile | [OPENETR_MLWR_PROFILE.md](./OPENETR_MLWR_PROFILE.md) |
| Control Desk identity vocabulary | [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md) |
| MLWR webapp domain adapter | [MLWR_WEBAPP_DOMAIN_ADAPTER_DESIGN_NOTE.md](./MLWR_WEBAPP_DOMAIN_ADAPTER_DESIGN_NOTE.md) |
| Nostr event wire format | [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md) |
| CLI command mapping | [OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md](./OPENETR_CLI_IMPLEMENTATION_WALKTHROUGH.md) |
| Machine-readable CLI output | [OPENETR_CLI_JSON_MODEL.md](./OPENETR_CLI_JSON_MODEL.md) |
| Generic verifier and recognition policy | [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md) |
| KYC as an application-level recognition concern | [OPENETR_GENERIC_VERIFIER_POLICY.md#kyc-as-a-recognition-concern](./OPENETR_GENERIC_VERIFIER_POLICY.md#kyc-as-a-recognition-concern) |
| System integration approach | [SYSTEM_INTEGRATION_CONSIDERATIONS.md](./SYSTEM_INTEGRATION_CONSIDERATIONS.md) |
| Regular event kind migration | [REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md](./REGULAR_EVENT_KIND_MIGRATION_DESIGN_NOTE.md) |
| ZK-SNARK decision rationale | [ZK_SNARKS_AND_HASH_COMMITMENTS_DESIGN_NOTE.md](./ZK_SNARKS_AND_HASH_COMMITMENTS_DESIGN_NOTE.md) |
