# MLWR Receipt Replacement and Loss Profile

Status: Design note in progress.

This note captures the current OpenETR design discussion for lost, destroyed, or failed-control warehouse receipts under an MLWR-style profile.

Article 13 is one of the places where the OpenETR control graph meets a harder legal workflow. OpenETR can preserve signed evidence about what happened, but it should not by itself decide when a warehouse receipt is legally lost, destroyed, replaced, or made inoperative.

## Core Gap

OpenETR can prove and display evidence such as:

- this receipt object existed;
- this origin event identified the receipt;
- this profile signed the origin event;
- this key or profile appeared to control the receipt under the evaluated graph;
- this graph was terminated or otherwise marked as ended;
- this replacement receipt was issued;
- this authority, warehouse operator, registry, court, or trusted participant signed an attestation;
- these two receipt graphs are linked;
- these competing origin or control graphs exist for the same underlying goods or receipt context.

Article 13 asks a different question:

When is a receipt legally lost or destroyed, and when is a replacement legally valid?

That question is not only a protocol question. It depends on the applicable MLWR enactment, storage agreement, warehouse operator duties, registry or platform rules, court or arbitral orders, notice requirements, indemnity rules, and verifier policy.

## Electronic Loss

For electronic receipts, "loss" may mean failure of the Article 6 control conditions or loss of practical control.

Possible examples include:

- the current controller can no longer exercise control;
- the graph can no longer satisfy Article 6 reliability or exclusive-control requirements;
- the authoritative control state is ambiguous;
- the signing key was compromised, destroyed, or lost;
- required events, relays, stores, or attestations are unavailable;
- multiple competing origin or control graphs make recognition unsafe;
- a warehouse operator, registry, court, or other recognized authority declares the receipt lost or control failed.

OpenETR can record evidence of these conditions and can surface verifier warnings. It should not automatically decide that these facts are sufficient for legal loss or replacement.

## Proposed Replacement Workflow

A future MLWR replacement profile should define a clear replacement procedure.

At a high level, the workflow may look like this:

1. A participant declares that the receipt is lost, destroyed, compromised, or no longer satisfies Article 6 control conditions.
2. Required parties review or attest the loss. Depending on policy, this may include the current controller, warehouse operator, registry, court, secured party, or other authority.
3. The original receipt graph is marked cancelled, terminated, superseded, or otherwise inoperative under the selected policy.
4. A replacement receipt is issued as a new origin event or controlled object.
5. The replacement links back to the original receipt, original origin event, or loss declaration.
6. Verifiers know which graph to recognize and which graph to treat as cancelled, replaced, warning-only, or disputed.

## Open Design Questions

The profile needs to answer at least these questions:

- Who can declare loss?
- Who must authorize replacement?
- Is the existing `terminate` action enough, or should OpenETR add `action=replace`, `action=cancel`, `action=supersede`, or another MLWR-specific action?
- Should replacement be modeled as a new origin event, a new controlled object, or a linked continuation of the original object?
- How should the replacement link to the original receipt: `e` reference, `ref`, structured tags, original object digest, or a combination?
- How should the system prevent or warn about two active receipts for the same goods?
- What notice, waiting period, indemnity, registry, court, or warehouse-operator evidence is required?
- What should the verifier show when the original graph and replacement graph conflict?
- Which failures are hard invalidity, which are warnings, and which are recognition-layer non-recognition?
- What is only evidence, and what is legal recognition?

## Possible Event Model

The current implementation already has useful pieces:

- origin events for issued receipt objects;
- control events for later control-relevant actions;
- `e` links to connect graph events;
- `o` tags to query by object digest;
- `terminate` to end a lifecycle under policy;
- `attest` for signed statements by authorities, registries, warehouse operators, auditors, or other participants;
- `ref` for external references such as registry files, court files, claim numbers, or business references.

A future profile could define a replacement sequence using existing actions first:

1. `attest` with `type=loss` or `type=control_failure`.
2. `terminate` or cancellation-style event on the original graph.
3. New `issue` event for the replacement receipt.
4. `attest` with `type=replacement` linking the replacement back to the original receipt or loss declaration.

If this becomes too ambiguous, OpenETR may need a dedicated action such as:

- `replace`
- `cancel`
- `supersede`
- `declare_loss`

The design should avoid adding a new action until it is clear that existing `attest` and `terminate` events cannot express the workflow safely.

## Verifier Behavior

A verifier should not hide evidence merely because a replacement workflow is incomplete or disputed.

Instead, it should enumerate the relevant graph evidence and annotate it:

- original origin event;
- original control chain;
- current controller before alleged loss;
- loss or control-failure declarations;
- required attestations;
- termination, cancellation, or supersession events;
- replacement origin event;
- links between original and replacement;
- outstanding encumbrances or claims;
- warnings about missing approvals, missing links, duplicate active graphs, or unknown signers;
- the selected policy's recognition result.

The verifier may then classify the state under policy, for example:

- active original receipt;
- loss alleged but not recognized;
- replacement pending;
- original cancelled and replacement recognized;
- competing graphs require manual review;
- replacement rejected under policy;
- no recognized active receipt.

## Boundary

OpenETR's role is to make the replacement evidence inspectable, signed, queryable, and replayable.

The legal conclusion belongs elsewhere. An MLWR replacement profile, registry, court, arbitral forum, warehouse operator policy, or relying system must decide:

- whether the receipt was lost or destroyed;
- whether control failed;
- whether replacement was authorized;
- whether the old receipt is inoperative;
- whether the replacement receipt is legally effective;
- whether any claims, encumbrances, or holder protections survive replacement.

This boundary is important. Replacement affects the integrity of the entire control model. The design should be specified before implementation rather than hidden inside a convenience command.

