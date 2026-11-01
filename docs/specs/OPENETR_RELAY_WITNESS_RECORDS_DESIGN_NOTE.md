# Relay Witness Records for OpenETR

*Design note | 31 October 2026 | Experimental implemented convention, non-normative*

The companion [Witness Record Specification, draft 0.1](./OPENETR_WITNESS_RECORD_SPEC.md)
now proposes explicit conformance requirements. This note retains the rationale
and standards roadmap; publication of the draft is not standards adoption.

## Convention and standards status

Witness Records are an **optional extension to relay capabilities and OpenETR
integrations**, carried using existing Nostr events and queries. They are not a
change to Nostr's event envelope, signatures, WebSocket messages or subscription
filters. A witnessing relay additionally acts as an event author; an aware client
interprets its observation-receipt schema. Clients that do not implement the
convention need not interpret those events, and relays remain free to apply their
ordinary admission and retention policies. Protocol compatibility does not mean
that every relay will accept or retain these events.

The extension adds application semantics, not new transport mechanics. It does
not amend NIP-01, NIP-09, OpenETR's normative wire format, or Core Record Ruleset
1.0. Witnessing and append-only retention are separate capabilities: enabling
one does not imply the other.

The kind-1418 allocation, Spurline schema names, version markers and signed-event
commitment are currently an experimental interoperability convention, **not an
approved NIP or normative OpenETR standard**. Implementation and deployment do
not confer standards status. A future relay standard and an optional OpenETR
witness profile could adopt or revise this convention through their respective
review processes; neither outcome is assumed.

## Architectural purpose

A relay can do more than carry someone else's evidence. It can create its own
signed evidence that it observed and cryptographically verified a particular
signed event at a stated time. That testimony can then travel independently of
the relay that produced it.

For OpenETR, the proposed application model is an Anchor Record with zero or
more associated **Witness Records**. Each Witness Record is a relay-signed
observation receipt referencing the exact Anchor Event. Publisher Notices may
have their own Witness Records. Witnessing one event does not witness its
successors, the underlying artifact bytes, or an entire Evidence Graph.

This extends the available evidence without making the relay the authority over
what the underlying assertion means.

## Relationship to the existing ruleset

Section 15 of [Core Record Ruleset 1.0](./OPENETR_CORE_RECORD_RULESET_1_0.md)
explicitly excludes witness records and external time evidence. This proposal
does not alter that boundary, the ruleset's outputs, or the existing
[Nostr wire format](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md).

Applications would run two distinct evaluations:

- The existing ruleset evaluation of anchors, notices, and their qualifying
  relationships.
- A supplementary witness-policy evaluation of observation receipts, supporting
  authorization, and time assertions.

A valid anchor does not become invalid because no Witness Record was retrieved.
A trusted witness does not make an otherwise invalid anchor valid. Any future
ruleset that makes witness evidence a condition of a consequence must specify
and version that dependency explicitly.

Spurline's local implementation supports service commissioning, initial witness
authorization, signed renewal and revocation, and local suspend/resume. Its
experimental receipt profile uses kind 1418 and includes a wire/binding validator
and cryptographic fixture. Spurline now implements automatic receipt issuance.
Oakgate implements optional discovery, signature and exact signed-subject binding
checks, and display alongside anchor evidence. This demonstrates the convention
between these implementations, not universal interoperability or standards
conformance. Full relying-party commissioning, authorization lifecycle, compromise
and clock-policy evaluation remains separate from these cryptographic checks.

The deployed system-clock profile (schema version 3) declares
`clock_basis: "system-clock"`, `clock_accuracy: "unspecified"` and
`clock_uncertainty_ms: null`. It makes an attributable observation-time claim;
it does not establish a bounded-accuracy trusted timestamp. Oakgate also supports
the experimental v1 and v2 receipt profiles and labels clock claims accordingly.

## Roles and trust decisions

| Role | Contribution | Boundary |
| --- | --- | --- |
| Original author | Signs an anchor or notice | Authorship does not establish truth or authority |
| Witness relay | Signs an observation of the exact signed event | Observation is not endorsement or ruleset validation |
| Commissioning authority | Authorizes a particular service key for a witness role and policy | Commissioning is not proof of ongoing correct operation |
| Hosting relay or archive | Makes a subject or receipt available | Hosting a receipt does not make the host its witness |
| Relying party | Selects recognized authorities and evaluates the evidence | Trust is a local policy decision, not conferred by discovery |

The trust path is from a relying party's recognition policy, through the
commissioning authority's signed authorization, to the witness's signed receipt.
The relying party remains responsible for deciding which authority it accepts.

A service commissioning statement that an operator **operates** a relay does
not automatically authorize timestamp witnessing. The additional authorization
must bind the service key, witness role, exact policy, permitted subject kinds,
and validity interval. The operator's private key need not enter the relay.

Even with authorization, acceptance of a time assertion depends on the witness's
clock, key security, and operating practices. A signature proves attribution,
not clock accuracy. A compromised witness key could produce backdated receipts;
commissioning does not remove that risk.

## The observed claim and signature binding

The proposed claim is:

> This witness observed this particular signed event and successfully verified
> its event identifier and signature at the stated observation time.

The receipt must bind the subject signature as well as its event ID. A timestamp
over an event ID alone does not establish that the corresponding signature
existed then: an attacker can precommit unsigned contents and sign them after
later acquiring the author's key.

The proposed Spurline classical profile defines a commitment as:

```text
SHA256(
  ASCII("spurline.observed-signed-event.v1") || 0x00 ||
  decode_hex(subject.id) || decode_hex(subject.sig)
)
```

The decoded ID and signature have fixed lengths of 32 and 64 bytes respectively.
The verifier recomputes the subject ID, verifies the subject signature, and
checks the commitment. Other algorithms require explicitly specified profiles;
this does not automatically cover PQ events.

Under an accepted witness policy, an observation with bounded clock uncertainty
supports the conclusion that the signed event existed no later than the upper
end of the attested observation interval. It does not establish exact creation
time, first publication anywhere, or validity before a deadline without the
additional policy assessment that such a conclusion requires.

## NIP-03 status and the signature-existence distinction

As checked on 31 October 2026, [NIP-03: OpenTimestamps Attestations for
Events](https://github.com/nostr-protocol/nips/blob/master/03.md) is marked
`draft`, `unrecommended`, and `optional`, with a vulnerability warning. Use
**unrecommended** as its precise published status, rather than implying a formal
deprecation or removal. Its kind-1040 format carries an OpenTimestamps proof
whose digest is the referenced event ID.

Under [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md), the event
ID commits to the public key, timestamp, kind, tags and content, but not `sig`.
The following is this design's threat analysis of that distinction, rather than
a quotation of the brief NIP-03 warning:

1. An attacker constructs unsigned event contents naming a target public key
   and obtains an earlier timestamp commitment to the resulting event ID.
2. If the attacker later acquires that private key, it can sign those precommitted
   contents without changing the event ID.
3. The old commitment still matches, but does not prove that the signature
   existed at the earlier time. Treating it as pre-compromise signed evidence
   would therefore be unsound. No hash collision or broken timestamp proof is
   required for this confusion.

This convention instead requires verification of the subject signature and a
domain-separated commitment to **both ID and exact signature**, as specified
above. A signature produced later cannot match an earlier commitment to a
different signature. This addresses the signature-existence binding problem;
it does not prove that the witness actually observed the event when it claims.

A relay-signed receipt is not a Bitcoin-backed OpenTimestamps proof, a repair to
NIP-03, or its standardized successor. Witness honesty, clock policy and key
security remain explicit dependencies. In particular, a compromised witness can
backdate its own signed claim even when the subject binding is correct. Any
future OpenTimestamps integration would need a separately reviewed profile
specifying which signed object is committed and what time conclusion follows.
Existing kind-1040 attestations must not be relabeled as this convention's
signature-bound Witness Records.

## Proposed record and discovery contract

A Witness Record uses experimental regular-event kind 1418, authored by the
witness relay and separate from OpenETR kinds 1415 and 1416. This is a local
selection, not a registry reservation or registered NIP. The
[frozen Spurline profile](https://github.com/trbouma/spurline/blob/main/docs/observation-receipt-v1.md)
defines its encoding and fixture. Kind 1417 remains the separate linked-evidence
proposal; it is not reused for observation receipts.

The proposed record contains:

| Element | Purpose |
| --- | --- |
| Receipt event ID, witness pubkey, and signature | Independently verifiable witness authorship |
| Subject `e` reference | Exact anchor or notice lookup |
| Subject author and kind tags | Discovery hints checked against the subject |
| Schema and signature profile | Explicit interpretation of the receipt |
| Signed-subject commitment | Binding to both subject contents and signature |
| Observation time, issuance time, and uncertainty | Distinguish observation from later receipt publication |
| Live or backfill mode | Avoid implying that an old stored event was witnessed at its original timestamp |
| Policy digest and authorization event ID | Bind the assertion to exact supporting evidence |

The proposed discovery tags are:

```text
["e", SUBJECT_EVENT_ID]
["p", SUBJECT_AUTHOR_HEX]
["k", SUBJECT_KIND_DECIMAL]
["t", "spurline-observation-receipt-v1"]
```

After locating an anchor, an application could query its configured evidence
sources with:

```json
["REQ", "anchor-witnesses", {
  "kinds": [1418],
  "#e": ["<anchor event id>"],
  "limit": 100
}]
```

Substitute the actual ID. This version-neutral query discovers candidate receipts;
clients must check the schema, version-specific tags and exact binding before
interpreting them. The tag example above is for v1; v2 and v3 use their respective
`spurline-observation-receipt-v2` and `spurline-observation-receipt-v3` markers.
The kind filter alone does not establish validity.
Omitting `authors` permits discovery of multiple witnesses; a configured list
can restrict retrieval. Returned records are candidates, not trusted timestamps.
Limits, unavailable relays, and timeouts must remain visible as retrieval scope.

Applications must not insert the receipt's `e` reference into the OpenETR
Publisher Notice chain. It expresses observation, not an OpenETR predecessor
or consequence. Use a separate relationship type in application data models.

## Verification and presentation

For each candidate, independently verify the receipt and subject, match the
subject reference and signature commitment, then resolve the exact witness
authorization, request, commissioning chain, and policy artifact. Verify that
the authorization covers the witness key, role, subject kind, policy, and
relevant observation and issuance interval.

Apply the relying party's recognition and clock policy separately. Report
missing evidence, unsupported profiles, unrecognized authorities, expired
permission, and disputed time assertions without collapsing them into a generic
"verified" badge. Evaluate the signed lifecycle and applicable compromise
evidence; a local current-state check cannot prove globally complete revocation
knowledge.

An application can display an anchor's existing result with a **Witness Records**
section listing witness and commissioning identities, observation time and
uncertainty, signature and authorization findings, trust decision, policy
reference, and receipt ID. This is proposed presentation guidance, not a new
Core Record Ruleset output schema.

An empty result should say **No Witness Records found in the queried sources**.
It does not establish that no relay observed the event or that the anchor is
invalid. A Nostr publication acknowledgment is not a Witness Record.

## Multiple witnesses and portable evidence

Each witness produces its own signed assertion. Deduplicate identical receipts
by event ID while retaining their retrieval sources. Three copies of one
receipt are one witness assertion, not three witnesses.

Group receipts by exact signed-subject commitment and witness key. Preserve
different receipts from the same key, including discrepancies, rather than
counting them as independent witnesses. Distinct keys may still share an
operator, clock, or infrastructure; independence requires a policy assessment.

Different observation times are expected. Do not average them or let a majority
choose a winning OpenETR notice branch. Any policy that selects an earliest
accepted time bound should preserve the individual receipts and explain the
selection. Additional witnesses do not prove global completeness.

A portable evidence package should retain the subject, receipts, exact
authorization and commissioning evidence, policy artifacts, retrieval
observations, and evaluation parameters. A verifier can then check the signed
claims without contacting the original witness, provided the package contains
the necessary evidence. Assessing current revocation or compromise knowledge
may still require additional retrieval. Package integrity does not establish
completeness or ongoing service health.

## Relay extension and safeguards

Automatic witnessing should be opt-in, initially limited to kinds 1415 and
1416, and require independent signature verification even if ordinary relay
checks are relaxed. Persist the subject and durable observation job atomically,
then sign and publish a retained receipt through a retryable outbox. Preserve
its exact event ID across delivery retries. Exclude receipts from automatic
witnessing to prevent loops.

Clock-health failures, absent authorization, queue exhaustion, and signing
failures must not produce fabricated or backdated observations. Existing events
can be witnessed at a new backfill observation time, not silently at their
author-declared creation time. Public status must distinguish relay acceptance,
pending receipt work, and an issued receipt.

Combine this with a disclosed [evidence-retention policy](./OPENETR_EVIDENCE_RETENTION_AND_DELETION_DESIGN_NOTE.md),
not a promise of permanence. Public receipt references can reveal associations;
limit subject kinds and publication destinations and disclose witnessing to
publishers. Operators retain their stated administrative removal powers, which
affect availability rather than automatically reversing a consequential state.

## Proposed next steps

1. Use the frozen experimental receipt profile and fixture for interoperability
   tests; do not advertise its kind as a registered allocation.
2. Integrate signed authorization lifecycle evaluation and compromise assessment
   into relying applications before production use.
3. Exercise Spurline's implemented observation and publication pipeline under
   operational failures and independent interoperability tests.
4. Extend the implemented optional discovery with a separate witness-policy
   evaluator without changing Core Record Ruleset 1.0.
5. Test multiple witnesses, duplicate hosting, missing dependencies, signature
   substitution, clock failures, backfill, crashes, and partial retrieval.

## Possible path to standardization

1. Publish versioned wire profiles, fixtures and negative test vectors, including
   exact-signature binding, unsupported versions and conflicting clock claims.
2. Obtain independent relay and client implementations and review privacy,
   abuse, key compromise, backfill, retention and resource-limit behavior.
3. Propose a relay-facing NIP covering receipt semantics, discovery, algorithm
   profiles, clock declarations and an agreed event-kind allocation. Resolve any
   allocation conflicts explicitly rather than treating 1418 as reserved.
4. Propose an optional OpenETR witness-evidence specification defining attachment
   to anchors/notices, portable evidence packaging and separate verification,
   authorization, recognition and time-policy results.
5. If a future ruleset makes witness evidence consequential, publish a separately
   versioned ruleset with explicit dependencies and missing-evidence behavior.
   Do not silently alter Core Record Ruleset 1.0.
6. Specify migration from experimental receipts to any adopted profile. Preserve
   original signed receipts and their original interpretation; do not relabel
   legacy evidence as conforming to a later standard.

Standardization can define interoperable claims and checks. It cannot make a
witness universally trustworthy or guarantee historical completeness.

Companion Spurline documentation provides the [receipt design](https://github.com/trbouma/spurline/blob/main/docs/automatic-observation-receipts.md),
[operator runbook](https://github.com/trbouma/spurline/blob/main/docs/witness-operator-runbook.md),
and [sample record and client queries](https://github.com/trbouma/spurline/blob/main/docs/openetr-witness-records.md).
The covering [policy brief](../../docs-site/policy-briefs/relays-as-accountable-witnesses.md)
explains the architectural significance.
