# Canonical ETR Transaction Infographic

This note is a simplified visual companion to [CANONICAL_ETR_TRANSACTION_SPEC.md](./CANONICAL_ETR_TRANSACTION_SPEC.md).

It is intended to help readers quickly visualize the canonical model without replacing the full specification.

Diagram legend:

- solid lines denote lifecycle or control-state progression
- dotted lines denote witness, attestation, or recognition association rather than state transfer

## 1. Core Logic

```mermaid
flowchart LR
    A["Declare<br>substantive action or assertion"] --> B["Attest<br>accountable recognition or validation"]
    B --> C["Recognize<br>effect under policy"]
```

Key idea:

- publication alone does not equal effect
- effect depends on recognition
- attestation provides the stronger basis for recognition

## 2. Canonical Action Families

```mermaid
flowchart TD
    O["Controlled Object"] --> I["Issue"]
    O --> T["Transfer"]
    O --> E["Encumber"]
    O --> D["Discharge"]
    O --> R["Redeem"]
    O --> X["Terminate"]
```

Key idea:

- `Issue`, `Transfer`, `Encumber`, `Discharge`, `Redeem`, and `Terminate` are lifecycle-relevant actions
- attestation is not shown as a lifecycle action family here because it operates as a witness or recognition layer attached to relevant events

## 3. Transfer in the Strong Canonical Model

```mermaid
flowchart LR
    A["Current Controller"] --> B["Declare Transfer"]
    C["Counterparty"] --> D["Accept Transfer"]
    B --> E["Recognized<br>as transfer action set"]
    D --> E
    F["Attested"] -.-> B
    F -.-> D
    E --> G["New Current Controller"]
```

Key idea:

- the strong canonical model treats transfer as more than mere publication
- recognition depends on the declared transfer action set
- attestation may attach to the relevant transfer events without itself being a state transition

## 4. Narrow Trusted-Counterparty Variant

```mermaid
flowchart LR
    A["Current Controller"] --> B["Declare Transfer"]
    C["Counterparty"] --> D["Accept Transfer"]
    B --> E["New Current Controller"]
    D --> E
    F["Locally Recognized<br>by Trusted Parties"] -.-> E
```

Key idea:

- a small, otherwise trusted set of parties may choose to recognize effect without separate third-party attestation
- this is a weaker profile for portability, independent verification, and later dispute resolution

## 5. Lifecycle View

```mermaid
flowchart TD
    P["Pre-Issuance"] --> I["Issue"]
    I --> A["Active"]
    A --> T["Transfer"]
    T --> A
    A --> E["Encumber"]
    E --> A
    A --> D["Discharge"]
    D --> A
    A --> R["Redeem"]
    R --> RP["Redemption Pending"]
    RP --> X["Terminate"]
    X --> Z["Terminated"]
    AT["Attestation may attach<br>to relevant events"] -.-> I
    AT -.-> T
    AT -.-> E
    AT -.-> D
    AT -.-> R
    AT -.-> X
```

Key idea:

- multiple lifecycle actions may occur while the object is active
- attestation is not itself a lifecycle state transition, even though lifecycle events may be attested
- termination ends the active lifecycle

## 6. Control Layer vs Recognition Layer

```mermaid
flowchart LR
    A["OpenETR Control Layer<br>signed events and control history"] --> B["Recognition Layer<br>law, contract, policy, attestation"]
    B --> C["Recognized effect"]
```

Key idea:

- OpenETR records authenticated facts
- the Recognition Layer determines legal or operational effect

## 7. Endorsement / Indorsement in the Revised Model

```mermaid
flowchart LR
    A["TRANSFER<br>changes control"] --> C["Recognition framework may characterize result"]
    B["ATTEST<br>adds authenticated meaning or instruction"] --> A
    B --> C
    C --> D["Endorsement / Indorsement<br>if applicable"]
```

Key idea:

- endorsement or indorsement is not a standalone universal protocol primitive
- it is a recognition-layer characterization of one or more underlying OpenETR events
