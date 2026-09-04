# Records-First Authenticity And Digital Originality Design Note

## Status

Draft conceptual design note, 4 September 2026.

## Purpose

This note explains why OpenETR uses a records-first approach to authenticity
and digital originality. It places that decision in historical context while
preserving a clear boundary between historical analogy, technical evidence,
institutional recognition, and legal effect.

The central thesis is:

> A Digital Original is not one privileged copy of a file. It is an exact
> Digital Artifact whose consequential state can be independently derived
> from authentic records.

The shorthand is:

> Copies are plural; consequential state is singular.

This is not a claim that every legal regime must use the term Digital Original
or give an OpenETR record a particular effect. OpenETR supplies independently
verifiable evidence and defined state-transition rules. Recognition regimes
decide which actors, records, and derived states they accept and what follows.

## Design Decision

OpenETR begins with the record rather than requiring a resolved institutional
identity as the gateway to the record:

```text
exact Digital Artifact
  -> attributable signed events concerning it
  -> Digital Controllable Record
  -> state-transition rules
  -> Consequential State
  -> recognition for a stated purpose
  -> external effect
```

The minimum identity fact required by the protocol is the public key that
signed an event. A recognition system may subsequently determine that the key
represents a particular person, organization, warehouse, authority, service,
device, or software agent.

An identity-first architecture commonly begins by resolving a subject and its
credentials, keys, roles, or service endpoints before evaluating a statement.
That is useful where identity assurance is the primary objective. OpenETR has
a different primary objective: preserving independently verifiable records of
consequential actions concerning an exact digital artifact.

Identity is therefore important but not foundational in the same way:

- signatures establish cryptographic attribution;
- profiles and external systems associate operational meaning with keys;
- registries, credentials, attestations, and trust frameworks support
  recognition; and
- law, policy, contract, and institutional rules determine effect.

## The "Cult Of The Original"

The phrase **"cult of the original"** describes a modern tendency to locate
authenticity and authority in a singular artifact with a privileged physical
history. Walter Benjamin observed that a traditional original possesses a
unique presence in time and place, while technical reproduction substitutes a
plurality of copies for that unique existence. His analysis is concerned with
works of art, but the distinction helps expose a problem with digital records:
perfect reproduction is an ordinary property of the medium, not an exceptional
act.

Historical scholarship also shows that authenticity has not always depended
exclusively on modern forensic ideas of singular authorship, physical origin,
and an unbroken material object. In some medieval settings, authority could be
relational, institutional, customary, devotional, or functional. Copies and
reconstructions could participate in an accepted tradition even where modern
historical methods would question their material origin.

OpenETR does not adopt a medieval proposition that accepted utility, belief,
or spiritual truth may substitute for factual provenance. Nor does it treat a
plausible reconstruction as equivalent to authentic evidence. The comparison
identifies one narrower and useful insight:

> The authority associated with a record need not reside exclusively in one
> privileged physical embodiment.

OpenETR combines that relational insight with modern cryptographic exactness.
It can therefore be understood as a model of **cryptographically rigorous
relational authenticity**.

## Relocating Historical Testimony

For a physical artifact, changes in condition, custody, and ownership may be
carried by the object's unique material history. A byte-for-byte digital copy
does not carry a visibly distinct patina or naturally privileged location.

OpenETR relocates the relevant historical testimony from a particular storage
instance into a Digital Controllable Record (DCR): one signed event or a graph
of signed and linked events concerning the artifact.

The model separates four things that physical practice often combines:

| Concern | OpenETR treatment |
| --- | --- |
| Exact content | A cryptographic digest identifies the Digital Artifact. |
| Attributable history | Signed events identify the keys making assertions or taking actions. |
| Consequential history | Event links and transition rules permit a verifier to derive state. |
| Accepted authority and effect | A recognition context decides which actors, graph, and state it accepts for a purpose. |

The DCR does not create a new physical original. It preserves the evidence
from which the artifact's consequential history can be reconstructed and
evaluated without relying exclusively on the application that first displayed
or stored it.

## Originality Without A Privileged Copy

Byte-for-byte copies having the same digest represent the same Digital
Artifact. Moving, backing up, transmitting, or rendering those bytes does not
create a second artifact identity and does not independently duplicate its
control state.

Consequential state attaches to the digest-addressed artifact through its
validated DCR. It does not attach separately to every file-system instance,
download, attachment, or storage location.

OpenETR therefore separates:

- originality from uniqueness of physical embodiment;
- artifact identity from storage location;
- authenticity from recognition;
- cryptographic attribution from legal identity; and
- protocol-derived state from external effect.

A Digital Original is consequentially singular even when its exact bytes are
widely reproduced. A relying party can obtain any exact copy, identify it by
digest, retrieve or receive the relevant signed evidence, and independently
evaluate the candidate state.

## A Records-First Account Of Forgery

Under this model, copying the bytes of an artifact is not itself forgery. A
perfect copy remains an instance of the same digest-addressed Digital
Artifact. The relevant failures become more precise:

| Conduct or defect | Result |
| --- | --- |
| Altering the artifact bytes | Produces a different digest and therefore a different Digital Artifact. |
| Claiming that another key signed an event | Fails signature verification. |
| Signing an action without recognized authority | Produces cryptographically attributable evidence that may be invalid under transition policy or denied recognition and effect. |
| Publishing an unlinked or malformed transition | Produces evidence that does not validly continue the candidate control graph. |
| Constructing a conflicting history | Produces competing branches or claims that a verifier must report and a recognition policy must evaluate. |
| Misrepresenting the real-world subject behind a key | Creates an identity or recognition failure, even if the signature itself is valid. |
| Omitting relevant evidence | Creates an evidence-completeness and retrieval-coverage problem rather than proving that the omitted event does not exist. |

The operative question changes from:

> Is this the one authentic physical copy?

to:

> What exact artifact is this, what authentic signed records concern it, what
> consequential state follows under the applicable rules, and under which
> recognition context is that state accepted?

OpenETR verifiers should report those dimensions separately. A valid signature
does not prove authority. A valid transition does not compel recognition. An
apparently complete graph does not prove universal completeness. Each proof
proves only what it proves.

## Design Consequences

The records-first decision has the following consequences for OpenETR:

1. **The artifact is content-addressed.** The digest, not a platform record id
   or storage location, establishes the artifact identity used by the control
   layer.
2. **The history is evidence-addressed.** Signed event ids and explicit links
   preserve inspectable evidence of assertions and state transitions.
3. **Consequential state is derived.** No application's mutable status field
   is the exclusive source of truth for the control state.
4. **Copies remain useful.** Any exact copy can be checked against the same
   digest and DCR evidence.
5. **Identity stays composable.** DIDs, credentials, KYC results, registries,
   Nostr Web of Trust attestations, TRQP responses, and host-system accounts
   may support recognition without becoming mandatory dependencies of the
   base record protocol.
6. **Recognition remains contextual.** Different relying parties may apply
   different rule books to the same authentic evidence and may reach different
   conclusions about recognition or effect.
7. **Infrastructure is non-exclusive.** Signed records may be obtained from
   public relays, private relays, archives, evidence packages, or local stores
   and verified without the originating application running.

## Scope And Limits Of The Historical Analogy

The historical comparison is explanatory, not normative. It does not establish
legal equivalence between medieval documentary practice and a modern
electronic transferable record. It does not relax OpenETR's cryptographic or
state-transition requirements. It does not imply that social acceptance can
repair altered bytes, invalid signatures, or broken graph links.

The analogy helps distinguish two questions:

- Must authenticity depend on one unique material carrier?
- Can authority and effect instead arise from verifiable relationships,
  attributable actions, and a recognized context?

OpenETR answers the first question **no** and makes the second question
explicit. Cryptography supplies evidence of exact content and signed actions;
protocol rules derive candidate consequential state; external institutions
determine recognition and effect.

## Working Maxims

- Copies are plural; consequential state is singular.
- A Digital Original is consequentially original, not physically uncopyable.
- The digest identifies the artifact; the DCR records what happened to it.
- The control graph carries consequential history without becoming a claim of
  universal authority.
- Identity informs recognition; it does not exclusively own the record.
- Cryptography establishes attributable evidence, not legal effect.
- Each proof proves only what it proves.

## Sources And Further Reading

Historical sources provide context rather than normative requirements:

- [Walter Benjamin, *The Work of Art in the Age of Mechanical Reproduction*](https://web.mit.edu/allanmc/www/benjamin.pdf)
- [Alexander Nagel, "The Copy and Its Evil Twin: Thirteen Notes on Forgery"](https://www.mit.edu/~allanmc/nagle.forgery.pdf)
- [Diarmaid MacCulloch, "Faking the Canon"](https://www.lrb.co.uk/the-paper/v36/n03/diarmaid-macculloch/faking-the-canon)

Related OpenETR documents:

- [Digital Originality, Control, And Standing Design Note](./DIGITAL_ORIGINALITY_CONTROL_AND_STANDING_DESIGN_NOTE.md)
- [Digital Controllable Record Design Note](./DIGITAL_CONTROLLABLE_RECORD_DESIGN_NOTE.md)
- [Consequential State Architecture Design Note](./CONSEQUENTIAL_STATE_ARCHITECTURE_DESIGN_NOTE.md)
- [Provenance And Control Design Note](./PROVENANCE_AND_CONTROL_DESIGN_NOTE.md)
- [OpenETR Generic Verifier Policy](./OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR, W3C DIDs, Nostr, And did:webvh Analysis Note](./OPENETR_DIDS_NOSTR_AND_DID_WEBVH_ANALYSIS_NOTE.md)
