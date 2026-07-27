# Apostille Documents Domain Adapter Specification

This specification describes an OpenETR domain adapter for Apostille document workflows.

It is intended to support Apostille-related evidence, portability, verification, and archival workflows without claiming that OpenETR issues Apostilles, replaces Competent Authorities, or decides legal recognition under the HCCH 1961 Apostille Convention.

## Status

Draft.

## Purpose

The Apostille Documents domain adapter lets OpenETR represent apostilled document packages as digest-identified controllable records.

The adapter should make Apostille workflows inspectable by linking:

- the public document
- the Apostille certificate or e-Apostille
- issuing Competent Authority metadata
- e-Register references
- verification evidence
- replacement, correction, revocation, or warning evidence
- certified translations or related legalization artifacts, where applicable

The compact design goal is:

```text
OpenETR should preserve portable signed evidence about an apostilled package.
Competent Authorities and recognition policies decide Apostille effect.
```

## Architectural Boundary

The Apostille domain adapter sits above the generic OpenETR control layer.

```text
Apostille domain adapter
  public document packages, Apostille metadata, Competent Authority references,
  e-Register links, verification events, replacement/correction workflows

OpenETR control layer
  digest identity, origin records, linked evidence records, attestations,
  graph traversal, verifier warnings

Wire format
  signed events, event kinds, tags, object queries, relay retrieval

Recognition layer
  Apostille Convention rules, Competent Authority practice, e-Register checks,
  receiving-state policy, institutional verifier policy, courts, agencies
```

OpenETR may verify signatures and preserve evidence. It does not decide:

- whether a document is a public document under the Convention
- whether a particular authority is competent for that document class
- whether an Apostille is legally valid in a receiving jurisdiction
- whether a receiving institution must accept a document
- whether a paper or electronic Apostille has been properly issued under local procedure

Those are recognition-layer questions.

## Domain Model

The adapter should distinguish the following concepts.

### Public Document

The public document is the underlying document for which an Apostille is issued.

Examples may include:

- birth certificate
- marriage certificate
- court document
- notarial act
- educational record
- corporate registry extract
- public authority certificate
- certified copy

OpenETR should not decide whether a document qualifies as a public document for Apostille purposes.

### Apostille Certificate

The Apostille certificate is the authority-issued certificate attached to, associated with, or logically linked to the public document.

In an electronic workflow, it may be:

- a digitally signed e-Apostille
- an embedded certificate page in a PDF package
- a detached or sidecar certificate
- a machine-readable record associated with an e-Register entry
- a paper certificate represented by a scanned or digitized package

### Apostilled Document Package

The apostilled document package is the OpenETR-facing artifact.

It may include:

- the public document
- the Apostille certificate
- metadata describing the issuing authority
- registry lookup number or URL
- verification artifacts
- translations or related certifications
- packaging metadata

The package is the preferred starting-point Controlled Object.

### Competent Authority

A Competent Authority is a designated authority of a Contracting Party that may issue Apostilles.

In OpenETR, a Competent Authority should be modeled as a recognized issuer, attestor, registry source, or recognition input. It should not be treated as a generic user profile without authority context.

### e-Register

An e-Register is an online register used to verify Apostilles issued by a Competent Authority.

An OpenETR graph may link to an e-Register reference, but should not imply that the OpenETR graph replaces the e-Register.

## Controlled Object Model

The recommended first implementation treats the full apostilled document package as the Controlled Object.

```text
apostilled document package
  -> canonical package bytes
  -> SHA-256 digest
  -> OpenETR origin record
  -> linked authority, registry, verification, and lifecycle evidence
```

This model is intentionally artifact-centric.

It lets a verifier answer:

- Is this the same package that was recorded?
- What evidence is linked to this package?
- Which authority or registry references are associated with it?
- Has the package been superseded, corrected, warned, or revoked under a recognized policy?

It avoids forcing OpenETR to parse every possible Apostille certificate format.

## Alternative Object Models

Some deployments may need more granular object models.

### Public Document As Primary Object

The underlying public document may be the primary Controlled Object, with Apostille certificates modeled as linked evidence.

```text
public document digest
  -> OpenETR origin
  -> linked Apostille evidence
  -> linked verification evidence
```

This can be useful where the same public document may receive multiple Apostilles, translations, or recognition artifacts over time.

### Apostille Certificate As Primary Object

The Apostille certificate itself may be the primary Controlled Object.

```text
e-Apostille bytes
  -> digest
  -> authority attestation graph
```

This can be useful for authority-operated e-Register mirrors or audit systems.

### Bundle Graph

A mature profile may model the public document, Apostille certificate, translation, and e-Register response as separate digest-identified objects linked by evidence records.

```text
public document object
  -> apostille certificate object
  -> e-register verification object
  -> translation object
  -> recognition decision object
```

This is more expressive, but it requires stronger profile rules for linking, display, and recognition.

## Recommended Starting Point

Use the apostilled document package as the Controlled Object.

That approach is simpler for early adoption because:

- the relying party usually receives a document package, not a graph of separate files
- whole-package integrity is easy to explain and recompute
- the package can contain paper-derived, PDF, or e-Apostille material
- the graph can still link to official e-Register evidence
- future profiles can add granular linked objects without changing the base pattern

## Domain Roles

The adapter should distinguish OpenETR profiles from Apostille-domain roles.

Relevant roles may include:

- document holder
- requesting party
- issuing public authority
- notary or certifying official
- Competent Authority
- e-Register operator
- verifier
- receiving institution
- translator
- legalization authority, where applicable outside the Apostille Convention flow
- archive or custodian

OpenETR profile keys may represent these actors, but legal or institutional authority must be established by recognition policy or trusted authority data.

## Domain Actions

The adapter should expose Apostille-domain actions rather than generic database operations.

| Domain action | OpenETR mapping |
| --- | --- |
| Create package draft | Domain-system action outside OpenETR |
| Validate package completeness | Domain validation / possible verifier annotation |
| Record package origin | OpenETR `ISSUE` / origin record |
| Attach Apostille evidence | OpenETR linked evidence or `ATTEST` |
| Attach Competent Authority reference | Linked evidence, authority metadata, or recognition input |
| Attach e-Register reference | Linked evidence / registry reference |
| Record verification check | OpenETR `ATTEST` or linked evidence record |
| Record corrected package | New object plus supersession link |
| Record replacement package | New object plus replacement link |
| Record warning or invalidity notice | Authority `ATTEST`, warning event, or policy annotation |
| Record revocation or withdrawal notice | Authority `ATTEST` or domain-specific revocation profile |
| Archive package | Linked evidence / lifecycle attestation |
| Terminate reliance on package | OpenETR `TERMINATE` or policy-level non-recognition, depending on profile |

Many Apostille workflows do not require transfer of control. The adapter should not force transferable-record semantics where the domain only needs authority, evidence, status, and verification.

## Suggested Event Tags

The adapter may use signed structured tags to make Apostille evidence discoverable.

### Origin Record Tags

Recommended tags for the origin record:

- `["domain", "apostille"]`
- `["document_type", "apostilled_document_package"]`
- `["record_reference", "<local_package_or_case_reference>"]`
- `["record_description", "<short_description>"]`
- `["package_digest", "<sha256_digest>"]`
- `["package_media_type", "<iana_media_type>"]`
- `["jurisdiction", "<issuing_jurisdiction_or_country_code>"]`
- `["apostille_convention", "hcch-1961"]`

### Apostille Evidence Tags

Recommended tags for linked evidence or attestation records:

- `["evidence_type", "apostille_certificate"]`
- `["apostille_number", "<certificate_number>"]`
- `["apostille_date", "<date>"]`
- `["competent_authority", "<authority_identifier_or_name>"]`
- `["competent_authority_jurisdiction", "<jurisdiction>"]`
- `["public_document_type", "<document_type>"]`
- `["public_document_issuer", "<issuer_identifier_or_name>"]`
- `["public_document_date", "<date_if_applicable>"]`

### e-Register Tags

Recommended tags for registry references:

- `["evidence_type", "apostille_eregister_reference"]`
- `["eregister_url", "<official_lookup_url>"]`
- `["eregister_reference", "<lookup_number_or_identifier>"]`
- `["eregister_authority", "<authority_identifier_or_name>"]`
- `["verification_time", "<iso8601_or_unix_time>"]`
- `["verification_result", "matched" | "not_matched" | "unavailable" | "warning"]`

### Lifecycle Tags

Recommended tags for replacement, correction, warning, or revocation evidence:

- `["action", "replace" | "correct" | "warn" | "revoke" | "verify"]`
- `["supersedes", "<prior_object_digest_or_event_id>"]`
- `["replacement_for", "<prior_object_digest_or_event_id>"]`
- `["reason", "<reason_code_or_short_text>"]`
- `["effective_time", "<iso8601_or_unix_time>"]`
- `["authority_event", "<authority_event_id_if_any>"]`

These tags are profile suggestions. Production deployments should define stable controlled vocabularies and validation rules.

## Verification Model

A verifier should separate technical verification from recognition.

### Technical Checks

Technical checks include:

- recompute the package digest
- verify OpenETR event signatures
- retrieve the object graph
- verify linked evidence digests
- verify exact object references
- verify authority event signatures where authority events are represented in OpenETR
- check for replacement, warning, revocation, or termination events under the selected policy

### Apostille Checks

Apostille checks include:

- verify the Apostille certificate or e-Apostille signature, where applicable
- check the official e-Register where available
- verify the certificate number and date
- verify the issuing Competent Authority
- verify the public document description or metadata
- verify whether the certificate has been corrected, replaced, revoked, withdrawn, or marked invalid by an official source

### Recognition Checks

Recognition checks include:

- determine whether the authority is competent for the document class
- determine whether the issuing and receiving jurisdictions are in scope
- determine whether the receiving institution accepts the evidence
- determine whether translations, notarizations, certified copies, or additional steps are required
- determine whether a warning or registry mismatch blocks reliance

OpenETR should present these checks separately.

A package digest can match while the Apostille is not recognized. An Apostille can verify while the presented package is not the same package that was recorded in OpenETR.

## Status Dimensions

The adapter should avoid one overloaded status field.

Recommended status dimensions include:

### Package Status

Examples:

- `DRAFT`
- `RECORDED`
- `SUPERSEDED`
- `REPLACED`
- `ARCHIVED`

### Apostille Status

Examples:

- `NOT_ATTACHED`
- `ATTACHED`
- `E_APOSTILLE_SIGNED`
- `PAPER_APOSTILLE_REPRESENTED`
- `CORRECTED`
- `REPLACED`
- `REVOKED`
- `WARNING`

### Registry Verification Status

Examples:

- `NOT_CHECKED`
- `MATCHED`
- `NOT_MATCHED`
- `UNAVAILABLE`
- `INCONCLUSIVE`

### Recognition Status

Examples:

- `NOT_EVALUATED`
- `RECOGNIZED`
- `RECOGNIZED_WITH_WARNINGS`
- `NOT_RECOGNIZED`
- `REQUIRES_MANUAL_REVIEW`

The OpenETR graph can support status derivation, but the status meanings are domain policy choices.

## Package Integrity And Canonicalization

The domain adapter should define what bytes are hashed.

For a PDF package, the digest should be computed after:

- the public document is attached or embedded
- the Apostille certificate is attached or embedded
- electronic signatures are applied
- metadata is finalized
- any QR codes, visible seals, or verification pages are generated
- the distribution package is complete

If an archive package is used, the profile should define:

- archive format
- file ordering
- compression behavior
- metadata inclusion
- filename normalization
- character encoding
- timestamp normalization

Without package rules, two systems may assemble semantically equivalent packages that hash differently.

## Replacement And Correction

An Apostille package may be corrected, replaced, withdrawn, or superseded.

The adapter should not overwrite prior packages.

Recommended pattern:

```text
old package digest
  -> origin / evidence graph
  -> replacement or correction event
  -> new package digest
  -> new origin / evidence graph
```

The verifier should show:

- the original package
- the new package
- the relationship between them
- who asserted the replacement
- whether the asserting party is recognized
- the policy outcome

## Privacy And Data Minimization

Apostille packages may contain personal, sensitive, educational, civil-status, court, immigration, corporate, or notarial information.

OpenETR should avoid publishing unnecessary contents or personal data to public relays.

Recommended patterns include:

- publish digest and metadata only
- keep document bytes in controlled storage
- use private or permissioned relays where appropriate
- link to official authority or e-Register sources without copying personal data
- record verification result metadata without exposing document content
- use redacted evidence packages where policy permits

The graph should preserve evidence, not become an unnecessary public dossier.

## Non-Goals

The Apostille domain adapter should not make OpenETR responsible for:

- issuing Apostilles
- operating official e-Registers
- replacing Competent Authorities
- deciding Convention scope
- determining receiving-state acceptance
- certifying public-document authenticity
- certifying translations
- legalizing documents outside the Apostille workflow
- storing sensitive document contents on public infrastructure

Those matters belong to Competent Authorities, official registries, local law, treaty practice, receiving institutions, and verifier policy.

## Recommended Roadmap

A practical implementation should proceed in stages.

1. Treat the full apostilled document package as an opaque digest-identified Controlled Object.
2. Define origin-record tags for `domain=apostille`, package reference, jurisdiction, document type, and media type.
3. Add linked evidence records for Apostille certificates, e-Register references, verification checks, translations, and related certifications.
4. Add verifier-policy warnings for unknown authority, missing e-Register reference, registry mismatch, superseded package, revoked Apostille, and stale verification.
5. Add private-storage and relay guidance for sensitive documents.
6. Define a granular bundle graph only after package, privacy, authority, and recognition rules are stable.

## Open Questions

Further design work should decide:

- whether authority metadata should be represented as OpenETR profile records, linked evidence records, or external trust-registry inputs
- whether e-Register checks should be signed as OpenETR attestations by verifiers
- how to model paper Apostilles that have been scanned into electronic packages
- how to represent certified translations and downstream legalization steps
- whether package-level or document-level digesting should be preferred for particular jurisdictions
- how to distinguish official revocation, correction, withdrawal, expiry, and verifier warning states
- which tags should become mandatory for an Apostille domain profile

## References

- HCCH Apostille Section: https://www.hcch.net/en/conventions/causes/specials/apostille
- HCCH electronic Apostille Programme FAQ: https://www.hcch.net/en/publications-and-studies/details4/?pid=5576
- HCCH 1961 Apostille Convention
- [CONTROLLABLE_RECORDS_TAXONOMY.md](./CONTROLLABLE_RECORDS_TAXONOMY.md)
- [LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md](./LINKED_EVIDENCE_RECORD_KIND_DESIGN_NOTE.md)
