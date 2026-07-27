# OpenETR and C2PA Design Note

This note describes how OpenETR can complement C2PA content provenance.

The purpose is not to replace C2PA or to treat whole-file digesting as a substitute for provenance verification. The useful design question is narrower:

> How can OpenETR provide final-artifact integrity evidence for a file that may already carry C2PA provenance?

## Summary

OpenETR and C2PA operate at different layers.

C2PA is a content provenance framework. It attaches, embeds, or references a signed manifest that describes provenance assertions about a media asset or document.

OpenETR is a control and evidence graph for digest-identified records. It can record a digest of a finalized artifact and then associate signed lifecycle events, control events, and linked evidence with that digest.

The compact model is:

```text
C2PA:
content -> manifest/assertions/signature -> provenance verification

OpenETR:
final artifact bytes -> digest -> signed object-centric evidence graph
```

Used together:

```text
C2PA explains where the content came from.
OpenETR proves which finalized artifact is being relied on.
```

## Design Boundary

C2PA answers provenance questions.

Examples include:

- who or what created the content
- what edits or transformations occurred
- which assertions are attached to the content
- whether the manifest is signed
- whether protected content still matches the manifest
- whether the C2PA certificate or trust chain is acceptable to a relying party

OpenETR answers object and control evidence questions.

Examples include:

- what exact file was recorded
- what digest identifies that file
- which signer created the origin record
- what control events or linked evidence records reference that object
- whether the same file can later be recomputed to the same digest
- what candidate control or evidence graph exists for that object

The Recognition Layer remains separate from both.

It decides:

- whether the C2PA signer is trusted
- whether the C2PA assertions are sufficient
- whether the OpenETR signer is recognized
- whether an OpenETR event has legal, commercial, operational, or institutional effect
- whether a mismatch, missing manifest, revoked certificate, or altered file blocks recognition

## Final-Artifact Digest Pattern

The recommended OpenETR pattern is to digest the final packaged file after C2PA processing is complete.

The sequence is:

1. Generate or assemble the document, image, video, dataset, or other asset.
2. Apply any document signatures, visible digital seals, Verifiable Credentials, QR elements, or domain-specific trust features.
3. Add, embed, or reference the C2PA manifest.
4. Sign the C2PA manifest.
5. Finalize the file package.
6. Compute the OpenETR digest over the final artifact bytes.
7. Publish or preserve an OpenETR origin, control, or linked evidence record for that digest.

The important ordering rule is:

```text
C2PA finalization first.
OpenETR digesting second.
```

If the file changes after the OpenETR digest is recorded, the digest should no longer match. That is expected and should be treated as evidence that the presented artifact is not byte-for-byte identical to the recorded artifact.

## Possible Event Usage

OpenETR can use different event patterns depending on whether the C2PA-enabled file is itself the controlled object or supporting evidence for another controlled object.

### C2PA File As Controlled Object

If the C2PA-enabled artifact is the primary record, the artifact digest may be used directly as the OpenETR Controlled Object identifier.

Example:

```text
final-c2pa-enabled.pdf
  -> sha256(final-c2pa-enabled.pdf)
  -> OpenETR origin event
  -> later control or evidence events
```

This is appropriate where the artifact itself is the record being issued, transferred, presented, or relied on.

### C2PA File As Linked Evidence

If the C2PA-enabled artifact supports another controlled object, it should be modeled as linked evidence.

Example:

```text
warehouse-receipt.pdf
  -> controlled object digest
  -> OpenETR control graph

inspection-photo-with-c2pa.jpg
  -> evidence artifact digest
  -> linked evidence record referencing the warehouse receipt object
```

This is appropriate where C2PA helps prove provenance of supporting content, such as inspection photos, compliance documents, product lifecycle media, repair evidence, or certification artifacts.

## Suggested Metadata

An OpenETR event should not need to parse or duplicate the full C2PA manifest.

Where helpful, an event may include structured references such as:

- `["artifact_digest", "<sha256_digest>"]`
- `["artifact_media_type", "<iana_media_type>"]`
- `["c2pa", "present"]`
- `["c2pa_manifest_digest", "<digest_if_known>"]`
- `["c2pa_manifest_location", "embedded" | "sidecar" | "remote"]`
- `["c2pa_verifier", "<tool_or_policy_identifier>"]`
- `["c2pa_verification_time", "<iso8601_or_unix_time>"]`
- `["c2pa_verification_result", "valid" | "invalid" | "not_checked" | "warning"]`
- `["recognition_policy", "<policy_identifier>"]`

These tags should be treated as evidence metadata, not as a replacement for C2PA verification.

The verifier should still validate the C2PA manifest with C2PA-aware tooling where C2PA provenance is relevant to recognition.

## Verification Model

A relying party should perform two independent checks.

### C2PA Check

The C2PA check verifies provenance.

It should determine:

- whether a C2PA manifest is present or referenced
- whether protected content matches the manifest
- whether the manifest signature validates
- whether the signer certificate or trust chain is acceptable
- whether the assertions satisfy the relevant policy

### OpenETR Check

The OpenETR check verifies final-artifact identity and graph evidence.

It should determine:

- whether the presented artifact hashes to the recorded OpenETR digest
- whether the OpenETR event signatures are valid
- whether the object graph can be retrieved and traversed
- whether linked evidence records point to the expected object
- whether the selected verifier policy recognizes the relevant events

The checks are complementary.

A C2PA check may pass while the OpenETR digest fails if the file is C2PA-valid but not the exact artifact recorded by OpenETR.

An OpenETR digest may pass while the C2PA check fails if the file is byte-identical to the recorded artifact but the C2PA manifest is missing, invalid, untrusted, or insufficient under policy.

## Assessment Matrix

| Question | C2PA | OpenETR |
| --- | --- | --- |
| What is the provenance of this content? | Strong fit | Not the primary role |
| Who signed the provenance record? | Strong fit | Not the primary role |
| What assertions are attached to the content? | Strong fit | Not the primary role |
| Has protected content changed relative to the manifest? | Strong fit | Indirectly, through whole-file digest mismatch |
| Is this exact final artifact unchanged? | Depends on packaging and verifier behavior | Strong fit |
| Can verification work without parsing the file internals? | No, requires C2PA-aware tooling | Yes, for digest identity |
| Can evidence be linked into a broader object lifecycle graph? | Not by itself | Strong fit |

## Risks And Caveats

### Digest Timing

The OpenETR digest must be computed after all C2PA embedding, signing, packaging, compression, metadata writing, and export steps are complete.

If a workflow computes the digest too early, later legitimate C2PA or packaging operations will break the digest match.

### Metadata Stripping

C2PA manifests and file metadata can be affected by export, upload, download, optimization, sanitization, or platform transformation tools.

Some systems strip metadata, especially from images and video. A workflow that depends on C2PA evidence should explicitly test each transport and storage step.

### Trust Separation

A matching OpenETR digest does not prove that C2PA assertions are true.

It proves only that the presented bytes match the bytes that were recorded.

Similarly, a valid C2PA manifest does not prove that the artifact is the same final package that an OpenETR event recorded, unless the OpenETR digest is recomputed and matched.

### Transformations

Some workflows intentionally transform files after creation, for example by rendering, compressing, flattening, redacting, optimizing, or wrapping them.

Such workflows should define whether:

- every transformation creates a new OpenETR object
- transformations are modeled as linked evidence
- only a final distribution package is digest-recorded
- transformed derivatives are outside the recognized artifact set

## Recommended Policy Position

OpenETR should treat C2PA as a provenance input, not as a competing control layer.

C2PA provides embedded or attached provenance for content.

OpenETR provides external final-artifact integrity and object-centric graph evidence.

The recommended policy framing is:

```text
C2PA records content provenance.
OpenETR records final-artifact identity and control evidence.
Recognition policy decides what effect to give both.
```

This approach is especially useful where a relying party needs to know both:

- what a digital document or media asset claims to be
- whether the exact final artifact being presented is the artifact that was recorded

## Open Questions

Further design work should decide:

- whether OpenETR should define a standard `c2pa` tag family
- whether C2PA verification results should be signed as OpenETR attestation events
- whether C2PA manifest digests should be recorded separately from whole-file digests
- how sidecar manifests should be represented in linked evidence records
- how verifier policy should distinguish `c2pa_missing`, `c2pa_invalid`, `c2pa_untrusted`, and `c2pa_not_required`
- whether domain profiles such as MLWR or Product Passports should require C2PA for particular classes of evidence

