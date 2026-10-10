# GS1 Digital Link And Content Addressed Product Information

## Status And Scope

Design and analysis note, 10 October 2026. Describes the implemented OpenQR
artifact-link model and a proposed structured-product-record extension. It does
not allocate GS1 identifiers, define a new event kind, or claim GS1 certification.

The [policy brief](https://trbouma.github.io/openetr/policy-briefs/gs1-digital-link-and-verifiable-product-information/)
provides the public-policy overview. The
[OpenQR implementation note](https://github.com/trbouma/openqr/blob/main/docs/GS1_DIGITAL_LINK_IMPLEMENTATION_NOTE.md)
documents exact FastAPI behaviour and validation boundaries.

## Complementary Responsibilities

GS1 Digital Link provides product identification in a web-compatible form.
A compatible checkout application extracts the identifiers; a consumer browser
opens the web resource. OpenETR adds signed evidence concerning an exact digital
artifact rather than replacing the retail identification system.

| Concern | Mechanism | Limit |
| --- | --- | --- |
| Product identification | GTIN and optional lot/serial | Requires appropriate allocation and usage |
| Convenient navigation | HTTPS resolver domain | Availability and operation depend on that service |
| Artifact byte identity | SHA-256 digest | Does not guarantee retrieval or truth |
| Attribution of an association | Signed OpenETR anchor | Identifies a signing key, not automatically an authorized producer |
| Presentation | Browser, OpenQR, or another reader | Codec and document support vary |
| Recognition and consequence | Integrator's accepted evidence and rules | Not supplied by the barcode alone |

The distinction between symbology and payload matters: QR is the visual carrier;
GS1 Digital Link is the URL convention. The chosen approach uses an ordinary QR
generator, not FNC1-based GS1 QR mode. Scanner readiness and printed-symbol
requirements still need validation. See [GS1 URI syntax](https://ref.gs1.org/standards/digital-link/uri-syntax/1.7.0/)
and [retail guidance](https://ref.gs1.org/guidelines/2d-in-retail/).

## URL And Digest Convention

Illustrative template:

```text
https://example.com/01/{gtin}/10/{lot}/21/{serial}?d={digest}
```

Generated links use `d`, saving five ASCII bytes. The descriptive `digest` alias
remains supported for existing links and authors who prefer it. Readers accept
exactly one occurrence of either name, never both, even if their values match.
Both accept the same digest encodings; generation and redirects use `d`.

Lot and serial segments are optional. `d` (alias `digest`) is an OpenQR application extension,
not a newly defined GS1 Application Identifier. Its generated value is:

```text
base64url_without_padding(SHA-256(exact_artifact_bytes))
```

The 32-byte digest becomes 43 characters. OpenQR also accepts lowercase hex on
input and normalizes to hex for the `o` event tag and relay filter. No reserialization,
transcoding, or normalization is applied to the artifact before hashing.

The digest is not the GS1 serial: AI 21 is limited to 20 characters, and a document
can legitimately describe many product instances. Product identity and content
version identity must not be conflated.

This is a custom direct-resolution extension under the
[OpenETR QR Resolver Profile](OPENETR_QR_RESOLVER_PROFILE_1_0.md), not its query-free
Standard Web Resolver Profile. The GS1 values identify the associated product,
not another OpenETR record. OpenQR currently supports only a bounded subset of
Digital Link syntax and is not a full GS1-conformant resolver.

## Implemented Binding Through The Anchor

For an uploaded video, datasheet, or other artifact, the anchor signs the
hexadecimal digest in `o` together with `gs1_gtin`, optional `gs1_lot`, and
optional `gs1_serial`. The event is kind 1415 with action `issue`.

```text
Exact artifact bytes -> artifact digest
Signed anchor -> artifact digest + GTIN + optional lot/serial
Digital Link -> same artifact digest + product identifiers
```

The artifact need not contain the identifiers. Their association with it is
committed by the signed event, not necessarily by the artifact hash itself.
Verification retrieves the bytes, checks the digest, verifies the anchor, and
compares the product fields. Putting a digest beside identifiers in a URL without
checking signed evidence would not establish their association.

The [wire format](OPENETR_NOSTR_WIRE_FORMAT_SPEC.md) supplies event identity and
signature rules. The application tags are structured publisher assertions, not
proof that GS1 assigned the identifier to the signer. OpenQR displays mismatches
without discarding independently verifiable artifacts or other candidate anchors.

## Proposed Binding Within A Product Record

A stronger content-level commitment can be obtained by making a structured
product record the artifact itself. An illustrative record could contain:

```json
{
  "profile": "example-product-record-draft",
  "gtin": "09520123456788",
  "lot": "LOT456",
  "serial": "ABC123",
  "resources": [
    {"role": "product-video", "sha256": "<full video digest>", "media_type": "video/mp4"},
    {"role": "datasheet", "sha256": "<full PDF digest>", "media_type": "application/pdf"}
  ]
}
```

This is a conceptual example, not an implemented schema. The GTIN is documentation
test data. A versioned schema, parsing rules, resource limits, and conformance tests
must be agreed before deployment.

Hash the exact finalized product-record bytes. Publish an ordinary signed anchor
whose `o` references that hash. The QR then carries the product-record digest, not
the video digest. This avoids making the record contain its own digest or hashing
a self-referencing signed anchor. The anchor signature remains separate from the
artifact hash.

Verification would:

1. Extract the expected record digest and product identifiers from the link.
2. Retrieve the exact product-record bytes and verify their hash before parsing.
3. Parse under the declared schema, rejecting ambiguous fields such as duplicate
   JSON keys, and compare the product identifiers with the URL.
4. Verify the anchor's event ID and signature and its reference to the record digest.
5. Apply issuer-recognition rules independently of signature correctness.
6. Retrieve referenced media as needed and verify each resource's own digest.

With this design, altering an identifier inside the record changes the digest;
altering only the URL's identifier fails the comparison. No separate signature
per identifier is needed. If canonical serialization is introduced later, the
profile must specify it; verifiers must not silently reserialize exact-byte artifacts.
OpenQR does not yet parse this proposed product-record schema.

## Resolution Without The Printed Domain

An aware reader can recover the digest from the scanned URL without making a
request to its host. It can query its chosen relays by `#o`, inspect signed anchors
and safe storage hints, and obtain the same bytes from another Blossom server,
an HTTPS mirror, a local cache, or an archive. A different website can present
the material without changing its identity.

This independence has prerequisites: the reader understands the extension,
has usable discovery sources, can obtain a copy, and can evaluate the relevant
signatures and recognition rules. A digest is not a global discovery service.
An ordinary phone camera normally follows the URL and does not perform this
alternative resolution automatically. Offline verification needs previously
obtained artifact bytes, evidence, and any required recognition material.

OpenQR implements configurable relay and Blossom pools, not arbitrary mirror
discovery. Additional reader integrations are an architectural possibility, not
a claim that every scanner or resolver already supports them.

## Independent Regulatory Acquisition And Certificate Verification

A regulator can implement a purpose-built acquisition application while consumers
continue using ordinary mobile QR cameras. The consumer camera opens the HTTPS
URL; the regulatory reader parses the scanned text locally and need not contact
that URL's domain. GTIN, lot, serial, and digest become separate inputs to the
regulator's verification policy rather than an instruction to trust a website.

For a Certificate of Analysis, the proposed workflow is:

1. Acquire the barcode payload and validate its identifier and digest syntax.
2. Obtain the original certificate bytes from any permitted source, including a
   file already held by the regulator. Do not hash a screenshot, printed copy,
   extracted text, or regenerated PDF as if it were the original digital file.
3. Compute SHA-256 over those exact bytes and compare the normalized result with
   the barcode digest. A mismatch fails artifact correspondence regardless of
   whether the filenames or visible pages look alike.
4. Extract the certificate's GTIN, lot, and serial under a declared document
   schema or review procedure. Compare each required field with the barcode,
   preserving meaningful leading zeros and applying only defined normalization.
5. Retrieve relevant OpenETR anchors and associated evidence by digest and any
   applicable event references. Verify event IDs, signatures, and artifact links.
6. Validate any embedded or separately referenced signatures and seals under
   their applicable formats, then apply issuer-recognition and authority rules.
7. Evaluate any required correction, withdrawal, validity-period, or supersession
   evidence under the regulator's rules, reporting retrieval scope and limitations.

Two assertions must be distinguished: **these are the exact committed bytes**
and **these bytes contain the matching identifiers in the relevant fields**.
The second requires interpreting the document. A hash comparison alone cannot
perform it. Documents with multiple products, contradictory identifiers, missing
fields, or ambiguous OCR must not pass by a loose substring match. Structured
records can support deterministic field checks; ordinary PDF certificates need a
specified extraction profile or explicit human confirmation. Batch-level
certificates must not be presented as containing an item serial they do not state.

If the barcode digest identifies a product manifest rather than the certificate
itself, first verify and parse the manifest, then verify the certificate against
its referenced digest. The certificate digest must not be compared directly with
the manifest digest. An indirect reference must be made explicit in the result.

When the certificate itself is the hashed artifact, matching its bytes and fields
creates a cryptographically verifiable binding to the acquired barcode payload,
subject to the hash's security assumptions and correct parsing. It is not an
incontrovertible physical or legal fact: a barcode can be copied or replaced,
an issuer can make false assertions, and a valid certificate can later be withdrawn.

OpenETR signatures and any applicable associated evidence can be discovered using
the [wire-format conventions](OPENETR_NOSTR_WIRE_FORMAT_SPEC.md). Retrieval is not
equivalent to recognizing a seal. The [electronic seals design note](ELECTRONIC_SEALS_DESIGN_NOTE.md)
distinguishes proposed sealing profiles from implemented core signature verification.
An integration must specify how a seal or external signature is referenced, what
bytes it covers, what validation material is needed, and whose authority is accepted.
Finalized embedded signatures or seals are part of the exact bytes being hashed;
adding one later changes the artifact digest.

Current OpenQR supports digest lookup, byte verification, anchor-signature checks,
and comparison with signed GS1 tags. Automated certificate field extraction,
external signature/seal validation, and this regulator-specific evaluation workflow
are integration work, not existing OpenQR functionality. A future regulatory pilot
should test independent acquisition from a held file as well as retrieval with
the printed domain unavailable.

## Visual Confirmation And Optional Identity Applications

A product record may include a photograph to support visual inspection. The
photograph must be embedded in the exact hashed artifact or referenced by digest
from a verified manifest. A mutable image URL alone does not bind the displayed
image to the record. For a referenced image, verify its bytes against its own
digest before rendering; preserve the distinction between the manifest digest
and the image digest.

The record should identify whether the image depicts a product model, a batch,
or the particular serialized item, and state any asserted capture context. An
inspector can compare packaging, markings, and visible characteristics with the
verified image. Report artifact integrity, identifier correspondence, issuer
recognition, and visual assessment separately. A matching photograph does not
prove provenance, unseen properties, or that the label has not been copied.

As an optional extension outside this product scenario, a passport- or
driver's-licence-related record could contain a portrait or biometric template.
An officer could manually compare the portrait with its presenter; compatible
software could assist portrait comparison or compare a newly acquired biometric
sample with the verified template. A template is not necessarily a viewable image
and requires a declared format and compatible comparison process.

Such an integration would need to define:

- The exact artifact bytes, image or template references, and signature coverage.
- Recognition of the issuing authority and checks for expiry, revocation, or
  supersession under the applicable rules.
- Capture and comparison procedures, uncertainty reporting, human review, and
  safeguards against replay or other presentation attacks where required.
- Access authorization, encryption where appropriate, retention limits, and
  controls on disclosure and cross-context correlation.

Do not put personal images or biometric templates into public relay events or
publicly retrievable storage by default. A digest does not conceal accessible
content, establish consent, or anonymize a person. Protected retrieval can still
allow an authorized verifier to check the bytes independently. A digest match
verifies reference material, while a biometric or visual match is a distinct
assessment with its own limitations; neither alone establishes legal identity.

These examples illustrate an extensible verification architecture. They do not
define a new identity-document standard, require GS1 identifiers for people, or
claim that OpenQR currently implements biometric comparison or identity checks.

## Physical Trade And Tamper-Evident Attachment

Independent document verification can reduce uncertainty in physical trade and
help participants concentrate inspection on correspondence between the verified
record and the goods presented. It does not reduce every trade risk to a physical
match: issuer authority, record currency, quality claims, and transaction rules
remain separate considerations.

A tamper-resistant sticker bearing the barcode is one possible attachment
mechanism. An integration should specify the item or packaging to which it is
attached, who applies it, and how inspectors assess removal or replacement.
Destructible and tamper-evident features can reveal interference; they should not
be described as tamper-proof or as making the printed payload uncopyable.

A physical-trade pilot should test:

- Controlled label application and correspondence with the item's serial number.
- Inspection of label condition alongside verified photographs and identifiers.
- Removal, copying, substitution, and opening or replacement of labelled packaging.
- Recording handover observations, including who inspected what and when, where
  the integration requires attributable inspection evidence.
- Legitimate repackaging or relabelling, with explicit rules for preserving the
  relationship to earlier records rather than silently reusing an old label.

A package-level seal does not by itself prove its contents or establish title.
Report digital verification and physical inspection outcomes separately. No new
OpenETR action or transfer ruleset is introduced by this attachment convention.

## Comparison With Existing Campaign Links

| Property | `/{campaign}/{digest}` | GS1 Digital Link |
| --- | --- | --- |
| Digest location | Path | `d` query parameter (`digest` also accepted) |
| Product identifiers | Not in URL | GTIN, optional lot/serial |
| Dispatch | Campaign passed through; currently no campaign rules | Default `etr` handler |
| Evidence lookup | Kind 1415 plus `#o` | Same |
| Indirection database | Not needed | Not needed |
| Product-association check | Not requested by URL | Compared with signed GS1 tags |
| Retail meaning | No standard GTIN structure | Interpretable by compatible GS1 systems |

Neither current route is an opaque campaign-token mapping. Both carry the digest
directly and converge on the same lookup and rendering functions. Incoming GS1
fields are validated before the lookup; they do not become relay filter keys.

## Operational And Policy Boundaries

Changing file bytes produces a new digest. The printed code remains committed to
the old version. A later correction, withdrawal, or supersession therefore needs
separate evidence and explicit rules; anchor discovery alone is not a current-state
determination. Selective or incomplete relay responses can omit relevant notices.

Replication improves availability but is not guaranteed by signatures. Access
restrictions remain necessary for confidential information; public QR codes and
public storage should not expose private product or customer data inadvertently.

A copied label yields the same valid references as the original. Label replacement
can substitute an entirely different digest and signing key. Recognition, physical
anti-counterfeit measures, and any ownership or redemption rules remain separate.
An ordinary point-of-sale scan does not constitute an OpenETR control transfer.

For small labels, the additional URL data increases symbol density. Test the actual
payload, print process, margins, error correction, bottle curvature, and scanner
population. A scratch-off label intended for post-purchase access may need to be
separate from the visible checkout code. See the
[production design note](OPENETR_QR_PRODUCTION_AND_SCRATCH_OFF_DESIGN_NOTE.md).

## Pilot Acceptance Criteria

1. Verify GS1 identifier allocation and test checkout behaviour with the retailer.
2. Confirm native phone navigation and artifact rendering for intended formats.
3. Verify signed product associations and reject altered or duplicate identifiers.
4. Retrieve and verify the same bytes with the printed domain unavailable.
5. Test missing copies, unavailable relays, conflicting assertions, and replaced labels.
6. Define version and later-notice handling before making current-status claims.

The intended outcome is provider-independent verification of product information,
not an assertion that cryptography alone establishes product truth or legal effect.
