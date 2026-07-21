# Recognition Boundary

OpenETR is focused on control-layer evidence.

Recognition frameworks decide what effect to give that evidence.

The recurring pattern is:

```text
real-world object, product, document, or record
  -> canonical file or data artifact
  -> digest
  -> signed origin record
  -> signed control records or linked evidence records
  -> verifier, registry, authority, or relying party decides effect
```

OpenETR does not decide effect. It provides the control layer and preserves the evidence that a recognition layer can evaluate.

## Control Questions

OpenETR can answer questions such as:

- what object digest is being referenced?
- which origin event created the object record?
- which signed events reference the same object?
- how do control events link through `e` references?
- which profile key signed each event?
- what candidate control state can be derived from the graph?
- which linked evidence records point back to the object?

## Recognition Questions

Other systems decide questions such as:

- is this signer legally authorized?
- is the issuer recognized as a warehouse operator?
- does this profile satisfy KYC or onboarding requirements?
- does a registry recognize the event?
- does a statute give legal effect to the transition?
- should a transfer, encumbrance, discharge, redemption, or termination be accepted under a policy?

## Recognition Inputs

Recognition may depend on:

- local allow lists or known entities;
- contacts and references;
- TRQP;
- Web of Trust;
- OpenETR attestation events;
- KYC providers;
- registries;
- enterprise account systems;
- contractual network rules;
- statutory or regulatory requirements.

## Verifier Rule Books

Because OpenETR is an open signed-event system, any organization can write a verifier rule book on top of the same graph.

A generic verifier should expose warnings rather than pretending invalid or unrecognized transitions do not exist.

A domain verifier can add stronger rules, safeguards, or exemptions.

## Source Specs

- [OpenETR Generic Verifier Policy](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR TRQP Integration Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_TRQP_INTEGRATION_NOTE.md)
- [OpenETR Nostr Web Of Trust Integration Note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_NOSTR_WEB_OF_TRUST_INTEGRATION_NOTE.md)
- [ZK-SNARKs And Hash Commitments Design Note](https://github.com/trbouma/openetr/blob/main/docs/specs/ZK_SNARKS_AND_HASH_COMMITMENTS_DESIGN_NOTE.md)
