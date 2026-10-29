# NIST Key Management Guidance And OpenETR

## Status And Sources

Policy and architecture analysis, 29 October 2026. This is guidance for integrations, not a security audit, a new wire-format specification, or an assertion that the demonstration application implements every control described here.

Primary source: Elaine Barker, NIST SP 800-57 Part 1 Revision 5, *Recommendation for Key Management: Part 1 - General*, May 2020. References below use section numbers and printed page numbers in the supplied PDF, not PDF viewer page numbers. See the [NIST publication page](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) and [publication](https://doi.org/10.6028/NIST.SP.800-57pt1r5).

This review concerns Revision 5 specifically. A deployment with formal compliance obligations must separately assess applicable current requirements, algorithms, modules, and operating procedures. Recommendations for OpenETR below are architectural conclusions drawn from the guidance, not NIST endorsements of OpenETR or a particular custody model.

## 1. Executive Assessment

OpenETR users should ordinarily interact with meaningful actions and Commitment Profiles through an application that provides appropriate authentication, operation authorization, protected signing, and a documented recovery route. Handling a raw private key should not be a prerequisite for issuing, inspecting, or evaluating a record.

NIST provides unusually direct support for minimizing human exposure to keys. Section 9.3, p. 118, prefers that humans cannot view keys and requires plaintext-key access to be traceable to the accessing entity. This supports hidden-by-default key handling, but does not prescribe a user-facing application or require central server custody.

Direct key access remains possible in OpenETR. Export and self-managed operation can serve portability, specialist workflows, and deliberate self-custody. They should be explicit, risk-assessed capabilities, not routine onboarding or a universal recovery instruction. A deployment may prohibit export under its own policy even though the protocol does not.

The central qualification is recovery. NIST treats signing keys differently from decryption keys. **Recovering the user, restoring signing capability, and restoring the same private key are distinct operations.** An application-managed account should not silently imply indefinite backup of every signing key.

## 2. What NIST Supports And What It Does Not Establish

| Source | Guidance relevant to this analysis | OpenETR implication |
| --- | --- | --- |
| Section 1 | Key management covers the lifecycle, not just algorithm selection. | A functioning signer is not a complete operational security design. |
| Section 5.2, pp. 33-34 | Separate key purposes in general; exceptional permitted combinations are specific. | Distinguish login credentials, event-signing keys, wrapping keys, and report-decryption keys. |
| Sections 5.3 and 5.3.6, pp. 34-46 | Cryptoperiods depend on risk and use; signing and verification lifetimes differ. | Define when to stop new signatures without discarding public verification evidence. |
| Sections 6.1-6.2 | Protect key information in storage and transit according to its type and use. | Hiding an `nsec` in the interface is not protection from application compromise. |
| Section 8.2.2.1, Table 7, p. 105 | Private signing-key backup is generally discouraged, with justified exceptions under owner control. | Do not recommend universal recoverable signing-key escrow. |
| Section 8.3.1, Table 9, pp. 109-110 | Archival requirements differ by key type; private signing keys are not archival material. | Historical verification normally needs public keys and evidence, not old private signers. |
| Section 9.1, p. 116 | Authenticate and authorize access to key-management functions and record access attempts. | A valid login must not automatically authorize every profile, export, or recovery operation. |
| Sections 9.2-9.4, pp. 116-120 | Inventory, responsibility, traceability, and audit are separate controls. | Maintain key references and ownership metadata without placing secrets in inventory or audit logs. |
| Section 9.5.4, pp. 124-125 | Compromise requires revocation, assessment, replacement where needed, and notification. | An account reset alone is not recovery from exposure of signing material. |
| Appendix B.3.1, pp. 136-137; B.5, pp. 145-146 | Recovery is key-type-specific and requires an explicit policy. | Assess replacement and continuity before electing to restore the same signer. |

The guidance does not establish that a web application is inherently safer than self-custody. The outcome depends on storage, authorization, software integrity, operations, and recovery controls. Nor does it make a valid signature proof of a human user's intention.

## 3. The Recommended Application Boundary

A proposed production integration should separate:

```text
User or service authenticates to the host application
  -> application authorizes a specific profile and operation
  -> protected signer validates and signs the requested event
  -> OpenETR publishes independently verifiable evidence
  -> a verifier evaluates the Evidence Graph under identified rules
  -> recognition determines acceptance and effect
```

The user-facing action should identify the artifact, operation, Acting Profile, and material consequences. Sensitive actions may require fresh authentication, additional approval, or separation of duties. An existing session is not an unlimited signing mandate.

The signer should receive a constrained, validated operation rather than an unrestricted instruction to sign arbitrary bytes. Protect against cross-tenant access, profile substitution, confused-deputy behaviour, replay, and changes between approval and signing. Keep secrets out of client responses, URLs, telemetry, exception traces, and application logs.

A passkey-style experience is an analogy for the product boundary, not a claim that a WebAuthn key can directly produce a Nostr event signature. The authentication mechanism and OpenETR signing mechanism may be entirely separate.

## 4. Custody Is A Separate Decision

| Deployment pattern | What the application manages | Main consideration |
| --- | --- | --- |
| Device-managed signer | User interaction, authorization, and access to a protected local signer. | Device loss, local malware, platform capability, and continuity. |
| Organization-managed signer | Account access and a controlled signing service. | Operator authority, insider access, tenant isolation, and service compromise. |
| External or remote signer | Requests to a separately controlled signer with explicit approvals. | Request binding, delegation, availability, and recovery responsibilities. |
| User-managed key | Import or connection to a user-selected signer, potentially with raw key handling. | Accidental exposure, unmanaged copies, loss, and bypass of host controls. |

These are integration options, not a claim that every pattern is supported by the current component. Hardware and managed-key services must be checked for compatibility with the required signing operation. Nostr uses Schnorr signatures over `secp256k1`; support for a generic elliptic-curve or ECDSA key is not enough. [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md#events-and-signatures)

A provider that holds a usable private key can potentially sign. Its controls and responsibilities must be made explicit. Application mediation should not be described as exclusive user custody unless the implementation actually provides that property.

## 5. Applying The Guidance To Root And Profile Keys

OpenETR's Control Desk Key organizes configuration and access to independent Commitment Profile keys. It is an administrative role, not a special cryptographic key type or automatically a certificate-authority root. The root-to-profile relationship is not mathematical derivation or, by itself, legal delegation. See the [root-and-profile model](ROOT_AND_PROFILE_IDENTITY_MODEL.md).

Where the root can decrypt or obtain profile signer material, compromise of that root may expose the associated profile set. Document this dependency in the key inventory and incident plan. Separate administrative access from routine signing where practical, and avoid using the administrative key as the everyday signer merely for convenience.

Classify each actual use of a key. A key called a root may sign configuration and participate in protecting secrets; those uses need separate assessment. Section 5.2's purpose-separation principle is a potential tension where a Nostr key is reused for signing and encryption/key agreement. Naming it a root or encrypting its stored representation does not resolve the tension. A dedicated storage-wrapping key can separate storage protection from event signing, but any remaining protocol-level reuse still needs review.

Relay-backed encrypted configuration does not remove key custody. If the only means of unlocking it is a lost root secret, a password reset cannot reconstruct it. Conversely, if the host can recover that secret, the host's recovery authority is part of the security model.

## 6. Four Different Meanings Of Recovery

### Account Recovery

Restore legitimate access to a user-facing account. This requires a recovery policy appropriate to the account's authority. It need not export, replace, or reveal an OpenETR private key.

### Restoration Of Signing Capability

Restore the ability to perform authorized operations, potentially with a new profile key or a prearranged alternative signer. Recognition of continuity must be explicit. A new key is a new Key-Based Identifier; it does not inherit standing simply because the application gives it the old profile name.

### Recovery Of The Same Private Signing Key

Restore a protected copy of an existing signer. Table 7 and Appendix B.3.1.1 generally discourage this because additional holders or copies complicate attribution and support for non-repudiation. NIST permits justified exceptions and calls for a highly secure recovery method; depending on the circumstances, a recovered signer is for immediate use and replacement as soon as possible.

A deployment should document why restoration of the same key is preferable to generating and recognizing a replacement, who controls any backup, which approvals are required, and how recovery is audited. It should not call indefinite retained signing material an archive for verifying old records: the private key is not needed for that verification.

### Recovery Of Decryption Capability

Restore access to encrypted records that must remain available. This may require retention of decryption keys and related metadata under a different policy. Loss of a signing key does not prevent verification of its existing public evidence; loss of a report-decryption key can make its confidential content inaccessible.

The four processes can share an interface but should not share an unexamined authorization policy. Recovery is itself a sensitive operation, not a support shortcut around normal security.

## 7. Optional Export And Direct User Handling

Recommended OpenETR integration policy: keep private keys out of ordinary user workflows, but allow a deployment to offer deliberate export or self-managed operation where justified. Public identifiers may be displayed without treating them as secrets; private `nsec` material requires a different interaction.

Where export is enabled, a proposed control set includes:

- Fresh authentication and explicit authorization for the particular key and purpose.
- A warning that export creates another signing capability and changes the custody assumptions.
- Prefer protected transfer to an intended signer or encrypted export over routine plaintext clipboard copying.
- Record the export authorization and key identifier without recording the secret.
- Explain that deleting a downloaded file or removing a profile does not prove all copies have been destroyed.
- Document responsibility for imported keys, including possible copies held by previous custodians.

These recommendations do not create a NIST exception or guarantee conformance. Some deployments should disable export entirely. OpenETR protocol permissiveness is not organizational permission.

## 8. Rotation, Compromise, And Historical Evidence

NIST's cryptoperiod recommendations are risk-based guidance, not an instruction to overwrite a record's signer. Section 5.3.6 recommends approximately one to three years for private signing keys under its stated assumptions, while allowing justified variation. Do not turn this into a universal OpenETR expiry or claim that all signatures become invalid when the private key retires.

Rotation produces a new public key. Existing events retain their original signatures and identifiers. An integration needs authenticated continuity evidence and recognition rules for new authority; changing a local profile label alone is insufficient. This note does not define a new rotation event or assume that cross-key succession is already handled by the Core Record Ruleset.

On suspected compromise, stop affected signing, investigate dependencies, replace exposed keys as needed, and communicate through authenticated channels. Root compromise may require review of every profile secret it could access. Revoking sessions or re-encrypting the same exposed key does not remove an attacker's signing ability.

An attacker retaining a private key can still create mathematically valid signatures. Effective rejection depends on verifiers learning and applying the relevant compromise evidence and policy. A statement signed only by an already-compromised key is not sufficient by itself to establish a trustworthy successor.

Historical reliance may require trusted timing and evidence snapshots. A Nostr event's declared timestamp is not independent proof that it predates a compromise. Preserve public verification material, signed events, algorithm information, and the recognition basis for past decisions. Plan for algorithm ageing separately from ordinary key rotation.

## 9. The Evidence Graph Boundary

Application-managed custody does not make the application the sole authority for existing evidence. Once published or exported, an event can be verified using its public key without the account system or original signer running.

The Digital Artifact is identified by its digest. Signed events form its Evidence Graph. Defined rules derive Consequential State. The artifact with that state is a Digital Original; recognition determines whether it is accepted for a purpose.

The application remains responsible for deciding who may initiate signing and for explaining how its signing authority is protected. A shared organizational profile attributes the event to that key, not uniquely to one employee. Protected operational logs and approvals may be needed to establish the human or service context. Those logs need not become public relay records.

Independent verification of past evidence and dependence on a protected signer for future actions are compatible. Portability of public evidence does not require exposing private keys, and a non-exportable key does not prevent exporting the evidence it signed.

## 10. Implementation And Assurance Checklist

Before describing a deployment as production-ready, establish:

1. A key inventory covering roles, owners, custodians, uses, locations, dependencies, activation, retirement, and compromise status, without raw secrets in ordinary inventory records.
2. A supported signing boundary with tested algorithm compatibility, authorization checks, tenant isolation, and secret-handling controls.
3. Separate policies for account recovery, signer replacement, exceptional private signing-key restoration, and decryption recovery.
4. Explicit export/import permissions and a policy for pre-existing copies held elsewhere.
5. A tested incident process that distinguishes session compromise, host compromise, root exposure, and profile-key exposure.
6. A way for relying parties to assess rotation, compromise, continuity, and historical timing without silently rewriting past evidence.
7. Audits of successful and failed key operations, with access controls, retention, and no key material in logs.
8. Demonstrated recovery exercises, removal of departed users' access, and contingency plans for provider or device failure.

These are integration acceptance criteria, not implemented features established by this review. No new event kinds or wire-format fields are proposed here. Formal conformity requires assessment of the whole system, including algorithms and cryptographic modules. Following SP 800-57 management principles does not make a Nostr deployment NIST-approved or FIPS-validated.

## Related Reading

- [Policy brief](../../docs-site/policy-briefs/application-managed-keys-and-openetr.md)
- [System Integration Considerations](SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Root And Profile Identity Model](ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Core Record Ruleset](OPENETR_CORE_RECORD_RULESET_1_0.md)
- [OpenETR Axioms](../../docs-site/openetr/axioms.md)
- [Better Identity Practices](OPENETR_BETTER_IDENTITY_PRACTICES_ANALYSIS_NOTE.md)
