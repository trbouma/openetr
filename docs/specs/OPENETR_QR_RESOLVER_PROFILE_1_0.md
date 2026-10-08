# OpenETR QR Resolver Profile 1.0

## Status

Draft specification for review and implementation.

Profile identifier:

```text
openetr:qr-resolver:1.0
```

This document defines a minimal QR code model for discovering OpenETR evidence
concerning a byte-identified Digital Artifact. The model has two independent
parts:

1. a **Resolver Profile**, which determines how a scan is dispatched and
   handled; and
2. an **Artifact Digest**, encoded as either lowercase hexadecimal or unpadded
   Base64URL, which identifies the exact Digital Artifact.

For most implementations, the Resolver Profile produces an HTTPS URL that an
ordinary mobile-device camera can open. An application MAY instead implement a
custom Resolver Profile and QR handler, as Safebox Web does for
application-controlled scanning flows. In every profile, the SHA-256 digest is
the sole record identifier and retains the same meaning regardless of which
permitted encoding is used.

The governing principle is:

> The QR code identifies the Digital Artifact. The resolver interprets the
> evidence concerning it.

## 1. Purpose

The purpose of this specification is to provide a QR code model that:

- can normally be opened by ordinary mobile-device QR scanners through the
  Standard Web Resolver Profile;
- can also be handled by a purpose-built application under a declared custom
  Resolver Profile;
- remains small and visually robust;
- carries one stable artifact identifier;
- does not bind the artifact to a particular event, relay, ruleset, or derived
  state;
- allows the resolver implementation to evolve without changing a printed QR
  code; and
- preserves the distinction between discovery, cryptographic verification,
  ruleset evaluation, recognition, and effect.

## 2. Conformance Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document indicate normative requirements.

An implementation claiming conformance with this profile SHALL identify the
profile as `openetr:qr-resolver:1.0` in implementation documentation or
machine-readable metadata.

## 3. Architectural Position

This profile is a presentation and discovery profile. It is not:

- an OpenETR Anchor Event;
- a Digital Controllable Record;
- proof that an Anchor Event exists;
- proof that a particular publisher is authoritative;
- a statement of Consequential State;
- a ruleset or recognition policy; or
- evidence of legal, institutional, contractual, or operational effect.

The Resolver Profile selects a convenient route to a handler. It does not make
that handler the exclusive authority for the artifact or its evidence. Any
party that obtains the digest can use another profile or conforming
implementation, retrieve evidence from other sources, and independently
verify the results.

```text
QR payload
  -> Resolver Profile: determines dispatch and handling
  -> Artifact Digest: identifies the Digital Artifact

resolver
  -> discovers candidate evidence
  -> verifies the retrieved evidence
  -> evaluates it under an identified ruleset
  -> presents evidence and derived state separately

recognition context
  -> decides what authority, acceptance, or effect follows
```

## 4. Scope

This specification defines:

- the two-part Resolver Profile and Artifact Digest model;
- the Standard Web Resolver Profile;
- requirements for custom Resolver Profiles;
- the canonical SHA-256 digest representation;
- QR symbol generation requirements;
- minimum resolver behavior;
- multiple-Anchor-Event handling;
- redirect and implementation-evolution behavior; and
- presentation and security requirements.

## 5. Out Of Scope

This profile does not define:

- how an artifact is issued or distributed;
- which relays, databases, archives, or other evidence sources a resolver uses;
- which Anchor Event is authoritative;
- which ruleset a resolver must apply after discovery;
- legal recognition or effect;
- trusted time, global ordering, consensus, or finality;
- a globally unique resolver service; or
- a guarantee that all relevant evidence has been retrieved.

## 6. Terms

### 6.1 Digital Artifact

Persistent digital content identified by the SHA-256 digest of its exact
bytes, as defined by OpenETR Core Record Ruleset 1.0.

### 6.2 Artifact Digest

The 32-byte SHA-256 digest of the exact bytes of a Digital Artifact.

### 6.3 Artifact Digest Encoding

A textual representation of the Artifact Digest in one of the two encodings
defined by this profile:

- 64-character lowercase hexadecimal; or
- 43-character unpadded Base64URL.

Both encodings represent the same 32-byte digest value. Encoding does not
create a different Digital Artifact or record identifier.

### 6.4 Resolver Profile

A declared set of rules that determines how a QR Payload carries an Artifact
Digest, how a scanner or application dispatches the payload, and how the
receiving handler extracts the digest.

A Resolver Profile may use an HTTPS URI, a custom URI scheme, an
application-specific descriptor, or an application scanning context. It SHALL
NOT change the meaning or representation of the Artifact Digest.

### 6.5 Resolver

A service or application handler that accepts an Artifact Digest, retrieves or
receives candidate evidence concerning that digest, verifies the evidence, and
presents the resulting observations and derivations.

### 6.6 Resolver Authority

The URI authority component identifying the host that operates the Resolver.
The Resolver Authority is a routing and service-discovery choice. It is not, by
itself, evidence concerning the artifact.

### 6.7 QR Payload

The exact character string encoded in the QR symbol.

## 7. QR Payload Model

### 7.1 Two-Part Model

Every conforming QR use SHALL consist logically of:

```text
Resolver Profile + Artifact Digest
```

The Resolver Profile determines how the digest is encoded, dispatched, and
delivered to a Resolver. The Artifact Digest is the only component that
identifies the record.

The Resolver Profile MAY be selected explicitly by a URI scheme or payload
prefix. It MAY instead be selected by the scanning application or workflow,
provided that the handler unambiguously extracts a permitted Artifact Digest
Encoding and the applicable profile is documented.

### 7.2 Digest Requirements

The Artifact Digest SHALL contain the SHA-256 digest of the artifact's exact
bytes. A conforming payload SHALL encode that digest using one of the following
forms.

#### 7.2.1 Lowercase Hexadecimal

The hexadecimal encoding SHALL:

- contain exactly 64 characters;
- use only lowercase hexadecimal characters `0-9` and `a-f`; and
- decode to exactly 32 bytes.

Example:

```text
2976895f610a8e928249f365827c2fd385d2c7d71da0e4d3bf47845f8dcbdd20
```

#### 7.2.2 Unpadded Base64URL

The Base64URL encoding SHALL:

- use the URL- and filename-safe Base64 alphabet defined by RFC 4648 Section 5;
- contain exactly 43 characters;
- use only ASCII letters, digits, `-`, and `_`;
- omit all `=` padding characters;
- use case-sensitive comparison; and
- decode to exactly 32 bytes.

Example representing the same digest as Section 7.2.1:

```text
KXaJX2EKjpKCSfNlgnwv04XSx9cdoOTTv0eEX43L3SA
```

A decoder SHALL reject a Base64URL value whose canonical unpadded re-encoding
does not reproduce the supplied value. This prevents non-canonical encodings
with invalid unused bits.

#### 7.2.3 Common Requirements

The encoded Artifact Digest SHALL be recoverable from the QR Payload without
network access.

The Artifact Digest SHALL be the sole record identifier in the QR Payload. A
custom Resolver Profile SHALL NOT substitute an event identifier, database
key, opaque token, or service-specific record identifier for the digest.

A conforming generator MAY use either encoding. Base64URL is RECOMMENDED when
minimizing QR payload length is the primary concern. Lowercase hexadecimal is
RECOMMENDED when direct comparison with OpenETR event tags, command output, or
general-purpose SHA-256 tooling is the primary concern.

### 7.3 Standard Web Resolver Profile

Standard Web Resolver Profile identifier:

```text
openetr:qr-resolver:https:1.0
```

The Standard Web Resolver Profile SHALL produce an absolute HTTPS URI in this
form:

```text
https://{resolver-authority}/etr/{artifact-digest}
```

Example:

```text
https://openetr.org/etr/2976895f610a8e928249f365827c2fd385d2c7d71da0e4d3bf47845f8dcbdd20
```

Equivalent compact example:

```text
https://openetr.org/etr/KXaJX2EKjpKCSfNlgnwv04XSx9cdoOTTv0eEX43L3SA
```

The URI SHALL conform to the generic URI syntax in RFC 3986. The
`{artifact-digest}` SHALL appear as the final path segment.

A conforming Standard Web Resolver SHALL accept both digest encodings.

Production payloads using this profile SHALL use HTTPS. Ordinary mobile
scanners can therefore open the payload without requiring an OpenETR-specific
handler.

An implementation MAY use HTTP for local development, but such a payload does
not conform to the Standard Web Resolver Profile for production use.

### 7.4 Custom Resolver Profiles

An application MAY define a custom Resolver Profile for a dedicated QR handler.
This permits implementations such as Safebox Web to receive a scan inside an
existing application workflow rather than sending it through the device's
default web browser.

A custom Resolver Profile SHALL document:

- a stable profile identifier and version;
- the exact payload syntax or scanning context;
- which permitted Artifact Digest Encodings are accepted and how they are
  extracted;
- how the payload is dispatched to the handler;
- validation and error behavior; and
- any security, privacy, installation, or platform dependencies.

A custom profile SHOULD use a URI conforming to RFC 3986 when operating-system
dispatch is required. A custom scheme or descriptor MAY be used when a
purpose-built scanner owns dispatch. Custom profiles SHOULD remain as compact
as practical and SHOULD allow the digest to be recovered without contacting
the original handler.

The use of a custom profile does not create a different artifact identity. The
same digest MAY be resolved through the Standard Web Resolver Profile, a
Safebox Web handler, another application, a CLI, or a local verifier.

### 7.5 Excluded Data

The QR Payload SHALL NOT include:

- a Nostr event identifier;
- an `npub`, public key, profile, or signer identifier;
- an `nobj`, `nevent`, or other NIP-19 identifier;
- relay addresses or relay hints;
- a ruleset identifier;
- a claimed state or verification result;
- artifact metadata such as a filename, reference, or description; or
- any other value that functions as a second record identifier.

A Standard Web Resolver Profile payload SHALL NOT include a query component or
fragment component. A custom Resolver Profile SHOULD avoid them and SHALL
document their syntax if the profile requires either one for dispatch.

For URI-based profiles, user information in the URI authority component SHALL
NOT be used.

These exclusions ensure that the QR code does not select one candidate Anchor
Event, freeze a retrieval topology, or encode a verifier's conclusion.

## 8. QR Symbol Profile

The QR symbol SHALL conform to QR Code Model 2 as specified by ISO/IEC 18004.

A conforming generator SHALL:

- encode the complete payload required by the selected Resolver Profile
  without additional text;
- use error-correction level M;
- provide a quiet zone of at least four modules on every side;
- use dark modules on a light, solid background;
- preserve square modules without stretching, interpolation, or distortion;
- choose the smallest QR version that accommodates the payload at level M; and
- render at a size that keeps each module distinct in the intended medium.

The QR symbol SHALL NOT contain an overlaid logo, icon, text, or other
decoration. Branding MAY appear beside the symbol but SHALL NOT intrude into
the symbol or its quiet zone.

For raster output, a generator SHOULD use an integer number of device pixels
or printer dots per module and SHOULD avoid antialiasing. Vector output is
RECOMMENDED for print workflows where the final dimensions are controlled.

The physical size needed for dependable scanning depends on the payload
length, QR version, print quality, viewing distance, camera, lighting, and
substrate. Implementers SHOULD test the final rendered symbol on representative
mobile devices and in the intended operating conditions.

## 9. Resolver Requirements

### 9.1 Input Validation

A conforming Resolver SHALL:

1. identify the applicable Resolver Profile;
2. extract the encoded Artifact Digest according to that profile;
3. validate the digest syntax before performing evidence retrieval;
4. decode the value to exactly 32 bytes;
5. normalize the value to 64-character lowercase hexadecimal for OpenETR
   event comparison and object-centric queries; and
6. reject malformed or unsupported identifiers without interpreting them as
   event identifiers or search text.

A Resolver implementing the Standard Web Resolver Profile SHALL accept an
HTTPS `GET` request at `/etr/{artifact-digest}`. A custom Resolver Profile
SHALL define its equivalent dispatch behavior.

### 9.2 Evidence Discovery

The Resolver MAY use Nostr relays, local event stores, archives, databases,
third-party services, or other sources to discover evidence. Its retrieval
architecture is not encoded in the QR Payload.

When using the OpenETR Nostr binding, the Resolver SHOULD:

1. query candidate Anchor Events using `kind = 1415` and
   `#o = [normalized-lowercase-hex-digest]`;
2. query later Evidence Events using the applicable kinds and the same `#o`
   value;
3. validate event identifiers and signatures;
4. validate graph references and required tags; and
5. evaluate qualifying evidence under an explicitly identified ruleset.

The Resolver SHALL NOT treat relay delivery or database retrieval as proof
that an event is valid, complete, authoritative, or recognized.

### 9.3 Multiple Anchor Events

More than one valid Anchor Event may carry the same Artifact Digest. A
Resolver SHALL NOT infer from the QR Payload that one candidate Anchor Event is
the unique or authoritative anchor.

If multiple candidate Anchor Events are retrieved, the Resolver SHALL either:

- present them separately; or
- explain the identified recognition policy used to select, rank, or exclude
  them.

The Resolver SHALL NOT silently collapse competing candidates into one
apparently universal record.

### 9.4 Ruleset Evaluation

If the Resolver derives Consequential State, it SHALL identify the ruleset used
for that derivation. A Resolver applying OpenETR Core Record Ruleset 1.0 SHOULD
report the ruleset identifier `openetr:core-record:1.0`.

The Resolver SHALL distinguish:

- validated evidence;
- state derived under an identified ruleset;
- warnings or evidence limitations; and
- recognition or effect determined outside the OpenETR protocol.

### 9.5 Retrieval Results

The Resolver SHALL NOT represent failure to retrieve evidence as proof that no
evidence exists or that the artifact is invalid. A no-result response SHOULD
state the retrieval scope, sources, and time where practical.

The Resolver SHOULD expose or display:

- the full Artifact Digest;
- candidate Anchor Event identifiers and publishers;
- the evidence sources or retrieval scope;
- signature and structural-verification results;
- the applied ruleset identifier, if any;
- derived state, if any;
- material warnings; and
- the time at which retrieval or evaluation occurred.

Machine-readable responses SHOULD follow the OpenETR CLI JSON model where that
model is applicable.

### 9.6 Artifact Verification

Possession of the QR Payload does not prove possession or integrity of the
artifact bytes. If the Resolver retrieves or accepts an artifact, it SHALL
compute SHA-256 over the exact bytes and SHALL compare the result with the
Artifact Digest before presenting the artifact as the identified Digital
Artifact.

A Resolver MAY evaluate evidence using only the supplied digest. In that case,
it SHALL NOT imply that it independently verified the artifact bytes.

## 10. Dispatch And Resolver Evolution

A Resolver using the Standard Web Resolver Profile MAY redirect the canonical
URI to another internal route or presentation surface. Redirects SHALL
preserve the Artifact Digest without changing its value or meaning.

A redirect target MAY contain implementation-specific parameters, but the
printed or otherwise distributed QR Payload SHALL remain in the Standard Web
Resolver Profile form defined by Section 7.3.

A custom Resolver Profile MAY dispatch to an installed application, an
application-controlled web route, or another documented handler. Changes to
that dispatch mechanism SHALL preserve the digest and its meaning.

Resolver operators SHOULD keep canonical resolver URIs durable. Changes to
relay pools, storage systems, verifier implementations, user interfaces, and
rulesets SHOULD be made behind the canonical URI so that existing printed QR
codes continue to resolve.

## 11. Human-Readable Presentation

A printed or displayed QR code SHOULD be accompanied by:

- a concise label indicating that it resolves information concerning the
  artifact;
- the resolver domain, application, or profile; and
- a human-readable digest or digest prefix sufficient to compare records and
  diagnose scanning errors.

The accompanying language SHOULD avoid claims such as "verified," "valid,"
"authentic," or "current" unless the displayed result states what was
verified, under which ruleset, from which evidence, and within which
recognition context.

## 12. Security And Trust Considerations

QR codes and resolver links are untrusted inputs. Implementations and users
SHOULD account for:

- substituted QR labels;
- visually similar or malicious resolver domains, schemes, or applications;
- TLS or DNS compromise;
- stale, partial, censored, or selectively presented evidence;
- malicious artifacts associated with a digest lookup;
- unsafe redirects;
- tracking through resolver requests; and
- overstatement of what a successful lookup proves.

The digest makes independently retrieved artifact bytes comparable. It does
not authenticate the printed label, establish who created the artifact, or
determine which Anchor Publisher should be recognized.

A Resolver SHOULD minimize request logging and SHOULD avoid adding
record-specific tracking identifiers to resolver payloads. Sensitive domains
SHOULD consider the privacy implications of transmitting an Artifact Digest to
a public or application-specific Resolver.

## 13. Conformance Summary

A QR code conforms to `openetr:qr-resolver:1.0` when:

1. the applicable Resolver Profile and version are declared or unambiguously
   determined by the scanning context;
2. the payload carries either the lowercase hexadecimal or unpadded Base64URL
   encoding of the SHA-256 Artifact Digest in accordance with that profile;
3. the digest can be recovered without network access;
4. the digest is the sole record identifier;
5. the payload contains no event, relay, signer, ruleset, or state data;
6. a Standard Web Resolver Profile payload contains no query or fragment;
7. the QR symbol follows the rendering requirements in Section 8; and
8. the handler follows the minimum Resolver behavior in Section 9.

## 14. References

- [OpenETR Core Record Ruleset 1.0](OPENETR_CORE_RECORD_RULESET_1_0.md)
- [OpenETR Nostr Wire Format Specification](OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [OpenETR CLI JSON Model](OPENETR_CLI_JSON_MODEL.md)
- [RFC 3986: Uniform Resource Identifier Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986)
- [RFC 4648: Base-N Encodings](https://www.rfc-editor.org/rfc/rfc4648)
- [ISO/IEC 18004: QR code bar code symbology specification](https://www.iso.org/standard/83389.html)
- [DENSO WAVE: QR Code Standards](https://www.qrcode.com/en/about/standards.html)
- [DENSO WAVE: QR Code Error Correction](https://www.qrcode.com/en/about/error_correction.html)
- [DENSO WAVE: QR Code Quiet Zone](https://www.qrcode.com/en/howto/code.html)
