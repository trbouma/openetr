# OpenETR And Open Trust Layer

Open Trust Layer (`OTL`) and OpenETR address different but complementary parts of the digital trade trust stack.

OTL focuses on participant identity, secure communication, compliance messaging, payment sessions, and local counterparty trust decisions. OpenETR focuses on the controlled record itself: its digest, origin event, control graph, linked evidence, dependencies, and verifier-policy output.

The useful distinction is:

```text
OTL:
  who are the parties, how do they communicate,
  what credentials do they present, and how do they coordinate payment?

OpenETR:
  what record is controlled, who controls it now,
  what signed events prove its lifecycle, and what evidence supports recognition?
```

## Complementary Layers

OTL provides a participant-facing layer. It uses `did:webvh`, Verifiable Credentials, LEI and KYC-related credentials, DIDComm, out-of-band session establishment, address proofs, and payment-flow messages.

OpenETR provides an object-facing layer. It records origin, transfer, pledge, release, presentation, surrender, redemption, replacement, and dependency evidence for digest-identified records.

These layers can work together:

```text
OTL identity and transport
  -> identify counterparties and exchange messages securely

OpenETR control graph
  -> preserve durable evidence about the controlled record

Domain adapter
  -> translate evidence into eBL, eWR, eBoE, ePN, or other domain semantics

Recognition policy
  -> decide whether the evidence is accepted under law, rulebook, registry, or institutional policy
```

## Policy Position

OpenETR should not absorb OTL, and OTL should not be treated as a replacement for OpenETR.

The better architecture is compositional:

- use OTL for identity, messaging, payment coordination, and credential exchange
- use OpenETR for durable control evidence over transferable records
- use domain adapters for legal and operational meaning
- use recognition policy for final reliance decisions

This preserves an important principle:

```text
participation is open
trust is local
recognition is contextual
control evidence is portable
```

## Practical Implications

For warehouse receipts, OTL could help identify the warehouse operator, depositor, and bank, while OpenETR records issuance, pledge, release, transfer, and redemption of the receipt.

For bills of lading, OTL could help carriers, shippers, consignees, banks, and agents coordinate securely, while OpenETR preserves the eBL control graph.

For trade finance, OTL payment or settlement messages can become linked evidence in OpenETR, but payment should not automatically be treated as transfer of control unless the domain adapter and recognition policy say so.

## Boundaries To Preserve

OTL credentials can help identify a counterparty. They do not prove control over a record.

OTL address proofs can show control of a blockchain address. They do not prove control over an ETR.

OTL KYC exchanges can support compliance. They do not replace domain authority, registry status, legal recognition, or verifier policy.

OTL sessions can preserve communication continuity. OpenETR control graphs preserve object lifecycle continuity after the session, email, chat, or API context has disappeared.

## Bottom Line

OTL can make OpenETR workflows easier to coordinate and safer to exchange.

OpenETR can give OTL-enabled workflows a durable control fabric for the records that matter.

The combined policy message is simple:

```text
identify and communicate through OTL
control and verify records through OpenETR
recognize legal effect through domain policy, law, registries, and institutions
```

## Related Design Note

- [OpenETR And Open Trust Layer Review Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_AND_OPEN_TRUST_LAYER_REVIEW_NOTE.md)
