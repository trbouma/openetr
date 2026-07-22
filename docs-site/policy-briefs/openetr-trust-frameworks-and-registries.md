# OpenETR, Trust Frameworks, And Registries

Trust frameworks try to make digital ecosystems trustworthy by codifying expected behavior.

They define rules, roles, assurance levels, conformity criteria, certification processes, registries, labels, credentials, and governance mechanisms. In many systems, the goal is to make trust more than a vague social expectation. It becomes something that can be assessed, certified, queried, audited, and enforced.

OpenETR fits into that landscape differently.

OpenETR is not itself a full trust framework. It is a general control layer for durable electronic records. Its job is to preserve signed evidence about digest-identified records so trust frameworks, registries, authorities, and relying parties can decide what effect to give that evidence.

## What Trust Frameworks Do

Trust frameworks attempt to answer questions such as:

- Who is allowed to participate?
- What rules must participants follow?
- Which roles exist in the ecosystem?
- Which credentials, attestations, labels, or certifications are acceptable?
- Which registries or authorities are recognized?
- What evidence is required before a service, credential, transaction, or participant is trusted?
- What happens when a participant is suspended, revoked, or no longer compliant?

This is visible in frameworks such as Gaia-X and the Pan-Canadian Trust Framework.

Gaia-X frames its trust framework around technical and organizational standards, compliance criteria, digital clearing-house functions, self-descriptions, verifiable credentials, registries, trust anchors, and ecosystem rule books.

The Pan-Canadian Trust Framework frames digital trust through modular rules, standards, specifications, guidance, conformity assessment, certification, privacy, security, interoperability, and trusted identity services.

In both cases, the framework attempts to codify behavior so that participants can rely on a shared governance model.

## What Registries Do

Registries operationalize recognition.

A registry may answer questions such as:

- Is this issuer admitted?
- Is this participant currently active?
- Is this public key valid or revoked?
- Is this credential type accepted?
- Is this service compliant?
- Is this record registered?
- Which endpoint should be used for discovery?
- Which authority or trust anchor should be consulted?

Registries are therefore recognition infrastructure. They can be public, private, sectoral, jurisdictional, institutional, or ecosystem-specific.

But a registry does not need to be the only place where evidence exists.

That distinction is important.

## What OpenETR Does

OpenETR preserves durable signed evidence about a record.

At the control layer, OpenETR can show:

- the digest of the controlled object;
- the signed origin control record;
- later signed control records;
- linked evidence records;
- event ids, signatures, tags, and graph links;
- which profile key signed each record;
- which candidate control or lifecycle state can be derived;
- which warnings or recognition annotations a verifier produced.

This evidence can then be evaluated by a trust framework, registry, authority, court, platform, marketplace, or relying party.

OpenETR does not decide the final recognition outcome.

It supplies the signed control evidence needed for that decision.

## The Under-Appreciated Layer

Trust frameworks often focus on governance, rules, roles, certification, credentials, and compliance.

Those are necessary.

But durable electronic records also need an object-centric evidence layer:

```text
record or artifact
  -> digest
  -> signed origin control record
  -> signed control records and linked evidence records
  -> verifier policy / registry / trust framework decides effect
```

Without that layer, trust frameworks can become too dependent on one platform, one registry database, one credential presentation, or one application session.

OpenETR makes the object history independently inspectable.

That is the underpinning: not trust by assertion alone, but trust supported by durable signed evidence.

## Fragmentation As A Missing Control Layer

A recent OpenCanada article, **Canada Is Measuring Digital Government Against the Wrong Model**, argues that Canada should not measure digital government only by what appears online. The harder question is whether a federation can make services, data, and responsibilities work across departments, programs, institutions, and jurisdictions.

That diagnosis points to an architectural gap.

Fragmentation is not only a coordination failure. It is also what happens when systems lack a shared control layer for durable records.

Without that layer, each institution tends to ask the same questions again:

- Which record is authoritative?
- Who controls it?
- Who signed or updated it?
- Which source can be trusted?
- Which registry or authority recognizes the actor?
- What evidence survives after the transaction or presentation flow ends?

Trust frameworks can codify expected behavior, and registries can recognize actors or statuses, but they still need durable object-level evidence to evaluate.

OpenETR is aimed at that missing layer. It gives digital-government and trust-framework ecosystems a way to preserve:

- object identity by digest;
- signed origin control records;
- signed lifecycle and control events;
- linked evidence records;
- durable query links and QR codes;
- verifier annotations that distinguish evidence from recognition.

In a federated environment, this matters because the same record may need to be understood by multiple institutions without forcing all of them into one database, one portal, one wallet, or one registry.

The policy point is simple:

```text
Fragmentation is not solved only by putting services online.
It requires shared control evidence that can cross institutional boundaries.
```

## How OpenETR Complements Trust Frameworks

| Trust-framework need | OpenETR contribution |
| --- | --- |
| Evidence of what happened | Signed origin, control, and linked evidence records. |
| Stable object identity | Digest-based Controlled Object identifiers. |
| Auditability | Reconstructable control and evidence graphs. |
| Interoperability | Shared event grammar and object-centric queries. |
| Registry integration | Registries can recognize profile keys, object digests, event ids, and graph states. |
| Policy overlays | Different rule books can evaluate the same signed evidence without forking the protocol. |
| Revocation or suspension evidence | Authority notices, registry references, attestations, or linked evidence can be attached to the graph. |

OpenETR therefore gives trust frameworks something concrete to evaluate.

The framework can still define the behavior. The registry can still decide recognition. OpenETR preserves the durable signed evidence underneath.

## Gaia-X Example

Gaia-X uses trust-framework concepts to support compliance, technical compatibility, policy rules, trust anchors, digital clearing-house services, self-descriptions, and verifiable credentials.

OpenETR could complement such an ecosystem by providing object-centric evidence for controlled records that participate in a data space or compliance process.

For example, OpenETR could record:

- a service-offering evidence artifact by digest;
- a signed origin record for that artifact;
- linked evidence records for certifications, audits, or compliance checks;
- registry references to trust anchors or labels;
- verifier output under a Gaia-X-style rule book.

Gaia-X-style governance would still decide compliance and recognition.

OpenETR would preserve what was signed, by whom, about which object, and in what graph relationship.

## Pan-Canadian Trust Framework Example

The Pan-Canadian Trust Framework is focused on trustworthy digital identity, credential, authentication, privacy, security, and supporting services.

OpenETR does not replace that identity and assurance framework.

Instead, OpenETR could support durable records that rely on PCTF-style recognition inputs.

For example:

- a credential or attestation may help prove that an organization is recognized;
- a registry may confirm the status of a service provider;
- a verifier policy may require a particular assurance level;
- OpenETR can record the object-specific event signed by the recognized profile key.

The trust framework answers who and under what rules.

OpenETR answers what happened to the record.

## Registries Without Total Custody

One important implication is that registries do not have to host every record.

A registry can:

- recognize issuers;
- map profile keys to organizations;
- publish status, suspension, or revocation information;
- index object digests and endpoints;
- define accepted schemas or event types;
- provide recognition responses to verifiers.

The actual record artifact can remain with an issuer, platform, storage service, archive, holder, or sector-specific system.

OpenETR gives the registry a digest and signed graph to reference.

That reduces pressure to make the registry both governance authority and universal storage provider.

## Recognition Queries

Trust registries become especially useful when a verifier needs to ask:

```text
Is this actor recognized for this action on this resource under this authority?
```

The Trust Over IP **Trust Registry Query Protocol (TRQP)** is a useful example of this pattern. TRQP gives verifiers a standard way to query a trust registry for authorization or recognition information without making that registry the source of the OpenETR graph.

That maps naturally to OpenETR:

- actor: the signer profile key or mapped organization;
- action: issue, transfer, attest, encumber, discharge, redeem, terminate, or link evidence;
- resource: warehouse receipt, Product Passport, Apostille document, service offering, credential, or another durable record type;
- authority: the trust framework, registry, regulator, institution, or governance body.

OpenETR can show that the actor signed the event.

TRQP or another trust-registry interface can say whether that actor is authorized or recognized for that action and resource.

The verifier decides what effect follows.

## Why This Matters For Policy

Policy discussions often treat trust as something created by rules and compliance alone.

Rules matter. Compliance matters. Registries matter.

But durable electronic records also need evidence that can survive outside a single platform and be inspected later by different parties.

OpenETR gives policymakers a way to separate:

- the control layer: what the signed graph shows;
- the trust framework: what behavior and assurance rules apply;
- the registry: which actors, authorities, statuses, or records are recognized;
- the verifier: what effect to give the evidence in context.

That separation is useful because it lets sectors adopt shared digital-record infrastructure without forcing one trust framework to become the whole technical stack.

## What OpenETR Should Not Claim

OpenETR should not claim to be:

- a complete trust framework;
- a conformity assessment program;
- a certification authority;
- a trust registry;
- a compliance engine;
- a governance authority;
- a legal recognition engine.

Instead, OpenETR should claim the narrower and more durable role:

```text
A general control layer that preserves signed evidence for durable electronic records.
```

Trust frameworks codify behavior.

Registries operationalize recognition.

OpenETR preserves the evidence they need to evaluate.

## Source Specifications

- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR And TRQP Integration Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_TRQP_INTEGRATION_NOTE.md)
- [OpenETR And Nostr Web Of Trust Integration Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WEB_OF_TRUST_INTEGRATION_NOTE.md)
- [Why Control Is Not Recognition](why-control-is-not-recognition.md)

## External References

- [Gaia-X Trust Framework Architecture](https://docs.gaia-x.eu/technical-committee/architecture-document/25.05/trust_framework_architecture/)
- [Gaia-X Trust Framework](https://docs.gaia-x.eu/policy-rules-committee/trust-framework/22.10/)
- [Pan-Canadian Trust Framework](https://diacc.ca/trust-framework/)
- [PCTF Overview](https://diacc.ca/overview/)
- [ToIP Trust Registry Query Protocol v2.0 Approved Specification](https://trustoverip.github.io/tswg-trust-registry-protocol/approved/)
- [Canada Is Measuring Digital Government Against the Wrong Model](https://opencanada.org/canada-is-measuring-digital-government-against-the-wrong-model/)
