# Graduated Disclosure

Digital verification is often framed as a choice between revealing a record
and withholding it. That is too crude for ordinary institutional and community
work.

A passport should not have to be published merely so a relying party can check
an authority's attestation. A vendor permit may reasonably be public. A damage
photograph may need to be inspected by an insurer but retained only when a
claim is disputed. A delivery photograph may need to be available to the
customer without remaining under the exclusive control of the delivery
platform.

OpenETR supports a more practical model: **graduated disclosure**.

> Publish the evidence necessary for verification, disclose the record only
> when the decision requires it, and retain it only when deeper verification
> is justified. Surrender control only when the domain and legal context call
> for an actual transfer, discharge, cancellation, or custodial handoff.

## What Graduated Disclosure Means

Graduated disclosure increases access and verification depth in proportion to
the consequence of the decision.

In plain language, the interaction can be described as:

```text
Check     -> verify signed evidence without taking the record
Present   -> inspect the exact record temporarily for a decision
Share     -> receive and retain the record when deeper review is justified
Surrender -> transfer, discharge, cancel, or give up control of the record
```

These words are intentionally ordinary. They describe what a user or verifier
is trying to do, without forcing them to learn protocol vocabulary first.

| Plain-language level | Record exposure | Technical pattern |
| --- | --- | --- |
| **Check** | The artifact remains private; the verifier checks digest-bound signed evidence, status, and recognized signer information | Evidence-only verification |
| **Present** | The exact artifact is made available temporarily so the verifier can inspect it and compare its digest with the signed evidence | Presentation verification |
| **Share** | The verifier receives the exact artifact and may retain it under an appropriate authority, agreement, or policy | Deep verification |
| **Surrender** | Control is transferred, discharged, redeemed, cancelled, revoked, or given into another authority's custody | Control event, termination event, redemption event, revocation event, or domain-specific recognition act |

Some records may also be intentionally public. In that case, anyone can inspect
the artifact and compare it with the signed evidence. Public records still fit
the model, but they start from a higher-disclosure posture.

The more technical disclosure ladder is:

```text
signed evidence only
    -> public or temporary representation
    -> temporary exact-artifact presentation
    -> retained artifact for deep verification
    -> surrender, redemption, transfer, cancellation, or revocation of control
```

The stages are not security levels automatically assigned by the protocol.
They are choices made by the holder, issuer, verifier, and applicable policy.
Different records and decisions can stop at different stages.

| Stage | Record exposure | Typical verification |
| --- | --- | --- |
| **Evidence only** | The artifact remains private; a digest and minimal signed statement are available | Signature, event structure, recognized signer, and later lifecycle evidence |
| **Public artifact** | The artifact or an authorized representation is openly retrievable | Anyone can calculate the digest and compare it with signed evidence |
| **Presentation verification** | The exact artifact is made temporarily available for inspection without routine retention | Visual inspection, exact digest comparison, Control History, and recognition policy |
| **Deep verification** | The verifier receives and may retain the exact artifact under an appropriate authority or agreement | Native-format validation, metadata or forensic analysis, signed evidence, recognition inputs, and verifier-specific policy |
| **Surrender of control** | The holder gives up control or the record's operative status changes under the domain rulebook | Transfer, redemption, discharge, cancellation, revocation, seizure, or custodial control event |

This is an escalation model. Most routine decisions should not require the
most consequential stage.

The product-language version of the same escalation model is:

```text
Check first.
Present when the decision requires the record.
Share only when retention or deep analysis is justified.
Surrender only when control itself is meant to change.
```

Surrender is different from sharing. Sharing gives another party a copy or
access to the exact artifact. Surrender changes who controls the operative
record, or changes whether the record remains operative at all.

## Graduated Disclosure Is Not Selective Disclosure

Selective disclosure and graduated disclosure solve related but different
problems.

**Selective disclosure** normally means revealing particular attributes while
withholding others. A credential holder might prove that they are over a
threshold age without revealing a birth date. Cryptographic selective
disclosure may use derived proofs, zero-knowledge systems, or format-specific
credential mechanisms.

**Graduated disclosure** governs how far the complete verification interaction
proceeds. A verifier may first inspect public evidence, then view a temporary
artifact, and only later receive the exact record for independent analysis.

The two models can be combined:

```text
selective disclosure -> which facts are revealed
graduated disclosure -> how much access and verification the decision warrants
```

OpenETR does not require advanced selective-disclosure cryptography in its base
protocol. Digest commitments, signed events, and verifier policy already
support useful graduated disclosure. Specialized credentials and domain
adapters can add selective disclosure where appropriate.

## The OpenETR Role

OpenETR gives a digest-identified Digital Artifact the **Controlled Object**
role when it becomes the subject of a candidate event graph. It binds signed
Anchor, Control, Attestation, and linked-evidence events to that object. The
role does not itself assert valid consequential state; that state must be
derived from valid events under OpenETR rules.

The compact model is:

```text
exact artifact -> digest -> Controlled Object -> valid event graph
               -> consequential state -> recognition policy
```

This makes it possible to separate the artifact from evidence about the
artifact.

For a sensitive document, an authorized notary or issuer may publish only:

- the object digest;
- a narrowly scoped signed statement;
- the signing key or resolvable organizational profile;
- the relevant time and event relationships; and
- later revocation, replacement, attestation, or control events.

The artifact can remain in the holder's safekeeping environment. When it is
presented, a verifier calculates the digest over the exact presented bytes and
compares it with the signed event graph.

For a less-sensitive record, the artifact itself may be published beside the
evidence. A vendor permit, public licence, inspection certificate, or product
record may be intended for broad retrieval and routine verification.

OpenETR carries evidence. It does not decide whether disclosure is authorized
or whether the signer must be recognized. Those decisions remain with domain
policy and the relying party.

## Presentation Verification

Presentation verification should satisfy many ordinary interactions.

A holder displays a human-readable record and presents a QR code. The verifier
can inspect the representation, acquire the exact artifact temporarily, and
follow a durable link to its signed OpenETR evidence. The verifier checks:

1. The presented bytes calculate to the referenced object digest.
2. The event ids and signatures verify.
3. The origin and relevant control or attestation events form a coherent
   candidate graph.
4. The signer is recognized for the claimed role under the verifier's policy.
5. No relevant replacement, revocation, termination, or contradictory event
   changes the conclusion.

The verifier need not routinely import or retain the record. This reduces data
accumulation while still allowing meaningful independent verification.

In the plain-language model, this is **Present**. The holder lets the verifier
see and test the exact record for the immediate decision, but the default is
not permanent transfer or routine retention.

Visual inspection alone is not cryptographic verification. A screenshot,
photograph, rescan, crop, or recompressed file normally has different bytes and
therefore a different digest. The presentation workflow must make the exact
attested artifact available to the verifier if an exact digest comparison is
claimed.

## Deep Verification

Deep verification is the escalation path for higher-consequence decisions,
secondary inspection, disputes, and specialized analysis.

The verifier receives the exact artifact into its own authorized verification
environment and may then:

- retain an evidentiary copy where policy permits;
- calculate and preserve the complete digest independently;
- perform native-format signature and schema validation;
- inspect metadata or conduct forensic analysis;
- query OpenETR evidence from independent relays or archives;
- consult registries, organizational authority sources, or community
  recognition inputs; and
- apply and record its own verifier policy.

Receiving a copy for verification does **not** transfer control, ownership, or
legal title. OpenETR control changes require the appropriate separately
authorized and signed control events. A digital copy can reproduce evidence;
it cannot copy control merely by existing.

In the plain-language model, this is **Share**. The holder or responsible
system gives the verifier the record because the decision requires retention,
forensic review, dispute handling, audit, or another higher-consequence use.

## Surrender Of Control

Surrender is the final and most consequential stage.

In the positive case, surrender is exactly what many electronic transferable
record systems are designed to support. A party may surrender control of a
record after payment, performance, presentation, delivery, redemption, or
discharge of an obligation.

Examples include:

- a bill of lading is surrendered so goods can be released;
- a warehouse receipt is redeemed so stored goods can be delivered;
- a pledge over a receipt is discharged after the secured obligation is paid;
- a promissory note is discharged after payment;
- a transferable record is transferred to a new controller as part of a
  commercial transaction.

OpenETR fits this model well because surrender can be represented as a signed
control event, redemption event, discharge event, termination event, or
domain-specific event interpreted by a domain adapter and recognition policy.

The concerning case is different. Some situations may require a person to
surrender a record that is closely tied to personal status or mobility, such
as a passport at a border, in a detention context, or during an administrative
process. In that setting, surrender may not be a routine commercial handoff.
It may become a coercive or rights-affecting act, especially if the document
can be retained, suspended, cancelled, or revoked.

That distinction should be explicit:

```text
commercial surrender:
  control changes because the transaction calls for delivery,
  payment, discharge, redemption, or completion

coercive surrender:
  control is demanded by an authority or gatekeeper,
  possibly affecting movement, status, rights, or access
```

OpenETR can record signed evidence that surrender occurred, who requested it,
who accepted it, what authority was asserted, and what later events affected
the record. It should not treat every surrender as benign merely because it is
cryptographically well formed.

A verifier or domain policy should distinguish:

- voluntary surrender from compelled surrender;
- temporary custody from permanent transfer;
- presentation from retention;
- retention from revocation;
- commercial discharge from state or platform cancellation;
- ordinary workflow completion from a rights-affecting restriction.

This is another reason to keep control, disclosure, and recognition separate.
A valid event can prove that a key signed a surrender statement. It does not
by itself prove that the surrender was lawful, voluntary, proportionate, or
recognized for every purpose.

## Practical Examples

### Passports And Birth Certificates

A passport authority, civil registry, or recognized notary may attest only to
the digest of an exact digital artifact. The sensitive document remains
private.

For a routine check, the holder presents the document and QR-linked evidence.
The verifier compares the exact bytes with the authority's signed event and
applies its own recognition policy. If a secondary inspection is required, the
verifier receives the exact artifact and performs deeper native, registry, or
forensic checks.

A recognized origin proves that a key made a signed statement about an exact
artifact. It does not by itself prove that the presenter is the rightful
holder. Holder binding may require a photograph comparison, a component-key
challenge, a control event, or another domain-appropriate method.

Surrender changes the risk profile. A border or administrative process may
require a person to give up custody or control of a passport. That may be
lawful and temporary in some contexts, but it may also become a revocation,
seizure, or mobility restriction. A graduated disclosure model should make
that escalation visible instead of treating surrender as just a deeper form of
inspection.

### Vendor Permits

A vendor permit is often intended to be displayed publicly. The issuing
authority may publish both the permit artifact and its signed OpenETR evidence.
Customers and inspectors can retrieve the permit, verify its digest, identify
the issuer, and check for expiry, replacement, suspension, or revocation
events without requesting private disclosure from the vendor.

### Insurance Damage Evidence

An adjuster, inspector, emergency official, or authorized agent can attest to
the digest of an exact photograph of a damaged vehicle or building. Any
byte-level alteration breaks the digest match.

That integrity result has a precise meaning: the file has not changed since it
was attested. It does not independently prove when or where the scene occurred,
that the scene was genuine, or that the agent's interpretation was correct.
Those are claims carried by the signed statement, supporting evidence, and
recognition policy.

A claims officer may use temporary presentation for ordinary review. A
disputed or high-value claim may proceed to deep verification, metadata review,
forensic analysis, and authorized retention.

### Delivery And Service Evidence

A delivery worker or service provider can create a photograph and bind it to a
signed statement about a delivery or completed task. The customer receives
portable evidence rather than merely viewing an image held inside the
provider's application.

The customer can verify that the image is the exact artifact attested by a
recognized provider or worker. That does not automatically prove that the
correct parcel reached the correct address. A validly signed image of the wrong
doorstep remains valid evidence of what was photographed, not proof of correct
delivery. Context and policy still matter.

### Trade And Professional Records

The same model applies to warehouse receipts, bills of lading, inspection
reports, health records, legal instruments, and notarized PDFs. Routine
counterparties can inspect a presentation and Control History. Banks, courts,
regulators, insurers, or auditors can request the exact artifact when their
decision warrants deeper verification.

For transferable records, surrender may also be the intended end of a
transaction. A holder may surrender a bill of lading to obtain delivery of
goods, surrender a warehouse receipt to redeem stored goods, or discharge an
encumbrance after payment. In these cases, surrender is not merely disclosure.
It is a control-state transition.

## Integrity, Origin, Recognition, And Meaning

Graduated disclosure works only if the verifier keeps distinct questions
separate.

| Question | Evidence source |
| --- | --- |
| Are these the exact attested bytes? | Digest comparison |
| Which key made the statement? | Event signature |
| What did that key claim? | Signed event content and tags |
| Is that key authorized or recognized? | Registry, organizational, community, contractual, or legal policy |
| Is the record current? | Control and lifecycle evidence |
| Is the presenter the rightful holder? | Holder-binding or control evidence appropriate to the domain |
| Has control been surrendered, redeemed, discharged, revoked, or terminated? | Control graph and domain-specific lifecycle events |
| Should the verifier rely on it? | Verifier policy and surrounding facts |

A hash proves integrity relative to exact bytes. A signature proves that a key
signed a statement. Recognition connects that key to an authority or role.
Policy decides what conclusion follows. None of these layers should silently
stand in for the others.

## Privacy Limits Of Hash-Only Publication

Publishing only a digest can greatly reduce disclosure, but it does not make
the evidence anonymous.

A public digest can become a stable correlation identifier. If an artifact is
predictable or drawn from a small set of possible values, an observer may be
able to guess candidate content and compare its digest. Event metadata may
also reveal the signer, timing, role, or relationships even when content is
withheld.

Implementations and policy profiles should therefore:

- publish only the metadata needed for the verification purpose;
- avoid embedding unnecessary personal information in public events;
- distinguish public evidence from public content;
- consider salted commitments or privacy-preserving higher-layer proofs where
  dictionary attacks or correlation are realistic;
- define who receives temporary or retained artifacts; and
- define when presentation, sharing, or surrender is permitted; and
- define deletion, retention, audit, surrender, revocation, and dispute procedures outside the base
  protocol.

OpenETR's base digest remains useful because it lets any recipient of the exact
artifact verify the match without a specialized proving system. More private
commitment schemes may be added by domain adapters and verifier policies when
their operational complexity is justified.

## Safebox Web As A Practical Implementation

[Safebox Web](https://trbouma.github.io/safebox-web/) demonstrates how
graduated disclosure can become an ordinary user interaction.

An Acorn safeguards the private record and exact Original Record. Safebox Web
can render it, temporarily present it through a QR-mediated capability, show
its Control History and durable verifier link, or share the exact record when
deep verification is required. OpenETR supplies portable digest-bound evidence
without requiring Safebox Web to become the registry or recognition authority.

The implementation boundary is:

```text
Acorn       -> safeguards the key and exact record
Safebox Web -> presents, shares, and explains the verification workflow
OpenETR     -> supplies digest-bound signed evidence and Control History
Verifier    -> decides recognition and effect
```

See [Graduated Disclosure in Safebox Web](https://trbouma.github.io/safebox-web/graduated-disclosure/)
for the application-facing model.

## Policy Implications

Graduated disclosure gives institutions a practical alternative to both
centralized record custody and indiscriminate document exchange.

It can:

- reduce unnecessary collection of sensitive records;
- let holders carry portable evidence across applications;
- preserve an escalation path for disputes and high-consequence decisions;
- let communities and institutions recognize different authorities over the
  same evidence substrate;
- reduce exclusive dependence on the issuer's application or database; and
- make the reason for disclosure legible to the holder and verifier.

The objective is not disclosure avoidance at all costs. It is disciplined,
proportionate access to evidence.

## Policy Position

Institutions should avoid treating verification as a single yes-or-no demand
for the underlying record.

The better policy model is:

| Level | Plain-language question | Policy posture |
| --- | --- | --- |
| **Check** | Can the relying party verify status and evidence without taking the record? | Prefer this for routine, low-risk, or privacy-sensitive checks. |
| **Present** | Does the relying party need to inspect the exact record for the immediate decision? | Permit temporary access where the decision requires the artifact itself. |
| **Share** | Does the relying party need to retain the record for review, audit, dispute, or compliance? | Require a clear authority, purpose, retention rule, and accountability path. |
| **Surrender** | Is control itself meant to change, end, or move into another party's custody? | Treat this as a control and rights event, not merely as disclosure. |

This is especially important because surrender has two faces.

In commercial transferable-record systems, surrender can be normal and
constructive. It may complete performance, release goods, discharge a debt, or
end an encumbrance after payment.

In personal, mobility, identity, or status systems, surrender can be coercive
or rights-affecting. A demand to surrender a passport, credential, permit, or
identity document should be governed with much greater care than a request to
check or present evidence.

OpenETR's contribution is to make the transition explicit. A verifier should
be able to see whether a record was merely checked, temporarily presented,
shared for retention, or surrendered as a control-state change.

## Core Principle

```text
Evidence can be public while content remains private.
Presentation can be temporary while verification remains durable.
Deep verification can be available without becoming the default.
Surrender can be explicit when control is meant to change.
```

That is the promise of graduated disclosure: enough evidence for the decision
at hand, with a clear path to go deeper when justified and a clear warning
when the interaction crosses from disclosure into surrender of control.

## Related Material

- [Why Control Is Not Recognition](why-control-is-not-recognition.md)
- [Policy Guards And Cryptographic Evidence](policy-guards-and-cryptographic-evidence.md)
- [OpenETR And C2PA](openetr-and-c2pa.md)
- [Safebox Web: Deep Verification](https://trbouma.github.io/safebox-web/deep-verification/)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [ZK-SNARKs And Hash Commitments In OpenETR](https://github.com/trbouma/openetr/blob/main/docs/specs/ZK_SNARKS_AND_HASH_COMMITMENTS_DESIGN_NOTE.md)
