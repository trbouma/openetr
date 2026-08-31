# System Integrators

OpenETR is designed to fit inside existing systems rather than replace them.

A system integrator may already have:

- user accounts and authentication
- KYC or onboarding controls
- business workflows
- document storage
- registries or platform databases
- APIs, queues, and audit logs
- domain-specific rulebooks
- legal or institutional recognition requirements

OpenETR adds a portable control-evidence layer underneath those systems.

The shortest description is:

```text
your system keeps the workflow
OpenETR signs the control evidence
your verifier policy decides what to rely on
```

## Where OpenETR Fits

OpenETR is useful when an electronic record needs durable evidence of lifecycle state.

That includes records that may be issued, transferred, pledged, released, presented, surrendered, redeemed, terminated, replaced, or linked to supporting evidence.

The host system remains responsible for the user-facing product. OpenETR provides the signed object-centric graph that can travel between systems.

```text
Host application
  accounts, roles, UX, document storage, workflow, domain policy

OpenETR
  artifact digest, Anchor record, control records, linked evidence,
  dependency edges, verifier output

Recognition layer
  law, registry rules, institutional policy, contracts, relying-party decisions
```

## Common Integration Questions

| Question | Integration Answer |
| --- | --- |
| Do we need to replace our application? | No. OpenETR is intended to sit behind existing workflows. |
| Does OpenETR store the document? | Not necessarily. OpenETR can identify the document by digest while the host system stores the content. |
| Does OpenETR perform KYC? | No. KYC and account binding belong to the host system or an external provider. |
| Does OpenETR decide legal effect? | No. It preserves evidence. Recognition belongs to law, registries, contracts, institutional policy, or verifier rulebooks. |
| Can events move through our API instead of Nostr? | Yes, if the signed event data and graph links are preserved. Nostr is the reference wire format, not the only possible transport pattern. |
| Can OpenETR be invisible to end users? | Yes. The host application can expose domain actions while OpenETR signs and verifies evidence behind the scenes. |

## Suggested Reading Path

Start with:

- [How OpenETR Fits](fit.md)
- [Integration Patterns](patterns.md)
- [Boundaries And Responsibilities](boundaries.md)

Then read the core OpenETR pages:

- [OpenETR Overview](../openetr/index.md)
- [Control Layer](../openetr/control-layer.md)
- [Integration Model](../openetr/integration.md)
- [Recognition Boundary](../openetr/recognition.md)
- [Component And CLI](../openetr/component-and-cli.md)
- [Nostr Wire Format](../openetr/wire-format.md)

For domain-specific integration:

- [Warehouse Receipts](../getting-started.md)
- [Warehouse Receipt Pilot Boundary Notes](../warehouse-receipt-pilot.md)
- [Bills of Lading](../bills-of-lading.md)
- [Product Passports](../product-passports.md)
- [Apostille Documents](../apostille-documents.md)

For deeper specification work:

- [System Integration Considerations](https://github.com/trbouma/openetr/blob/main/docs/specs/SYSTEM_INTEGRATION_CONSIDERATIONS.md)
- [Generic Domain Adapter Specification](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_DOMAIN_ADAPTER_SPEC.md)
- [Root And Profile Identity Model](https://github.com/trbouma/openetr/blob/main/docs/specs/ROOT_AND_PROFILE_IDENTITY_MODEL.md)
- [Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [Specification Index](https://github.com/trbouma/openetr/blob/main/docs/specs/INDEX.md)
