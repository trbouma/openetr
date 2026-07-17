# ZK-SNARKs And Hash Commitments In OpenETR

This note records the current OpenETR design position on ZK-SNARKs and similar zero-knowledge proof systems.

## Status

Design note.

OpenETR is not currently pursuing ZK-SNARKs as part of the base protocol.

The current position is that SHA-256 object commitments, Nostr signatures, and signed control-event graphs are sufficient for the core OpenETR protocol goals.

ZK proofs may still be useful as optional domain-adapter, attestation, or recognition-layer features where privacy-preserving claims about hidden data are required.

## Core Protocol Question

The base OpenETR protocol asks:

> Does this object digest have this signed origin event and this signed control history?

The core primitives are:

- SHA-256 object digest;
- Nostr event signatures;
- `o` tags linking events to the controlled object digest;
- `e` tags linking control events into a graph;
- verifier policy that decides recognition effect.

In short:

```text
hash binds the object
signature binds the actor
event graph binds the control history
policy decides recognition
```

For that purpose, ZK-SNARKs do not add much to the base protocol.

## What SHA-256 Provides

OpenETR currently identifies the controlled object by digest.

For a file-backed record:

```text
document/file -> sha256 digest -> signed OpenETR origin event
```

The digest lets a verifier confirm that:

- the presented file matches the object referenced by the OpenETR origin event;
- later control events refer to the same object through the `o` tag;
- the object identity can be queried and reconstructed across relays or local event stores;
- a different file cannot feasibly be substituted for the same digest.

The security properties OpenETR relies on are:

- preimage resistance: given a digest, it is computationally infeasible to find a file with that digest;
- second-preimage resistance: given one file, it is computationally infeasible to find a different file with the same digest;
- collision resistance: it is computationally infeasible to find two different files with the same digest.

These properties are enough for ordinary object binding.

The verifier does not need to know a secret witness to confirm that a presented file hashes to the digest in the signed event.

## What Signatures Provide

The digest alone does not say who issued or controlled the object.

OpenETR uses signed Nostr events for that.

The event signature lets a verifier confirm that:

- a particular public key signed the origin or control event;
- the event id is bound to the event content and tags;
- the object digest, action tags, participant tags, and graph links are part of the signed statement.

This is the core evidence model.

The protocol does not depend on a platform database asserting that state changed. It depends on signed events that can be independently retrieved and verified.

## Why ZK-SNARKs Are Not In The Base Protocol

ZK-SNARKs are powerful when a party needs to prove a statement about hidden data without revealing the data.

That is not the normal OpenETR base-protocol problem.

For the base protocol, the relevant questions are usually:

- Does this file hash to the object digest?
- Did this issuer sign the origin event?
- Did this controller sign the control event?
- Does this event refer to the same object through `o`?
- Does this event link to the prior event through `e`?
- What candidate control graph can be reconstructed?
- What does the selected verifier policy recognize?

Those questions can be answered using ordinary hash verification, signature verification, event retrieval, and graph traversal.

Adding ZK-SNARKs to the base protocol would increase implementation complexity without improving the ordinary object-identity or control-graph guarantees.

It would also introduce new operational questions:

- Which proving system is required?
- Which circuit definitions are canonical?
- Who maintains trusted setup material, if any?
- Which proof verifier is required by implementations?
- How are proof versions handled?
- How do domain-specific schemas map into generic proof circuits?
- How are failed or missing proofs treated under policy?

Those questions may be appropriate for specialized applications, but they should not be mandatory for every OpenETR implementation.

## Where ZK Proofs Could Add Value

ZK proofs may be useful above the base protocol where a party wants to prove a fact about private or selectively disclosed data.

Examples include:

- proving that a hidden document contains a required field without revealing the full document;
- proving that a receipt amount is within a permitted range without revealing the exact amount;
- proving that goods belong to an allowed category without disclosing detailed commercial information;
- proving that a party holds a credential without revealing the credential itself;
- proving that a document conforms to a schema without publishing all fields;
- proving that an off-chain computation over several private records produced a stated result.

In these cases, the ZK proof would be an additional evidence item.

It could be carried by:

- an OpenETR `attest` event;
- a domain-specific structured tag or content payload;
- an external verifier service referenced by an event;
- a domain adapter that understands a particular proof system;
- a recognition policy that requires or accepts the proof.

The ZK proof would support a recognition or privacy-preserving disclosure policy. It would not replace the object digest, event signature, or control graph.

## Relationship To Recognition Policy

The OpenETR policy boundary is important.

The base protocol should remain neutral about whether a domain requires a ZK proof.

A verifier policy may decide that a ZK proof is:

- not required;
- optional supporting evidence;
- required for a particular domain;
- required only above a threshold amount or for a sensitive field;
- a substitute for direct disclosure;
- insufficient unless combined with a trusted attestor, registry, or KYC recognition source.

Different systems may make different choices while still using the same base OpenETR event graph.

This follows the same philosophy used for KYC, TRQP, Web of Trust, and other recognition inputs:

> OpenETR carries signed control evidence. Domain and verifier policies decide which additional recognition evidence is required.

## Current Decision

OpenETR should not require ZK-SNARKs for the base protocol at this time.

The rationale is:

- SHA-256 already gives the required object-binding commitment;
- Nostr signatures already give signer attribution;
- `o` and `e` tags already give object query and control-graph traversal;
- verifier policy already handles recognition questions;
- ZK proof systems would add significant complexity;
- the main ZK use cases are domain-specific privacy or recognition overlays, not base control mechanics.

Therefore the current design decision is:

```text
Use SHA-256 commitments and signed Nostr events for the base protocol.
Allow ZK proofs as optional higher-layer evidence where a domain adapter or verifier policy needs them.
Do not make ZK-SNARKs mandatory for OpenETR interoperability.
```

## Future Reconsideration Triggers

OpenETR may revisit this decision if a concrete domain requires privacy-preserving proof semantics that cannot be handled well with ordinary hashes, signatures, attestations, and selective disclosure.

Examples that could justify renewed work include:

- a warehouse receipt profile requiring privacy-preserving proof of goods attributes;
- a financing workflow requiring proof of limits without revealing commercial terms;
- a regulator or registry requiring proof of eligibility without public disclosure;
- a widely adopted credential or document proof ecosystem with stable circuits and verifier tooling;
- a partner implementation demonstrating a compelling domain adapter that uses ZK proofs without burdening the base protocol.

Until then, ZK proof work should remain exploratory and optional.
