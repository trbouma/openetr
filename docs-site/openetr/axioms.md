# OpenETR Axioms

The ten axioms are the centre of gravity of this page. They describe what
OpenETR treats as evidence, how Consequential State is derived, and where the
protocol's responsibility ends. The Canonical Definitions provide the precise
vocabulary needed to express those axioms, while the Five Maxims distill what
follows from them into statements that are easier to remember and apply.

Read the definitions first as a common vocabulary, the axioms as the
foundational model, and the maxims as its practical summary. The axioms are a
conceptual guide; the wire-format specification and implementation
specifications define the normative technical details.

## Canonical Definitions

The core definitions are repeated here for convenience:

- A **Digital Artifact** is persistent digital content with a unique content
  identity, normally established by a cryptographic digest.
- A **Digital Controllable Record (DCR)** is the signed evidence structure from
  which defined rules derive Consequential State concerning a Digital Artifact
  after the evidence is validated.
- **Consequential State** is state that follows when validated DCR evidence is
  evaluated according to defined protocol and verifier rules. It is a derived
  result, not another event or authoritative database row.
- A **Digital Original** is a Digital Artifact with Consequential State.
- A **Key-Based Identifier (KBI)** is an identifier whose canonical value is
  public-key verification material or a deterministic encoding of that
  material. It identifies the signing key used to verify attributable signed
  evidence; it does not, by itself, establish the identity, actor type,
  authority, role, or recognition of the actor associated with that key.

The complete set of formal terms is maintained in
[Clause 3 of the OpenETR committee draft](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_DRAFT_NATIONAL_STANDARD.md#3-terms-and-definitions).

## Ten Axioms

The diagram summarizes how the core terms relate before the axioms state the
model's foundational propositions.

![OpenETR model showing Digital Artifact, Digital Controllable Record, Consequential State, Digital Original, Recognition, and Effect](../assets/images/openetr-model.png)

### 1. The Digest Identifies The Artifact

A **Digital Artifact** is identified by a cryptographic digest, independently
of its filename, location, format, or number of copies.

### 2. A Signature Attributes A Statement

Every OpenETR event is an immutable, attributable statement by a signing key.
A valid signature establishes authorship and integrity; it does not, by
itself, establish authority, recognition, or legal effect.

### 3. An Anchor Begins A Candidate Record

An **Anchor Record** establishes the starting point of a candidate **Digital
Controllable Record (DCR)**. It does not, by itself, establish uniqueness,
validity, or recognition.

### 4. Links Construct The Evidence Graph

DCR records reference prior records and related evidence through cryptographic
identifiers. These links construct an **Evidence Graph** from which protocol
rules can derive Consequential State. The portion concerned specifically with
control transitions forms the **Control Graph**. Links establish relationships;
they do not, by themselves, establish validity or state.

### 5. Events Are Evidence; State Is Derived

Events are not overwritten to represent current state. **Consequential State**
is derived by evaluating signed DCR evidence according to defined rules.

### 6. Invalid Claims Remain Visible

Conflicting, unauthorized, or malformed statements remain part of the
available evidence. A verifier warns about or excludes them according to its
rule book rather than erasing signed history.

### 7. A Digital Original Has Consequential State

A **Digital Original** is a Digital Artifact for which consequential state has
been established through a DCR. Identical copies represent the same artifact;
copying its bytes does not independently create another consequential history.

Whether a person, institution, system, or law recognizes that state as
authoritative for a particular purpose remains a separate question.

### 8. Verification Is Separate From Recognition

OpenETR verifies digests, signatures, event links, graph structure, and
protocol transitions. External systems, policies, institutions, and laws
determine recognition and effect.

### 9. Identity Is Actor-Neutral And Contextual

A **Key-Based Identifier (KBI)** identifies public-key verification material
used to attribute signed evidence. It does not identify an actor as a matter of
protocol. Whether a KBI is associated with a person, organization, service,
device, or autonomous agent, and whether that actor is recognized or
authorized for a particular purpose, is determined by the applicable context.

In the Nostr binding, the 32-byte public key is the KBI. Its hexadecimal form
is the canonical wire encoding, while `npub` is the human-readable encoding of
the same key.

### 10. DCR Evidence Is Portable Across Systems And Domains

Signed records do not belong to one application, relay, operator, or
jurisdiction. Domain adapters translate business actions into the general
OpenETR model, while any conforming system can store, retrieve, and verify the
resulting DCR.

## Five Maxims

The same model can be expressed in five short statements:

1. **Digests identify.** A cryptographic digest establishes which exact Digital
   Artifact the evidence concerns, independently of its filename, location, or
   number of identical copies.
2. **Signatures attribute.** A valid signature establishes that a particular
   signing key made a statement concerning the artifact, without by itself
   proving the signer's identity, authority, or recognition.
3. **Links order.** Cryptographic references connect signed records into an
   Evidence Graph and establish their claimed relationships, without by
   themselves deciding whether those records are valid or effective.
4. **Rules determine what follows.** Defined protocol and verifier rules
   evaluate the available DCR evidence and derive the Consequential State that
   the evidence supports.
5. **Recognition gives effect.** A relying party, institution, agreement, or law
   determines whether to accept the evidence or derived state for a stated
   purpose and what consequence that acceptance produces.

The first three maxims describe portable cryptographic evidence. The fourth
describes the derivation of Consequential State. The fifth preserves the
boundary between what OpenETR can verify and the effect that others choose or
are required to give the result.

## Related Reading

- [OpenETR committee draft](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_DRAFT_NATIONAL_STANDARD.md)
- [OpenETR Overview](index.md)
- [Control Layer](control-layer.md)
- [Consequential State](consequential-state.md)
- [Recognition Boundary](recognition.md)
- [Nostr Wire Format](wire-format.md)
- [Digital Controllable Record design note](https://github.com/trbouma/openetr/blob/main/docs/specs/DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
