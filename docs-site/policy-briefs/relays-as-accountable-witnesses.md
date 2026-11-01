# Relays as Accountable Witnesses

*Policy brief | 31 October 2026*

## Policy proposition

A relay can be extended from a carrier of evidence into a producer of evidence.
Instead of merely returning a signed record, it can issue its own signed
statement that it observed and verified that particular signed record at a
stated time.

For OpenETR, this would allow an Anchor Record to be accompanied by Witness
Records from one or more relays. The testimony could be copied, archived,
discovered, and independently verified without requiring the original witness
to serve every subsequent inquiry.

The proposition is not that relays should decide what a record means. It is
that they can make their observations attributable and portable, while the
applicable ruleset and relying party's recognition policy determine what
follows from those observations.

## From availability to testimony

An ordinary relay answers a retrieval question: can it return this event now?
A witnessing relay makes an additional assertion: it observed this exact signed
event at a particular time and successfully checked its identifier and
signature. That assertion is itself signed evidence.

This matters because the author's own timestamp does not provide independent
evidence of when its signed assertion existed. A recognized witness can provide
an additional time claim without requiring every participant to adopt a common
application or entrust the relay with the underlying transaction's meaning.

For example, a publisher anchors a product document and later issues a caution
notice. Witness Records can provide attributable observations of each signed
event. They do not establish that the product is safe, that the publisher had
authority, or that every possible notice has been found.

## Separate responsibilities

| Participant | Responsibility |
| --- | --- |
| Author | Makes and signs the underlying assertion |
| Witness relay | Attests to observing and verifying that signed assertion |
| Commissioning authority | Authorizes the service key to witness under a stated policy |
| Relying party | Decides which authorities and time assertions it recognizes |

The commissioning relationship supplies a basis for accountability. It does not
make every commissioned relay universally trusted. Authorization to operate a
relay and authorization to provide observation timestamps are separate roles.

A relying party may recognize an operator for witness commissioning while
declining a particular clock policy or deployment. It can also distinguish
cryptographic validity from trust: a receipt may be correctly signed yet provide
no accepted time conclusion under that party's policy.

## Portable testimony without a central adjudicator

Because the observation is a signed record, a different relay or archive can
carry it without becoming its author. An evidence package can preserve the
original event, its Witness Records, the commissioning and authorization chain,
and the applicable policy.

This separates the source of testimony from its distribution. A verifier with
sufficient supporting evidence can check the witness's signed claim without
contacting that witness. Current knowledge about compromise or revocation may
still require additional evidence; portability is not a guarantee of completeness.

Several relays can witness the same event. Their observations may strengthen
confidence when the witnesses are recognized and meaningfully independent.
Several hosting copies of one receipt, however, are not several witnesses.
Even separate keys may share one operator or clock source.

This is a model of attributable observations, not an automatic consensus
mechanism. Witness counts must not decide ownership, validate an assertion's
contents, or choose among conflicting OpenETR transitions.

## Security and time boundaries

A Witness Record must bind the actual subject signature as well as the event
identifier. Otherwise, an earlier commitment to unsigned contents could be
misrepresented as proof that a signature produced later already existed.

Even a properly bound receipt relies on the witness's clock, operating practices,
and signing-key protection. A compromised witness key could produce backdated
assertions. Explicit authorization, disclosed clock uncertainty, incident
procedures, and independent supporting evidence are therefore central to the
trust model, not optional implementation details.

The intended time conclusion is bounded: under an accepted witness policy, the
signed event existed no later than the upper end of its attested observation
interval. That is not its exact creation time or proof of first publication.

Witnessing also creates privacy obligations for deployment design. Public
references can reveal relationships even when event content is not repeated.
Operators should disclose the policy, limit eligible records, and specify
retention and removal boundaries rather than silently witness all relay traffic.

## Learning from NIP-03

[NIP-03](https://github.com/nostr-protocol/nips/blob/master/03.md), the
OpenTimestamps event-attestation proposal, is currently marked **unrecommended**
with a vulnerability warning, not formally labeled deprecated (checked
31 October 2026). Its proof targets an event ID.

The important design lesson is that committing to contents and establishing
the existence of a signature are different claims. Nostr event IDs exclude the
signature. In this design's threat analysis, an attacker could precommit unsigned
contents and sign them after a later key compromise; the earlier commitment
would not prove that the signature existed then.

Our convention binds the exact verified signature as well as the ID. That closes
this binding gap, but does not eliminate trust in the witness. A dishonest or
compromised witness can still claim a false observation time. Relay receipts
are not OpenTimestamps proofs and are not presented as an approved replacement
for NIP-03. The [design note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_RELAY_WITNESS_RECORDS_DESIGN_NOTE.md#nip-03-status-and-the-signature-existence-distinction)
separates these security and standards boundaries in detail.

## Relationship to OpenETR

[Core Record Ruleset 1.0](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CORE_RECORD_RULESET_1_0.md)
expressly leaves external time evidence outside its scope. Witness Records
should initially be an optional supplementary assessment alongside the existing
anchor and notice evaluation, not a silent amendment to that ruleset.

Applications could display an Anchor Record and a list of associated Witness
Records, showing who witnessed it, who commissioned the witness, the claimed
observation time and uncertainty, and the relying party's trust decision. No
receipt found should mean only that no receipt was found in the queried sources.

This complements [evidence retention](preserving-openetr-evidence.md). Retention
helps keep assertions available; witnessing adds attributable observations about
their signed existence. Neither alone establishes truth, legal effect, or global
historical completeness.

## An extension by convention, not yet a standard

This is an optional extension to both relay capabilities and OpenETR applications.
It uses existing Nostr signed events and ordinary queries: no new transport,
subscription mechanism or event envelope is required. The relay becomes an
additional author of evidence, and participating applications understand its
receipt schema. Other clients need not interpret it. Ordinary relay admission
and retention limits still apply.

The new semantics are currently an experimental interoperability convention,
not an approved NIP or normative OpenETR requirement. In particular, kind 1418
is not a reserved allocation. The convention does not amend NIP-09 or make
append-only retention a prerequisite, and it does not change Core Record Ruleset
1.0. Protocol compatibility should not be confused with universal support.

The convention could inform future standards on both sides: a relay-facing NIP
for observation receipts and an optional OpenETR specification for their
discovery and assessment. That path requires independent implementations,
security and privacy review, shared test vectors, agreement on allocation and
versioning, and an explicit migration policy. Any future ruleset that gives
witness evidence consequential effect must separately define that dependency.
Deployment is evidence that an approach can work, not evidence of standards
approval or universal trust.

## Implementation path

Spurline's local implementation supports commissioning, witness authorization,
signed renewal and revocation, and local suspension. Its frozen experimental
receipt profile uses kind 1418, with wire-validation code and a cryptographic
fixture; this is not a registered allocation. Automatic issuance is now implemented
in Spurline. Oakgate discovers and displays receipts after checking signatures
and binding to the exact signed anchor or notice, separately from the core
ruleset result. Full application witness-trust evaluation remains outstanding.

The deployed version-3 profile uses the relay's system clock with explicitly
unspecified accuracy. This supplies an independent, attributable observation
claim, not a bounded-accuracy timestamp guarantee. A receipt's valid signature
does not itself establish commissioning, current authorization or truthful time.

The next steps are to test the experimental receipt profile across applications,
exercise durable observation and publication, assess compromise handling, and add
witness-policy assessment to applications. Tests should
cover multiple witnesses, duplicate copies, signature substitution, missing
authorization, clock failures, and partial evidence retrieval.

The architectural opportunity is clear: **relays can carry both assertions and
portable testimony about those assertions, without becoming the authority over
their meaning.**

## Supporting design

The [Witness Record Specification (draft 0.1)](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_WITNESS_RECORD_SPEC.md)
proposes interoperable requirements based on the experimental convention.
Kind 1418 remains provisional; publication does not imply standards adoption
or certification of current implementations.

The [Relay Witness Records design note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_RELAY_WITNESS_RECORDS_DESIGN_NOTE.md)
describes discovery, verification, trust boundaries, and integration milestones.
Spurline's [operator runbook](https://github.com/trbouma/spurline/blob/main/docs/witness-operator-runbook.md)
and [application guide](https://github.com/trbouma/spurline/blob/main/docs/openetr-witness-records.md)
provide the companion operational and record-format details.
