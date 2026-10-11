# GS1 Barcode Acquisition And Anchor Discovery

## Status And Scope

Draft integration specification, 10 October 2026. Intended for safebox-web scanner
acquisition and handling, and other OpenETR-aware readers. MUST, SHOULD, and MAY
express requirements of this profile, not changes to GS1 or Nostr standards.

This profile discovers kind `1415` anchors using an indexed GTIN, then evaluates
lot, expiry, and optional serial locally. It supports existing product labels
without requiring an OpenETR digest or website URL in the barcode. It does not
define regulatory acceptance, physical authenticity, or a transferable-record
ruleset. This document specifies work to implement; it does not claim that
safebox-web or OpenQR already implements this complete workflow.

## Worked Scan

The scanned payload is:

```text
01000576060290961727013110693773
```

Its GS1 element-string interpretation is:

```text
(01)00057606029096(17)270131(10)693773
```

| AI | Field | Exact value |
| --- | --- | --- |
| 01 | GTIN | `00057606029096` |
| 17 | Expiry, YYMMDD | `270131` |
| 10 | Batch/lot | `693773` |

In this product context the expiry represents 31 January 2027. Parentheses are
human-readable notation, not encoded payload characters. There is no serial or
artifact digest in this scan. Lot is the final variable-length field, so no
following field separator is needed to determine its end.

## Acquisition And Parsing

The scanner MUST preserve decoded payload and symbology/GS1 metadata when the
scanner SDK supplies them. It MUST preserve ASCII group separators (0x1D) rather
than removing them before GS1 parsing. FNC1 is a symbology function, not the
literal string `FNC1`; SDK representations must be handled explicitly.

Classify the acquisition before lookup:

| Input | Handling |
| --- | --- |
| EAN/UPC or validated raw GTIN | Extract the GTIN and normalize to 14 digits |
| GS1 element string, such as GS1 DataMatrix | Parse AIs using GS1 syntax rules |
| GS1 Digital Link | Parse product identifiers and any supported digest extension |
| Existing OpenETR digest link | Preserve the existing digest lookup workflow |
| Other or ambiguous payload | Report unsupported/ambiguous input; do not guess |

Use a maintained GS1-aware parser or the GS1 Barcode Syntax Engine where suitable.
Do not search arbitrary text for `01`, `10`, or `17` substrings. Fixed-length AI
01 consumes 14 digits; AI 17 consumes six; AI 10 is variable length and requires
correct separator handling when followed by another field. AI 21 is serial.
Order is not fixed to the worked example. Unsupported fields must be parsed
safely or rejected, not stripped in a way that changes field boundaries.

For manually entered element strings without symbology metadata, require an
explicit GS1 mode and unambiguous parsing. Do not classify any numeric string
beginning with `01` as a valid GS1 payload. UPC-E requires proper expansion by a
symbology-aware decoder; an eight-digit UPC-E must not be treated as GTIN-8 merely
because its length matches.

GTIN normalization MUST preserve leading zeros, validate the GS1 check digit,
and produce 14 ASCII digits. Lot and serial remain strings: preserve case and
leading zeros, and do not trim or numerically coerce the decoded field. Duplicate
supported AIs MUST be reported as ambiguous rather than choosing one silently.

## Anchor Tag Convention

One anchor asserts one product association for an exact artifact:

```json
[
  ["action", "issue"],
  ["o", "<64-character lowercase SHA-256 digest of the artifact>"],
  ["g", "00057606029096"],
  ["gs1_lot", "693773"],
  ["gs1_expiry", "270131"]
]
```

The example above is a tag template, not a complete signed event. `g` is required
for indexed discovery. Optional qualifiers are omitted when absent, not emitted
with empty values. AI 21 maps to `gs1_serial`. Each association tag MUST occur
at most once. All tags are signed as part of the event.

This profile introduces **`gs1_expiry`**, storing the exact six-character AI 17
value in **YYMMDD**, not an ISO date or Unix timestamp. It is a named metadata
tag; relay indexing is not required. New publishers MUST validate it against
the applicable GS1 date rules and domain profile.

Preserve the original six digits for matching. Century interpretation, display,
and expiry-policy decisions are separate and MUST NOT silently assume every
two-digit year is in the 2000s. Where GS1 permits a zero day (`DD=00`), retain it
and apply the specified end-of-month interpretation for display/policy only.
Do not silently equate it to an explicitly encoded final day during exact matching.
Regulated healthcare rules require a valid day from 1 January 2025; a reader
must not present a legacy zero-day value as compliant with that requirement.
Ambiguous or invalid dates require a diagnostic rather than an invented date.

Readers accept legacy `gs1_gtin` under the wire-format compatibility rules, but
anchors carrying only that legacy tag cannot be discovered by `#g` alone.
No event is edited or re-signed automatically to migrate historical tags.

## GTIN Discovery

Query every configured query relay using:

```json
{"kinds": [1415], "#g": ["00057606029096"]}
```

The intent is to enumerate all available anchors matching that GTIN within the
declared relay scope, then inspect qualifiers locally. Do not add `#gs1_lot` or
`#gs1_expiry` filters or limit discovery to the current user's signing key.
Use the application's configured query relays, not a URL supplied by the barcode.

Deduplicate by event ID across relays. Validate each event's ID, signature, kind,
`action=issue`, canonical `g`, and canonical artifact `o` before treating it as a
candidate. Do not rely only on the relay having honoured the requested filter.
Malformed, duplicated, or conflicting association fields produce a rejected
association with a reason; they must not be merged across different anchors.

Nostr `REQ` limits and relay retention mean a response cannot prove global
completeness. Implement bounded, cancellable retrieval and pagination where
supported; record queried relays, failures, limits, and whether discovery may be
incomplete. NIP-01 does not provide a universal cursor. Timestamp pagination
must account for multiple events sharing a timestamp, deduplicate overlapping
pages, and report saturation if it cannot exhaust a timestamp bucket. `EOSE`
means the relay completed that subscription's stored response, not that every
historical event is available. Never present a capped first page as all records.

## Local Matching Rules

For each valid GTIN candidate, compare every qualifier present in the scan:

| Scanned field | Required anchor field | Match |
| --- | --- | --- |
| GTIN | `g` | Exact canonical 14-digit value |
| Lot | `gs1_lot` | Exact string |
| Expiry | `gs1_expiry` | Exact validated six-digit value |
| Serial | `gs1_serial` | Exact string |
| Digest, if supplied by a link | `o` | Same normalized SHA-256 digest |

All supplied constraints MUST match within the same anchor. A missing required
qualifier is **incomplete**, not an exact match; a different value is a
**mismatch**. Do not silently fall back to GTIN-only matching when a scan supplied
lot and expiry. General product records MAY appear separately, labelled as such.

If the anchor has qualifiers absent from the scan, classify it as a
**more-specific candidate**: the scan cannot establish that those additional
qualifiers apply. A GTIN-only scan may therefore return multiple lots without
claiming that any one lot is the item scanned. A candidate is an **exact field
match** only when the supported product qualifiers on both sides correspond.

For the worked scan:

| Anchor lot | Anchor expiry | Result, assuming same GTIN and no serial |
| --- | --- | --- |
| `693773` | `270131` | Exact field match |
| `693774` | `270131` | Lot mismatch |
| `693773` | `270228` | Expiry mismatch |
| `693773` | absent | Incomplete |
| absent | absent | General product record, not a lot/expiry match |

Matching is not recognition. Preserve all matching candidates, including
different publishers, document types, versions, and digests. Never select the
first response or newest timestamp as authoritative merely because it matches.
Apply the application's explicit issuer-recognition and record-selection rules,
or ask the user to select while displaying the differences.

## Separate Anchors For Lots And Expiry Combinations

Different `(GTIN, lot, expiry)` combinations MAY have separate regular kind 1415
anchor events. This tuple is a discovery and matching key, not a uniqueness rule
or a replaceable event slot. Multiple anchors for one tuple are also possible.

Each anchor's `o` identifies its exact artifact. Different certificates normally
have different digests. If the same artifact applies to multiple lots, separate
anchors MAY associate that same digest with different tuples. The signed tags
assert the association; they do not prove that the identifiers are written in
the document. In-document correspondence requires separate domain validation.

## Artifact Retrieval And Presentation

After matching, obtain the selected candidate's artifact using its `o` digest,
verified Blossom hints, and configured retrieval sources. Independently hash the
returned bytes. Preserve the complete candidate event and signer attribution.
Do not fetch every candidate's potentially large artifact automatically; apply
selection, size limits, cancellation, and existing SSRF protections first.

Show the parsed GTIN, lot, expiry and serial; candidate match status; publisher;
artifact digest; retrieval/verification result; and query coverage. Keep field
matching, signature verification, issuer recognition, and expiry assessment
distinct. Use “No matching anchor found in the queried relays,” not “No record
exists.” An expired product association remains discoverable evidence.

A raw GS1 scan contains no artifact commitment. Its digest is learned from the
selected signed anchor. A digest-bearing scan supplies an additional expected
artifact commitment. Neither mode alone proves physical authenticity or title.

## Safebox Web Implementation Checklist

1. Extend scanner decoding to retain symbology and GS1 separators alongside QR URLs.
2. Introduce a tested GS1 parsing adapter returning raw payload, GTIN, optional
   lot/expiry/serial, optional digest, and diagnostics.
3. Add bounded multi-relay `#g` discovery and coverage reporting using Stroma.
4. Validate and deduplicate events, then apply the local matching rules above.
5. Present candidates without silently accepting unknown issuers or incomplete matches.
6. Reuse digest-based artifact retrieval and verification after candidate selection.
7. Add publication support for `gs1_expiry` where an issuing workflow needs it.
8. Keep the current digest-link and non-GS1 acquisition paths working.

OpenQR currently publishes `g`, lot, and serial and resolves digest links.
This spec adds an expiry convention and GTIN discovery workflow; it does not
automatically add those features to OpenQR's forms, parser, or Digital Link URLs.
GS1 Digital Link AI 17 is a query attribute; adding support must preserve existing
`d`/`digest` handling and explicitly update that parser's accepted parameters.

## Acceptance Tests

- The worked scan yields the exact GTIN, lot and expiry above, without a serial.
- GS1 fields in other permitted orders parse correctly; variable-length fields
  followed by fields require preserved separators. Ambiguous stripped input fails.
- UPC/EAN normalization preserves zeroes, validates check digits, and handles UPC-E.
- Wrong GTIN, invalid signature, duplicate tags, conflicting aliases, malformed
  dates, and duplicate supported AIs cannot produce an accepted field match.
- Same GTIN with different lot/expiry anchors yields only the matching tuple as exact.
- Missing qualifiers remain incomplete; extra qualifiers remain more-specific.
- Multiple exact matches remain visible; no first-result or newest-event trust shortcut.
- Relay duplicate events collapse by event ID; timeout, truncation and same-time
  pagination saturation are reported as potentially incomplete discovery.
- Artifact digest mismatch fails byte verification; matching bytes do not by
  themselves promote an unknown publisher to a recognized issuer.
- Existing digest links continue to work, and conflicting scanned digests fail.

## References

- [OpenETR Nostr wire format](OPENETR_NOSTR_WIRE_FORMAT_SPEC.md#optional-gs1-product-association)
- [GS1 content-addressed information design note](GS1_DIGITAL_LINK_CONTENT_ADDRESSED_PRODUCT_INFORMATION_DESIGN_NOTE.md)
- [GS1 Application Identifiers](https://ref.gs1.org/ai/)
- [GS1 retail implementation guidance, including date rules](https://ref.gs1.org/guidelines/2d-in-retail/)
- [GS1 Digital Link URI syntax](https://ref.gs1.org/standards/digital-link/uri-syntax/)
- [GS1 Barcode Syntax Engine](https://github.com/gs1/gs1-syntax-engine)
- [NIP-01 filters and subscriptions](https://github.com/nostr-protocol/nips/blob/master/01.md)
