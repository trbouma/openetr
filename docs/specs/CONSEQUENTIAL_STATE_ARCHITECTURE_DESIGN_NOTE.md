# Consequential State Architecture Design Note

## Status

Draft architectural design note for OpenETR.

This note defines the architectural rule that should govern OpenETR state,
events, projections, and application boundaries.

## Core Principle

> Consequential state should be derived from end-verifiable events, not
> asserted solely by applications.

**Consequential State Architecture (CSA)** is an architectural approach in
which state affecting control, authority, rights, obligations, restrictions,
standing, or permitted actions is established and transitioned through signed,
independently verifiable events.

Applications may maintain projections of consequential state, but they are not
its sole authority:

> Applications interpret consequential state; they do not own it.

## Digital Artifacts And Digital Originals

A **Digital Artifact** is persistent digital content having a unique content
identity established by a cryptographic digest. It may exist in any number of
locations or byte-for-byte copies. Copies with the same protocol-defined digest
represent the same Digital Artifact.

A **Digital Original** is a Digital Artifact for which OpenETR can derive
consequential state from a relevant set of valid, end-verifiable events under
the applicable protocol rules.

This is a technical architecture definition. It does not claim that an
external institution, community, contract, or jurisdiction must recognize the
object or give its state legal or operational effect.

The central proposition is:

> Content makes an artifact identifiable. Consequential state makes it an
> original.

Consequential state may concern:

- current control;
- transfer;
- encumbrance;
- discharge;
- termination;
- delegation or authority;
- standing asserted or represented by a protocol profile; or
- another protocol-defined condition affecting what may be done with the
  object.

Copying content does not copy or alter consequential state. A byte-for-byte
copy with the same digest represents the same Digital Artifact, but possession
of the copy does not create a new controller or valid state transition.

## End-Verifiable Events

A consequential state transition **MUST** be represented by events that can be
verified independently of the application, platform, registry, or database
that produced, stored, transmitted, indexed, or displayed them.

An end-verifiable event must provide sufficient cryptographic and referential
evidence to determine:

1. which key signed the event;
2. which Digital Artifact and, where applicable, prior event it concerns;
3. which transition or assertion is being made;
4. whether the event is authentic and unaltered;
5. which prior state, signatures, guards, or events constrain it; and
6. how it participates in derivation of consequential state.

The durable primitive is not an application's state row. It is portable,
verifiable evidence of a state transition.

## Derived State

Consequential state is derived by applying OpenETR protocol rules to the
relevant valid event set:

```text
End-Verifiable Events
          |
          v
    Protocol Rules
          |
          v
  Consequential State
          |
   +------+------+ 
   |      |      |
   v      v      v
 App A  App B  System C
```

Independent conforming implementations receiving the same relevant valid
events **SHOULD** derive the same consequential protocol state.

Applications **MAY** maintain databases, indexes, caches, APIs, snapshots, and
materialized views. These are projections of consequential state rather than
its ultimate source of authority.

A projection must be reproducible or auditable from the event evidence and the
identified protocol or policy version used for derivation.

## Conflicts And Candidate State

End-verifiability does not eliminate conflicting events or incomplete event
sets. OpenETR must specify how a verifier handles:

- multiple candidate Anchor Events for the same object;
- competing branches;
- invalid signatures or malformed references;
- transitions made by a key lacking control under the prior derived state;
- unresolved or missing prior events;
- superseded events;
- terminated graphs; and
- events observed in different orders.

Chronology alone is not authority. Until protocol rules and any applicable
recognition policy resolve a conflict, a verifier should preserve candidate
graphs and describe the state as ambiguous, incomplete, or disputed rather
than silently selecting one.

## Recognition And Effect

Consequential state, recognition, and effect are distinct:

**Consequential State** is protocol state derived from end-verifiable events
that is capable of affecting control, authority, rights, obligations,
restrictions, standing, or permitted actions.

**Recognition** is acceptance of an actor, event, graph, object, or derived
state by a person, organization, institution, system, community, jurisdiction,
or applicable rule for a stated purpose.

**Effect** is the consequence produced when recognized state is given force or
acted upon.

```text
EVENT
  |
  v
CONSEQUENTIAL STATE
  |
  v
RECOGNITION
  |
  v
EFFECT
```

OpenETR can establish end-verifiable consequential state without claiming that
every external party or jurisdiction must recognize it or give it a particular
legal, institutional, contractual, community, or operational effect.

The term **recognized Digital Original** may be used when it is important to
state that a Digital Original and its consequential state have been accepted
under an identified recognition context. The unqualified technical term does
not imply universal recognition.

## Nostr As An Event Substrate

Nostr is a useful substrate for CSA because its primitive is a signed,
addressable, referential event. A Nostr event can carry evidence concerning:

- control;
- transfer;
- encumbrance;
- discharge;
- delegation;
- binding;
- termination;
- recognition; or
- another consequential relationship.

Events can reference objects and other events, allowing consequential state to
be represented as a verifiable event graph.

Relays transport and preserve evidence. They do not need to determine the
meaning or effect of that evidence. OpenETR defines the event grammar,
validation rules, and consequential state machine.

```text
Nostr   -> event substrate
OpenETR -> consequential state machine
```

Nostr is the current OpenETR technical binding, not the definition of CSA.
Another technical substrate could implement the same architectural rule if it
preserved portable end-verifiability and deterministic state derivation.

## Application Independence

Because consequential state is derived from end-verifiable events rather than
a particular application's database, the same state can be reconstructed
across applications and systems.

An application may disappear, become unavailable, change operators, or be
replaced without necessarily destroying the evidence required to reconstruct
state:

> System failure need not become state failure.

The Internet analogy is useful but should remain precise:

```text
TCP/IP routes packets around damaged connections.
Nostr can route evidence around damaged systems.
OpenETR lets conforming implementations derive state from that evidence.
```

State is not copied from one application's private database to another. Events
are transmitted and preserved; conforming applications independently derive
the applicable consequential state.

## OpenETR Layering

OpenETR should distinguish:

| Layer | Responsibility |
| --- | --- |
| Artifact Layer | Establish the unique content identity of persistent digital content. |
| Event Layer | Carry signed evidence concerning the artifact and transitions affecting it. |
| State Layer | Derive consequential state according to versioned OpenETR rules. |
| Recognition Layer | Determine which actors, graphs, objects, or states are accepted for a purpose. |
| Effect Layer | Apply legal, institutional, contractual, community, or operational consequences. |

The architecture can be summarized as:

```text
UNIQUE CONTENT
      |
      v
DIGITAL ARTIFACT
      |
      | end-verifiable events
      v
CONSEQUENTIAL STATE
      |
      v
DIGITAL ORIGINAL
      |
      v
  RECOGNITION
      |
      v
    EFFECT
```

## OpenETR Design Rule

For every state variable proposed for OpenETR, ask:

> Is this state consequential?

If it is consequential, the specification **SHOULD** identify:

1. which event or sequence of events establishes it;
2. which signing key or keys are permitted to produce those events;
3. which prior state, events, signatures, or guards constrain the transition;
4. how another implementation independently verifies the transition;
5. how conflicting, invalid, superseded, ambiguous, or terminated events are
   resolved; and
6. which consequential state results.

A consequential state field that cannot answer these questions should not be
treated as authoritative protocol state. It may instead be application
metadata, a cache, a hint, an unresolved assertion, or recognition-layer
input.

The protocol **SHOULD NOT** make consequential state depend solely upon an
application database row, mutable API response, private job status, or
operator-controlled projection.

## Relationship To C2PA

C2PA and OpenETR are complementary.

C2PA binds signed provenance assertions to content and describes creation,
transformation, ingredients, and publication history. OpenETR identifies the
Digital Artifact and derives consequential state from a portable control-event graph.
Recognition determines what effect a relying party gives both forms of
evidence.

```text
C2PA        -> explains the content and its provenance
OpenETR     -> explains consequential state and control
Recognition -> explains accepted meaning and effect
```

A valid C2PA Content Credential does not automatically create OpenETR
consequential state. It may be evidence referenced by an OpenETR event or an
input to recognition policy. Conversely, a valid OpenETR graph does not prove
that C2PA provenance assertions are true or trusted.

## Architectural Definition

> Consequential State Architecture is an architecture in which consequential
> state is derived from portable, end-verifiable evidence of state
> transitions, allowing that state to be independently reconstructed and
> interpreted across applications and systems.

For OpenETR:

> A Digital Artifact has uniquely identifiable content. A Digital Original is
> a Digital Artifact with consequential state.

The governing principle is:

> Move the evidence for consequential state out of applications and into
> end-verifiable events.

The objective is simple:

> Digital Originals should outlive applications.

## Specification Consequences

Future OpenETR specifications and reviews should:

- apply the OpenETR Design Rule to every consequential state field;
- distinguish raw events, valid events, derived state, recognition results,
  and external effect;
- identify the protocol and policy versions used to derive a projection;
- preserve conflicting candidate evidence rather than hiding it;
- make application caches and database projections explicitly non-authoritative;
- support export or retrieval of sufficient evidence for independent replay;
  and
- test that independent implementations derive equivalent state from the same
  event set.

## Related Notes

- [Digital Originality, Control, And Standing Design Note](./DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md)
- [OpenETR Nostr Wire Format Specification](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Provenance And Control Design Note](./PROVENANCE_AND_CONTROL_DESIGN_NOTE.md)
- [OpenETR And C2PA Design Note](./OPENETR_AND_C2PA_DESIGN_NOTE.md)
