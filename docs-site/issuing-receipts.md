# Issuing Receipts

Issuance is the first warehouse receipt workflow.

The warehouse operator creates or obtains a receipt document, then OpenETR commits to that exact artifact by digest.

## Minimal Issuance Evidence

An OpenETR origin event records:

| Evidence | Description |
| --- | --- |
| Receipt digest | SHA-256 digest of the uploaded document. |
| Object tag `o` | Digest-addressed object identity. |
| Origin event id | Event id of the signed issuance event. |
| Issuer profile | Nostr public key of the selected profile signer. |
| Signature | Nostr event signature over the event payload. |
| Structured tags | Signed metadata such as `name`, `size_bytes`, `digest_generated_at`, `domain`, `document_type`, `record_reference`, and `record_description`. |

The file itself remains wherever the warehouse operator or integrated system stores it.

## What OpenETR Does Not Parse

For the base use case, OpenETR does not decide whether the warehouse receipt content is legally sufficient.

Out of scope for the base protocol:

- goods quantity validation;
- grade, weight, quality, or inspection validation;
- warehouse terms and conditions;
- warehouse licensing or bonding;
- KYC or AML checks;
- whether the warehouse actually holds the goods;
- legal effect under a particular enactment.

Those issues belong to domain systems, legal frameworks, registries, attestors, and verifier policies.

## Domain Fields

The MLWR webapp presents fields such as:

| UI Label | OpenETR Tag |
| --- | --- |
| Receipt reference | `record_reference` |
| Goods description | `record_description` |

These are signed event tags. They are not recovered by parsing the event content string.

The event `content` field is reserved for a short human-readable narrative.

## Source Notes

- [MLWR Warehouse Operator Issuance Use Case](https://github.com/trbouma/etrix/blob/main/docs/specs/MLWR_WAREHOUSE_OPERATOR_ISSUANCE_USE_CASE.md)
- [OpenETR Nostr Wire Format](https://github.com/trbouma/etrix/blob/main/docs/specs/OPENETR_NOSTR_WIRE_FORMAT_SPEC.md)

