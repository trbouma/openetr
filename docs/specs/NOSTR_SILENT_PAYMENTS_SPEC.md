# Nostr Silent Payments (NSP) Specification Note

## Purpose

This note defines **Nostr Silent Payments (NSP)** as a distinct Silent Payments derivation and recovery model.

The NSP model uses the BIP-352 Silent Payments protocol for payment construction, scanning, and output recovery, but it differs from common wallet-seed Silent Payments implementations in the origin of its base key material.

## Definition

Nostr Silent Payments is a Silent Payments model whose base scan and spend key material is derived deterministically from a Nostr identity rather than from a conventional wallet seed tree alone.

Under the NSP derivation contract:

- a Silent Payments address can be derived from a known `npub`
- the matching private scan and spend keys can be derived from the corresponding `nsec`
- the resulting wallet is a valid Silent Payments receive model with its own scan, detection, and spend-reconstruction behavior

## Distinct Wallet Class

NSP must be treated as its own model, not merely as another address encoding.

This is because:

- the address format is Silent Payments compatible
- the downstream transaction and scanning model is Silent Payments compatible
- but the base key derivation contract is identity-derived rather than wallet-seed/BIP32-derived

So while an NSP address may look like another valid `sp1...` Silent Payments address, it is not necessarily reconstructible by wallet software that assumes only a BIP32/BIP352 seed-tree origin.

## Base Derivation Model

Let:

- `d` = Nostr private key
- `P = dG` = Nostr public key

Derive deterministic domain-separated tweak scalars:

- `t_scan = H_tag("nostr-sp/scan", P)`
- `t_spend = H_tag("nostr-sp/spend", P)`

Then derive the NSP public keys:

- `ScanPub = P + t_scan G`
- `SpendPub = P + t_spend G`

And, when the matching private key is available, the NSP private keys:

- `scan_priv = d + t_scan mod n`
- `spend_priv = d + t_spend mod n`

The Silent Payments address is then:

- `sp1... = bech32m(v0 || ScanPub || SpendPub)`

This makes NSP:

- publicly derivable from `npub`
- privately controllable from `nsec`
- compatible with Silent Payments payment construction and scanning logic

## Root-Equivalent Scan Key Caveat

Under the NSP derivation contract, the private scan key is:

- `scan_priv = d + t_scan mod n`

where:

- `d` is the Nostr private key
- `t_scan = H_tag("nostr-sp/scan", P)`
- `P = dG` is public from the `npub`

Because `t_scan` is publicly computable from the `npub`, disclosure of `scan_priv` allows recovery of:

- `d = scan_priv - t_scan mod n`

Once `d` is recovered, the NSP spend private key is also recoverable:

- `spend_priv = d + t_spend mod n`

Therefore, in NSP:

- the scan private key is root-equivalent
- disclosing `scan_priv` reveals the original `nsec`
- disclosing `scan_priv` also reveals `spend_priv`

This is a fundamental consequence of the additive NSP derivation model and is not merely an implementation detail.

## Relationship to BIP-352

The NSP does not replace or alter the core BIP-352 per-payment model.

Instead:

- BIP-352 defines how senders derive per-payment outputs and how receivers scan for them
- NSP defines how the receiver's base Silent Payments keys are obtained from Nostr identity

So NSP is best understood as:

- a valid receiver-key origin model
- feeding into the standard Silent Payments transaction and scanning flow

## Relationship to Wallet-Compatible BIP32 Silent Payments

A wallet-compatible Silent Payments implementation may derive its base scan/spend keys from a private seed tree, for example through hardened BIP32 paths such as:

- `m/352h/...`

That wallet class is different from NSP.

### NSP

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

An NSP-derived address may be accepted by software that is merely asked to send to a valid Silent Payments address.

However, a third-party wallet can only fully support NSP if it explicitly implements the NSP derivation contract.

Supporting NSP means supporting:

- `npub -> ScanPub / SpendPub / sp1...`
- `nsec -> scan_priv / spend_priv`
- NSP receipt detection
- NSP spend/sweep reconstruction

This is different from supporting only:

- seed-derived BIP32 Silent Payments wallets

Therefore, NSP should be treated as a separate, named, and explicit derivation type in any third-party implementation.

## Scanning Model

NSP remains a valid Silent Payments model for:

- local receipt detection
- local txid validation
- local sweep and spend reconstruction

However, because the NSP scan private key is root-equivalent, NSP should be treated as:

- safe for local scanning
- unsafe for untrusted remote scanning

### Remote Scanner Implication

A remote scanner such as a Frigate server can technically scan for NSP receipts if it is given:

- the NSP `scan_priv`
- the NSP `spend_pub`

Practical CLI testing confirmed that a Frigate server can:

- accept NSP-derived scan and spend key material
- accept the derived NSP `sp1...` address in the returned subscription data
- return matching transaction history for an NSP scan
- allow local OpenETR validation of the returned txids against the NSP receipt logic

But this interoperability result must not be misread as a safe trust model.

Because `scan_priv` reveals the root key and spend key under the NSP derivation contract:

- a remote scanner can be NSP-compatible at the protocol level
- but disclosure of the NSP scan private key compromises the full wallet

So the correct operational interpretation is:

- NSP remote scanning is technically possible
- NSP remote scanning is not safe against the scanner operator
- NSP should be treated as a local-scan wallet class unless the user intentionally accepts full key disclosure

### Frigate-Specific Conclusion

For NSP:

- Frigate interoperability is real
- but it is appropriate only for self-hosted or fully trusted scanner environments

For untrusted or third-party remote scanning:

- NSP should not be used
- seed-derived hardened BIP352 wallet modes are safer candidates because disclosure of the derived scan key is not trivially reversible back to the root key in the same way

## Minimum Third-Party Support Model

A third-party wallet that wants to support NSP should implement at least:

1. NSP public derivation from `npub`
2. NSP private scan/spend derivation from `nsec`
3. Silent Payments receipt scanning using the derived NSP scan key
4. Output-private-key reconstruction for spend/sweep from matched NSP receipts

Optional enhancements include:

- NSP ownership verification tools
- NSP address display from `nip05 -> npub`
- NSP txid-hint workflows
- NSP receipt confirmation and sweep UX
- explicit warnings that NSP scan private key disclosure compromises the root key and spend key

## Normative Interpretation

For specification and implementation purposes, Nostr Silent Payments should be treated as:

- a valid Silent Payments wallet class
- with an identity-derived base key contract
- distinct from wallet-seed/BIP32 Silent Payments wallet classes

Wallet software that does not implement the NSP derivation contract should not claim NSP recovery or NSP scanning compatibility merely because it supports generic Silent Payments addresses.
