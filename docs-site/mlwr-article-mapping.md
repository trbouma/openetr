# MLWR Article Mapping

The MLWR article mapping tracks how OpenETR evidence could be recognized under, or given effect by, Model Law on Warehouse Receipts requirements.

The mapping is intentionally about **recognition and effect**. Those questions are technically outside the base OpenETR protocol, but they are closely mapped to protocol evidence such as object digests, signed control records, current-controller derivation, attestations, and verifier policy output.

OpenETR can show what was signed, linked, retrieved, transferred, pledged, discharged, presented, or terminated. MLWR-style law, registry rules, contracts, institutional policy, courts, and verifiers decide what legal or operational effect follows.

## How To Read The Mapping

The mapping distinguishes between:

| Category | Meaning |
| --- | --- |
| Protocol evidence | OpenETR provides digest, signature, event, graph, or verification evidence relevant to the article. |
| Supported by adapter | The Warehouse Receipts workspace uses domain language or workflow mapping that helps present that evidence. |
| Recognition / effect | OpenETR can provide evidence, but legal effect depends on law, registry, policy, or verifier recognition. |
| Gap / design note | More design work is needed. |

## Current Focus

The current strongest coverage is around:

- terminology mapping;
- electronic receipt identity by digest;
- initial control-record evidence;
- control event evidence;
- transfer and control graph reconstruction;
- recognition boundary documentation.

Some articles require deeper policy or domain design. Those are intentionally tracked as gaps rather than hidden.

## Source Mapping

The working table is maintained in:

- [MLWR Article Requirements Mapping](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_ARTICLE_REQUIREMENTS_MAPPING.md)

Related profile notes:

- [OpenETR MLWR Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_MLWR_PROFILE.md)
- [MLWR Change Of Medium Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_CHANGE_OF_MEDIUM_PROFILE.md)
- [MLWR Receipt Replacement And Loss Profile](https://github.com/trbouma/openetr/blob/main/docs/specs/MLWR_RECEIPT_REPLACEMENT_AND_LOSS_PROFILE.md)
