# Linked Evidence Record Kind Design Note

This note considers introducing a distinct OpenETR event kind for **linked evidence records**.

The motivating use case is Digital Product Passports. A Product Passport may need to reference later documents such as repair reports, refurbishment certificates, recall notices, recycling records, laboratory reports, inspection records, audit certificates, or end-of-life documents. Those documents are important evidence, but they do not necessarily transfer control of the original passport record.

## Proposed Event Kind

| Kind | Name | Status | Purpose |
| --- | --- | --- | --- |
| `1417` | linked evidence record | proposed | Associates another document, artifact, or evidence item with an existing OpenETR graph without changing control state. |

This would sit beside the current working event kinds:

| Kind | Purpose |
| --- | --- |
| `1415` | Origin record for a Controlled Object. |
| `1416` | Control/action record that may affect control state or lifecycle state. |
| `1417` | Linked evidence record that associates supporting evidence with the graph. |

## Core Distinction

`1417` should not be treated as a transfer, termination, pledge, discharge, redemption, or other control action.

It should answer a narrower question:

> Which signed evidence items are associated with this OpenETR object graph, who linked them, and what relationship did they claim?

That makes it useful for domains where a record accumulates evidence over time without behaving like a transferable record.

## Candidate Minimum Shape

A linked evidence record could use:

```json
{
  "kind": 1417,
  "tags": [
    ["o", "<primary_object_digest>"],
    ["linked_digest", "<linked_document_digest>"],
    ["evidence_type", "<evidence_type>"],
    ["name", "<optional_display_name>"],
    ["mime_type", "<optional_media_type>"],
    ["ref", "<optional_url_or_registry_reference>"]
  ],
  "content": ""
}
```

Required tags:

- `o`: the primary OpenETR object digest being annotated or supported;
- `linked_digest`: the digest of the linked evidence document or artifact;
- `evidence_type`: the claimed relationship type.

Optional tags:

- `e`: a prior event id if the evidence is intended to attach to a specific origin, control, or evidence event;
- `name`: display name for the linked artifact;
- `mime_type`: media type of the linked artifact;
- `ref`: URL, registry identifier, storage pointer, or external reference;
- `profile`: domain or policy profile identifier;
- `subject`: optional product id, batch id, serial number, component id, or other domain subject.

## Product Passport Example

For a repair report linked to a Product Passport:

```json
{
  "kind": 1417,
  "tags": [
    ["o", "<passport_digest>"],
    ["linked_digest", "<repair_report_digest>"],
    ["evidence_type", "repair_report"],
    ["name", "repair-report-2026-07-21.pdf"],
    ["mime_type", "application/pdf"],
    ["ref", "https://example.invalid/records/repair-report-2026-07-21"]
  ],
  "content": ""
}
```

A Product Passport verifier could then ask:

- does the linked document digest match the retrieved evidence item?
- did a recognized issuer, repairer, auditor, registry, or authority sign the evidence record?
- is this signer authorized for `evidence_type=repair_report` under the selected Product Passport profile?
- does the linked evidence update the passport, annotate it, supersede prior evidence, or merely provide supporting material?

## Relationship To `1416 action=attest`

The current `1416` event family includes `action=attest`.

There are two possible designs:

| Option | Description | Tradeoff |
| --- | --- | --- |
| Keep linked evidence as `1416 action=attest` | Treat evidence links as a subtype of the existing control event family. | Simpler event registry, but risks mixing control-relevant actions with non-control evidence attachments. |
| Introduce `1417` | Give linked evidence its own event kind and query path. | Cleaner domain semantics, especially for Product Passports, but adds a new event kind and implementation surface. |

The reason to consider `1417` is clarity. Product Passport lifecycle evidence is often not a control action. A distinct kind lets clients query evidence attachments without interpreting them as possible control transitions.

## Recognition And Effect Boundary

`1417` would provide signed protocol evidence only.

It could show:

- a linked evidence document digest;
- the primary object digest it relates to;
- the claimed evidence type;
- the signer that made the association;
- optional references for retrieval or registry lookup.

It would not decide:

- whether the evidence is legally or regulatorily sufficient;
- whether the signer is authorized for that evidence type;
- whether the evidence changes mandatory passport content;
- whether the evidence supersedes earlier information;
- whether a market, regulator, registry, or relying party must accept it.

Those conclusions belong to the relevant Product Passport profile, delegated act, registry rules, authority practice, marketplace policy, or verifier policy.

## Query Behavior

A verifier interested in an OpenETR object would likely query:

1. `kind = 1415` events by `#o` for origin records;
2. `kind = 1416` events by `#o` for control and lifecycle actions;
3. `kind = 1417` events by `#o` for linked evidence records.

If the linked evidence document is stored by digest, the verifier may separately retrieve the linked document by `linked_digest` and verify that its hash matches the event tag.

## Open Questions

- Should `1417` always point to the primary object with `o`, or should it also support linking evidence to a specific event with required `e`?
- Should `linked_digest` be queryable with a single-letter Nostr tag, or is an explicit named tag preferable for readability?
- Should evidence replacement, supersession, or withdrawal be represented by another `1417` evidence record, by `1416 action=attest`, or by a future dedicated action?
- Should `evidence_type` values be generic OpenETR terms, domain-profile terms, or both?
- Should linked evidence records be allowed to carry structured JSON content, or should all machine-readable semantics live in tags and referenced artifacts?
- Should `1417` be limited to non-control evidence, or can it also link evidence supporting a control action such as pledge, discharge, redemption, or termination?

## Current Recommendation

Treat `1417` as a proposed event kind and do not implement it until the Product Passport mapping review clarifies the needed evidence relationships.

The design direction is promising because it preserves the core distinction:

- `1415` creates the original object graph;
- `1416` records control-relevant actions;
- `1417` links supporting evidence without implying transfer of control.
