# Nostr Silent Payments (NSP) Derivation Decision Note

## Decision

OpenETR will preserve its current public-derivable Silent Payments derivation model as the primary OpenETR Silent Payments identity mode.

This means OpenETR will continue to derive the Silent Payments address from a Nostr identity in a way that allows:

- `npub -> sp1...`
- `nip05 -> npub -> sp1...`
- public ownership checks against a derived `sp1...`

OpenETR will not replace this model with a BIP-32-only Silent Payments derivation scheme as the default OpenETR behavior.

## Why

The current OpenETR derivation model is intentionally identity-linked.

It preserves a capability that would be lost under a BIP-32 hardened derivation model:

- deriving the Silent Payments receive address from public Nostr identity material alone

That public derivability is important for OpenETR because it enables:

- publishing or deriving a Silent Payments address from a known `npub`
- deriving a Silent Payments address from a `nip05` identifier once resolved to `npub`
- checking whether a provided Silent Payments address belongs to a resolved Nostr identity
- tight alignment between Nostr identity and OpenETR Silent Payments addressing

## Current OpenETR Model

OpenETR currently derives Silent Payments keys from the Nostr identity itself by:

1. Starting from the base Nostr key material.
2. Normalizing the private key to the BIP-340 even-y representative when private material is available.
3. Deriving deterministic domain-separated tweaks from the base public key.
4. Producing:
   - `scan_pub_key`
   - `spend_pub_key`
   - final `sp1...` address

The standardized OpenETR derivation tags are:

- `nostr-sp/scan`
- `nostr-sp/spend`

This design allows the public-key-only derivation path that OpenETR relies on for ownership checks and public identity linkage.

## Side-by-Side Derivation Comparison

Both the OpenETR identity-derived approach and the BIP-32 wallet-style approach are mathematically sound ways to produce a Silent Payments address.

In both cases, the final goal is the same:

- derive a `scan` key
- derive a `spend` key
- encode `sp1... = bech32m(v0 || ScanPub || SpendPub)`

The difference is how those keys are derived.

### OpenETR Identity-Derived Approach

OpenETR starts from the Nostr identity itself.

Let:

- `d` = base private key from the `nsec`
- `P = dG` = base public key from the `npub`

OpenETR derives two deterministic tweak scalars from the public key:

- `t_scan = H_tag("nostr-sp/scan", P)`
- `t_spend = H_tag("nostr-sp/spend", P)`

Then it derives the public Silent Payments keys using point addition:

- `ScanPub = P + t_scan G`
- `SpendPub = P + t_spend G`

When private material is available, it derives the private keys using scalar addition:

- `scan_priv = d + t_scan mod n`
- `spend_priv = d + t_spend mod n`

These two views are consistent because secp256k1 satisfies:

- `(d + t)G = dG + tG`

That means:

- a sender can derive the `sp1...` address from `npub` alone using public-key math
- the receiver can derive the matching private scan/spend keys from `nsec`
- both sides arrive at the same `ScanPub`, `SpendPub`, and `sp1...`

This is what makes the OpenETR approach:

- public-derivable
- independently verifiable
- tightly linked to Nostr identity

### Important Security Consequence

The same additive property also creates an important limitation.

Because:

- `scan_priv = d + t_scan mod n`
- `t_scan` is publicly computable from the `npub`

anyone who learns `scan_priv` can recover:

- `d = scan_priv - t_scan mod n`

and then derive:

- `spend_priv = d + t_spend mod n`

So in the NSP model:

- `scan_priv` is root-equivalent
- disclosure of `scan_priv` reveals the original `nsec`
- disclosure of `scan_priv` also reveals the spend private key

This means the public-derivable NSP model should be treated as:

- a valid local-scanning wallet model
- not a safe untrusted remote-scanning model

### BIP-32 Wallet-Style Approach

The BIP-32-style approach starts from the raw `nsec` bytes as seed material rather than from the public Nostr identity.

It computes a BIP-32 master node:

- `master = HMAC-SHA512("Bitcoin seed", nsec_bytes)`

Then it derives hardened Silent Payments child keys such as:

- `bspend = m / 352' / coin_type' / 0' / 0' / 0`
- `bscan  = m / 352' / coin_type' / 0' / 1' / 0`

The resulting public keys are:

- `SpendPub = b_spend G`
- `ScanPub = b_scan G`

The final Silent Payments address is then:

- `sp1... = bech32m(v0 || ScanPub || SpendPub)`

This is also sound, but it behaves like an HD wallet tree rather than a public identity derivation.

Because the derivation paths are hardened:

- the private seed material is required
- the address cannot be derived from `npub` alone

This makes the BIP-32 approach:

- wallet-oriented
- seed-oriented
- more compatible with wallet import/export expectations
- not publicly derivable from Nostr identity

## Why Both Approaches Are Sound

Both approaches are valid because both produce a consistent `scan` key and `spend` key pair that can be used within the Silent Payments protocol.

They differ in derivation contract, not in whether the resulting Silent Payments address is mathematically meaningful.

The OpenETR model is sound because:

- it uses deterministic secp256k1 additive key derivation
- the public and private derivations match through:
  - `(d + t)G = dG + tG`

The BIP-32 model is sound because:

- it uses standard HD-wallet derivation from a master seed
- it produces deterministic child private/public keys under a well-defined tree

In both cases:

- the resulting `sp1...` address is an off-chain Silent Payments identifier
- the on-chain payment still becomes a fresh derived Taproot output
- the `sp1...` address itself does not appear in the transaction

## Main Tradeoff

The main difference is not on-chain privacy.
Both approaches preserve the core Silent Payments privacy model on-chain.

The main difference is off-chain identity linkage and verifiability:

- OpenETR identity-derived approach:
  - public derivability from `npub`
  - independent public ownership verification
  - weaker off-chain unlinkability between Nostr identity and Silent Payments identity

- BIP-32 wallet-style approach:
  - no public derivation from `npub`
  - stronger off-chain unlinkability from the public Nostr identity
  - no independent public ownership verification from identity alone

OpenETR preserves the first model because public derivability and independent verifiability are important to the OpenETR identity-centered architecture.

## Attribution and Intent Implications

The public-derivable OpenETR model has an important attribution property:

- if a Silent Payments address can be deterministically generated from a known `npub`
- then the holder of the matching `nsec` cannot be uniquely implicated as having intentionally created or published that address

This is because the derivation does not require a secret act by the `nsec` holder.
Anyone with:

- the `npub`
- the OpenETR derivation rule

can derive the same `sp1...` address independently.

That means the linkage:

- `npub -> sp1...`

is a property of the derivation contract itself, not evidence of an intentional author action by the private-key holder.

In other words:

- the address may validly belong to that Nostr identity under the OpenETR convention
- but the existence of that address alone does not prove the `nsec` holder deliberately created, endorsed, or published it

This provides a form of plausible deniability around authorship or intent:

- ownership under the derivation rule can be independently verified
- intentional publication or endorsement cannot be inferred from derivation alone

By contrast, in an attestation-based linkage model, the identity owner would need to publish a signed statement or event explicitly asserting the relationship.

Examples of attestation-based linkage include:

- a signed Nostr event declaring a Silent Payments address
- a signed proof object binding `npub` to `sp1...`
- another private-key-authenticated publication channel

That alternative model changes the evidentiary meaning of the linkage:

- deterministic public derivation proves compatibility with the derivation rule
- signed attestation demonstrates intent or endorsement by the private-key holder

This is another reason OpenETR's derivation choice is distinct from a pure attestation model.
OpenETR gains independent verifiability, but the resulting linkage should be interpreted as:

- mathematically attributable under the OpenETR derivation contract

not as:

- direct proof of intentional publication by the `nsec` holder

## Nostr Silent Payments Interpretation

For OpenETR, it is reasonable to think of the Silent Payments capability derived from a Nostr identity as a distinct **Nostr Silent Payments (NSP)** model.

Under the OpenETR derivation rule:

- every `npub` can be treated as having a corresponding NSP-derived Silent Payments address
- the NSP model can be derived independently from public identity material
- but it can be impossible to prove that the `nsec` holder intentionally created it, published it, or is even aware that it exists

This is an important conceptual distinction.

Nostr Silent Payments is not just a displayed address string.
It is a distinct receive-and-recovery model with its own operational properties:

- it has a deterministic `sp1...` receive identity
- incoming payments do not reveal that `sp1...` identity on-chain
- receipt detection requires knowledge of the corresponding private scan key
- spending or sweeping detected outputs requires knowledge of the corresponding private spend key

In practice, that means:

- public observers may be able to derive that an NSP-derived Silent Payments address exists for a known `npub` under the OpenETR convention
- but they cannot detect which on-chain outputs belong to it without the relevant private key material
- and they cannot determine whether the identity owner has ever checked for, acknowledged, or claimed those outputs

## Detection and Sweep Properties

Silent Payments receipts can only be detected by a party with the relevant private scanning material.

For OpenETR, that means:

- the `sp1...` address can be derived publicly
- but the received on-chain outputs can only be recognized by a holder of the matching private scan key

Once detected, those outputs can be swept to unrelated destination addresses.
After sweeping:

- there is no reusable on-chain address linking the swept funds back to the original `sp1...`
- the recipient can move funds into other wallets or addresses under their control
- the visible chain history does not expose a simple public mapping from the donor to the recipient's known identity

This protects both sides of the transaction:

- the donor is protected because the act of paying the NSP-derived Silent Payments address does not publicly reveal a durable recipient identity on-chain
- the recipient is protected because discovering, claiming, and sweeping the funds requires private key knowledge and can be done to unrelated addresses

As a result, the funding relationship between donor and recipient is difficult to establish from public chain data alone.

## Sender Assurance and Anti-Spoofing Implications

Another important implication of the OpenETR derivation model is that the Silent Payments address is mathematically linked to the Nostr identity.

Because the `sp1...` address can be deterministically derived from the `npub` under the OpenETR derivation rule:

- any statement, profile, or event signed by that `npub` can be associated with the corresponding NSP-derived Silent Payments address
- the sender does not need to trust a separately copied or manually transcribed Silent Payments address

This gives the sender a strong assurance property:

- if the sender knows the intended recipient `npub`
- and the sender knows the OpenETR derivation rule

then the sender can derive the correct Silent Payments address independently and verify that it is the expected one.

That means the sender can avoid relying on:

- an unsigned pasted address
- a typo-prone manually shared address
- a substituted address embedded by a malicious intermediary
- a spoofed address presented alongside otherwise valid identity content

In practical terms, this removes an important class of spoofing risk.

Under this model:

- the correct Silent Payments address is fixed by the recipient identity and the derivation contract
- it is not an arbitrary value that can be swapped out without detection

So while signed Nostr content can still communicate intent, context, or payment instructions, the sender does not need to trust that content to supply the address itself.

The sender can instead:

1. resolve or verify the intended recipient `npub`
2. derive the expected Silent Payments address locally
3. send to that derived address

This substantially reduces the possibility of malicious address spoofing in identity-linked payment flows.

## Distinct Wallet Model

For all practical purposes, Nostr Silent Payments should be treated as its own distinct derivation and recovery model.

It should not be treated as merely another view of the exact OpenETR `p2tr` wallet.

Nostr Silent Payments differs from the exact `p2tr` wallet in several important ways:

- it is discovered by scanning, not by watching one fixed visible address
- it uses an off-chain `sp1...` receive identifier rather than a reusable on-chain address
- it requires different logic for receipt discovery
- it requires distinct spend reconstruction for detected outputs
- it has different privacy, attribution, and verification properties

For that reason, OpenETR should continue to model and present:

- the exact `p2tr` wallet
- and the Nostr Silent Payments

as separate Bitcoin capabilities, even when both are ultimately derived from the same Nostr identity.

## Rejected Default Alternative

The main alternative considered was a BIP-32 wallet-style Silent Payments derivation model in which:

- the raw `nsec` bytes are used as the BIP-32 seed
- a Silent Payments wallet tree is derived under hardened `m/352'/...` paths

That model is attractive for wallet interoperability, but it has an important tradeoff:

- hardened derivation requires private key material

As a result, the following would no longer be possible:

- deriving `sp1...` from `npub`
- deriving `sp1...` from `nip05`
- checking ownership of a Silent Payments address from public identity alone

Because those capabilities are important to OpenETR, this model is not the default OpenETR Silent Payments derivation contract.

## Consequences

By preserving the current OpenETR derivation model:

- OpenETR keeps public derivability
- OpenETR keeps the web and CLI ownership-check workflows
- OpenETR keeps a strong link between Nostr identity and Silent Payments identity
- OpenETR gains independent public verifiability of Silent Payments ownership

That independent verifiability means:

- anyone who knows the `npub`
- and knows the OpenETR derivation rule

can independently derive the expected `sp1...` address and verify that it belongs to that Nostr identity under the OpenETR convention.

This does not require:

- access to the `nsec`
- a separate signed attestation
- a private proof exchange

This is a deliberate OpenETR design choice.

OpenETR intentionally trades some off-chain identity unlinkability for independent public verifiability.

But:

- OpenETR should not assume the resulting `sp1...` addresses are directly interoperable with wallet software that expects a BIP-32 Silent Payments wallet tree

## Compatibility Strategy

If OpenETR later wants stronger external wallet interoperability, it should add a second explicit Silent Payments mode rather than replacing the current one.

Recommended future naming:

- `Nostr Silent Payments (NSP)`
- `Wallet-compatible Silent Payments`

The first mode preserves:

- public derivability
- identity ownership checks
- OpenETR identity semantics

The second mode could preserve:

- wallet import/export compatibility
- BIP-32 account structures
- broader cross-wallet expectations

These two modes should be treated as distinct derivation contracts and should not be silently merged.

## Operational Rule

OpenETR should continue to treat its current Silent Payments derivation as the canonical OpenETR identity-linked mode.

Any future wallet-compatible BIP-32 mode should be:

- additive
- explicitly labeled
- documented as a separate interoperability mode
