# OpenETR, LEI, And Verifiable Trade

OpenETR is intended to complement organizational identity infrastructure such as LEI and proto-LEI, and to align with the broader Verifiable.Trade argument for portable, verifiable trade objects.

It should not be framed as a replacement for either.

The clean boundary is:

```text
LEI / proto-LEI:
Who is this organization?

Verifiable trade object models:
How can trade data carry verifiable identity, control, integrity, and state evidence?

OpenETR:
What signed events exist for this digest-identified object, and how does its control or evidence graph evolve?

Recognition policy:
Should this actor, event, graph, or dependency be accepted in this domain?
```

## Complementary Infrastructure

Digital trade needs several layers of trust infrastructure.

Organizational identity is one layer. A relying party needs to know whether a signer, issuer, carrier, bank, warehouse operator, manufacturer, or Competent Authority is the organization it claims to be.

Control and evidence is another layer. A relying party also needs to know what happened to a particular record: who issued it, who transferred it, who attested to it, whether it was encumbered, whether it was redeemed, whether it was superseded, and which evidence supports those conclusions.

OpenETR belongs primarily to the second layer.

It can use LEI, proto-LEI, registries, trust frameworks, credentials, and Verifiable.Trade-style reference layers as recognition inputs.

It should not require any one identity system in the base protocol.

## LEI And proto-LEI Role

The LEI provides a globally standardized identifier for legal entities where coverage exists.

The proto-LEI concept points toward a broader global reference layer that can connect local business registries and fragmented identifiers without replacing those authoritative sources.

For OpenETR, this is valuable because profile keys are cryptographic signers, not full organizational identity records.

An OpenETR verifier may need to resolve:

```text
profile npub
  -> claimed organization reference
  -> LEI / proto-LEI / local registry identifiers
  -> legal entity and status
  -> domain authorization
  -> recognition outcome
```

This can help answer practical questions:

- Is this profile linked to the carrier named in the bill of lading?
- Is this warehouse operator recognized for this receipt workflow?
- Is this bank the secured lender it claims to be?
- Is this manufacturer the issuer of the Product Passport?
- Is this authority competent for this Apostille evidence?
- Is this organization active, dissolved, merged, renamed, or otherwise changed?

The organizational reference strengthens recognition. It does not replace the OpenETR event signature or object graph.

## Verifiable Trade Alignment

The Verifiable.Trade articles argue for trade data that carries verifiable evidence of origin, control, integrity, authority, and state transitions across organizations.

OpenETR is compatible with that direction.

It provides a concrete control/evidence graph pattern:

```text
record artifact or canonical package
  -> digest
  -> signed origin event
  -> signed control, attestation, and evidence events
  -> verifier evaluates graph
  -> recognition policy decides effect
```

This aligns especially well with MLETR-style concerns:

- integrity
- exclusive control
- singularity of authoritative control state
- transfer of control
- presentation
- surrender or termination
- evidence portability across systems

OpenETR should remain careful, though. It should not claim to compute the complete legal state of a trade transaction. It records the signed evidence needed for a verifier or domain adapter to evaluate state.

## Identity Plus Object History

LEI and proto-LEI help identify organizations.

OpenETR helps preserve object history.

Both are needed.

An organization may be perfectly identified, but a verifier still needs to know what that organization did to a specific record.

Likewise, an OpenETR graph may be cryptographically valid, but a verifier still needs to know whether the signer maps to a recognized legal entity or role.

The architecture should therefore compose the layers:

```text
organizational reference
  -> resolves who the actor is

OpenETR graph
  -> records what the actor signed about the object

domain adapter
  -> explains the event in domain language

recognition policy
  -> decides whether to rely on it
```

## Dependency Integrity

The Verifiable.Trade discussion of dependency integrity is also useful for OpenETR.

Trade records do not stand alone. A bill of lading may support financing. A warehouse receipt may support insurance. A certificate of origin may support customs treatment. A Product Passport may depend on component certifications or repair evidence.

OpenETR can support dependency integrity by making cross-object relationships explicit:

```text
object A changes
  -> related object B may require warning, revalidation, notice, or manual review
  -> recognition policy decides the effect
```

This is not a hidden legal engine.

It is signed dependency evidence that domain adapters and verifiers can inspect.

## Fabric, Not Platform

OpenETR is not intended to become the single platform for digital trade.

Existing systems can keep their own:

- registries
- account systems
- ERP and logistics workflows
- bank platforms
- carrier systems
- customs environments
- credential ecosystems
- identity providers
- domain rulebooks

OpenETR can provide portable signed evidence that moves between them.

That makes it complementary to LEI, proto-LEI, Verifiable.Trade-style reference layers, and trust registries.

The shared goal is not centralization. It is interoperability.

## Non-Replacement Position

OpenETR should not claim to replace:

- LEI
- proto-LEI
- business registers
- trust registries
- Verifiable.Trade protocols or governance
- identity wallets
- KYC or AML systems
- domain platforms
- legal recognition frameworks

It should claim something narrower and more useful:

```text
OpenETR gives digest-identified records portable signed control and evidence graphs.
Those graphs can be evaluated with organizational reference layers and recognition policies.
```

## Policy Position

The recommended policy position is:

```text
Use LEI / proto-LEI to strengthen organizational reference.
Use OpenETR to preserve object-specific control and evidence history.
Use Verifiable.Trade-style trust and state-transition thinking to guide interoperability.
Keep recognition decisions explicit and domain-specific.
```

That composition avoids a common mistake in digital trade architecture: expecting one system to be identity layer, control layer, registry, legal engine, document platform, and business application all at once.

OpenETR is strongest when it remains the portable evidence fabric.

## Source Specifications

- [OpenETR Organizational Reference Layer Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_ORGANIZATIONAL_REFERENCE_LAYER_DESIGN_NOTE.md)
- [OpenETR Dependency Integrity Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_DEPENDENCY_INTEGRITY_DESIGN_NOTE.md)
- [OpenETR Generic Domain Adapter Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [OpenETR TRQP Integration Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_TRQP_INTEGRATION_NOTE.md)

