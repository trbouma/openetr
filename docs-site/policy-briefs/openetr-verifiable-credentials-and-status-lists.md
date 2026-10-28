# OpenETR, Verifiable Credentials, And Status Lists

*Policy brief | 28 October 2026*

## Policy Proposition

Digital transactions require confidence both in the parties involved and in the records on which they rely. These are connected questions, but they are not the same question.

W3C Verifiable Credentials can provide evidence of a party's qualifications, organizational affiliation, or authority. Bitstring Status Lists can communicate status information about those credentials. OpenETR provides signed evidence about digital artifacts, from which an identified rulebook derives consequential state. Recognition policies determine whether the parties and resulting conclusions are accepted in a particular context.

**Credentials can support recognition of the parties. OpenETR can support evaluation of what follows from the documents between them.** Neither mechanism alone establishes legal effect.

This is a proposed composition of complementary mechanisms, not a claim that OpenETR currently implements a W3C status-list adapter.

## Different Questions Within One Transaction

| Question | Contribution |
| --- | --- |
| What is claimed about this party's standing? | Credentials containing attributable claims about qualifications, roles, or authority. |
| What status has been published for that credential? | A status-list entry interpreted for its stated purpose. |
| What evidence concerns this exact document? | OpenETR anchors and associated signed events discovered using its digest. |
| What consequential state follows? | An identified rulebook evaluating applicable evidence. |
| May we rely on that conclusion here? | Recognition policy applying domain, institutional, contractual, and jurisdictional requirements. |

This division is an architectural choice, not an exclusive allocation of capabilities. Verifiable Credentials can describe things other than people, and OpenETR can carry evidence relevant to recognition. The aim is to combine useful mechanisms without requiring one to perform every role.

## What The W3C Mechanisms Contribute

A Verifiable Credential expresses issuer claims in a tamper-evident form. Verifying it does not automatically establish the truth of its claims or the issuer's authority. Acceptance remains a verifier decision. [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/#trust-model)

Bitstring Status Lists associate credentials with indexed entries in secured lists. They support revocation, suspension, refresh, and custom messages. Lists can be cached or supplied by holders; a live issuer API call is not mandatory. The familiar 131,072 one-bit entries are a default size, not a maximum; larger and multiple lists are possible. Shared retrieval helps reduce credential-specific tracking. [W3C Bitstring Status List 1.0](https://www.w3.org/TR/vc-bitstring-status-list/)

Credential status does not necessarily determine the underlying entitlement, and the status-list issuer can differ from the credential issuer. [Conceptual framework](https://www.w3.org/TR/vc-bitstring-status-list/#conceptual-framework) and [status-list credential](https://www.w3.org/TR/vc-bitstring-status-list/#bitstringstatuslistcredential)

## What OpenETR Contributes

OpenETR starts with the digital artifact. A verifier possessing its exact bytes can generate its digest and discover associated signed evidence through available relays or local collections. Discovery does not require an issuer-assigned status-list position or an issuer-specific API.

The digest identifies the artifact, not a uniquely authoritative claim about it. Multiple parties can publish evidence concerning the same artifact. Recognition remains necessary to distinguish an accepted issuer or inspector from an unrelated signer.

OpenETR's broader concept is not merely a larger menu of status labels. It is the evaluation of evidence under an identified rulebook. Notices, inspections, corrections, and other assertions can contribute different information. A domain rulebook determines which assertions apply, how conflicts are handled, and what conclusions follow. Transferable-record rules require additional safeguards and should not be assumed from the Core Record Ruleset alone.

**Status can be a conclusion drawn from evidence, rather than only a published field.** That does not make a published status less useful: it can itself be an input to evaluation.

## Example Of A Cargo Inspection

Consider a receiving organization deciding whether to rely on an inspection report accompanying a shipment. A proposed integrated workflow would be:

1. **Recognize the inspector.** Obtain a credential asserting the inspector's qualification and scope. Establish that its issuer is recognized for that purpose.
2. **Check the credential.** Verify its securing proof, validity period, and relevant status information under the receiving organization's policy.
3. **Connect standing to the signing key.** Establish an authenticated binding between the credential subject and the key signing the OpenETR event. A matching display name is insufficient; possession of a credential alone does not establish this binding.
4. **Verify the report.** Hash the exact report bytes, retrieve the associated anchor and inspection evidence, and verify signatures and document references. Check the cargo identifiers against the report under the Cargo Inspection Profile.
5. **Evaluate the evidence.** Apply the selected inspection rulebook, including relevant corrections, notices, scope limitations, and unresolved conflicts.
6. **Record the decision.** Preserve the evidence versions, retrieval times, rulebook version, and recognition basis used to accept, reject, or refer the report for review.

A recognized inspector does not make every report correct. An intact report does not establish that its signer was authorized. The combined workflow addresses both questions without collapsing them.

## Time And Effect Must Remain Explicit

Suppose the inspector's credential is revoked after the report was signed. A receiving organization must distinguish current credential status from authority at the time of inspection, and from the report's acceptability today.

A domain policy might distinguish routine expiry from a key compromise or a finding of misconduct. Those situations need not have identical consequences for earlier reports. Conversely, a presently acceptable credential does not prove historical authority.

An OpenETR event's declared timestamp is not, by itself, independent proof of when an inspection occurred. Historical decisions may require retained status snapshots, effective dates, independent timing evidence, or further authoritative assertions. Missing evidence should produce an explicit limitation, not an invented certainty.

## Distribution And Privacy Trade Offs

For OpenETR, issuer-independent retrieval means that the same signed evidence can be served by another relay, archive, or synchronized collection. It does not mean that availability, freshness, or completeness is guaranteed. An empty query result cannot prove that no adverse notice exists.

A relay operator may observe a digest query even when it is independent of the issuer. Broader retrieval followed by local filtering can reduce that exposure, but follow-up queries for notices may reveal the specific interest. Applications should assess the complete retrieval pattern.

Personal credentials need not be published on public relays to support this composition. Exchange only the recognition evidence necessary for the decision, using appropriate access and disclosure controls. Even public references and digests can enable correlation.

Neither approach should be selected on an unsupported claim of superior scale. Compact status entries and individually signed evidence have different storage, bandwidth, verification, and historical-detail trade offs. Millions of records require operational planning in either architecture.

## Integration Without Protocol Dependence

An integration profile could consume a W3C status list as recognition evidence, or publish a status projection derived from OpenETR evidence under a named rulebook. Such an adapter would need explicit mappings, authority checks, freshness rules, and error handling. Publishing an artifact digest alone would not make a document a conforming W3C credential.

The OpenETR core need not mandate Verifiable Credentials, DIDs, or a particular status service. A domain may instead use registries, direct attestations, or other recognition mechanisms. Semantic interoperability belongs in the applicable domain profile and rulebook, not in an assumption that all credentials or document states mean the same thing.

## Policy Recommendations

- Keep party standing, credential status, document integrity, and consequential state as separate decision inputs.
- Require an authenticated connection between recognized parties and the keys signing record evidence.
- Make temporal scope and unavailable or stale evidence visible in decisions.
- Preserve portability without requiring personal credentials to become public evidence.
- Specify recognition responsibilities and rulebook versions instead of treating technical verification as automatic legal acceptance.

The policy opportunity is composition: **credentials support confidence in who may act; OpenETR preserves evidence of what was asserted about a document; rulebooks and recognition determine what follows.**

## Related OpenETR Documents

- [Core Record Ruleset 1.0](../docs/specs/OPENETR_CORE_RECORD_RULESET_1_0.md)
- [Inspection Evidence Specification](../docs/specs/OPENETR_INSPECTION_EVIDENCE_SPEC.md)
- [Cargo Inspection Profile](../docs/specs/OPENETR_CARGO_INSPECTION_PROFILE.md)
- [TRQP Integration Note](../docs/specs/OPENETR_TRQP_INTEGRATION_NOTE.md)
- [Why Control Is Not Recognition](why-control-is-not-recognition.md)
- [OpenETR, LEI, And Verifiable Trade](openetr-lei-and-verifiable-trade.md)
