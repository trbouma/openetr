# Digital Controllable Record Design Note

## Status

Draft canonical terminology and boundary note for OpenETR.

## Definition

A **Digital Controllable Record (DCR)** is a single end-verifiable record or a
graph of related end-verifiable records through which consequential state
concerning a Digital Artifact can be established and transitioned.

A DCR is not a file. The file or canonical content is the **Digital Artifact**.
The DCR is the signed evidence structure that concerns it.

```text
DIGITAL ARTIFACT
uniquely identifiable content
        |
        v
DIGITAL CONTROLLABLE RECORD
single record or record graph
        |
        v
CONSEQUENTIAL STATE
        |
        v
DIGITAL ORIGINAL
```

The canonical definitions are:

- A **Digital Artifact** is persistent digital content with a unique content
  identity, normally established by a cryptographic digest.
- A **Digital Controllable Record** establishes and transitions consequential
  state concerning a Digital Artifact.
- A **Digital Original** is a Digital Artifact with consequential state.

> Content makes an artifact identifiable. Consequential state makes it an
> original.

## Structure

A DCR may contain one record or a directed graph of records expressing:

- origin or issuance;
- control and transfer;
- encumbrance and discharge;
- provenance or attestation;
- delegation;
- surrender, redemption, or termination; or
- another protocol-defined consequential relationship.

The DCR is evidence. A conforming implementation validates that evidence and
derives consequential state from it under identified, versioned protocol
rules. An application may cache the result, but the cache is not the authority.

Every displayed consequential state should therefore be traceable to the DCR
record or records that produced it.

## Claims And Recognition

A provenance claim (“I created this artifact”) is distinct from an authority
claim (“I recognize or certify this artifact for purpose X”). OpenETR can show
who signed either claim and which artifact it concerns. Whether the signer has
recognized standing or authority is a recognition-layer question.

Cryptographic validity does not itself create legal or institutional effect:

```text
DCR EVENT
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

## Legal Boundary

**Digital Controllable Record** is an OpenETR protocol construct. It is not a
synonym for the **Controllable Electronic Record** defined by UCC Article 12.
A DCR may qualify as a CER, electronic transferable record, negotiable cargo
document, or another legally recognized record where the applicable legal
requirements are satisfied.

Domain profiles may define the additional rules needed for bills of lading,
warehouse receipts, or other instruments. They should not encode legal
classification into the generic DCR merely by naming it.

## Nostr Binding

Nostr provides signed events, identifiers, references, keys, relay transport,
and redundant distribution. OpenETR defines event semantics, authorization,
transition rules, conflict handling, and state derivation.

> Nostr provides the event substrate. OpenETR defines the consequential state
> machine.

Relays preserve and transport DCR evidence. They do not determine OpenETR
state.

## Application Boundary

Implementations should separate:

```text
ARTIFACT         digest + content
DCR              signed end-verifiable records or graph
STATE PROJECTION derived consequential state
```

The state projection should be produced through one versioned derivation
boundary conceptually equivalent to:

```text
derive_state(artifact_id, dcr_records) -> ConsequentialState
```

If the answer to “Why is this state true?” is only “because the application
database says so,” the implementation is not aligned with Consequential State
Architecture.

## Copying And Originality

Byte-identical files with the same digest represent the same Digital Artifact.
Copying those bytes does not create another DCR and does not independently
reproduce consequential state.

> A copy can reproduce content. It cannot independently reproduce
> consequential state.

## Governing Rules

- Consequential state should be derived from end-verifiable events, not
  asserted by applications.
- Applications interpret consequential state; they do not own it.
- Recognition determines the effect given to consequential state.
- System failure need not become state failure.
- Digital Originals should outlive applications.

## Terminology Migration

The canonical and public OpenETR surfaces use the model in this note. Some
older domain-adapter and comparison drafts may still use **Controlled Object**
for the digest-identified artifact. In those drafts, the term should be read as
**Digital Artifact** until the document receives a contextual migration. It
must not be mechanically reinterpreted as DCR, because a DCR is the signed
record or graph, not the file.
