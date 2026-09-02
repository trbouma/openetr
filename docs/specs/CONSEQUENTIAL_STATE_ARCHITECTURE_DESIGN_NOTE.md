# Consequential State Architecture Design Note

## Status

Draft architectural design note for OpenETR.

This note defines the architectural rule that should govern OpenETR state,
events, projections, and application boundaries.

## Core Principle

> Consequential state should be derived from end-verifiable evidence according
> to defined rules, not merely asserted by applications, databases or
> blockchains.

**Consequential State Architecture (CSA)** is an architectural approach in
which signed, independently verifiable records form a DCR spanning an
artifact's evidenced lifecycle. Validation checks that evidence, and defined
rules derive state affecting control, authority, rights, obligations,
restrictions, standing, or permitted actions.

Applications may maintain projections of consequential state, but they are not
its sole authority:

> Applications derive consequential state; they do not own it.

## Digital Artifacts, Controllable Records, And Digital Originals

A **Digital Artifact** is persistent digital content having a unique content
identity established by a cryptographic digest. It may exist in any number of
locations or byte-for-byte copies. Copies with the same protocol-defined digest
represent the same Digital Artifact.

A **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records through which consequential state
concerning a Digital Artifact can be established and transitioned. A DCR is
the protocol evidence structure, not the file or content that it concerns.

A **Digital Original** is a Digital Artifact for which consequential state has
been established by validating its DCR under an applicable policy.

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

The canonical relationship is:

```text
DIGITAL ARTIFACT
uniquely identifiable content
        |
        | referenced by
        v
DIGITAL CONTROLLABLE RECORD
single record or record graph spanning the evidenced lifecycle
        |
        | evaluated by
        v
STATE TRANSITION RULES
protocol-defined transition rules
        |
        | derive
        v
CONSEQUENTIAL STATE (validation result)
        |
        | establishes
        v
DIGITAL ORIGINAL
```

Creation, scanning, translation, rendering, or transformation may produce a
new Digital Artifact. Novelty alone does not make it a Digital Original:

> Creation produces a Digital Artifact. Consequential state makes that
> artifact a Digital Original.

A creator may make a provenance claim such as “I created this artifact.” An
issuer or other authority may make a different claim such as “I certify this
artifact as authoritative for purpose X.” OpenETR establishes who signed the
claim and which artifact it concerns. Recognition of the signer's standing or
authority remains a separate determination.

## Digital Controllable Record

A DCR may consist of:

- one end-verifiable record;
- multiple related records; or
- a directed graph of control, transfer, encumbrance, discharge, provenance,
  delegation, termination, or related events.

The graph is evidence. Validation checks the DCR graph as a whole, and defined
state transition rules derive current consequential state from the valid
evidence. The DCR therefore spans the signed evidence lifecycle between
content identity and state evaluation; it must not be used as a synonym for the
Digital Artifact itself.

**Digital Controllable Record** is an OpenETR protocol term. It is not legally
synonymous with a **Controllable Electronic Record (CER)** under UCC Article
12. A DCR may qualify as a CER, electronic transferable record, negotiable
cargo document, or another legally recognized record only where the applicable
legal requirements are satisfied.

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
6. how it participates in policy validation of the DCR and the resulting
   consequential state.

The durable primitive is not an application's state row. It is portable,
verifiable evidence of a state transition.

## State Transition Rules

OpenETR uses ordinary state transition rules to determine how valid
consequential actions change consequential state.

```text
CURRENT CONSEQUENTIAL STATE
        |
        | consequential action
        | evidenced by signed event
        v
TRANSITION RULE
        |
        v
NEW CONSEQUENTIAL STATE
```

A consequential action is an action capable of producing a protocol-defined
change in consequential state. OpenETR control primitives include:

- Anchor;
- Transfer;
- Encumber;
- Discharge;
- Terminate.

Domain profiles may define additional actions or effect concepts such as
relinquishment, surrender, redemption, amendment, cancellation, or replacement.
Those profiles should state whether the concept is a state transition, a
domain interpretation of one or more transitions, or an external recognition
effect.

Consequential actions deserve durable, end-verifiable evidence. A conforming
implementation should be able to determine from the DCR and identified policy:

1. the prior consequential state;
2. the consequential action asserted by the event;
3. whether the signing key was permitted to make that transition;
4. whether transition guards were satisfied;
5. whether the event links coherently into the relevant DCR graph; and
6. the new consequential state, if the transition is valid.

## Derived State

Consequential state is produced by validating the relevant DCR record or graph
under an identified policy and applying the relevant state transition rules.
The policy includes the applicable OpenETR protocol rules and any stated
profile constraints needed for that evaluation:

```text
DCR Record Or Graph + Identified Policy
          |
          | validate and apply state transition rules
          v
  Consequential State (result)
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

A projection must be reproducible or auditable from the DCR evidence and the
identified policy version used for validation.

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
DCR OR DCR GRAPH + DEFINED RULES
  |
  | validate evidence and derive state
  v
CONSEQUENTIAL STATE (result)
  |
  v
RECOGNITION
  |
  v
EFFECT
```

OpenETR can derive consequential state from end-verifiable DCR evidence
according to defined rules without claiming that
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
validation rules, and state transition rules.

```text
CONSEQUENTIAL ACTION
        |
        v
NOSTR EVENT
signed evidence
        |
        v
NOSTR RELAYS
transport and preserve
        |
        v
OPENETR RULES
validate and derive state
        |
        v
CONSEQUENTIAL STATE
```

Nostr carries the events. OpenETR determines their consequences.

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
| DCR Layer | Carry the signed, end-verifiable record or record graph concerning the artifact. |
| State Layer | Validate the DCR under an identified, versioned policy and expose the resulting consequential state. |
| Recognition Layer | Determine which actors, graphs, objects, or states are accepted for a purpose. |
| Effect Layer | Apply legal, institutional, contractual, community, or operational consequences. |

The architecture can be summarized as:

```text
UNIQUE CONTENT
      |
      v
DIGITAL ARTIFACT
      |
      | referenced by
      v
DIGITAL CONTROLLABLE RECORD
      |
      | validate as a whole under an identified policy
      v
CONSEQUENTIAL STATE (validation result)
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
Digital Artifact and validates its portable DCR graph under an applicable
policy to produce consequential state.
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

For every feature, reviewers should also ask:

1. What is the Digital Artifact and which digest identifies it?
2. What DCR record or graph establishes the relevant state?
3. Who is authorized to produce those records, and what prior state constrains
   the transition?
4. Can another implementation reproduce the same state and trace it to
   inspectable evidence?
5. Is recognition being confused with protocol state?
6. Would the consequential state survive if the originating application
   disappeared?

## Related Notes

- [Digital Originality, Control, And Standing Design Note](./DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md)
- [OpenETR Nostr Wire Format Specification](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Provenance And Control Design Note](./PROVENANCE_AND_CONTROL_DESIGN_NOTE.md)
- [OpenETR And C2PA Design Note](./OPENETR_AND_C2PA_DESIGN_NOTE.md)
