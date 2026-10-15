# OpenETR Inspection Evidence And Encrypted Report Convention

## Status

Draft extension for review and implementation, October 15, 2026. This document
does not claim implementation support in OpenETR, OpenQR, Acorn, or Safebox Web.
Proposed extension identifier: `openetr:inspection:0.1`.

Depends on [Core Record Ruleset 1.0](./OPENETR_CORE_RECORD_RULESET_1_0.md) and
the [Nostr wire format](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md). MUST, SHOULD, and
MAY express requirements within this proposed extension, not deployed behavior.

## 1. Evidence And Recognition

An inspection is an attributable assessment concerning an anchored artifact and
its stated subject. It is not proof that an inspection occurred or that its
findings are true. The signer may differ from the Anchor Publisher.

All events add evidence. Corrections, withdrawals, and claims of supersession
do not delete or rewrite prior statements. References establish relationships;
an identified ruleset and the relying party's recognition policy determine
whether those relationships have consequences. Publication alone confers no
authority, changes no control, and settles no competing claim globally.

### 1.1 Workflow Selection

An inspection report can be the primary anchored artifact or evidence concerning
another anchored artifact. Implementations MUST distinguish these workflows;
they MUST NOT require a redundant inspection event merely because an anchored
artifact is an inspection report.

| Flow | Initial situation | Evidence published |
| --- | --- | --- |
| A: Assess an existing record | A suitable anchor is found and selected. | A `1416` inspection linked to that anchor or a qualifying predecessor. |
| B: Establish the subject, then assess it | No suitable anchor is found; a separate subject record is needed. | A `1415` anchor for the subject artifact, followed by a `1416` inspection. |
| C: Issue an inspection report | The completed report is itself the primary artifact. | A `1415` anchor for the report; a separate `1416` inspection is optional and must add a distinct assessment or relationship. |

### 1.2 Acquisition And Anchor Selection

For Flow A, acquire a reference by scanning a barcode, supplying an artifact
digest, uploading the original file, or selecting a record. Product identifiers
may discover candidate anchors, but do not replace the exact-byte digest.
Validate candidate event signatures and artifact associations and identify the
specific anchor intended as the assessment's context. Retrieve and verify the
artifact when needed to establish inspection scope; disclose any access limits.

Multiple anchors may identify the same artifact, and multiple artifacts may
concern the same goods. The application MUST NOT silently equate those cases
or select an authoritative anchor solely by timestamp. Selection MUST be explicit
or follow an identified domain policy, with its basis available to the user.
Selecting an anchor does not endorse its claims or recognize its publisher.

Record search scope, failures, and incomplete results. "No suitable anchor found"
is not proof that none exists elsewhere. It permits consideration of Flow B or C,
not a claim of globally unique issuance. The inspector MAY originate an anchor;
doing so grants neither ownership of the goods nor inspection authority.

The physical inspection may occur before digital lookup or publication. Only
the linked inspection event requires a known predecessor event ID. Claimed
observation time and publication or observation evidence remain distinct.

### 1.3 Flow A: Assess An Existing Record

Resolve and select the anchor, establish the subject and scope, and publish the
assessment as `action=inspection`. Its `e` identifies the selected anchor or
qualifying predecessor; its `o` retains that anchor's artifact digest. A separate
report can have its own `report_digest` without replacing `o`. Later notices
about this assessment derive inspector position under Section 4.

### 1.4 Flow B: Establish The Subject Then Assess It

Create or obtain an artifact describing the subject, such as a lot description
or shipment manifest. Preserve its exact bytes, calculate its digest, and publish
a conforming `1415` anchor. The inspector may sign both this anchor and the later
inspection, but their roles remain distinct: originating a subject record and
assessing its stated subject.

The artifact may be a document the inspector received, not one they authored.
Anchoring a received manifest or report records the inspector's signed association
with those bytes; it does not imply authorship, endorsement, or issuance of its
contents. Preserve the received bytes unchanged and distinguish the source
document from any subsequent assessment created by the inspector.

If no suitable artifact exists, the application MUST create or obtain one before
anchoring. It may generate a subject document from inspector-confirmed inputs,
or generate the completed inspection report for Flow C. Finalize and preserve
the exact bytes before computing `o` and signing. A manually entered shipment
number or subject URL alone is not an artifact digest, and this workflow does
not permit a digest-free anchor. App-generated content must be reviewed by the
inspector; file generation does not itself perform an inspection.

Once the anchor event ID is known, publish the `1416` assessment using that ID
in `e` and the subject artifact digest in `o`. Apply Flow A's validation rules.
Do not substitute a hash of selected business identifiers for the subject
artifact's digest. Identify the goods, inspection occurrence, and report as
distinct domain concepts even if the application presents them together.

### 1.5 Flow C: Anchor The Inspection Report Itself

Preserve the completed report as the artifact and publish its conforming `1415`
anchor (`action=issue` in the current wire binding). Here `o` identifies the
report's exact bytes. Core anchoring establishes the key's signed association
with that artifact; it MUST NOT automatically be presented as proof that the
publisher performed the inspection, authored the report, or endorsed every finding.

If anchoring is intended to constitute report issuance or endorsement, the domain
profile MUST define that meaning and the signed evidence supporting it. A verifier
must be able to distinguish the inspector issuing a report from a third party
merely anchoring a copy. An application button label or possession of the file
alone is insufficient. The exact issuance/endorsement declaration is a review
decision for the domain profile, not a new universal meaning for `action=issue`.

No separate inspection event is required for basic report anchoring. A later
independent assessment or distinct assertion may use `1416` with this report's
anchor as its context. The report publisher's own corrections or withdrawal use
Core 1.0 Publisher Notices targeting the report anchor or its notice ancestry;
notices about a separate inspection follow Section 4 instead.

Revised report bytes require a new digest and, if independently anchored, a new
anchor. A correction or successor reference can associate the records without
rewriting the earlier evidence or crossing digest scope in the parent chain.
For confidential reports, the profile MUST specify whether the anchored artifact
is plaintext or an encrypted envelope; their digests are not interchangeable.
Section 5's encrypted `1416` report convention does not silently define encrypted
`1415` issuance. That binding remains a separate implementation gate.

## 2. Inspection Event

An inspection event, when used, MUST be a signed regular kind `1416` event containing exactly one
of each required tag:

```json
[
  ["o", "<anchored_artifact_sha256_hex>"],
  ["e", "<anchor_or_preceding_inspection_or_notice_event_id>"],
  ["action", "inspection"],
  ["relation", "assesses"]
]
```

`inspection` is an action value, not a standalone tag or a new event kind.
`relation` MUST be one of `assesses`, `supplements`, `corrects`, or `supersedes`.
It expresses the signer's claimed relationship to the event identified by `e`.
It does not itself establish recognized correction or supersession.

Inspection relationships add assessment evidence; they do not update the earlier
inspector's derived position. That position is derived from qualifying notices
under Section 4. A later assessment claiming `supersedes` is not a substitute
for a withdrawal or supersession notice about the earlier statement. A domain
policy that assigns additional consequences MUST define its precedence and
conflict rules explicitly; timestamp order alone is insufficient.

The single `e` link MUST resolve, through qualifying predecessors, to a valid
kind `1415` anchor. Every event on that path MUST carry the same `o` digest.
An inspection MAY follow the anchor, another inspection, or a notice whose
ancestry resolves to that anchor. Missing parents, cycles, unsupported actions,
and scope mismatches MUST be reported, not silently repaired. Additional
supporting references MAY use `ref`; they are not alternate graph parents.

The `o` digest continues to identify exact artifact bytes. A GTIN, cargo-lot
identifier, or hash of selected shipment fields MUST NOT replace it.

## 3. Report And Subject

An inspection may assess the anchored artifact itself or make an assessment
about goods described by that artifact. The domain profile MUST distinguish
those meanings and specify subject identifiers, inspection scope, sampling,
claimed observation time, findings, and any required supporting evidence.
Semantic interpretation and recognition of inspectors remain domain concerns.

The report can be the already anchored artifact, a separate referenced artifact,
or an inline narrative. Optional named tags are:

| Tag | Meaning |
| --- | --- |
| `report_digest` | SHA-256 of the exact plaintext report bytes, when publicly disclosed. |
| `report_url` | Retrieval hint for an external plaintext or encrypted report; not an authority. May repeat for mirrors. |
| `ciphertext_digest` | SHA-256 of the exact external encrypted envelope bytes. |
| `encryption` | Identifier and version of an agreed encryption-envelope profile. |
| `key_ref` | Friendly reference to a separately protected content-key record. |
| `key_owner` | Canonical public key of the profile holding that key record, when different from the event signer. |

An external plaintext report MUST have a signed `report_digest`, even when it
is delivered privately rather than through a public URL. A locator alone is
insufficient. If the report is the anchored artifact, `o` supplies its binding;
any additional `report_digest` MUST equal `o`. If a separate report is assessed,
its digest MUST NOT replace the subject artifact's `o`. Inline plaintext content
is protected by the event signature and need not repeat its digest.

For external encrypted reports, `ciphertext_digest` is required and the plaintext
digest MUST be authenticated either publicly or within the protected envelope
as specified in Section 5. In every form, report bytes accepted as verified MUST
be bound to the signed inspection evidence. A mismatch is an integrity failure;
an inaccessible report is an access limitation, not a successful integrity check.

Except for `report_url`, these tags MUST NOT repeat. Digest values use 64-character
lowercase hex. `key_owner` uses the Nostr 32-byte public key in lowercase hex.
Plaintext narrative belongs in `content`; structured report data belongs in
defined tags or a separately specified report format. Protected structured data
belongs inside the authenticated encrypted envelope, not public tags.

A separate report digest does not change the graph's `o`. If a revised artifact
is independently anchored, it gets its own digest and anchor; a successor
reference links it without making a cross-digest graph parent.

## 4. Notices About Inspections

Use the existing `action=notice` and `notice_type` vocabulary for errata,
withdrawal, correction, or supersession. Do not introduce an `errata` action.

This extension permits a notice to target an inspection, or a preceding notice
in that inspection's notice branch. It MUST carry exactly one `e`, `o`, `action`,
and supported `notice_type`. Trace its notice ancestry back to the inspection.
For the baseline inspector-position derivation, the notice signer MUST equal
that inspection's signer. More than one terminal qualifying notice produces
`conflicting_notices`; timestamp ordering MUST NOT silently choose a winner.
No qualifying notice means `no_notice_found`, not approval or current validity.

A different signer may publish a correction, disagreement, or claim of authority.
Retain and attribute that evidence, but do not apply it as the inspector's own
position. A separately identified domain rulebook may recognize additional
authority and MUST explain that decision.

Core 1.0 remains unchanged: only qualifying notices from the Anchor Publisher
derive the Anchor Publisher's position through its permitted notice ancestry.
Inspection-targeted notices do not enter that core derivation, even if the same
key signed both anchor and inspection. Maintain inspector position separately.

## 5. Optional Encryption

An inspection report MAY be confidential while its signed references remain
public. Choose one of these forms:

- **External report:** `content` is empty or a non-sensitive narrative;
  `report_url` supplies hints, and `ciphertext_digest` identifies the encrypted
  envelope. `encryption` and `key_ref` are required.
- **Inline report:** `content` contains the serialized encrypted envelope;
  `encryption` and `key_ref` are required. The signed event protects these exact
  content bytes. This form MUST NOT also specify an external `report_url` or
  `ciphertext_digest`.

An encryption profile MUST define authenticated encryption, key sizes, nonce
generation, authentication tags, encoding, associated-data binding, envelope
versioning, and recipient key wrapping. Use established reviewed formats and
libraries. Unknown profiles MUST be reported as unsupported, not guessed.
The concrete cryptographic profile is intentionally pending; this draft alone
is NOT a complete interoperable encrypted-event format.

Plaintext and ciphertext digests identify different bytes. A public
`report_digest` is optional because it may disclose correlations or permit
guessing predictable content. If withheld, it MUST be included in the protected
report or disclosure envelope under the selected profile. That profile MUST
authenticate the binding between the plaintext digest, ciphertext, key owner,
key reference, and relevant artifact/event context without circular hashing.

An authorized reader verifies the signed event, verifies an external ciphertext
digest where applicable, unwraps the disclosed key, authenticates and decrypts
the envelope, and checks the plaintext digest. Successful decryption does not
establish issuer recognition, physical authenticity, or current acceptability.
An unavailable key is an access limitation, not proof of an invalid inspection.

## 6. Profile Scoped Key References

Before encrypting a report, the originating profile SHOULD generate a fresh
cryptographically random symmetric content key and an independent `key_ref`.
The reference MUST NOT be derived from that key or a wallet seed phrase.

Safebox Web / Acorn's proposed friendly-reference convention is two independently
random BIP39 English words followed by an integer from 0 through 99, without
spaces. For example:

```json
["key_ref", "mapleharbor42"]
```

Use the BIP39 word list only, not mnemonic-generation or seed-derivation semantics.
The numeric suffix has no leading zero except `0` itself. Treat the full string
as an opaque lookup value, not a secret or a phrase to reconstruct a key from.
Other applications MAY define another reference format under an explicit profile.

Lookup scope is `(key_owner, key_ref)`, with `key_owner` defaulting to the
inspection event's signer. An application MUST NOT silently substitute the root
or control desk key. The friendly format has 419,430,400 possible combinations;
it is guessable and does not guarantee uniqueness, even within one profile.

Check for existing allocations and regenerate on collision. Concurrent devices
must coordinate allocation or detect duplicates and report ambiguity. A relay
query alone cannot prove uniqueness. Never silently overwrite a different key
or choose the newest record to resolve an ambiguous reference. Fresh references
SHOULD be used for fresh keys; do not reassign old references to different keys.

## 7. Relay Backed Key Storage And Disclosure

Store the content key and its authenticated report/context binding in a record
encrypted for the originating profile. Confirm the configured persistence policy
before relying on that record; retain recovery arrangements appropriate to the
application. Relay retention and root-key recovery MUST NOT be assumed.

The public `key_ref` lets a requester ask for the right key. It grants no access.
The owner authenticates the recipient and authorizes disclosure separately, then
delivers the content key and binding encrypted for that recipient's public key.
The recipient's private key unwraps that disclosure; the content key decrypts
the report. Multi-recipient access can wrap the same content key separately for
each authorized recipient without changing the report.

Key-record and disclosure event kinds, indexed lookup tags, storage encryption,
request authentication, and envelope formats remain implementation decisions to
be specified before interoperable deployment. No new kind assignment is made
here. These private application records are not automatically DCR graph events.
`key_ref` is a named descriptive tag; NIP-01 single-letter indexing must not be
assumed for it. A private store may use a separately defined lookup convention.

Other parties may discover encrypted key records; confidentiality comes from
encryption, not hidden discovery. Public key references, signer identities, and
graph links can reveal associations. Disclosure cannot reliably be revoked once
a recipient retains the key or plaintext. A notice can express withdrawal, but
cannot cryptographically undo access already granted.

## 8. Verification And Presentation

Preserve separate outcomes for event integrity, graph completeness, inspection
scope, inspector position, report integrity, access availability, issuer
recognition, and domain acceptance. Unknown extensions remain visible with no
invented core consequence. Multiple inspections are not inherently a conflict.
Record queried sources, limits, failures, and observation time. Report absence
as absence within the retrieval scope, never global nonexistence.

`created_at` and inspection dates are signer assertions, not independently
verified timing. Witnessing, timestamping, freshness, physical association, and
recognition of authority require their own rules and evidence.

An implementation supporting a domain profile MUST expose the profile and
acceptance-policy identifiers, subject identifiers, evaluated event IDs, report
digest and integrity outcome, signer and recognition outcome, notice-derived
position, competing assessments, retrieval scope and failures, observation time,
and freshness outcome. Domain acceptance MUST remain separate from successful
signature validation. A simple UI summary MUST retain these underlying results.

Discovery by a single `o` does not enumerate all inspections of the same goods.
A domain profile MUST define subject-reference conventions and cross-artifact
discovery when it claims that capability. See the draft
[Cargo Inspection Profile](./OPENETR_CARGO_INSPECTION_PROFILE.md) for a bounded
pilot using privately exchanged PDF reports and public signed references.

## 9. Implementation Gates And Tests

### 9.1 Minimum Inspection Pilot

Before a plaintext or privately exchanged report pilot, implement and test:

1. Plain inspections linked to anchors, inspections, and notices; separate
   inspector and anchor-publisher positions; competing notice branches.
2. Invalid signatures, wrong digests, missing parents, cycles, and unsupported
   actions without hiding the supplied evidence or changing core state.
3. Altered report bytes, repeated legitimate inspections, different signers,
   corrections, new report artifacts, and claimed cross-signer supersession.
4. Mandatory external-report digest binding, changed bytes at an unchanged URL,
   private file delivery, unavailable reports, and digest mismatches.
5. All three issuance workflows, including report-only anchoring without a
   redundant inspection event, subject-first anchoring, and assessment of an
   existing anchor selected from multiple candidates.
6. No-results versus failed or incomplete discovery, third-party anchoring of a
   report versus recognized issuance, and corrections using the appropriate
   core-publisher or inspector-specific notice ancestry.
7. A domain profile for subject discovery, signed issuance, recognition, freshness,
   and reproducible acceptance results; retained decision snapshots and privacy review.

### 9.2 Optional Confidential Report Extension

Encrypted payload support additionally requires:

1. A selected interoperable encryption profile and private-store binding, with
   independent test vectors for exact plaintext, ciphertext, and recipient envelopes.
2. Wrong keys, modified ciphertext, unsupported formats, substituted key records,
   mismatched owner/reference/context, and missing encryption metadata tests.
3. Empty stores, duplicate references, concurrent allocation, unavailable relays,
   unauthorized requests, successful recipient disclosure, and recovery tests.
4. Secret-free logs and UI distinctions between encrypted, decrypted, verified,
   and recognized. Do not advertise encryption interoperability before these gates pass.

Private bilateral delivery of a report does not require this encryption extension.

Review decisions before a domain pilot: choose the primary artifact (issued PDF
or defined structured record), specify any rendition associations, define the
signed issuance/endorsement declaration, and establish issuer recognition and
decision-time freshness requirements. These choices may refine this draft.

The first implementation may support plaintext inspection evidence while keeping
encrypted report support explicitly unavailable until its profile is finalized.
