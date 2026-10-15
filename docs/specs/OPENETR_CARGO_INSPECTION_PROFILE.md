# OpenETR Cargo Inspection Profile

## Status And Purpose

Draft for review, October 15, 2026. Proposed identifier:
`openetr:cargo-inspection:0.1`. Not an implemented or certified capability.

This profile specializes the [Inspection Evidence extension](./OPENETR_INSPECTION_EVIDENCE_SPEC.md)
and [Core Record Ruleset](./OPENETR_CORE_RECORD_RULESET_1_0.md) for a pilot with
one inspector and one financier, buyer, or insurer. It authenticates report
issuance and supports independent verification, not financing registration,
pledge exclusivity, title transfer, or proof that physical observations are true.

MUST, SHOULD, and MAY apply within this draft profile. Domain rules remain
external to the generic OpenETR protocol. The profile separates reproducible
evidence checks from each relying party's recognition and acceptance policy.

## 1. Primary Artifact And Workflows

The minimum pilot uses the exact issued PDF as the report artifact. Preserve
those bytes; re-rendering creates a different artifact. Canonical structured
records and alternate renditions are future profile versions, not implicit
equivalents of the PDF. The report may remain in existing private delivery
channels. A public download URL and relay-backed decryption keys are not required.

### Artifact Origin And Application Responsibility

The inspector can anchor either **a document they received** or **an inspection
report they created**. These are different assertions, even when the same profile
signs the anchor:

| Artifact origin | Meaning of anchoring | Application behavior |
| --- | --- | --- |
| Received document, such as a manifest or another party's report | The inspector anchors those exact bytes as a reference; authorship and endorsement are not implied. | Preserve the original bytes and distinguish the source from the inspector's later assessment. Do not automatically add the report-issuance declaration. |
| Inspector-created inspection report | Under this profile's explicit declaration, the inspector issues their own assessment. | Finalize the PDF, obtain inspector confirmation, calculate its digest, and sign the issuance evidence. |
| No suitable document yet exists | An artifact must first be created or obtained. | Generate a subject document or inspection PDF from confirmed inputs, or accept an uploaded document, before anchoring. |

In every case, `o` MUST be SHA-256 of the exact artifact bytes, encoded as
64 lowercase hexadecimal characters. The application calculates it; the
inspector does not manually invent it. Neither a cargo number nor an `i` URL
replaces it. Preserve the finalized file for later verification. Editing or
re-rendering it afterward produces a different artifact and digest.

A received document may lack the namespace or scope detail required for a
profile-conforming subject artifact. Do not edit it silently to make it conform.
It may be anchored as a generic record and selected under Flow A with explicit
association checks, or the app may create a separate subject document referencing
the original and preserve both. Generating a document does not establish the
truth of its contents or that a physical inspection occurred.

All three inspection-extension workflows are supported:

| Flow | Signed issuance event | Digest binding |
| --- | --- | --- |
| A: Existing subject anchor | `1416`, `action=inspection`, referencing the selected subject graph. | `o` identifies the subject artifact; mandatory `report_digest` identifies the PDF. |
| B: New subject anchor | Create the subject artifact's `1415` anchor, then publish the same inspection shape as A. | The subject and report digests remain distinct. |
| C: Report first | `1415`, `action=issue`, with the profile declarations below. | `o` and `report_digest` both identify the PDF. No redundant inspection event is required. |

A third party anchoring a copy without the issuance declaration is not an issuer
under this profile. A third party making that declaration is making an attributable
claim, not automatically becoming a recognized inspector.

### 1.1 Subject Anchors Are Not Inspection Reports

A subject anchor created under Flow B MUST conform to the core `1415` anchor
shape and include this profile's `profile`, `subject_ref`, `i`, and `k=web` tags.
It MUST NOT carry `statement=inspection_report_issued` unless its artifact is
actually an issued inspection report, in which case it is Flow C instead.
Section 2's report-issuance requirements apply to the subsequent inspection,
not to the subject-only anchor. The subject artifact MUST describe the reference
namespace, identifiers, and intended scope. Publishing it establishes a signed
reference point, not ownership, exclusive subject identity, or an inspection result.

## 2. Signed Issuance Declaration

The issuance event MUST include exactly one of each tag below, in addition to
the requirements of its event kind and action:

```json
[
  ["profile", "openetr:cargo-inspection:0.1"],
  ["statement", "inspection_report_issued"],
  ["subject_ref", "<canonical_HTTPS_subject_URL>"],
  ["i", "<same_canonical_HTTPS_subject_URL>"],
  ["k", "web"],
  ["inspection_ref", "<absolute_inspection_identifier_URI>"],
  ["report_digest", "<exact_pdf_sha256_hex>"],
  ["observed_at", "<YYYY-MM-DDTHH:MM:SSZ>"],
  ["location_ref", "<absolute_location_identifier_URI>"],
  ["criteria_ref", "<absolute_criteria_identifier_URI>"],
  ["finding", "conforms"]
]
```

By signing this declaration the signer asserts that it issues the identified
report as its inspection assessment of the identified subject, under the stated
criteria, at the declared observation time and location. This meaning applies
only to this profile; it does not redefine generic `action=issue`.

`finding` MUST be `conforms`, `deviations`, or `inconclusive`. It expresses the
inspector's conclusion, not the financier's approval. `observed_at` is a signer
assertion; `created_at` is not independent proof of inspection or publication time.

The PDF MUST state the subject and inspection references, observation scope,
location, criteria, findings, and any sampling or limitations. It SHOULD describe
the physical association (marks, seal numbers, photographs, custody references)
needed to support the claimed scope. The verifier MUST compare the signed summary
with the report, manually if no supported extraction format exists. A digest match
alone does not establish that the fields correspond or that the claims are true.
If comparison cannot be completed, report `unknown`, not a match.

## 3. Subject And Inspection Identity

`subject_ref` identifies goods within an explicit namespace, for example
`https://example.com/cargo-lots/LOT-2026-001`. It is an identifier, not a requirement
to visit that website. The pilot participants MUST agree on its issuer, namespace,
scope, and canonical spelling. This initial profile uses the URL identifier type
from [NIP-73](https://github.com/nostr-protocol/nips/blob/master/73.md): `i` carries
the subject URL and `k=web` identifies its type. It defines no `k=gs1` type and
does not use NIP-39's external-account identity-proof semantics.

For the bounded pilot, agree on an ASCII HTTPS URL with lowercase scheme and
host, no credentials, no explicit default port, and no query or fragment. Use `/` for an
empty path; preserve meaningful path case and trailing slashes. Percent escapes,
where needed, use uppercase hex, with unreserved characters written literally.
Avoid dot segments. Agree on this form before signing; verifiers MUST NOT rewrite
signed tags to make them match. Compare the canonical strings exactly and report
noncanonical values. Different domains and path aliases remain different
identifiers unless an explicit domain mapping is supplied. Hashes of commodity,
quantity, and origin are not accepted as universal cargo identities.

`inspection_ref` identifies one inspection occurrence; a new inspection gets a
new reference. A correction to the report for the same occurrence retains it.
Different parties may claim the same reference; it is not proof of uniqueness.
Record signer keys and event IDs when grouping revisions.

Each issuance covers one subject in this bounded profile. Combined shipments,
splits, merges, and identity aliases require explicit additional mappings in a
future profile or identified policy; do not infer them from similar descriptions.
The report digest, subject reference, and inspection reference answer different
questions and MUST remain separate.

### 3.1 Manual Cargo And Shipment References

Scanning is optional. An inspector MAY enter a cargo or shipment reference
manually, using the same subject-selection and verification workflow. The
application MUST collect or obtain from explicitly selected configuration:

| Input | Requirement | Illustrative value |
| --- | --- | --- |
| Reference type | Required; identifies the numbering scheme's category. | `shipment` |
| Issuer / namespace | Required stable namespace identifier, not just an organization display name. | `https://example.com/namespaces/shipment-references` |
| Reference value | Required string; preserve meaningful leading zeros, punctuation, and case. | `SHIP-2026-00482` |
| Subdivision type and value | Optional pair; identifies the inspected part of the shipment. | `lot`, `LOT-03` |

A standalone cargo-lot reference may use its own namespace and `cargo_lot`
reference type instead of a shipment plus subdivision. A booking or transport
document number MUST NOT silently be treated as a cargo identity: the mapping
must define what subject it identifies and any additional scope required.

Commodity, quantity, origin, marks, and packaging details assist subject
confirmation and belong in the report where relevant. They MUST NOT be silently
hashed or concatenated into a supposedly universal subject identifier. A
reference without a namespace is ambiguous and MUST NOT produce an affirmative
subject match.

### 3.2 Namespace Mapping To The Subject URL

Pilot participants MUST share an identified, versioned mapping from the manual
inputs to the canonical HTTPS subject URL. A mapping defines:

- The reference issuer, namespace identifier, supported reference types, and
  intended subject scope.
- Validation and normalization rules, including any allowed case conversion,
  whitespace treatment, Unicode handling, and preservation of leading zeros.
- A fixed HTTPS base and path template, the encoding of each input component,
  and the permitted subdivision types.
- Handling of identifier reuse, namespace migration, and aliases. If numbers
  repeat over time, the mapping must require enough context to disambiguate them.

Mappings are agreed application configuration or independently accepted domain
data, not instructions to trust merely because an event or website supplies them.
Two implementations using the same mapping and inputs MUST construct the same
URL. Namespace mapping does not prove issuer authority or physical identity.

For example, a mapping named `example-shipment-v1` could map the inputs above to:

```text
https://example.com/shipments/SHIP-2026-00482/lots/LOT-03
```

Its signed subject tags are:

```json
[
  ["subject_ref", "https://example.com/shipments/SHIP-2026-00482/lots/LOT-03"],
  ["i", "https://example.com/shipments/SHIP-2026-00482/lots/LOT-03"],
  ["k", "web"]
]
```

The example's template is `/shipments/{reference}/lots/{lot}` when a lot is
supplied, and `/shipments/{reference}` otherwise. These represent different
scopes. A shipment-wide result MUST NOT be silently accepted as a lot-specific
assessment. Other namespaces may use different templates; this example is not
a universal shipping-number resolver.

Validate inputs before encoding. Encode variable components as individual path
segments using the mapping's rules; never interpolate raw input as a path or
allow it to replace the scheme or host. Reject unsupported dot segments, control
characters, and malformed values. Do not apply double decoding or numeric
conversion. Show the normalized reference and resolved scope for confirmation.

Query `#i` using the constructed URL, as described in Section 4. The inspector
need not type or visit the URL. Retain the original inputs, normalized values,
namespace/mapping version, and resulting URL with the acquisition audit record.
Include the business reference, namespace, and mapping version in the issued
report so its digest commits to that context; this section adds no new event tags.

### 3.3 Unresolved References And No Results

If no accepted mapping exists, the app MUST report `namespace_mapping_required`
as an acquisition outcome and request a configured namespace, an explicitly
confirmed canonical subject URL, or a supported artifact/event reference.
It MUST NOT invent a subject URL and claim cross-system discoverability.
These acquisition outcomes do not add core ruleset states.

A failed or truncated search is `lookup_incomplete`, not "no records exist".
After a successful bounded search with no suitable match, the inspector may
continue with Flow B or C, subject to explicit confirmation and the same agreed
subject mapping. A new local namespace requires agreement before claiming it
will interoperate with other participants. Finding several candidates requires
scope and recognition checks, not automatic selection of the newest event.

Record whether identifiers were scanned, manually entered, or imported, and any
operator corrections. Where a scan is available, preserve it separately from
the normalized values. None of these acquisition methods establishes that the
reference belongs to the physical goods; inspection remains necessary.

### 3.4 Subject Identity Versus A Canonical Cargo Lot Digest

The inspection use-case paper proposes a canonical cargo-lot digest derived
from stable business fields, separate from a raw report hash. This profile
addresses its cross-report identification and discovery purpose through the
namespaced `subject_ref` and matching `i` value instead. The identifier can stay
constant across distinct reports, report revisions, and assessments of the same
subject without requiring those artifacts to share a digest.

Hashing the subject identifier would primarily provide a fixed-length
representation. It would not establish who assigned the identifier, whether it
is unique in the business context, or whether it belongs to the physical goods.
Participants would still need the same namespace and normalization agreement.

A hash over a canonical collection of cargo fields has a different additional
purpose: it commits to those exact field values. A plain `i` reference does not
provide that commitment. If quantity, commodity, origin, or other descriptive
fields matter to acceptance, they MUST be authenticated in signed event data or
in an artifact whose digest is bound to the signed evidence, and checked by the
verifier. Merely retrieving those fields from the subject URL is insufficient.
The signature authenticates an assertion, not the truth of its physical claims.

Consequently, this profile does not require a separate cargo-lot digest for
lookup. It separates three responsibilities:

| Element | Responsibility |
| --- | --- |
| `subject_ref` / `i` | Identify the claimed cargo subject and discover related records. |
| `o` / `report_digest` | Commit to the exact bytes of the anchored artifact and any separate report. |
| Event signature | Attribute the signed identifiers, digest references, and assertions to a key. |

This is a deliberate alternative to the paper's proposed identity mechanism,
not a claim that an identifier and a content hash are equivalent. If a domain
later needs a canonical cargo-field commitment, it may define that separately,
including field selection, serialization, versioning, and update semantics.
It MUST NOT replace the exact-byte meaning of `o` or silently change the agreed
subject identifier whenever descriptive fields change. The artifact digest
remains essential even when no separate cargo-lot digest is used.

## 4. Discovery Across Reports

The `i` tag repeats `subject_ref` as an indexed external-content identifier,
following NIP-73's URL convention with exactly one `k=web` tag in this profile.
The cargo-subject role is defined by this profile, not by `k=web` itself.
Query participating relays for kinds `1415` and `1416` with `#i` equal to the
subject URI. Verify profile, statement, tag cardinality, signature, and equality
of `i` and `subject_ref`, and `k=web` locally. Relay filters do not establish semantic validity.

Classify subject-only anchors separately from report issuance events. A conforming
subject anchor without `statement=inspection_report_issued` is a discovery and
graph-context candidate, not a verified inspection or a malformed report. Apply
Section 1.1 to subject anchors and Section 2 to report issuance candidates. Generic
anchors outside this profile may still be selected under Flow A after explicit
subject-association checks; do not label them profile-conforming automatically.

### 4.1 GS1 Digital Links And Independent Inspection Apps

A GS1 Digital Link is a web URL and MAY supply the subject identifier. No new
GS1-specific `k` value is required. For example, this illustrative lot reference
uses the same NIP-73 URL convention:

```json
[
  ["subject_ref", "https://example.com/01/09520123456788/10/LOT456"],
  ["i", "https://example.com/01/09520123456788/10/LOT456"],
  ["k", "web"]
]
```

The same printed link can support two experiences. A compatible consumer camera
opens the website. An inspection app MAY instead parse the supported GS1
identifiers and OpenETR digest extension without visiting the encoded domain.
It can query configured relays, obtain artifacts from another repository or a
privately supplied file, verify their digests and signatures, and apply its own
issuer-recognition and acceptance rules. This optional app behavior is not
provided by the `k` tag itself and is not claimed as implemented by this draft.

Distinguish the scanned resolver URL from the stable subject identifier. A
printed link may include report-specific `d` or `digest` and campaign `c` or
`campaign` parameters. These MUST NOT be part of the subject URL used in `i`:
otherwise different reports or campaigns would fragment subject discovery.
The app MUST preserve and validate a supplied digest separately as an expected
artifact reference, not discard it when constructing the subject lookup.

Only apply a defined GS1 parsing and subject-extraction procedure. Do not blindly
strip every query parameter from arbitrary URLs: other parameters may affect
meaning. Unsupported GS1 fields or subject mappings require explicit handling,
not a silent assertion that the remaining URL identifies the same subject.
The initial query-free subject form supports product, lot, and serial path
identifiers; additional subject qualifiers require a profile extension.

Different resolver domains produce different `i` values even when their GS1
identifiers match. Optional broader discovery can query the existing GTIN `g`
tag and compare signed lot/serial associations locally. It MUST NOT equate
different URL subjects solely because their GTIN matches. A GTIN identifies a
product class, not necessarily the lot or individual item under inspection.

With a scanned digest, verify the expected bytes; without one, the app discovers
candidate report digests from signed evidence and must label that distinction.
In both cases, check identifier correspondence and recognized issuer authority.
A matching code or report does not prove the label belongs to the physical item,
and independent retrieval still requires an available, accessible copy.

See [GS1 barcode acquisition](./GS1_BARCODE_ACQUISITION_AND_ANCHOR_DISCOVERY_SPEC.md)
and the [QR resolver profile](./OPENETR_QR_RESOLVER_PROFILE_1_0.md).

### 4.2 Evidence Retrieval Scope

For each candidate, also retrieve its artifact graph using `#o` and missing
predecessors by event ID. Resolve qualifying notices for each candidate issuance.
An optional issuer-filtered search MUST disclose that restriction; it cannot
establish absence of evidence from other issuers. Deduplicate events by ID, not
by subject or report digest.

Relay pagination, result limits, timeouts, and inaccessible sources MUST be
reported. Subject queries cannot prove completeness. Newly discovered reports
with different digests remain candidates; do not hide them by selecting the
newest timestamp. Private subject references may themselves disclose sensitive
relationships. Participants must approve public metadata exposure before pilot
publication, or use controlled-access sources with explicit access limitations.

## 5. Corrections And Competing Assessments

A revised PDF requires a new digest and signed issuance event. A correction
retains `inspection_ref`; a genuinely new inspection uses a new reference.

To change its stated position on an earlier issuance, the original signer MUST
publish a qualifying `notice` such as `corrected`, `superseded`, or `withdrawn`.
For Flow C, follow Core 1.0 anchor-publisher notice ancestry. For A/B, follow
the inspection extension's inspector-notice ancestry. A correction notice SHOULD
identify the replacement via `successor` (report digest) and this profile's
optional `replacement_event` tag (exactly one 64-character lowercase hex event
ID when present). This named tag is a supporting reference, not an `e` parent.
Resolve and validate that replacement rather than treating the pointer as proof.

A `relation=supersedes` inspection alone does not change the earlier issuer's
notice-derived position. Conflicting terminal notices remain a conflict. A
referenced successor that cannot be retrieved remains unavailable, not verified.
Cross-digest successor links never replace the same-digest `e` parent rule.

Multiple inspections of the same subject are not automatically conflicting.
Surface distinct issuers, occurrences, criteria, and observation times. Two
different reports for the same signer and inspection reference without an
unambiguous correction relationship are unresolved alternatives. Contradictory
findings across inspectors require a disclosed domain decision, not automatic
selection. Withhold positive acceptance when required resolution is unavailable.

## 6. Inspector Recognition And Decision Time

The relying party MUST identify a versioned acceptance policy before deriving
an acceptance outcome. Its configuration MUST specify recognized keys, associated
organizations, authorized inspection scopes, accreditation evidence where required,
key-status handling, permitted criteria, and how the relevant effective periods
are evaluated. LEIs and registry identifiers may support recognition; neither a
tag nor a valid signature alone establishes accreditation or competence.

The policy MUST specify freshness thresholds, required query sources, treatment
of unavailable evidence, required observation or timestamp assurance, and the
effect of recognized notices. These values are deployment choices, not universal
protocol constants. If a required policy input is missing, return review-required.

Retain a decision snapshot: evaluated events and reports or access-controlled
references, source observations, failures and limits, verifier version, policy
version, recognition evidence, decision time, and the reason for the outcome.
New evidence may change a later assessment; it MUST NOT silently rewrite the
historical snapshot. An optional signed decision attestation requires its own
profile and is not introduced here.

## 7. Verification Result

A verifier MUST return these separate dimensions in a machine-readable result:

| Field | Required information |
| --- | --- |
| `profile` | This profile identifier and evaluator version. |
| `subject_ref`, `inspection_ref` | Evaluated identities and their namespace context. |
| `candidates` | Anchor and issuance event IDs, signer, report digest, claimed finding and observation time. |
| `integrity` | Signature, report digest, and report/summary correspondence results separately: pass, fail, or unknown. |
| `position` | Applicable notice-derived publisher or inspector position and supporting event IDs. |
| `alternatives` | Competing reports, branches, and unresolved references. |
| `recognition` | Recognized, unrecognized, or unknown; evidence and policy basis. |
| `retrieval` | Sources, filters, observation times, failures, pagination limits, and completeness limitations. |
| `freshness` | Pass, fail, or unknown under the identified policy. |
| `acceptance` | Acceptable, not acceptable, or review required; policy identifier/version and reasons. |

This table defines required semantics, not a finalized JSON schema. A normative
schema and shared test fixtures remain a pre-interoperability review gate.

The UI may summarize results as evidence found, none found in scope, competing
evidence, or lookup incomplete. These discovery summaries MUST NOT substitute for
the separate acceptance outcome. An unrecognized signature or inaccessible report
must never be summarized as a successfully verified inspection.

## 8. Minimum Pilot And Review Gates

For a worked Flow B example, see Section 9 below.

The first pilot needs no new financing registry, transfer action, public report
hosting, or relay-backed content-key system. Agree on the identifiers and policy,
issue an exact PDF through one of the three flows, exchange it through an approved
channel, and verify it using a second implementation or independently operated
client. Demonstrate retrieval of signed evidence outside the issuer's application.

Before claiming interoperability, finalize the tag vocabulary and JSON schema,
provide complete signed event fixtures for each flow, and specify discovery and
replacement-reference test vectors. This draft's URI/`i` discovery convention is
proposed for review; existing applications must not be presumed to implement it.

Tests MUST include altered PDFs, missing digest bindings, copied reports anchored
by another key, wrong lot or inspection references, report/summary disagreement,
unrecognized or out-of-scope inspectors, repeated legitimate inspections,
correction branches, missing successors, withdrawn reports, stale evidence,
failed queries versus empty results, and evidence discovered after a decision.

Manual-acquisition tests MUST also cover identical numbers in different
namespaces, leading zeros and case-sensitive values, supported subdivisions,
shipment-versus-lot scope, repeated identifiers requiring additional context,
unknown mappings, malformed input and path injection, and mapping-version
changes. Two clients must produce the same `i` for the agreed test vectors.
Verify that an absent mapping, failed lookup, or ambiguous candidate set cannot
be presented as a verified subject association.

Confidential payload encryption is an optional later capability governed by the
inspection extension's separate gates. Pilot records must still undergo privacy
and authorization review even when the PDF itself is exchanged privately.

## 9. Worked Example: First Encounter With A Cargo Lot

This illustrative Flow B scenario uses fictional identifiers. An inspector
arrives at a warehouse to examine a shipment they have not encountered before.
It describes proposed application behavior, not an implemented feature.

### 9.1 Identify The Subject

The inspector reads the shipping paperwork and enters:

| Field | Example |
| --- | --- |
| Reference type | Shipment |
| Namespace | `https://example.com/namespaces/shipment-references` |
| Mapping | `example-shipment-v1` |
| Shipment reference | `SHIP-2026-00482` |
| Subdivision | Lot `LOT-03` |
| Description | 100 cartons of bottled wine |

The configured mapping yields:

```text
https://example.com/shipments/SHIP-2026-00482/lots/LOT-03
```

The inspector confirms the scope. This is a subject identifier; the application
does not need to visit that URL. The description assists confirmation but does
not replace the namespaced reference.

### 9.2 Search Before Creating

The app queries configured relays using `#i` and the canonical subject URL,
with kinds `1415` and `1416`. It validates and classifies candidate subject
anchors and inspection reports separately. No suitable anchor is found in this
example, and the app offers:

> No matching record found in the sources checked. Create a new subject record?

The search scope and any limitations remain available. A failed lookup is not
shown as a clean empty result. Proceeding creates another candidate record;
it does not assert that the subject has never been recorded elsewhere.

### 9.3 Create The Subject Artifact And Anchor

After confirmation, the inspector creates a subject document describing the
shipment, lot, reference namespace, mapping, observed markings, and intended
scope. This document identifies what will be assessed; it does not assert that
the goods passed inspection. The app preserves its exact bytes and computes
their SHA-256 digest, represented below as `<subject_digest>`.

The active inspector profile signs a core-conforming `1415` anchor. In addition
to any other core-required fields, its tags include:

```json
[
  ["action", "issue"],
  ["o", "<subject_digest>"],
  ["profile", "openetr:cargo-inspection:0.1"],
  ["subject_ref", "https://example.com/shipments/SHIP-2026-00482/lots/LOT-03"],
  ["i", "https://example.com/shipments/SHIP-2026-00482/lots/LOT-03"],
  ["k", "web"]
]
```

It carries no inspection-report issuance declaration. The app publishes the
anchor, records publication outcomes, and retains the signed event and artifact
under its preservation policy. The inspector is the Anchor Publisher, not
automatically the goods' owner or a recognized inspection authority.

### 9.4 Perform And Document The Inspection

The inspector examines the goods against the identified criteria and produces
a report stating the scope, findings, and limitations. For example:

> Examined the exterior condition of 100 cartons. Three cartons showed water
> damage. Bottle contents were not tested.

The app preserves the issued PDF and calculates `<report_digest>`. The physical
work could have occurred before digital registration; its declared observation
time must describe the actual claimed observation, not simply the upload time.

### 9.5 Publish The Assessment

The inspector signs a `1416` inspection referencing the new anchor. Illustrative
tags are shown below; placeholders must be replaced with actual values:

```json
[
  ["o", "<subject_digest>"],
  ["e", "<subject_anchor_event_id>"],
  ["action", "inspection"],
  ["relation", "assesses"],
  ["profile", "openetr:cargo-inspection:0.1"],
  ["statement", "inspection_report_issued"],
  ["subject_ref", "https://example.com/shipments/SHIP-2026-00482/lots/LOT-03"],
  ["i", "https://example.com/shipments/SHIP-2026-00482/lots/LOT-03"],
  ["k", "web"],
  ["inspection_ref", "https://example.com/inspections/INS-2026-017"],
  ["report_digest", "<report_digest>"],
  ["observed_at", "2026-10-15T14:00:00Z"],
  ["location_ref", "https://example.com/locations/warehouse-07"],
  ["criteria_ref", "https://example.com/criteria/exterior-carton-condition/v1"],
  ["finding", "deviations"]
]
```

The report may be delivered privately. A `report_url` is optional; the signed
digest remains mandatory. The inspection concerns the subject document's graph,
so `o` remains `<subject_digest>` even though the report is another artifact.
The publication is attributable evidence, not an automatically accepted finding.

### 9.6 Independent Review And Later Evidence

A financier, buyer, or regulator searches the same subject reference and obtains
the signed events and report through available, authorized channels. Its verifier
checks signatures, ancestry, digests, identifiers, notices, recognition, and
freshness. The relying party applies its own acceptance policy and retains a
decision snapshot. It may need the subject document as well as the inspection
report to confirm scope; unavailable evidence must remain visible.

```text
Subject document -- exact-byte digest --> Anchor (1415)
                                           ^
                                           | e reference
                                    Inspection (1416)
                                           |
                                           +-- report_digest --> Inspection PDF
```

The inspector has originated a subject record and added an assessment without
claiming exclusive authority over that subject. Another inspector may publish
additional evidence. A correction to this assessment uses an inspector notice;
a correction to the subject anchor's publisher position uses core notice rules.
Neither deletes the original evidence.

### 9.7 Simpler Alternative

If a separate subject document adds no value, use Flow C: complete the report,
anchor its exact bytes with the signed inspection-report issuance declaration,
and omit the redundant inspection event. Here `o` equals `report_digest`.
Both workflows retain the subject URL for discovery. Flow B is useful when a
separate subject record is intended to accumulate multiple assessments; Flow C
is sufficient when the report itself is the primary record.
