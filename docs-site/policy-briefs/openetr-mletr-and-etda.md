# OpenETR, MLETR, And ETDA

OpenETR is designed to support electronic transferable records without becoming tied to one statute, platform, or document family.

That matters because two influential legal models are now shaping digital trade:

- the UNCITRAL Model Law on Electronic Transferable Records (`MLETR`)
- the United Kingdom Electronic Trade Documents Act 2023 (`ETDA`)

Both seek to make electronic records perform functions that paper trade documents have historically performed. But they do so with different scopes, language, and policy instincts.

OpenETR should be able to support both.

## The Policy Problem

Paper trade documents work because possession of the paper object can carry legal and commercial consequences.

In trade, finance, transport, and warehousing, paper documents may allow a holder to claim performance, transfer rights, present goods-related claims, or support financing.

Electronic information does not naturally behave this way.

It can be copied, forwarded, exported, mirrored, or displayed in many systems at once. A PDF or database record can contain the right words, but that does not by itself answer the deeper legal questions:

- Which electronic record is the operative one?
- Has it retained integrity?
- Who controls it?
- Can only one person exercise control at a time?
- Has control been transferred?
- Was the prior controller deprived of control?
- Can the current controller demonstrate control?
- Which law, contract, registry, or platform rule recognizes the result?

MLETR and ETDA are attempts to answer these questions in law.

OpenETR answers a narrower technical question:

```text
Can we produce portable, signed, object-specific evidence
that a legal or institutional framework can evaluate?
```

## MLETR And ETDA In Brief

MLETR is a model law designed for international harmonization.

It uses functional-equivalence principles. It asks whether an electronic transferable record can perform the legal functions of a paper transferable document or instrument. Its important ideas include reliable methods, integrity, exclusive control, identification of the person in control, transfer of control, change of medium, and non-discrimination against foreign electronic transferable records.

ETDA is UK legislation.

It enables certain electronic trade documents to be possessed, indorsed, and transferred under UK law. It uses gateway criteria for electronic trade documents, a reliable-system framing, protection against unauthorized alteration, demonstrable control, and transfer rules intended to deprive the previous controller of control.

The two approaches are broadly compatible, but they are not identical.

## The Main Difference

MLETR is optimized for harmonization.

ETDA is optimized for UK legal implementation.

That distinction matters for OpenETR because OpenETR should be usable across jurisdictions, document families, and recognition regimes.

If OpenETR adopts ETDA's statutory vocabulary as its core model, it risks becoming too tied to one national approach.

If OpenETR aligns only with abstract MLETR concepts and ignores ETDA, it risks failing to support an important legal environment for trade conducted under English law.

The better approach is layered:

```text
OpenETR core:
  controlled objects, signed events, control graphs, linked evidence

MLETR alignment:
  default international functional-equivalence orientation

ETDA profile:
  UK recognition profile over the same OpenETR evidence
```

## What OpenETR Provides

OpenETR can provide technical evidence for the functions that MLETR and ETDA care about.

| Legal Concern | OpenETR Contribution |
| --- | --- |
| Identification | digest-identified Controlled Object and signed origin event |
| Integrity | recomputable hash, signed events, prior-event references, linked evidence |
| Control | object-specific control graph and candidate current-controller derivation |
| Exclusive control | verifier policy that recognizes only one current controller path |
| Demonstration of control | presentable graph of signed events and profiles |
| Transfer | signed transfer event linked to prior control state |
| Deprivation of prior controller | graph state that no longer recognizes the transferor as current controller |
| Endorsement | signed attestation, transfer metadata, or domain-specific event |
| Change of medium | paper-to-electronic and electronic-to-paper lifecycle events |
| Reliability | method-level and system-level evidence for verifier policy |

This makes OpenETR useful without pretending that cryptography alone creates legal effect.

## Control Is Not Recognition

OpenETR can show that a record has a signed control graph.

That does not automatically mean a court, bank, port, carrier, registry, insurer, or customs authority must recognize the result.

Recognition depends on the applicable framework:

- MLETR enactment
- ETDA
- local trade law
- contract
- registry rulebook
- platform terms
- institutional policy
- evidence of identity and authority

The same OpenETR graph may be accepted under one policy, warned under another, and rejected under a third.

That is a feature, not a weakness.

It means OpenETR can preserve common evidence while allowing different legal and operational systems to apply their own rules transparently.

## Recommended Policy Position

OpenETR should treat MLETR as the stronger default alignment target for international trade.

MLETR is technology-neutral, model-law based, and designed for cross-border harmonization. Its vocabulary of electronic transferable records, reliable methods, exclusive control, integrity, and international interpretation fits OpenETR's role as portable control infrastructure.

OpenETR should also support ETDA directly.

ETDA is commercially important because of the role of English law in trade and finance. But it should be implemented as a recognition profile and domain-adapter policy, not as the default language of the OpenETR core.

The policy stance is:

```text
Build once around controllable records and signed control graphs.
Recognize many times through MLETR, ETDA, contracts, registries,
and institutional policies.
```

## Practical Implications

For implementers, this means:

- do not build separate control infrastructure for each statute
- keep the OpenETR core jurisdiction-neutral
- define MLETR and ETDA verifier profiles
- separate cryptographic validity from legal recognition
- record transfer, endorsement, encumbrance, redemption, and change-of-medium events explicitly
- expose reliability evidence as policy input
- preserve the graph even when recognition differs across jurisdictions

For policymakers, this means:

- legal harmonization still matters
- technology neutrality should be preserved
- closed-platform possession should not become the only route to digital trade
- reliable methods and reliable systems should be evaluated through inspectable evidence
- cross-border recognition improves when technical evidence is portable

## Bottom Line

OpenETR is not a substitute for MLETR or ETDA.

It is a technical fabric that can help records satisfy the evidence demands of both.

MLETR and ETDA decide when an electronic record has legal effect. OpenETR helps produce the signed, portable, inspectable control graph that makes that decision easier to evaluate.

## Related Design Note

- [OpenETR MLETR And ETDA Mapping Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_MLETR_ETDA_MAPPING_DESIGN_NOTE.md)

## Related OpenETR Materials

- [OpenETR Generic Domain Adapter Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR Generic Transfer Model](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_TRANSFER_MODEL.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Control Event Minimum Shapes](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROL_EVENT_MINIMUM_SHAPES.md)
- [MLWR Change Of Medium Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_CHANGE_OF_MEDIUM_PROFILE.md)
