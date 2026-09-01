# Legal Confidence, Paperless Trade, And OpenETR

In his 21 August 2026 address, [*Getting the Paper out of International Trade and Finance: Why not now?*](https://github.com/trbouma/openetr/blob/main/docs/source/BFSLA.Speech.pdf), to the Banking and Financial Services Law Association Conference, Sir Geoffrey Vos, Master of the Rolls, asks what is still preventing international trade and finance from leaving paper behind.

His answer is not that the technology is missing.

The deeper problem is confidence: confidence that electronic trade documents will be legally effective, that different systems will interoperate, that banks, insurers, carriers, customs authorities, and traders will recognize the result, and that cross-border private law will respond predictably when something goes wrong.

OpenETR cannot create that confidence by itself. It can, however, provide a practical control layer around which legal statements, reliable-system assessments, domain standards, and recognition policies can converge.

## The Speech's Thesis

The speech identifies encouraging progress but no decisive transition. It reports that electronic bill of lading adoption increased from approximately 1 percent in 2021 to approximately 11 percent in 2026, against an annual market of roughly 45 million bills of lading.

It then identifies four connected barriers:

1. uneven legal recognition of electronic transferable records;
2. the absence of a mainstream international digital currency;
3. commercial and operational reluctance to abandon paper;
4. the need for a credible catalyst that can increase legal and market confidence.

The speech's practical conclusion is important. Paperless trade should not wait for central bank digital currencies, stablecoins, or cryptoassets to become the dominant means of payment. Electronic trade documents can operate alongside ordinary digitally transferred fiat currency.

The same modular reasoning applies to trade-document infrastructure. Digitizing documents, data, control, and payment does not require every function to run on one platform or one technical architecture.

## The Legal Foundation

The speech highlights the UNCITRAL Model Law on Electronic Transferable Records, the United Kingdom's Electronic Trade Documents Act 2023, UCC Article 12 in the United States, and the United Nations Convention on Negotiable Cargo Documents.

Its discussion of the UK Act is especially relevant to OpenETR. A reliable electronic system must be able to:

- identify the document and distinguish it from copies;
- protect it against unauthorized alteration;
- prevent more than one person from exercising control at the same time;
- allow the person in control to demonstrate control;
- ensure that transfer deprives the previous controller of control.

These are legal functions, not prescriptions for a particular database, blockchain, or software vendor.

OpenETR is designed around the same functional questions:

| Reliable-system concern | OpenETR evidence |
| --- | --- |
| Identify the operative record | SHA-256 Digital Artifact identifier |
| Detect alteration | Recalculation of the digest over the exact artifact or canonical data package |
| Evidence control | Signed origin and control events linked in an object-specific graph |
| Demonstrate current control | Reconstructable candidate controller state under a stated verifier policy |
| Evidence transfer | Signed transition linked to the prior control event |
| Deprive the previous controller | Policy-derived state that no longer recognizes the transferor as current controller |

This mapping is useful, but it must not be overstated. OpenETR provides inspectable evidence. Whether an implementation is a reliable system under applicable law depends on the complete operational arrangement, including identity, authorization, key custody, security, availability, governance, error handling, and recognition policy.

## A Third Architectural Position

The speech describes the electronic bill of lading market as divided between centralized-ledger platforms and DLT or blockchain platforms. That division can create interoperability problems and make adoption feel like a choice of closed ecosystems.

OpenETR takes a narrower architectural position.

It is not a universal centralized ledger, and it is not a blockchain smart-contract platform. It uses cryptographically signed events that can be stored and retrieved through public or private Nostr relays, local event stores, archives, or application databases.

```text
existing trade platform
  -> digest of the operative record
  -> signed OpenETR control events
  -> portable Digital Controllable Record
  -> state transition rules produce consequential state
  -> independent verifier applies its rule book
```

This allows a centralized platform, a DLT platform, a carrier system, a bank, or a customs service to retain its own architecture while exchanging independently verifiable control evidence.

The policy opportunity is interoperability without requiring infrastructure uniformity.

## Documents, Data, And Control

The speech looks beyond electronic documents toward streamed data flows, near-real-time cargo information, automated customs filings, and supply-chain updates.

OpenETR should not attempt to become the data standard or transport mechanism for those streams. Standards such as DCSA, UN/CEFACT, customs data models, and sector APIs remain responsible for the meaning and exchange of trade data.

OpenETR can provide the control and evidence layer around selected records or canonical data packages:

```text
domain data or document
  -> canonical artifact or package
  -> digest
  -> signed control and evidence graph
```

A continuously changing data stream is not one permanently fixed OpenETR object. A system can instead create digest-identified snapshots, packages, or linked evidence records at legally or operationally meaningful points.

This preserves the distinction between:

- moving operational data;
- identifying the exact record being relied upon;
- recording who made a consequential control commitment;
- deciding the legal effect of that commitment.

## Digital Currency Is Not A Dependency

The speech argues that paperless trade can proceed using established fiat currencies. This aligns directly with OpenETR's separation of concerns.

OpenETR does not require:

- a central bank digital currency;
- a stablecoin;
- Bitcoin or another cryptoasset;
- an on-chain payment;
- a tokenized trade document;
- atomic settlement between payment and control.

A payment system may be linked as evidence or used as a workflow condition, but payment is not part of the core control protocol.

This lets parties improve the document and control layer without waiting for a separate transformation of money.

## Control, Transfer, And Tokenisation

The speech describes the International Jurisdiction Taskforce's work on four areas: control; transfer, extinguishment, and good-faith acquisition; tokenisation; and custody and insolvency.

Each area exposes an important OpenETR boundary.

### Control

OpenETR provides a technology-neutral event model for reconstructing candidate control. It does not assert that cryptographic control automatically satisfies every legal definition of control.

### Transfer And Good-Faith Acquisition

OpenETR can show the signed sequence of events and identify competing branches or policy warnings. Private law decides whether a transfer is legally effective, whether defects are cured, and whether a good-faith acquirer is protected.

### Tokenisation

A Digital Artifact identifier is not itself the cargo, goods, document of
title, or underlying claim. Nor does DCR evidence automatically create a
tokenized asset. OpenETR binds signed evidence to a digest-identified artifact,
validates that evidence, and applies protocol rules to derive consequential
state. The applicable legal framework determines what that artifact and state
embody or represent.

### Custody And Insolvency

OpenETR reduces dependence on a single platform by making signed events portable and independently storable. It does not eliminate custody risk. The legal and operational consequences of a compromised key, insolvent service provider, unavailable signer, or failed repository still require clear contractual, technical, and private-law treatment.

## Legal Statements As Recognition Infrastructure

The speech proposes that the International Jurisdiction Taskforce could publish a legal statement to clarify cross-border private-law questions and increase commercial confidence.

That kind of work complements OpenETR particularly well.

OpenETR separates control evidence from recognition. A legal statement, statute, contract, registry rule book, or institutional policy can explain how a verifier should interpret the evidence.

```text
OpenETR DCR and policy validation:
  what was signed, by which key, about which artifact, in what sequence,
  and what state results under the identified validation policy

legal or institutional rule book:
  whether the signer and transition are recognized and what effect follows
```

A widely respected legal statement could therefore become a shared recognition input without requiring every platform to implement the same internal technology.

## A Practical Catalyst

The speech calls for a catalyst capable of moving participants from technical readiness to commercial confidence.

OpenETR can contribute by making limited, cross-system pilots easier to structure. A pilot does not need to replace payment, customs, banking, carrier, or document-generation systems. It can focus on a bounded question:

```text
Can two independent systems identify the same trade record,
exchange its signed control evidence, reconstruct the same graph,
and explain any difference in legal or institutional recognition?
```

Useful pilot milestones would include:

1. agree on the canonical document or data package;
2. map domain actions to the OpenETR control grammar;
3. publish signed events from independent organizations;
4. replicate and query those events across independent infrastructure;
5. test transfer, encumbrance, discharge, surrender, and termination scenarios;
6. apply MLETR, ETDA, contractual, or institutional verifier profiles;
7. document key custody, failure, recovery, and platform-insolvency assumptions;
8. compare recognition results across jurisdictions and participants.

This is smaller than solving all of paperless trade. That is precisely what makes it useful.

## Policy Position

The speech supports a clear OpenETR policy position:

- proceed with electronic control records without waiting for digital currency;
- preserve technology neutrality across centralized, distributed, and relay-backed systems;
- treat legal certainty and interoperability as adoption infrastructure;
- keep trade data standards separate from the control-event grammar;
- describe OpenETR as evidence for reliable-system evaluation, not proof of legal compliance by itself;
- make control evidence portable so platforms do not have to share one runtime or custodian;
- use domain and jurisdictional verifier policies to make recognition assumptions explicit;
- support legal statements and cross-border principles that clarify control, transfer, tokenisation, custody, and insolvency.

## Bottom Line

The speech argues that the transition away from paper no longer depends primarily on invention. It depends on coordination, confidence, legal clarity, and practical interoperability.

OpenETR is relevant because it does not ask the market to adopt one universal trade platform or one digital currency. It offers a smaller common layer: digest-identified records, signed control events, portable graph reconstruction, and explicit policy-based recognition.

That does not finish the work of paperless trade.

It gives independent systems and legal frameworks something concrete to coordinate around.

## Source And Related Materials

- Sir Geoffrey Vos, Master of the Rolls, [*Getting the Paper out of International Trade and Finance: Why not now?*](https://github.com/trbouma/openetr/blob/main/docs/source/BFSLA.Speech.pdf), Banking and Financial Services Law Association Conference, 21 August 2026.
- [OpenETR And Paperless Trade](./openetr-and-paperless-trade.md)
- [OpenETR, MLETR, And ETDA](./openetr-mletr-and-etda.md)
- [OpenETR And TradeTrust](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_AND_TRADETRUST_COMPARISON.md)
- [System Integration Considerations](https://github.com/trbouma/openetr/blob/main/docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
