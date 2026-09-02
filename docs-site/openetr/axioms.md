# OpenETR Axioms

OpenETR can be distilled into ten foundational propositions. Together they
describe what the protocol treats as evidence, how state is derived, and where
the protocol's responsibility ends.

These axioms are a conceptual guide. The wire-format specification and
implementation specifications define the normative technical details.

## 1. The Digest Identifies The Artifact

A **Digital Artifact** is identified by a cryptographic digest, independently
of its filename, location, format, or number of copies.

## 2. A Signature Attributes A Statement

Every OpenETR event is an immutable, attributable statement by a signing key.
A valid signature establishes authorship and integrity; it does not, by
itself, establish authority, recognition, or legal effect.

## 3. An Anchor Begins A Candidate Record

An **Anchor Record** establishes the starting point of a candidate **Digital
Controllable Record (DCR)**. It does not, by itself, establish uniqueness,
validity, or recognition.

## 4. Links Create The Control Graph

Later control records reference prior records. Shared artifact identifiers and
cryptographic event references allow the DCR to be reconstructed and verified
independently.

## 5. Events Are Evidence; State Is Derived

Events are not overwritten to represent current state. **Consequential State**
is derived by evaluating signed DCR evidence according to defined protocol and
verifier rules.

## 6. Invalid Claims Remain Visible

Conflicting, unauthorized, or malformed statements remain part of the
available evidence. A verifier warns about or excludes them according to its
rule book rather than erasing signed history.

## 7. A Digital Original Has Consequential State

A **Digital Original** is a Digital Artifact for which consequential state has
been established through a DCR. Identical copies represent the same artifact;
copying its bytes does not independently create another consequential history.

Whether a person, institution, system, or law recognizes that state as
authoritative for a particular purpose remains a separate question.

## 8. Verification Is Separate From Recognition

OpenETR verifies digests, signatures, event links, graph structure, and
protocol transitions. External systems, policies, institutions, and laws
determine recognition and effect.

## 9. Identity Is Actor-Neutral And Contextual

An `npub` identifies a signing key. Whether it represents a person,
organization, service, or autonomous agent, and whether that actor is trusted
or authorized, is determined outside the protocol.

## 10. Control Is Portable Across Systems And Domains

Signed records do not belong to one application, relay, operator, or
jurisdiction. Domain adapters translate business actions into the general
OpenETR model, while any conforming system can store, retrieve, and verify the
resulting DCR.

## The Five Maxims

The same model can be expressed in five short statements:

> **Digests identify. Signatures attribute. Links order. Policies interpret.
> Recognition gives effect.**

The first three describe the portable cryptographic evidence. Policy derives
what follows from that evidence. Recognition determines what consequence that
state receives outside the protocol.

## Related Reading

- [OpenETR Overview](index.md)
- [Control Layer](control-layer.md)
- [Consequential State](consequential-state.md)
- [Recognition Boundary](recognition.md)
- [Nostr Wire Format](wire-format.md)
- [Digital Controllable Record design note](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
