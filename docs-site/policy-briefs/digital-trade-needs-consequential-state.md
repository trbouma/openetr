# Digital Trade Needs Consequential State

## Policy Proposition

**Digital trade needs consequential state.**

Trade does not become digital merely because a document becomes a PDF, a form
becomes data, or a workflow moves online. Trade records matter because actions
concerning them have consequences: goods may be released, control transferred,
payment demanded, collateral encumbered, obligations discharged, or a record
terminated.

The policy and architectural question is therefore not only:

> Can the document move electronically?

It is also:

> Can another party independently determine what happened concerning the
> record, what state follows, and whether that state should be recognized?

OpenETR addresses that second question. It makes signed evidence concerning an
exact Digital Artifact portable across systems and allows Consequential State
to be derived under identified rules. Commercial parties, registries,
institutions, contracts, and applicable law remain responsible for recognition
and effect.

## From Paperless Documents To Digital Trade

The [WTO Trade Facilitation Agreement](https://www.wto.org/english/docs_e/legal_e/tfa_e.htm)
supports faster movement, release, and clearance of goods, cooperation among
border authorities, and greater acceptance of electronic processes and copies.
The WTO's
[cross-border paperless trade resources](https://www.wto.org/english/tratop_e/dtt_e/dtt-cross_e.htm)
also emphasize that implementation requires legal, technical, governance, and
standards work rather than document conversion alone.

Trade is a plurality of systems:

- exporters and importers;
- carriers, freight forwarders, ports, and terminals;
- warehouse operators and inspection services;
- banks, insurers, and secured lenders;
- customs and other border authorities;
- registries, single windows, and trade platforms; and
- courts, arbitral bodies, and other recognition authorities.

These participants do not share one database, application, jurisdiction, or
rule book. Yet they need to rely on many of the same consequential records.

## The Consequential Record

A commercial record does more than convey information. Depending on its domain
and recognition context, it may provide evidence that:

- a warehouse operator holds identified goods;
- a carrier received or shipped goods;
- a named party controls a transferable record;
- a transfer or endorsement occurred;
- a security interest or encumbrance remains outstanding;
- a document was presented or surrendered;
- an obligation was performed or discharged;
- an inspection, origin, or compliance claim was made; or
- a record ceased to have effect.

The contents of a document may explain the transaction, but the file alone
does not preserve all of these consequences. A receiving party also needs
evidence of the relevant actions, their attribution, their relationships to
prior actions, and the rules under which a resulting state is derived.

OpenETR separates those concerns:

```text
Digital Artifact
  exact persistent content identified by digest

Digital Controllable Record
  signed evidence concerning consequential actions

Consequential State
  the result derived from validated DCR evidence under identified rules

Recognition And Effect
  the commercial, institutional, contractual, or legal conclusion
```

## The Platform Boundary

Many digital trade systems make one platform the exclusive source of the
operative answer. The platform stores the document, maintains the participant
accounts, decides which workflow actions are available, and displays who
currently controls the record.

That model can work within a network. It becomes a barrier when the record
must cross platforms, when a participant changes providers, when evidence is
needed years later, or when different institutions need to apply different
recognition policies.

The concentration also creates commercial and institutional leverage. Whoever
controls the application, database, API, or registry may control access to the
record's history and current status. Service interruption, vendor failure,
withdrawal of cooperation, data loss, or a contractual dispute can become a
state-verification failure.

OpenETR proposes a narrower dependency:

> A platform may operate the workflow without exclusively owning the evidence
> from which the record's consequential state is derived.

Applications remain useful. They authenticate users, enforce permissions,
manage documents, coordinate approvals, connect to physical operations, and
present state. OpenETR gives the consequential evidence an existence that can
survive outside the application.

## Making Trade Consequences Portable

OpenETR does not send a mutable status field from one platform to another. It
makes the basis for reproducing the result portable:

```text
artifact identity
  + attributable signed events
  + cryptographic graph relationships
  + identified rules and evaluation parameters
  -> reproducible Consequential State
  -> contextual recognition
  -> commercial or legal effect
```

This allows the internal bureaucracy to remain upstream. An exporter, carrier,
warehouse, bank, or authority can use its own accounts, identity systems,
approval chains, and operational controls. The receiving party need not adopt
the same internal organization. It evaluates the consequential record and
introduces only the identity, authority, and recognition evidence required for
its purpose.

The interoperability principle is:

> Do not require every trade system to share one authority model. Make the
> evidence needed to reproduce the consequential result portable.

## Relationship To MLETR

The
[UNCITRAL Model Law on Electronic Transferable Records](https://uncitral.un.org/en/texts/ecommerce/modellaw/electronic_transferable_records)
enables electronic records to perform functions associated with transferable
paper documents and instruments. Its technology-neutral framework emphasizes
identification of the electronic transferable record, integrity, control,
exclusive control, identification of the person in control, reliability, and
change of medium.

OpenETR can supply technical evidence relevant to those functions:

| MLETR Concern | OpenETR Contribution |
| --- | --- |
| Identify the record | A cryptographic digest identifies the exact Digital Artifact. |
| Preserve integrity | The digest is recomputable and signed events are tamper-evident. |
| Establish control evidence | A DCR records attributable control transitions. |
| Derive current control | Rules evaluate the valid candidate Control Graph. |
| Identify the controller | A signing key is cryptographically attributable; external evidence supports actor recognition. |
| Assess reliability | Verifier output and integration evidence support a method-level and system-level assessment. |
| Change medium | Domain actions can record an authorized transition between electronic and paper representations. |

OpenETR does not declare that these contributions satisfy MLETR in a particular
jurisdiction. MLETR expressly preserves the role of substantive law, and each
enactment may differ. The protocol supplies evidence for an applicable legal or
institutional analysis.

## Warehouse Receipts As The First Domain

The
[UNCITRAL-UNIDROIT Model Law on Warehouse Receipts](https://uncitral.un.org/en/mlwr)
provides a concrete first domain. Warehouse receipts can support the transfer
of stored goods and their use as collateral. The Model Law addresses issuance,
contents, replacement, change of medium, transfers, dealings, warehouse-operator
obligations, and pledge bonds.

The OpenETR Warehouse Receipts domain adapter translates that language into a
general protocol model:

```text
warehouse receipt PDF or data package -> Digital Artifact
issuance and evidence records          -> DCR evidence
transfer, encumbrance, discharge,
redemption, termination               -> consequential actions
MLWR and local law                    -> recognition and effect
```

The document can continue to move through existing channels. OpenETR is
concerned with its digest and the signed evidence of consequential actions,
not with becoming the warehouse's inventory, document-management, lending, or
registry system.

## Other Digital Trade Domains

The same architecture can support distinct domain adapters:

| Domain | Examples Of Consequential State |
| --- | --- |
| Electronic bills of lading | current controller, transfer, presentation, surrender, termination |
| Warehouse receipts | issuance, control, encumbrance, discharge, delivery, cancellation |
| Bills of exchange and promissory notes | issuance, acceptance, transfer, presentment, payment, discharge |
| Certificates and inspection records | issued, superseded, withdrawn, accepted for a stated purpose |
| Product Passports | current evidence set, lifecycle status, repair, recall, retirement |
| Customs and trade permissions | submitted, accepted, amended, released, suspended, revoked |

Each adapter supplies natural business terminology and domain rules. The
OpenETR core remains concerned with artifact identity, signed DCR evidence,
graph relationships, and state derivation.

## Recognition Is Still The Work

Portable evidence does not make trade law or institutional policy disappear.
A bank, carrier, warehouse, customs authority, registry, insurer, buyer, or
court may ask different questions of the same DCR:

- Is the issuer recognized for this document type?
- Does the signing key map to an authorized legal or operational actor?
- Was the applicable reliable method used?
- Is the evidence set sufficiently complete?
- Does an encumbrance prevent the proposed action?
- Is the record recognized under the governing law or contract?
- What priority, title, liability, or protected-holder effect follows?

OpenETR keeps these recognition questions visible instead of hiding them inside
one universal `valid` result. The same authentic evidence may be accepted under
one policy, produce warnings under another, and lack legal effect under a
third.

## Policy And Adoption Priorities

Governments, trade bodies, financial institutions, and technology providers
considering this architecture should:

1. identify the documents and events that genuinely change commercial or legal
   position;
2. map domain terminology and law to the OpenETR core without importing one
   jurisdiction's legal conclusions into the protocol;
3. separate document movement from portable evidence of control and lifecycle
   actions;
4. make verifier output disclose the evidence set, rules, warnings, conflicts,
   and recognition basis;
5. test cross-platform retrieval and verification rather than only workflows
   inside one vendor environment;
6. preserve confidentiality by keeping commercial content off public relays
   unless publication is appropriate;
7. connect signed digital actions to the systems that control physical goods,
   settlement, delivery, and regulatory operations;
8. provide durable archives and evidence packages in addition to live relay or
   API access; and
9. pilot with a narrow document family and real relying parties before
   expanding the domain model.

## What OpenETR Does Not Do

OpenETR does not:

- replace MLETR, MLWR, ETDA, trade law, or contracts;
- prove the existence, condition, location, or delivery of physical goods;
- perform KYC or establish legal identity;
- operate customs, banking, logistics, warehouse, or settlement systems;
- provide global ordering or consensus;
- guarantee that all relevant evidence has been retrieved;
- determine title, priority, negotiability, liability, or legal effect; or
- require every participant to use the same application or infrastructure.

Those boundaries are a source of interoperability. They let OpenETR remain a
small control-and-evidence layer beneath a plurality of commercial systems and
legal regimes.

## Bottom Line

Paperless trade makes information electronic. Digital trade also requires the
consequences of important records to remain intelligible across systems,
organizations, and jurisdictions.

OpenETR contributes a focused architectural principle:

> Trade platforms can manage workflows. They should not have to be the
> exclusive source from which consequential state can be known.

By making artifact identity and signed DCR evidence portable, OpenETR allows
another system to reconstruct the record, apply identified rules, derive
Consequential State, and make its own recognition decision. That is how digital
trade records can move without requiring the world's trade systems to become
one platform.

## Related Reading

- [Warehouse Receipts Need Consequential State](warehouse-receipts-need-consequential-state.md)
- [OpenETR And Paperless Trade](openetr-and-paperless-trade.md)
- [OpenETR, MLETR, And ETDA](openetr-mletr-and-etda.md)
- [OpenETR And Global ETR Use Cases](openetr-and-global-etr-use-cases.md)
- [OpenETR, LEI, And Verifiable Trade](openetr-lei-and-verifiable-trade.md)
- [Warehouse Receipts](../getting-started.md)
- [Consequential State](../openetr/consequential-state.md)
- [System Integrator Guidance](../system-integrators/index.md)
