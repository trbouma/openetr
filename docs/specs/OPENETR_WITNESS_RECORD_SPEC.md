# OpenETR Witness Record Specification

**Version:** 0.1 — Draft for review  
**Date:** 31 October 2026  
**Status:** Optional experimental extension; not an adopted standard or approved NIP

## 1. Scope and conformance

This draft specifies independently signed observation receipts associated with
OpenETR Anchor Events and Evidence Events. It formalizes the deployed
Spurline/Oakgate convention for review, without changing existing signed bytes.
Specification version 0.1 is not a receipt `schema_version`.

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT and MAY express requirements
for implementations claiming conformance to this draft. They do not impose
requirements on ordinary Nostr relays or existing OpenETR applications.

Two roles are defined: a **producer** issues receipts; a **verifier** checks and
reports them. Implementations MUST declare their role and supported receipt
versions. Verifiers MUST support version 3; versions 1 and 2 are optional
compatibility profiles. Producers MAY implement any listed profile but MUST
satisfy its clock declarations and applicable authorization policy.

This is an extension of relay and application capabilities using ordinary Nostr
events and queries. Kind `1418` is a **provisional OpenETR draft assignment**,
not a reserved Nostr allocation. Admission and retention policies still apply.
This draft does not change NIP-09, require append-only storage, amend the core
OpenETR wire specification, or change Core Record Ruleset 1.0.

## 2. Meaning and boundaries

A Witness Record makes this attributable claim:

> The witness observed this exact signed event and successfully checked its
> event ID and signature at the stated observation time.

The receipt MUST NOT be interpreted as endorsement of the subject's contents,
verification of its artifact bytes, proof of first publication, proof of global
evidence completeness, or a control transition. A receipt for one event does not
witness its predecessors, successors or entire Evidence Graph.

A hosting relay is not necessarily the witness. The witness is the receipt's
signer. Signature validity does not establish authority, truthful time, or
independence from the subject author.

## 3. Envelope and subject

The receipt MUST be a classical Nostr event of kind `1418`, signed by the witness
key. Both receipt and subject IDs MUST be recomputed and their Schnorr signatures
verified under NIP-01. Subject kind MUST be `1415` or `1416`. Cryptographic
verification of a subject does not establish that it qualifies under an OpenETR
ruleset; that evaluation remains separate.

IDs and public keys MUST be 32-byte lowercase hexadecimal values; signatures
MUST be 64-byte lowercase hexadecimal values. Kind and creation time MUST be
nonnegative integers, not booleans, within `0..2^53-1`. Receipt `created_at` MUST
equal `floor(issued_at_ms / 1000)`.

For receipt version `V`, the exact tag array MUST be:

```text
[["e", SUBJECT_EVENT_ID],
 ["p", SUBJECT_AUTHOR_HEX],
 ["k", SUBJECT_KIND_DECIMAL],
 ["t", "spurline-observation-receipt-vV"]]
```

Replace `V` with `1`, `2` or `3`. Tags MUST match the subject and content version;
extra tags, reordered tags, duplicate tags and extra tag elements are invalid
under these profiles. The `e` tag denotes observation, not a Publisher Notice
predecessor relationship. Receipts MUST NOT be inserted into notice chains.

## 4. Content and signed-subject commitment

Content MUST be a JSON object serialized as a string with lexicographically
sorted keys, compact separators and no additional whitespace. Duplicate keys,
unknown fields and noncanonical encoding MUST be rejected. All defined string
values are ASCII constants or lowercase hexadecimal, avoiding Unicode
normalization ambiguity. Numerical fields MUST use integer JSON notation,
not floats, exponent notation or booleans, within `0..2^53-1`.

All profiles have exactly these fields, plus the version-specific fields below:

| Field | Requirement |
| --- | --- |
| `schema` | `org.spurline.observation-receipt` |
| `schema_version` | Integer `1`, `2` or `3` |
| `subject_profile` | `nostr-schnorr-secp256k1-v1` |
| `event_id` | Exact subject event ID |
| `signed_event_digest` | Lowercase SHA-256 commitment defined below |
| `observed_at_ms` | Claimed UTC Unix observation time in milliseconds |
| `issued_at_ms` | Claimed UTC Unix issuance time in milliseconds; not before observation |
| `clock_uncertainty_ms` | Version-specific integer or JSON `null` |
| `validation` | `event-id-and-signature` |
| `observation_mode` | `live` or `backfill` |
| `witness_policy_digest` | SHA-256 of exact policy artifact bytes, 64 lowercase hex characters |
| `authorization_event_id` | Exact authorization event ID, 64 lowercase hex characters |

The commitment MUST be computed as:

```text
SHA256(
  ASCII("spurline.observed-signed-event.v1") || 0x00 ||
  decode_hex(subject.id) || decode_hex(subject.sig)
)
```

The ID and signature contribute exactly 32 and 64 bytes respectively. A different
valid signature for the same ID requires a different commitment. Verifiers MUST
retain the exact signed subject rather than discard signature variants before
checking binding. The domain string's `v1` is unchanged across receipt versions
1–3. These profiles do not support post-quantum signatures or algorithm fallback.

## 5. Clock profiles and observation modes

| Receipt version | Required clock fields | Interpretation |
| --- | --- | --- |
| 1 | Integer `clock_uncertainty_ms`; no `clock_basis` or `clock_accuracy` fields | Claimed numeric uncertainty, requiring separate policy assessment |
| 2 | `clock_uncertainty_ms: null`, `clock_accuracy: "unspecified"`, `clock_basis: "ntp-synchronized-system-clock"` | Witness claims synchronization but no numerical accuracy bound |
| 3 | `clock_uncertainty_ms: null`, `clock_accuracy: "unspecified"`, `clock_basis: "system-clock"` | System-clock observation with no synchronization or numerical accuracy guarantee |

For v1, `observed_at_ms + clock_uncertainty_ms` MUST also fit the safe integer
range. A verifier MUST NOT convert `null` uncertainty into zero. Millisecond
representation is not a claim of millisecond accuracy. Synchronization claims
are not independently proven by a valid receipt signature.

`live` means observation during the producer's current acceptance/validation
flow. `backfill` means observation of an already stored or retrieved event.
Both MUST use the actual new observation time, never the subject's `created_at`
as a substitute. Issuance can occur later through a durable queue; producers
MUST preserve the original observation metadata across retries.

Only an explicitly accepted time policy can derive a time bound. For v1 this
may be the upper end of an accepted observation interval. Versions 2 and 3 alone
MUST NOT yield a numerical accuracy guarantee or an independently established
deadline conclusion.

## 6. Production and relay behavior

Automatic witnessing MUST be explicitly enabled and scoped to eligible subject
kinds. A producer MUST verify the exact subject before recording successful
observation, and MUST NOT recursively witness receipts under this profile.
It MUST have valid witness authorization under its configured commissioning and
policy profile at the times that profile requires. Ordinary permission to
operate a relay is not by itself authorization to witness.

Producers SHOULD durably retain the exact subject, observation metadata and
pending issuance job. Retrying publication of an already signed receipt MUST
reuse that receipt, not fabricate a fresh observation. Clock failures, missing
authorization or signing failures MUST NOT generate invented observations.
Relay acceptance and receipt issuance MUST remain distinguishable; a Nostr
`OK` response is not a Witness Record.

Operators SHOULD disclose witnessing, retention and administrative removal
policies, and bound queues and resource use. Public references may expose
associations. This draft promises neither permanent retention nor receipt
issuance for every accepted event.

## 7. Discovery and verification

Applications SHOULD query configured evidence sources by subject event ID:

```json
{"kinds":[1418],"#e":["<subject-event-id>"],"limit":100}
```

The placeholder is illustrative, not a valid ID. An optional author filter can
restrict discovery but does not prove trust. Omitting a version marker permits
discovery of all versions; the verifier MUST inspect the actual schema and tags.
The artifact digest is not the subject event ID. Untrusted receipt references
MUST NOT silently select network destinations.

A verifier MUST:

1. Check the receipt envelope, ID and signature.
2. Parse content strictly and select a supported profile. Unsupported versions
   MUST be reported as unsupported, not accepted by approximation.
3. Retrieve the exact subject and independently check its ID and signature.
4. Validate all profile fields, exact tags, time relationships and commitment.
5. Report cryptographic/binding validity separately from authorization, authority
   recognition, clock-policy assessment and any accepted time conclusion.

Missing subjects are incomplete evidence, not successful binding. Malformed or
invalid receipts MUST NOT be presented as verified. Implementations MAY retain
them for diagnostics. Queries SHOULD be bounded; sources, failures, limits and
retrieval time MUST be available in the assessment context. Empty results MUST
NOT imply that no witness exists.

## 8. Authorization and evaluation results

This draft defines evidence references, not a universal commissioning format or
trust root. Full trust evaluation requires an explicitly named authorization
profile and relying-party policy. It MUST verify the referenced grant, witness
key, role, covered kinds, exact policy bytes/digest, applicable validity periods,
commissioning evidence and relevant known renewal/revocation/compromise evidence.
An unsupported authorization profile MUST NOT be treated as an accepted grant.

Results MUST distinguish at least these dimensions; equivalent field names are
permitted because this draft does not prescribe an application JSON API:

| Dimension | Distinctions that must be preserved |
| --- | --- |
| Receipt/profile checks | Valid, invalid, unsupported, incomplete |
| Authorization | Accepted, rejected, incomplete, not evaluated |
| Authority recognition | Recognized, unrecognized, not evaluated |
| Time-policy assessment | Accepted, rejected, indeterminate, not evaluated |
| Retrieval coverage | Queried sources and limitations; no assumed global completeness |

A cryptographic verifier MAY leave trust dimensions unevaluated, but MUST say
so. A generic “verified” badge MUST NOT imply those assessments occurred.
Signatures do not prove complete revocation knowledge or truthful clocks.
Core Record Ruleset 1.0 results MUST remain unchanged by receipt presence,
absence or trust outcome. Any consequential dependency requires a separately
versioned ruleset.

## 9. Multiple receipts and portable evidence

Deduplicate identical receipts by event ID, retaining all retrieval sources.
Preserve distinct receipts, including conflicting claims from one witness.
Group by exact signed-subject commitment and witness key when assessing them.
Multiple copies are not independent witnesses; different keys may also share
an operator or clock. Verifiers MUST NOT average times or use witness counts
to select an OpenETR notice branch without a separate explicit policy.

Portable evidence SHOULD include the exact subject and receipts, policy bytes,
authorization and commissioning dependencies, relevant lifecycle evidence,
retrieval observations and evaluation policy/version. Offline verification MUST
identify missing dependencies and the limits of its revocation knowledge.

## 10. NIP-03 and security considerations

NIP-03's event-ID timestamping does not bind the subject signature. Its published
status and the precommitment/later-key-compromise threat are discussed in the
[design note](./OPENETR_RELAY_WITNESS_RECORDS_DESIGN_NOTE.md#nip-03-status-and-the-signature-existence-distinction).
The exact-signature commitment here addresses that binding gap, not witness
dishonesty. A compromised witness key can still issue backdated claims.

This draft is not a repair to NIP-03 or an OpenTimestamps proof profile. A valid
receipt proves attribution of a claim, not independent truth of its timestamp.
Consumers SHOULD assess correlated witnesses, compromise evidence, replayed
receipts, resource exhaustion and privacy leakage. Re-presenting an old receipt
MUST NOT be displayed as a new observation.

## 11. Compatibility, testing and standardization

Existing Spurline v1–v3 wire values are retained intentionally. A future neutral
schema name, kind allocation, canonicalization or algorithm profile MUST be
explicitly versioned. Verifiers MUST NOT rewrite, relabel or re-sign old evidence
as if it conformed to a newer profile. Unsupported receipts can be preserved
without being accepted. Kind collisions require schema checks and coordinated
migration, not a claim that this draft reserves 1418 globally.

Conformance tests MUST cover the following, as applicable to supported versions:

- Valid receipt/subject pairs and exact commitment recomputation.
- Altered subject or receipt signatures/IDs; a mismatched subject commitment.
- Extra/duplicate/reordered tags and fields; noncanonical JSON; unknown versions.
- Negative, boolean, fractional, unsafe and inconsistent times; profile-specific
  null/zero uncertainty behavior and mismatched outer creation time.
- Missing subjects, duplicate hosting, multiple witnesses and conflicting claims.
- Partial retrieval and unavailable authorization; no change to core evaluation.
- Live/backfill distinctions and preservation of signed receipts across retries.

The [Spurline v1 fixture](https://github.com/trbouma/spurline/blob/main/tests/fixtures/observation-receipt-v1.json)
is an initial cryptographic test vector, not a complete conformance suite.
Publication of an independently reproducible v1–v3 positive/negative vector
bundle, independent implementation review, and agreement on a Nostr kind
allocation remain prerequisites proposed for progression beyond draft status.

Spurline implements issuance and Oakgate implements discovery and cryptographic
display checks. This statement does not certify either implementation against
every requirement in this new draft, particularly full trust evaluation.

## References

- [Relay Witness Records design note](./OPENETR_RELAY_WITNESS_RECORDS_DESIGN_NOTE.md)
- [Core Record Ruleset 1.0](./OPENETR_CORE_RECORD_RULESET_1_0.md)
- [OpenETR Nostr wire format](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [Spurline receipt profile v1](https://github.com/trbouma/spurline/blob/main/docs/observation-receipt-v1.md)
- [Spurline receipt profile v2](https://github.com/trbouma/spurline/blob/main/docs/observation-receipt-v2.md)
- [Spurline system-clock operation](https://github.com/trbouma/spurline/blob/main/docs/system-clock-witness-setup.md)
- [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md)
- [NIP-03](https://github.com/nostr-protocol/nips/blob/master/03.md)
