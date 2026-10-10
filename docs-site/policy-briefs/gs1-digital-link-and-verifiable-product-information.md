# GS1 Digital Link And Verifiable Product Information

## Policy Proposition

A product barcode can do more than identify an item at checkout. It can also
connect people and machines to information they can verify independently of
the website that first presents it.

GS1 Digital Link supports two complementary uses of one 2D barcode: a compatible
retail system can extract product identifiers for checkout, while a consumer's
phone can open a product information reference. This does not require two
different printed codes. [GS1 Digital Link](https://www.gs1.org/standards/gs1-digital-link).

OpenETR adds an evidence layer to that reference. An artifact digest in the link
identifies exact digital material, while a signed anchor associates that material
with the product identifiers. Videos, product datasheets, instructions, and other
files can be retrieved from different sources and checked against the same digest.

**The printed domain can be an entry point without becoming the exclusive source
of the information or the authority for its integrity.**

The broader proposition is **one barcode, multiple experiences, and independent
trust decisions**. Participants can share a product reference without having to
share an application, information provider, or rulebook for recognizing evidence.

## One Code With Two Uses

A QR Code carrying a GS1 Digital Link is an ordinary QR symbol containing a
structured web address. For example, a link can carry a GTIN, a lot number, a
serial number, and an application-defined digest parameter. GS1 permits
appropriately named extension parameters alongside its standard identifiers.
[GS1 URI syntax](https://ref.gs1.org/standards/digital-link/uri-syntax/1.7.0/).

At checkout, a compatible scanner and retail application use the product
identifiers. The retailer does not need to download a video or evaluate OpenETR
evidence to identify the product and look up its price.

On a phone, the same QR opens a website. The website can show a video, a
datasheet, or other product information and expose the supporting signed evidence.
The ordinary phone camera need not understand OpenETR to open that page.

Checkout interoperability still requires suitable retailer systems, assigned
identifiers, and compliant printed symbols. Generating a QR image alone does not
certify those conditions. [GS1 retail implementation guidance](https://ref.gs1.org/guidelines/2d-in-retail/).

## One Reference, Different Trust Models

Different uses are not merely different screens after a scan. They can also
reflect different decisions about what evidence to require and whose assertions
to recognize:

| Reader | Experience | Basis for reliance |
| --- | --- | --- |
| Retail checkout | Extract identifiers and look up the item | Retailer product records and trading arrangements |
| Consumer camera | Open the linked website and view information | The consumer's assessment of the site and producer; opening the URL does not itself verify OpenETR evidence |
| OpenETR-aware application | Retrieve and verify the referenced artifact and signed anchors | Digest and signature checks, followed by the application's recognition rules |
| Regulatory reader | Independently acquire a certificate, compare identifiers, and inspect the goods | The regulator's accepted issuers, required evidence, and inspection procedures |

Including a digest makes the regulatory option especially useful. A regulator
can use its own acquisition application, obtain the exact artifact from an
independent archive or permitted source, and compare its calculated digest with
the scanned value. It can then check the product identifiers and signed evidence
without treating the producer's website or its displayed verification result as
authoritative. The compact `d` parameter and descriptive `digest` alias carry the
same commitment; the choice of spelling does not change the trust model.

These checks establish correspondence with the scanned reference, not that the
reference itself deserves trust. A substituted label can carry a different digest
and a valid signature from an unrecognized key. The regulator must still recognize
the relevant issuer, evaluate current applicability, and assess the physical
association. The digest supplies a common integrity check, not a universal trust
decision.

OpenETR therefore supports shared evidence without requiring shared conclusions.
A buyer may accept a supplier assertion that a regulator considers insufficient;
the regulator may require a recognized laboratory's certificate and additional
inspection. Both can evaluate the same independently verifiable material under
their own explicit rules. Ordinary checkout and consumer access can continue
without adopting that regulatory workflow.

For deployment, this means verification capabilities can be added to existing
applications without requiring another printed code or a single mandatory
verification platform. Independent readers still need compatible conventions,
available evidence, and appropriate access rights. GS1 supplies the standardized
product-identification structure; the OpenETR extension supports portable evidence;
each recognizing party retains responsibility for what follows from it.

## Information That Can Outlive Its Website

A web address normally tells a reader where to ask for information. A digest
also tells a verifier which exact bytes it expects to receive.

An OpenETR-aware reader can extract the digest directly from the scanned text,
query its own relay sources for signed anchors, and retrieve the artifact from
available content-addressed storage, a mirror, or a local copy. It need not first
contact the domain printed on the label.

This is an alternative-reader capability, not automatic behaviour of an ordinary
phone camera. The camera's normal action remains opening the URL. Nor does a
digest guarantee that any copy is available: preservation, replication, evidence
discovery, and access arrangements remain operational responsibilities.

The architectural benefit is portability. A supplier can change hosting providers;
a retailer can use its own interface; an assessor can retain an independent copy.
They can verify the same material without making the original website the sole
custodian of its integrity.

## A Wine Label Example

A bottle's label can serve retail identification and open a producer's video.
OpenQR already supports registering an artifact, optionally storing it on Blossom,
publishing a signed OpenETR anchor, and producing both a regular digest link and a
GS1 Digital Link. Supported MP4 files can be presented in a browser player;
PDF datasheets can be previewed as documents.

Today, the anchor's signature binds the artifact digest to the supplied GTIN and
optional lot and serial. Verification checks the file bytes and whether the URL's
product identifiers match a verified anchor's tags. The video need not itself
contain machine-readable product identifiers.

A proposed next step is a structured product record containing those identifiers
and the digests of related videos or datasheets. Hashing that record would commit
its digest to its product fields and resource references. This is a design option,
not a feature already implemented by OpenQR.

## Consumer Cameras And Independent Regulatory Readers

The same printed symbol can serve different readers. A consumer uses the normal
mobile camera to open the HTTPS product page. A regulator could build its own
2D barcode acquisition application that extracts the GTIN, lot number, serial
number, and digest and applies its own verification workflow, without following
the printed domain. These are complementary uses of the same payload.

Consider a Certificate of Analysis whose exact digital bytes contain the product
identifiers. The regulator can obtain the certificate through the supplier, an
archive, or another available source, calculate SHA-256 independently, and compare
it with the digest in the barcode. It then checks that the certificate's GTIN,
lot, and serial match the corresponding barcode fields. These checks establish a
cryptographically verifiable binding between the scanned reference and the exact
certificate containing those identifiers. Merely showing the identifiers beside
a digest on a webpage would not establish the same binding.

This workflow need not start by downloading from the label's website: it can
start with a certificate already held by the regulator. Machine-readable fields
allow automated comparison; PDF text or scanned pages need defined extraction
rules or human review. Matching bytes alone does not confirm what those bytes say.

The regulator can separately retrieve signed anchors and associated evidence using
OpenETR protocols and conventions. Signature checks establish attribution to a key;
the regulator decides whether that key belongs to an accepted laboratory or other
authorized issuer. Where signatures or seals are embedded in the certificate or
referenced by associated evidence, their own validation and recognition requirements
also apply. OpenQR does not yet implement a general Certificate of Analysis parser
or seal-validation workflow. See the
[electronic seals discussion](electronic-seals-and-openetr.md).

The binding is strong, but not an absolute guarantee of analytical truth, current
validity, or attachment to the genuine physical sample. Those remain distinct
questions for the regulator's evidence and rules.

## Extending Verification To Visual Inspection

The verified artifact can also contain a photograph of the product, allowing an
inspector to compare its appearance, packaging, or visible markings with the item
in front of them. Alternatively, a verified manifest can reference a photograph
by its own digest. In that case, the reader verifies both the manifest and the
photograph before displaying it. The issuer should distinguish a representative
product image from a photograph of the particular serialized item.

This adds a physical inspection step to digital verification, not a guarantee of
physical authenticity. A digest establishes which image was committed; the
inspector assesses whether the observed item corresponds to that image. A copied
label, reused photograph, or visually convincing substitute can still require
additional checks.

**Aside: identity documents.** The same separation could support a record
associated with a passport or driver's licence. A digest-identified document could
contain a portrait for manual comparison by an officer, or a biometric template
for comparison with a newly acquired sample using compatible recognition software.
Computer assistance could also help compare a portrait. Cryptographic verification
would establish the integrity and signed attribution of the reference material;
the comparison would remain a separate assessment, not proof of identity by hash.
Issuer recognition, document validity, and the officer's authority remain external
requirements.

This is an illustration of extensibility, not a proposed replacement for existing
identity-document standards or an implemented OpenQR feature. Such an integration
would need protected access, data minimization, retention controls, and appropriate
handling of uncertain matches and presentation attacks. Portraits and biometric
templates should not be placed on publicly accessible relays or blob stores merely
because they can be content-addressed; a digest is not encryption or anonymization.
Independent verification need not mean public disclosure.

## Supporting Trade In Physical Goods

The same approach can support trade by allowing buyers, sellers, carriers, and
inspectors to verify the same product records independently. Once the document
bytes, identifiers, and recognized issuer assertions have been checked, attention
can focus more clearly on whether the goods presented are the goods described.
This reduces information uncertainty without making physical correspondence the
only remaining question: quality, current validity, contractual obligations, and
authority may still require separate checks.

A tamper-resistant sticker carrying the 2D barcode can strengthen that physical
association. Destructible or tamper-evident labels, applied under a controlled
process and checked at handover, can make removal, replacement, or interference
more apparent. Combined with serial numbers, verified photographs, and inspection,
they provide a practical bridge between independently verifiable records and
physical goods. Packaging-level labels should be understood as identifying that
package, not automatically proving the authenticity of everything inside it.

The barcode itself remains copyable. Label design, initial attachment, custody,
and inspection therefore remain part of the assurance process. OpenETR supports
verification of the digital evidence; the physical safeguards support confidence
that the evidence applies to the goods being traded. Neither a scan nor a label
alone establishes ownership or effects a transfer of control.

## Integrity Is Not Authenticity Of The Bottle

The digest establishes byte integrity relative to the expected value. The anchor's
signature attributes an assertion to a signing key. Recognition determines whether
that key is authorized to speak for the product or producer.

A copied label remains copyable. An attacker may also replace an entire label,
including its digest. Product authenticity, issuer recognition, ownership, and
current control are not established merely because a file and signature verify.
The current OpenQR lookup does not evaluate a complete product lifecycle ruleset.

Likewise, an unchanged printed digest identifies a particular version, not
necessarily the latest or currently applicable information. Corrections and
withdrawals require discoverable evidence and explicit evaluation rules.

## Policy Priorities

1. **Preserve existing retail interoperability.** Add independent verification
   without replacing legitimate GS1 identification and checkout arrangements.
2. **Require exportable evidence.** Retain exact artifacts and signed assertions
   so a change of provider does not prevent independent checking.
3. **Distinguish verification from recognition.** Interfaces should state what
   was verified and avoid implying that a signature proves product claims.
4. **Plan for availability and change.** Replication, access control, versioning,
   and later notices are necessary alongside cryptographic integrity.
5. **Test alternative readers.** A useful pilot should recover and verify the
   same material with the printed domain unavailable, using prearranged independent
   storage and evidence sources.

## Bottom Line

GS1 identifies the product. Content addressing identifies the material.
OpenETR supplies attributable evidence linking them. Applications present and
interpret that evidence under the rules relevant to their users.

The result is a familiar checkout and product-information experience with an
additional capability: **the material can be independently retrieved and verified,
rather than being inseparable from the website encoded on its label.**

## Detailed Analysis And Design Notes

- [GS1 Digital Link and content-addressed product information design note](https://github.com/trbouma/openetr/blob/main/docs/specs/GS1_DIGITAL_LINK_CONTENT_ADDRESSED_PRODUCT_INFORMATION_DESIGN_NOTE.md)
- [OpenQR FastAPI implementation and comparison with campaign routes](https://github.com/trbouma/openqr/blob/main/docs/GS1_DIGITAL_LINK_IMPLEMENTATION_NOTE.md)
- [OpenETR QR Resolver Profile 1.0](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_QR_RESOLVER_PROFILE_1_0.md)
- [QR production and scratch-off considerations](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_QR_PRODUCTION_AND_SCRATCH_OFF_DESIGN_NOTE.md)
- [OpenETR Nostr wire format](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [EU Digital Product Passports and OpenETR](eu-digital-product-passports-and-openetr.md)
