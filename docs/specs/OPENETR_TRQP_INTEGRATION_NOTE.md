# OpenETR And TRQP Integration Note

This note describes how the Trust Over IP Trust Registry Query Protocol (TRQP) can relate to OpenETR.

## Status

Draft design note.

This note is exploratory. It does not make TRQP mandatory for OpenETR implementations. It describes how TRQP can be used as one recognition and authority-query mechanism above the OpenETR signed-event control graph.

## Summary

OpenETR and TRQP address complementary parts of a digital trust architecture.

OpenETR provides:

- cryptographically signed event evidence;
- object identity through document or record digests;
- a control graph of origin and later control events;
- relay-backed publication and retrieval;
- domain adapters such as the MLWR adapter;
- verifier policies that decide how to recognize candidate graph transitions.

TRQP provides:

- a standard read-only protocol for querying trust registries;
- authorization queries;
- recognition queries;
- a PARC-style query model using entity, action, resource, authority, and optional context;
- a bridge between different trust ecosystems and their systems of record.

The architectural fit is:

> OpenETR creates and verifies the signed evidence graph. TRQP can help a verifier decide whether an actor, authority, role, or action should be recognized under a selected governance framework.

TRQP belongs in the OpenETR recognition and verifier-policy layer, not in the base wire format.

## Layer Placement

OpenETR separates:

1. **Evidence layer**: signed Nostr events, event ids, object digests, tags, and graph links.
2. **Control layer**: the OpenETR event grammar and graph model.
3. **Domain adapter layer**: MLWR, bills of lading, transferable records, credentials, or other domain semantics.
4. **Recognition layer**: verifier policies, rule books, registries, authorities, and legal or operational effect.

TRQP fits primarily in layer 4.

It should not be required to publish or retrieve OpenETR events. A verifier should still be able to inspect the OpenETR graph locally if it already has the signed events and the applicable policy.

TRQP becomes useful when the verifier needs to ask questions such as:

- Is this signer authorized to issue this kind of record?
- Is this warehouse profile recognized as a warehouse operator under this framework?
- Is this party recognized as an authority for this resource?
- Does one authority recognize another authority for a particular action and resource?
- Was the authorization valid at the time the OpenETR event was signed?

## PARC Mapping

TRQP uses a Principal, Action, Resource, Context pattern. In the approved TRQP v2.0 specification this is expressed using `entity_id`, `action`, `resource`, `authority_id`, and optional `context`.

The mapping to OpenETR is natural:

| TRQP concept | TRQP field | OpenETR mapping |
| --- | --- | --- |
| Principal | `entity_id` | OpenETR signer profile, signer npub, DID, LEI-linked entity, or profile-controlled actor |
| Action | `action` | OpenETR `action` tag such as `issue`, `initiate`, `accept`, `encumber`, `discharge`, `redeem`, `terminate`, or `attest` |
| Resource | `resource` | Domain resource such as `warehouse-receipt`, `electronic-transferable-record`, `bill-of-lading`, or `mlwr-receipt` |
| Context | `authority_id` plus optional `context` | Governance framework, registry authority, jurisdiction, policy profile, timestamp, locator, document type, or role context |

This mapping lets an OpenETR verifier translate a graph transition into a trust-registry question.

## Authorization Queries

A TRQP authorization query asks whether an authority authorizes an entity to take an action on a resource.

In OpenETR terms, this can be used to evaluate whether a signed event should be recognized as effective under a selected policy.

Example recognition question:

> Did the MLWR authority authorize this warehouse profile to issue warehouse receipts at the time this origin event was signed?

Possible TRQP-style query:

```json
{
  "entity_id": "npub1...",
  "authority_id": "did:web:mlwr.example",
  "action": "issue",
  "resource": "warehouse-receipt",
  "context": {
    "time": "2026-07-12T14:00:00Z",
    "domain": "MLWR",
    "role": "warehouse-operator"
  }
}
```

The OpenETR verifier can then annotate the graph transition:

- authorized and recognized;
- structurally valid but not authorized;
- authorization unknown;
- registry unavailable;
- registry response does not match the selected verifier rule book.

The signed OpenETR event remains visible either way. TRQP affects recognition, not the existence of the signed evidence.

## Recognition Queries

A TRQP recognition query asks whether one authority recognizes another authority for an action and resource.

This is useful for cross-ecosystem OpenETR verification.

Example recognition question:

> Does Authority A recognize Authority B as competent to authorize warehouse operators for MLWR warehouse receipts?

This matters when OpenETR records move across:

- jurisdictions;
- trade platforms;
- registry operators;
- banking networks;
- warehouse receipt systems;
- customs or port systems;
- public and private trust communities.

In this pattern, OpenETR provides the portable graph. TRQP helps discover whether the verifier's chosen authority recognizes the authority behind the signer, registry, or domain rule book.

## OpenETR Verifier Flow With TRQP

A verifier that uses TRQP could follow this sequence:

1. Determine the OpenETR object id from the document digest or supplied object reference.
2. Retrieve origin events using `kind = 1415` and `#o`.
3. Retrieve control events using `kind = 1416` and `#o`.
4. Verify event ids, signatures, required tags, and `e` links.
5. Enumerate candidate control chains.
6. Apply the generic OpenETR verifier policy.
7. Select a domain policy or rule book, such as an MLWR policy.
8. Translate each policy-relevant event into TRQP authorization or recognition questions.
9. Attach TRQP results as policy annotations.
10. Derive the recognized state according to the selected rule book.

The important separation is:

- OpenETR answers: What was signed? By whom? About what object? In what graph relationship?
- TRQP answers: Does a trust registry say this actor or authority is authorized or recognized for this action and resource?
- The verifier policy answers: What effect should the verifier give to the signed event and registry response?

## Relationship To Root-And-Profile Identity

OpenETR root-and-profile identity is an operational identity-management pattern.

The root organizes profile keys, relay-backed configuration, aliases, and profile recovery. Profile keys sign day-to-day OpenETR events.

TRQP can help map those profile keys into a governance context.

For example:

- an OpenETR profile npub signs an `issue` event;
- the profile contains a name, address, LEI, DID, or other structured metadata;
- a verifier maps the profile to a TRQP `entity_id`;
- a trust registry is queried to determine whether that entity is authorized to issue the relevant resource.

The root key itself does not have to be exposed to TRQP. In most integrations, the profile signer is the relevant actor because it is the key that signed the OpenETR event.

The root may still matter operationally if a rule book cares about account administration, profile governance, or how signer keys are managed, but that is a policy choice above the OpenETR wire format.

## Relationship To Domain Adapters

Domain adapters translate domain concepts into the generic OpenETR control model.

For the MLWR domain, examples include:

- warehouse operator;
- holder or controller;
- electronic warehouse receipt;
- transfer of control;
- encumbrance;
- discharge;
- redemption;
- termination.

A TRQP-enabled MLWR adapter can map those domain concepts into TRQP resources and actions.

For example:

| MLWR / OpenETR event | TRQP action | TRQP resource |
| --- | --- | --- |
| `action=issue` by warehouse profile | `issue` | `warehouse-receipt` |
| `action=initiate` by current controller | `transfer` or `initiate-transfer` | `warehouse-receipt` |
| `action=encumber` by secured party or controller | `encumber` | `warehouse-receipt` |
| `action=discharge` by releasing party | `discharge` | `warehouse-receipt-encumbrance` |
| `action=redeem` by holder/controller | `redeem` | `warehouse-receipt` |
| `action=attest` by inspection or custody actor | `attest` | `warehouse-receipt-event` |

The exact vocabulary should be defined by the selected governance framework or domain profile.

## Local-First And Runtime Independence

TRQP should not undermine OpenETR's local-first verification philosophy.

OpenETR is designed so that a verifier can evaluate signed event evidence without depending on the original publisher's running code at time of performance.

A TRQP query may be useful or required by a policy, but it should be treated as an external policy input, not as the source of the OpenETR graph.

Possible operating modes include:

- live TRQP query at verification time;
- cached TRQP responses stored with audit evidence;
- signed authority statements retrieved separately;
- local trust-registry mirror;
- offline verifier rule book with no live TRQP dependency;
- warning-only mode when the TRQP endpoint is unavailable.

The appropriate mode is a policy and assurance decision.

For high-assurance or dispute-sensitive workflows, a verifier may want to store the TRQP response, timestamp, endpoint, authority id, and policy version as part of its audit package.

## Error And Warning Semantics

TRQP results should be surfaced as verifier annotations.

Examples:

| Condition | Suggested OpenETR treatment |
| --- | --- |
| TRQP authorizes the signer | transition may be recognized if other policy rules pass |
| TRQP denies authorization | signed event remains visible; transition is not recognized or is policy-blocked |
| TRQP endpoint unavailable | warning, pending recognition, cached fallback, or policy failure depending on rule book |
| TRQP authority not recognized | warning or policy block |
| TRQP response malformed | warning or hard verifier error depending on whether the response is required |
| TRQP says authorization existed at event time but not now | may still recognize historical event if the policy evaluates at signing time |
| TRQP says authorization exists now but not at event time | likely warning or policy block for historical event |

The generic OpenETR verifier should not hide events because a TRQP check fails. It should show the signed evidence and explain the recognition outcome.

## Implementation Surfaces

OpenETR could integrate TRQP through several surfaces:

1. Python component:
   - add an optional TRQP client module;
   - allow verifier policies to call it while building query results;
   - return structured policy annotations.

2. CLI:
   - add options such as `--policy`, `--trqp-endpoint`, `--authority-id`, or `--resource`;
   - display TRQP authorization and recognition outcomes in `query-etr`;
   - support machine-readable output for automation.

3. Web app:
   - show TRQP authority checks in the control desk;
   - display policy warnings without hiding the underlying signed graph;
   - let users choose a policy or authority context.

4. Domain adapters:
   - define domain-specific action/resource vocabulary;
   - map OpenETR profiles and event tags into TRQP query fields;
   - define how TRQP responses affect recognition.

5. Protocol-level integration:
   - independent implementations can query OpenETR events directly from relays and call TRQP endpoints directly without using the demonstration app.

## Non-Goals

This note does not propose that:

- TRQP replaces OpenETR event signatures;
- TRQP replaces Nostr relays;
- TRQP becomes mandatory for all OpenETR use cases;
- the OpenETR wire format embeds live TRQP responses;
- a TRQP endpoint becomes the source of truth for the OpenETR control graph;
- every verifier must reach the same recognition outcome.

TRQP is best understood as a standard authority-query interface available to verifier policies.

## Design Principle

OpenETR should remain a portable, signed, event-based control layer.

TRQP should be used when a verifier needs a standardized way to ask:

> Who is authorized or recognized to perform this action on this resource under this authority?

Together, they form a clean layered model:

```text
OpenETR signed events
  -> cryptographic graph verification
  -> domain adapter interpretation
  -> TRQP authority / recognition checks
  -> verifier policy outcome
```

This keeps OpenETR general while allowing deployments to plug into formal trust registries where governance, authorization, and inter-ecosystem recognition matter.

## Related Documents

- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [SYSTEM_INTEGRATION_CONSIDERATIONS.md](./SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [OPENETR_LAYERED_ARCHITECTURE_NOTE.md](./OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OPENETR_MLWR_PROFILE.md](./OPENETR_MLWR_PROFILE.md)
- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [ToIP TRQP v2.0 Approved Specification](https://trustoverip.github.io/tswg-trust-registry-protocol/approved/)
