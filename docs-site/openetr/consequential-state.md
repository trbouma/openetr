# Consequential State

OpenETR is designed around one governing principle:

> Consequential state should be derived from end-verifiable events, not
> asserted solely by applications.

## Digital Artifact, Digital Controllable Record, And Digital Original

A **Digital Artifact** is persistent digital content with a unique content
identity established by a cryptographic digest. It may exist in many locations
or byte-for-byte copies; copies with the same digest represent the same Digital
Artifact.

A **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records concerning a Digital Artifact. It is
the signed evidence structure, not the artifact itself.

A **Digital Original** is a Digital Artifact with consequential state
established through a valid DCR under the applicable protocol rules.

> Content makes an artifact identifiable. Consequential state makes it an
> original.

Copying content does not copy consequential state.

```text
Digital Artifact
  -> Digital Controllable Record
  -> OpenETR rules
  -> consequential state
  -> Digital Original
```

## Why This Matters

Most applications keep important state in a database: who controls a record,
whether a restriction applies, or whether a lifecycle has ended. When the
application disappears, that state may become inaccessible or impossible to
verify independently.

OpenETR uses a different boundary. Applications create and present signed
events. Protocol rules derive the resulting state. An application can cache a
projection for performance, but another implementation can reconstruct the
same result from the evidence.

```text
event -> protocol rules -> consequential state
```

## End-Verifiable Events

An end-verifiable event carries enough portable evidence for a verifier to
check it without trusting the application that submitted or displayed it. In
the OpenETR Nostr profile, that includes the event body, public key, signature,
object reference, prior-event references, action, and required protocol tags.

Nostr provides the signed event substrate and relay transport. OpenETR defines
which events matter, how they relate, which transitions are valid, and what
state follows.

## Applications Project State

An OpenETR application may maintain indexes, caches, and friendly views. These
are projections, not the sole source of truth.

For each consequential state variable, the specification should identify:

1. the events that may change it;
2. the signing keys permitted to authorize those events;
3. the prior-state constraints;
4. the deterministic verification procedure;
5. the rules for conflict, supersession, and termination; and
6. the resulting state.

## Recognition Is A Separate Boundary

Derivable protocol state does not compel recognition. A law, contract,
institution, community, or relying-party policy still decides whether to
accept the actor, graph, or state for a stated purpose and what effect follows.

```text
protocol-valid state -> recognition -> external effect
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
