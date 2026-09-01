# Digital Originality, Control, And Standing Design Note

## Status

Draft design note.

## Purpose

This note captures a core design decision for OpenETR and related applications:
a Digital Artifact becomes a Digital Original, in the OpenETR technical sense,
when its DCR is validated under an applicable policy and that validation
establishes consequential state. Recognition accepts that result for a stated
purpose and determines external effect.

The central distinction is:

> Digital originality is about consequential state, not copy prevention.

OpenETR implements this distinction through Consequential State Architecture.
Copying bytes does not copy control, satisfy transition guards, or create a
valid state transition. A relying party still decides whether to recognize the
derived state and what effect to give it.

Within that architecture, OpenETR represents consequential actions as
end-verifiable events and defines the state transition rules by which those
events change consequential state.

## Core Thesis

In a digital environment, perfect copies are normal. Originality therefore
cannot be treated as a natural property of one physical instance of the bytes.
The content identifies the artifact; end-verifiable events establish its
consequential state.

The working thesis is:

> A Digital Artifact has uniquely identifiable content. A Digital Original is
> a Digital Artifact with consequential state.

This gives five separate layers:

| Layer | Question | Example |
| --- | --- | --- |
| Artifact | What exact persistent content is identified? | A PDF, scan, JSON document, image, or structured record identified by digest. |
| DCR | What signed record or record graph exists? | Anchor, transfer, encumber, discharge, terminate. |
| State transition rules and consequential state | What state results when the DCR is evaluated under the identified policy? | Current controller, active guards, lifecycle state, candidate branches. |
| Recognition | Which actor, graph, object, or state is accepted for a stated purpose? | A verifier recognizes a warehouse operator or candidate graph. |
| Effect | What consequence follows from recognized state? | Treated as an authoritative copy, transferable record, official record, or evidentiary record. |

Policy validation of the DCR can establish consequential state. It cannot
compel external recognition or effect.

## Definitions

### Digital Artifact

A Digital Artifact is persistent digital content having a unique content
identity established by a cryptographic digest. It may be stored, copied,
referenced, transmitted, or rendered without those operations changing its
identity or consequential state. Byte-for-byte copies with the same digest
represent the same Digital Artifact.

### Digital Controllable Record

A Digital Controllable Record (DCR) is one end-verifiable record or a graph of
related end-verifiable records through which consequential state concerning a
Digital Artifact can be established and transitioned. It is the signed
protocol evidence structure, not the artifact itself.

Digital Controllable Record is the preferred protocol term for this evidence
layer. It is not a synonym for the file or for a legally recognized
Controllable Electronic Record under UCC Article 12.

### Digital Original

A Digital Original is a Digital Artifact for which consequential state has
been established by validating its DCR under an applicable policy.

This is a technical architecture term. A **recognized Digital Original** is a
Digital Original whose actor, graph, object, or derived state has also been
accepted under an identified recognition context for a stated purpose.

The term is used here as a conceptual term, not as a claim that every legal regime uses the same vocabulary. Some regimes may instead refer to an authoritative electronic copy, an electronic transferable record, a controllable electronic record, an official electronic record, or another domain-specific category.

### Authority

An Authority is an actor that makes an assertion relevant to the object or its control state. In OpenETR this may be visible as the signer of an Anchor Event, a controller, a domain system, or another actor in the control graph.

OpenETR can verify that a cryptographic key made a signed assertion. It does not decide, by itself, whether that actor has real-world authority for a given purpose.

### Recognition

Recognition remains relational and contextual:

> A relying party, institution, community, or legal regime recognizes an actor, assertion, object, or control state for a particular purpose.

The important question is not only whether an object was anchored or signed. The question is whether the relevant authority is recognized for the relevant purpose.

### Standing

Standing may be asserted in a DCR, derived by validation, or accepted through
recognition. A validation policy may produce a standing-related state, but
**recognized standing** exists only when a recognition context accepts that
state for a purpose.
Examples include official copy, evidentiary copy, transferable record, retired
record, cancelled record, or non-authoritative copy.

Policy validation of DCR evidence can establish consequential state.
Recognition determines whether a relying party accepts that state and what
effect follows.

### Effect

Effect is the consequence that law, policy, contract, institutional rules, community governance, or another recognition regime gives to a recognized object, state, or action.

Rules determine effect.

## What Does Not Create Consequential State

The following actions do not independently create OpenETR consequential state:

- Scanning a physical document.
- Hashing a digital file.
- Signing a digest outside a protocol-valid state transition.
- Timestamping a record.
- Storing a record in a repository.
- Anchoring a digest in a system that does not define the resulting state.
- Publishing a malformed, invalid, unauthorized, or unlinked control event.
- Placing a file in a digital wallet.

Each may help establish integrity, authenticity, provenance, or persistence.
A valid OpenETR Anchor Event forms a one-record DCR. Validation of that DCR
under an applicable policy can establish initial consequential state. That
makes the identified Digital Artifact a
Digital Original in the technical OpenETR sense, while recognition and effect
remain unresolved.

Useful shorthand:

- Hashing establishes integrity, not originality.
- Signing establishes an assertion, not necessarily authority.
- Arbitrary anchoring establishes a reference point, not consequential state.
- Validation of a one-record Anchor DCR under an applicable policy may
  establish candidate consequential state, not universal recognition.
- Control transitions are consequential because conforming implementations can
  derive state from them.
- Digital originality is not a uniqueness property of the bytes.

## The Control Layer

The term Control Layer should be retained and used precisely:

> The Control Layer is an expressive grammar for describing control state, governing valid state transitions, and establishing or removing guards upon those transitions, independent of any particular technical binding.

The Control Layer has two jobs:

- Describe control state.
- Govern valid control-state transitions.

It lets a system express statements such as:

- A anchors object X.
- B controls object X.
- B transfers object X to C.
- B encumbers object X.
- An encumbrance on object X is discharged.
- Object X is terminated.

The Control Layer does not decide whether A is legally empowered to make X an official record. It does not decide whether B is a licensed warehouse operator. It does not perform KYC. It does not create recognition. Those matters belong to domain systems and recognition regimes.

## Grammar And Technical Binding

The Control Layer is a grammar. A technical binding is an implementation of that grammar.

| Concept | Role |
| --- | --- |
| Control Layer grammar | Defines what can be meaningfully expressed. |
| Technical binding | Defines how those statements are represented, signed, linked, published, and verified. |
| Recognition context | Determines whether an actor, assertion, object, or state is accepted for a purpose. |
| Applicable rules | Determine the legal, institutional, contractual, or community effect. |

For example:

```text
Controller -> TRANSFER -> New Controller
```

The Control Layer says that transfer is a meaningful state transition. A Nostr binding can specify the event kind, signed structure, object references, controller keys, prior event references, validation rules, and relay publication model.

In short:

```text
Control Layer != Nostr
OpenETR Control Layer -> Nostr binding
```

OpenETR should therefore not be described only as a wire protocol. It defines and implements a control layer that can be bound to one or more technical protocols.

## Control Primitives

The minimal control primitive set is:

- Anchor.
- Transfer.
- Encumber.
- Discharge.
- Terminate.

### Anchor

Anchor creates the first candidate DCR record for a Digital Artifact. It
provides a technical reference point and a starting point for the control
graph.

When the one-record DCR is validated under an applicable policy, it may produce
initial consequential state for a candidate control graph. It may therefore
bring the identified Digital Artifact into the Digital Original model.
It does not establish that its candidate graph is uniquely authoritative,
recognized, or legally effective. Earlier terminology such as Original Event
should still be avoided because the event is an anchor, not a declaration of
universal authority.

A single object or digest may have multiple Anchor Events. Different recognition contexts may recognize different anchoring authorities for different purposes.

### Transfer

Transfer changes the controller of a controlled Digital Artifact, subject to the current state and any applicable transition guards.

Transfer describes a control-state change. It does not, by itself, describe the legal or institutional meaning of the transfer.

### Encumber

Encumber establishes a guard on subsequent control-state transitions.

An encumbrance may represent a pledge, lien, hold, policy restriction, approval requirement, pending obligation, domain-specific lock, or other condition that must be satisfied before certain transitions are valid.

### Discharge

Discharge removes or deactivates a guard previously established by an encumbrance.

Discharge is preferred over release as the generic control primitive because it maps more naturally to obligations, liens, holds, and other state-transition constraints.

### Terminate

Terminate ends the active control state of the object.

Termination may represent cancellation, retirement, destruction of control status, replacement, expiry, or another domain-specific end state, depending on the recognition context and applicable rules.

## Transition Guards

Transition guards are conditions arising from the current control state that determine whether a proposed control-state transition is valid.

Encumber and Discharge are the Control Layer transitions that establish and remove those guards:

```text
ENCUMBER  -> creates or activates a guard
DISCHARGE -> removes or deactivates a guard
TRANSFER  -> must satisfy applicable guards
TERMINATE -> must satisfy applicable guards
```

This keeps the model simple. Encumbrances are not merely metadata. They affect whether later control-state transitions are valid.

## Effect Primitives

Control primitives describe what happens to control. Effect primitives describe what it means.

The generic effect vocabulary is:

- Recognition.
- Standing.
- Relinquishment.

These are not primitive control-state transitions. They may accept, interpret,
or give consequence to derived state, but they belong to recognition and
effect policy rather than the base event grammar.

### Recognition

Recognition is the acceptance of an actor, assertion, object, or control state for a particular purpose.

For example, a verifier may recognize a licensing authority as authoritative for driver licences, a warehouse operator as authoritative for warehouse receipts, or a community governance body as authoritative for a community record.

### Standing

Standing is status asserted or derived for the Digital Artifact. A relying
party's recognition context determines whether it accepts that standing and
the applicable rules determine its effect.

For example, a controlled Digital Artifact may be recognized as the original warehouse receipt, an authoritative electronic copy, an official municipal record, or a non-authoritative copy.

### Relinquishment

Relinquishment means that a party gives up a recognized claim, right, position, or control-related status associated with the object.

Surrender is a domain-specific form of relinquishment. It may be positive, as when a transferable record is surrendered after payment or discharge of an obligation. It may also raise concern, as when a person is required to surrender a passport or other credential to an authority that may revoke or retain it.

The Control Layer may represent surrender through one or more control transitions, such as:

```text
Surrender intent or effect
  -> Transfer to authority
  -> Possible termination
```

Transfer describes the control-state change. Surrender or relinquishment describes the real-world meaning around that change.

## Consequential State Pipeline

The model is best understood as a derivation pipeline with a separate external
effect path:

```text
Digital Artifact
  -> Digital Controllable Record
  -> OpenETR state transition rules
  -> Consequential state
  -> Digital Original
  -> Recognition
  -> Effect

Control events: Anchor -> Transfer -> Encumber -> Discharge -> Terminate
```

End-verifiable events make the object's consequential state independently
derivable. Recognition and effect determine what external parties do with that
state.

## Example: Driver's Licence

A physical driver's licence can be scanned into a file. That scan becomes a
Digital Artifact when its canonical bytes are bound to a protocol-defined
digest. It can be signed, timestamped, stored, copied, and anchored without a
particular file instance becoming uniquely original.

They do not, by themselves, establish OpenETR consequential state for the scan.

The scan becomes a Digital Original in the technical OpenETR sense when its DCR
is validated under an applicable policy and produces consequential state. It becomes a recognized
Digital Original for a licensing purpose only if a competent licensing
authority or relevant recognition regime accepts the actor, graph, object, and
derived state for that purpose.

The sequence is:

```text
Physical licence
  -> Scan
  -> Digital Artifact
  -> candidate Digital Controllable Record (Anchor)
  -> Digital Original
  -> Recognition by competent authority
  -> Recognized standing and effect
```

This also allows physical and digital originals to coexist. OpenETR's technical
definition does not pretend that a physical original disappeared or require a
jurisdiction to accept the Digital Artifact. It requires clarity about derived
state, recognition context, standing, and purpose.

## Community And Institutional Records

The same model applies outside formal state-issued credentials.

A community archive, Indigenous government, municipality, church, historical society, corporation, standards body, or trade association may recognize particular records for particular purposes. OpenETR can make that recognition digitally expressible, verifiable, and durable, but it does not manufacture the authority of the recognizing body.

A useful formulation is:

> The community recognizes the record. OpenETR makes that recognition digitally expressible, verifiable, and durable.

This matters because many records have authority before they are digitized. The design goal is not to replace that authority with cryptography. The design goal is to preserve and express the connection between control, recognition, and consequence in a digital environment.

## Relationship To Legal Terminology

Digital Original is not proposed here as a universal legal term. Different regimes use different concepts.

Relevant adjacent language includes:

- MLETR's functional equivalence approach for electronic transferable records, including integrity, singularity, and control.
- UCC terminology such as authoritative electronic copy and controllable electronic record.
- UK ETDA concepts of exclusive control and reliable systems.
- Digital preservation uses of digital original and born-digital original.
- Domain-specific official record, title document, receipt, bill, certificate, permit, passport, licence, or credential terminology.

OpenETR can use Digital Original as a carefully defined conceptual term while mapping that concept to domain-specific legal language where necessary.

## Relationship To Check, Present, Share, And Surrender

The graduated disclosure vocabulary remains useful:

- Check.
- Present.
- Share.
- Surrender.

Those interaction modes become more meaningful when consequential state is
visible and recognition is stated separately. Checking a Record File verifies
content and event evidence. Presenting a Digital Original exposes its derived
state without transferring it. Sharing discloses the Record File and evidence
without copying control. Surrender may relinquish control, recognized status,
or both under a domain profile.

However, Surrender should not be treated as the generic primitive in the Control Layer. At the generic layer, Relinquishment is the effect concept. Domain profiles can define surrender as a specific form of relinquishment and map it to one or more control transitions.

## Product Naming Implications

The naming distinction should remain consistent across user-facing products and protocol documents:

- Mainstay Register is the preferred functional name for the Mainstay registration or notary capability.
- VouchSafe is the preferred name for a generic user-facing application that uses OpenETR to register existing records or digital forms as Digital Originals.
- Strata should be reserved as a possible future application name, suggesting layers of evidence and history.

Preferred language:

> VouchSafe uses OpenETR to register records as Digital Originals.

Use caution with VouchSafe etymology. The historical meaning of vouchsafe is closer to grant, concede, or bestow. The product resonance is vouch plus safe, but documentation should not claim that the historical word literally meant to vouch for and keep safe.

## Design Implications For OpenETR

1. Use Anchor Event rather than Original Event where the protocol event establishes an initial anchored control state.
2. Allow more than one Anchor Event for the same object or digest.
3. Preserve the distinction between consequential protocol state, recognition, and effect.
4. Keep the Control Layer independent from any single technical binding.
5. Treat Nostr as a technical binding for the Control Layer, not as the Control Layer itself.
6. Model encumbrances as transition guards.
7. Keep Recognition, Standing, and Relinquishment in the effect layer, not as primitive control transitions.
8. Ensure verifier output distinguishes integrity, authenticity, event validity, consequential state, recognition, standing, and effect.
9. Avoid implying that OpenETR performs KYC, creates legal authority, determines institutional recognition, or substitutes for a reliable system where law or policy requires one.

## Specification Language

The following language can be reused in future specs:

**Digital Artifact:** Persistent digital content having a unique content
identity established by a cryptographic digest. Byte-for-byte copies with the
same digest represent the same Digital Artifact.

**Digital Controllable Record:** One end-verifiable record or a graph of
related end-verifiable records through which consequential state concerning a
Digital Artifact can be established and transitioned.

**Control Layer:** An expressive grammar for describing control state, governing valid state transitions, and establishing or removing guards upon those transitions, independent of any particular technical binding.

**Technical Binding:** A concrete representation of Control Layer statements in a signed, verifiable, publishable, and machine-processable form.

**Transition Guard:** A condition arising from the current control state that determines whether a proposed control-state transition is valid.

**Digital Original:** A Digital Artifact for which consequential state has
been established by validating its DCR under an applicable policy.

**Consequential State:** The result of validating end-verifiable DCR evidence
under an identified policy. The result is capable of affecting control,
authority, rights, obligations, restrictions, standing, or permitted actions
when it is recognized for a stated purpose.

**Recognition:** The acceptance of an actor, assertion, object, or control state by a relying party, institution, community, or legal regime for a particular purpose.

**Standing:** Status asserted or derived for a Digital Original; recognized
standing is that status accepted under an identified recognition context for a
stated purpose.

**Effect:** The consequence that law, policy, contract, institutional rules, community governance, or another recognition regime gives to a recognized object, state, or action.

**Relinquishment:** A party giving up a recognized claim, right, position, or control-related status associated with a Digital Artifact.

## Open Questions

- Which existing documents and implementation terms should be migrated from Original Event to Anchor Event?
- How should public material distinguish the technical term Digital Original from a recognized Digital Original in a specific domain?
- How should verifier interfaces visually distinguish protocol validity from recognized standing?
- How should domain adapters express the recognition regime that gives a Digital Original standing?
- Which state variables in each domain profile pass the Consequential State Architecture design rule?
- Which domain profiles require an explicit surrender operation, and which should model relinquishment through existing transfer, discharge, or terminate transitions?

## Related Notes

- [Provenance And Control Design Note](./PROVENANCE_AND_CONTROL_DESIGN_NOTE.md)
- [Consequential State Architecture Design Note](./CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [Control Event Policy Guards Design Note](./CONTROL_EVENT_POLICY_GUARDS_DESIGN_NOTE.md)
- [OpenETR Generic Domain Adapter Specification](./OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Warehouse Receipt Pilot Boundary Notes](./MLWR_WAREHOUSE_RECEIPT_PILOT_BOUNDARY_NOTES.md)
