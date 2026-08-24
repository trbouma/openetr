# OpenETR And Global ETR Use Cases

The ICC Digital Standards Initiative publication `Electronic Transferable Records in Practice: Seven Cross-Border Use Cases` shows that electronic transferable records are moving from isolated pilots toward practical cross-border trade infrastructure.

The cases span electronic bills of lading, electronic bills of exchange, electronic promissory notes, and electronic warehouse receipts. They show a common pattern: the hard problem is no longer just making a paper document digital. The hard problem is preserving control, integrity, recognition context, and evidence as records move across platforms, banks, logistics systems, warehouses, registries, and jurisdictions.

## Policy Context

The publication identifies three major ETR families:

| ETR Family | Practical Role | Primary Scaling Challenge |
| --- | --- | --- |
| Electronic bills of lading | Documents of title for goods in transit | Legal recognition and platform interoperability |
| Electronic bills of exchange and promissory notes | Negotiable instruments and payment obligations | Banking network coordination and legal treatment |
| Electronic warehouse receipts | Collateral instruments for stored goods | Physical asset control and reliable warehouse evidence |

Each family needs a different domain adapter. But all three share a common need for portable evidence of origin, control, transfer, presentation, encumbrance, surrender, redemption, or discharge.

## Where OpenETR Fits

OpenETR should not be understood as a replacement for TradeTrust, GSBN, trace:original, IQAX, ICE CargoDocs, banks, customs systems, warehouse systems, MLETR, ETDA, or platform rulebooks.

OpenETR fits between systems as a correctness and control-evidence protocol:

```text
Trade ecosystem:
  laws, platforms, registries, banks, carriers, warehouses,
  customs systems, corridor arrangements, and financing contracts

OpenETR:
  digest-identified records, signed origin and control events,
  linked evidence, dependency edges, and verifier-policy output

Recognition layer:
  MLETR, ETDA, local law, rulebooks, institutional policy,
  registry status, trusted-corridor arrangements, and court decisions
```

This positioning is important. OpenETR does not grant legal effect by itself. It makes the evidence of control inspectable, portable, and reusable across recognition contexts.

## What The Use Cases Show

The use cases point to four policy lessons.

First, statutory recognition matters for scale. Platform rulebooks and bilateral arrangements can support early adoption, but MLETR-style and ETDA-style recognition reduce the need for bespoke trust arrangements.

Second, transitional mechanisms are useful. Trusted corridors, government cooperation, and MLETR-aligned issuance points can bridge legal asymmetry while reform proceeds.

Third, interoperability is now central. The cross-platform eBL cases show that participants want to keep their existing systems while still relying on a common control state.

Fourth, ETRs are becoming financing infrastructure. Bills of exchange, promissory notes, and warehouse receipts turn digitized trade records into bankable obligations, collateral, and secondary-market assets.

## OpenETR Implications

OpenETR can help by treating each transferable record as a digest-identified controlled object with a signed control graph.

For eBLs, OpenETR can record issuance, transfer, presentation, and surrender events while domain adapters preserve maritime and carrier-specific semantics.

For eBoEs and ePNs, OpenETR can record issuance, acceptance, endorsement, transfer, and discharge evidence while leaving negotiability and legal priority to the recognition layer.

For eWRs, OpenETR can record issuance, pledge, transfer, release, and redemption events while linking to warehouse attestations, inspections, inventory records, customs approvals, and financing evidence.

The common policy value is portability:

```text
build once around portable control evidence
recognize many times under law, rulebooks, corridors, registries, and verifier policy
```

## Implementation Priorities

The use cases suggest several priorities for OpenETR:

- define proof bundles that receiving systems can inspect without joining the originating platform
- make the recognition basis explicit in verifier output
- support domain adapters for eBL, eWR, eBoE, ePN, electronic delivery order, and pledge-financing packages
- model cross-object dependencies among logistics, warehouse, customs, financing, and registry records
- treat physical asset evidence as linked evidence, not as something cryptography can prove on its own
- keep the OpenETR core domain-neutral while allowing domain adapters to express legal and operational meaning

## Bottom Line

The global ETR use cases show that digital trade infrastructure is becoming multi-platform, multi-jurisdictional, and finance-facing. OpenETR fits as a portable control fabric for that environment.

It does not replace the clothing of each domain. It provides a common fabric from which domain-specific legal and operational garments can be cut.

## Related Design Note

- [OpenETR Global ETR Use Cases Review Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GLOBAL_ETR_USE_CASES_REVIEW_NOTE.md)
