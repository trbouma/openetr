# From Cashu Proofs To OpenETR

## Policy Proposition

Digital continuity requires more than keeping an application running. People
need to retain usable records when software changes, recover them when services
fail, and evaluate their significance without depending exclusively on the
system that first presented them.

The development path from lnfastapi through Safebox and the Mainstay family to
OpenETR illustrates how those requirements can emerge from practical work. A
wallet-storage insight became a private-record architecture, then a way to
preserve files, and ultimately a framework for deriving consequential state
from independently verifiable evidence.

**The application can help people use their records without being the permanent
home of their data or the exclusive authority for what those records mean.**

This brief is a project retrospective and an account of the policy lessons
drawn from it. It is not a claim that the underlying protocols were invented
by these projects, or that cryptography eliminates operational and institutional
responsibilities.

## The Starting Point: A Payment Application

The local Git history of lnfastapi begins on June 26, 2022. The safebox-2
repository begins on July 23, 2024. These are repository milestones, not claims
about the first conception or public release of every capability that followed.

The work began with a concrete problem space: making payments and wallet
functions usable. It did not begin with a complete theory of portable digital
evidence. That distinction matters. The broader architecture emerged through
building, using, breaking, and improving working systems.

## September 2024: Proofs Could Be Events

In the project creator's recollection, the decisive insight came in September
2024: Cashu proofs could be stored as Nostr events on relays. The immediate
follow-up question was, “why not records too?”

The insight was about separating the wallet's application interface from the
place where its private data was preserved. Sensitive proof material could be
protected in encrypted event content, while relay infrastructure supplied a
means of publishing and retrieving that content.

Storing a proof does not establish that it remains spendable. Mint checks,
recovery procedures, and coordination between writers still matter. Relay
storage is not a substitute for payment finalization or a mechanism that
independently prevents double spending.

Nevertheless, the architectural opening was substantial: if this approach could
preserve sensitive wallet material, it could also preserve private notes,
documents, credentials, and other user records. The wallet could become a
general-purpose private record environment without making every record a
financial instrument.

## From Records To Files Through Blossom

The next expansion was from event-carried records to larger files through
Blossom. Events could retain record metadata and references; content-addressed
storage could hold the associated bytes. Private attachments could be encrypted,
with the information needed to access them protected inside private records.

This separated several responsibilities that applications often combine:

| Responsibility | Architectural role |
| --- | --- |
| Attribute an event | A signature that can be checked against its signing key |
| Protect private content | Encryption and controlled access to decryption material |
| Identify exact file bytes | A cryptographic digest |
| Preserve and retrieve material | Relay and file-storage services, with appropriate replication and access arrangements |
| Present useful workflows | Applications that interpret and display the records |

A digest permits a downloaded file to be checked independently of the server
that supplied it. It does not guarantee that a copy is available. Encryption
protects content, but does not make key loss harmless or erase all metadata
exposure. These boundaries became practical design requirements rather than
reasons to abandon portability.

## A Family Of Components, Not One Indispensable Application

As the work developed, responsibilities became more explicit across the
Mainstay family. The [Mainstay product vision](https://github.com/trbouma/safebox-acorn/blob/main/docs/MAINSTAY-PRODUCT-VISION.md)
describes a local-first entry point coordinating independently useful components:
Safebox for user workflows, Acorn for portable keys, funds, records, signing,
and recovery, Spurline for event continuity, Grove for blob storage, and Clear
for bounded local currencies and vouchers. Stroma supplies a narrower runtime
boundary for Nostr operations and, more recently, pooled Blossom retrieval.

The ambition is continuity across connected and disrupted conditions. It should
not be read as a promise that every payment can finalize offline, that all
components have identical maturity, or that infrastructure ceases to matter.
Confirmed funds and pending value must remain distinguishable; local access and
external settlement are different capabilities.

The separate safebox-acorn repository begins on July 27, 2026. OpenETR's
repository begins earlier that year, on April 25. The projects therefore
developed in parallel and informed one another. The conceptual sequence in this
retrospective is not a claim that each repository was created only after the
previous project was complete.

## OpenETR: From Preserving Records To Deriving Consequences

The storage architecture answered an increasingly general question: how can
people preserve and recover private material without tying its lifetime to one
application?

OpenETR addresses a further question: what can another party establish from
the evidence, and what state follows under defined rules?

Its [axioms](../openetr/axioms.md) make the distinctions explicit:

- A digest identifies a **Digital Artifact** independently of its location.
- A signature attributes a statement to a signing key; it does not alone
  establish that key's institutional authority.
- An anchor begins a candidate **Digital Controllable Record**, not an
  automatically recognized or universally unique original.
- Linked evidence, validated and evaluated under defined rules, supports
  derived **Consequential State**.
- Recognition and effect remain questions for the relevant relying party,
  institution, agreement, or law.

This was more than adding a verification badge to a stored file. It made the
basis for a conclusion explicit and potentially reproducible by another
implementation. The application could show its evidence and rules rather than
ask a user to accept its displayed status as the sole source of truth.

The distinction between wallet records and OpenETR evidence is important.
Mutable private application state can be maintained through replaceable relay
events. OpenETR's consequential history is derived from linked signed evidence;
it is not simply the latest private database snapshot given a new name. Nor does
every private Safebox record automatically become an OpenETR DCR.

The resulting policy proposition is described in [Why OpenETR](why-openetr.md):
make consequences portable while keeping verification separate from recognition.
Shared evidence need not force every participant to adopt the same recognition
policy, but reproducible protocol conclusions require compatible rules and
sufficient evidence.

## A Barcode Makes The Principle Concrete

The GS1 Digital Link work provides a visible expression of this evolution.
An ordinary camera can open a website from a barcode. An independent reader can
instead extract identifiers and a supplied digest, seek supporting evidence
through its own configured sources, and evaluate the result without treating
the printed website as authoritative.

The URL is then an acquisition input, not an instruction to trust its host.
A digest checks correspondence with exact bytes; a signed anchor can associate
those bytes with product identifiers. Recognition of the issuer, the truth of
the product claim, and the association with the physical item remain separate
questions. A substituted barcode is not made trustworthy merely because its
references and signatures are internally consistent.

See [GS1 Digital Link And Verifiable Product Information](gs1-digital-link-and-verifiable-product-information.md)
for the detailed model and its limits. The important continuity with the
original wallet insight is the reduction of dependence on one application or
hosting location—not the elimination of all trust.

## Migration As A Practical Test Of Continuity

A recent record migration supplied a small but meaningful test. In the
creator's reported run, 38 eligible private records were accounted for: ten
were already present at the destination and 28 were subsequently copied and
verified. Earlier attempts exposed missing source locations and unavailable
file endpoints; supplying current and older Blossom sources enabled recovery.

The operation decrypted and checked attachments, encrypted them with fresh keys
for the destination, and verified readback. It left source records unchanged
and excluded funds and operational payment state. That demonstrated a bounded
form of continuity across software generations and private-key migration—not
a complete backup guarantee or proof that every historical record was found.

The later BlossomPool integration improves acquisition by querying candidate
servers concurrently and accepting a digest-verified response. It does not
solve competing wallet writers, repair uncertain payment state, or change the
meaning of the recovered records.

This experience also qualifies the portability claim: formats, legacy lookup
conventions, available copies, and migration tools all matter. Portability is
something to exercise and verify, not merely declare in an architecture diagram.

## Policy Lessons

### Treat Exit And Recovery As Normal Capabilities

Procurement and deployment decisions should ask whether users can recover their
material and move it to another implementation or identity. An export button
is insufficient if the result lacks attachments, usable decryption material,
provenance, or a documented interpretation.

### Separate Integrity From Availability And Recognition

Digest checks, signature validation, replication, and institutional recognition
answer different questions. A resilient design states which question each
component answers and reports uncertainty where the evidence is incomplete.

### Preserve Evidence Alongside Conclusions

A displayed status is useful, but it should not be the only surviving record
of how a consequential decision was reached. Retaining relevant signed evidence,
ruleset versions, and evaluation context makes later review and independent
verification possible, subject to access and preservation requirements.

### Make Local Continuity Honest

Local infrastructure can preserve access and pending work during disruption.
It must not represent unavailable external confirmation as completed settlement.
The same discipline applies to evidence: failure to retrieve a notice does not
prove that no such notice exists anywhere.

### Keep Cryptographic Capability Distinct From Authority

Possessing a private key enables cryptographic operations. It does not, on its
own, establish a person's identity, an organization's mandate, or the legal
effect of an action. This boundary becomes more important as software agents
participate in payment and record workflows.

## The Continuing Research Direction

The proposed “Synthetic Minds” and “Simple Mind” work extends the same question
to agents: could goals, context, and durable state persist outside a particular
LLM or execution host, with models serving as replaceable reasoning services?
That is a research direction, not a demonstrated consequence of using relays,
and it does not establish consciousness, secure delegation, or trace-free host
execution.

OpenETR offers a complementary question for such experiments: which actions
create consequential evidence, under what authority, and how can another
participant verify what follows? The [agent authority brief](verifiable-agent-authority-and-openetr.md)
explores that boundary.

## Retrospective Conclusion

The defining September 2024 question was modest: if Cashu proofs can be stored
as events, why not records too? Blossom extended the answer to files. The
Mainstay family gave the responsibilities distinct components and a continuity
vision. OpenETR brought the reasoning into a framework for evidence, rules,
consequential state, and recognition.

The enduring idea is not that every system should become a wallet, nor that
every record should become a transferable instrument. It is that people should
not have to lose their data, its evidentiary value, or the ability to evaluate
it independently when an application or service changes.

## Basis And Scope Of This Retrospective

This account was prepared on October 11, 2026 from the project creator's
recollections and reported migration results, local repository history, and
the project documentation linked above. September 2024 is a recalled insight,
not a date independently established by a particular commit. Repository start
dates refer to root commits in the inspected histories. The migration is a
reported operational example, not an independent audit.

The brief interprets one development lineage. It makes no claim of priority
over Cashu, Nostr, Blossom, or other work on cryptographic records, and makes
no independent legal-compliance claim.
