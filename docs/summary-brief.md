# Silent Wallet Summary Brief

OpenETR's Silent Payments model creates a distinct **Silent Wallet** for a Nostr identity.

Under the OpenETR derivation rule, a Silent Payment address can be deterministically derived from a known `npub`. This means every Nostr identity can be treated as having a corresponding Silent Wallet, even if the identity owner has never explicitly published or acknowledged it.

This creates several important properties:

- **Independent verifiability**: anyone who knows the `npub` and the OpenETR derivation rule can derive the expected Silent Payment address and verify it independently.
- **Anti-spoofing assurance**: a sender does not need to trust a pasted or manually shared address. The correct Silent Payment address is fixed by the recipient identity and can be derived locally.
- **Plausible deniability**: because anyone can derive the Silent Payment address from the `npub`, the existence of that address does not prove the `nsec` holder intentionally created, published, or even knew about it.
- **Private receipt detection**: while the Silent Payment address is publicly derivable, only the holder of the matching private scan key can detect which on-chain outputs belong to the Silent Wallet.
- **Private fund control**: only the holder of the matching private spend path can sweep or spend the detected outputs.

This protects both the sender and the recipient.

- The sender is protected because they can derive the correct receive address themselves and avoid spoofed payment instructions.
- The recipient is protected because incoming payments do not expose a reusable on-chain receive address, and detected outputs can be swept to unrelated addresses.

As a result, the funding relationship between donor and recipient is difficult to establish from public chain data alone.

The key architectural insight is that OpenETR differs from a wallet-style Silent Payments implementation in **how the receiver's base Silent Payments keys are derived**.

- In OpenETR, the Silent Wallet is derived from Nostr identity using deterministic additive tweaks.
- In a wallet-style implementation, the Silent Payments keys are usually derived from private seed material through a BIP-32 tree.

The resulting `sp1...` address is still the same kind of Silent Payments object in both cases, so a sender paying to it may see no practical difference. The difference shows up on the receiver side: scanning, recovery, and wallet interoperability depend on whether the wallet can reconstruct the matching private scan and spend keys from the same derivation contract.

For practical purposes, the Silent Wallet should be treated as its own distinct wallet model:

- it is identity-linked
- it is privately discoverable
- it is publicly verifiable
- it is difficult to attribute to intentional publication
- and it preserves the core on-chain privacy benefits of Silent Payments

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

The OpenETR Silent Wallet approach reduces those gaps significantly.

The sender can derive the correct Silent Payment address directly from the recipient identity, so there is no need to trust:

- a copied payment address
- an address provided by a third party
- an address embedded in a message that could have been altered or spoofed

That means the sender has strong assurance they paid the correct identity without relying on a separate trusted address-distribution channel.

At the same time, the recipient can later confirm receipt using private scan knowledge and, if needed, produce signed statements about receipt or sweeping without the blockchain itself exposing a reusable public funding relationship.

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
