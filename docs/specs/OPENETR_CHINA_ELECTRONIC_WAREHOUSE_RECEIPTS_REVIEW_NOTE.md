# OpenETR And China Electronic Warehouse Receipts Review Note

## Status

Research note, 4 September 2026.

This note is not legal advice and does not assert that OpenETR complies with
Chinese law. It identifies questions for technical mapping, counsel review,
and a possible warehouse-receipt pilot.

## Regulatory Development

China's ten-agency *Provisions on Promoting and Regulating the Application of
Electronic Documents*, Order No. 22, took effect on 1 September 2026.

The official text is available from the State Taxation Administration:

- [Order No. 22: Provisions on Promoting and Regulating the Application of Electronic Documents](https://shanxi.chinatax.gov.cn/web/detail/sx-11400-545-1820386)

The provisions address electronic documents used in goods trade,
transportation, warehousing, finance, and related activities. The transferable-
document provisions require careful study because they address document
uniqueness, exclusive control, controller identification, transfer of control,
identity verification, and reliable-system factors.

## Confirmed Architectural Separation

The regulation separates several questions that should remain separate in an
OpenETR assessment.

### User Identity

Article 12 requires an electronic-document system operator to establish
business rules, verify user identity information according to law, and define
rights and obligations through service agreements.

This is primarily a host-system and recognition responsibility. An OpenETR
signature identifies the signing key; it does not independently establish the
user's civil identity, licensing status, employment authority, or KYC result.

### Transferable-Document Control

Article 14 states that a reliable system serving transferable electronic
documents should be capable of:

- identifying the electronic document and ensuring its uniqueness;
- maintaining exclusive control from creation until the document ceases to
  have effect;
- identifying the controller; and
- ensuring that control moves when the document is transferred.

These requirements are closely related to the OpenETR DCR, transition-rule,
Consequential State, and Digital Original model. Technical similarity does not
by itself establish legal equivalence.

### Reliable System

Articles 14 to 16 address traceability, tamper resistance, issuer
identification, medium conversion, operating rules, data integrity, signature
requirements, access controls, software and hardware security, operational
stability, disaster recovery, audit, certification, standards, and identity
verification services.

OpenETR can provide or reference evidence relevant to some of these factors.
Protocol validity alone does not demonstrate that a deployment satisfies the
complete reliable-system assessment.

## Proposed Mapping Model

The pilot mapping should use two coordinated but separate tracks.

### DCR And Consequential State Track

| Regulatory concern | Candidate OpenETR evidence or behavior |
| --- | --- |
| identify the electronic document | SHA-256 Digital Artifact digest and object identifier |
| establish initial control | kind `1415` Anchor Event evaluated under an identified policy |
| identify the controller | controller derived from the accepted candidate chain |
| exclusive control | policy evaluation of competing anchors, branches, and controller-changing actions |
| transfer control | linked kind `1416` initiate and accept actions under transition rules |
| pledge or encumbrance | `encumber` and `discharge` actions and outstanding-encumbrance state |
| cease to have effect | `terminate` or domain-specific redemption and termination rules |
| medium conversion | proposed `change_medium` design and evidence linking electronic and paper states |

### Recognition And Reliable-System Track

| Regulatory concern | Integration or recognition evidence |
| --- | --- |
| verified user identity | host account, identity service, credential, registry, or KYC evidence |
| recognized warehouse operator | licensing, registry, accreditation, or authority evidence |
| authorized system user | host authorization and Commitment Profile custody controls |
| operating rules | versioned organizational verifier and publishing policies |
| access and key protection | deployment security and Control Desk Key custody evidence |
| continuity and disaster recovery | relay, archive, backup, and recovery controls |
| independent audit or certification | associated evidence or external assessment references |
| legal recognition and effect | identified Chinese legal, regulatory, contractual, or institutional policy |

## The Uniqueness Question

Digital Artifact bytes can be copied. OpenETR does not attempt to prevent
identical copies because each copy resolves to the same digest-addressed
artifact.

OpenETR instead seeks to derive a singular consequential state from accepted
DCR evidence. The principal legal-design question is therefore:

> Can the regulation's uniqueness requirement be satisfied by singular,
> verifiable consequential and control state rather than prevention of
> byte-for-byte copies?

The OpenETR architecture supports that interpretation technically, but the
regulation does not settle the legal interpretation in OpenETR terms. Chinese
counsel, regulators, standards participants, or a supervised pilot should
review the hypothesis before it is presented as a compliance conclusion.

## Proposed Pilot Work

1. Obtain an authoritative translation or bilingual legal review of the
   relevant provisions.
2. Define a China warehouse-receipt Domain Adapter vocabulary and policy
   identifier without changing the generic OpenETR control grammar.
3. Map issuance, transfer, pledge, discharge, redemption, termination, and
   change of medium to exact DCR evidence and derived state.
4. Define how the verifier reports competing anchors, branches, missing links,
   unknown retrieval coverage, and outstanding encumbrances.
5. Create a reliable-system evidence dossier covering identity verification,
   operating rules, key custody, access control, continuity, audit, and
   certification.
6. Test independent reconstruction from multiple relays, an archive, and a
   local evidence package.
7. Seek legal review of uniqueness, exclusive control, controller
   identification, transfer, pledge, and cessation of effect.

## Non-Claims

This note does not claim that:

- Order No. 22 is a general enactment of the UNCITRAL MLETR;
- a valid OpenETR DCR automatically satisfies Chinese law;
- a public relay pool is, by itself, a reliable electronic-document system;
- a signing key is, by itself, a legally identified or authorized user;
- consequential state conclusively satisfies the legal meaning of uniqueness;
  or
- protocol verification determines recognition or legal effect.

## Related Documents

- [OPENETR_MLWR_PROFILE.md](./OPENETR_MLWR_PROFILE.md)
- [MLWR_ARTICLE_REQUIREMENTS_MAPPING.md](./MLWR_ARTICLE_REQUIREMENTS_MAPPING.md)
- [CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md](./CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [MULTI_MODALITY_ARCHITECTURE_NOTE.md](./MULTI_MODALITY_ARCHITECTURE_NOTE.md)
- [SYSTEM_INTEGRATION_CONSIDERATIONS.md](./SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [OPENETR_GENERIC_VERIFIER_POLICY.md](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OPENETR_ROADMAP.md](./OPENETR_ROADMAP.md)

