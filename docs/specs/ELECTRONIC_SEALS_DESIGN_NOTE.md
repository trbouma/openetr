# Electronic Seals And OpenETR

## Status And Scope

Exploratory design note supporting the
[Electronic Seals And OpenETR policy brief](../../docs-site/policy-briefs/electronic-seals-and-openetr.md).
This proposes a domain profile, not a new base action, registered schema,
implemented sealing workflow, or claim of legal seal equivalence.

The starting point is John Gregory's 2011 discussion of transactional seals,
which distinguishes deliberate sealing from ordinary signing and corporate
identification. His historical analysis should not be read as a current survey
of every jurisdiction. See [Electronic Seals](https://www.slaw.ca/2011/10/28/electronic-seals/).

## Design Position

OpenETR can provide an evidence foundation for electronic sealing: bind a
statement to exact bytes, attribute it to a signing key, preserve supporting
authority evidence, and derive scoped state under identified rules. Whether
that process constitutes a seal with a particular effect depends on the
applicable legal regime and recognition policy.

Distinguish four questions:

| Question | Evidence or decision required |
| --- | --- |
| Which artifact was sealed? | Exact-byte SHA-256 digest and verifiable reference |
| Which key made the statement? | Signed event and event-identifier verification |
| For whom, in what capacity, and with what intention? | Explicit statement plus organizational, mandate, approval, or other authority evidence |
| What effect follows? | Identified profile rules and separate legal or institutional recognition |

A seal attesting organizational origin is not automatically an execution of a
deed. Neither is automatically a transfer of control. A graphic, profile name,
or QR code is presentation or discovery, not sufficient evidence of sealing.

## Proposed Evidence Profile

The profile should define an explicit signed sealing statement containing or
cryptographically binding the following information. These are conceptual
requirements, not proposed wire-tag names:

- artifact digest and digest algorithm;
- seal purpose, such as organizational origin, approval, certification, or
  deliberate execution under a specified legal rulebook;
- the exact declaration adopted by the signer and its version;
- principal, signer capacity, and references to authority or approval evidence;
- relevant anchor or other event identifiers;
- profile identifier and version, and claimed jurisdiction or rulebook;
- signer-declared time, distinguished from independent Temporal Proof;
- policy-defined status and relationship to later corrections or withdrawals.

Before implementation, choose a versioned representation whose required
semantics are machine-readable and signed. Human-readable event content alone
must not become an implicit state-transition parser. Merely mentioning a seal
in an Anchor Event does not establish a new core consequence.

Two representation options warrant review: an extension to the signed anchor
for an initial sealing statement, or separate signed associated evidence
referencing an existing anchor. The latter accommodates third-party sealing
without making the sealer the Anchor Publisher. No event kind or `seal` action
is allocated by this note.

## Baseline And Extension Boundary

[Core Record Ruleset 1.0](OPENETR_CORE_RECORD_RULESET_1_0.md) establishes anchored
state and the Anchor Publisher's signed position. It does not establish
organizational authority, sealing intent, a current controller, or legal effect.
Its Publisher Notices must use the same key as the anchor.

A sealing extension must define its own statement validation, authority
requirements, state dimensions, conflicts, and missing-evidence handling. It
must preserve baseline meanings. A new organizational key cannot silently
replace the original publisher for Core 1.0 notices; rotation and recovery
require explicit extension rules and supporting evidence.

Keep seal issuer, Anchor Publisher, and Current Controller distinct. In a
warehouse-receipt workflow, the warehouse's origin seal can remain attributable
to the warehouse after control transfers. A controller cannot withdraw that
seal merely by acquiring control, and a seal withdrawal does not itself
transfer control or rescind a transaction.

## Workflow And Verification

1. Finalize the exact artifact bytes. Any visible badge or embedded signature
   added later changes the byte identity and needs a separately identified
   representation or a new artifact.
2. Present the artifact, principal, capacity, purpose, and declaration for
   explicit adoption. A deed-oriented workflow needs a distinct deliberate
   act and any required execution, witnessing, and delivery evidence.
3. Sign the declaration with its artifact and context binding. Automated
   organizational origin seals may instead operate under a defined mandate;
   automation does not establish human intent.
4. Preserve the signed evidence, authority dependencies, ruleset, and any
   independently verifiable time evidence. Relays and hosting sites are
   retrieval mechanisms, not the source of seal authority.
5. Verify artifact correspondence, signature, declaration, authority, temporal
   scope, relevant later evidence, and profile rules separately. Report the
   recognition result and resulting operational effect explicitly.

Verification should distinguish a digest computed from presented bytes from
a lookup using a supplied digest. A QR link retrieves evidence; it does not
prove that a printed page or screenshot reproduces the sealed bytes.

## Lifecycle, Security, And Disclosure

Retain original statements and append later evidence. A withdrawal records a
position; it does not erase past execution or necessarily cancel an obligation.
Do not conflate certificate revocation, compromised-key evidence, withdrawal
of an assertion, and invalidity of an underlying document.

Historical verification needs applicable authority evidence, certificate or
credential status where relevant, time evidence, and the rules used. A current
registry response alone may not establish past authority. Missing or divergent
evidence must remain visible; no notice found is not proof of continuing validity.

Protect signing keys, define approval and delegation boundaries, and bind every
statement to its artifact and purpose to prevent reuse for another document
or action. Preserve conflicts instead of choosing the most recent declared
timestamp as authoritative.

Documents and authority evidence can remain private where the profile permits.
Digests and public event metadata can still permit correlation or candidate-file
matching. Future private-proof mechanisms must satisfy the
[Private Evidence And Verified Propositions](PRIVATE_EVIDENCE_AND_VERIFIED_PROPOSITIONS_DESIGN_NOTE.md)
design requirements; they are not assumed capabilities of this profile.

## Regulated Seal Integration

For public seals and Apostilles, apply the more specific
[Apostille domain adapter](APOSTILLE_DOCUMENTS_DOMAIN_ADAPTER_SPEC.md).
It distinguishes public-document authentication, authority-issued certificates,
register responses, and observer attestations. An OpenETR sealing profile
must not add mandatory legalisation to the Convention process or mistake
a third-party anchor for official issuance.

The Canadian federal seal pathway in [PIPEDA section 39](https://laws-lois.justice.gc.ca/eng/acts/P-8.6/section-39.html)
depends on the covered federal provision and a secure electronic signature
identified as the person's seal. The
[Secure Electronic Signature Regulations](https://lois.justice.gc.ca/eng/regulations/SOR-2005-30/page-1.html)
prescribe a process and certificate requirements. A native OpenETR signature
does not demonstrate that those requirements have been met.

Likewise, eIDAS defines specific seal categories and requirements. A qualified
electronic seal requires a qualified certificate and qualified creation device;
OpenETR anchoring alone supplies neither. See
[eIDAS Articles 3 and 35-40](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A02014R0910-20241018).

An integration can preserve or reference a separately created regulated seal
and its validation material. It must identify whether that seal covers the
artifact, a detached statement, or a package. Anchoring a validation report
does not make the underlying artifact qualified-sealed. Where embedding a seal
changes a file, anchor the final bytes or explicitly identify both artifacts.

## Next Design Step

Start with an organizational-origin profile for a bounded institutional use
case. Define the statement schema, key-to-organization evidence, mandate and
rotation rules, status semantics, independent verification bundle, and test
vectors before adding UI or a seal-verification API. Deed execution and
regulated qualified-seal integration require distinct profiles and review.

## Related Specifications

- [Organizational Reference Layer](OPENETR_ORGANIZATIONAL_REFERENCE_LAYER_DESIGN_NOTE.md)
- [Actor-Neutral Identity](OPENETR_ACTOR_NEUTRAL_IDENTITY_DESIGN_NOTE.md)
- [Consequential State Architecture](CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [Generic Verifier Policy](OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Apostille Documents Domain Adapter](APOSTILLE_DOCUMENTS_DOMAIN_ADAPTER_SPEC.md)
