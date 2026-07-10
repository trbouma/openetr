# MLWR Article Requirements Mapping

This document is a working implementation traceability matrix for the UNCITRAL-UNIDROIT Model Law on Warehouse Receipts (MLWR).

It lists each MLWR article, gives a short project-oriented summary, and leaves a column for mapping OpenETR implementation evidence against the article.

This is not legal advice and does not assert that OpenETR satisfies any enacted warehouse receipt law by itself. OpenETR is a signed evidence and control layer. Legal validity, authorization, protected-holder status, priority, enforcement, and local-law recognition remain questions for the relevant MLWR enactment, institutional rules, contracts, registries, courts, and policy profiles.

Primary source: [UNCITRAL-UNIDROIT Model Law on Warehouse Receipts - English PDF](https://www.unidroit.org/wp-content/uploads/2025/01/2024-uncitral-unidroit-mlwr.pdf).

## Mapping Table

| Chapter | Article | Article title | Short summary | Project mapping / evidence |
| --- | --- | --- | --- | --- |
| I. Scope and general provisions | 1 | Scope of application | Applies the law to warehouse receipts and defines a receipt as an electronic record or paper document issued and signed by a warehouse operator acknowledging goods and promising delivery to the holder. | See [Article 1 scope analysis](#article-1-scope-analysis). OpenETR fits as a domain-adaptable evidence and control layer for electronic warehouse receipt workflows, while leaving legal validity, operator authority, goods verification, and local-law recognition outside the base protocol. |
| I. Scope and general provisions | 2 | Definitions | Defines key terms including depositor, electronic record, holder, negotiable warehouse receipt, non-negotiable warehouse receipt, protected holder, storage agreement, and warehouse operator. | See [Article 2 terminology crosswalk](#article-2-terminology-crosswalk). The MLWR domain adapter uses warehouse-receipt terms in routes, page text, forms, and result sections, while mapping those terms to the generic OpenETR object, profile, event, control, participant, and lifecycle model. |
| I. Scope and general provisions | 3 | Non-derogation | Provides that the Model Law provisions may not be varied or derogated from by agreement. | See [Article 3 non-derogation analysis](#article-3-non-derogation-analysis). OpenETR can record agreed workflows, control events, attestations, and policy references, but those records do not let parties contract out of mandatory MLWR requirements. |
| I. Scope and general provisions | 4 | Interpretation | Directs interpretation with regard to the Model Law's international origin and the need for uniform application. | See [Article 4 interpretation analysis](#article-4-interpretation-analysis). OpenETR supports this goal by keeping the core control model generic and portable, with MLWR-specific terminology isolated in the domain adapter and recognition rules left to local enactments or policy profiles. |
| II. Issuance and contents; replacement and change of medium | 5 | Obligation to issue a warehouse receipt | Requires a warehouse operator to issue a receipt for stored goods when requested by the depositor under the storage agreement. | See [Article 5 issuance obligation analysis](#article-5-issuance-obligation-analysis). OpenETR implements the evidence path for issuing a receipt origin event, but the legal obligation to issue and the depositor request/storage-agreement conditions remain recognition-layer and policy-profile questions. |
| II. Issuance and contents; replacement and change of medium | 6 | Electronic warehouse receipt | Requires a reliable method to identify an electronic receipt, keep it subject to control, retain integrity, establish exclusive control, identify the person in control, and transfer control. | TBD |
| II. Issuance and contents; replacement and change of medium | 7 | General reliability standard for electronic warehouse receipts | Sets a context-sensitive reliability standard for methods used under article 6, including operational rules, integrity, access controls, security, audit, accreditation, standards, and proof in fact. | TBD |
| II. Issuance and contents; replacement and change of medium | 8 | Representations by the depositor | Treats a depositor's issuance request as representations about authority to deposit, authority to request the receipt type, and disclosed third-party rights or claims. | TBD |
| II. Issuance and contents; replacement and change of medium | 9 | Incorporation of the storage agreement in the warehouse receipt | Allows storage agreement terms to be incorporated or referenced in the receipt, subject to availability to transferees and inconsistency limits. | TBD |
| II. Issuance and contents; replacement and change of medium | 10 | Information to be included in a warehouse receipt | Lists required receipt information, including receipt label, negotiability terms, parties, goods description and quantity, known third-party claims, storage period, storage place, unique identifier, issuance date/place, and storage-agreement date. | TBD |
| II. Issuance and contents; replacement and change of medium | 11 | Additional information that may be included in a warehouse receipt | Allows optional receipt information such as insurance, storage fees, goods quality, and commingling of fungible goods. | TBD |
| II. Issuance and contents; replacement and change of medium | 12 | Goods in sealed packages and similar situations | Allows warehouse operators to qualify goods descriptions when inspection or verification is impracticable or commercially unreasonable. | TBD |
| II. Issuance and contents; replacement and change of medium | 13 | Loss or destruction of a warehouse receipt | Provides a replacement process for lost or destroyed receipts and treats electronic loss as failure of article 6 conditions or loss of control. | TBD |
| II. Issuance and contents; replacement and change of medium | 14 | Change of medium of a warehouse receipt | Allows change between paper and electronic media, requires the prior medium to become inoperative, and preserves rights and obligations. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 15 | Transfer of a negotiable warehouse receipt | Defines transfer for paper receipts by endorsement/delivery or delivery, and for electronic receipts by transfer of control. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 16 | Rights of a transferee generally | Gives a transferee the benefit of the warehouse operator's obligation and the rights the transferor could convey, subject to protected-holder rules. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 17 | Protected holder of a negotiable warehouse receipt | Defines protected-holder status based on valid transfer, good faith, lack of knowledge of adverse claims or defences, and ordinary-course business or financing. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 18 | Rights of a protected holder of a negotiable warehouse receipt | Specifies the rights acquired by a protected holder, with alternative formulations for rights in the receipt and goods, and shields against many prior claims, defences, and judgments. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 19 | Third-party effectiveness of a security right | Provides ways a security right in a negotiable receipt may become effective against third parties, including registry, control of electronic receipts, or possession of paper receipts. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 20 | Representations by a transferor of a negotiable warehouse receipt | Provides that a transferor represents receipt authenticity and lack of known impairing facts except as notified to the transferee. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 21 | Limited representation by intermediaries | Limits representations by known intermediaries to authorization to transfer, rather than the broader article 20 representations. | TBD |
| III. Transfers and other dealings in negotiable warehouse receipts | 22 | Transferor not responsible for the warehouse operators' performance | Clarifies that transfer alone does not guarantee the warehouse operator's performance. | TBD |
| IV. Rights and obligations of the warehouse operator | 23 | Duty of care | Requires the warehouse operator to store and preserve goods with the care expected of a diligent and competent operator, with limits on liability exclusions. | TBD |
| IV. Rights and obligations of the warehouse operator | 24 | Duty to keep goods separate | Requires goods covered by each receipt to remain identifiable, while allowing permitted commingling of fungible goods of the same type and quality. | TBD |
| IV. Rights and obligations of the warehouse operator | 25 | Lien of the warehouse operator | Defines the warehouse operator's lien for charges and preservation/sale expenses and limits the lien against protected holders. | TBD |
| IV. Rights and obligations of the warehouse operator | 26 | Obligation of the warehouse operator to deliver | Requires delivery to the holder or nominee upon delivery instruction, surrender of the receipt, and payment of qualifying outstanding amounts; requires cancellation after delivery. | TBD |
| IV. Rights and obligations of the warehouse operator | 27 | Partial delivery | Allows partial delivery on similar conditions, with notation of the partial delivery on the receipt and return of the receipt to the holder. | TBD |
| IV. Rights and obligations of the warehouse operator | 28 | Split warehouse receipts | Requires split receipts at the holder's request, covering the same total goods, upon surrender and reasonable costs; requires cancellation of the original. | TBD |
| IV. Rights and obligations of the warehouse operator | 29 | Exoneration from delivery obligation | Relieves the warehouse operator from delivery where goods are lost or destroyed without operator liability, disposed of through lien/storage termination, or delivery is prevented by court order or circumstances beyond control. | TBD |
| IV. Rights and obligations of the warehouse operator | 30 | Termination of storage by the warehouse operator | Allows the warehouse operator to terminate storage through notice, demand payment/removal, reserve sale rights, shorten periods for deteriorating goods, use public notice where needed, and dispose of hazardous goods. | TBD |
| V. Pledge bonds | 31 | Scope of provisions on pledge bonds | Provides that the optional pledge-bond chapter governs effects once a pledge bond is transferred separately from the warehouse receipt. | TBD |
| V. Pledge bonds | 32 | Issuance and form of a pledge bond | Defines pledge bonds as associated but detachable paper documents or separately controllable electronic records that represent a payment right and grant a security right in the goods. | TBD |
| V. Pledge bonds | 33 | Effect of a pledge bond | Makes the warehouse receipt holder's rights to goods subject to the pledge-bond holder's rights and provides payment/surrender and enforcement consequences. | TBD |
| V. Pledge bonds | 34 | Transfers and other dealings | Allows pledge bonds to be transferred with or separately from the receipt, requires amount/due-date information for first separate transfer, and applies negotiable-receipt transfer rules. | TBD |
| V. Pledge bonds | 35 | Rights and obligations of the warehouse operator | Requires both receipt and pledge-bond holders for splits and delivery before due date, and allows delivery against the pledge bond after due date. | TBD |
| VI. Application of this Law | 36 | Entry into force | Provides enactment timing and application to warehouse receipts and optional pledge bonds issued after entry into force. | TBD |
| VI. Application of this Law | 37 | Repeal and amendment of other laws | Provides placeholders for repealing or amending other laws as part of enactment. | TBD |

## Mapping Guidance

Use the final column to point to concrete project artifacts, not abstract claims. Good entries should name:

- the relevant OpenETR command, route, service, or event shape;
- the signed event evidence that is produced or queried;
- the profile or role expected to sign the event;
- the validation rule, policy rule, or recognition assumption being applied;
- any remaining legal, institutional, or local-law dependency.

Examples of useful evidence references include:

- `openetr issue-etr`
- `openetr query-etr`
- `openetr transfer initiate`
- `openetr transfer accept`
- `openetr encumber`
- `openetr discharge`
- `openetr redeem`
- `openetr terminate-etr`
- `/warehouse-receipts`
- `/warehouse-receipts/query`
- `/warehouse-receipts/issue`
- `/warehouse-receipts/transfer/initiate`
- `/warehouse-receipts/transfer/accept`
- `/warehouse-receipts/encumber`
- `/warehouse-receipts/discharge`
- `/warehouse-receipts/redeem`
- `/warehouse-receipts/terminate`
- `openetr/services/control_events.py`
- `openetr/services/query_etr.py`
- `docs/specs/OPENETR_MLWR_PROFILE.md`
- `docs/specs/MLWR_WEBAPP_DOMAIN_ADAPTER_DESIGN_NOTE.md`

## Article 1 Scope Analysis

Article 1 frames the MLWR as applying to warehouse receipts. It also establishes the basic concept of a warehouse receipt as an electronic record or paper document issued and signed by a warehouse operator, acknowledging receipt of goods and promising delivery to the holder.

The current OpenETR implementation should be mapped to Article 1 as an electronic-record evidence and control layer, not as a complete warehouse-receipt law.

| Article 1 requirement / concept | Current project evidence | OpenETR generic mapping | Assessment |
| --- | --- | --- | --- |
| Applies to warehouse receipts | The dedicated MLWR web surface is rooted at `/warehouse-receipts` and presents workflows as warehouse receipt issuance, query, transfer, pledge/lien/restriction, release, presentation for delivery, and completed delivery. | A warehouse receipt is represented as a Controlled Object with an origin event and related control events. | Demonstrated at the domain-adapter level. The UI speaks MLWR warehouse receipt language while the service layer remains generic. |
| Receipt may be an electronic record | `examples/MLWR001.pdf` and uploaded receipt files are accepted as receipt event data; the system hashes the file and uses the digest to derive the OpenETR object identity. | Electronic record bytes become an object digest, `o` tag, `d` tag, and object reference queried through the generic OpenETR model. | Demonstrated for document-backed electronic receipt evidence. A future policy profile should define canonical formats, accessibility, and retention requirements. |
| Issued by a warehouse operator | The MLWR profile describes the warehouse operator as the issuer/obligor role; the MLWR page uses profile selection so the selected operational profile signs issuance and later actions. | Warehouse operator maps to an OpenETR profile signer, commonly the author of the `kind 31415` origin event. | Cryptographic signer evidence is implemented. Legal authority, licensing, custody, and operator qualification remain recognition-layer questions. |
| Signed by the warehouse operator | Issuance through `/warehouse-receipts/issue` or `openetr issue-etr <receipt-file>` publishes a signed Nostr origin event. Query output shows the issuer/profile that signed the origin event. | Nostr event signature on `kind 31415` origin event. | Implemented as cryptographic signature evidence. Signature attribution, authority, and legal intent require policy and applicable law. |
| Acknowledges receipt of goods | The current system treats the uploaded receipt document as the controlled receipt object. The MLWR issue flow can also place `goods_description` in a signed structured origin-event tag and shows it as `Event Data`. | Goods information is not a base protocol primitive; it may be carried in named signed tags, the referenced receipt document, a schema-backed receipt payload, or later attestations. | Partially supported as document and tag evidence. Not yet implemented as a full structured goods schema, inspection evidence, quantity validation, or warehouse custody attestation. |
| Promises delivery to the holder | The MLWR page exposes presentation for delivery and completed delivery actions, and the query result derives the current holder/controller from the control-event chain. | Holder maps to current controller; delivery-related steps map to `redeem` and `terminate` control events. | Workflow evidence exists. The legal promise to deliver, defenses, and warehouse delivery obligations are outside the base protocol and should be handled by Article 26 mapping, receipt terms, and recognition policy. |
| Can support paper/electronic boundary | The matrix includes Article 14 for change of medium, and the MLWR profile is document-format neutral. | A paper receipt can be represented by a digest or replacement event process, but the current model is strongest for electronic event chains. | Not yet fully implemented. Change-of-medium rules, making the prior medium inoperative, and replacement procedures require additional policy and event patterns. |
| Does not replace local warehouse receipt law | `OPENETR_MLWR_PROFILE.md` states that OpenETR does not determine legal validity, goods existence/conformity, operator authority, protected-holder status, perfection, priority, liability, title, or final legal effect. | OpenETR supplies signed evidence to a Recognition Layer. | Explicitly documented. This is a design boundary, not a gap in the base protocol. |

Article 1 therefore supports the current project framing: OpenETR can provide signed, inspectable evidence for electronic warehouse receipt workflows, while an MLWR enactment or recognition profile decides when that evidence has legal effect.

## Article 3 Non-Derogation Analysis

Article 3 means the MLWR rules are mandatory within their scope. Parties may use contracts, platform rules, registry rules, policy profiles, and private workflows, but those arrangements cannot vary or derogate from the Model Law provisions where the Model Law applies.

For OpenETR, Article 3 is mainly a guardrail for how the project describes recognition. OpenETR may publish signed evidence of what parties did and what policies they referenced. It should not claim that a protocol event, profile setting, or private agreement can override mandatory MLWR requirements.

| Article 3 requirement / concept | Current project evidence | OpenETR generic mapping | Assessment |
| --- | --- | --- | --- |
| MLWR provisions are not privately waivable | The MLWR profile states that legal validity, authorization, protected-holder status, perfection, priority, liability, title, and final legal effect belong to the Recognition Layer. | OpenETR events are evidence inputs, not self-executing legal overrides. | Aligned as a documented boundary. The implementation avoids claiming that publication alone determines legal effect. |
| Contracts and policy profiles may still provide context | The MLWR profile lists contract terms, institutional policy, registry/platform rules, and attestation requirements as Recognition Layer inputs. | Policy references, attestations, external references, and participant signatures can be linked to the OpenETR event chain. | Supported as evidence architecture. A policy profile can add conditions, but it should not purport to waive mandatory MLWR rules. |
| OpenETR control events do not displace mandatory law | Transfer, encumbrance, discharge, redemption, and termination events are published as signed control-relevant assertions. | `kind 31416` control events record actions; recognition remains outside raw event publication. | Aligned. A relay-visible event proves that an action was declared, not that MLWR legal consequences necessarily follow. |
| Domain adapter should not expose waiver language | The MLWR Control Desk explains that OpenETR records signed evidence while MLWR-style law, local enactment, registry policy, contract, and courts decide legal effect. | The webapp is a domain adapter over the generic OpenETR service layer. | Current language is consistent with Article 3. Future UI should avoid controls that imply users can opt out of MLWR mandatory rules. |
| Recognition profiles must respect enacted law | Future policy profiles are listed as planned work for minimal demo, registry-backed, and secured-finance recognition modes. | Recognition profiles should evaluate the OpenETR chain under a named legal/institutional policy. | Not fully implemented. Future work should include a rule that policy profiles cannot mark mandatory MLWR requirements as waived merely because parties agreed. |

Article 3 therefore reinforces the project boundary: OpenETR can make agreements, actions, signatures, attestations, and policy references inspectable, but it does not turn private protocol choices into a waiver of MLWR requirements.

## Article 4 Interpretation Analysis

Article 4 directs interpreters to consider the Model Law's international origin and the need to promote uniformity in its application.

For OpenETR, Article 4 argues against embedding one jurisdiction's warehouse-receipt assumptions directly into the base protocol. The project should provide a portable evidence and control vocabulary that can be interpreted consistently across MLWR-style implementations, while allowing local enactments and policy profiles to supply the legally specific recognition rules.

| Article 4 requirement / concept | Current project evidence | OpenETR generic mapping | Assessment |
| --- | --- | --- | --- |
| Respect international origin | The OpenETR MLWR profile is framed as an MLWR-style profile rather than a single-country warehouse receipt implementation. | Base OpenETR concepts use generic terms: Controlled Object, profile, origin event, control event, participant, action, and lifecycle. | Aligned. The model avoids making one domestic warehouse receipt regime the protocol default. |
| Promote uniform application | The MLWR domain adapter translates warehouse receipt workflows into a stable generic event model instead of creating warehouse-only event semantics. | `kind 31415` origin events and `kind 31416` control events provide reusable wire-level shapes across receipt types and legal frameworks. | Aligned. Uniformity is supported by using the same event primitives for issuance, transfer, encumbrance, discharge, redemption, and termination. |
| Keep domain vocabulary intelligible | The webapp speaks warehouse receipt language in routes, headings, forms, and result sections. | Domain terms are presentation-layer terms mapped to the generic service layer and wire model. | Aligned. Users see MLWR concepts without forcing MLWR-specific terminology into the OpenETR core. |
| Preserve local enactment flexibility | The MLWR profile states that local enactment, warehouse licensing rules, registry/platform rules, contract terms, and institutional policy belong to the Recognition Layer. | OpenETR records evidence; recognition profiles determine whether the evidence is legally or institutionally effective. | Aligned. This allows different MLWR enactments to interpret the same evidence under their own rules while still sharing a common evidence model. |
| Avoid overclaiming legal interpretation | The docs repeatedly state that OpenETR does not decide legal validity, protected-holder status, perfection, priority, liability, title, or final legal effect. | Raw event publication is separated from recognition under policy. | Aligned. The protocol remains portable precisely because it does not hard-code legal conclusions. |
| Enable cross-domain reuse | The domain adapter note says the same pattern can support electronic bills of lading, promissory notes, certificates, bearer-style presentation records, and secured finance records. | The generalized OpenETR model can be reused wherever a Controlled Object needs signed control evidence and queryable lifecycle state. | Strongly aligned with Article 4's uniformity impulse. Reuse across domains encourages consistent interpretation of shared control concepts. |

Article 4 therefore supports the project's layered design: warehouse receipt terms belong in the MLWR domain adapter; common control evidence belongs in the generic OpenETR core; legal interpretation belongs in the applicable recognition profile, enactment, or institutional rule set.

## Article 5 Issuance Obligation Analysis

Article 5 concerns the warehouse operator's obligation to issue a warehouse receipt for stored goods when requested by the depositor under the storage agreement.

For OpenETR, Article 5 divides into two parts:

- what the system can currently evidence: issuance of a receipt object by a selected profile;
- what the system should not claim by itself: that the warehouse operator was legally obligated to issue, that the depositor validly requested issuance, or that the storage agreement conditions were satisfied.

| Article 5 requirement / concept | Current project evidence | OpenETR generic mapping | Assessment |
| --- | --- | --- | --- |
| Warehouse operator can issue a receipt | The MLWR Control Desk includes an `Issue Receipt` form at `/warehouse-receipts/issue`; the CLI exposes `openetr issue-etr <receipt-file>`. | Issuance maps to a `kind 31415` origin event for a Controlled Object derived from the uploaded receipt digest. | Implemented as signed issuance evidence. The signer is the selected profile, commonly representing the warehouse operator or issuer. |
| Issuance is signed by the selected operational profile | The webapp requires login and a selected warehouse operator or issuer profile before issuing a warehouse receipt. | The selected profile supplies the Nostr signer for `publish_issue_etr`; query output can later show the origin issuer/profile. | Implemented as cryptographic signer evidence. Legal authority of that profile remains outside the base protocol. |
| Receipt object is tied to stored-goods documentation | The current flow accepts an uploaded warehouse receipt document such as `examples/MLWR001.pdf`, hashes it, and records structured origin-event tags including `name`, `digest_generated_at`, and `size_bytes`. | The document digest becomes the object identity used in `o` and `d` tags and query filters. Document metadata is carried in signed named tags. | Partially aligned. The system identifies the receipt document but does not yet validate goods existence, quantity, custody, or conformity. |
| Depositor request is required | The MLWR profile identifies the depositor role and notes that workflows may issue directly to the depositor or transfer from warehouse operator to depositor. | A depositor can be represented as a profile participant, transferee, or future attestation subject. | Not yet implemented as a required issuance prerequisite. Future work should add depositor request evidence or an attestation/action type tied to issuance. |
| Storage agreement condition matters | The MLWR mapping recognizes storage agreement as an external term or referenced document; the profile says recognition may depend on contract terms and institutional policy. | Storage agreement evidence could be linked by a signed named tag, `ref` metadata, external document digest, schema-backed receipt field, or attestation. | Not yet implemented as a dedicated issuance validation. Article 9 should define storage-agreement incorporation and availability more fully. |
| Issuance policy determines acceptable issuer and initial controller | `OPENETR_MLWR_PROFILE.md` says issuance policy should specify whether the warehouse operator must be the issuer, whether the initial controller is the warehouse operator/depositor/another party, required operator metadata, and whether registry or authority attestation is needed. | Policy profile over the OpenETR origin event and profile metadata. | Documented but not fully automated. Current implementation lets the active profile issue; future recognition profiles should enforce MLWR-specific issuance policy. |
| Legal obligation to issue is not decided by OpenETR | The project boundary states that OpenETR does not determine warehouse operator authority, legal validity, goods existence/conformity, or final legal effect. | OpenETR supplies signed evidence to a Recognition Layer. | Explicitly aligned. OpenETR can prove an issue event happened, not that Article 5 compelled it or that refusal to issue was unlawful. |

Article 5 therefore maps to OpenETR's origin-event issuance machinery, with an important boundary: the current implementation records signed issuance evidence, while the depositor request, storage-agreement entitlement, warehouse-operator obligation, and any sanctions for non-issuance must be handled by the MLWR enactment, storage agreement, registry/platform policy, or future recognition profile.

## Article 2 Terminology Crosswalk

Article 2 is where the MLWR vocabulary starts to become implementation vocabulary.

The current project deliberately keeps three levels separate:

- MLWR domain language used by the warehouse receipts webapp;
- generic OpenETR concepts used by the CLI, service layer, and event model;
- legal conclusions that remain outside the protocol and must be made by an MLWR enactment, institutional rule set, registry, contract, or policy profile.

| MLWR Article 2 term | MLWR-domain usage in this project | Generic OpenETR mapping | Current implementation evidence | Boundary / gap |
| --- | --- | --- | --- | --- |
| Warehouse receipt | The webapp presents a `warehouse receipt` as the object being issued, queried, transferred, pledged, released, presented, and completed. | Controlled Object identified by a digest and OpenETR object id; origin event establishes the first signed record for that object. | `/warehouse-receipts`, `/warehouse-receipts/issue`, `/warehouse-receipts/query`; `openetr issue-etr`; `openetr query-etr`; `publish_issue_etr`; `build_query_etr_result`; `kind 31415`. | OpenETR identifies and tracks a receipt object, but does not yet parse or validate a full structured Article 10 receipt schema. |
| Electronic record | Uploaded PDF or other receipt representation is treated as the controlled electronic record whose digest is used as the stable object identity. | File/document bytes become `sha256` digest; digest maps to `o` and `d` tag values and an object reference. Structured source metadata is carried in signed named tags. | `examples/MLWR001.pdf`; web upload flows; `openetr issue-etr <receipt-file>`; query filters over `#o` and `#d`; origin tags such as `name`, `digest_generated_at`, and `size_bytes`. | The protocol is document-format neutral. Accessibility, storage, rendering, and canonicalization rules must be specified by a policy profile. |
| Warehouse operator | The MLWR page and profile docs use `warehouse operator` as the issuer/obligor role for warehouse receipt workflows. | Operational profile signer; commonly origin-event author, obligor participant, attestor, or terminating party depending on action. | Profile selection on `/warehouse-receipts`; `OPENETR_MLWR_PROFILE.md` role mapping; `signer_npub`; `publish_issue_etr`; profile-backed signing. | OpenETR proves which profile signed. It does not itself prove legal licensing, authority, custody, or warehouse status. |
| Depositor | The MLWR profile treats depositor as the person depositing goods or on whose behalf goods are stored. | Participant/profile that may be initial controller, transferee, or attestation subject depending on the configured workflow. | `OPENETR_MLWR_PROFILE.md` role mapping; profile aliases; transfer commands and routes using participant profiles. | Current UI does not yet expose a dedicated depositor field or depositor representation event. |
| Holder | The MLWR page uses `current holder / controller` for the party shown as controlling the receipt. | Derived current controller from the evaluated OpenETR origin and control-event chain. | `warehouse_receipt_result.html`; `openetr query-etr`; `build_query_etr_result`; transfer initiate/accept events; current-controller summary. | OpenETR can derive current controller evidence. Legal holder status and protected-holder status remain recognition-layer conclusions. |
| Protected holder | The MLWR profile identifies protected-holder status as a legal recognition question. | Not a base protocol state; should be represented by policy evaluation, attestation, or recognition output over the event chain. | `OPENETR_MLWR_PROFILE.md`; query output provides the evidence needed for later evaluation: origin, transfers, profiles, control history, encumbrances. | Not implemented as a final legal determination. Future work should define protected-holder policy checks and supporting attestations. |
| Negotiable warehouse receipt | The domain adapter can present and transfer a receipt as a transferable warehouse receipt workflow. | Controlled Object whose control can be transferred through generic OpenETR control events. | `/warehouse-receipts/transfer/initiate`; `/warehouse-receipts/transfer/accept`; `openetr transfer initiate`; `openetr transfer accept`; `kind 31416 action=initiate/accept`. | The current implementation does not yet encode negotiable vs non-negotiable as a structured receipt attribute. |
| Non-negotiable warehouse receipt | The MLWR table recognizes this term, but the current MLWR page is focused on control and transfer workflows. | Could be represented as a Controlled Object with policy rules that disable or restrict transfer actions. | Generic controls exist, but no dedicated non-negotiable policy profile is implemented yet. | Needs structured receipt metadata or recognition policy to prevent treating a non-negotiable receipt as freely transferable. |
| Storage agreement | The MLWR profile treats storage terms as external terms that may be referenced by a receipt or attestation. | External reference, receipt payload field, signed named tag, or attestation linked to the Controlled Object. | `OPENETR_MLWR_PROFILE.md`; `ref` and `type` metadata on control events; origin-event tags can identify document name, digest generation time, size, receipt reference, goods description, and related domain context. | No dedicated storage-agreement schema or incorporation validation yet. Article 9 mapping should define this more fully. |
| Goods | The receipt document represents goods stored with the warehouse operator; the app currently tracks the receipt while allowing a `goods_description` origin-event tag. | Goods information can be represented as signed named event data, receipt document content, a future schema-backed payload, or attestation linked to the Controlled Object. | `examples/MLWR001.pdf`; `Event Data`; `goods_description` tag; receipt digest/object id in query result. | No current structured goods schema, inspection data, quantity validation, or commingling model. |
| Control | The MLWR domain uses holder/controller language and transfer of receipt control. | Current controller derived from origin and `kind 31416` control events; transfer uses `initiate` and `accept`; encumbrances do not change controller by themselves. | `build_query_etr_result`; `/warehouse-receipts/query`; control history; `openetr transfer initiate`; `openetr transfer accept`; `openetr encumber`; `openetr discharge`. | Legal exclusivity and reliability of control are Article 6 and 7 questions; OpenETR provides evidence for that analysis. |
| Signature / signed by warehouse operator | The MLWR adapter requires the selected profile to sign issue and control actions. | Nostr event signature by the selected OpenETR profile key. | Profile selection; `signer_npub`; `whoami`; `profile show`; Nostr `kind 31415` and `kind 31416` signed events. | Signature evidence is cryptographic. Legal attribution, authority, and intent still require policy and law. |

## Initial Observations

The strongest current OpenETR alignment is likely with articles focused on electronic receipt identity, control, integrity evidence, transfer of control, lifecycle evidence, surrender/presentation-style actions, encumbrance evidence, discharge evidence, and queryable state.

The project does not yet attempt to satisfy article 10 as a structured warehouse receipt schema. Today, `examples/MLWR001.pdf` and uploaded receipt documents are treated as signed/digested event data rather than parsed structured receipt fields.

The project also does not yet decide protected-holder status, priority, enforcement, operator liability, warehouse care duties, or local-law effectiveness. Those should be modelled as recognition rules, attestations, external registry references, or policy profiles layered on top of the OpenETR evidence chain.
