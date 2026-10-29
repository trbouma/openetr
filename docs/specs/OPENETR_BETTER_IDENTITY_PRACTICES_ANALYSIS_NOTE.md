# Better Identity Practices And OpenETR Analysis

## Status And Source

Policy and architecture analysis, 29 October 2026. Proposed integration patterns below are not new protocol requirements or claims of implemented compliance controls.

This note reviews the Better Identity Coalition's *Verifiable Digital Credentials - Best Practices for Organizations Requesting and Using Identity Data*, version 1.0, October 2026. Page references are to the 14-page PDF supplied for review. The [publisher's initiative page](https://www.betteridentity.org/key-initiatives/best-practices) provides the [published report](https://cdn.prod.website-files.com/669e6b8b6e7143c969f9e491/6ae125c6de7cdc2be4c368ce_vdc-best-practices-v1-0-october-2026.pdf).

The report concerns government-issued verifiable digital credentials (VDCs), including mobile driver's licences. Its terminology should not be read as specifying only the W3C Verifiable Credentials format. It proposes voluntary practices, not a certification scheme, and expressly leaves implementation infrastructure and enforcement arrangements open (pp. 3-6). This analysis is not a statement of Coalition endorsement or legal compliance.

## 1. Overall Assessment

The guidance is compatible with OpenETR's records-first model, provided an integration does not turn portable evidence into a permanent identity-observation system.

The report asks when organizations should request identity information, how much they should request, and what they should do with it. OpenETR addresses a different question: which artifact is involved, what signed evidence concerns it, what state follows under identified rules, and whether that state is recognized for a purpose.

These concerns can be composed without making real-world identity a prerequisite for every record operation. A verifier may need to establish the standing of a document's issuer without identifying the person reading the document. A service may need a narrow eligibility assertion without collecting the underlying identity credential.

The core architectural opportunity is **portable, attributable evidence without mandatory universal identification**. The limitation is equally important: cryptography can support accountable decisions but cannot make an excessive request proportionate, prevent every misuse after disclosure, or establish that consent was freely given.

## 2. The Report's Policy Structure

The introduction warns that easier identity verification could normalize identification for activities that previously allowed anonymity or pseudonymity (p. 2). The principles distinguish justified requests from requests made merely because identity technology is available (pp. 7-8).

The use-case tables separate legal or regulatory purposes, business or risk-based purposes, and restricted purposes (pp. 8-14). They include financial services, health, government, employment, age restrictions, vehicle rental, hospitality, education, visitor access, ticketing, and recovery. These are contextual guidance, not universal attribute requirements for every jurisdiction or every transaction in those sectors.

The appendix adds operational expectations concerning minimization, transparent purpose and retention, restricted reuse and sharing, tracking, correction and deletion, alternatives, and separation of government credentials from authentication (p. 14).

An OpenETR integration should not convert the tables into unconditional collection allowlists. Inclusion of a field in a bundle does not establish its necessity for every case. The adopting organization must justify its actual request, apply the relevant jurisdictional context, and provide review and redress.

## 3. Mapping The Four OpenETR Concepts

| Concept | Mechanism | Policy and recognition boundary |
| --- | --- | --- |
| Digital Artifact | Identify exact bytes with a cryptographic digest, independent of filename or retrieval location. | Decide which artifact is relevant, whether it should be retained, and whether even its digest may be disclosed. |
| Evidence Graph | Validate attributable events and their links concerning the artifact. | Determine who may make relevant assertions, which sources are acceptable, and whether collection of this evidence is proportionate. |
| Consequential State | Evaluate validated evidence using identified rules; expose uncertainty and conflicts. | Define domain meanings, temporal requirements, acceptable evidence, and institutional decision criteria. |
| Digital Original | An artifact with Consequential State established through its Evidence Graph. | Decide whether that Digital Original is authoritative and acceptable for this transaction. |

These distinctions follow the [OpenETR axioms and canonical definitions](../../docs-site/openetr/axioms.md) and [Core Record Ruleset](OPENETR_CORE_RECORD_RULESET_1_0.md).

An anchor does not make a scanned identity document a government-issued credential. A digest establishes byte identity, not factual accuracy or authority. More than one anchor can concern the same artifact. A Digital Original under a rulebook is not automatically an accepted legal original, proof of a person's identity, or evidence of a right to receive a service.

Recognition concerns the artifact, supporting evidence, derived state, purpose, and applicable context together. Identical bytes do not force all institutions to accept the same conclusion.

## 4. Mapping The Six Principles

The following mapping paraphrases the report's principles (pp. 7-8). The OpenETR contributions and safeguards are this note's recommendations.

| Guidance | OpenETR contribution | Required safeguard or external decision |
| --- | --- | --- |
| Preserve anonymous and pseudonymous participation. | Key-based attribution need not establish a civil identity; public document verification need not identify its reader. | Avoid mandatory identity checks for discovery or verification. Reused keys and metadata can still correlate activity. |
| Minimize disclosure and avoid tracking. | Separate the subject artifact from the evidence needed for a specific conclusion. | Use appropriate credential disclosure technology and private exchange. A digest is neither a selective-disclosure proof nor automatic anonymization. |
| Permit relevant requests for justified legal or regulatory purposes. | Bind a decision to identified evidence and a versioned policy basis. | Establish the actual applicable obligation and request only necessary attributes. The protocol does not determine law. |
| Enable justified remote services formerly requiring identity evidence. | Preserve evidence of a transaction-specific eligibility or authority determination. | Assess proportionality, scope, usability, and whether a less intrusive route is available. |
| Keep permissions specific to the use case and avoid pressured disclosure. | A proposed integration can record the request scope and the response associated with it. | Enforce scope in the service; a signed response is not proof of meaningful choice or blanket consent. |
| Restrict unjustified collection, including advertising and tracking purposes. | Portable evidence can help audit a recorded request and decision. | Reject inappropriate requests before disclosure. An event graph cannot prevent an undisclosed secondary use. |

## 5. Mapping The Operational Practices

The appendix (p. 14) is especially important because organizational conduct cannot be reduced to signature verification.

| Practice | Proposed integration response | What OpenETR alone cannot guarantee |
| --- | --- | --- |
| Collect minimally. | Evaluate a narrow assertion where sufficient, rather than retain the source credential. | That all systems refrain from collecting extra information. |
| Explain purpose, use, and retention. | Present a clear request and retain a protected, versioned record of the stated terms where necessary. | Comprehension, accessibility, or honest purpose declarations. |
| Limit use to the transaction. | Bind decisions to a transaction context and enforce application authorization. | Prevention of reuse once readable information has been disclosed. |
| Restrict sharing or sale. | Minimize distribution and control recipients and storage. | Compliance by recipients or operators merely because an event is signed. |
| Avoid tracking. | Avoid public per-person lookup keys; consider local verification and broader retrieval. | Unlinkability of repeated digests, keys, timestamps, or network requests. |
| Support correction and deletion. | Add correction evidence where appropriate and operate retention and deletion controls for confidential data. | Erasure of public events or copies outside the operator's control. |
| Offer alternatives. | Permit an assisted process to produce equivalent evidence where policy allows. | Service accessibility, staffing, fair outcomes, or availability of an offline route. |
| Keep credentials separate from authentication. | Authenticate the account using a suitable host mechanism; separately authorize a profile to sign a consequential statement. | Secure authentication or key custody simply by introducing an OpenETR profile. |

## 6. Three Distinct Control Points

**Before disclosure: request policy.** The wallet or service decides whether the requester may ask for the specified attributes, for this purpose, in this context. It can deny or narrow the request. This is an enforcement point, not merely a later warning in a record verifier.

**During evidence evaluation: the record rulebook.** The verifier checks artifact identity, event integrity, links, and the applicability of evidence. It derives only the state the available evidence supports. Domain semantics belong here or in incorporated domain specifications, not in an assumed universal identity vocabulary.

**At reliance: recognition and effect.** The relying organization decides whether the issuer, actor, evidence, and derived state are accepted for the proposed action. Its decision may require human review or appeal.

A system may package these policies together, but should distinguish them in its results. A technically valid event can describe a request that policy forbids. A privacy-compliant request can still receive invalid evidence. Neither condition should be hidden by a single unexplained verification badge.

## 7. Authentication, Signing, And Actor Recognition

The report advises using authentication technologies such as passkeys rather than government credential key material for routine authentication (p. 14). An OpenETR integration can preserve that separation:

```text
host account authentication
  -> authorization for a particular operation
  -> appropriate identity or attribute evidence, only if necessary
  -> profile signs the consequential statement
  -> record evaluation and contextual recognition
```

The Control Desk Key can remain behind the host application's account boundary. Its profile keys attribute signed statements, but their management does not by itself establish legal delegation. Key custody, operation approval, recovery, and the binding between a recognized actor and a signing key require explicit design.

OpenETR remains actor-neutral. A person, organization, or service may be associated with a signing key under a domain policy. This does not imply that an automated agent can supply a person's consent or exercise a human entitlement without authority.

Separate profiles may reduce some correlation, but public links between profiles, shared artifacts, or metadata can defeat that separation. Neither a root-and-profile hierarchy nor a new key automatically provides anonymity.

## 8. Privacy And Persistence Tensions

### Digests Can Be Correlation Handles

A stable digest lets parties recognize the same bytes. That is valuable for artifact verification and potentially harmful for identity privacy. If the artifact is known or guessable, an observer can test a candidate against the digest. Public tags, URLs, and repeated signer keys can disclose more than the underlying encrypted report.

Do not publish an individual's credential, its stable digest, or presentation history merely to demonstrate that an identity check took place. Determine whether a separate minimized decision artifact is sufficient. That artifact has its own digest; it is not interchangeable with the source credential and does not independently prove the underlying attributes.

### Corrections Are Not Deletion

Additive notices can qualify a publisher's position without rewriting signed evidence. They cannot remove personal information already copied to independent relays. Encrypting a record and destroying a local key also cannot recall keys or plaintext already disclosed.

An implementation should decide what must remain confidential before publication, limit recipients, document retention, and handle deletion in systems it controls. It should state where immutable audit evidence and deletion expectations cannot both be met by the proposed storage design. OpenETR does not require personal data to be placed on public infrastructure.

### Auditing Can Create A New Surveillance Dataset

A log of every identity presentation may be more sensitive than any single presentation. Record only the evidence needed to explain a decision, with scoped access and retention. A signed event proves an attributable statement, not that every disclosure or subsequent use was logged.

Issuer-independent retrieval reduces dependence on issuer-operated endpoints but does not hide queries from relay operators. Cache and network design, organizational separation, and appropriate access controls remain necessary.

## 9. Illustrative Generalized Workflow

Consider an institution deciding whether to accept a professional report. It needs confidence in the report and the professional's standing; it does not automatically need the reader's government identity.

1. **Define the decision.** Identify the report, acceptance purpose, required standing, and policy version. Establish which participants, if any, must disclose personal attributes.
2. **Check necessity before requesting data.** Obtain a narrowly scoped professional qualification assertion if needed, rather than defaulting to a full identity document. Offer an appropriate alternative process.
3. **Identify the artifact.** Hash the exact report bytes. Retrieve the candidate anchor and associated evidence from permitted sources.
4. **Validate attribution and context.** Verify signatures and links; establish the recognized relationship between the report signer and the relevant qualification. A shared name is insufficient.
5. **Evaluate state.** Apply the named rulebook to available notices, corrections, or inspections. Report uncertainty, missing evidence, and conflicts rather than equating silence with approval.
6. **Recognize the Digital Original.** Determine whether the artifact with its derived Consequential State is accepted for this purpose. Preserve that decision separately from the general cryptographic verification result.
7. **Retain minimally and provide redress.** Preserve the necessary evidence references, policy version, temporal scope, and decision basis under appropriate access controls; provide correction, review, and retention processes.

This pattern generalizes to product certificates, academic records, eligibility determinations, and institutional decisions. It does not assert that those use cases require the same identity attributes or acceptance rules.

## 10. Proposed Integration Profile

No immediate change to event kinds, canonical definitions, or core wire-format tags follows from this report. A separate domain integration profile could specify:

- Requester recognition, purpose categories, necessity assessment, and prohibited requests.
- Minimum attribute sets, alternatives, and private disclosure mechanisms.
- Authenticated binding between relevant actors and event-signing keys.
- The exact artifact or minimized decision artifact being anchored.
- Rulebook identifiers and versions, evidence dependencies, temporal scope, and fresh-evidence requirements.
- Separate outputs for integrity, state derivation, authority recognition, and acceptance.
- Retention, deletion, correction, access control, appeal, and independent oversight.

These are proposed profile responsibilities, not currently assigned OpenETR tags or a new supported JSON schema. Existing core anchors and notices are not a complete identity-request or wallet authorization system. Credential verification, selective disclosure, and any specialized privacy proofs require appropriate external implementations.

Where decisions depend on standing at a past time, retain the necessary protected evidence snapshot and timing basis. A current credential status cannot alone establish historical authority, and a self-declared event timestamp is not trusted time.

## 11. Review And Acceptance Tests

A pilot should demonstrate that:

1. Public artifact verification can occur without demanding the reader's civil identity unless a justified access policy requires it.
2. A prohibited or excessive identity request is rejected before disclosure, even when the requester can produce valid signatures.
3. Minimal assertions do not silently trigger retention of complete source credentials.
4. Actor-to-key bindings are authenticated and scoped; matching names or control of a profile are not treated as sufficient authority.
5. Missing or stale evidence leads to a visible limitation rather than a falsely positive result.
6. Correction changes the evaluated position without being described as erasure of earlier evidence.
7. Personal attributes, predictable digests, and persistent presentation identifiers do not leak through public tags, URLs, or logs.
8. A supported alternative route reaches a reviewable decision without requiring personal key management or a government VDC.
9. A reviewer can reproduce the recorded decision using its retained evidence and identified rules, subject to authorized access and retention limits.

These tests assess a deployment, not conformance by the abstract protocol to the Coalition's voluntary practices.

## 12. Conclusion

The report provides a policy argument for limiting identity demands. OpenETR can support that direction by making record integrity and consequential evidence independently verifiable without making universal identification a prerequisite.

Its role is to identify the artifact, validate the evidence graph, and derive Consequential State under defined rules. Whether the resulting Digital Original is accepted, which identity attributes may be requested, and how people are protected remain explicit governance responsibilities.

The model does not remove policy. It gives policy decisions an inspectable evidentiary basis while leaving their legitimacy open to institutional review and challenge.

## Related Reading

- [Policy brief](../../docs-site/policy-briefs/better-identity-practices-and-openetr.md)
- [OpenETR axioms](../../docs-site/openetr/axioms.md)
- [Core Record Ruleset](OPENETR_CORE_RECORD_RULESET_1_0.md)
- [System Integration Considerations](SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Actor-Neutral Identity Design Note](OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [Policy Guards Design Note](CONTROL_EVENT_POLICY_GUARDS_DESIGN_NOTE.md)
- [Verifiable Credentials And Status Lists](../../docs-site/policy-briefs/openetr-verifiable-credentials-and-status-lists.md)
