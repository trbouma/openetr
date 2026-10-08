# OpenETR QR Production And Scratch-Off Design Note

## Status

Design note for review, prototyping, and production testing.

This note is non-normative. It supplements the
[OpenETR QR Resolver Profile 1.0](OPENETR_QR_RESOLVER_PROFILE_1_0.md) with
practical considerations for printing OpenETR resolver QR codes, especially
under removable scratch-off coatings on curved product labels such as wine
bottles.

## 1. Purpose

An OpenETR QR code may be technically valid but still perform poorly after it
is printed, coated, applied to a curved surface, scratched, exposed to moisture,
and scanned by an ordinary mobile device.

This note addresses the resulting production questions:

- how small an OpenETR QR code can reasonably be printed;
- how digest encoding affects QR density;
- how quiet zones and module size affect scanning;
- whether error-correction level M is sufficient for scratch-off use;
- whether decorative modules or logos should be used;
- how bottle curvature, coating, and residue affect the symbol; and
- what a concealed QR code can and cannot establish about a physical product.

The central production principle is:

> The smallest code that scans once is not the smallest code that should be
> manufactured.

## 2. Relationship To The QR Resolver Profile

The QR Resolver Profile separates:

1. the **Resolver Profile**, which determines dispatch and handling; and
2. the **Artifact Digest**, which identifies the exact Digital Artifact.

For ordinary mobile-device scanning, the Standard Web Resolver Profile uses:

```text
https://{resolver-authority}/etr/{artifact-digest}
```

Version 1 permits either:

- a 64-character lowercase hexadecimal SHA-256 digest; or
- a 43-character unpadded Base64URL encoding of the same 32-byte digest.

Both representations identify the same Digital Artifact. The Resolver
normalizes either representation to lowercase hexadecimal before performing
OpenETR object queries.

The compact Base64URL representation is preferable where the physical QR size
is constrained. It reduces the payload without introducing an opaque record
identifier or changing the underlying digest.

## 3. Reference Payload

This note uses the following digest from a live public OpenETR example:

```text
72f268d79dc36412a21d046cc2124b9ca02aab3c712eb23e67fd96d86a38e38f
```

Its equivalent unpadded Base64URL encoding is:

```text
cvJo153DZBKiHQRswhJLnKAqqzxxLrI-Z_2W2Go4448
```

Using `openetr.org` as the Resolver Authority produces these payloads:

```text
https://openetr.org/etr/72f268d79dc36412a21d046cc2124b9ca02aab3c712eb23e67fd96d86a38e38f
```

```text
https://openetr.org/etr/cvJo153DZBKiHQRswhJLnKAqqzxxLrI-Z_2W2Go4448
```

Both URLs resolve to the same
[live record](https://openetr.org/etr/cvJo153DZBKiHQRswhJLnKAqqzxxLrI-Z_2W2Go4448)
and are normalized to the hexadecimal digest before OpenETR evidence is
queried.

The hexadecimal URL contains 88 characters. The Base64URL form contains 67
characters.

## 4. QR Geometry

### 4.1 Module Counts

At common QR error-correction levels, the reference payloads produce the
following symbols with the current Python `qrcode` encoder:

| Digest encoding | Error correction | QR version | Active modules | Modules including four-module quiet zone |
| --- | --- | ---: | ---: | ---: |
| Hexadecimal | L | 5 | 37 x 37 | 45 x 45 |
| Hexadecimal | M | 6 | 41 x 41 | 49 x 49 |
| Hexadecimal | Q | 8 | 49 x 49 | 57 x 57 |
| Hexadecimal | H | 9 | 53 x 53 | 61 x 61 |
| Base64URL | L | 4 | 33 x 33 | 41 x 41 |
| Base64URL | M | 5 | 37 x 37 | 45 x 45 |
| Base64URL | Q | 6 | 41 x 41 | 49 x 49 |
| Base64URL | H | 8 | 49 x 49 | 57 x 57 |

The Base64URL representation saves one QR version at each listed correction
level for this payload. Exact versions remain dependent on the Resolver
Authority, path, digest, encoder, and error-correction setting.

### 4.2 Physical Size

Physical width is calculated as:

```text
(active modules + quiet-zone modules) x module size
```

For the Base64URL Version 5-M symbol:

| Printed module size | Active symbol | Complete footprint including quiet zone |
| ---: | ---: | ---: |
| 0.50 mm | 18.5 mm | 22.5 mm |
| 0.45 mm | 16.7 mm | 20.3 mm |
| 0.40 mm | 14.8 mm | 18.0 mm |
| 0.33 mm | 12.2 mm | 14.9 mm |

The table gives mathematical dimensions, not a guarantee of scan performance.
Smaller modules are less tolerant of dot gain, registration error, surface
damage, camera focus, glare, and residue.

### 4.3 Quiet Zone

A quiet zone of at least four modules shall remain clear on every side of the
symbol. The quiet zone is part of the production footprint even though it does
not contain encoded modules.

No text, border, illustration, varnish transition, cut line, scratch-panel
edge, or label artwork should intrude into it. The revealed surface should
provide a continuous light background throughout the quiet zone.

## 5. Recommended Production Sizes

### 5.1 General Printed Use

For clean, flat, high-quality printed material, a Base64URL Version 5-M symbol
may be prototyped at a complete footprint of approximately 18 to 20 mm. This
range should not be adopted for production without testing the actual printing
process and representative mobile devices.

### 5.2 Scratch-Off Bottle Labels

For a scratch-off QR code on a wine bottle, the recommended starting point is:

```text
QR payload       Standard Web Resolver Profile with Base64URL digest
Error correction M
QR footprint     22 to 25 mm, including quiet zone
Scratch panel    approximately 27 to 30 mm
Modules          solid black squares
Background       matte white
Logo             none inside the symbol
```

A 24 mm complete Version 5-M footprint provides a module size of approximately
0.53 mm. This is a useful starting balance between label area and scanning
margin.

![To-scale rendering of a 24 mm OpenETR QR code and 30 mm scratch panel on a representative 750 ml wine bottle](../images/openetr-wine-bottle-qr-scale.svg)

**Figure 1. Representative bottle and QR scale.** The illustration uses one
SVG unit per millimetre. The bottle is modelled at 300 mm high by 75 mm wide,
the revealed QR footprint is 24 mm, and the indicated scratch panel is 30 mm.
The image may be scaled by a viewer, but the relative dimensions remain exact.
Actual 750 ml bottle and label dimensions vary by manufacturer.

An 18 mm footprint should be treated as an aggressive lower boundary for this
use case. A footprint near 15 mm may scan under controlled conditions but is
not recommended for a consumer-facing scratch-off label.

These recommendations are starting points, not universal minimums. Production
approval should depend on measured scan performance after printing, coating,
application, conditioning, and consumer-style removal.

## 6. Scratch-Off Construction

### 6.1 Layering

The QR code should be printed on the permanent label substrate beneath an
opaque removable coating. It should not be printed on the removable coating.

A representative layer sequence is:

```text
removable opaque scratch coating
release layer compatible with the printing system
black QR symbol and white quiet-zone background
permanent product label
bottle surface
```

The coating and release layer should be selected as a tested system. Poorly
matched materials can remove ink, leave adhesive, polish the substrate to a
reflective surface, or leave residue that closes the light spaces between
modules.

### 6.2 Scratch Panel Size

The scratch panel should extend beyond the complete QR footprint so that its
edge does not become a false border or intrude into the quiet zone. A margin of
approximately 2 to 3 mm on each side is a reasonable prototype starting point.

The panel should include enough space for a concise instruction without
placing that instruction inside the revealed quiet zone.

### 6.3 Surface And Contrast

The revealed surface should be:

- high contrast;
- matte rather than glossy;
- resistant to smearing;
- resistant to ordinary condensation and handling; and
- free of metallic residue over the symbol.

Black modules on a white background provide the greatest conventional scanning
margin. Metallic inks, reverse-polarity symbols, transparent substrates,
gradients, and low-contrast brand colours should be avoided for the concealed
production symbol.

## 7. Bottle And Label Geometry

A cylindrical bottle curves the QR code away from the camera. The effect is
most significant across the horizontal dimension of the symbol.

Production placement should:

- use the flattest available portion of the label panel;
- avoid the bottle shoulder and base transition;
- avoid the label seam and areas likely to wrinkle;
- avoid highly reflective glass or foil immediately around the symbol;
- keep the scratch panel within a visually continuous front-facing area; and
- preserve enough surrounding space for the phone camera to focus.

The code should be tested after the label has been applied to the actual bottle,
not only as a flat press proof.

## 8. Error Correction

The QR Resolver Profile 1.0 specifies level M, which provides approximately 15
percent codeword restoration under the QR error-correction model. The compact
reference payload produces a Version 5-M symbol.

Scratch-off production creates a plausible case for also testing level Q:

- level M uses fewer, larger modules at a given physical footprint;
- level Q provides greater damage recovery but increases the reference payload
  to Version 6; and
- scratches and residue may create concentrated rather than evenly distributed
  damage.

For a controlled pilot, compare at least:

| Candidate | Suggested complete footprint | Purpose |
| --- | ---: | --- |
| Base64URL Version 5-M | 22 to 25 mm | Current profile and larger modules |
| Base64URL Version 6-Q | 24 to 27 mm | Greater damage tolerance |

If Q materially improves field performance, the QR Resolver Profile may need a
named scratch-off production variant. A production implementation should not
silently describe a Q symbol as conforming to a profile that normatively
requires M.

## 9. Module Styling And Branding

The installed QR library can render square, gapped-square, rounded, or circular
modules. It can also apply colours, gradients, and embedded images.

Those capabilities should not be confused with production suitability.

For scratch-off labels at the lower end of the size range:

- use solid square modules;
- keep the finder patterns square and unobstructed;
- do not use circular or gapped modules;
- do not use gradients;
- do not place a logo inside the symbol; and
- place branding beside the scratch panel instead.

Dots and rounded modules may be evaluated for larger visible QR codes, but they
consume scanning margin that is more valuable after a scratch coating has been
removed.

## 10. Print Resolution And Artwork

Production artwork should be generated as vector output where possible. Raster
output should:

- use an integer number of printer dots per QR module;
- avoid antialiasing;
- avoid image resampling after generation;
- preserve exact square geometry; and
- be generated at the final physical dimensions.

DENSO WAVE recommends at least four printer dots per module as a printing
baseline. For this use case, the intended module sizes and a 600 dpi production
process should normally provide substantially more than four dots per module.

The printer should inspect for dot gain that closes light gaps and for dropout
that breaks dark modules. A high nominal printer resolution does not compensate
for poor ink, substrate, coating, or finishing behaviour.

## 11. Verification And Acceptance Testing

### 11.1 Test Articles

Testing should use production-representative:

- labels;
- inks and underprint;
- release layers and scratch coatings;
- bottle materials, colour, and geometry;
- application equipment;
- finishing and varnish processes; and
- environmental conditioning.

A PDF proof or office-printer sample is not sufficient for production approval.

### 11.2 Device Matrix

The test matrix should include:

- current and older iOS devices;
- current and older Android devices;
- default camera applications;
- the Safebox Web or other custom handler, where applicable;
- bright retail lighting;
- dim indoor lighting;
- glare and angled viewing;
- dry and condensation-exposed bottles; and
- cleanly and poorly scratched samples.

### 11.3 Damage Conditions

Samples should be evaluated after:

- complete clean removal;
- incomplete edge removal;
- residual coating across data modules;
- fingernail scratching;
- coin scratching;
- light abrasion during shipping;
- label scuffing;
- moisture exposure; and
- ordinary handling contamination.

### 11.4 Acceptance Criteria

Before production, the project should define measurable acceptance criteria,
including:

- first-attempt scan rate;
- maximum acceptable scan time;
- supported device range;
- supported viewing distance and angle;
- acceptable percentage of residual coating;
- correct extraction of both permitted digest encodings;
- correct resolver response for valid, unknown, and malformed digests; and
- absence of false claims when no OpenETR evidence is retrieved.

A candidate should be enlarged or otherwise revised if it only succeeds after
repeated repositioning, manual camera zoom, unusually bright lighting, or
complete laboratory-quality cleaning.

## 12. Security And Product Claims

### 12.1 What The Scratch Layer Provides

A scratch layer can provide:

- concealment before purchase or use;
- visible evidence that the panel has been opened;
- a deliberate consumer interaction; and
- some resistance to casual pre-purchase scanning.

### 12.2 What It Does Not Provide

A scratch layer does not make the QR code unclonable. A QR payload may be
copied before coating, during production, after legitimate reveal, or from a
photograph.

The Artifact Digest is an identifier, not a password or bearer secret. It
should not be treated as confidential authorization merely because it appears
under a scratch panel.

Scanning a valid OpenETR resolver URL does not, by itself, prove:

- that the label is attached to the intended bottle;
- that the bottle contents are genuine;
- that the QR code has not been copied;
- that the scanner is the first purchaser;
- that the product has not been refilled or substituted; or
- that a retrieved Anchor Event is recognized by the relying party.

### 12.3 Bottle-Specific Records

If the use case includes anti-counterfeiting, activation, or first-purchaser
interaction, each bottle should use a bottle-specific Digital Artifact and
digest. Reusing one digest across a product run makes every printed QR
interchangeable.

A stronger system may combine:

- a unique bottle-specific artifact;
- issuer-signed OpenETR evidence;
- a physical tamper-evident label;
- controlled production and serialization;
- a signed activation or redemption notice; and
- a recognition policy that states what duplicate or later scans mean.

Even this combination does not create universal consensus or make a physical
object cryptographically unclonable. It provides evidence that a verifier can
evaluate under an identified rulebook.

## 13. Initial Pilot Recommendation

The recommended initial wine-bottle pilot is:

```text
Resolver profile     openetr:qr-resolver:https:1.0
Digest encoding      unpadded Base64URL
Error correction     M
QR footprint         24 mm including quiet zone
Scratch panel        27 to 30 mm
Module style         solid black squares
Background           matte white
Embedded logo        none
Artwork              vector preferred
Production output    600 dpi or better where rasterization occurs
Record strategy      one bottle-specific digest where individualization matters
```

The pilot should also include a 25 to 27 mm level-Q comparison sample to
determine whether greater damage recovery offsets its denser module matrix.

No production minimum should be adopted until the complete label system passes
the acceptance tests described in Section 11.

## 14. Open Design Questions

1. Should QR Resolver Profile 1.0 permit both M and Q, or should Q be defined in
   a separate scratch-off production profile?
2. Does the product use case require one digest per product type, batch, case,
   or individual bottle?
3. Is the scratch panel intended for concealment, tamper evidence, consumer
   engagement, activation, anti-counterfeiting, or a combination?
4. Should a custom application Resolver Profile provide an additional compact
   payload, and what happens when the application is not installed?
5. What signed evidence, if any, should follow first reveal, activation, or
   redemption?
6. What recognition policy governs duplicate, delayed, or offline scans?

## 15. References

- [OpenETR QR Resolver Profile 1.0](OPENETR_QR_RESOLVER_PROFILE_1_0.md)
- [OpenETR Core Record Ruleset 1.0](OPENETR_CORE_RECORD_RULESET_1_0.md)
- [DENSO WAVE: QR Code Versions And Module Counts](https://www.qrcode.com/en/about/version.html)
- [DENSO WAVE: QR Code Error Correction](https://www.qrcode.com/en/about/error_correction.html)
- [DENSO WAVE: QR Code Quiet Zone](https://www.qrcode.com/en/howto/code.html)
- [DENSO WAVE: QR Code Module Size](https://www.qrcode.com/en/howto/cell.html)
