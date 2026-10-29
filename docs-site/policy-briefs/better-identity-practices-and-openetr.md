# Better Identity Practices And OpenETR

*Policy brief | 29 October 2026*

## Policy Proposition

Making identity easier to verify should not make identity mandatory everywhere. Digital systems should ask for personal information because a particular decision requires it, not simply because a credential is available.

The Better Identity Coalition's October 2026 guidance makes this distinction central to responsible use of government-issued digital credentials. OpenETR can support the same direction from a records-first perspective: **establish which artifact is involved, evaluate its evidence and consequential state, and request identity information only where the applicable policy justifies it.**

Knowing whether a report has been corrected is different from knowing the identity of the person reading it. Knowing whether its signer is professionally qualified is different from collecting the reader's government credential.

[Read the detailed analysis and practice mapping](../docs/specs/OPENETR_BETTER_IDENTITY_PRACTICES_ANALYSIS_NOTE.md).

## What The Guidance Adds

The Coalition's voluntary practices distinguish justified identity requests from unnecessary collection and tracking. They emphasize proportionate disclosure, purpose limits, transparency, alternatives, and responsible handling of information. The report does not establish certification or a technical enforcement system; responsibility remains with adopting organizations. See the [publisher's initiative page](https://www.betteridentity.org/key-initiatives/best-practices) and [report](https://cdn.prod.website-files.com/669e6b8b6e7143c969f9e491/6ae125c6de7cdc2be4c368ce_vdc-best-practices-v1-0-october-2026.pdf), especially pp. 3-8 and 14.

The broader lesson is that a technically verifiable request is not necessarily an appropriate request. A valid signature cannot establish that collecting a person's attributes is necessary or fair.

## From Artifact To Accepted Digital Original

OpenETR contributes mechanisms that can operate beneath different policy frameworks:

| Layer | Contribution |
| --- | --- |
| Digital Artifact | A digest identifies the exact content being considered. |
| Evidence Graph | Signed, linked statements provide an inspectable basis for evaluation. |
| Consequential State | An identified rulebook determines what follows from validated evidence. |
| Digital Original | The artifact has Consequential State through its Evidence Graph. |
| Recognition and effect | The relying party determines whether that Digital Original is accepted for a stated purpose. |

An anchor does not confer government authority, establish personal identity, or make a document legally effective. These distinctions preserve the [OpenETR axioms](../openetr/axioms.md): verification and state derivation support recognition but do not replace it.

## Policy At The Right Decision Points

Before disclosure, a wallet or service should determine whether a request is justified and whether fewer attributes would suffice. This is where excessive requests must be prevented; recording them afterward is not an adequate substitute.

During record evaluation, an OpenETR verifier checks the artifact and available evidence and applies a named rulebook. The result should distinguish valid evidence, missing information, conflicts, and derived state.

At the point of reliance, an organization determines whether the actor, evidence, and state are acceptable in its context. That decision needs accountability and a route for review. A protocol cannot resolve legitimacy by itself.

These responsibilities may be implemented by one application or several independent systems. They should remain distinguishable even when the user experience is simple.

## A Practical Example

An institution receives a professional inspection report. It can verify the exact report using its digest, retrieve associated signed evidence, and evaluate relevant corrections or notices. Separately, it can assess evidence that the inspector was qualified and that the signing key was authorized.

The institution does not automatically need the report reader's identity, a copy of the inspector's full government credential, or a public record of every verification. It needs the evidence necessary for the decision.

After evaluating the report under its rulebook, it may accept the resulting Digital Original for a particular purpose, request further evidence, or decline reliance. A different institution may apply different recognition requirements to the same bytes without changing the underlying evidence.

This pattern applies more generally to product certificates, academic records, institutional decisions, and other consequential documents. The domain determines the necessary attributes and meanings; OpenETR does not impose a universal identity model.

## Privacy Must Be Designed Into The Integration

A records-first approach does not automatically preserve privacy. Reused public keys, stable document digests, detailed tags, and relay queries can enable correlation. Hashing an identity document does not anonymize it.

Sensitive credentials and presentation histories should not be published merely to demonstrate that a check occurred. An integration may instead retain a protected, minimized decision artifact where sufficient. That artifact is an assertion about the decision, not a replacement proof of every source attribute.

Similarly, a correction notice is not deletion. OpenETR can preserve evidence of a changed position but cannot erase copies already distributed outside an operator's control. Collection, access, retention, and deletion must be designed before publication.

The report also separates government credentials from routine authentication (p. 14). Host applications can authenticate users with suitable account mechanisms while keeping OpenETR signing keys behind that boundary. People should not have to manage raw keys to participate, and alternative service routes remain an organizational responsibility.

## Recommended Direction

- Require a purpose-specific justification before requesting identity attributes.
- Separate credential evidence, account authentication, authority to sign, and document acceptance.
- Use the minimum evidence needed, with access and retention appropriate to its sensitivity.
- Identify the rulebook and recognition basis behind consequential decisions.
- Provide alternatives, correction, review, and redress instead of treating cryptographic verification as final authority.

This calls for an integration profile, not a new identity requirement in the OpenETR core. The [detailed analysis](../docs/specs/OPENETR_BETTER_IDENTITY_PRACTICES_ANALYSIS_NOTE.md#10-proposed-integration-profile) outlines proposed responsibilities and pilot tests; it does not claim they are all implemented.

**OpenETR can make evidence about records portable without making people's identities universally observable. Whether an implementation achieves that outcome depends on its policy, privacy design, and institutional conduct.**

## Related Reading

- [Detailed analysis](../docs/specs/OPENETR_BETTER_IDENTITY_PRACTICES_ANALYSIS_NOTE.md)
- [Verifiable Credentials And Status Lists](openetr-verifiable-credentials-and-status-lists.md)
- [System Integration Considerations](../docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [OpenETR Axioms](../openetr/axioms.md)
