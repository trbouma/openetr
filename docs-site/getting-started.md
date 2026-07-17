# Using The App

The fastest way to use the MLWR Control Desk is the live application:

```text
https://openetr.org/
```

The app is designed for warehouse receipt workflows first. It lets you work in warehouse receipt language while the underlying OpenETR component publishes, queries, and verifies signed control records.

## What You Can Do

The Control Desk supports two broad modes.

| Mode | What You Can Do |
| --- | --- |
| Read-only | Query a receipt document by uploading the file and recomputing its digest. |
| Signed in | Select an acting profile, issue receipt origin events, and publish control records. |

Read-only users can inspect whether a receipt artifact has an OpenETR record.

Signed-in users can operate a Control Desk with profiles and signer keys.

## Control Desk Concepts

| Term | Meaning In The App |
| --- | --- |
| Control Desk | The operating surface for warehouse receipt actions. |
| Control Desk Key | The root/admin key used for recovery and profile management. |
| Acting Profile | The profile currently used to sign warehouse receipt actions. |
| Receipt Control Record | A signed OpenETR origin or control event. |
| Docs | Link back to this documentation site. |

The **Acting Profile** is the profile that signs operational actions such as issuing, transferring, encumbering, discharging, redeeming, or terminating a receipt.

## Query A Receipt

Use **Query Receipt State** when you have a warehouse receipt file and want to inspect its OpenETR state.

1. Open the Control Desk.
2. Upload the warehouse receipt file.
3. Confirm or adjust the relay field.
4. Select **Query Warehouse Receipt**.

The app computes the file digest locally in the request flow, queries the configured relays, and shows the origin event, current controller, lifecycle state, control events, and outstanding encumbrances where available.

## Sign In And Select An Acting Profile

To issue or control receipts, sign in with a Control Desk Key or session key.

When signed in, the Control Desk shows:

- the Control Desk Key;
- the Acting Profile;
- a profile selector;
- an **Update Current Profile** button;
- a **Backup Key** action for recovery material.

Use the profile selector to choose which profile should sign operational actions.

## Back Up The Control Desk Key

The **Backup Key** dialog lets you copy recovery material to the clipboard.

Store this material carefully. The Control Desk Key can organize and recover relay-backed profile configuration and signer records.

## Update The Acting Profile

Use **Update Current Profile** to edit the selected profile metadata.

Profile metadata may include:

- name;
- display name;
- about;
- address;
- website;
- NIP-05;
- LEI or other identifying fields.

The profile editor publishes an updated Nostr profile event for the acting signer.

## Issue A Receipt

Use **Issue Receipt** when the warehouse operator wants to publish the first OpenETR origin event for a warehouse receipt artifact.

The app:

1. hashes the uploaded receipt file;
2. creates the object id;
3. signs an origin event with the Acting Profile;
4. includes structured event tags such as receipt reference and goods description where provided;
5. publishes the event to the configured relay set.

The receipt file itself remains outside OpenETR. OpenETR records the digest and control evidence.

## Next Steps

- [Issuing Receipts](issuing-receipts.md)
- [Control Actions](control-actions.md)
- [Identity Model](identity-model.md)

For local development or deployment, see [Installation And Local Development](installation.md).
