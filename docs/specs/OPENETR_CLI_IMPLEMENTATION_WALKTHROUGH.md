# OpenETR CLI Implementation Walkthrough

This note connects the current OpenETR specifications to the reference CLI behavior.

It is not a separate protocol specification. It is a practical map from the current specs to the commands and event shapes implemented by the CLI.

## Status

Draft, reflecting the current `openetr` CLI implementation.

## Spec-To-Implementation Map

The current CLI implements the Nostr wire model described in [OPENETR_NOSTR_WIRE_FORMAT_SPEC.md](./OPENETR_NOSTR_WIRE_FORMAT_SPEC.md).

At a high level:

- `openetr issue-etr` publishes a `kind 31415` origin event
- `openetr transfer initiate` publishes a `kind 31416` event with `action=initiate`
- `openetr transfer accept` publishes a `kind 31416` event with `action=accept`
- `openetr terminate-etr` publishes a `kind 31416` event with `action=terminate`
- `openetr attest` publishes a `kind 31416` event with `action=attest`
- `openetr encumber` publishes a `kind 31416` event with `action=encumber`
- `openetr discharge` publishes a `kind 31416` event with `action=discharge`
- `openetr redeem` publishes a `kind 31416` event with `action=redeem`
- `openetr query-etr` queries the origin and control-event families and derives the current object state

The implementation constants for these actions live in `openetr/control.py`.

## Identity Setup

The CLI uses the root/profile model described in [ROOT_AND_PROFILE_IDENTITY_MODEL.md](./ROOT_AND_PROFILE_IDENTITY_MODEL.md).

Create or update a profile with relay and query defaults:

```bash
openetr profile set warehouse \
  --relays wss://relay.openetr.org \
  --kind 31415 \
  --query-timeout 10 \
  --publish-wait 2.0 \
  --limit 20 \
  --query-output full
```

Publish the public profile metadata:

```bash
openetr profile publish \
  --profile warehouse \
  --name "Delhi Warehouse" \
  --display-name "Warehouse" \
  --about "Warehouse custodian profile" \
  --address "123 Startop Way, Delhi, India" \
  --force
```

Use the profile as the active signer:

```bash
openetr profile use warehouse
openetr whoami
```

Inspect the root administrative identity and controlled profiles:

```bash
openetr root
```

## Issue An Object

Issue a controlled object from a local file:

```bash
openetr issue-etr examples/MLWR001.pdf
```

Implementation mapping:

- event kind: `31415`
- `d` tag: object digest hex
- `o` tag: object digest hex
- signer: active profile signer unless overridden
- object digest: SHA-256 of the source file

The same command can be used with other files, such as:

```bash
openetr issue-etr examples/ebl6.md
```

## Query Object State

Query the current state and control history:

```bash
openetr query-etr examples/MLWR001.pdf
```

The query command resolves:

- the initial origin event
- matching `kind 31416` control events
- control-event chains linked by `e` tags
- lifecycle state, including active, redemption-pending, or terminated
- current controller
- profiles for relevant signers and participants where available
- encumbrance summary, including outstanding and discharged encumbrances

This is the main CLI surface for verifying the effect of the event shapes described in the wire-format and control-event specs.

## Transfer Control

Initiate a transfer from the current controller to another profile:

```bash
openetr transfer initiate examples/MLWR001.pdf --transferee exporter
```

Implementation mapping:

- event kind: `31416`
- `action`: `initiate`
- `d`: `<object_hex>:initiate`
- `o`: `<object_hex>`
- `e`: prior origin or control event id
- `p`: transferee pubkey

The transferee accepts after switching profiles:

```bash
openetr profile use exporter
openetr transfer accept examples/MLWR001.pdf
```

Implementation mapping:

- event kind: `31416`
- `action`: `accept`
- `d`: `<object_hex>:accept`
- `o`: `<object_hex>`
- `e`: transfer initiate event id or prior control event id selected by the implementation

The query output should then show the exporter as the current controller if the local recognition logic accepts the transfer chain.

## Encumber And Discharge

Declare an encumbrance in favor of a beneficiary profile:

```bash
openetr encumber examples/MLWR001.pdf \
  --beneficiary lender \
  --type pledge \
  --ref encumbrance-MLWR001-001
```

Implementation mapping:

- event kind: `31416`
- `action`: `encumber`
- `d`: `<object_hex>:encumber`
- `o`: `<object_hex>`
- `e`: prior origin or control event id
- `p`: beneficiary or secured-party pubkey
- optional `type`: encumbrance subtype, such as `pledge`
- optional `ref`: external reference

Discharge a specific encumbrance by referencing the encumbrance event id:

```bash
openetr discharge examples/MLWR001.pdf \
  --encumbrance-event <encumbrance_event_id_or_nevent> \
  --releasing-party lender \
  --ref discharge-MLWR001-001
```

Implementation mapping:

- event kind: `31416`
- `action`: `discharge`
- `d`: `<object_hex>:discharge`
- `o`: `<object_hex>`
- `e`: prior origin or control event id
- `enc`: encumbrance event id being discharged
- optional `p`: beneficiary or releasing-party pubkey
- optional `ref`: external reference

`openetr query-etr` reports encumbrances as:

- total encumbrances
- discharged encumbrances
- outstanding encumbrances
- detail for each outstanding encumbrance, including beneficiary, type, and ref where present

## Redeem And Terminate

Record presentation to an obligor:

```bash
openetr redeem examples/MLWR001.pdf \
  --obligor warehouse \
  --ref redemption-MLWR001-001
```

Implementation mapping:

- event kind: `31416`
- `action`: `redeem`
- `d`: `<object_hex>:redeem`
- `o`: `<object_hex>`
- `e`: prior origin or control event id
- `p`: obligor pubkey
- optional `ref`: external reference

The reference query logic treats redeem as moving the object into a redemption-pending lifecycle state.

Terminate the active lifecycle:

```bash
openetr terminate-etr examples/MLWR001.pdf
```

Implementation mapping:

- event kind: `31416`
- `action`: `terminate`
- `d`: `<object_hex>:terminate`
- `o`: `<object_hex>`
- `e`: prior origin or control event id

The reference query logic treats terminate as ending the active lifecycle when recognized.

## Web App Query Surface

The web app uses the same query service as the CLI for object-state evaluation.

When a user uploads or queries a document, the result page should expose the same derived state as `openetr query-etr`, including:

- origin event
- matching control events
- summary control chains
- lifecycle state
- current controller
- encumbrance summary and outstanding encumbrances

## Notes On Recognition

The CLI publishes and queries signed wire-level events.

It does not by itself decide legal title, mandate, priority, perfection, or binding effect.

Those questions remain part of the recognition layer described in the canonical and generic transfer specs.
