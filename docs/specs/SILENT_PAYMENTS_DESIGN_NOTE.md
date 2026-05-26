# Silent Payments Design Note

## Purpose

OpenETR will keep its existing exact-key Taproot `p2tr` wallet flow and add a separate Bitcoin Silent Payments capability based on BIP-352.

The two modes serve different goals:

- existing `p2tr` wallet:
  exact single-address Taproot spending and deterministic wallet control
- Silent Payments:
  privacy-preserving static receive addresses with receiver-side scanning

Silent Payments should be treated as an additional receive protocol, not as a replacement for the current OpenETR Taproot wallet.

## Design Goals

OpenETR Silent Payments should provide:

- a stable `sp1q...` receive address per profile or root context
- compatibility with the existing relay-backed and multi-modality architecture
- deterministic recovery from OpenETR key material
- a clear separation between:
  - spendable exact `p2tr` wallet control
  - privacy-preserving Silent Payments receiving
- shared implementation in `openetr` with thin CLI, web, and API adapters

## Non-Goals

This design does not initially attempt to:

- replace the existing `p2tr` wallet flow
- merge Silent Payments balances into the exact single-address Taproot wallet balance
- make Silent Payments the default Bitcoin receive mode everywhere
- solve full light-client Silent Payments scanning in the first iteration

## Coexistence Model

OpenETR will expose two parallel Bitcoin capabilities.

### Exact Taproot Wallet

This remains the current OpenETR behavior:

- derive a canonical single-address `p2tr` wallet from a Nostr key
- inspect balance
- export `taproot_wif`
- create and sign spend transactions directly

### Silent Payments Receive Mode

This adds a second Bitcoin receive identity:

- derive a Silent Payments scan/spend key pair
- publish or display a static `sp1q...` Silent Payment address
- scan blockchain activity to detect payments
- derive per-output spend keys when needed

The operational rule is:

- `p2tr` mode is exact-key and immediately spendable by OpenETR
- Silent Payments mode is private static receiving with scan-based discovery

## Key Derivation Model

OpenETR should derive Silent Payments material deterministically from the existing Nostr identity, using explicit domain separation.

More specifically:

- the public Silent Payments address material must be derivable from the identity's public key (`npub`)
- the corresponding private scan and spend keys must be derivable from the matching private key (`nsec`)

Recommended approach:

1. Start from the normalized OpenETR base public key for the identity.
2. Derive domain-separated Silent Payments tweaks from that normalized base public key.
3. Use those tweaks to derive the public Silent Payments keys:
   - `scan_pub_key`
   - `spend_pub_key`
4. When the matching `nsec` is available, derive:
   - `scan_priv_key`
   - `spend_priv_key`
5. Publish or display:
   - encoded Silent Payment address `sp1q...`

Recommended domain tags:

- `nostr-sp/scan`
- `nostr-sp/spend`

OpenETR standardizes these tags as part of the deterministic Silent Payments derivation scheme. A change to these tags changes the derived public Silent Payments keys and final `sp1q...` address for the same identity, and changes the private scan/spend keys when the `nsec` is available, so they must be treated as part of the compatibility contract.

This keeps Silent Payments key material:

- deterministic
- profile-specific
- publicly derivable from the Nostr identity
- recoverable from OpenETR-controlled keys
- distinct from the existing exact `p2tr` wallet flow

## Recovery Model

Recovery should be deterministic and should not require separate local wallet state.

More specifically:

- the public Silent Payments address should remain recoverable from the public Nostr identity material
- the private scan and spend keys should remain recoverable from the matching profile `nsec`
- detected outputs should remain recoverable by rescanning with the private scan key material

The user should be able to recover:

- the Silent Payments address
- the scan key
- the spend key
- any detected outputs after rescanning

This matches the broader OpenETR philosophy:

- minimal local state
- deterministic regeneration where possible
- relay-backed or query-backed discovery where appropriate

## Shared Core Implementation

All Silent Payments behavior should live in `openetr`, not in individual adapters.

Recommended shared module areas:

- `openetr/bitcoin_silent.py`
  or
- `openetr/bitcoin.py`
  if the code remains compact enough

Core shared functions should include:

- `derive_silent_payment_keys(nostr_key)`
- `derive_silent_payment_address(nostr_key)`
- `scan_silent_payment_outputs(...)`
- `summarize_silent_payment_receipts(...)`
- `derive_silent_payment_spend_key(...)`

## CLI Surface

Recommended initial CLI commands:

- `openetr get-silent-payment-address <nsec|npub|nip05>`
- `openetr check-silent-payment-receipts <nsec> [--limit 20]`

Possible later command:

- `openetr spend-silent-payment <nsec> <destination_address> <outpoint-or-detected-output> ...`

The first iteration should prioritize:

- address derivation
- receipt scanning
- transaction summary

Direct spending from detected Silent Payments outputs can be added later.

## Web App Surface

Recommended initial web experience:

- show a `Silent Payments` pane separate from the existing exact `Bitcoin Wallet` pane
- allow the user to:
  - derive the `sp1q...` address
  - show it as text and QR
  - scan and summarize recent detected Silent Payments receipts

The web app should treat the Silent Payments capability as a distinct wallet model and should not mix:

- exact `p2tr` wallet balance
- Silent Payments receipts

Those should be presented as separate views because they are different receive-and-spend models with different discovery, privacy, attribution, and recovery properties, not merely different presentations of the same wallet.

## API Surface

Recommended future agent/API endpoints:

- `GET /api/bitcoin/silent/address`
- `POST /api/bitcoin/silent/scan`
- `GET /api/bitcoin/silent/receipts`

These endpoints should return structured JSON derived from the shared `openetr` service layer.

## Scanning Model

Silent Payments require receiver-side scanning.

The first OpenETR implementation should assume:

- scanning against an Esplora-compatible source or full-node-derived transaction feed
- server-side or CLI-side scanning in bounded windows
- explicit recent-history or pagination parameters

Recommended first-pass scan controls:

- `limit`
- optional `last_seen_txid`
- optional block-height range later

This keeps the first implementation practical without claiming full-wallet historical scan coverage from day one.

### Txid Hint Model via NIP-17

OpenETR should explicitly support a more efficient discovery pattern in which the sender provides the Bitcoin transaction id as an out-of-band hint over Nostr.

Recommended near-term pattern:

1. The receiver shares a Silent Payments `sp1q...` address.
2. The sender pays that address from a Bitcoin wallet.
3. The sender sends a NIP-17 DM to the receiver containing the resulting Bitcoin `txid`.
4. The receiver uses that `txid` as a targeted scan hint:
   - fetch the transaction
   - run Silent Payments receipt detection on that transaction
   - confirm whether one of the outputs belongs to them

This model has several advantages:

- avoids broad block-range scanning for routine payments
- reduces public Esplora/API load and rate-limit risk
- fits naturally with OpenETR's Nostr-centric identity model
- gives the receiver a fast confirmation path before full wallet-style scanning exists

This should be treated as the preferred first operational discovery pattern, even after bounded block scanning exists.

Recommended DM payload shape:

```json
{
  "type": "silent_payment_hint",
  "txid": "<bitcoin-txid>",
  "network": "mainnet",
  "note": "optional human context"
}
```

OpenETR should eventually support:

- extracting Silent Payments txid hints from NIP-17 DMs
- offering one-click receipt verification from the DM
- optionally sweeping or managing the detected output after verification

This design does not replace autonomous receiver-side scanning. It provides a practical and efficient interoperability layer for the first production-capable OpenETR Silent Payments workflows.

## Storage Model

OpenETR should avoid storing derived Silent Payments secrets redundantly.

Preferred model:

- derive scan/spend keys from deterministic OpenETR key material when needed
- cache only transient scan results where useful
- avoid persistent local storage of duplicate Silent Payments secret state

If scan cursors or optimization indexes are introduced later, they should be treated as:

- optional acceleration data
- reconstructible state

## Security Model

Silent Payments improve receive privacy, but they introduce scanning complexity.

Important security and operational rules:

- keep the existing exact `p2tr` wallet model for straightforward sending and recovery
- derive Silent Payments keys with strict domain separation
- never silently merge the two wallet models
- clearly label Silent Payments as a separate Bitcoin receive protocol

## Relationship to BIP-352 Per-Payment Math

It is important to distinguish between:

1. how the receiver's base Silent Payments keys are created
2. how a sender creates a particular Silent Payments transaction output for that receiver

The second part is the familiar BIP-352 transaction-level math.
The first part is where OpenETR differs.

### BIP-352 Base Model

In the usual BIP-352 description, Bob already has Silent Payments key material.

Using simplified notation:

- Bob publishes a Silent Payments public key `B`
- Alice has an input private/public key pair `a/A`

Alice creates a payment output:

- `P = B + hash(a·B)·G`

Bob later scans using the matching private key `b` and the sender input public key `A`:

- because `a·B = b·A`

For multiple outputs to the same receiver in one transaction, BIP-352 extends this by introducing an integer counter:

- `P0 = B + hash(a·B || 0)·G`
- `P1 = B + hash(a·B || 1)·G`
- and so on

Bob detects them by computing the same sequence with:

- `P0 = B + hash(b·A || 0)·G`
- `P1 = B + hash(b·A || 1)·G`
- and so on

This is the core per-payment Silent Payments mechanism.

### OpenETR Adaptation Layer

OpenETR does not replace that transaction-level concept.

Instead, OpenETR adds a deterministic identity-derived layer before it.

OpenETR first derives the receiver's Silent Payments identity from the Nostr identity itself.

Starting from:

- Nostr private key `d` when available
- Nostr public key `P = dG`

OpenETR derives deterministic domain-separated tweaks from the base public key:

- `t_scan = H_tag("nostr-sp/scan", P)`
- `t_spend = H_tag("nostr-sp/spend", P)`

It then derives the receiver's base Silent Payments public keys:

- `ScanPub = P + t_scan G`
- `SpendPub = P + t_spend G`

When the matching `nsec` is available, it derives the matching private keys:

- `scan_priv = d + t_scan mod n`
- `spend_priv = d + t_spend mod n`

These derived keys form the OpenETR Silent Payments identity.

### Same Downstream Transaction Math

Once the OpenETR Silent Payments identity has been derived, the normal Silent Payments transaction logic applies on top of it.

That means OpenETR still uses the same style of downstream mechanism:

- sender-side ECDH against receiver public Silent Payments material
- output tweaking by hashed shared-secret values
- receiver-side scanning with private scan key material
- repeated checks for `k = 0, 1, 2...` for multiple outputs

So OpenETR differs from the usual BIP-352 wallet model in:

- how the receiver's base Silent Payments keys are obtained

and not in the basic idea that:

- the sender derives a per-payment output from shared secret material
- the receiver detects the output by recomputing the same relation with private scan knowledge

### Summary

The cleanest way to view the difference is:

- BIP-352 wallet model:
  - receiver Silent Payments keys originate from wallet seed material
- OpenETR model:
  - receiver Silent Payments keys originate from Nostr identity via deterministic additive tweaks

After that key-origin step, both approaches can use the same class of per-payment Silent Payments ECDH and output-tweak logic.

### Compact Comparison

| Aspect | BIP-352 protocol layer | OpenETR base derivation | Wallet-style BIP-32 derivation |
|---|---|---|---|
| Primary concern | How sender and receiver use Silent Payments keys for payments and scanning | How receiver Silent Payments base keys are derived from Nostr identity | How receiver Silent Payments base keys are derived from wallet seed material |
| Starting material | Assumes receiver already has Silent Payments keys | `npub` and, when available, matching `nsec` | private seed material / raw `nsec` bytes used as BIP-32 seed |
| Public derivability | Not the focus of the protocol layer | Yes | No |
| `npub -> sp1...` | Not defined by the protocol itself | Yes | No |
| Private scan/spend recovery | Required for detection and spending, but origin not prescribed | Derived from matching `nsec` | Derived from BIP-32 private tree |
| Per-payment output math | Yes | Yes, after OpenETR base derivation | Yes, after wallet base derivation |
| Multiple-output `k = 0, 1, 2...` logic | Yes | Yes | Yes |
| Main product implication | Protocol behavior | Identity-linked Nostr Silent Payments (NSP) with public verifiability | Wallet-compatible Silent Payments tree with stronger off-chain unlinkability |

### Practical Interoperability Recap

The resulting Silent Payments address is still the same kind of object in both derivation models:

- a valid `sp1...` address
- containing receiver Silent Payments public key material
- usable by a sender to construct Silent Payments outputs

So at the address-format and sender-payment level, the address can appear effectively the same even when the underlying derivation origin is different.

This means:

- a sending wallet that is only asked to pay to a valid `sp1...` address may see no practical difference
- a receiving or scanning wallet may see an important difference, because it must reconstruct the matching private scan/spend keys correctly

The key interoperability distinction is therefore not:

- how the address looks on the wire

but:

- how the receiver reconstructs the private key material behind that address

So the practical rule is:

- the Silent Payments address format can look the same
- the downstream sending flow can look the same
- but receiving, scanning, and recovery depend on whether the wallet uses the same underlying derivation contract
- expose scan and spend semantics explicitly in UI and CLI messaging

### Traceability Tradeoff

The most important traceability difference between the identity-derived NSP model and a seed-derived BIP-352 wallet is off-chain identity linkage, not on-chain output visibility.

In the NSP model:

- anyone who knows the `npub`
- and knows the derivation rule

can derive the expected static `sp1...` address.

That means NSP creates a public relationship of the form:

- `known npub -> known silent payment address`

This gives NSP two important sender-side benefits:

- independent public verifiability
- stronger anti-spoofing assurance than a published `sp1...` string alone

But it also creates a clear tradeoff:

- NSP has weaker off-chain unlinkability from the public Nostr identity than a seed-derived BIP-352 wallet

By contrast, a wallet-derived BIP-352 address is not publicly derivable from the `npub`, so it provides stronger off-chain identity unlinkability but weaker sender-side independent verification unless the recipient publishes or signs the address through some other channel.

What does not materially change is the core on-chain Silent Payments privacy model:

- the static `sp1...` address still does not appear on-chain
- each payment still lands as a fresh Taproot-looking output
- outside observers still cannot trivially identify which outputs belong to that static address without the relevant scan key material

### Machine and Agentic Identity Use Case

The identity-derived NSP model is also a natural fit for machine, service, and agentic identity.

In this use case, the recipient may have:

- a generated `npub`
- a matching `nsec`
- and no published social profile, website, or human-facing payment page

That means there may be no practical address-distribution channel at all beyond the public identity key itself.

NSP solves that coordination problem cleanly:

- the receiving component exposes only its `npub`
- the sending component derives the correct static Silent Payments address independently
- no separate payment-address registry is required
- and the resulting payment still benefits from the normal on-chain Silent Payments privacy model

This makes NSP well suited to:

- agent-to-agent settlement
- component-to-component billing
- service payments between autonomous systems
- internal private treasury transfers between software-controlled Nostr identities

This use case also changes how the traceability tradeoff should be evaluated.

- the identity-derived NSP model does create a stronger public correlation between the static `sp1...` address and the public `npub` than a hardened seed-derived BIP-352 wallet
- but for bare, ephemeral, or non-human `npub` identities, that correlation may be an acceptable or even desirable tradeoff
- if the `npub` is not associated with a rich human-facing profile, social graph, or public persona, then the off-chain linkage cost can be materially lower
- in that setting, independent derivability and address-authenticity guarantees may be more valuable than maximum identity unlinkability

This machine-identity use case also highlights one of NSP's strongest properties:

- even in the complete absence of a human-readable profile or explicit published address, a valid Silent Payments receive identity can still be derived from the `npub` alone

If scan/spend key separation is implemented per BIP-352, OpenETR should prefer:

- online scanning with scan key responsibilities
- minimized exposure of spend key material

### NSP Scan Key Security Caveat

The NSP additive derivation model creates an important security constraint on scanning.

NSP derives:

- `scan_priv = d + t_scan mod n`
- `spend_priv = d + t_spend mod n`

where:

- `d` is the Nostr private key
- `t_scan = H_tag("nostr-sp/scan", P)`
- `t_spend = H_tag("nostr-sp/spend", P)`
- `P = dG` is public from the `npub`

Because `t_scan` is publicly computable from the `npub`, anyone who learns `scan_priv` can recover:

- `d = scan_priv - t_scan mod n`

and then derive:

- `spend_priv = d + t_spend mod n`

So in the NSP model:

- `scan_priv` is root-equivalent
- disclosure of `scan_priv` reveals the original `nsec`
- disclosure of `scan_priv` also reveals the NSP spend private key

Therefore NSP remains a sound local-scanning wallet model, but it does not support a safe untrusted remote-scanning model.

## Implementation Notes and Interoperability Glitches

The first OpenETR Silent Payments implementation exposed several practical glitches that are worth documenting because they are easy to reintroduce accidentally.

### Proven NSP Implementation Result

Implementation and live CLI testing now support a stronger conclusion than the original design note assumptions:

- the Nostr Silent Payments (NSP) derivation is not merely theoretically valid
- it functions as a real Silent Payments wallet mode
- it can receive payments and validate txids locally
- it can technically interoperate with a remote Frigate scanner
- but remote scanner use exposes the root-equivalent NSP scan key and therefore is not a safe trust model

In practical terms, the following are now confirmed:

- direct txid-based NSP receipt validation works
- historical NSP receipt scanning via Frigate works at the protocol level
- multiple discovered Frigate matches can be validated locally against the NSP receipt logic
- the NSP scan/spend key model is sufficient for remote scanner interoperability
- the NSP scan private key is root-equivalent, so remote Frigate scanning should be treated as trusted-operator-only or local-only in practice

This means NSP should be treated as an implemented wallet model, not merely as a derivation thought experiment or design placeholder.

### What We Discovered

The most important implementation discovery was twofold:

- remote scanning compatibility depends on the Silent Payments receiver key interface, not on the upstream derivation origin
- NSP scan-key disclosure compromises the root key because of the additive derivation model

More specifically:

- Frigate does not need the wallet to be BIP32-derived
- Frigate only needs a valid:
  - `scan_priv`
  - `spend_pub`
- if those keys are internally consistent, Frigate can discover matching Silent Payments history for the wallet

This was demonstrated in practice with the NSP keys.

That result matters because it narrows the true interoperability boundary while also exposing the true security boundary:

- third-party wallet recovery still depends on whether the wallet implements the NSP derivation contract
- remote scanner compatibility does not
- remote scanner safety does

So the correct interpretation is:

- NSP is distinct from wallet-compatible BIP32 Silent Payments at the wallet derivation layer
- NSP is compatible with Frigate-style remote scanning at the scan-key layer
- NSP is not safe for untrusted remote scanning because `scan_priv` reveals `d` and therefore `spend_priv`

### Frigate Integration Lessons

The Frigate work also exposed several protocol and implementation details that are easy to miss:

- Electrum negotiation matters:
  - `server.version` must be the first RPC on a new connection
- Frigate response formats vary:
  - subscription notifications may arrive in a dict-shaped `params` payload rather than the list-shaped form assumed by some Electrum clients
- one-shot scans and follow-mode subscriptions are different:
  - the client must be prepared for either an immediate result or a result followed by progress/history notifications
- start-height matters operationally:
  - a tip-height scan may correctly return no history
  - an older known-receipt height is a better interoperability test

The practical lesson is that an empty Frigate result should not be interpreted immediately as a derivation failure. It may instead reflect:

- no history after the chosen start height
- protocol-shape mismatch in the client
- or differing notification timing assumptions

The separate security lesson is that Frigate interoperability should not be confused with Frigate safety for NSP:

- protocol compatibility was proven
- trust minimization was not
- NSP should therefore be treated as a local-scan or trusted-scanner model

### 1. Esplora Script Type Naming Differences

During early receipt detection testing, Cake Wallet produced transactions whose Esplora `scriptpubkey_type` values were returned as:

- `v0_p2wpkh`
- `v1_p2tr`

The initial OpenETR scanner only recognized:

- `p2wpkh`
- `p2tr`

Result:

- eligible input pubkeys were not extracted
- Taproot outputs were not recognized as candidate Silent Payments outputs

Fix:

- normalize Esplora script type aliases before input/output classification

### 2. Taproot Output Matching Must Use X-Only Keys

Taproot outputs on-chain are represented as x-only pubkeys.

The initial OpenETR scanner compared:

- full compressed derived pubkeys

against:

- Taproot output keys reconstructed with an assumed `02` prefix

That can fail whenever the actual derived output point has odd y.

Fix:

- compare Taproot outputs using x-only pubkey bytes
- treat the on-chain output key as x-only for receipt matching

### 3. Input Hash Serialization Bug

The initial implementation computed the BIP-352 `Inputs` tagged hash using:

- lowest outpoint
- x-only bytes of the summed input pubkey

But the receiver derivation needs the full compressed summed input pubkey.

Result:

- sender and receiver derived different shared-secret contexts

Fix:

- include the full compressed summed input pubkey in `hash BIP0352/Inputs(...)`

### 4. Shared Secret Tweak Serialization Bug

The first scanner version derived `t_k` using:

- x-only bytes of the shared point
- little-endian serialization for the index `k`

That does not match the intended BIP-352 serialization flow.

Fix:

- hash the full compressed shared point for `BIP0352/SharedSecret`
- serialize `k` using `ser_32(k)` in big-endian form

### 5. Public Key Aggregation API Misuse

The Python `secp256k1` binding used by OpenETR expects raw `secp256k1_pubkey *` handles when combining public keys.

The first implementation attempted to combine higher-level wrapper objects directly.

Result:

- summed input pubkey derivation failed
- receipt detection reported that input pubkeys summed to an invalid point

Fix:

- pass the underlying raw secp256k1 pubkey handles into the combine call

### 6. Transaction Inspection Was Essential

The addition of a dedicated transaction inspection command was important for debugging interoperability:

- `openetr inspect-silent-payment-tx <txid>`

This made it possible to see:

- actual input types
- witness structure
- extracted pubkeys
- candidate Taproot outputs

Without this tool, it would have been much harder to separate:

- transaction parsing issues
- BIP-352 derivation issues

from one another.

### Resulting Guidance

Based on the implementation work so far:

- Silent Payments address derivation alone is not enough to claim interoperability
- receipt detection must be tested against real wallet-produced transactions
- Esplora response normalization should be treated as part of the compatibility layer
- transaction-inspection tooling should remain part of the OpenETR developer and operator workflow

## Rollout Plan

Recommended rollout phases:

1. Silent Payments derivation only
   - derive scan/spend keys
   - derive and display `sp1q...`
   - CLI and web display support

2. Receipt scanning
   - summarize recent detected Silent Payments receipts
   - CLI and web summaries
   - targeted txid-hint scanning via NIP-17 DM

3. Recovery and rescan ergonomics
   - scanning checkpoints
   - better historical recovery workflow

4. Spending support
   - spend detected Silent Payments outputs
   - only after the receipt and recovery model is stable

## Recommended Product Framing

OpenETR should describe the feature like this:

- `Bitcoin Wallet`
  exact Taproot single-address wallet derived from OpenETR key material

- `Silent Payments`
  private static receive address capability derived from the same OpenETR identity, requiring scan-based payment detection

This makes the distinction clear and avoids confusing users into thinking Silent Payments is just another name for the current `p2tr` wallet flow.
