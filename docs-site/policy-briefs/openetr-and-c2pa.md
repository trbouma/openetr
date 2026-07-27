# OpenETR And C2PA

OpenETR-style whole-file digesting and C2PA content provenance are complementary approaches to digital trust.

They should not be treated as competing models.

## Executive Summary

C2PA attaches a signed provenance record to content. The C2PA manifest is like a sidecar record added to the file, often embedded inside the PDF, image, video, or other asset. It can describe who created the asset, what actions were performed, what assertions are being made, and whether the protected content still matches the signed provenance record.

OpenETR can provide an additional final-artifact integrity layer by taking a cryptographic digest of the completed file. This is similar to notarizing an already executed or signed document. The file may already contain signatures, credentials, C2PA provenance, or other trust material; OpenETR then records a digest of the final packaged artifact so the exact file can be checked later.

Used together, C2PA helps explain and verify the provenance of the content, while OpenETR helps prove that the completed artifact is byte-for-byte the same file that was recorded.

The short version is:

```text
C2PA is the signed provenance record attached to the content.
OpenETR is the notarization of the final completed file.
```

Or:

```text
C2PA explains what the document is and where it came from.
OpenETR proves this exact final file has not changed.
```

## What C2PA Provides

C2PA is designed for content provenance and authenticity. A C2PA-enabled PDF, image, video, or other asset can carry a manifest that contains signed metadata about the asset.

A C2PA manifest can support questions such as:

- Who or what system created the content?
- What actions were performed on the content?
- What assertions are attached to the content?
- What hashes bind the manifest to the protected content?
- Was the manifest signed?
- Is the signing certificate or trust chain acceptable?
- Has the content been modified since the manifest was created?

C2PA is therefore especially useful when the relying party needs context about the provenance of the content, not just a yes-or-no answer about whether a file has changed.

## What OpenETR Provides

An OpenETR-style digest approach can provide whole-file integrity for the final artifact.

The model is:

```text
final file -> cryptographic digest -> recorded integrity reference
```

If any byte of the final file changes, the digest changes. This makes the model simple to explain, simple to reproduce, and useful as a final artifact integrity check.

The digest does not need to understand the internal structure of the file. It does not need to parse a PDF, interpret a C2PA manifest, or understand a Verifiable Credential.

It treats the final file as the evidence object.

## Why The Layers Are Different

C2PA and OpenETR answer different trust questions.

| Question | C2PA | OpenETR |
| --- | --- | --- |
| What is the provenance of this content? | Strong fit | Not its main purpose |
| Who signed the provenance record? | Strong fit | Not its main purpose |
| What assertions are attached to the content? | Strong fit | Not its main purpose |
| Has protected content changed relative to the manifest? | Strong fit | Indirectly, if the whole-file digest changes |
| Is this exact final file unchanged? | Not always the simplest model | Strong fit |
| Can the check be reproduced without understanding file internals? | Requires C2PA-aware verification | Strong fit |

C2PA is richer. OpenETR-style digesting is simpler.

The policy opportunity is to use both where each is strongest.

## Recommended Combined Workflow

A combined workflow can be described as:

1. Generate the document or digital asset.
2. Add any required document signatures, Verifiable Credentials, QR or visible digital seal elements, or other trust features.
3. Add or embed the C2PA manifest and sign the provenance record.
4. Finalize the file package.
5. Compute the OpenETR digest over the final file.
6. Record, notarize, register, or otherwise preserve the digest as the external integrity reference.

This creates two related forms of evidence:

- internal provenance evidence carried with the file through C2PA
- external final-artifact integrity evidence through the OpenETR digest

## Assessment Implications

For assessment purposes, the two layers should be tested separately and then described as complementary controls.

C2PA evidence should show:

- the file contains or references a C2PA manifest
- the manifest has meaningful assertions
- the C2PA signature validates
- the certificate or trust chain is acceptable for the relying context
- tampering with the protected content is detected by C2PA-aware verification tooling

OpenETR evidence should show:

- the digest algorithm used
- the exact file over which the digest was computed
- where and how the digest was recorded
- how a relying party can recompute the digest
- that any modification to the final file changes the digest

Combined evidence should show:

- the OpenETR digest was computed after the C2PA-enabled file was finalized
- the digest corresponds to the same artifact that is presented to relying parties
- the C2PA verifier and the OpenETR digest check can both be run independently
- exceptions are clearly explained if later packaging, compression, metadata stripping, or file transformations change the byte-level digest

## Risks And Caveats

The combined model is strong, but it must be implemented carefully.

First, the digest must be taken at the right point. If the file is changed after the OpenETR digest is recorded, the digest will no longer match. That is the point of the control, but workflows must be clear about when the file becomes final.

Second, C2PA manifests and file metadata can be affected by export, upload, download, optimization, or sanitization tools. Some services strip metadata, especially from images. A process that preserves C2PA evidence should be explicitly tested.

Third, the trust questions remain distinct. A matching OpenETR digest proves the file is unchanged from the recorded artifact. It does not, by itself, explain whether the C2PA signer is trusted, whether the C2PA assertions are appropriate, or whether the credential claims are true.

Fourth, C2PA verification requires appropriate C2PA tooling and trust material. OpenETR digest verification may be simpler to reproduce, but it should not be used as a substitute for provenance validation when provenance is the policy requirement.

## Developer And Assessor Questions

Useful implementation questions include:

- At what point in the workflow is the C2PA manifest created?
- Is the C2PA manifest embedded in the file or carried as an external sidecar?
- What assertions are included in the manifest?
- What key or certificate signs the C2PA manifest?
- What verifier can validate the C2PA evidence?
- At what point is the OpenETR digest computed?
- Is the digest computed over the final C2PA-enabled file?
- Where is the digest recorded or notarized?
- Can a relying party independently recompute and compare the digest?
- What file transformations are allowed after digesting, if any?

## Policy Position

OpenETR can complement C2PA by adding a final whole-file notarization layer to a document or asset that may already carry signed provenance evidence.

The recommended policy framing is:

```text
C2PA provides embedded or attached provenance for the content.
OpenETR provides external integrity evidence for the finalized artifact.
Together, they support both provenance assurance and final-file integrity.
```

This combined approach is especially useful where a relying party needs to know both what a digital document claims to be and whether the exact final document package has remained unchanged.

