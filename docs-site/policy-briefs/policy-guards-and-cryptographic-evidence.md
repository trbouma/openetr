# Policy Guards And Cryptographic Evidence

OpenETR is unequivocal about publishing evidence.

It records digest-identified objects, signed origin records, linked control records, and related evidence in a form that can be retrieved, replayed, and independently verified.

But OpenETR is equally clear about what that evidence does not do by itself.

A signed event is not universal recognition. A cryptographically valid control graph is not automatic legal, regulatory, commercial, or institutional effect. Recognition depends on the rule book by which the evidence is evaluated.

That distinction is central to OpenETR.

```text
Cryptographic evidence shows what was signed.
Policy guards describe what a system should allow.
Recognition decides what effect the evidence receives.
```

The operating principle is:

```text
Transact globally.
Validate locally.
```

OpenETR lets evidence move through a shared digital environment, while leaving recognition to the party, institution, registry, authority, or rule book that must decide whether to rely on it.

## The High Seas Analogy

Global trade has always had to operate across boundaries.

Maritime commerce developed long before any single sovereign, port, registry, or platform could govern trade end to end. Ships, cargo, receipts, bills of lading, financing arrangements, insurance claims, and court disputes moved across jurisdictions.

Commerce at sea therefore depended on records, customs, signatures, possession, endorsement, attestation, and recognition practices that could travel.

The high seas were not the domain of one database or one legal authority.

What mattered was whether a record, claim, or act would be recognized by the party who needed to rely on it.

OpenETR is trying to recreate that operating discipline for durable electronic records.

It supports publication in a shared environment, movement across institutional boundaries, reliance on signed and reviewable evidence, and recognition by the relevant relying party rather than by a single controlling system.

That is why OpenETR should not confuse evidence with universal effect.

## The Evidence Layer

OpenETR's base contribution is durable cryptographic evidence.

At the evidence layer, OpenETR can show:

- the digest of the controlled object;
- the origin record that introduced the object into the graph;
- the profile key that signed each event;
- the control records linked to the object;
- the prior-event links between records;
- transfer, acceptance, encumbrance, discharge, redemption, termination, attestation, or linked-evidence actions;
- whether the event ids, signatures, tags, and graph shape can be verified.

These are powerful facts.

They make the control history inspectable without requiring every participant to trust one database, registry, portal, wallet, or platform.

But they are still evidence.

Evidence must be evaluated.

## The Guard Layer

Policy guards are implementation rules that decide whether a particular application, CLI, API, service, registry, or workflow should allow an event to be created, published, accepted, or treated as clean.

For example, a baseline OpenETR guard may ask:

- Is the object digest well formed?
- Can the active control chain be resolved?
- Is the signer the current controller before initiating a transfer?
- Is the signer the intended transferee before accepting a transfer?
- Is the target chain ambiguous?
- Does an encumbrance event being discharged actually exist?
- Has a duplicate action already been published for this object and signer?

These checks matter.

They reduce operator error. They make the reference workflow safer. They give implementers a clear model for ordinary OpenETR behavior. They also make future attestation and verifier-policy work more concrete.

That is why OpenETR is consolidating baseline guards into a shared component used by both the web app and CLI.

The guard model is not limited to transfers. It applies across the control-event set, including:

- `initiate`
- `accept`
- `encumber`
- `discharge`
- `redeem`
- `terminate`
- `attest`

Transfer is the clearest example because it changes controller state. But the same guard pattern applies whenever the reference implementation needs to decide whether a control-relevant action is well formed, properly linked, consistent with the apparent graph state, and safe to publish under the baseline policy.

The goal is a reference implementation that supports the majority of expected scenarios out of the box, while still allowing participants to devise and enforce their own policy guards.

## Guards Are Not Cryptographic Enforcement

Policy guards are not the same thing as cryptographic enforcement.

OpenETR uses signed Nostr events. A relay can accept a structurally valid signed event even if the reference OpenETR component would have refused to publish it. Another implementation can also choose a different guard policy.

That does not make guards useless.

It means guards should be understood correctly.

A baseline guard says:

> This implementation is willing to publish or process this event under its configured policy.

It does not say:

> Every relying party must recognize this event as effective.

The downstream verifier still has work to do.

## The Recognition Layer

Recognition is where the rule book enters.

A rule book may be legal, regulatory, contractual, institutional, commercial, operational, or private. It may be implemented by a registry, platform, regulator, bank, warehouse operator, marketplace, court, trust framework, enterprise system, or individual verifier.

The recognition layer may ask:

- Is this issuer recognized for this domain?
- Does this profile key map to an authorized organization or role?
- Does a registry recognize this action?
- Does a trust framework require additional credentials or attestations?
- Does a transfer require both initiation and acceptance?
- Does an outstanding encumbrance block transfer recognition?
- Does a termination require a particular actor?
- Does a discharge properly release a recognized encumbrance?
- Does an attestation come from an accepted attestor?
- Are the required domain-specific fields present?
- Is this evidence sufficient for the relying party's purpose?

These questions cannot be answered by signatures alone.

They depend on context.

## Same Evidence, Different Rule Books

Two verifiers may inspect the same OpenETR graph and reach different recognition conclusions.

That is not a protocol failure.

It is the expected result of keeping evidence and recognition separate.

For example:

- A warehouse receipt registry may require an issuer profile recognized as a warehouse operator.
- A bank may require KYC, secured-lending rules, and encumbrance disclosure.
- A marketplace may require a recognized manufacturer or Product Passport issuer.
- A customs authority may require registry status and product-category rules.
- A private counterparty workflow may accept a lighter operational rule book.

Each can evaluate the same signed evidence without requiring a different OpenETR protocol.

The protocol preserves the control evidence.

The rule book determines effect.

## Why The Reference Implementation Matters

If guards are not universal enforcement, why build them into the reference implementation?

Because most users should not have to assemble the baseline control model from scratch.

The reference implementation should provide a practical default:

- friendly input resolution at the edge;
- canonical hex identifiers inside;
- baseline guard checks before publishing;
- consistent behavior across the CLI and web app;
- clear warnings and errors;
- inspectable verifier-policy output;
- extension points for stricter domain policies.

This gives ordinary deployments a solid starting point.

It also gives specialized deployments a place to customize.

A warehouse receipt network, Product Passport registry, Apostille authority, health-records system, secured lender, or private consortium should be able to replace or extend the default guard policy without changing the base OpenETR wire format.

This is not an attempt to make OpenETR closed.

It is an attempt to make the baseline behavior consistent, reviewable, testable, and replaceable.

That is the right balance:

```text
shared evidence substrate
  + reference baseline guards
  + local rule books
  = interoperable control with contextual recognition
```

## Policy Implication

Many digital trust systems struggle because they try to make one layer do everything.

They ask one platform, one registry, one wallet, one credential, or one smart contract to be the evidence layer, the rule book, the enforcement mechanism, and the recognition authority.

OpenETR takes a different approach.

It separates:

- cryptographic evidence: what was signed and how it links to the object;
- policy guards: what an implementation allows or warns about;
- verifier policy: how a relying party evaluates the graph;
- recognition: what effect the relying party gives the evidence.

This separation makes OpenETR more useful for real institutional environments.

It lets evidence travel across systems while letting rule books remain accountable to the domains, laws, contracts, registries, and communities that actually rely on them.

## Source Specifications

- [Recognition Boundary](../openetr/recognition.md)
- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Control Event Policy Guards Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROL_EVENT_POLICY_GUARDS_DESIGN_NOTE.md)
- [Identifier Resolution Rules](https://github.com/trbouma/openetr/blob/main/docs/specs/IDENTIFIER_RESOLUTION_RULES.md)
- [Control Event Minimum Shapes](https://github.com/trbouma/openetr/blob/main/docs/specs/CONTROL_EVENT_MINIMUM_SHAPES.md)
- [OpenETR Layered Architecture Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_LAYERED_ARCHITECTURE_NOTE.md)
