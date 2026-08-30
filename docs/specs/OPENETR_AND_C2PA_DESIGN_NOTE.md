# OpenETR and C2PA Design Note

This note describes how OpenETR can complement C2PA content provenance.

The purpose is not to replace C2PA or to treat whole-file digesting as a
substitute for provenance verification. The useful design question is:

> How can C2PA provenance evidence participate in an OpenETR Consequential
> State Architecture without being mistaken for control, recognition, or
> effect?

## Summary

OpenETR and C2PA operate at different layers.

C2PA is a content provenance framework. It attaches, embeds, or references a signed manifest that describes provenance assertions about a media asset or document.

OpenETR is a consequential-state and evidence graph for digest-identified
records. It binds end-verifiable events to an object and applies protocol rules
to derive control and lifecycle state independently of any one application.

The compact model is:

```text
C2PA:
content -> manifest/assertions/signature -> provenance verification

OpenETR:
final artifact bytes -> digest -> end-verifiable events -> consequential state
```

Used together:

```text
C2PA explains the content and its provenance.
OpenETR explains the object's consequential state and control.
Recognition explains accepted meaning and effect.
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

OpenETR answers object and consequential-state questions.

Examples include:

- what exact file was recorded
- what digest identifies that file
- which signer created an Anchor Event
- what control events or linked evidence records reference that object
- whether the same file can later be recomputed to the same digest
- what candidate control or evidence graphs exist for that object
- which consequential state follows from each valid graph under the applicable
  OpenETR rules

The Recognition Layer remains separate from both.

It decides:

- whether the C2PA signer is trusted
- whether the C2PA assertions are sufficient
- whether the OpenETR signer is recognized
- whether an OpenETR event has legal, commercial, operational, or institutional effect
- whether a mismatch, missing manifest, revoked certificate, or altered file blocks recognition

## Provenance Versus Control

The deeper distinction is not only that C2PA and OpenETR use different digest patterns.

They solve different problems.

```text
C2PA:
  Is this provenance authentic for this asset?

OpenETR:
  What object is this, and what consequential state follows from its valid events?
```

C2PA binds signed provenance assertions to an asset. Its hard-binding mechanisms let a validator determine whether a manifest belongs with a particular asset and whether the protected content still matches the signed claim.

That is the right model for photographs, videos, generated media, and other content where the relying party needs to know who created the asset, what transformations occurred, and which provenance assertions remain cryptographically bound to the presented content.

OpenETR starts from a different object of concern.

For an electronic transferable record, the key question is not only whether the bytes have provenance. The key question is whether a particular record has a signed control history and a current controller under a selected verifier policy.

The distinction can be stated this way:

```text
C2PA binds assertions to an asset.
OpenETR binds assertions and control transitions to an identified record.
```

Or more sharply:

```text
C2PA makes provenance portable with content.
OpenETR makes consequential state reconstructable without making control copyable.
```

This matters because digital copying is not the security problem by itself. Everything digital can be copied. The necessary property for an electronic transferable record is that copying the bytes, assertions, signatures, or history cannot copy or alter control of the record.

For example, a party may wrap an existing record and its evidence inside a new package:

```text
Record A
  digest = abc123
  control graph = issue -> transfer -> endorse -> transfer

Record B
  digest = def456
  contains Record A and evidence about Record A
  signed by another party
```

That may create a new provenance or evidence statement about `Record B`.

It does not insert the new signer into the control graph for `Record A`.

This is the digital analogue of photocopying a bill of lading. The photocopy may reproduce the words and even the visible endorsement history, but it does not give the copy-holder possession of the operative bill. In OpenETR terms, copies may reproduce evidence, but they do not create a new recognized current controller unless the control graph and recognition policy support that result.

This distinction fits the OpenETR layered model:

```text
Protocol:
  Can I verify these signatures, hashes, events, and references?

Consequential state:
  Who controls this record, which guards apply, and what lifecycle state follows?

Recognition:
  What legal, commercial, institutional, or operational effect follows?
```

C2PA operates primarily around cryptographically verifiable provenance.
OpenETR adds a consequential state machine for records whose lifecycle,
transfer, encumbrance, redemption, or termination must be independently
derived over time.

## Digital Original Boundary

Under OpenETR Consequential State Architecture:

> A Digital Object has stably identifiable content. A Digital Original has
> consequential state.

A C2PA Content Credential can provide strong end-verifiable provenance
evidence, but C2PA validity alone does not establish OpenETR consequential
state. A C2PA-enabled asset becomes a Digital Original in the OpenETR technical
sense when valid OpenETR events establish consequential state for the
identified object.

Recognition remains separate. A relying party may require a trusted C2PA
signer, particular capture assertions, a valid OpenETR control graph, and a
recognized OpenETR signer before giving the Digital Original evidentiary,
institutional, contractual, or legal effect.

```text
C2PA provenance evidence
          +
OpenETR end-verifiable events
          |
          v
OpenETR consequential state
          |
          v
Digital Original
          |
          v
Recognition -> Effect
```

## Final-Artifact Digest Pattern

The recommended OpenETR pattern is to digest the final packaged file after C2PA processing is complete.

The sequence is:

1. Generate or assemble the document, image, video, dataset, or other asset.
2. Apply any document signatures, visible digital seals, Verifiable Credentials, QR elements, or domain-specific trust features.
3. Add, embed, or reference the C2PA manifest.
4. Sign the C2PA manifest.
5. Finalize the file package.
6. Compute the OpenETR digest over the final artifact bytes.
7. Publish or preserve an OpenETR Anchor Event, control event, or linked evidence record for that digest.

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
  -> OpenETR Anchor Event
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
- which consequential state follows from the valid relevant event set

### Recognition Check

The recognition check is separate from C2PA and OpenETR protocol validation.
It should determine which signers, assertions, graphs, objects, or derived
states are accepted for the stated purpose and what effect follows.

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
| Can consequential control state be independently reconstructed? | Not a base C2PA function | Strong fit |
| Does validation compel legal or institutional effect? | No | No; recognition remains separate |

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

OpenETR should treat C2PA as a provenance input, not as a competing
consequential state layer.

C2PA provides embedded or attached provenance for content.

OpenETR provides external final-artifact identity and end-verifiable events
from which consequential state can be derived.

The recommended policy framing is:

```text
C2PA explains the content.
OpenETR explains consequential state and control.
Recognition explains accepted meaning and effect.
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

## Related Documents

- [Provenance And Control Design Note](./PROVENANCE_AND_CONTROL_DESIGN_NOTE.md)
- [Consequential State Architecture Design Note](./CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [Digital Originality, Control, And Standing Design Note](./DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md)
