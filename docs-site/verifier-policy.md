# Verifier Policy

OpenETR is an open signed-event system.

Any organization can write its own verifier rule book on top of the OpenETR event graph.

## Baseline Verifier

The generic verifier should inspect:

- event signatures;
- event kinds;
- object tag `o`;
- action tags;
- prior-event links through `e`;
- participant tags;
- encumbrance references;
- lifecycle state;
- known or unknown npubs.

When a transition breaks a rule, the generic verifier should report a warning rather than erase the event or raise an unrecoverable error.

## Domain Verifiers

An MLWR verifier can add domain-specific policy:

- whether an issuer is a recognized warehouse operator;
- whether a holder is recognized;
- whether an encumbrance is effective;
- whether a discharge was signed by an appropriate releasing party;
- whether a termination event should be accepted;
- whether a change of medium is recognized;
- whether KYC, registry, TRQP, or Web of Trust evidence is sufficient.

## Recognition Boundary

OpenETR focuses on control.

Recognition concerns sit above it:

- KYC;
- legal entity mapping;
- warehouse licensing;
- registry status;
- attestation;
- Web of Trust;
- Trust Registry Query Protocol;
- jurisdiction-specific effect.

This is similar to TCP/IP supporting applications without enforcing application-level policy. The protocol can carry identifiers and signed facts; the integrating system decides which facts it recognizes.

## Source Notes

- [OpenETR Generic Verifier Policy](https://github.com/trbouma/etrix/blob/main/docs/specs/OPENETR_GENERIC_VERIFIER_POLICY.md)
- [OpenETR TRQP Integration Note](https://github.com/trbouma/etrix/blob/main/docs/specs/OPENETR_TRQP_INTEGRATION_NOTE.md)
- [OpenETR Nostr Web Of Trust Integration Note](https://github.com/trbouma/etrix/blob/main/docs/specs/OPENETR_NOSTR_WEB_OF_TRUST_INTEGRATION_NOTE.md)

