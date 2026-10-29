# Evidence Graph Design Note

## Status

Draft canonical terminology and boundary note for OpenETR.

Updated 29 October 2026: **Evidence Graph** replaces **Digital Controllable
Record (DCR)** as the primary model term. This note retains its existing
filename so published links continue to work.

## Definition

An **Evidence Graph** is a single end-verifiable record or a
graph of related end-verifiable records through which consequential state
concerning a Digital Artifact can be established and transitioned.

An Evidence Graph is not a file. The file or canonical content is the **Digital Artifact**.
The Evidence Graph is the signed evidence structure that concerns it.

```text
DIGITAL ARTIFACT
uniquely identifiable content
        |
        v
EVIDENCE GRAPH
single record or record graph spanning the evidenced lifecycle

Evidence Graph + IDENTIFIED RULESET
        |
        | validation and state transition rules
        v
CONSEQUENTIAL STATE -> RECOGNITION -> EFFECT

DIGITAL ARTIFACT + ESTABLISHED CONSEQUENTIAL STATE
        |
        v
DIGITAL ORIGINAL
```

The canonical definitions are:

- A **Digital Artifact** is persistent digital content with a unique content
  identity, normally established by a cryptographic digest.
- An **Evidence Graph** is the signed evidence structure from which
  defined rules derive consequential state concerning a Digital Artifact after
  the evidence is validated.
- A **Digital Original** is a Digital Artifact with consequential state.

> Content makes an artifact identifiable. Consequential state makes it an
> original.

## Structure

An Evidence Graph may contain one record or a directed graph of records expressing:

- anchoring or issuance assertions;
- control and transfer;
- encumbrance and discharge;
- provenance or attestation;
- delegation;
- surrender, redemption, or termination; or
- another protocol-defined consequential relationship.

The Evidence Graph is evidence. A conforming implementation evaluates the record or graph
as a whole under an identified, versioned ruleset. Consequential
state is the result of that evaluation, not another record beside the Evidence Graph. An
application may cache the result, but the cache is not the authority.

Every displayed consequential state should therefore be traceable to the Evidence Graph
record or records that produced it.

The Evidence Graph records the consequential actions. State transition rules determine
their consequences.

```text
Consequential Action
        |
        v
End-verifiable event
        |
        v
Evidence Graph record or graph
        |
        v
Identified, versioned ruleset
        |
        v
Consequential State
```

## Claims And Recognition

A provenance claim (“I created this artifact”) is distinct from an authority
claim (“I recognize or certify this artifact for purpose X”). OpenETR can show
who signed either claim and which artifact it concerns. Whether the signer has
recognized standing or authority is a recognition-layer question.

Cryptographic validity does not itself create legal or institutional effect:

```text
EVIDENCE GRAPH + IDENTIFIED RULESET
    |
    | validation
    v
CONSEQUENTIAL STATE (result)
    |
    v
RECOGNITION
    |
    v
EFFECT
```

## Legal Boundary

**Evidence Graph** is an OpenETR protocol construct. It is not a
synonym for the **Controllable Electronic Record** defined by UCC Article 12.
An Evidence Graph may qualify as a CER, electronic transferable record, negotiable cargo
document, or another legally recognized record where the applicable legal
requirements are satisfied.

Domain profiles may define the additional rules needed for bills of lading,
warehouse receipts, or other instruments. They should not encode legal
classification into the generic Evidence Graph merely by naming it.

## Nostr Binding

Nostr provides signed events, identifiers, references, keys, relay transport,
and redundant distribution. OpenETR defines event semantics, authorization,
transition rules, conflict handling, and state derivation.

> Nostr carries the events. OpenETR determines their consequences.

Relays preserve and transport Evidence Graph records. They do not determine OpenETR
state.

## Application Boundary

Implementations should separate:

```text
ARTIFACT         digest + content
Evidence Graph              signed end-verifiable records or graph
STATE PROJECTION state derived from validated Evidence Graph records under defined rules
```

The state projection should be produced through one versioned derivation
boundary conceptually equivalent to:

```text
evaluate_evidence_graph(artifact_id, evidence_records, policy_id) -> ConsequentialState
```

If the answer to “Why is this state true?” is only “because the application
database says so,” the implementation is not aligned with Consequential State
Architecture.

## Copying And Originality

Byte-identical files with the same digest represent the same Digital Artifact.
Copying those bytes does not create another Evidence Graph and does not independently
reproduce consequential state.

> A copy can reproduce content. It cannot independently reproduce
> consequential state.

## Governing Rules

- Consequential state should be derived from end-verifiable evidence according
  to defined rules, not merely asserted by applications, databases or
  blockchains.
- Applications derive consequential state; they do not own it.
- Recognition determines the effect given to consequential state.
- System failure need not become state failure.
- Digital Originals should outlive applications.

## Terminology Migration

Evidence Graph replaces Digital Controllable Record (DCR), not Digital Artifact.
The artifact remains the byte-identified content; the graph is the signed
evidence concerning it. A single anchor can form a one-node candidate graph.
Later events add evidence, not necessarily a control transition. The Control
Graph remains the subset used by a ruleset to derive control consequences.

This is a terminology migration, not a wire-format or runtime API migration.
Existing event kinds, tags, signed bytes, event IDs, and protocol behaviour
remain unchanged. Legacy filenames and published URLs are retained for
compatibility. The conceptual function above is illustrative, not an API name.

The minimum defined baseline is [OpenETR Core Record Ruleset
1.0](./OPENETR_CORE_RECORD_RULESET_1_0.md). It derives anchored state and a
Publisher Position from an Anchor Event and qualifying Publisher Notices.
Transfer, Current Controller, encumbrance, discharge, and similar state require
an additional ruleset.
