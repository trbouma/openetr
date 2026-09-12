# Human Rights Need Consequential State

## Executive Proposition

**Human rights need consequential state.**

The word *state* carries two meanings here. Human rights depend on States,
institutions, courts, and public authorities to recognize rights, protect their
exercise, prevent violations, and provide effective remedies. In a
computational system, *state* is the resulting condition derived after relevant
events have been evaluated according to rules.

The two meanings meet in a practical proposition:

> A right matters in practice because it changes the state of the world.

A right may establish that a person is entitled to enter, remain, vote, work,
receive a benefit, control property, obtain a remedy, or challenge an adverse
decision. It may also constrain what an institution is permitted to do. A
declaration of a right is indispensable, but practical enjoyment also depends
on institutions recognizing its consequence and systems preserving reliable
evidence of what has been decided, exercised, restricted, corrected, or
remedied.

OpenETR raises a narrower architectural question:

> Must the evidence needed to determine consequential state remain exclusively
> inside the State's application, database, registry, or service?

OpenETR's answer is no. Public authority and legal effect remain institutional
and legal questions. But the evidence from which a consequential result is
derived can be made independently verifiable and portable across systems.

## Rights, Institutions, And Consequences

The [Universal Declaration of Human Rights](https://www.un.org/en/about-us/universal-declaration-of-human-rights)
describes human rights as a common standard for all peoples and nations. It
also connects rights to recognition before the law and to effective remedies
through competent institutions. The
[International Covenant on Civil and Political Rights](https://www.ohchr.org/sites/default/files/Documents/ProfessionalInterest/ccpr.pdf)
requires States Parties to respect and ensure Covenant rights and to provide
accessible and effective remedies for violations.

These instruments make an important point for digital architecture: rights are
not exhausted by their expression as information. Their implementation
depends on consequential acts and institutional duties.

Historically, public and legal institutions have maintained records expressing
consequential conditions such as:

- this person is recognized as a citizen;
- this licence, permit, or status is active;
- this judgment or remedy has been granted;
- this restriction has been imposed, reviewed, or lifted;
- this property interest is registered or transferred;
- this benefit has been approved, suspended, or restored; and
- this public authority has made, corrected, or withdrawn a decision.

The record does not create the underlying dignity or all of the rights of the
person. It can, however, carry evidence of a decision or condition that changes
what institutions and other actors are required or permitted to do.

## Undocumented Individuals

The problem of **undocumented individuals** is commonly expressed as a lack of
birth registration, legal identity, official identification, or accessible
proof of recognized status. The
[United Nations Legal Identity Agenda](https://unstats.un.org/legal-identity-agenda/)
connects recognition as a person before the law with Sustainable Development
Goal Target 16.9: legal identity for all, including birth registration. The
[World Bank ID4D Global Dataset](https://id4d.worldbank.org/global-dataset)
estimated in 2025 that approximately 800 million people lacked official
identification, while many more lacked digitally verifiable identification.

OpenETR cannot register a birth, determine nationality, confer legal identity,
or require a State to recognize a person. Those remain legal and institutional
responsibilities. It can, however, help address a related architectural
failure: even after an authorized institution has recognized a person, status,
entitlement, or remedy, the evidence may remain dependent on one paper
document, registry entry, database, application, platform, or live service.

This creates two distinct forms of being undocumented:

```text
substantive exclusion
  no competent institution has recognized or recorded the relevant status

evidentiary dependence
  a status has been recognized, but usable proof depends on one document,
  database, application, platform, or service
```

OpenETR is principally relevant to the second problem. It can also support
programmes addressing the first by preserving independently verifiable
evidence of registration, adjudication, correction, or recognition once a
competent authority acts.

For example, a person should not become practically undocumented merely
because a certificate is lost, a portal account is closed, an agency replaces
its software, a vendor relationship ends, or a registry service is temporarily
unavailable. An exact artifact and its DCR evidence could be obtained through
authorized channels and verified without treating one physical embodiment or
live application as the sole source of the consequential answer.

This architecture must remain inclusive. It must not require the affected
person to manage cryptographic keys, operate specialized software, or publish
sensitive identity information. Public institutions and trusted
intermediaries may provide accessible presentation, recovery, representation,
and protected evidence services while preserving independent verifiability at
the protocol layer.

## The Risk Of Application-Owned Consequence

Digital public systems commonly represent consequential status as a database
field behind an application or API. This can make the operational answer
dependent on the continuing availability and cooperation of the system that
holds it.

That dependency is also a concentration of power. Whoever exclusively controls
the document, database, application, platform, or service may be able to delay
access, alter a projection, suppress relevant history, impose a new commercial
dependency, or make verification conditional on continued cooperation. Where
governance is weak, the same concentration can create opportunities for
corruption, coercion, discriminatory administration, or the quiet disappearance
of an inconvenient decision.

Separating the ability to derive Consequential State from any one presentation
surface reduces that leverage. It does not remove institutional authority or
eliminate corruption. It makes the evidentiary basis more difficult for one
technical operator to monopolize and gives affected people, oversight bodies,
courts, and other authorized verifiers a way to check what was signed and what
follows under the identified rules.

If that system becomes unavailable, changes suppliers, loses history, denies
access, or cannot exchange reliable evidence with another institution, the
person affected may be left with a screenshot, PDF, reference number, or
unsupported assertion. The right may still exist, but its practical exercise
can become harder because the evidence of the consequential decision is
trapped in one administrative context.

This is especially important when a person crosses:

- departments or levels of government;
- courts, tribunals, and administrative bodies;
- public and private service providers;
- jurisdictions;
- legacy and replacement systems; or
- periods of institutional or technological disruption.

A system that is authoritative for making a decision need not be the only
system capable of verifying that the decision was made and determining what
follows from the resulting record.

## The OpenETR Contribution

OpenETR does not define human rights, determine eligibility, replace public
authority, or compel legal recognition. It offers an evidence architecture for
consequential digital records:

```text
right, law, or policy
  -> institutional process and authorized decision
  -> signed evidence concerning an exact Digital Artifact
  -> Digital Controllable Record
  -> Consequential State derived under identified rules
  -> recognition by the competent authority or relying party
  -> practical effect, exercise, review, or remedy
```

The upstream institution remains responsible for lawful authority, fair
procedure, authentication, authorization, reasons, accessibility, and redress.
OpenETR can make the resulting evidence independently verifiable outside the
application that first recorded it.

This is the sense in which OpenETR seeks to **make consequences portable**.
It does not copy an authoritative status field or make every recipient accept
one institution's conclusion. It makes the artifact identity, signed evidence,
event relationships, and rules basis portable enough for another verifier to
reproduce the protocol result and then apply its own recognition policy.

## What-First Rather Than Identity-First

Rights-related digital architecture is often identity-first. A system begins
by resolving who a person is, accumulating attributes and relationships, and
then deciding what services or actions follow.

OpenETR begins with a more limited set of questions:

1. What record is being presented?
2. What signed evidence concerns that exact record?
3. What consequential state follows under the identified rules?
4. What identity, authority, or relationship evidence does this particular
   use require?

This approach does not make identity irrelevant. It makes identity
proportionate to the consequence being evaluated. A relying party should not
need an entire identity or delegation graph when a recognized consequential
record and proof of the rightful presenter are sufficient for the purpose.

That boundary can support privacy:

> Prove only what the consequence requires.

## The Bitcoin Bridge

The line **Bitcoin did that for money** provides a useful conceptual bridge.
The [Bitcoin white paper](https://bitcoin.org/bitcoin.pdf) described a system
in which participants could verify a transaction history and apply shared
rules without relying exclusively on a financial institution to maintain the
operative ledger.

Bitcoin demonstrated that consequential state concerning a narrow digital
object can be independently derived from cryptographic evidence and protocol
rules. Its mechanism is specific: a globally ordered proof-of-work ledger,
consensus rules, and a native monetary asset.

OpenETR generalizes the architectural insight but not the Bitcoin mechanism.
It does not use proof of work, establish global consensus, issue money, or
replace competent institutions. It preserves signed evidence concerning
digest-identified artifacts and lets identified rules derive candidate
Consequential State. Recognition and external effect remain contextual.

The card's three lines can therefore be read as a progression:

```text
Human rights need consequential state.
Bitcoin demonstrated independently derivable state for money.
OpenETR explores the pattern for other consequential digital records.
```

The phrase **OpenETR is for everything else** is intentionally expansive as
positioning. As an architectural claim, it means that the pattern may apply to
many domains beyond money. It does not mean that every human right should be
encoded as an OpenETR record or reduced to a deterministic state machine.

## Rights-Preserving Design Conditions

Applying consequential-state architecture to rights-related records creates
serious obligations. Independent verifiability is not enough. A suitable
implementation should address at least the following conditions.

### Data Minimization And Confidentiality

Sensitive personal information should not be published merely because signed
events are portable. Public evidence should normally use digests, selective
references, protected payloads, or private distribution arrangements. A
digest may still expose information when the possible source values are
predictable, so privacy analysis must consider the underlying data.

### Contestability And Effective Remedy

People need a practical way to challenge adverse evidence and decisions. An
immutable record of an assertion must not make the assertion incontestable.
Corrections, appeals, reversals, suspensions, and remedies should be expressed
as attributable subsequent evidence whose consequence is defined by policy.

### Reasons And Evidence Sufficiency

A state transition should identify the rule and evidence basis needed for
review. Cryptographic attribution proves that a key signed a statement; it
does not prove that the decision was lawful, reasonable, unbiased, or based on
sufficient evidence.

### Accessibility And Non-Exclusion

No person's practical enjoyment of a right should depend solely on possessing
a private key, operating specialized software, or maintaining network access.
Human-accessible assistance, recovery, representation, and non-digital paths
remain necessary where the right or public service requires them.

### Temporal Integrity

Rights and statuses may begin, expire, be suspended, restored, corrected, or
reviewed. Verifiers should distinguish signed timestamps from trusted time and
should disclose the evidence set, policy version, and temporal basis used to
derive a result.

### Institutional Accountability

Actor-neutral signatures do not erase public responsibility. A host system
must preserve the mapping from operational keys to accountable authorities and
must apply the governance, audit, authorization, and human-review requirements
of its domain.

### Plural Recognition And Due Process

Different institutions may have different lawful roles and recognition rules.
OpenETR should expose evidence and derivation clearly without pretending that
one technical verifier can settle every legal disagreement. Conflict must be
visible, and the applicable review or adjudication process must remain
available.

## Policy Implications

Public institutions considering independently verifiable consequential records
should:

1. identify the decisions and events that genuinely change a person's legal or
   operational position;
2. separate the authority to decide from the technical evidence that the
   decision occurred;
3. make that evidence verifiable outside the originating application without
   disclosing unnecessary personal information;
4. publish or identify the rules used to derive consequential state;
5. preserve correction, appeal, review, and remedy as first-class transitions;
6. provide accessible alternatives, representation, and recovery mechanisms;
7. keep identity evidence proportionate to the consequence being evaluated;
8. require systems to report uncertainty, conflict, incomplete evidence, and
   recognition limits; and
9. avoid making a vendor, platform, ledger, or live API the exclusive source
   from which a person's consequential status can be known; and
10. distinguish people who have not yet received legal recognition from people
    whose recognized status has become inaccessible because its evidence is
    trapped in one document or system.

## What OpenETR Must Not Claim

OpenETR must not claim that:

- cryptographic state creates or defines a human right;
- a valid signature proves lawful authority or informed consent;
- deterministic rules can replace judgment, proportionality, or due process;
- immutable evidence should prevent correction or remedy;
- public event publication is appropriate for sensitive personal records;
- every jurisdiction must recognize the same result; or
- independent verification eliminates the need for trusted institutions.

The protocol can make evidence durable and derivation reproducible. Human
rights law, democratic institutions, courts, public authorities, and affected
people determine the normative and practical effect.

## Bottom Line

Human rights require more than declarations. They require institutions capable
of changing conduct, recognizing status, constraining power, and providing
effective remedies. Increasingly, those consequences are administered through
digital systems.

The policy opportunity is not to move human rights into a protocol. It is to
ensure that evidence of consequential decisions is not exclusively owned by
the application or institution that happens to process it.

> The State remains responsible for rights. Consequential state need not remain
> trapped inside the State's database.

For undocumented individuals, this distinction is concrete. OpenETR cannot
create the recognition that the State has failed to provide. It can help ensure
that recognition already granted does not disappear merely because a document
is lost or the application that recorded it is unavailable, uncooperative, or
compromised.

That is the deeper connection to OpenETR: important digital records should be
capable of carrying independently verifiable evidence of what happened and
what follows, while recognition, accountability, review, and remedy remain
firmly grounded in human institutions.

## Related Reading

- [Maybe We Have Identity Backwards](https://trbouma.substack.com/p/maybe-we-have-identity-backwards)
- [Consequential State](../openetr/consequential-state.md)
- [Why OpenETR](why-openetr.md)
- [OpenETR And Government Modernization](openetr-and-government-modernization.md)
- [Policy Guards And Cryptographic Evidence](policy-guards-and-cryptographic-evidence.md)
- [Records-First Authenticity And Digital Originality Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/RECORDS_FIRST_AUTHENTICITY_AND_DIGITAL_ORIGINALITY_DESIGN_NOTE.md)
