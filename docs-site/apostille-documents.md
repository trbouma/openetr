# Apostille Documents

Apostille Documents are a future OpenETR domain workspace.

OpenETR can support Apostille Convention workflows as **evidence, portability, and verification infrastructure**. It should not be presented as the authority that issues Apostilles or decides their legal recognition.

Under the HCCH Apostille Convention, Apostilles are issued and verified by designated **Competent Authorities**. The HCCH electronic Apostille Programme, or e-APP, supports electronic issuance and verification, including e-Apostilles and e-Registers. OpenETR should complement those authority-led systems rather than replace them.

## How OpenETR Could Fit

OpenETR could treat an apostilled document package as a **Controlled Object**.

That package might include:

- the public document;
- the Apostille certificate;
- e-Apostille data;
- authority metadata;
- registry lookup URL or identifier;
- revocation, correction, or replacement references;
- supporting notarial or certification material.

The digest of that package becomes the OpenETR object identity. OpenETR can then record a control graph around the object.

## Competent Authorities As Recognized Attesters

In an OpenETR model, a Competent Authority should be treated as the **issuer of a recognized attestation**, not as the attestation itself.

That means:

- the **Controlled Object** is the document package being apostilled;
- the **Competent Authority** is a trusted issuer or controller identity;
- the **Apostille** is an authority attestation over the document package, its digest, or both;
- the **recognition rule** says that attestations from this authority, for this jurisdiction and document class, are accepted as Apostille evidence.

This separates technical verification from legal recognition:

| Question | Layer |
| --- | --- |
| Does the signature verify? | Technical verification. |
| Is the issuer a known authority? | Trust registry or authority metadata. |
| Is the authority competent for this document? | Legal, jurisdictional, or governance rule. |
| Is the Apostille accepted by the relying party? | Recognition outcome. |

This lets OpenETR represent the evidence graph without overclaiming. OpenETR can verify signatures, preserve digest-linked evidence, link to official authority sources, and show the chain of control. The legal effect still depends on the relevant Convention rules, Competent Authority practice, registry evidence, and relying-party policy.

## Candidate Control Records

An Apostille Documents domain profile could define control records such as:

| Control Record | Purpose |
| --- | --- |
| Origin control record | First OpenETR record for the apostilled document bundle. |
| Authority attestation | Signed statement by, or linked to, a Competent Authority or recognized registry source. |
| Registry reference | Link to an official e-Register or verification endpoint. |
| Verification event | Evidence that a verifier checked the Apostille at a particular time. |
| Replacement event | Link from a superseded Apostille package to a corrected or reissued one. |
| Revocation, warning, or invalidity notice | Signed notice from an authority or recognized verifier. |
| Translation or legalization reference | Link to related certified translations, legalization steps, or downstream recognition artifacts. |

## Where OpenETR Helps

OpenETR could make Apostille document workflows more portable by giving every apostilled package:

- a durable digest-based identifier;
- a QR code and durable link;
- a retrievable original record, if stored;
- an inspectable control graph;
- independent signature and event verification;
- links to official Competent Authority or registry verification sources.

This could be useful when apostilled documents circulate across email, portals, registries, courts, universities, immigration systems, commercial counterparties, and long-term archives.

## Recognition Boundary

OpenETR should not claim:

- to issue Apostilles;
- to replace Competent Authorities;
- to decide whether an Apostille is legally valid;
- to force recognition by a Contracting Party;
- to replace official e-Registers or e-Apostille certificates.

Instead, OpenETR can say:

> Here is the controlled document bundle, its digest, its signed evidence graph, and its links to official authority or registry verification.

Legal recognition remains with the relevant authority, law, treaty framework, registry, relying institution, or verifier policy.

## Domain Vocabulary

| OpenETR Concept | Apostille Documents Mapping |
| --- | --- |
| Controlled Object | Apostilled document bundle, e-Apostille package, notarized/certified document package, or related verification artifact. |
| Origin control record | Initial OpenETR record for the package digest. |
| Control graph | Linked evidence about authority, provenance, registry references, verification, replacement, or warnings. |
| Recognition layer | Apostille Convention rules, Competent Authority practice, e-Register checks, local law, court or agency policy, and relying-party verification rules. |

More to come.
