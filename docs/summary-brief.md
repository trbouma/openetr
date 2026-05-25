Skip to content
 
# Nostr Silent Payments (NSP) Summary Brief

[Jump to Infographic](#infographic)

The BIP-352 Silent Payments proposal creates an opportunity to define a distinct **Nostr Silent Payments (NSP)** derivation model for a Nostr identity.

This work arose from related efforts to derive a Taproot (`p2tr`) address from a Nostr public key and to understand how Nostr identity material could map deterministically into Bitcoin wallet semantics. That earlier exploration made it clear that the same identity-linked approach could be extended beyond a single visible Taproot address into a richer Silent Payments receive model.

One of its most important properties is that Silent Payments can provide a **static payment address**: a stable Silent Payments receive identity that can be reused by senders without creating a reusable on-chain receive address.

Under the Nostr Silent Payments derivation rule, a Silent Payment address can be deterministically derived from a known `npub`. This means every Nostr identity can be treated as having a corresponding Nostr Silent Payments address model, even if the identity owner has never explicitly published or acknowledged it.

This creates several important properties:

- **Independent verifiability**: anyone who knows the `npub` and the Nostr Silent Payments derivation rule can derive the expected Silent Payment address and verify it independently.
- **Anti-spoofing assurance**: a sender does not need to trust a pasted or manually shared address. The correct Silent Payment address is fixed by the recipient identity and can be derived locally.
- **Plausible deniability**: because anyone can derive the Silent Payment address from the `npub`, the existence of that address does not prove the `nsec` holder intentionally created, published, or even knew about it.
- **Private receipt detection**: while the Silent Payment address is publicly derivable, only the holder of the matching private scan key can detect which on-chain outputs belong to the identity-derived Nostr Silent Payments model.
- **Private fund control**: only the holder of the matching private spend path can sweep or spend the detected outputs.

## Important Security Caveats

NSP has a strong sender-verification and receiver-privacy story, but it also has an important scanning constraint that must be understood clearly.

In the NSP derivation model:

- `scan_priv = d + t_scan mod n`
- `t_scan` is publicly computable from the `npub`
- anyone who learns `scan_priv` can recover `d`
- once `d` is known, the observer can also derive `spend_priv`

This means:

- the NSP scan private key is root-equivalent
- disclosing `scan_priv` discloses the underlying `nsec`
- disclosing `scan_priv` also discloses the NSP spend private key
- NSP is a strong **local-scanning** model
- NSP is **not** a safe untrusted remote-scanning model

Operationally, that means:

- local scanning is the preferred NSP model
- self-hosted or fully trusted scanner infrastructure can be acceptable
- untrusted third-party remote scanners should not be treated as safe for NSP
- the sender-side benefits of public derivability remain intact even though the receiver-side scan key must be handled as a root secret

This protects both the sender and the recipient.

- The sender is protected because they can derive the correct receive address themselves and avoid spoofed payment instructions.
- The recipient is protected because incoming payments do not expose a reusable on-chain receive address, and detected outputs can be swept to unrelated addresses.

As a result, the funding relationship between donor and recipient is difficult to establish from public chain data alone.

The key architectural insight is that Nostr Silent Payments differs from a wallet-style Silent Payments implementation in **how the receiver's base Silent Payments keys are derived**.

- The Nostr Silent Payments model is derived from Nostr identity using deterministic additive tweaks.
- In a wallet-style implementation, the Silent Payments keys are usually derived from private seed material through a BIP-32 tree.

The resulting `sp1...` address is still the same kind of Silent Payments object in both cases, so a sender paying to it may see no practical difference. The difference shows up on the receiver side: scanning, recovery, and wallet interoperability depend on whether the wallet can reconstruct the matching private scan and spend keys from the same derivation contract.

For practical purposes, Nostr Silent Payments should be treated as its own distinct derivation and recovery model:

- it is identity-linked
- it is privately discoverable
- it is publicly verifiable
- it is difficult to attribute to intentional publication
- and it preserves the core on-chain privacy benefits of Silent Payments

There is also a direct traceability tradeoff to understand.

- NSP gives stronger independent verification than a published `sp1...` address string alone, because a sender can derive the correct address from a known `npub` or human-readable `NIP-05`
- this is especially useful when the recipient has no better public communication channel than a profile, website, or `NIP-05` identifier
- but that same public derivability means the static Silent Payment address is more attributable to the public Nostr identity than in a seed-derived BIP-352 wallet
- the tradeoff is therefore stronger sender assurance and anti-spoofing on one side, and weaker off-chain identity unlinkability on the other

What does not materially change is the on-chain privacy model:

- the static `sp1...` address still does not appear on-chain
- each payment still lands as a fresh Taproot-looking output
- outsiders still cannot trivially identify which outputs belong to that static address without the relevant scan key material

## High-Risk and Adversarial Environments

This model has especially important implications in high-risk or adversarial environments where counterparties may be required to:

- send payment to a known identity
- later confirm receipt
- produce signed confirmations or acknowledgements

In those environments, ordinary payment coordination often creates trust gaps that must be managed by:

- intermediaries
- compliance staff
- auditors
- counterparties maintaining off-chain address books and attribution records

The Nostr Silent Payments (NSP) approach reduces those gaps significantly.

The sender can derive the correct Silent Payment address directly from the recipient identity, so there is no need to trust:

- a copied payment address
- an address provided by a third party
- an address embedded in a message that could have been altered or spoofed

That means the sender has strong assurance they paid the correct identity without relying on a separate trusted address-distribution channel.

At the same time, the recipient can later confirm receipt using private scan knowledge and, if needed, produce signed statements about receipt or sweeping without the blockchain itself exposing a reusable public funding relationship.

In practice, for NSP, that receipt detection should be treated as a local or fully trusted-operator function. A third-party scanner can technically discover NSP receipts, but using one requires disclosing a root-equivalent scan key and therefore giving up the wallet's key isolation.

This changes the operational trust model in an important way:

- address authenticity can be derived independently
- receipt detection can be performed privately by the intended recipient
- receipt confirmation can be made explicitly and deliberately, rather than inferred from public chain data

As a result, many of the trust gaps that would otherwise need to be:

- maintained by third parties
- documented through shared address registries
- or risk-managed through manual verification procedures

are reduced or eliminated by the cryptographic structure itself.

In short, this approach lets counterparties:

- derive the correct payment destination independently
- avoid spoofed payment instructions
- confirm receipt deliberately and privately
- and do so without exposing a durable public linkage between sender and recipient on-chain

## Protecting Vulnerable Donors and Recipients

This model is also important for protecting vulnerable donors who might otherwise reveal themselves unintentionally through ordinary Bitcoin payment coordination.

A useful real-world example is the 2022 Canadian trucker protest funding environment. During that period:

- donor information associated with crowdfunding support for the convoy was leaked and reported on publicly, exposing names, email addresses, locations, and other identifying details in many cases; see [ABC News](https://www.abc.net.au/news/2022-02-16/australians-donate-to-canadian-convoy-givesendgo-fundraiser/100832928) and [The Guardian](https://www.theguardian.com/world/2022/feb/14/foreign-money-funding-extremism-in-canada-says-hacker)
- crypto-related accounts and addresses associated with convoy funding were identified and targeted by authorities and intermediaries; see [Reuters via Investing.com](https://www.investing.com/news/stock-market-news/td-bank-freezes-two-accounts-that-received-c14-million-in-support-of-canada-protests-2762814) and reporting on address blacklisting such as [CryptoAdventure](https://cryptoadventure.com/canadas-national-police-blacklist-34-crypto-addresses-involved-with-trucker-convoy/)

That episode shows how vulnerable both donors and recipients can become when:

- payment destinations are publicly reused
- recipient infrastructure is easy to map
- donor activity can be linked to known recipient endpoints
- third parties can identify, freeze, or pressure visible funding paths

The Nostr Silent Payments model helps prevent or sharply reduce that exposure.

With the Nostr Silent Payments model:

- the sender can derive the correct destination from identity without relying on a publicly circulated payment address
- that independent derivation is stronger than merely trusting an `sp1...` address published on a website, profile page, or message thread, because those published address strings can be spoofed, replaced, or tampered with
- in many real cases the recipient may have no safer public communication channel than a human-readable `NIP-05` address, and NSP lets the sender resolve that identity and derive the correct Silent Payment address locally
- the reusable `sp1...` receive identity does not appear on-chain
- the actual received outputs are not publicly obvious without the private scan key
- the recipient can later sweep funds to unrelated addresses, reducing durable public linkage

This makes it much harder to:

- track down vulnerable donors from a known public Bitcoin address reuse pattern
- map incoming payments to a publicly attributed recipient address
- establish a clear public funding relationship between a specific donor and recipient from chain data alone

In that sense, the Nostr Silent Payments model protects both sides:

- the donor is less likely to reveal themselves by paying a publicly watchable recipient address
- the donor is less likely to be tricked by a spoofed or substituted Silent Payment address, because the correct destination can be derived independently from the intended Nostr identity
- the recipient is less likely to have their funding flows mapped and attributed through visible receive infrastructure

Everything here comes with tradeoffs, and that should be stated plainly.

- NSP gives stronger sender-side address assurance than a published `sp1...` string alone
- NSP is especially useful when the only practical public identifier is an `npub` or a human-readable `NIP-05`
- NSP improves recipient privacy on-chain and in payment coordination
- but NSP also requires that receipt scanning be kept local or limited to fully trusted scanner infrastructure because the NSP scan key is root-equivalent

So the correct conclusion is not that NSP removes every risk. It is that NSP removes one of the largest and most common privacy failures in Bitcoin payments, while introducing a clear operational requirement around how the receiver performs scanning.

The Nostr Silent Payments (NSP) model shows that Bitcoin payments do not have to force a tradeoff between identity assurance and financial privacy. By making the correct receive identity independently derivable from Nostr while keeping on-chain receipt discovery and fund control private, this approach creates a stronger, safer, and more trustworthy payment model for both senders and recipients. It reduces spoofing risk, narrows operational trust gaps, protects vulnerable counterparties, and opens the door to a form of Bitcoin coordination that is more resilient in ordinary use and far more defensible in adversarial environments.

This also offers an important practical privacy advantage relative to layered Bitcoin privacy solutions such as Lightning and Cashu. Those systems can provide strong privacy properties, but they introduce additional infrastructure and additional trust or operational dependencies, including node operators, routing assumptions, channel management, or mint operators. The Nostr Silent Payments (NSP) model achieves a comparable improvement in payment privacy at the address-coordination layer without requiring the user to rely on a Lightning node, a federated or custodial mint, or other specialized intermediary infrastructure. The result is a simpler privacy model built directly on Bitcoin and Nostr identity semantics, with fewer moving parts and fewer third-party trust assumptions at the address-coordination layer, provided NSP receipt scanning remains local or confined to fully trusted scanner infrastructure.

## Technical Addendum

The NSP approach leverages the BIP-352 payment model, but changes the base derivation layer.

BIP-352:

- starts from already-existing Silent Payments private keys (usually generated by a wallet hardware or app)
- does not prescribe where these keys came from

NSP:

- derives Silent Payments keys deterministically from the publicly known Nostr identity key (`npub`)

So the BIP-352 base derivation is essentially:

- “pick or derive private keys, then compute pubkeys”

NSP is simply adding another base-derivation option:

- “start from the publicly known Nostr key d/P, derive additive tweaks, and turn that into scan/spend keys”

So in a nutshell, the core difference is this: instead of starting from an already-existing Silent Payments wallet keyset, NSP derives the receiver’s base Silent Payments keys from the publicly known Nostr identity (`npub`).
Everything else is the same at the sender and address-format layer. There is no difference in how the Silent Payments addresses are used on the sending side, but the receiver (the `nsec` holder) needs to know the NSP recovery rule.

Math details on the NSP base derivation:

Let:

```
d = Nostr private key
P = dG = Nostr public key
```

where `d` is the scalar value of the `nsec`

Derive deterministic tweaks:

```
t_scan = H_tag("nostr-sp/scan", P)
t_spend = H_tag("nostr-sp/spend", P)
```

Then:

```
ScanPub = P + t_scan G
SpendPub = P + t_spend G
```

the two public keys are encoded into the address:

```
sp1... = bech32m(v0 || ScanPub || SpendPub)
```


and privately:

```
scan_priv = d + t_scan mod n
spend_priv = d + t_spend mod n
```

This additive derivation also creates the most important security caveat in the NSP model:

```
d = scan_priv - t_scan mod n
```

Because `t_scan` is publicly computable from the `npub`, anyone who learns `scan_priv` can recover `d` and then derive `spend_priv`. So NSP scanning should be treated as local-only or trusted-scanner-only. It should not be described as a safe untrusted remote-scanning model.

As far as any sending wallet is concerned, the `sp1...` address is nothing special; it is just another Silent Payments address. However for the receiver, they need to know how to recover against those address using `d` (their `nsec`)

The opsec recommendation is to never spend from this wallet to an address outside of your control. Always sweep to a fresh address under your control.

Some might philosophically object to using the `nsec` this way, but NSP gives every Nostr identity an attributable Silent Payments derivation by default while still preserving plausible deniability about intentional publication or awareness.

## Further Reading

- [BIP-352 Silent Payments](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki)
- [Silent Payments Design Note](./specs/SILENT_PAYMENTS_DESIGN_NOTE.md)
- [Nostr Silent Payments Derivation Decision Note](./specs/SILENT_PAYMENTS_DERIVATION_DECISION_NOTE.md)
- [Nostr Silent Payments Specification Note](./specs/NOSTR_SILENT_PAYMENTS_SPEC.md)

## Infographic

![Infographic](https://raw.githubusercontent.com/trbouma/openetr/main/docs/images/nsp.jpg)
