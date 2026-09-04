# China Electronic Warehouse Receipts

China's ten-agency *Provisions on Promoting and Regulating the Application of
Electronic Documents*, Order No. 22, took effect on 1 September 2026. The
regulation creates a valuable research and pilot context for OpenETR warehouse
receipts because it separately addresses transferable-document control, user
identity, and reliable-system considerations.

The [official Chinese text](https://shanxi.chinatax.gov.cn/web/detail/sx-11400-545-1820386)
includes requirements concerning document uniqueness, exclusive control,
controller identification, transfer of control, identity verification,
traceability, security, continuity, and audit.

## OpenETR Mapping Direction

The technical mapping will examine:

```text
Digital Artifact digest
  -> DCR evidence
  -> derived controller and exclusive-control state
  -> transfer, pledge, discharge, and termination
```

It will separately examine:

```text
user identity verification
  -> warehouse-operator recognition
  -> operating and custody controls
  -> audit and reliable-system evidence
  -> legal recognition and effect
```

## Central Research Question

OpenETR permits identical copies of a Digital Artifact because they resolve to
the same content digest. Originality comes from consequential state, not copy
prevention.

The central question is whether legal uniqueness under the Chinese regime can
be satisfied by singular, verifiable consequential and control state. That is
a plausible technical interpretation, but it requires Chinese legal or
regulatory validation before being presented as a compliance conclusion.

OpenETR does not currently claim that a valid DCR, a public relay pool, or a
signing key independently satisfies the regulation's complete requirements.

Read the detailed [China electronic warehouse-receipt review note](https://github.com/trbouma/openetr/blob/main/docs/specs/OPENETR_CHINA_ELECTRONIC_WAREHOUSE_RECEIPTS_REVIEW_NOTE.md).

