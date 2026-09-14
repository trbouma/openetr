# Apostille Records Need Consequential State

## Policy Proposition

**Apostille records need consequential state.**

An Apostille allows a public document issued in one jurisdiction to be
presented in another without the traditional chain of diplomatic or consular
legalisation. It matters because a receiving court, university, registry,
immigration authority, commercial party, or other institution may rely on the
authenticated origin of the document.

The Apostille does not certify that every statement in the underlying document
is true. It authenticates a narrower set of facts concerning the document's
origin. The receiving institution separately decides whether the document is
admissible, recognized, sufficient, current, or effective for its purpose.

That makes the Apostille Convention a strong example of the OpenETR principle:

> Each proof proves only what it proves.

OpenETR can help preserve the exact apostilled document package, attributable
evidence concerning it, and the basis for determining its lifecycle state. It
does not issue Apostilles, replace Competent Authorities or e-Registers, or
decide recognition under the Convention.

## What An Apostille Establishes

The
[HCCH Apostille Handbook](https://www.hcch.net/en/publications-and-studies/details4/?pid=5888)
explains the practical operation of the 1961 Apostille Convention for
Competent Authorities and people relying on Apostilles. In simplified terms,
an Apostille authenticates the origin of the underlying public document,
including the relevant signature, the capacity in which the signatory acted,
and the identity of any seal or stamp.

It does not, by itself, establish:

- that the contents of the public document are accurate;
- that the public document remains current;
- that the underlying act was lawful;
- that the person presenting the document is its subject or rightful bearer;
- that the receiving institution must accept it for every purpose; or
- what legal effect the underlying document receives.

The Convention therefore separates authentication of origin from recognition
of content and effect. OpenETR should preserve that separation exactly.

## The Cross-Border Record Problem

An apostilled document package may pass through many hands and systems:

- the authority or official that produces the public document;
- a notary or certifying official;
- the designated Competent Authority;
- an e-Apostille issuance system;
- an e-Register;
- translation and document-handling services;
- the person or organization presenting the package; and
- one or more receiving institutions in another jurisdiction.

The relying party needs more than a visible certificate page. It may need to
determine:

- whether this is the exact document package associated with the Apostille;
- whether the Apostille was issued by the identified Competent Authority;
- whether its particulars correspond with the authority's register;
- whether the package has been altered;
- whether a correction, replacement, warning, or later authority record exists;
- when and from which source a verification was performed; and
- which recognition rules apply in the receiving jurisdiction.

These questions become harder when verification depends entirely on one QR
code, portal, database, vendor, or live registry endpoint.

## The e-APP Foundation

The HCCH
[electronic Apostille Programme](https://www.hcch.net/en/instruments/specialised-sections/apostille/e-app-notifications/)
supports two complementary components:

- **e-Apostilles**, issued electronically and signed using electronic means;
- **e-Registers**, through which particulars of issued Apostilles can be
  checked.

The [HCCH e-APP guidance](https://www.hcch.net/en/publications-and-studies/details4/?pid=5576)
describes technology as a means of extending the Convention into the electronic
environment without changing its nature. This is the correct starting point
for OpenETR.

OpenETR should complement e-APP by making document identity and related
evidence portable. It should not create a parallel authority system or imply
that a relay record outranks the register maintained by the Competent
Authority.

## The OpenETR Contribution

OpenETR can treat the apostilled document package as a Digital Artifact:

```text
public document + Apostille certificate + agreed package structure
  -> Digital Artifact identified by digest
  -> signed DCR evidence concerning the package
  -> Apostille-record lifecycle rules
  -> Consequential State
  -> Convention, authority, and receiving-party recognition
  -> evidentiary, administrative, or legal effect
```

The DCR could preserve evidence that:

- a particular package was recorded;
- an identified authority signed or attested to the package;
- an official e-Register reference was associated with it;
- a verification was performed against an identified source at a stated time;
- a corrected or replacement package was issued;
- an authority published a warning, withdrawal, or invalidity notice; or
- a translation or related certification concerns the same public document.

These records support consequential state concerning the package. They do not
expand what the Apostille itself authenticates.

## Choosing The Digital Artifact

The first policy decision is what exact content the digest identifies.

### Whole-Package Model

The simplest initial model treats the public document and Apostille certificate
as one canonical package:

```text
apostilled package bytes -> SHA-256 digest -> DCR evidence
```

This is easy to present and verify, but any change to the package creates a new
Digital Artifact.

### Linked-Object Model

A more expressive model identifies separate artifacts and links them:

```text
public document artifact
  <- Apostille certificate artifact
  <- e-Register verification artifact
  <- translation or related certification artifact
```

This allows one public document to be associated with multiple Apostilles,
translations, verifications, or recognition decisions. It also requires clear
rules for packaging, linking, and display.

The existing OpenETR Apostille domain specification recommends beginning with
the whole package while allowing later profiles to adopt more granular linked
objects.

## Making Apostille Consequences Portable

The Competent Authority remains the issuer. The e-Register remains an official
verification source where the applicable authority provides one. OpenETR's
contribution is to prevent the evidence presented to another institution from
being intelligible only through the originating application.

```text
package identity
  + authority-linked evidence
  + registry reference or verification evidence
  + identified lifecycle rules
  -> reproducible package state
  -> receiving-party recognition
  -> purpose-specific effect
```

This can help when a package moves through courts, universities, immigration
systems, corporate registries, procurement systems, archives, or private
transactions that do not share one application.

The portability claim must remain precise:

> OpenETR can preserve what was verified, against which source, and when. It
> cannot turn a historical verification into a permanent guarantee of current
> recognition.

If current e-Register confirmation is required, the verifier should perform it.
If the source is unavailable, preserved signed evidence may support continuity
or review, but recognition policy decides whether it is sufficient.

## Power, Availability, And Long-Term Evidence

Official registers and authority systems are necessary parts of the Convention
framework. Exclusive dependence on their current presentation layer can still
create fragility.

A QR code may stop resolving. A portal may be replaced. A verification response
may change format. An authority may reorganize. A receiving institution may
need evidence decades after issuance. A person may possess the correct document
but be unable to demonstrate what an earlier registry check returned.

Separating the evidentiary record from a particular application or service can
improve continuity and accountability. It allows authorized parties to retain
the exact package and attributable evidence of verification without claiming
that the archive itself becomes the Competent Authority.

This also reduces the ability of a technical intermediary to become an
unreviewable gatekeeper between the person presenting a document and the
institution evaluating it. The legal authority remains where the Convention
places it; the evidence becomes less dependent on one vendor or interface.

## Candidate Consequential State

An Apostille-record domain profile might derive states such as:

- package recorded;
- authority attestation present;
- official register reference present;
- register particulars verified at an identified time;
- superseded by a corrected package;
- replaced;
- authority warning present;
- withdrawal or invalidity notice present; or
- verification incomplete or source unavailable.

These states must identify their evidence and temporal basis. Terms such as
`valid Apostille` should be avoided as a universal protocol conclusion because
they compress technical integrity, authority competence, current registry
information, Convention scope, and receiving-party recognition into one label.

## Privacy And Access

Apostilled packages may contain birth, marriage, education, court, immigration,
corporate, notarial, or other sensitive information. Portability does not imply
public disclosure.

Implementations should:

- keep document contents off public relays unless publication is lawful and
  appropriate;
- avoid publishing predictable digests of sensitive documents without a
  privacy analysis;
- use protected evidence packages, encryption, private storage, or
  access-controlled exchange;
- disclose only the metadata required for verification;
- provide accessible verification for people who cannot manage keys or
  specialized software; and
- retain correction, challenge, and remedy processes outside the immutable
  event history.

## Policy And Implementation Priorities

An Apostille-record profile should:

1. define the canonical apostilled package or linked-object model;
2. preserve the distinction between the public document, Apostille certificate,
   Competent Authority, e-Register, and receiving institution;
3. model authority and registry references as recognition evidence rather than
   self-proving metadata;
4. record the source and time of verification checks;
5. define correction, replacement, warning, and withdrawal relationships;
6. report cryptographic integrity separately from Convention recognition and
   document effect;
7. use protected exchange for personal or sensitive documents;
8. test long-term verification when the original portal or vendor is
   unavailable; and
9. design with Competent Authorities and actual receiving institutions rather
   than treating the protocol as a substitute for their rules.

## What OpenETR Does Not Do

OpenETR does not:

- issue an Apostille;
- designate or replace a Competent Authority;
- certify the truth of the underlying public document;
- prove that an authority was competent for a document class by signature
  alone;
- replace an official e-Register;
- guarantee that an earlier verification remains current;
- determine whether the Convention applies;
- compel a receiving institution to accept the document; or
- determine the underlying document's legal effect.

## Bottom Line

The Apostille Convention already demonstrates a disciplined trust boundary:
one authority authenticates origin, while another institution decides what the
document means and whether to rely on it.

OpenETR can make the digital evidence around that boundary more portable:

> Competent Authorities authenticate origin. Receiving institutions determine
> effect. No one application should exclusively own the evidence connecting
> the document package to those decisions.

That is how OpenETR can support the Apostille Convention without competing
with it.

## Related Reading

- [Apostille Documents domain](../apostille-documents.md)
- [Apostille Documents Domain Adapter Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/APOSTILLE_DOCUMENTS_DOMAIN_ADAPTER_SPEC.md)
- [Consequential State](../openetr/consequential-state.md)
- [Graduated Disclosure](graduated-disclosure.md)
- [Academic Records Need Consequential State](academic-records-need-consequential-state.md)
- [Human Rights Need Consequential State](human-rights-need-consequential-state.md)
