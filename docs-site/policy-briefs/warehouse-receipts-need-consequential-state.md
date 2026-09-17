# Warehouse Receipts Need Consequential State

## Policy Proposition

**Warehouse receipts need consequential state.**

A warehouse receipt is not valuable merely because it describes goods. It
matters because the warehouse operator acknowledges holding those goods and
undertakes to deliver them to the holder. In a negotiable system, dealings in
the receipt may also affect control, transfer, financing, security rights, and
the person entitled to demand delivery.

Those consequences should not exist only as a status field inside a warehouse
application, registry, lending platform, or document service. Another
authorized party should be able to identify the exact receipt, verify the
signed evidence concerning it, and determine what state follows under the
applicable rules.

OpenETR provides that control-and-evidence layer. The warehouse operator,
registry, lender, holder, applicable law, and other recognition authorities
remain responsible for the receipt's commercial and legal effect.

## The MLWR Foundation

The
[UNCITRAL-UNIDROIT Model Law on Warehouse Receipts](https://uncitral.un.org/en/mlwr)
was adopted in 2024 to help States establish or modernize warehouse-receipt law
for both paper and electronic receipts. It addresses issuance and contents,
replacement and change of medium, transfers and other dealings, warehouse-
operator obligations, and an optional pledge-bond system.

Under the Model Law's basic definition, a warehouse receipt is issued and
signed by a warehouse operator to acknowledge that it holds the covered goods
for the holder and promises to deliver them to the holder. That formulation
connects three distinct subjects:

```text
the goods
  physical assets held in the warehouse

the warehouse receipt
  the paper document or electronic record concerning those goods

the consequential state
  who controls the receipt, which dealings affect it, and whether it remains
  active, encumbered, redeemable, replaced, or terminated under applicable rules
```

OpenETR is concerned primarily with the second and third subjects. It cannot
prove from cryptographic events alone that the goods exist, remain in the
warehouse, match their description, or will be delivered.

## Why A Receipt Needs State

A receipt file can state a warehouse, depositor, description of goods,
quantity, date, and receipt number. Its bytes do not independently reveal what
happened after issuance.

A relying party may need to determine:

- whether this is the exact receipt originally recorded;
- which warehouse-operator or issuer key signed the initial evidence;
- whether the receipt remains active;
- who is the current controller under the applicable rules;
- whether a transfer was initiated and accepted;
- whether an encumbrance remains outstanding;
- whether a discharge released the identified encumbrance;
- whether the receipt was presented, redeemed, or terminated;
- whether it was replaced or its medium changed; and
- which warnings, conflicts, missing links, or recognition limitations remain.

These are consequential-state questions. They cannot be answered reliably by
copying the PDF or reading its visible contents alone.

## The OpenETR Model

OpenETR separates the receipt artifact from evidence of actions concerning it:

```text
warehouse receipt PDF or canonical data package
  -> Digital Artifact identified by SHA-256 digest
  -> signed Anchor Records and later evidence records form the DCR
  -> MLWR-aware and OpenETR rules evaluate the evidence
  -> Consequential State is derived
  -> law, registry, contract, and institutional policy determine effect
```

The receipt file remains outside the OpenETR event graph. OpenETR records its
digest and structured event data needed to understand the signed action. The
document may remain in the warehouse system, document repository, lender's
records, holder's custody, or another authorized store.

The DCR can travel independently of any one copy or storage location. Any exact
copy produces the same digest and can be evaluated against the same signed
evidence.

## A Digital Original Warehouse Receipt

Paper practice associates originality with a particular physical document.
Electronic records are naturally copyable, so the operative distinction must
come from evidence and state rather than physical scarcity.

In OpenETR:

- the digest identifies the exact Digital Artifact;
- the Anchor begins a candidate DCR for that artifact;
- signed evidence records preserve attributable consequential actions;
- graph links establish the claimed transition history;
- rules derive the current Consequential State; and
- the Digital Artifact with that state is a Digital Original.

Identical copies represent the same receipt artifact. Possessing a copy does
not independently make someone the controller, duplicate an encumbrance, or
create another valid receipt history.

Whether this satisfies a jurisdiction's requirements for an electronic
warehouse receipt, exclusive control, protected-holder status, or another legal
category remains a recognition question.

## Candidate Receipt Lifecycle

The current OpenETR control model can represent a focused receipt lifecycle:

```text
issue / Anchor
  -> active under initial controller
  -> transfer initiated
  -> transfer accepted by new controller
  -> encumbered and later discharged
  -> presented or redeemed
  -> terminated
```

Not every action forms one linear status. An active receipt may have multiple
encumbrance records, each requiring a discharge linked to the specific
encumbrance. A verifier should enumerate the graph and report outstanding
guards rather than reduce every condition to one label.

MLWR-specific profiles also need to address:

- replacement of a lost or damaged receipt;
- correction or amendment;
- change from paper to electronic medium or the reverse;
- delivery of part or all of the goods;
- non-negotiable and negotiable receipt distinctions;
- pledge bonds where adopted; and
- conflicting claims or legally ordered changes.

Some of these are implemented in the current demonstration; others remain
design and recognition work tracked in the MLWR requirements mapping.

## The Warehouse Operator Boundary

The warehouse operator has responsibilities that a signed event cannot replace.
Depending on applicable law and contract, these may include taking custody of
the goods, exercising care, keeping goods appropriately separate, issuing an
accurate receipt, and delivering goods to the person entitled to receive them.

The host warehouse system should remain responsible for:

- authenticated user accounts;
- warehouse and facility authorization;
- document preparation and issuance;
- inventory and physical-custody records;
- operational approvals;
- key custody and signing access;
- KYC, KYB, licensing, and compliance controls;
- connection between digital redemption and physical delivery; and
- correction, dispute, audit, and recovery procedures.

OpenETR records attributable evidence concerning the receipt and derives
protocol state. It does not operate the warehouse.

## Control Desk And Commitment Profiles

The OpenETR Warehouse Receipts application uses a **Control Desk** metaphor to
hide cryptographic mechanics behind a familiar operational surface.

```text
Control Desk Key
  organizes and recovers relay-backed configuration

Commitment Profiles
  independent operational signing keys organized by the Control Desk Key

Acting Profile
  the selected Commitment Profile signing the current receipt action
```

A warehouse may assign Commitment Profiles to facilities, operational roles,
departments, services, or automated workflows. The key identifies the signer
cryptographically. The warehouse system and recognition policy establish why
that key is authorized to act for the warehouse operator.

The root relationship is an integration and recovery convenience. It does not
make every profile action legally authorized merely because the Control Desk
Key organizes the profile.

## Making Receipt Consequences Portable

Warehouse-receipt systems do not need to become one global registry or adopt
one account and identity model. Their shared requirement can be smaller:

```text
receipt digest
  + attributable DCR evidence
  + graph relationships
  + identified rules and evaluation parameters
  -> reproducible Consequential State
  -> MLWR, local-law, registry, and counterparty recognition
  -> commercial or legal effect
```

A lender can examine encumbrance evidence. A buyer can inspect the candidate
controller path. A warehouse can evaluate presentation or redemption. A
registry can apply admission and reliability rules. A court can consider the
evidence under applicable law. They need not use the same application to begin
from the same cryptographic record.

> Do not make every warehouse, lender, registry, and trade platform share one
> database. Make the evidence of receipt consequences independently verifiable.

## Control Is Not Physical Custody

OpenETR control concerns the receipt artifact and the state derived from its
signed records. It does not prove physical custody or condition of the goods.

Evidence about the goods may be linked from:

- warehouse inventory systems;
- inspection and grading reports;
- weighing or measurement records;
- insurance certificates;
- IoT devices and environmental monitors;
- customs or regulatory records;
- photographs or other provenance systems; and
- recognized warehouse or third-party attestations.

Each item proves only what its issuer, method, and evidence support. A sensor
reading does not prove legal control. A warehouse signature does not prove the
goods are free of hidden defects. A valid receipt control graph does not prove
that physical delivery occurred.

## Encumbrance And Finance

Warehouse receipts can support financing because rights concerning stored
goods may be pledged or otherwise encumbered. This makes outstanding
encumbrances a central verifier concern.

OpenETR can preserve:

- the beneficiary or secured-party key identified by an encumbrance;
- the event that created the encumbrance;
- the controller and signer at that point in the graph;
- any guards the encumbrance places on later actions;
- a discharge linked to the exact encumbrance event; and
- unresolved or competing encumbrance evidence.

The protocol can report which encumbrances remain outstanding under its rules.
It does not determine perfection, priority, the secured obligation, protected-
holder status, or the legal effect of a discharge. Those conclusions belong to
secured-transactions law, the MLWR enactment, registry rules, contracts, and
applicable recognition policy.

## Change Of Medium And Replacement

The MLWR expressly addresses replacement and change of medium. These actions
need more than a new file upload because they can affect which representation
is operative.

A suitable OpenETR profile should preserve evidence that:

- an authorized actor initiated the change or replacement;
- the prior receipt and successor artifact are cryptographically identified;
- the relationship between them is explicit;
- the prior representation's consequential status is updated under the rules;
- duplicate operative receipts are not silently created; and
- the applicable warehouse, registry, and legal requirements were evaluated.

OpenETR design notes already track these concepts. Their legal sufficiency and
full implementation remain profile and pilot work.

## Recognition And Verifier Policy

The same authentic DCR evidence may receive different conclusions from
different verifiers.

A verifier may need to ask:

- Is the warehouse operator licensed or otherwise recognized?
- Does the signing key map to an authorized warehouse profile?
- Does the receipt contain the information required by applicable law?
- Does the system satisfy the required reliability standard?
- Is the candidate controller recognized as the holder?
- Do outstanding encumbrances block the proposed action?
- Does the jurisdiction recognize the electronic medium and method?
- Are physical-goods attestations sufficiently current?
- Does a protected-holder, priority, or delivery rule apply?

OpenETR should report cryptographic integrity, graph validity, Consequential
State, warnings, and recognition inputs separately. It should not compress all
of these questions into a universal `valid` result.

## Policy And Pilot Priorities

A warehouse-receipt implementation should:

1. begin with the operator issuing a receipt and creating its Anchor record;
2. identify the final receipt artifact by a deterministic SHA-256 digest;
3. keep receipt content and physical-goods systems outside the event graph;
4. connect each Commitment Profile to an authenticated and authorized warehouse
   account or workflow;
5. implement transfer, encumbrance, discharge, redemption, and termination with
   explicit prior-event links;
6. report all outstanding encumbrances and material graph conflicts;
7. link physical-custody and condition evidence without overclaiming what it
   proves;
8. develop replacement and change-of-medium workflows against the MLWR article
   mapping;
9. test retrieval and state derivation outside the originating warehouse
   application; and
10. involve warehouse operators, lenders, registries, holders, and legal
    authorities in recognition-policy design.

## What OpenETR Does Not Do

OpenETR does not:

- create or operate a warehouse;
- prove that goods exist, remain stored, or match the receipt description;
- replace inventory, registry, lending, or document-management systems;
- perform KYC, KYB, licensing, or account authentication;
- establish legal identity from a public key alone;
- determine title, priority, perfection, liability, or protected-holder status;
- guarantee exclusive control merely because a candidate graph exists;
- make a receipt legally negotiable or transferable;
- complete physical delivery when a receipt is redeemed; or
- compel recognition under the MLWR or any national law.

## Bottom Line

Warehouse receipts connect a document to goods, control, financing, and
delivery. Their value depends on consequences that must remain intelligible as
the receipt crosses warehouses, holders, lenders, registries, platforms, and
jurisdictions.

> The warehouse remains responsible for the goods. The law determines receipt
> effect. No one application should exclusively own the evidence needed to
> derive the receipt's consequential state.

That is the focused role of OpenETR in an MLWR-aligned warehouse-receipt system.

## Related Reading

- [Warehouse Receipts workspace](../getting-started.md)
- [MLWR Article Mapping](../mlwr-article-mapping.md)
- [Warehouse Receipt Pilot Notes](../warehouse-receipt-pilot.md)
- [Creating Receipt Evidence Records](../issuing-receipts.md)
- [Receipt Control Actions](../control-actions.md)
- [OpenETR MLWR Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_MLWR_PROFILE.md)
- [MLWR Article Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_ARTICLE_REQUIREMENTS_MAPPING.md)
- [MLWR Change Of Medium Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_CHANGE_OF_MEDIUM_PROFILE.md)
- [MLWR Receipt Replacement And Loss Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_RECEIPT_REPLACEMENT_AND_LOSS_PROFILE.md)

