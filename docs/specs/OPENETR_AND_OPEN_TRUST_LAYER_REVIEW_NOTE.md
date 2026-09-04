# OpenETR And Open Trust Layer Review Note

This note reviews the Open Trust Layer (`OTL`) protocol in relation to OpenETR.

Source reviewed:

- Open Trust Layer protocol draft: `https://www.otl.network/spec.html`
- Requested repository reference: `https://github.com/open-trust-layer/protocol.git`

The GitHub repository URL did not render directly during review, but the published protocol draft provides enough protocol detail to compare the architecture with OpenETR.

## Status

Draft review note.

## Summary

Open Trust Layer and OpenETR are complementary protocols, but they solve different problems.

OTL is participant-centric. It is concerned with identity, secure communication, counterparty validation, payment-session establishment, payment flows, compliance messaging, address proofs, and optional credential presentation.

OpenETR is object-centric. It is concerned with controlled records, signed origin events, control events, linked evidence, dependency edges, verifier-policy output, and recognition boundaries for electronic transferable records and other controllable records.

The compact distinction is:

```text
OTL:
  who are the participants, how do they communicate,
  what credentials do they present, and how do they coordinate payment?

OpenETR:
  what is the controlled record, what events define its lifecycle,
  who currently controls it, and what evidence supports recognition?
```

This makes OTL a plausible identity, secure messaging, and payment-coordination layer around OpenETR.

It does not make OTL a replacement for OpenETR's control graph.

## OTL Protocol Summary

OTL describes itself as open, permissionless infrastructure for verifiable identity and secure coordination in global crypto payments. It is designed to allow regulated virtual asset service providers (`VASPs`), self-custodied wallet holders, and autonomous agents to interoperate without a central coordinator, shared registry, or pre-approved consortium.

The design principles most relevant to OpenETR are:

- participants should not depend on a single central operator
- personally identifiable information should not touch shared infrastructure
- participation should be separate from trust
- trust and risk decisions should be made locally by each participant
- protocol layers should be modular and independently adoptable
- credentials enrich a participant's identity but do not create a single global gatekeeping system

The protocol is organized into five layers:

| OTL Layer | Function |
| --- | --- |
| Identity | `did:webvh`, Verifiable Credentials, LEI, KYC, service endpoints |
| Session Establishment | out-of-band session bootstrap through URL, QR, deep link, EIP-1193, or HTTP 402 flows |
| Transport | DIDComm v2 sign-then-encrypt envelopes and REST modes |
| Message Standards | typed message bodies for payment proposals, IVMS101, address proofs, credentials, negotiation, and settlement |
| Application | payment requests, push payments, payment channels, wallet attribution, non-custodial wallet identity, mint/burn requests |

OTL's identity model is based on `did:webvh`, where a participant publishes a DID document on an HTTPS domain. The DID document contains signing keys, encryption keys, service endpoints, and a `#whois` pointer to a public Verifiable Presentation where the participant may disclose claims such as LEI credentials.

OTL's transport model uses DIDComm for bilateral participant flows, with an inner signature for sender authentication and non-repudiation and an outer encrypted envelope for confidentiality. Some non-custodial wallet and agent flows can use REST-based interaction rather than a full DIDComm channel.

OTL's application layer defines payment and compliance flows. The protocol also emphasizes that the lower-layer primitives can be reused independently of the full DIDComm stack.

## OpenETR Summary

OpenETR is a control and evidence protocol for digest-identified records.

Its core concern is not participant discovery or payment-session choreography.

Its core concern is:

```text
record artifact or canonical package
  -> digest
  -> signed origin event
  -> signed control and evidence events
  -> control graph
  -> verifier-policy output
  -> recognition decision by an external layer
```

OpenETR is especially concerned with electronic transferable records and related controllable records, including:

- warehouse receipts
- bills of lading
- bills of exchange
- promissory notes
- delivery orders
- apostille documents
- product passports
- health records
- other records where control, presentation, transfer, redemption, replacement, or dependency integrity matter

OpenETR does not do KYC, legal entity registration, counterparty onboarding, federation governance, bank compliance, customs approval, or legal recognition by itself.

It preserves portable signed evidence that those systems can evaluate.

## Architectural Comparison

| Question | OTL Answer | OpenETR Answer |
| --- | --- | --- |
| Who is this participant? | Resolve `did:webvh`, inspect keys, endpoints, and credentials | Resolve OpenETR profile/root references and linked identity evidence |
| What organization is behind the participant? | LEI, KYC, licensing, and other Verifiable Credentials | Recognition policy may consult LEI, proto-LEI, registries, credentials, or platform accounts |
| How do participants communicate? | DIDComm, REST, OOB URLs, QR/deep links, HTTP 402 payment flows | Transport-neutral; events can move over Nostr relays, APIs, bundles, files, or other channels |
| What is the operative object? | Usually a payment request, session, address proof, or compliance message | A digest-identified Controlled Object |
| What changes state? | Application flow messages and payment/settlement events | Signed control events linked into a control graph |
| Who decides trust? | Each participant's local trust perimeter | Each verifier's policy and domain recognition context |
| What is private? | PII carried over encrypted peer-to-peer channels | Controlled content may stay external; OpenETR can expose hashes, event metadata, and selective linked evidence |
| What is durable? | DID logs, signed requests, message records, payment receipts, credential presentations | Object digest, origin event, control events, linked evidence, dependency edges, verifier output |

The most important difference is that OTL is optimized around participants and sessions, while OpenETR is optimized around controlled objects and lifecycle evidence.

## Complementarity

OTL can help OpenETR answer participant and channel questions.

OpenETR can help OTL-linked ecosystems answer controlled-record lifecycle questions.

The combined architecture can be described as:

```text
OTL identity layer
  did:webvh, LEI credentials, KYC credentials, licensing credentials,
  service endpoints, address ownership proofs

OTL session and transport layer
  OOB envelope, DIDComm, REST, payment-request flow,
  compliance and settlement messages

OpenETR object-control layer
  controlled object digest, origin event, control events,
  linked evidence, dependency edges, verifier-policy output

Domain adapter
  eBL, eWR, eBoE, ePN, eDO, apostille, product passport,
  warehouse receipt, or other domain-specific semantics

Recognition layer
  MLETR, ETDA, local law, platform rulebook, federation agreement,
  registry status, bank policy, court or administrative decision
```

In that architecture, OTL provides the participant-facing trust and communication substrate. OpenETR provides the object-facing control and evidence substrate.

Neither layer should absorb the other.

## Example Integration Pattern

An OpenETR event or proof bundle could be exchanged over an OTL DIDComm channel.

The flow might look like:

```text
1. Party A publishes a did:webvh identity and service endpoint.
2. Party B resolves Party A's DID and evaluates credentials.
3. The parties establish an OTL session.
4. Party A sends an OpenETR proof bundle over the encrypted channel.
5. Party B verifies OpenETR signatures, event linkage, object digest,
   dependency edges, and domain-adapter rules.
6. Party B evaluates the result under local recognition policy.
7. A payment, pledge, settlement, release, or other application event
   may be linked back into the OpenETR evidence graph.
```

The OpenETR proof bundle should remain independently verifiable after the OTL session ends.

The OTL channel can improve confidentiality and counterparty assurance, but the control evidence should not depend on the availability of the OTL session transcript unless that transcript is intentionally retained as linked evidence.

## Warehouse Receipt Pilot Implications

For a warehouse receipt pilot, OTL could provide useful surrounding infrastructure:

- identify the warehouse operator through `did:webvh`
- expose LEI or licensing credentials through a public presentation
- establish encrypted channels among the depositor, warehouse operator, bank, and verifier
- carry KYC or compliance material outside shared infrastructure
- carry payment, fee, pledge, release, or settlement coordination messages

OpenETR would remain responsible for the record-control layer:

- create the warehouse receipt Controlled Object
- bind the receipt to a digest
- record the warehouse operator's origin event
- record transfer, pledge, release, redemption, termination, or replacement events
- link inspection, inventory, customs, insurance, registry, or financing evidence
- derive current control and warnings under verifier policy

The pilot boundary should remain explicit:

```text
OTL may help identify and communicate with account holders.
The warehouse system remains responsible for KYC and account controls.
OpenETR records signed control evidence for the receipt.
Recognition policy decides whether to rely on that evidence.
```

## Bills Of Lading Implications

For electronic bills of lading, OTL could support secure coordination among carriers, shippers, consignees, banks, and agents.

It could help answer:

- is this counterparty reachable at a verified endpoint?
- does the counterparty disclose an LEI or other organizational credential?
- can the parties exchange presentation or payment details confidentially?
- can settlement or fee evidence be linked to the transaction?

OpenETR would answer:

- what exact eBL artifact or package is controlled?
- who originated it?
- which transfer event currently controls it?
- has it been presented or surrendered?
- are there conflicting branches or missing predecessor events?
- which registry, carrier, or platform evidence supports recognition?

In this model, OTL can support the corridor. OpenETR preserves the transferable record's control graph.

## Trade Finance Implications

For trade finance, OTL and OpenETR may be especially useful together.

OTL can coordinate payment and compliance flows. OpenETR can represent the controlled record, obligation, or collateral whose state affects the financing decision.

Examples:

- an eWR pledge financing event can link to an OTL payment or settlement receipt
- a bill of exchange transfer can be sent through an OTL DIDComm channel
- a bank can evaluate the counterparty through OTL credentials and evaluate the asset through OpenETR control evidence
- a verifier can keep KYC material private while retaining portable public evidence of the controlled record's lifecycle

This reinforces the idea that digital trade infrastructure needs both actor trust and object integrity.

## Identity Boundary

OTL's `did:webvh` identity model is useful, but OpenETR should not require it as the only identity substrate.

OpenETR currently has its own root and profile identity model. It should be able to link to:

- `did:webvh`
- LEI and proto-LEI records
- W3C Verifiable Credentials
- platform account identifiers
- Nostr public keys
- local registry identifiers
- domain-specific authority identifiers

The appropriate design is an identity-evidence binding:

```text
OpenETR profile signer
  -> linked identity evidence
  -> did:webvh / LEI / VC / registry / platform account
  -> verifier policy
  -> accepted, warning, rejected, or manual review
```

This preserves OpenETR's substrate neutrality while allowing OTL participants to be first-class identity evidence.

## Transport Boundary

OTL's DIDComm transport is attractive for confidential bilateral exchange.

OpenETR should remain transport-neutral.

An OpenETR event or proof bundle may travel through:

- Nostr relays
- OTL DIDComm channels
- direct API calls
- file attachments
- registry submissions
- platform-to-platform integrations
- offline evidence bundles

The transport may authenticate or encrypt delivery, but the OpenETR event must remain verifiable as an object-level assertion after transport.

This distinction prevents a common design mistake:

```text
secure delivery of a message
  !=
durable control state for the underlying record
```

OTL helps with secure delivery. OpenETR helps with durable control state.

## Payment Boundary

OTL's payment-request, push-payment, payment-channel, wallet-attribution, and mint/burn flows are adjacent to OpenETR but should not be confused with OpenETR control events.

A payment may be evidence for a domain-specific action.

Examples:

- payment evidence may support release of goods
- settlement evidence may support discharge of an obligation
- pledge financing proceeds may support creation of an encumbrance
- fee payment may support issuance or presentation

But payment is not automatically transfer of control.

OpenETR should model payment-related facts as linked evidence unless the domain adapter and recognition policy say that a payment event also triggers a control event.

## Compliance Boundary

OTL includes support for compliance exchanges, including IVMS101-style Travel Rule payloads and KYC-related credentials.

OpenETR should not incorporate KYC or AML checks into the base protocol.

Instead:

```text
compliance system / OTL credential exchange
  -> produces attestation, verifier output, or linked evidence
  -> OpenETR graph references that evidence where relevant
  -> domain policy decides whether the evidence is sufficient
```

This aligns with the warehouse receipt pilot boundary:

- the reliable system creates accounts tied to legal identity
- the reliable system manages KYC and account controls
- OpenETR records the signed control evidence that exists between systems
- recognition and federation are arrangements among system operators and relying parties

## Policy Alignment

OTL and OpenETR share an important policy posture:

```text
participation is open
trust is local
recognition is contextual
```

OTL expresses this through local trust perimeters, optional credentials, and modular protocol layers.

OpenETR expresses this through verifier policy, domain adapters, recognition boundaries, and portable evidence graphs.

Both avoid a single global trust authority.

The difference is the subject of trust:

```text
OTL:
  trust in participants and communication flows

OpenETR:
  trust in the lifecycle evidence of a controlled object
```

## Risks And Cautions

### Do Not Make OTL A Required OpenETR Dependency

OTL is valuable, but OpenETR should not depend on OTL for its base model.

OpenETR should be able to operate in jurisdictions, domains, and systems that use different identity and messaging stacks.

### Do Not Treat Address Proof As Record Control

An OTL address proof can show that a participant controls or is associated with a blockchain address.

It does not prove control over an ETR.

Control over an ETR should be represented in OpenETR through signed control events and verifier-policy derivation.

### Do Not Treat KYC As Recognition

KYC may establish that an account is tied to a legal identity.

It does not, by itself, establish that the account is authorized to issue, transfer, pledge, or redeem a particular class of record.

Domain authority still needs to be evaluated.

### Do Not Confuse Session Continuity With Object Continuity

OTL sessions provide bilateral interaction continuity.

OpenETR control graphs provide object lifecycle continuity.

An OpenETR proof should remain meaningful even when the session, chat, email, or API context in which it was exchanged is gone.

### Do Not Collapse Payment And Transfer

A payment can trigger a domain workflow, but payment does not automatically transfer title, possession, control, pledge rights, or documentary status.

The domain adapter must make that relationship explicit.

## Recommended OpenETR Work Items

The OTL comparison suggests several useful OpenETR design tasks:

- define an OTL-linked identity evidence profile
- define how `did:webvh` identifiers can appear in OpenETR linked evidence
- define a proof-bundle transport profile for DIDComm exchange
- define a payment-evidence linked event pattern
- define how OTL LEI/KYC/licensing credentials can be referenced without embedding private data
- add verifier-policy language for identity evidence source, credential issuer, and trust perimeter
- preserve Nostr/root/profile identity neutrality in the OpenETR core

## Open Questions

- Should OpenETR define a DID-linked profile binding format?
- Should OpenETR define an optional OTL transport profile for proof-bundle exchange?
- Should payment receipts be modeled as generic linked evidence or as a dedicated event kind?
- How should OpenETR represent confidential evidence that exists only inside an encrypted OTL channel?
- Should an OpenETR verifier output distinguish actor-identity confidence from object-control confidence?
- How should a domain adapter represent workflows where payment is a precondition for transfer, release, or surrender?

## Conclusion

Open Trust Layer and OpenETR address adjacent parts of the digital-trade trust stack.

OTL is well suited to participant identity, secure coordination, compliance messaging, and payment-session workflows.

OpenETR is well suited to durable object-control evidence for electronic transferable records and controllable records.

Together, they suggest a strong architecture:

```text
identify and coordinate through OTL
control and verify records through OpenETR
recognize legal effect through domain policy, law, registries, and institutions
```

That boundary should be preserved.

OTL can make OpenETR interactions easier and more secure. OpenETR can give OTL-linked trade workflows a durable, inspectable control graph for the records that move through them.

## Related Policy Brief

- [OpenETR And Open Trust Layer](../../docs-site/policy-briefs/openetr-and-open-trust-layer.md)

## Related Documents

- [OpenETR, W3C DIDs, Nostr, And did:webvh Analysis Note](./OPENETR_DIDS_NOSTR_AND_DID_WEBVH_ANALYSIS_NOTE.md)
- [OpenETR Organizational Reference Layer Design Note](./OPENETR_ORGANIZATIONAL_REFERENCE_LAYER_DESIGN_NOTE.md)
- [OpenETR, LEI, And Verifiable Trade Policy Brief](../../docs-site/policy-briefs/openetr-lei-and-verifiable-trade.md)
- [OpenETR Generic Domain Adapter Specification](./OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR MLETR And ETDA Mapping Design Note](./OPENETR_MLETR_ETDA_MAPPING_DESIGN_NOTE.md)
- [OpenETR Dependency Integrity Design Note](./OPENETR_DEPENDENCY_INTEGRITY_DESIGN_NOTE.md)
