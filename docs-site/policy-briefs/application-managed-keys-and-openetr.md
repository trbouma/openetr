# Application Managed Keys And OpenETR

*Policy brief | 29 October 2026*

## Policy Proposition

People should ordinarily use OpenETR through applications that provide appropriate login, operation authorization, and recovery. They should see meaningful profiles and actions, not be required to copy private keys to issue or inspect a document.

**Private-key handling should be hidden by default, not prohibited by the protocol.** Deliberate export and self-managed operation can remain available where deployment policy permits them. The recommended default for ordinary users is a protected signing capability behind an understandable application interface.

This is an integration recommendation informed by NIST SP 800-57 Part 1 Revision 5, not a claim that NIST prescribes one application or custody architecture. [Read the detailed analysis](../docs/specs/OPENETR_NIST_KEY_MANAGEMENT_ANALYSIS_NOTE.md).

## Direct Support From NIST

NIST's key-management guidance is concerned with the complete lifecycle: generation, storage, distribution, use, retirement, recovery, and destruction. Section 9.3, printed p. 118, expresses a preference that humans not be able to view keys, while requiring plaintext-key access to be traceable. Sections 9.1-9.4 connect key use to authenticated access, authorization, inventory, accountability, and audit. [NIST SP 800-57 Part 1 Revision 5](https://doi.org/10.6028/NIST.SP.800-57pt1r5)

That supports the direction OpenETR already contemplates: an application can manage the Control Desk Key and Commitment Profiles while exposing only the operational choices the user needs.

It does not mean that hiding a key on a screen makes it secure. The signing boundary must resist unauthorized use, including misuse by compromised accounts, application processes, and administrators.

## Manage Capability Rather Than Expose Secrets

A warehouse operator should be able to authenticate, select the appropriate profile, review the document and action, and authorize issuance. The application can then obtain the signature through a protected signer and publish the evidence.

The signer might be device-managed, organization-managed, or separately operated. Application-managed experience does not necessarily mean central server custody. Each arrangement needs explicit responsibility for authorization, availability, recovery, and compromise response.

A login is also not a blanket authorization to sign. The operation must be bound to the intended artifact, action, profile, and permissions. A service operating a profile key must not imply that the signature alone proves a particular human personally performed or intended the action.

## Recovery Needs A Precise Meaning

The most important qualification in NIST's guidance is that recovery is not identical for every key type.

**Account recovery** restores legitimate access to a service. **Recovery of signing capability** may establish a new authorized signer. **Recovery of the same private signing key** restores a copy of an existing secret. **Decryption recovery** restores access to encrypted information. These are different security decisions.

NIST generally discourages private signing-key backup, while recognizing justified exceptions, and generally prohibits archiving private signing keys. Public verification keys can be retained to verify historical evidence. Where signing-key recovery is justified, it requires a highly secure process and consideration of prompt replacement. See Table 7, Table 9, and Appendix B.3.1 of the [guidance](https://doi.org/10.6028/NIST.SP.800-57pt1r5).

Accordingly, an OpenETR application should promise a documented recovery route, not silently promise that every old signing key will always be recoverable. A replacement key also needs recognized continuity: reusing a profile's display name does not transfer the old key's authority.

## Optional Export With Explicit Responsibility

OpenETR need not prohibit an informed user from controlling their own key or exporting it to another signer. However, export creates another place from which signatures may be produced. It changes the security assumptions and may bypass the host application's approval and audit controls.

Where enabled, export should require explicit authorization, appropriate fresh authentication, a clear warning, protected handling, and an audit record that does not contain the secret. Routine plaintext clipboard copying should not be the default recovery experience. Some institutional deployments may reasonably disable export.

The protocol's ability to accept a valid signature is not permission for every application to expose every signer.

## Protected Keys And Portable Evidence

OpenETR separates the mechanism that creates evidence from the evidence that others evaluate. A protected application may be necessary to authorize a new signature. It need not remain available for others to verify an existing signed event.

The digest identifies the Digital Artifact. Signed events form its Evidence Graph. An identified rulebook derives Consequential State, producing a Digital Original whose acceptance remains a recognition decision.

This preserves the records-first model without forcing users to become key-management specialists. **Public evidence can remain portable even when private keys are non-exportable.**

Retiring a signer does not erase its historical evidence. Compromise, however, may change what a relying party should accept. An account password reset cannot neutralize an exposed private key; affected signers, dependencies, and recognition policies need a separate response.

## Business Identity And Recognition Responsibilities

Organizations operating end-user and business applications are responsible for
determining and implementing the customer and business verification their
activities require. This includes applicable Know Your Customer (KYC) and
Know Your Business (KYB) processes, recognition of authorized representatives,
and the binding between those parties and their signing profiles. Specialist
providers can support these checks; using OpenETR does not perform or replace them.

Secure login establishes access to an account. A valid event signature
attributes a statement to a key. Neither, by itself, establishes a verified
customer, a legitimate business, or authority to act for that business.

The resulting Evidence Graph must be evaluated under an identified rulebook
to derive Consequential State. The relying application or organization must
then assess acceptance and effect under the relevant recognition rules,
including applicable legislation, regulation, and contractual or institutional
requirements. A private rulebook is not a substitute for applicable law.

KYC is not a universal prerequisite for using OpenETR. The required checks and
their scope depend on the activity, parties, risk, and jurisdiction. Sensitive
onboarding documents need not be placed on public relays to establish a
recognition basis. Different relying parties may reach different acceptance
decisions from the same signed evidence and should make their reasons explicit.

## Recommended Direction

- Make protected, application-mediated signing the ordinary user experience.
- Separate login, authorization to act, administrative key management, and event signing.
- Establish applicable KYC/KYB and representative-authority checks, and evaluate evidence and effect under an identified rulebook and applicable legal requirements.
- Specify recovery by key type and purpose, including alternatives to restoring the same private signer.
- Treat export as an explicit policy choice rather than a mandatory feature or routine task.
- Preserve public verification evidence and establish clear rotation and compromise procedures.
- Assess cryptographic implementation and module requirements separately from management-policy alignment.

No new OpenETR wire-format fields are required by this brief. The recommended controls require implementation and operational assessment; they are not a certification of the demonstration app. Following NIST's key-management principles does not, by itself, establish NIST approval or FIPS validation.

## Related Reading

- [Detailed NIST analysis and integration checklist](../docs/specs/OPENETR_NIST_KEY_MANAGEMENT_ANALYSIS_NOTE.md)
- [System Integration Considerations](../docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Root And Profile Identity Model](../docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Better Identity Practices And OpenETR](better-identity-practices-and-openetr.md)
- [NIST publication page](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
