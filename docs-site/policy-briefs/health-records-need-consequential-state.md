# Health Records Need Consequential State

## Policy Proposition

**Health records need consequential state.**

A health record matters not only because it contains clinical information. It
matters because clinicians, patients, caregivers, laboratories, pharmacies,
insurers, and public-health authorities may act on it. A report may be
preliminary or final. A result may be corrected. A medication order may be
active, completed, or discontinued. A consent directive may be granted,
limited, superseded, or withdrawn.

Those distinctions can affect care. They should not depend exclusively on the
screen, database, portal, or vendor currently presenting the record.

OpenETR offers a narrow architectural contribution: identify an exact health
record artifact, preserve attributable evidence concerning its lifecycle, and
allow a verifier to derive record state under identified rules. Clinical
meaning, access authority, professional responsibility, and the effect given
to that state remain with health systems, practitioners, patients, law, and
applicable policy.

## A Health Record Is More Than Content

The [WHO Global Strategy on Digital Health](https://www.who.int/publications/i/item/9789240116870)
places digital health within the broader work of strengthening equitable,
effective, and sustainable health systems. WHO also emphasizes interoperability
and standards-based exchange as conditions for turning health data into useful
care rather than isolated application output.

The content of a clinical document is necessary, but often insufficient for
safe reliance. A receiving system may also need to know:

- which exact version is being presented;
- which practitioner, laboratory, organization, or device issued it;
- whether it was preliminary, final, corrected, superseded, or withdrawn;
- which prior record it amends;
- whether related evidence is available;
- which rules were used to interpret its lifecycle state; and
- whether the recipient is permitted to access and use it.

The last question is deliberately separate. Evidence can be cryptographically
valid while access remains unlawful or inappropriate.

## The Application-Owned Record Problem

Health information is commonly fragmented among hospitals, clinics,
laboratories, pharmacies, insurers, patient portals, personal devices, and
public-health systems. Each may maintain a useful local view. Trouble begins
when that view becomes the only place from which the status or history of a
consequential record can be known.

When a system changes vendors, an organization closes, a patient moves, or an
API is unavailable, a record may arrive without enough durable context to
distinguish:

```text
current from superseded
final from preliminary
original from altered
corrected from merely duplicated
attributable from unsupported
complete evidence from partial retrieval
```

This creates both continuity and power concerns. Exclusive technical control
over the record can give a platform or institution disproportionate control
over whether patients and authorized care providers can obtain, verify, or
challenge the evidence on which care depends.

## The OpenETR Contribution

OpenETR separates the health artifact from signed evidence about its lifecycle:

```text
clinical document or structured package
  -> Digital Artifact identified by digest
  -> signed DCR evidence concerning that artifact
  -> record-lifecycle rules
  -> Consequential State
  -> clinical, institutional, and legal recognition
  -> care or administrative effect
```

Consequential State might indicate that a record is:

- issued or attested;
- preliminary or finalized;
- amended by an identified later record;
- superseded;
- withdrawn;
- associated with a consent or access-policy reference; or
- dependent on linked laboratory, imaging, authorization, or provenance
  evidence.

These are examples for a future health-record domain profile. They are not yet
OpenETR core actions, and the base protocol should not pretend that every
clinical workflow shares one state machine.

## Relationship To FHIR

[HL7 FHIR Provenance](https://hl7.org/fhir/R5/provenance.html) records the
entities, activities, and agents involved in producing, revising, deleting, or
signing a FHIR resource. It supports assessments of authenticity, reliability,
integrity, and lifecycle context.

OpenETR should complement, not replace, FHIR:

| Concern | FHIR And Health Systems | OpenETR Contribution |
| --- | --- | --- |
| Clinical data | Represent observations, conditions, medications, encounters, and other health information. | Treat an agreed document, resource, or canonical package as a digest-identified Digital Artifact. |
| Provenance | Describe who or what created, transformed, or transmitted a resource. | Preserve independently verifiable signed evidence and cryptographic links concerning the artifact. |
| Workflow | Coordinate clinical orders, results, referrals, encounters, and care processes. | Record selected consequential lifecycle events without becoming the workflow engine. |
| Access control | Apply consent, role, purpose-of-use, and legal access rules. | Link or identify relevant evidence while leaving enforcement to protected health systems. |
| Record state | Maintain local status and versions. | Allow selected state to be reproduced from DCR evidence under an identified policy. |

The integration should define exactly which bytes or canonical package the
digest identifies. It should not assume that semantically equivalent FHIR
resources automatically have the same digest.

## Making Health-Record Consequences Portable

OpenETR does not make private clinical content public. It makes the evidence
basis for selected record state portable through authorized channels:

```text
artifact identity + signed lifecycle evidence + identified rules
  -> reproducible record state
  -> access and recognition policy
  -> permitted clinical or administrative use
```

A hospital may use its own identity, credentialing, approval, and clinical
systems. A receiving provider need not reproduce that internal machinery. It
needs the record, sufficient attributable evidence, and the recognition inputs
required for safe use.

This is a what-first inquiry:

1. What exact clinical artifact is being presented?
2. What happened concerning this version?
3. What state follows under the relevant record-lifecycle rules?
4. What professional, patient, consent, and institutional evidence is required
   before relying on it?

## Privacy And Safety Conditions

Health information demands a substantially more protective deployment model
than ordinary public records.

### No Presumption Of Public Publication

Raw health information, predictable digests, patient identifiers, and sensitive
metadata should not be published to public relays. Implementations should use
private storage, protected evidence exchange, encryption, access-controlled
relays, or appropriately designed proof mechanisms. Even a digest can disclose
information when the possible source values are guessable.

### Correction Without Erasure

Signed history should make corrections and supersession visible without
forcing a clinician to rely on obsolete content. Immutability of evidence must
not mean immutability of clinical judgment.

### Patient Access And Contestability

Patients should have practical ways to obtain records, understand material
changes, identify the responsible institution, request correction, and pursue
review or remedy. Independent verification should strengthen these rights, not
replace accessible service and human accountability.

### Clinical Meaning Remains External

A valid signature does not prove that a diagnosis is correct, a test is
clinically reliable, a treatment is appropriate, or a signer was professionally
authorized. Those conclusions require clinical standards, professional
governance, context, and judgment.

### Emergency And Delegated Access

Health systems need lawful emergency access, caregiver representation,
substitute decision-making, minors' protections, and other jurisdiction-specific
rules. A generic control graph must not silently determine those questions.

## Policy And Implementation Priorities

A health-record profile should:

1. begin with a narrow artifact such as a discharge summary, laboratory report,
   referral package, or immunization record;
2. define deterministic artifact packaging and digest rules;
3. distinguish provenance from clinical validity and record state;
4. define amendment, correction, supersession, and withdrawal explicitly;
5. integrate with FHIR rather than duplicating clinical schemas;
6. preserve privacy through protected storage and exchange by default;
7. keep access decisions and consent enforcement within accountable health
   systems;
8. expose evidence completeness, conflicts, policy version, and temporal limits
   in verifier output; and
9. test patient access, correction, downtime, migration, and cross-provider
   continuity as first-class scenarios.

## What OpenETR Does Not Do

OpenETR does not:

- diagnose, recommend treatment, or determine clinical truth;
- replace an electronic health record or health information exchange;
- define FHIR clinical resources;
- authenticate patients or credential practitioners by itself;
- grant access to protected health information;
- prove informed consent from a signature alone;
- make health data suitable for public relay publication;
- establish professional liability or legal effect; or
- guarantee that all clinically relevant evidence has been retrieved.

## Bottom Line

Health records matter because care follows from them. Their consequential
status should remain verifiable when records cross providers, systems, vendors,
and time.

> Health systems should control care and protect access. No one application
> should exclusively own the evidence needed to determine a health record's
> consequential state.

OpenETR can provide that evidence boundary while leaving clinical judgment,
privacy, authorization, and patient rights where they belong.

## Related Reading

- [Health Records domain](../health-records.md)
- [Consequential State](../openetr/consequential-state.md)
- [Graduated Disclosure](graduated-disclosure.md)
- [Human Rights Need Consequential State](human-rights-need-consequential-state.md)
- [Provenance Is Not Control](provenance-is-not-control.md)
