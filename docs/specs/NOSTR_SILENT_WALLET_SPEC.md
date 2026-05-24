# Nostr Silent Wallet (NSW) Specification Note

## Purpose

This note defines the **Nostr Silent Wallet (NSW)** as a distinct Silent Payments wallet class.

The NSW model uses the BIP-352 Silent Payments protocol for payment construction, scanning, and output recovery, but it differs from common wallet-seed Silent Payments implementations in the origin of its base key material.

## Definition

A Nostr Silent Wallet is a Silent Payments wallet whose base scan and spend key material is derived deterministically from a Nostr identity rather than from a conventional wallet seed tree alone.

Under the NSW derivation contract:

- a Silent Payments address can be derived from a known `npub`
- the matching private scan and spend keys can be derived from the corresponding `nsec`
- the resulting wallet is a valid Silent Payments receive model with its own scan, detection, and spend-reconstruction behavior

## Distinct Wallet Class

The NSW must be treated as its own wallet class, not merely as another address encoding.

This is because:

- the address format is Silent Payments compatible
- the downstream transaction and scanning model is Silent Payments compatible
- but the base key derivation contract is identity-derived rather than wallet-seed/BIP32-derived

So while an NSW address may look like another valid `sp1...` Silent Payments address, it is not necessarily reconstructible by wallet software that assumes only a BIP32/BIP352 seed-tree origin.

## Base Derivation Model

Let:

- `d` = Nostr private key
- `P = dG` = Nostr public key

Derive deterministic domain-separated tweak scalars:

- `t_scan = H_tag("nostr-sp/scan", P)`
- `t_spend = H_tag("nostr-sp/spend", P)`

Then derive the NSW public keys:

- `ScanPub = P + t_scan G`
- `SpendPub = P + t_spend G`

And, when the matching private key is available, the NSW private keys:

- `scan_priv = d + t_scan mod n`
- `spend_priv = d + t_spend mod n`

The Silent Payments address is then:

- `sp1... = bech32m(v0 || ScanPub || SpendPub)`

This makes the NSW:

- publicly derivable from `npub`
- privately controllable from `nsec`
- compatible with Silent Payments payment construction and scanning logic

## Relationship to BIP-352

The NSW does not replace or alter the core BIP-352 per-payment model.

Instead:

- BIP-352 defines how senders derive per-payment outputs and how receivers scan for them
- NSW defines how the receiver's base Silent Payments keys are obtained from Nostr identity

So NSW is best understood as:

- a valid receiver-key origin model
- feeding into the standard Silent Payments transaction and scanning flow

## Relationship to Wallet-Compatible BIP32 Silent Payments

A wallet-compatible Silent Payments implementation may derive its base scan/spend keys from a private seed tree, for example through hardened BIP32 paths such as:

- `m/352h/...`

That wallet class is different from NSW.

### NSW

- base key origin: Nostr identity
- public derivability from `npub`: yes
- private recovery from `nsec`: yes
- independent public ownership verification: yes

### Wallet-Compatible BIP32 Silent Payments

- base key origin: private seed material
- public derivability from `npub`: no
- private recovery from seed/xprv: yes
- independent public ownership verification: no

Both wallet classes may produce valid `sp1...` addresses and use valid Silent Payments downstream logic, but they are not the same derivation contract.

## Interoperability Implications

An NSW address may be accepted by software that is merely asked to send to a valid Silent Payments address.

However, a third-party wallet can only fully support NSW if it explicitly implements the NSW derivation contract.

Supporting NSW means supporting:

- `npub -> ScanPub / SpendPub / sp1...`
- `nsec -> scan_priv / spend_priv`
- NSW receipt detection
- NSW spend/sweep reconstruction

This is different from supporting only:

- seed-derived BIP32 Silent Payments wallets

Therefore, NSW should be treated as a separate, named, and explicit wallet type in any third-party implementation.

## Remote Scanner Compatibility

An NSW is compatible with remote Silent Payments scanners that operate at the scan-key layer rather than at the wallet-seed derivation layer.

In practice, this means a remote scanner such as a Frigate server can scan for NSW receipts if it is given:

- the NSW `scan_priv`
- the NSW `spend_pub`

The scanner does not need to know whether those keys came from:

- an identity-derived NSW contract
- a wallet-seed/BIP32 Silent Payments wallet

It only needs a valid and internally consistent Silent Payments key pair at the receiver scan/spend interface.

### Interoperability Result

Practical CLI testing confirmed that a Frigate server can:

- accept NSW-derived scan and spend key material
- accept the derived NSW `sp1...` address in the returned subscription data
- return matching transaction history for an NSW scan
- allow local OpenETR validation of the returned txids against the NSW receipt logic

This demonstrates that NSW compatibility with Frigate-style scanning depends on:

- the correctness of the Silent Payments receiver keys
- the Silent Payments scan protocol

and not on whether the wallet was originally derived from:

- a BIP32 wallet tree
- or a Nostr identity

### Scope of the Result

This does not mean every third-party wallet automatically supports NSW recovery or spending.

It means specifically that:

- a remote scanner can be NSW-compatible without implementing NSW wallet recovery
- a third-party wallet that wants full NSW support must still implement the NSW derivation contract locally
- Frigate-style discovery is compatible with NSW because it operates on the derived receiver keys, not on the upstream wallet-origin model

### Operational Caveat

Remote scanning with a Frigate server requires providing the NSW scan private key to the remote scanner for the duration of the scan session.

Therefore:

- Frigate compatibility is useful and real
- but remote Frigate use introduces a trust boundary around the scan private key
- self-hosted scanning remains preferable for sensitive or high-risk use cases

## Minimum Third-Party Support Model

A third-party wallet that wants to support NSW should implement at least:

1. NSW public derivation from `npub`
2. NSW private scan/spend derivation from `nsec`
3. Silent Payments receipt scanning using the derived NSW scan key
4. Output-private-key reconstruction for spend/sweep from matched NSW receipts

Optional enhancements include:

- NSW ownership verification tools
- NSW address display from `nip05 -> npub`
- NSW txid-hint workflows
- NSW receipt confirmation and sweep UX

## Normative Interpretation

For specification and implementation purposes, the Nostr Silent Wallet should be treated as:

- a valid Silent Payments wallet class
- with an identity-derived base key contract
- distinct from wallet-seed/BIP32 Silent Payments wallet classes

Wallet software that does not implement the NSW derivation contract should not claim NSW recovery or NSW scanning compatibility merely because it supports generic Silent Payments addresses.
