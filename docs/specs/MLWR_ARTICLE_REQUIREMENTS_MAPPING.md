# MLWR Article Requirements Mapping

This document is a working implementation traceability matrix for the UNCITRAL-UNIDROIT Model Law on Warehouse Receipts (MLWR).

It lists each MLWR article, gives a short project-oriented summary, and leaves a column for mapping OpenETR implementation evidence against the article.

This is not legal advice and does not assert that OpenETR satisfies any enacted warehouse receipt law by itself. OpenETR is a signed evidence and control layer. Legal validity, authorization, protected-holder status, priority, enforcement, and local-law recognition remain questions for the relevant MLWR enactment, institutional rules, contracts, registries, courts, and policy profiles.

Primary source: [UNCITRAL-UNIDROIT Model Law on Warehouse Receipts - English PDF](https://www.unidroit.org/wp-content/uploads/2025/01/2024-uncitral-unidroit-mlwr.pdf).

## Mapping Table

| Chapter | Article | Article title | Short summary | Project mapping / evidence |
| --- | --- | --- | --- | --- |
| I. Scope and general provisions | 1 | Scope of application | Applies the law to warehouse receipts and defines a receipt as an electronic record or paper document issued and signed by a warehouse operator acknowledging goods and promising delivery to the holder. | TBD |
| I. Scope and general provisions | 2 | Definitions | Defines key terms including depositor, electronic record, holder, negotiable warehouse receipt, non-negotiable warehouse receipt, protected holder, storage agreement, and warehouse operator. | See [Article 2 terminology crosswalk](#article-2-terminology-crosswalk). The MLWR domain adapter uses warehouse-receipt terms in routes, page text, forms, and result sections, while mapping those terms to the generic OpenETR object, profile, event, control, participant, and lifecycle model. |
| I. Scope and general provisions | 3 | Non-derogation | Provides that the Model Law provisions may not be varied or derogated from by agreement. | TBD |
| I. Scope and general provisions | 4 | Interpretation | Directs interpretation with regard to the Model Law's international origin and the need for uniform application. | TBD |
| II. Issuance and contents; replacement and change of medium | 5 | Obligation to issue a warehouse receipt | Requires a warehouse operator to issue a receipt for stored goods when requested by the depositor under the storage agreement. | TBD |
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

## Article 2 Terminology Crosswalk

Article 2 is where the MLWR vocabulary starts to become implementation vocabulary.

The current project deliberately keeps three levels separate:

- MLWR domain language used by the warehouse receipts webapp;
- generic OpenETR concepts used by the CLI, service layer, and event model;
- legal conclusions that remain outside the protocol and must be made by an MLWR enactment, institutional rule set, registry, contract, or policy profile.

| MLWR Article 2 term | MLWR-domain usage in this project | Generic OpenETR mapping | Current implementation evidence | Boundary / gap |
| --- | --- | --- | --- | --- |
| Warehouse receipt | The webapp presents a `warehouse receipt` as the object being issued, queried, transferred, pledged, released, presented, and completed. | Controlled Object identified by a digest and OpenETR object id; origin event establishes the first signed record for that object. | `/warehouse-receipts`, `/warehouse-receipts/issue`, `/warehouse-receipts/query`; `openetr issue-etr`; `openetr query-etr`; `publish_issue_etr`; `build_query_etr_result`; `kind 31415`. | OpenETR identifies and tracks a receipt object, but does not yet parse or validate a full structured Article 10 receipt schema. |
| Electronic record | Uploaded PDF or other receipt representation is treated as event data whose digest is used as the stable object identity. | File/document bytes become `sha256` digest; digest maps to `o` and `d` tag values and an object reference. | `examples/MLWR001.pdf`; web upload flows; `openetr issue-etr <receipt-file>`; query filters over `#o` and `#d`. | The protocol is document-format neutral. Accessibility, storage, rendering, and canonicalization rules must be specified by a policy profile. |
| Warehouse operator | The MLWR page and profile docs use `warehouse operator` as the issuer/obligor role for warehouse receipt workflows. | Operational profile signer; commonly origin-event author, obligor participant, attestor, or terminating party depending on action. | Profile selection on `/warehouse-receipts`; `OPENETR_MLWR_PROFILE.md` role mapping; `signer_npub`; `publish_issue_etr`; profile-backed signing. | OpenETR proves which profile signed. It does not itself prove legal licensing, authority, custody, or warehouse status. |
| Depositor | The MLWR profile treats depositor as the person depositing goods or on whose behalf goods are stored. | Participant/profile that may be initial controller, transferee, or attestation subject depending on the configured workflow. | `OPENETR_MLWR_PROFILE.md` role mapping; profile aliases; transfer commands and routes using participant profiles. | Current UI does not yet expose a dedicated depositor field or depositor representation event. |
| Holder | The MLWR page uses `current holder / controller` for the party shown as controlling the receipt. | Derived current controller from the evaluated OpenETR origin and control-event chain. | `warehouse_receipt_result.html`; `openetr query-etr`; `build_query_etr_result`; transfer initiate/accept events; current-controller summary. | OpenETR can derive current controller evidence. Legal holder status and protected-holder status remain recognition-layer conclusions. |
| Protected holder | The MLWR profile identifies protected-holder status as a legal recognition question. | Not a base protocol state; should be represented by policy evaluation, attestation, or recognition output over the event chain. | `OPENETR_MLWR_PROFILE.md`; query output provides the evidence needed for later evaluation: origin, transfers, profiles, control history, encumbrances. | Not implemented as a final legal determination. Future work should define protected-holder policy checks and supporting attestations. |
| Negotiable warehouse receipt | The domain adapter can present and transfer a receipt as a transferable warehouse receipt workflow. | Controlled Object whose control can be transferred through generic OpenETR control events. | `/warehouse-receipts/transfer/initiate`; `/warehouse-receipts/transfer/accept`; `openetr transfer initiate`; `openetr transfer accept`; `kind 31416 action=initiate/accept`. | The current implementation does not yet encode negotiable vs non-negotiable as a structured receipt attribute. |
| Non-negotiable warehouse receipt | The MLWR table recognizes this term, but the current MLWR page is focused on control and transfer workflows. | Could be represented as a Controlled Object with policy rules that disable or restrict transfer actions. | Generic controls exist, but no dedicated non-negotiable policy profile is implemented yet. | Needs structured receipt metadata or recognition policy to prevent treating a non-negotiable receipt as freely transferable. |
| Storage agreement | The MLWR profile treats storage terms as external terms that may be referenced by a receipt or attestation. | External reference, receipt payload field, event data, or attestation linked to the Controlled Object. | `OPENETR_MLWR_PROFILE.md`; `ref` and `type` metadata on control events; origin event content can identify document name, digest, size, and related references. | No dedicated storage-agreement schema or incorporation validation yet. Article 9 mapping should define this more fully. |
| Goods | The receipt document represents goods stored with the warehouse operator; the app currently tracks the receipt rather than modelling goods directly. | Goods information is part of the receipt event data or future structured payload; OpenETR object identity is the receipt/document digest. | `examples/MLWR001.pdf`; `Origin Event Data`; receipt digest/object id in query result. | No current structured goods schema, inspection data, quantity validation, or commingling model. |
| Control | The MLWR domain uses holder/controller language and transfer of receipt control. | Current controller derived from origin and `kind 31416` control events; transfer uses `initiate` and `accept`; encumbrances do not change controller by themselves. | `build_query_etr_result`; `/warehouse-receipts/query`; control history; `openetr transfer initiate`; `openetr transfer accept`; `openetr encumber`; `openetr discharge`. | Legal exclusivity and reliability of control are Article 6 and 7 questions; OpenETR provides evidence for that analysis. |
| Signature / signed by warehouse operator | The MLWR adapter requires the selected profile to sign issue and control actions. | Nostr event signature by the selected OpenETR profile key. | Profile selection; `signer_npub`; `whoami`; `profile show`; Nostr `kind 31415` and `kind 31416` signed events. | Signature evidence is cryptographic. Legal attribution, authority, and intent still require policy and law. |

## Initial Observations

The strongest current OpenETR alignment is likely with articles focused on electronic receipt identity, control, integrity evidence, transfer of control, lifecycle evidence, surrender/presentation-style actions, encumbrance evidence, discharge evidence, and queryable state.

The project does not yet attempt to satisfy article 10 as a structured warehouse receipt schema. Today, `examples/MLWR001.pdf` and uploaded receipt documents are treated as signed/digested event data rather than parsed structured receipt fields.

The project also does not yet decide protected-holder status, priority, enforcement, operator liability, warehouse care duties, or local-law effectiveness. Those should be modelled as recognition rules, attestations, external registry references, or policy profiles layered on top of the OpenETR evidence chain.
