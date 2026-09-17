# OPENETR/CD 1:2026

# Digital controllable records - Open protocol requirements for end-verifiable evidence and consequential state

## Committee draft

**Status:** Draft for discussion and technical review  
**Edition:** 1  
**Date:** 2026-09-10
**Language:** English working draft

> **Important notice:** This document is an OpenETR project draft prepared in
> the style of a consensus standard. It is not a National Standard of Canada,
> has not been developed or approved by an organization accredited by the
> Standards Council of Canada, and has not been approved or endorsed by the
> Standards Council of Canada. The identifier above is a project committee
> draft identifier only and is not a Canadian standards designation.

## Preface

This committee draft specifies a general model for identifying a Digital
Artifact, preserving end-verifiable evidence concerning it, and deriving
Consequential State from that evidence under an identified policy.

The draft is intended to support interoperability among independent systems,
organizations, sectors, and legal jurisdictions. It does not prescribe a
single application, registry, database, relay operator, document repository,
identity provider, trust framework, or legal rule book.

The initial interoperable wire binding uses signed Nostr events. The core
model is transport-neutral so that another event protocol or storage system
can implement an equivalent evidence model if it preserves the required
properties.

This draft should be reviewed through an open, balanced, consensus-oriented
standards-development process before it is considered for adoption by any
standards body. Such a process should include representation from users,
implementers, public-interest participants, legal and policy experts,
regulated sectors, conformity-assessment interests, and relevant authorities.

## Introduction

Digital content can be copied perfectly. A copy of a file can reproduce its
bytes, but the file alone cannot establish who made a consequential statement
about it, how that statement relates to prior statements, or what state follows
under defined rules.

OpenETR separates five concerns:

1. the **Digital Artifact**, identified by its content;
2. the **Digital Controllable Record (DCR)**, containing signed evidence;
3. **Consequential State**, derived from validated DCR evidence;
4. **Recognition**, supplied by an applicable external rule book; and
5. **Effect**, given to recognized state by a person, system, institution,
   contract, or law.

The model may be summarized as follows:

```text
Digital Artifact -> Digital Controllable Record -> Consequential State

Digital Artifact + established Consequential State -> Digital Original

Consequential State -> Recognition -> Effect
```

OpenETR does not make an application database the permanent source of truth.
Applications may store projections and indexes, but a conforming verifier can
reconstruct the evidence and derive state independently.

## 1 Scope

### 1.1 General

This document specifies requirements and recommendations for:

a) identifying a Digital Artifact by cryptographic digest;

b) constructing a DCR from signed, end-verifiable records;

c) anchoring and extending a candidate Evidence Graph, including any Control
Graph subset;

d) verifying record integrity, signer attribution, object consistency, and
graph links;

e) deriving Consequential State under an identified verifier policy;

f) representing generic control actions;

g) separating cryptographic verification from recognition and effect;

h) representing actor-neutral signing identities;

i) integrating OpenETR into independent host systems and domain adapters;

j) storing and retrieving evidence without dependence on one application at
the time of performance; and

k) implementing the OpenETR Nostr wire profile.

### 1.2 Application

This document is applicable to durable electronic records and other Digital
Artifacts for which independently verifiable consequential history is useful.
Examples include warehouse receipts, bills of lading, product passports,
certificates, credentials, permits, health records, provenance records, and
other electronic records.

### 1.3 Exclusions

This document does not determine:

a) legal title, ownership, negotiability, possession, priority, or protected
holder status;

b) whether an electronic record satisfies legislation in a jurisdiction;

c) KYC, AML, sanctions, licensing, registry, or accreditation sufficiency;

d) the authority of a signer to act for a person or organization;

e) the substantive content required for a domain document;

f) document custody, confidentiality, disclosure, or retention obligations;

g) whether a relying party is required to recognize a record; or

h) the legal, contractual, regulatory, or institutional effect of a record or
state.

## 2 Normative references

The following documents are referenced by the Nostr conformance profile. For
undated references, the implementing conformance statement shall identify the
revision or commit used.

- NIST FIPS PUB 180-4, *Secure Hash Standard (SHS)*.
- Nostr NIP-01, *Basic protocol flow description*.
- Nostr NIP-19, *bech32-encoded entities*.
- OpenETR, *OpenETR Nostr Wire Format Specification*.
- OpenETR, *Evidence Event Minimum Shapes*.

## 3 Terms and definitions

For the purposes of this document, the following terms and definitions apply.

### 3.1 actor

person, organization, service, autonomous agent, signing service, or combined
workflow associated by an integrating system with a signing key

Note 1 to entry: The protocol does not infer actor type from a public key.

### 3.2 Anchor Record

first signed record in a candidate DCR graph concerning a Digital Artifact

Note 1 to entry: An Anchor Record supplies a candidate starting point. It does
not by itself establish uniqueness, recognition, or effect.

### 3.3 candidate chain

ordered path through cryptographically linked records that has not necessarily
been accepted under the selected verifier policy

### 3.4 Commitment Profile

independent operational signing identity organized by a Control Desk Key and
used to sign OpenETR records

### 3.5 Consequential Action

action evidenced by a signed record that can affect derived state under an
applicable policy

### 3.6 Consequential State

state that follows when validated DCR evidence is evaluated according to
defined protocol and verifier rules

Note 1 to entry: Consequential State is a derived result, not another event or
authoritative database row.

### 3.7 Contact

locally named external party whose public key can be resolved for interaction

Note 1 to entry: A Contact name does not establish authority, familiarity, or
recognition.

### 3.8 control graph

subset of an Evidence Graph formed by the records to which defined rules assign
controller or control-transition consequences concerning the same Digital
Artifact

### 3.9 evidence record

signed, end-verifiable record that provides evidence of an action, assertion,
or relationship concerning a Digital Artifact and participates in a DCR

Note 1 to entry: An evidence record does not necessarily change control or
Consequential State. Defined rules determine what consequence, if any, follows.

### 3.10 Control Desk Key

administrative root signing identity used by an OpenETR environment to manage
configuration and Commitment Profiles

Note 1 to entry: The Control Desk Key and Commitment Profile keys are ordinary,
cryptographically independent key pairs. Their administrative relationship is
created by the OpenETR component, not by the underlying signature algorithm.

### 3.11 Digital Artifact

persistent digital content with a unique content identity, normally
established by a cryptographic digest

### 3.12 Digital Controllable Record

DCR

signed evidence structure from which defined rules derive Consequential State
concerning a Digital Artifact after the evidence is validated

Note 1 to entry: A DCR may consist of a single end-verifiable record or a graph
of related end-verifiable records.

### 3.13 Digital Original

Digital Artifact with Consequential State

Note 1 to entry: Consequential State is established through a DCR. Recognition
and effect remain external determinations.

### 3.14 domain adapter

component that maps domain vocabulary, roles, actions, and policies to and from
the generic OpenETR model

### 3.15 effect

legal, contractual, regulatory, institutional, operational, or other
consequence given to recognized state

### 3.16 end-verifiable

capable of being verified by a relying party from the evidence itself without
requiring the application that created or displayed the evidence to be running

### 3.17 event

cryptographically signed data structure containing an identifier, signer,
timestamp, type, tags, content, and signature

### 3.18 Evidence Event

cryptographically signed event that serves as an evidence record in a DCR

Note 1 to entry: In the OpenETR Nostr binding, a kind `1415` Anchor Event and a
kind `1416` event are Evidence Events. The Anchor Event begins a candidate DCR;
later Evidence Events extend or relate to it.

Note 2 to entry: The existence of an Evidence Event does not by itself establish
a state change, recognition, or effect.

### 3.19 evidence graph

DCR graph including Anchor Records, later evidence records, and any linked
evidence records

### 3.20 guard policy

policy applied before publication by an implementation to decide whether it
will sign or publish a proposed event

Note 1 to entry: A guard policy cannot prevent another implementation from
publishing a competing signed event.

### 3.21 Key-Based Identifier

KBI

identifier whose canonical value is public-key verification material or a
deterministic encoding of that material

Note 1 to entry: A KBI identifies the signing key used to verify attributable
signed evidence. It does not, by itself, establish the identity, actor type,
authority, role, or recognition of the actor associated with that key.

### 3.22 recognized state

Consequential State accepted under an identified external recognition policy
for a stated purpose

### 3.23 recognition

determination by a relying party, institution, registry, trust framework,
contract, or law that evidence or derived state is acceptable for a stated
purpose

### 3.24 Reference

external authority, registry, assessor, attestor, trust service, or other
source that can supply recognition or assurance context

### 3.25 relying party

person, organization, system, or authority that evaluates OpenETR evidence or
acts upon resulting state

### 3.26 verifier policy

identified and versioned rule book used to validate DCR evidence, enumerate
candidate chains, issue findings, and derive Consequential State

### 3.27 warning

structured finding that identifies a policy or evidence concern without
making otherwise authentic signed evidence disappear

## 4 Abbreviated terms

**AML** anti-money laundering  
**API** application programming interface  
**CLI** command-line interface  
**DCR** Digital Controllable Record  
**ETR** electronic transferable record  
**JSON** JavaScript Object Notation  
**KBI** Key-Based Identifier<br>
**KYC** know your customer  
**MLWR** Model Law on Warehouse Receipts  
**NIP** Nostr Implementation Possibility  
**REST** representational state transfer  
**SHA-256** Secure Hash Algorithm with a 256-bit output

## 5 Conventions and conformance

### 5.1 Verbal forms

In this document:

- **shall** indicates a requirement;
- **should** indicates a recommendation;
- **may** indicates a permission; and
- **can** indicates a possibility or capability.

### 5.2 Conformance targets

An implementation may claim conformance as one or more of the following:

a) **Core Publisher**, which creates signed OpenETR records;

b) **Core Verifier**, which verifies evidence and derives state;

c) **Domain Adapter**, which maps a domain to the OpenETR core;

d) **Nostr Publisher**, which implements the normative Nostr profile in
Annex A;

e) **Nostr Verifier**, which retrieves and verifies the normative Nostr profile
in Annex A; or

f) **Integration Surface**, which exposes the component through a machine or
human interface.

### 5.3 Conformance statement

A conformance claim shall identify:

a) the conformance target or targets;

b) the version of this document;

c) the implemented wire binding and its version;

d) the digest and signature algorithms;

e) the implemented action set;

f) the verifier policy identifier and version, where state is derived;

g) any domain profile implemented;

h) supported identifier encodings; and

i) known deviations, extensions, or unsupported optional features.

## 6 OpenETR reference model

### 6.1 Separation of concerns

A conforming implementation shall distinguish:

a) Digital Artifact content;

b) signed DCR evidence;

c) derived Consequential State;

d) recognition decisions; and

e) external effect.

An implementation shall not represent a mutable application state projection
as if it were the signed DCR evidence that produced it.

### 6.2 Layer model

The OpenETR model consists of four logical layers:

```text
Domain adapter
  domain vocabulary, workflows, validation, and policy presentation

OpenETR protocol layer
  DCR evidence, graph traversal, state transition rules, and state derivation

Wire binding
  signed records, identifiers, tags, transport, storage, and retrieval

Recognition layer
  law, contracts, registries, trust frameworks, and relying-party decisions
```

A conforming implementation may combine these layers in one deployment, but
shall preserve their logical boundaries.

### 6.3 Technology neutrality

The core model shall not require Nostr where an alternative binding preserves:

a) cryptographic attribution to a KBI;

b) stable artifact commitment;

c) immutable record identity;

d) record signature;

e) signed structured data;

f) explicit graph links;

g) replayable evidence history; and

h) independent verifier-policy inputs.

Implementations that exchange records using the OpenETR Nostr profile shall
conform to Annex A.

## 7 Digital Artifact identification

### 7.1 Digest identity

A Core Publisher shall identify a Digital Artifact by a cryptographic digest.

The digest algorithm shall provide pre-image resistance, second-pre-image
resistance, and collision resistance appropriate to the application.

The OpenETR Nostr profile shall use SHA-256.

### 7.2 Content boundary

The domain adapter or publisher shall define the bytes or canonical data over
which the digest is calculated.

Where canonicalization is used, the implementation shall document:

a) the canonicalization algorithm and version;

b) package finalization rules;

c) treatment of metadata and signatures embedded in the artifact;

d) whether transformations produce a new Digital Artifact; and

e) how alternate renderings relate to the canonical content.

### 7.3 Copying

Byte-identical copies having the same digest shall be treated as instances of
the same Digital Artifact.

Copying artifact bytes or DCR evidence shall not be interpreted as creating a
separate Digital Artifact, a new DCR history, another controller, or independent
Consequential State.

A copy of complete DCR evidence may be used by another conforming verifier to
reconstruct the same candidate graph and derive the same Consequential State
under the same identified rules.

### 7.4 Disclosure

An implementation may disclose the artifact, retain it privately, or make it
available through a separate content service. The DCR shall not require the
artifact bytes to be stored inside each evidence record.

## 8 Digital Controllable Record requirements

### 8.1 General

A DCR shall consist of one signed Anchor Record or a graph beginning with an
Anchor Record and extended by signed records concerning the same Digital
Artifact.

Each record shall be independently verifiable for integrity and signer
attribution.

### 8.2 Anchor Record

An Anchor Record shall:

a) identify the Digital Artifact;

b) identify its signer;

c) have a cryptographically derived record identifier;

d) carry a valid signature; and

e) declare an anchoring or issuance action.

An Anchor Record shall be treated as a candidate assertion. A verifier shall
not infer universal authority or uniqueness merely because an Anchor Record is
cryptographically valid.

More than one candidate Anchor Record may exist for the same Digital Artifact.

### 8.3 Later evidence records

A later evidence record shall:

a) identify the same Digital Artifact as the candidate Anchor Record;

b) identify the immediately prior record or specific record on which it
relies;

c) identify its action;

d) identify its signer; and

e) carry a valid signature.

An evidence record shall not be silently relinked to a different prior record.

### 8.4 Generic actions

The generic OpenETR action vocabulary includes:

- `issue`, to create an Anchor Record;
- `initiate`, to propose a transfer;
- `accept`, to accept a proposed transfer;
- `attest`, to make a signed assertion;
- `encumber`, to declare a claimed encumbrance;
- `discharge`, to release or satisfy a referenced encumbrance;
- `redeem`, to present the artifact to an obligor for performance; and
- `terminate`, to end the active lifecycle if recognized under policy.

A domain adapter may assign domain terminology to these actions. It shall
preserve the generic action semantics when claiming OpenETR interoperability.

### 8.5 Structured and unstructured data

Machine-readable event data shall be represented as signed structured fields
or tags.

Human-readable comments, summaries, and other unstructured context should be
represented separately from required structured data.

A verifier shall not be required to parse human-readable content to recover a
required graph link, artifact identifier, participant, action, or
action-specific reference.

### 8.6 Linked evidence

An implementation may associate supporting artifacts or attestations with a
DCR. Linked evidence shall identify:

a) the primary Digital Artifact or a specific DCR record;

b) the linked artifact or evidence item;

c) the signer making the association; and

d) the claimed relationship type.

Linked evidence shall not be interpreted as changing controller state unless
the selected policy explicitly assigns that consequence.

A linked-evidence relationship shall distinguish an evidentiary relationship
from a relationship to which defined rules assign a state consequence.
Evidentiary relationships may include `derived_from`, `ingredient_of`, and
`rendition_of`. These relationships shall not, by themselves, be interpreted as
meaning that one artifact supersedes or replaces another.

Relationships such as `supersedes` and `replaces` shall affect Consequential
State only where the selected verifier policy or Domain Adapter defines their
preconditions and effects.

Where linked evidence depends on an external verification mechanism, verifier
output should distinguish, where applicable, evidence availability, integrity,
content binding, signature or credential status, policy sufficiency, and
recognition. Provenance evidence shall not be represented as proving control,
supersession, recognition, or effect unless separate defined rules support that
conclusion.

### 8.7 Attestations

An attestation should identify the specific event, graph commitment, evidence
bundle, observation, or procedure to which it applies.

A valid attestation signature shall establish attribution of the attestation.
It shall not, by itself, establish that the attestor is:

a) the controller of the Digital Artifact;

b) the author of the underlying event;

c) the source of Consequential State;

d) a canonical registry; or

e) a recognition authority.

Defined rules shall determine what an attestation contributes to Consequential
State. An external recognition context shall determine what effect, if any, to
give the attestation or attestor.

## 9 Graph reconstruction and verification

### 9.1 Retrieval

A Core Verifier shall be capable of retrieving or accepting candidate records
for a supplied artifact identifier from one or more identified evidence
sources.

The verifier should avoid assuming that the first record returned by one
repository is authoritative.

The verifier shall not represent records returned by declared evidence sources
as proving that no additional or conflicting record exists elsewhere.

### 9.2 Structural verification

For each candidate record, a Core Verifier shall verify:

a) record identifier integrity;

b) signature validity;

c) signer identifier syntax;

d) artifact identifier syntax;

e) required record fields;

f) consistency of the artifact identifier across a candidate chain;

g) existence and identity of referenced prior records; and

h) action-specific required data.

### 9.3 Graph enumeration

A Core Verifier shall enumerate candidate Anchor Records and candidate graph
paths before applying recognition conclusions.

The verifier shall preserve competing, branching, or policy-questionable
signed evidence for inspection.

### 9.4 Broken links

A record whose required prior-record link is absent, malformed, cyclic, or
cryptographically inconsistent shall not be used as a valid extension of that
candidate chain.

The verifier should report the affected record and reason.

### 9.5 Reproducibility

Given the same evidence set, policy identifier, policy version, and evaluation
parameters, conforming verifiers shall produce equivalent structural findings
and Consequential State.

### 9.6 Verification result dimensions

A Core Verifier shall not represent all verification and recognition concerns
as one undifferentiated validity result.

Where applicable, verifier output shall distinguish:

a) artifact integrity;

b) event authenticity;

c) structural validity;

d) graph continuity;

e) historical continuity, where evaluated;

f) source consistency or divergence, where observations can be compared;

g) transition validity;

h) derived Consequential State;

i) retrieval coverage;

j) evidence sufficiency under the identified policy;

k) optional temporal assurance;

l) observation, witness, or audit attestation status;

m) linked-evidence and external-verification status, including provenance where
evaluated;

n) monitoring status, where applicable;

o) actor or authority recognition;

p) system reliability assessment; and

q) external recognition and effect.

An evaluated dimension should use a defined outcome vocabulary that can
distinguish `valid`, `invalid`, `unverifiable`, `conflicting`, `absent`,
`not_evaluated`, and `not_applicable` where those outcomes are meaningful.

An outcome for one dimension shall not be silently treated as an outcome for
another dimension.

### 9.7 Divergent observations and equivocation

Valid signatures shall not be represented as proving that every observer has
received a single globally consistent Evidence Graph.

Where observations from multiple evidence sources can be compared, a verifier
should report stale, incomplete, incompatible, or divergent evidence sets.
If the available evidence and rules do not support a unique state, the
verifier shall preserve the competing evidence and report the state as
ambiguous, conflicting, insufficiently evidenced, or otherwise unresolved.

The result shall identify the evidence sources, retrieval scope, rules, and
evaluation parameters on which the conclusion depends.

## 10 Consequential State

### 10.1 Derivation

Consequential State shall be derived from validated DCR evidence under an
identified verifier policy.

An implementation shall be able to identify the evidence records and policy
version that produced a displayed state.

### 10.2 State projection

An application may cache or index Consequential State. A cached projection
shall not replace the underlying evidence and shall be invalidated or
recalculated when the relevant evidence set or policy changes.

### 10.3 Generic state dimensions

A verifier may derive:

a) lifecycle state, including active, transfer pending, redemption pending,
or terminated;

b) candidate current controller;

c) candidate transfer participants;

d) declared encumbrances, discharges, and outstanding encumbrances;

e) attestations and linked evidence; and

f) structural and policy findings.

### 10.4 Digital Original

A Digital Original shall have Consequential State established through a DCR.

An implementation shall not claim that byte possession alone, file location,
or an application database row establishes a Digital Original.

Whether the Digital Original and its state are recognized as authoritative
for a particular purpose is determined under Clause 13.

### 10.5 Historical state derivation

Where sufficient evidence is available, a Core Verifier should be capable of
deriving Consequential State for a candidate DCR path ending at a specified
event.

A historical-state result shall identify:

a) the terminal event or graph cut;

b) the ancestor evidence used;

c) the evidence sources and retrieval scope;

d) the verifier policy identifier and version;

e) competing evidence present in the supplied evidence set;

f) unresolved links or completeness limitations; and

g) the resulting Consequential State and findings.

The result shall be represented as evidence-set-relative, rule-set-relative,
and path-relative. It shall not be represented as globally authoritative state
at the event's declared timestamp unless separate accepted evidence supports
that conclusion.

## 11 Verifier policy

### 11.1 Policy identification

A verifier policy used to derive state shall have a stable identifier and
version.

The verifier output shall identify the policy applied.

### 11.2 Baseline evaluation

A baseline verifier policy shall:

a) retrieve or accept the artifact evidence set;

b) verify cryptographic and structural correctness;

c) enumerate candidate chains;

d) evaluate generic transition rules;

e) identify ambiguity and conflicts;

f) produce structured findings; and

g) derive candidate Consequential State.

A verifier policy claiming OpenETR baseline-policy conformance shall publish
normative transition rules for every action from which it derives
Consequential State. For each supported action, those rules shall define:

a) permitted parent record kinds and actions;

b) required signer and participant relationships;

c) required structured evidence;

d) state preconditions;

e) state variables created, changed, or cleared;

f) handling of duplicate, competing, missing, or out-of-order evidence;

g) the conditions that produce invalid, conflicting, unverifiable, warning, or
non-recognition outcomes; and

h) treatment of unknown actions and extensions.

The policy shall also define whether and how an Anchor Record establishes
initial candidate controller, lifecycle, or other state. Where the applicable
rules do not define a consequence, a verifier shall not infer one from an
action label, signer identity, document text, or application state.

### 11.3 Evidence preservation

A policy violation shall not cause an otherwise authentic signed record to be
erased from the evidence set.

A verifier shall distinguish:

a) evidence that is cryptographically or structurally unusable;

b) evidence that is authentic but contrary to a policy rule; and

c) evidence accepted as effective under the selected policy.

### 11.4 Warnings

Policy concerns should be returned as structured warnings or non-recognition
annotations unless the concern prevents structural verification.

A warning should include:

a) a stable machine-readable code;

b) severity;

c) the affected record or identity;

d) a human-readable explanation; and

e) the policy consequence.

### 11.5 Domain and organizational policies

A domain or organization may define a policy overlay that adds safeguards,
actor requirements, schemas, attestations, exemptions, or recognition rules.

An overlay shall not conceal the baseline signed evidence or structural
result.

Different relying parties may reach different recognition conclusions from
the same authentic evidence set. Each conclusion shall identify the policy
under which it was reached.

## 12 Identity and key organization

### 12.1 Actor neutrality

The OpenETR protocol shall treat a signing key independently of whether it is
operated by a human, organization, service, autonomous agent, hardware device,
or combined workflow.

A valid signature shall establish that the signed record was produced using the
private-key capability corresponding to the identified KBI. It shall not be
represented as proof of key custody, actor intent, actor type, legal identity,
mandate, licensing, KYC status, or authority.

### 12.2 Principal, operator, and signer

An integrating system should distinguish:

a) the **principal**, on whose authority an action is performed;

b) the **operator**, which initiates or executes the action; and

c) the **signer**, which produces the cryptographic signature.

The system should retain or link evidence of these relationships where its
policy requires them.

### 12.3 Control Desk Key and Commitment Profiles

A Control Desk Key may organize one or more Commitment Profiles.

The relationship shall be treated as an application-level administrative
relationship, not as cryptographic derivation or inherent delegation between
the keys.

The same key may perform both roles, but production implementations should
separate administrative and operational signing roles where practical.

### 12.4 Acting Profile

Where more than one Commitment Profile is available, the user or host system
shall be able to determine which Commitment Profile is the Acting Profile for
a proposed operation.

A signed operational record shall identify the public key that actually signed
it, regardless of the profile label displayed by the application.

### 12.5 Contacts and References

A Contact may resolve a local name to an external participant public key.

A Reference may identify an external recognition or assurance source.

Neither a Contact nor a Reference shall, by itself, be treated as proof of
legal identity, authority, or trustworthiness.

### 12.6 Identifier resolution

Human-facing interfaces may accept profile names, Contact names, public-key
encodings, hexadecimal keys, or externally resolvable identifiers.

Before signing or comparison, an implementation shall normalize an identity
to the canonical public-key representation required by its wire binding.

Identifier resolution shall not be represented as recognition.

### 12.7 External key-history evidence

An implementation may consume or link evidence concerning historical or
current bindings between an actor identifier and a signing key. Such evidence
may come from a Key Transparency system, PKI, DID method, credential system,
trust registry, or another external mechanism.

Where later historical verification depends on external evidence, the
implementation should preserve or reference the evidence used at evaluation
time. A current directory response shall not be represented as proof of a
historical key binding.

External key-history evidence shall be evaluated under its own verification
and recognition rules. OpenETR shall not require one key-history mechanism.

### 12.8 Key protection

Private keys shall not be published in OpenETR events, logs, API responses, or
machine-readable command output.

An implementation shall protect private keys according to the risk and
assurance requirements of the host system. It should support separation of
administrative and operational keys, backup, rotation, recovery, suspension,
and incident response.

## 13 Recognition and effect

### 13.1 Boundary

OpenETR verification shall answer which key signed which record concerning
which Digital Artifact and how the record participates in a candidate DCR.

OpenETR core shall not claim that cryptographic validity alone establishes
legal, institutional, contractual, or regulatory effect.

### 13.2 Recognition inputs

A verifier policy may use recognition inputs including:

a) trust registries;

b) KYC or identity providers;

c) licensing or regulatory registries;

d) attestations and credentials;

e) Web of Trust signals;

f) organizational familiarity lists;

g) enterprise account and role systems;

h) contractual network rules; and

i) applicable legislation or judicial determinations.

### 13.3 KYC and actor assurance

KYC, AML, sanctions, agent governance, and similar actor-assurance controls
shall be treated as integration or recognition concerns unless a domain
profile expressly requires them.

Their absence shall not be represented as invalidating an otherwise valid
event signature.

### 13.4 Transparent conclusions

A recognized-state output should distinguish:

a) cryptographic findings;

b) structural graph findings;

c) protocol-policy findings;

d) recognition inputs consulted; and

e) the resulting effect or recommendation.

## 14 Domain adapters

### 14.1 General

A Domain Adapter shall translate domain actions and terms to the generic
OpenETR model and translate DCR results back into domain language.

### 14.2 Required profile information

A conforming Domain Adapter shall document:

a) scope and excluded record types;

b) intended users and relying parties;

c) Digital Artifact boundaries and canonicalization;

d) digest algorithm;

e) domain roles and their OpenETR mappings;

f) domain actions and their generic action mappings;

g) required structured event data;

h) verifier policy and recognition inputs;

i) privacy, disclosure, and retention assumptions;

j) error and warning presentation; and

k) any jurisdiction-specific requirements.

### 14.3 Legal terminology

A Domain Adapter may use legal or business terminology appropriate to its
users. It shall not imply that the generic OpenETR term itself satisfies a
legal classification.

For example, an OpenETR DCR is not automatically a controllable electronic
record under UCC Article 12 or an electronic transferable record under an
MLETR-based enactment.

### 14.4 Document independence

A Domain Adapter shall permit the protocol layer to remain logically separate
from document movement and storage.

The artifact may be exchanged by an existing document-management, registry,
messaging, repository, or API system.

## 15 Storage, transport, and availability

### 15.1 Independence from a running application

A conforming system shall enable signed DCR evidence to be exported or
retrieved in a form that can be verified without the originating application
being available at the time of performance.

### 15.2 Repository neutrality

DCR evidence may be stored on public relays, private relays, local relays,
databases, archives, files, or other repositories.

Repository acceptance shall not be treated as recognition of an event's
semantic or legal effect.

### 15.3 Redundancy

Implementations should use redundant retrieval or archival arrangements
appropriate to the required availability and retention period.

A relying party should be able to preserve the exact signed evidence needed to
reproduce a consequential-state determination.

### 15.4 Local operation

An implementation shall not require use of a third party's running OpenETR
application where the relying party possesses the required signed events and
verification software.

### 15.5 Relay-backed configuration

An implementation may store non-secret configuration as signed relay-backed
records. Bootstrap relay locations and root private-key material may remain
local or be protected by a host account or custody system.

### 15.6 Retrieval coverage

A verifier shall distinguish repository-specific retrieval completion from
global evidence completeness.

Where a repository or transport reports that all matching stored records have
been returned, the verifier may report completion for that source and query.
It shall not infer that no additional or conflicting record exists in another
repository or outside the observed evidence boundary.

A verifier should report whether additional records are known to be available,
authentication is required, pagination is incomplete, or retrieval
completeness is unknown.

Graph continuity and policy sufficiency shall be evaluated separately from
repository retrieval coverage.

## 16 Integration surfaces

### 16.1 General

The OpenETR component may be exposed through:

a) an installable software library;

b) a command-line interface;

c) machine-readable JSON input and output;

d) REST or other service APIs;

e) a web application; or

f) direct implementation of a wire binding.

All surfaces within one product should use a common service and policy layer so
that equivalent operations produce equivalent signed evidence and findings.

### 16.2 Machine-readable output

A machine-readable interface shall:

a) produce a documented response envelope;

b) separate success, failure, and warning conditions;

c) expose stable reason and warning codes;

d) avoid requiring parsing of human console prose;

e) preserve access to raw signed evidence where appropriate; and

f) exclude private keys and secret recovery material.

A machine-readable verifier result should identify each evaluated dimension,
its status, its evidence basis, and the policy or verification procedure used.
Command execution success shall not be represented as equivalent to protocol
validity, recognition, system reliability, or legal effect.

### 16.3 Human interfaces

A human interface should use domain terminology and make the Acting Profile,
proposed action, target artifact, warnings, and resulting state visible before
or after a consequential operation as appropriate.

### 16.4 Hypermedia

A web implementation may use a hypermedia-driven architecture. Client-side
code is not required for protocol conformance.

### 16.5 Automated interpretation and agentic systems

An implementation using automated extraction, interpretation, or inference
shall distinguish machine-generated conclusions from attributable signed or
otherwise independently verified evidence.

An inferred conclusion may be retained or linked as evidence where its source,
method, output, and attribution are identified. Its evidentiary contribution
shall be determined under the selected verifier policy.

Inference alone shall not be represented as proving issuance, actor identity,
authority, authorization, control, Consequential State, recognition, or effect.
Records produced through an autonomous agent or combined human-agent workflow
shall satisfy the same cryptographic, structural, policy, and recognition
requirements as records produced through another workflow.

## 17 Security, privacy, and operational considerations

### 17.1 Threat model

An implementation shall document threats relevant to its deployment,
including:

a) private-key compromise;

b) unauthorized use of a valid signer;

c) conflicting or deceptive records;

d) divergent, stale, or selectively withheld evidence-source results;

e) digest substitution or canonicalization errors;

f) stale state projections;

g) metadata correlation and privacy leakage;

h) denial of service; and

i) dependency or verifier compromise.

An implementation should also consider unauthorized or unexpected use of a
cryptographically valid signing key. Signature validity does not establish
actor intent.

### 17.2 Open publication

An implementation shall assume that events published to public relays can be
widely replicated and difficult to remove.

Sensitive personal, commercial, health, or confidential data should not be
placed directly in public event tags or content unless disclosure is intended
and permitted.

### 17.3 Digest limitations

A digest proves equality to supplied bytes; it does not prove the truth,
quality, legality, completeness, or confidentiality of the artifact.

Low-entropy or guessable hidden data may be vulnerable to dictionary attacks
even where only a digest is published.

### 17.4 Algorithm agility

Implementations should support an orderly transition to new digest or
signature algorithms. A conformance statement shall identify the algorithms
used.

### 17.5 Time

A signed event timestamp shall not be treated as independently trusted time
unless supported by an accepted timestamping or other time-assurance source.

The term **Anchor Event** is reserved in this document for the initial OpenETR
record that begins a candidate DCR. External timestamp, transparency-log, or
ledger evidence should be described as a **Temporal Proof** or another term
that does not imply that it creates OpenETR Consequential State.

Failure to obtain or verify optional Temporal Proof evidence shall not, by
itself, invalidate an otherwise valid DCR. The verifier shall report the
temporal-proof outcome separately.

### 17.6 Auditing and monitoring

An implementation may use independent witnesses, auditors, source comparison,
or monitoring services to strengthen evidence about observation and historical
continuity.

Auditing and monitoring shall not be represented as establishing controller
status, actor intent, recognition, or legal effect unless separate defined
rules and recognition inputs support those conclusions.

The OpenETR core shall not require a transparency log, globally consistent
event order, auditor network, or monitoring service.

### 17.7 Post-quantum considerations

The current Nostr profile is not post-quantum secure. Long-lived deployments
should preserve algorithm identifiers and migration evidence sufficient to
support future re-attestation or transition policies.

## 18 Conformity assessment

### 18.1 Core Publisher tests

A Core Publisher conformance assessment shall confirm that the publisher:

a) calculates the declared artifact digest correctly;

b) constructs required structured data;

c) creates stable record identifiers;

d) signs records with the declared signer;

e) links later records to the intended prior record; and

f) does not disclose private keys.

### 18.2 Core Verifier tests

A Core Verifier conformance assessment shall include:

a) valid and invalid signatures;

b) valid and invalid record identifiers;

c) missing required fields;

d) inconsistent artifact identifiers;

e) missing, cyclic, and conflicting graph links;

f) multiple candidate Anchor Records;

g) competing branches;

h) policy-valid and policy-questionable transitions;

i) reproducible state derivation;

j) historical state derivation at an identified event;

k) divergent or incomplete evidence-source results; and

l) preservation and reporting of authentic but unrecognized evidence;

m) distinct reporting of conflicting evidence; and

n) equivalent results from the same evidence set, policy version, and
evaluation parameters.

### 18.3 Domain Adapter tests

A Domain Adapter conformance assessment shall confirm the documented mappings
for artifact scope, roles, actions, structured data, warnings, policy, and
recognition boundaries.

Where a Domain Adapter uses automated interpretation, the assessment shall
confirm that inferred values are distinguishable from signed or independently
verified evidence and are not represented as establishing Consequential State
without defined rules.

### 18.4 Interoperability tests

Two implementations claiming the same wire profile should demonstrate that:

a) one can publish records retrieved by the other;

b) both verify the same record identifiers and signatures;

c) both reconstruct equivalent candidate graph paths; and

d) both derive equivalent state when supplied with the same evidence and
policy version.

# Annex A (normative) - OpenETR Nostr conformance profile

## A.1 General

An implementation claiming OpenETR Nostr conformance shall implement Nostr
event serialization, identifier derivation, Schnorr signatures, and relay
messages in accordance with NIP-01.

Human-facing bech32 encodings should conform to NIP-19. Canonical event fields
and filters shall use the hexadecimal forms required by NIP-01.

In this binding, the 32-byte Nostr public key is the KBI. Its 64-character
lowercase hexadecimal representation is the canonical wire encoding. `npub`
is the NIP-19 human-readable encoding of the same KBI and shall not replace the
hexadecimal value in NIP-01 event fields or relay filters.

## A.2 Event kinds

The profile defines:

| Kind | Name | Requirement |
| --- | --- | --- |
| `1415` | Anchor Event | Regular event beginning a candidate DCR |
| `1416` | Evidence Event | Regular event extending or relating to a candidate DCR |

Kinds `31415` and `31416` are deprecated prototype kinds and shall not be used
for newly published conforming DCR graphs.

## A.3 Common tags

The following tag rules apply:

a) `o` shall contain the 64-character lowercase hexadecimal SHA-256 digest of
the Digital Artifact;

b) `e` shall contain the hexadecimal event identifier of the prior or specific
record being referenced;

c) `p`, where required, shall contain a participant public key in hexadecimal
form;

d) `action` shall identify the semantic action;

e) `enc`, where required, shall identify the encumbrance event being
discharged;

f) `type` may contain an action-specific subtype; and

g) `ref` may contain an external or business reference.

Single-letter tags may be used as relay query anchors. Named tags shall be
treated as signed structured data even where relays do not index them.

No separate `origin` or `anchor` root-pointer tag is required. A verifier shall
recover the candidate Anchor Event by traversing `e` references to a valid
`kind 1415` event carrying the same `o` value.

## A.4 Anchor Event minimum shape

A `kind 1415` Anchor Event shall contain:

```json
{
  "kind": 1415,
  "tags": [
    ["o", "<artifact_sha256_hex>"],
    ["action", "issue"]
  ],
  "content": "<optional human-readable summary>"
}
```

It may include named structured metadata tags such as `name`,
`digest_generated_at`, `size_bytes`, `record_reference`,
`record_description`, `domain`, `document_type`, `schema`, or `schema_digest`.

## A.5 Evidence Event minimum shapes

Every `kind 1416` Evidence Event shall contain `o`, `e`, and `action`.

Additional minimum requirements are:

| Action | Additional required tag | Meaning |
| --- | --- | --- |
| `initiate` | `p` | intended transferee |
| `accept` | none | acceptance of referenced initiation |
| `terminate` | none | claimed lifecycle termination |
| `attest` | none | assertion about the record referenced by `e` |
| `encumber` | `p` | beneficiary or secured party |
| `discharge` | `enc` | encumbrance event being discharged |
| `redeem` | `p` | obligor to whom performance is presented |

Action-specific optional tags are defined in the OpenETR Nostr Wire Format
Specification.

## A.6 Content

Required machine-readable semantics shall be carried in event fields and tags.
The `content` field should contain only a human-readable summary, comment, or
other unstructured event data.

## A.7 Query

A Nostr Verifier shall be capable of:

a) querying `kind 1415` events using `#o`;

b) querying `kind 1416` events using `#o`;

c) obtaining directly referenced events by event identifier where needed;

d) validating each event identifier and signature; and

e) reconstructing candidate graph paths using `e` references.

Relay `OK` responses and storage acceptance shall not be treated as semantic
recognition of an event.

# Annex B (informative) - OpenETR axioms and maxims

## B.1 Ten axioms

1. **The digest identifies the artifact.** A Digital Artifact is identified by
   a cryptographic digest, independently of its filename, location, format, or
   number of copies.
2. **A signature attributes a statement.** Every OpenETR event is an immutable,
   attributable statement by a signing key. A valid signature establishes
   authorship and integrity; it does not, by itself, establish authority,
   recognition, or legal effect.
3. **An Anchor begins a candidate record.** An Anchor Record establishes the
   starting point of a candidate DCR. It does not, by itself, establish
   uniqueness, validity, or recognition.
4. **Links construct the Evidence Graph.** DCR records reference prior records
   and related evidence through cryptographic identifiers. Links establish
   claimed relationships; they do not, by themselves, establish validity or
   state.
5. **Events are evidence; state is derived.** Events are not overwritten to
   represent current state. Consequential State is derived by evaluating signed
   DCR evidence according to defined rules.
6. **Invalid claims remain visible.** Conflicting, unauthorized, or malformed
   statements remain part of the available evidence. A verifier warns about or
   excludes them according to its rule book rather than erasing signed history.
7. **A Digital Original has Consequential State.** A Digital Original is a
   Digital Artifact for which Consequential State has been established through
   a DCR. Identical copies represent the same artifact; copying its bytes does
   not independently create another consequential history.
8. **Verification is separate from recognition.** OpenETR verifies digests,
   signatures, record links, graph structure, and protocol transitions.
   External systems, policies, institutions, and laws determine recognition and
   effect.
9. **Identity is actor-neutral and contextual.** A KBI identifies public-key
   verification material used to attribute signed evidence. Whether it is
   associated with a person, organization, service, device, or autonomous agent,
   and whether that actor is recognized or authorized, is determined by the
   applicable context.
10. **DCR evidence is portable across systems and domains.** Signed records do
    not belong to one application, relay, operator, or jurisdiction. Domain
    adapters translate business actions into the general OpenETR model, while
    any conforming system can store, retrieve, and verify the resulting DCR.

## B.2 Five maxims

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

# Annex C (informative) - Integration model

## C.1 Host-system boundary

An integrating system commonly remains responsible for:

- user accounts and authentication;
- session and authorization management;
- key custody and recovery;
- document storage and movement;
- domain validation and workflow;
- KYC, AML, licensing, and registry checks;
- privacy, disclosure, and retention; and
- legal and operational recognition.

OpenETR commonly supplies:

- artifact identification;
- signed record construction;
- publication and retrieval;
- graph traversal;
- structural and cryptographic verification;
- verifier-policy findings; and
- Consequential State derivation.

## C.2 Integration patterns

Typical patterns include:

a) an account-based system hiding key and relay mechanics from users;

b) a host application importing the OpenETR Python component;

c) an automation or agent invoking the CLI with JSON output;

d) a service exposing REST APIs;

e) independent implementations exchanging Nostr-profile events; and

f) local archival and verification without a network dependency.

# Annex D (informative) - Domain examples

## D.1 Warehouse receipts

A warehouse receipt adapter can map:

| Domain concept | OpenETR concept |
| --- | --- |
| issued warehouse receipt file | Digital Artifact |
| warehouse issuance record | Anchor Record |
| warehouse operator signing identity | Commitment Profile |
| selected facility or issuer | Acting Profile |
| holder transfer | `initiate` and `accept` records |
| pledge or lien | `encumber` record |
| release | `discharge` record |
| presentation for delivery | `redeem` record |
| completed lifecycle | `terminate` record |

The adapter and applicable law determine whether this evidence satisfies MLWR,
MLETR, registry, licensing, protected-holder, priority, or delivery
requirements.

## D.2 Other domains

The same core may support bills of lading, product passports, credentials,
permits, health records, Apostille-related evidence, and other records. Each
domain profile should define its own artifact boundary, action mappings,
structured data, verifier policy, recognition inputs, and legal limitations.

# Annex E (informative) - Suggested conformance statement

```yaml
implementation: Example OpenETR Verifier
standard_draft: OPENETR/CD 1:2026
conformance_targets:
  - Core Verifier
  - Nostr Verifier
wire_binding:
  name: OpenETR Nostr
  kinds: [1415, 1416]
digest_algorithm: SHA-256
signature_algorithm: secp256k1 Schnorr
actions:
  - issue
  - initiate
  - accept
  - terminate
  - attest
  - encumber
  - discharge
  - redeem
verifier_policy:
  id: org.example.openetr.baseline
  version: 1.0.0
domain_profiles:
  - org.example.mlwr
deviations: []
```

# Bibliography

- OpenETR, *Digital Controllable Record Design Note*.
- OpenETR, *OpenETR Generic Verifier Policy*.
- OpenETR, *OpenETR Generic Domain Adapter Specification*.
- OpenETR, *Root and Profile Identity Model*.
- OpenETR, *OpenETR Actor-Neutral Identity Design Note*.
- OpenETR, *System Integration Considerations*.
- OpenETR, *OpenETR CLI JSON Model*.
- OpenETR, *Event Kind Registry*.
- OpenETR, *Linked Evidence Record Kind Design Note*.
- OpenETR, *Agentic AI Needs Consequential Evidence*.
- United Nations Commission on International Trade Law, *Model Law on
  Electronic Transferable Records*.
- United Nations Commission on International Trade Law and UNIDROIT, *Model
  Law on Warehouse Receipts*.
