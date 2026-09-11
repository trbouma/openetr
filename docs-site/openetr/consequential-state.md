# Consequential State

OpenETR is designed around one governing principle:

> Consequential state should be derived from end-verifiable evidence according
> to defined rules, not merely asserted by applications, databases or
> blockchains.

## Digital Artifact, Digital Controllable Record, And Digital Original

A **Digital Artifact** is persistent digital content with a unique content
identity, normally established by a cryptographic digest. It may exist in many
locations or byte-for-byte copies; copies with the same digest represent the
same Digital Artifact.

A **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records containing evidence of consequential
actions concerning a Digital Artifact. It is the protocol evidence structure,
not the artifact itself.

A **Digital Original** is a Digital Artifact for which consequential state has
been established through a Digital Controllable Record.

> Content makes an artifact identifiable. Consequential state makes it an
> original.

Copying content does not copy consequential state.

```text
Digital Artifact
  -> Digital Controllable Record
  -> consequential state derived according to protocol rules
  -> Digital Original
```

## Architectural Consequence

Most applications keep important state in a database: who controls a record,
whether a restriction applies, or whether a lifecycle has ended. When the
application disappears, that state may become inaccessible or impossible to
verify independently.

OpenETR uses a different boundary. Applications create and present signed
records that form a DCR. Cryptographic and structural checks validate the
evidence; defined protocol rules determine what consequential state follows.
An application can cache a projection for performance, but another conforming
implementation can reconstruct the same result from the evidence and rules.

```text
end-verifiable evidence -> OpenETR rules -> consequential state -> application projection
```

Actions have consequences. OpenETR represents consequential actions as
end-verifiable events and defines the rules by which those events change
consequential state.

> Applications derive consequential state; they do not own it.

## Making Consequences Portable

OpenETR can be summarized as an effort to **make consequences portable across
system boundaries**. That phrase does not mean that consequential state is
another object to copy or that one system's conclusion must bind every other
system. Consequential State remains a derived result.

What travels is the basis for reproducing that result:

```text
artifact identity + signed DCR evidence + identified rules
  -> reproducible consequential state
  -> contextual recognition
  -> external effect
```

The identity, authorization, approval, and delegation processes that caused an
organization to issue a consequential record may remain inside that
organization. A relying party need not reconstruct the entire upstream
authority model when the resulting record contains the evidence that its own
rules require.

This is a **what-first** boundary. The verifier begins by asking what artifact
and DCR are being presented, what state follows under the identified rules,
and what evidence is required for the proposed use. Actor identity, authority,
relationships, and other recognition evidence are introduced only to the
extent required by that use.

The portability claim is therefore precise:

> OpenETR makes the evidence and derivation of a consequential result
> portable. Recognition and effect remain contextual.

## End-Verifiable Events

An end-verifiable event carries enough portable evidence for a verifier to
check it without trusting the application that submitted or displayed it. In
the OpenETR Nostr profile, that includes the event body, public key, signature,
object reference, prior-event references, action, and required protocol tags.

Nostr provides the signed event substrate and relay transport. OpenETR defines
which events matter, how they relate, which transitions are valid, and what
state follows.

> Nostr carries the events. OpenETR determines their consequences.

## Applications Project State

An OpenETR application may maintain indexes, caches, and friendly views. These
are projections, not the authority for consequential state.

For each consequential state variable, the specification should identify:

1. the events that may change it;
2. the signing keys permitted to authorize those events;
3. the prior-state constraints;
4. the identified validation policy and transition rules;
5. the rules for conflict, supersession, and termination; and
6. the resulting state.

## Recognition Is A Separate Boundary

Consequential state derived under protocol rules does not compel recognition.
A law, contract, institution, community, or relying-party policy still decides
whether to accept the actor, graph, or state for a stated purpose and what
effect follows.

```text
consequential state -> recognition -> external effect
```

This separation lets OpenETR remain technically portable without pretending
that cryptography can decide institutional authority.

## Resilience Objective

The result is a deliberately application-independent architecture:

> System failure need not become state failure.

OpenETR's long-term objective is that Digital Originals—and the consequential
state associated with them—can outlive any particular application, database,
operator, or user interface.

For the normative design direction, see the
[Consequential State Architecture Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md).

For the broader records-first argument, see
[Maybe We Have Identity Backwards](https://trbouma.substack.com/p/maybe-we-have-identity-backwards).
