# OpenETR And Nostr Web Of Trust Integration Note

This note describes how Nostr Web of Trust (WoT) concepts can relate to OpenETR.

## Status

Draft design note.

This note is exploratory. It does not make any Web of Trust algorithm mandatory for OpenETR implementations. It describes how WoT signals can be used as recognition, filtering, reputation, and discovery inputs above the OpenETR signed-event control graph.

## Summary

OpenETR and Nostr Web of Trust address different questions.

OpenETR asks:

- What object is this event about?
- Which key signed it?
- Does the event id verify?
- Does the event carry the required OpenETR tags?
- How does this event link into the object control graph through `e` references?
- What state can be derived by applying a verifier policy?

Nostr Web of Trust asks:

- Which pubkeys are trusted from a particular point of view?
- Which pubkeys are close to a selected seed set?
- Which pubkeys are followed, muted, reported, or otherwise socially signaled?
- Which third-party trust or reputation assertions does the verifier choose to rely on?
- Which accounts, profiles, relays, or events should be ranked, filtered, or treated with caution?

The architectural fit is:

> OpenETR creates and verifies the signed control graph. Nostr Web of Trust can help a verifier decide which signers, profiles, assertions, relays, or graph branches deserve recognition, ranking, filtering, or warning treatment.

WoT belongs in the OpenETR recognition and verifier-policy layer, not in the base OpenETR wire format.

## Nostr Web Of Trust Background

Nostr Web of Trust is not one single standardized algorithm.

The usual starting point is the Nostr social graph, especially NIP-02 follow lists. A kind 3 follow-list event contains `p` tags for followed pubkeys and may include relay hints and petnames. Since kind 3 is replaceable, the latest follow list for a pubkey represents that user's current published social graph.

A WoT system typically:

1. chooses one or more seed pubkeys already trusted by the observer;
2. builds a directed graph from follow lists and optional negative or identity signals;
3. propagates trust or rank through that graph;
4. applies depth, decay, damping, normalization, or cutoff rules;
5. produces scores or classifications used by a client, relay, service, or verifier.

The exact scoring algorithm is not standardized. Two systems may both be valid while producing different scores because they use different seeds, graph depth, relay coverage, decay rules, or treatments of mutes, reports, and identity signals.

NIP-85 Trusted Assertions is also relevant. It gives trusted service providers a way to publish signed computed assertions, including WoT-like scores, as Nostr events. This is useful when computing the graph locally is too expensive or when a verifier wants to rely on a particular assertion provider.

The key lesson for OpenETR is:

> WoT should be treated as viewpoint-dependent evidence or policy input, not as an objective global truth.

## Layer Placement

OpenETR separates:

1. **Evidence layer**: signed Nostr events, event ids, object digests, tags, and graph links.
2. **Control layer**: the OpenETR event grammar and object control graph.
3. **Domain adapter layer**: MLWR, bills of lading, transferable records, credentials, or other domain semantics.
4. **Recognition layer**: verifier policies, rule books, registries, authorities, reputation, and legal or operational effect.

Nostr Web of Trust fits primarily in layer 4.

It may also support retrieval and discovery decisions around layer 1, such as which relays or assertion providers to query first, but it should not be required for structural OpenETR verification.

A verifier should still be able to inspect signed OpenETR events locally when it has the event set and a selected policy. WoT can then influence recognition, confidence, filtering, ranking, or warning annotations.

## How WoT Differs From TRQP

TRQP and Nostr Web of Trust are complementary but distinct.

| Dimension | TRQP | Nostr Web of Trust |
| --- | --- | --- |
| Core question | Is this entity authorized or recognized by an authority? | Is this pubkey trusted, reputable, or close to a trusted social graph from this viewpoint? |
| Source | Trust registry or system of record exposed through TRQP | Nostr social graph, follow lists, reports, mutes, identity signals, or trusted assertion providers |
| Model | Authority / entity / action / resource / context | Seed set / graph / score / assertion / local policy |
| Output | Authorization or recognition response | Score, rank, classification, trust distance, or assertion |
| Governance style | Formal authority and registry oriented | Social, reputational, community, or provider oriented |
| Best OpenETR layer | Recognition policy | Recognition policy, discovery, spam resistance, reputation |

TRQP is a good fit when a verifier needs formal authorization or recognition under a governance framework.

WoT is a good fit when a verifier needs social or reputational context about keys, profiles, relays, assertions, or communities.

They can be used together. For example, a verifier may require formal authorization from a TRQP registry and also use WoT scores to rank unknown attestors, warn about low-trust profiles, or select assertion providers.

## Relationship To Safebox WoT Record Verification

The Safebox `WOT-ATTESTATION-AND-RECORD-VERIFICATION.md` document is a useful concrete implementation reference because it separates several trust signals that are often blended together in casual discussion.

Safebox record verification combines:

1. **Validated**: the record payload parses as a Nostr event and the event signature validates.
2. **Attested By Owner**: the record owner has published a qualifying ownership/control attestation for the current Safebox.
3. **Recognized**: the record owner is reachable from a configured root authority set expanded through first-hop NIP-02 contact-list edges.
4. **Issuer WoT Scores**: configured trusted assertion providers are queried for advisory score tags about the owner.

This maps cleanly to OpenETR's verifier-policy model:

| Safebox signal | OpenETR analogue | OpenETR treatment |
| --- | --- | --- |
| `Validated` | event id, signature, kind, tag, and graph-shape verification | structural / cryptographic verification |
| `Attested By Owner` | OpenETR `action=attest`, domain-specific attestation, or signer control evidence | policy evidence that may affect recognition |
| `Recognized` | selected root, authority, profile, community, or consortium recognition set | recognition-layer policy result |
| `Issuer WoT Scores` | NIP-85-style trusted assertions or local WoT scoring for signer profiles | advisory confidence / ranking / warning input |

The Safebox design reinforces an important OpenETR principle:

> Validity, attestation, recognition, and reputation are distinct facts. A verifier may display them together, but should not collapse them into a single Boolean.

For OpenETR, this suggests that future verifier output should preserve separate fields for:

- structural validity;
- graph continuity;
- current-controller derivation;
- owner/controller/issuer attestation;
- recognition source and provenance;
- WoT score or classification;
- recognition effect under the selected policy.

Safebox's `Recognized By` rendering is also a useful pattern for OpenETR. If a signer is recognized because it appears in a root authority's contact list, the verifier should be able to show which root or authority supplied that recognition path. In OpenETR terms, a policy result should ideally explain:

- which root, seed, authority, or trusted provider was used;
- which pubkey was recognized;
- whether recognition was direct, first-hop, recursive, or provider-asserted;
- whether the result was used as a hard recognition rule or as a display warning.

Safebox's current model is intentionally shallow: configured root authorities plus one layer of kind-3 follow tags. That is not a general recursive WoT traversal, but it is a useful and understandable starting policy. OpenETR can adopt the same posture:

- simple default policies should be explicit and inspectable;
- deeper or weighted graph traversal can be added later as a separate policy;
- NIP-85-style provider scores should remain advisory unless a selected rule book makes them binding;
- attestation checks should be kept separate from recognition checks.

This is especially relevant to OpenETR because the same signed control graph may be viewed in different contexts. One verifier may treat a root-follow recognition path as sufficient for display confidence. Another may require TRQP authorization, an explicit OpenETR attestation, or a domain registry match before recognizing the transition as effective.

## Possible OpenETR Uses

### Signer And Profile Trust

OpenETR events are signed by Nostr pubkeys.

WoT can help a verifier decide how much confidence to place in a signer profile when formal registry data is absent, incomplete, or only part of the policy.

Examples:

- show a warning if an issuer profile has very low WoT score from the verifier's selected seed set;
- rank multiple competing origin events by signer reputation;
- flag newly created or socially isolated profiles for additional review;
- allow a community to recognize attestors that are trusted by its own graph;
- distinguish familiar operational counterparties from unknown pubkeys.

This should not replace signature verification. A low WoT score does not make a signature invalid. It changes recognition or confidence under a selected verifier policy.

### Relay And Evidence Source Selection

OpenETR can retrieve events from relays or local stores.

WoT can help select or prioritize evidence sources:

- prefer relays used by trusted profiles;
- warn when evidence appears only on relays outside the verifier's trust graph;
- use trusted relay operators as discovery hints;
- prioritize profiles' relay hints when looking for related profile or control events.

This is a retrieval policy, not the source of truth. The source of truth remains the signed event data and verifier policy.

### Attestation And Assertion Providers

OpenETR supports `action=attest` events and may later use additional assertion mechanisms.

WoT can help evaluate attestors:

- inspection agents;
- warehouse operators;
- auditors;
- carriers;
- banks;
- customs actors;
- community-recognized observers.

NIP-85-style trusted assertion providers are especially relevant where a third party computes scores or classifications. A verifier can decide which provider keys it trusts, retrieve their signed assertions, and attach those results to OpenETR verification output.

### Spam, Abuse, And Competing Graphs

OpenETR is an open signed-event system. Anyone with a key can publish structurally valid events.

WoT can help keep open publication usable:

- filter obvious spam origins;
- lower the display priority of unknown or low-trust competing origin records;
- mark suspicious control branches;
- require additional evidence for low-trust signers;
- help user interfaces avoid treating all events as equally relevant.

This fits the existing OpenETR verifier-policy philosophy: policy issues should be visible as annotations or warnings, not hidden by silently deleting signed evidence.

### Community Or Consortium Recognition

Different communities can use different trust graphs.

A warehouse receipt network, carrier network, trade finance network, or open-source community could define:

- seed pubkeys;
- trusted assertion providers;
- relay preferences;
- minimum score thresholds;
- warning thresholds;
- special handling for known participants.

This lets communities use the same OpenETR event graph while applying different recognition overlays.

## WoT Inputs

An OpenETR WoT-aware verifier may consider several categories of input.

| Input | Possible role |
| --- | --- |
| NIP-02 follow lists | Base social graph for trust propagation |
| Relay hints in follow lists | Discovery hints for profiles and events |
| Petnames | Local identity context for known counterparties |
| Mutes or reports | Negative trust or warning signals |
| NIP-85 trusted assertions | Signed third-party computed scores or classifications |
| Profile metadata | Name, address, LEI, website, NIP-05, or other identity clues |
| OpenETR aliases | Local operational names for pubkeys |
| Root-and-profile configuration | Organization of local or account-managed signer sets |
| Local verifier rule book | Seed sets, thresholds, and treatment rules |

None of these inputs should override basic OpenETR structural verification.

## WoT Output As Verifier Annotations

WoT results should be surfaced as verifier annotations.

Possible annotation fields:

| Field | Meaning |
| --- | --- |
| `wot_provider` | Local algorithm or assertion-provider pubkey |
| `wot_viewpoint` | Seed set, policy name, or community context |
| `wot_score` | Numeric score where available |
| `wot_rank` | Rank or percentile where available |
| `wot_classification` | Label such as trusted, unknown, low-trust, blocked, or needs-review |
| `wot_basis` | Follow graph, trusted assertion, local list, or mixed evidence |
| `wot_evaluated_at` | Timestamp for the WoT evaluation |
| `recognition_effect` | How the verifier policy used the result |

The verifier should be clear about the viewpoint.

For example:

```text
wot_warning:
  event_id: <event_id>
  signer: <npub>
  viewpoint: bank-consortium-default
  score: 0.12
  classification: low-trust
  recognition_effect: requires manual review
```

Reading a WoT score without knowing the seed set, provider, algorithm, or viewpoint can be misleading.

## OpenETR Verifier Flow With WoT

A verifier that uses WoT could follow this sequence:

1. Determine the OpenETR object id from the document digest or supplied object reference.
2. Retrieve origin events using `kind = 1415` and `#o`.
3. Retrieve control events using `kind = 1416` and `#o`.
4. Verify event ids, signatures, required tags, and `e` links.
5. Enumerate candidate control chains.
6. Apply the generic OpenETR verifier policy.
7. Select a WoT viewpoint, seed set, local trust graph, or trusted assertion provider.
8. Evaluate signer profiles, attestors, relays, or assertion providers using WoT inputs.
9. Attach WoT results as policy annotations.
10. Derive display priority, warnings, or recognized state according to the selected rule book.

The important separation is:

- OpenETR answers: What was signed? By whom? About what object? In what graph relationship?
- WoT answers: How trusted or reputable is this key, event source, attestor, or provider from a selected viewpoint?
- The verifier policy answers: What effect should the verifier give to the signed event and WoT result?

## Relationship To Root-And-Profile Identity

OpenETR root-and-profile identity organizes operational signers.

WoT can evaluate profile keys directly because profile keys sign OpenETR events. In most cases, the profile signer is the relevant WoT subject.

Possible patterns:

- use WoT to identify familiar profile keys in a trade network;
- use root-managed aliases as local seed or allow-list inputs;
- use profile metadata to map pubkeys into a local trust graph;
- treat root keys as administrative trust anchors only where the verifier's rule book cares about root-managed configuration;
- distinguish trust in the root's profile set from trust in any individual operational action.

The root does not make a profile key trusted by graph magic. It organizes the profile set. A WoT-aware verifier still needs a policy for whether and how the root relationship matters.

## Relationship To Domain Adapters

Domain adapters can decide which WoT questions matter.

For the MLWR domain:

- issuer reputation may matter for warehouse operators;
- attestor reputation may matter for inspection or custody claims;
- relay trust may matter for evidence discovery;
- social trust may be useful in demonstrations or open networks;
- formal authorization may still require TRQP or another registry mechanism.

Possible MLWR policy examples:

| Domain question | WoT use |
| --- | --- |
| Is this warehouse profile familiar to my network? | Score the issuer profile from selected seeds |
| Is this attestor credible? | Score attestor profile or trusted assertion provider |
| Which competing origin should be shown first? | Rank by issuer trust and graph continuity |
| Should this unknown signer block recognition? | Treat low WoT as warning, manual review, or policy block |
| Which relays should be queried first? | Prefer relays associated with trusted profiles |

The exact effect should be defined by the selected domain policy.

## Local-First And Runtime Independence

WoT should not undermine OpenETR's local-first verification philosophy.

A WoT-aware OpenETR verifier should support multiple operating modes:

- fully local graph computation from locally available follow lists;
- cached WoT scores;
- signed NIP-85-style trusted assertions;
- hosted WoT provider queries;
- community-maintained seed sets;
- offline rule books with no live WoT dependency;
- warning-only mode when WoT inputs are unavailable.

The selected policy should say whether WoT is:

- required for recognition;
- optional confidence evidence;
- display ranking only;
- spam filtering only;
- manual-review guidance.

If WoT results are used for high-impact recognition, the verifier should preserve the relevant inputs or assertions for audit:

- provider key;
- algorithm or policy identifier;
- seed set identifier;
- score or classification;
- evaluation time;
- source relays or assertion event ids.

## Risks And Cautions

WoT is useful, but it has sharp edges.

Key risks:

- cold start for new users or new organizations;
- popularity bias masquerading as authority;
- opaque scoring algorithms;
- community capture or echo chambers;
- sybil attacks if seed selection is weak;
- stale follow-list data;
- over-reliance on hosted scoring providers;
- privacy leakage from public follow lists or provider preferences;
- confusing global rank with personalized trust.

OpenETR should therefore avoid treating WoT as a universal truth source.

Better framing:

> WoT is a policy input that can improve ranking, warnings, reputation, and community recognition when the verifier understands the viewpoint and limitations.

## Implementation Surfaces

OpenETR could integrate WoT through several surfaces:

1. Python component:
   - add optional WoT scoring or assertion-consumption helpers;
   - expose structured verifier annotations;
   - allow policy plugins to supply seed sets and thresholds.

2. CLI:
   - add options such as `--wot-policy`, `--wot-seeds`, `--wot-provider`, or `--wot-threshold`;
   - show WoT warnings in `query-etr`;
   - support machine-readable output for agents.

3. Web app:
   - show signer trust annotations in the control desk;
   - show when an actor is trusted, unknown, or low-trust under the selected viewpoint;
   - keep signed graph evidence visible even when WoT produces warnings.

4. Domain adapters:
   - define which actors are WoT-relevant;
   - map domain roles to score requirements or warning thresholds;
   - combine WoT with TRQP, local policy, or registry evidence.

5. Protocol-level integrations:
   - independent implementations can query OpenETR events directly from relays and apply their own WoT graph or trusted assertion provider.

## Non-Goals

This note does not propose that:

- WoT replaces OpenETR signatures;
- WoT replaces the OpenETR control graph;
- WoT becomes mandatory for all OpenETR use cases;
- there is one canonical OpenETR trust score;
- OpenETR should standardize one WoT algorithm;
- a low WoT score makes an event cryptographically invalid;
- a high WoT score proves legal authority.

WoT is best understood as a viewpoint-dependent recognition, filtering, and confidence input.

## Design Principle

OpenETR should remain a portable, signed, event-based control layer.

Nostr Web of Trust should be used when a verifier needs a decentralized way to ask:

> From this viewpoint, how much confidence should I place in this signer, attestor, relay, assertion provider, or graph branch?

Together, they form a useful layered model:

```text
OpenETR signed events
  -> cryptographic graph verification
  -> domain adapter interpretation
  -> WoT reputation / confidence signals
  -> verifier policy outcome
```

This keeps OpenETR general while allowing deployments to use Nostr-native trust signals where social reputation, discovery, spam resistance, or community recognition matter.

## Related Documents

- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OPENETR_TRQP_INTEGRATION_NOTE.md](./OPENETR_TRQP_INTEGRATION_NOTE.md)
- [SYSTEM_INTEGRATION_CONSIDERATIONS.md](./SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [OPENETR_LAYERED_ARCHITECTURE_NOTE.md](./OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
- [OPENETR_MLWR_PROFILE.md](./OPENETR_MLWR_PROFILE.md)
- [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [Safebox: WOT-ATTESTATION-AND-RECORD-VERIFICATION.md](https://github.com/trbouma/safebox/blob/main/docs/specs/WOT-ATTESTATION-AND-RECORD-VERIFICATION.md)
- [Nostr Compass: Web of Trust](https://nostrcompass.org/en/topics/web-of-trust/)
- [Nostr Compass: NIP-02 Follow List](https://nostrcompass.org/en/topics/nip-02/)
- [Nostr Compass: NIP-85 Trusted Assertions](https://nostrcompass.org/en/topics/nip-85/)
