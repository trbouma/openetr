# Academic Records Need Consequential State

## Policy Proposition

**Academic records need consequential state.**

A transcript, diploma, certificate, microcredential, professional-training
record, or recognition decision matters because institutions and people act on
it. It may support admission, transfer credit, employment, professional
licensing, immigration, funding, or further study.

The document's content is only part of the question. A relying party may also
need to know whether the record was issued by a recognized institution,
whether it remains current, whether it was corrected or withdrawn, what
programme or learning it represents, and what recognition decision has been
made for a particular purpose.

OpenETR can make the evidence of those consequential actions portable without
becoming the university, registrar, accreditor, qualification framework, or
recognition authority.

## Academic Mobility Is A Recognition Problem

The
[UNESCO Global Convention on the Recognition of Qualifications concerning Higher Education](https://www.unesco.org/en/higher-education/global-convention)
establishes principles for fair, transparent, and non-discriminatory recognition
of higher-education qualifications and study. It is designed to support
mobility across institutions and borders, including circumstances where
refugees and displaced persons may have insufficient documentary evidence.

That context reveals several distinct questions:

- Is this the exact record that the institution issued?
- Has it changed since issuance?
- Which institution or authorized office issued or amended it?
- Is the institution or programme recognized?
- What qualification, credit, or learning does the record represent?
- Has the record been corrected, superseded, suspended, or withdrawn?
- Is it recognized as equivalent for admission, employment, licensing, or
  another stated purpose?

Cryptography can help answer the first three and preserve evidence relevant to
the others. It cannot make the recognition decision.

## The Registrar And Platform Boundary

Academic records are frequently tied to an institution's student-information
system, credential vendor, transcript-delivery service, or online account.
Those systems provide important operational controls, but they can also become
the only route through which a learner proves what was achieved.

This dependency becomes visible when:

- an institution closes or merges;
- a credential vendor changes;
- a learner loses portal access;
- records cross borders or sectors;
- a name or record is corrected;
- a qualification must be assessed decades later;
- a refugee or displaced person cannot obtain the expected document; or
- the receiving institution does not participate in the issuing platform.

A registrar should retain authority over issuance and correction. It need not
remain the exclusive operator of the software required to verify that an
attributable record was issued and what its evidenced lifecycle now shows.

## The OpenETR Contribution

OpenETR can represent an academic document or canonical data package as a
Digital Artifact and preserve signed lifecycle evidence as its DCR:

```text
transcript, diploma, certificate, or credential package
  -> Digital Artifact identified by digest
  -> signed issuance and lifecycle evidence
  -> academic-record rules
  -> Consequential State
  -> institutional or regulatory recognition
  -> admission, credit, employment, licensing, or other effect
```

Consequential State for an academic record might indicate that it is:

- issued;
- corrected by an identified later artifact;
- superseded;
- withdrawn or revoked under stated authority;
- associated with a recognized programme or institution attestation;
- accompanied by a qualification-recognition decision; or
- dependent on linked accreditation, identity, or assessment evidence.

These are candidate concepts for an academic-record domain profile. Academic
records are generally claim-centric and lifecycle-oriented, not transferable.
OpenETR should not impose warehouse-receipt concepts such as exclusive control
or transfer where they do not belong.

## Credentials And DCR Evidence

An academic credential and an OpenETR DCR answer related but different
questions.

```text
credential:
  What does this issuer claim about this learner or achievement?

DCR:
  What attributable records concern this exact artifact, and what lifecycle
  state follows under the identified rules?
```

A W3C Verifiable Credential, digitally signed PDF, structured transcript, or
other credential package may itself be the Digital Artifact. It may also be
linked evidence supporting another artifact. OpenETR need not replace the
credential format. It can preserve artifact identity, lifecycle links, and
evidence needed to determine whether the presented version remains current.

Recognition remains layered:

| Layer | Question |
| --- | --- |
| Artifact integrity | Are these the exact issued bytes or canonical data? |
| Signature attribution | Which key signed the relevant record? |
| Lifecycle state | Was it issued, corrected, superseded, or withdrawn? |
| Issuer recognition | Does the key represent an institution authorized to make the claim? |
| Qualification recognition | What academic or professional value does the record receive for this purpose? |
| External effect | Does it support admission, credit, licensing, employment, or another decision? |

## Making Academic Consequences Portable

An institution may use extensive internal processes to enrol a learner,
evaluate work, approve grades, confer an award, and authorize the registrar to
issue a record. A receiving institution normally does not need to reproduce
that entire bureaucracy.

It needs sufficient evidence to evaluate the resulting record:

```text
artifact identity + attributable lifecycle evidence + identified rules
  -> reproducible record state
  -> issuer and qualification recognition
  -> purpose-specific effect
```

This is the same what-first inversion used elsewhere in OpenETR. Begin with the
record being presented. Add identity, accreditation, programme, and authority
evidence only to the extent required for the recognition decision.

> Do not make every registrar and credential platform interoperable. Make the
> consequential academic record independently verifiable.

## Learners With Missing Documentation

Independent verification can reduce future documentary dependence, but it
cannot solve every case of missing records.

If an institution never issued or preserved a record, OpenETR cannot recreate
the learning or prove an award. Recognition procedures may need alternative
evidence, interviews, assessments, affidavits, partial records, or other means,
particularly for refugees and displaced persons.

Where evidence does exist, OpenETR can help prevent a person from becoming
practically undocumented because one paper diploma was lost or one transcript
service became inaccessible. Authorized issuers, archives, recognition bodies,
or the learner could retain an evidence package verifiable independently of
the original application.

## Privacy, Fairness, And Remedy

Academic records contain personal information and can shape life
opportunities. A suitable implementation should therefore provide:

### Data Minimization

Grades, student identifiers, disciplinary information, disability information,
and other sensitive data should not be placed on public relays. Use protected
content, private exchange, selective disclosure, or appropriately scoped
evidence packages.

### Correction And Appeal

Learners need accessible procedures to correct errors and challenge adverse
decisions. Signed history should preserve accountability while allowing later
evidence to correct, supersede, or reverse a prior state.

### Purpose-Specific Recognition

A qualification may be recognized differently for admission, transfer credit,
employment, immigration, or professional licensing. OpenETR should report the
evidence and state without collapsing those distinct decisions into universal
validity.

### Institutional Accountability

A valid signature does not prove that grading was fair, the programme was
accredited, the signer had authority, or a withdrawal was lawful. Institutions
and recognition bodies remain accountable for those determinations.

### Accessible Presentation

Learners should not need to manage raw cryptographic keys or specialized
software. Institutions, wallets, archives, and public services can provide
usable presentation and recovery while preserving independent verification.

## Policy And Implementation Priorities

An academic-record profile should:

1. select a narrow first artifact, such as a diploma, transcript, or
   microcredential package;
2. define deterministic artifact packaging and digest rules;
3. distinguish issuer signature, institutional recognition, accreditation, and
   qualification effect;
4. model correction, supersession, withdrawal, and reinstatement explicitly;
5. support existing credential and transcript formats instead of replacing
   them;
6. protect personal data through private exchange and graduated disclosure;
7. allow evidence to be retained by institutions, public archives, recognition
   bodies, and learners without making one vendor indispensable;
8. expose conflicts, incomplete evidence, policy versions, and recognition
   limits; and
9. test cross-border, institution-closure, long-term verification, and missing-
   documentation scenarios.

## What OpenETR Does Not Do

OpenETR does not:

- decide whether learning occurred or academic standards were met;
- replace registrars, institutions, accreditors, or qualification authorities;
- determine equivalency, transfer credit, admission, or professional licensing;
- establish that an issuing key represents a recognized institution by itself;
- require academic records to be transferable or exclusively controlled;
- make personal academic information suitable for public publication;
- resolve fraud, institutional closure, or missing evidence automatically; or
- compel another institution or jurisdiction to recognize a qualification.

## Bottom Line

Academic mobility depends on records that can outlive the application and
platform that issued them while remaining attributable, correctable, and
recognizable in context.

> Institutions confer qualifications. Recognition bodies determine their
> effect. No one platform should exclusively own the evidence needed to verify
> the academic record between them.

OpenETR can make that evidence portable without trying to make the world's
education systems identical.

## Related Reading

- [Consequential State](../openetr/consequential-state.md)
- [The Controllable Records Taxonomy](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROLLABLE_RECORDS_TAXONOMY.md)
- [EUDI Wallet And OpenETR](eudi-wallet-and-openetr.md)
- [Graduated Disclosure](graduated-disclosure.md)
- [Human Rights Need Consequential State](human-rights-need-consequential-state.md)
- [Apostille Documents](../apostille-documents.md)
