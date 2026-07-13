# MLWR Change of Medium Profile

Status: Design note in progress.

This note captures the current OpenETR design discussion for changing a warehouse receipt between paper and electronic media under an MLWR-style profile.

Article 14 is related to Article 13, but it is not the same workflow. Article 13 concerns loss, destruction, failed control, and replacement. Article 14 concerns a deliberate change of medium. The goal is to preserve the same receipt relationship, rights, obligations, and claims while making the prior medium inoperative.

## Core Design Point

OpenETR should treat change of medium as an explicit control-relevant transition.

A plain `terminate` event is not expressive enough by itself. It can say that an electronic graph ended, but it does not explain:

- that the reason was a paper-to-electronic or electronic-to-paper conversion;
- which prior medium became inoperative;
- which successor medium became operative;
- which paper receipt identifier or electronic object is now active;
- whether rights, obligations, claims, and control state carried forward;
- which signer, warehouse operator, registry, or other authority recognized the change.

For that reason, the profile should likely introduce:

```text
action=change_medium
```

or an equivalent MLWR-specific profile rule that combines `attest`, `terminate`, and required structured tags. The current recommendation is to design a dedicated `change_medium` event shape.

## Paper Must Remain Queryable

The paper side should not disappear from the control layer.

If the current operative medium is paper, OpenETR should still be able to answer:

- Is this paper receipt currently active?
- Was this paper receipt converted from an electronic receipt?
- Was this paper receipt later converted back to an electronic receipt?
- Which signed event or authority supports that status?
- Are there outstanding encumbrances, claims, or warnings carried from the electronic graph?

This means a medium-change event should leave a signed lookup trail for paper identifiers as well as electronic object identifiers.

## Candidate Event Shape

The current OpenETR wire format already supports:

- `kind = 1416` control events;
- `action` tags;
- `o` tags for object lookup;
- `e` tags for graph links;
- `p` tags for participants where needed;
- `ref` tags for external references;
- named structured tags for domain metadata.

A candidate `change_medium` event could use:

```text
kind = 1416
action = change_medium
o = <current_or_prior_object_digest>
e = <prior_event_id>
from_medium = electronic | paper
to_medium = paper | electronic
paper_reference = <warehouse_or_registry_paper_receipt_id>
paper_digest = <optional_digest_of_scanned_or_canonical_paper_record>
electronic_object = <object_digest_or_nobj>
electronic_origin_event = <origin_event_id_or_nevent>
authority = <optional_authority_pubkey_or_reference>
ref = <external_registry_or_business_reference>
```

The exact tag names are still open. The important idea is that the event must identify both sides of the medium change well enough for later verification.

## Electronic to Paper

For electronic-to-paper conversion, the event should establish:

- the electronic receipt object or origin event being converted;
- the latest recognized control event or current controller before conversion;
- the paper receipt identifier that becomes operative;
- the authority or warehouse operator that issued or recognized the paper receipt;
- whether the electronic graph is now inoperative;
- what claims, encumbrances, or references carry forward.

Illustrative event data:

```text
action=change_medium
from_medium=electronic
to_medium=paper
old_object=<electronic_object_digest>
old_event=<latest_recognized_event_id>
paper_reference=WR-PAPER-000123
ref=registry-file-456
```

The verifier should not treat this as ordinary termination. It should treat it as a medium conversion and then check whether the policy recognizes the paper receipt as the operative record.

## Paper to Electronic

For paper-to-electronic conversion, the event should establish:

- the paper receipt identifier or paper digest being converted;
- the authority or warehouse operator that declares the paper receipt inoperative;
- the new electronic receipt object or origin event;
- the initial electronic controller;
- any claims, encumbrances, or references carried from the paper context.

Illustrative event data:

```text
action=change_medium
from_medium=paper
to_medium=electronic
paper_reference=WR-PAPER-000123
paper_digest=<optional_digest>
new_object=<electronic_object_digest>
new_origin_event=<electronic_origin_event_id>
ref=registry-file-789
```

The verifier should be able to query the paper reference and discover that the paper medium has become inoperative because a recognized electronic receipt now exists.

## Active Medium State

The verifier should derive an active medium state, separate from ordinary lifecycle state.

Possible states include:

- `electronic_active`
- `paper_active`
- `medium_change_pending`
- `medium_change_disputed`
- `paper_superseded_by_electronic`
- `electronic_superseded_by_paper`
- `unknown_or_conflicting_medium`

This is not the same as `active`, `redemption_pending`, or `terminated`. A receipt may remain legally alive while the operative medium changes.

## Relationship to Termination

`terminate` may still be useful, but it should not carry the whole meaning of Article 14.

Possible options:

1. `change_medium` itself marks the prior medium inoperative under policy.
2. `change_medium` must be followed by `terminate` on the prior electronic graph.
3. `terminate` may be used only as a compatibility signal, while `change_medium` carries the legal reason and successor reference.

The current design preference is option 1 or 3. A single explicit `change_medium` event is easier for verifiers to reason about than a loosely coupled `attest` plus `terminate` sequence.

## Verifier Behavior

A verifier should enumerate the medium-change evidence and explain its policy conclusion.

It should show:

- the prior medium;
- the successor medium;
- the paper reference, if any;
- the electronic object or origin event, if any;
- the current or prior controller at the time of change;
- the authority or signer that declared the change;
- supporting references or registry records;
- outstanding encumbrances or claims;
- whether the prior medium is recognized as inoperative;
- whether the successor medium is recognized as active;
- warnings for missing links, missing authority, unknown signer, or conflicting active media.

The verifier should warn if both paper and electronic records appear active for the same receipt context.

## Open Questions

- Should `change_medium` be a generic OpenETR action or an MLWR-only domain action?
- What exact tag names should be used for `from_medium`, `to_medium`, `paper_reference`, and electronic references?
- Should paper references be relay-queryable with a short tag, or carried as named metadata only?
- Should a paper receipt have its own object digest even if OpenETR is not the operative control medium?
- Who must sign a medium-change event: current controller, warehouse operator, registry, both, or another authority?
- How do outstanding encumbrances carry across media?
- Does conversion require acceptance by the new controller or holder?
- How does a verifier distinguish unauthorized paper issuance from recognized medium change?
- Should the webapp expose medium state separately from lifecycle state?

## Boundary

OpenETR can preserve the signed evidence that a medium change was declared, linked, and recognized by specified signers.

It cannot by itself decide that a paper receipt was legally made inoperative, that an electronic receipt became legally effective, or that rights and obligations carried forward. Those conclusions belong to the MLWR enactment, storage agreement, warehouse operator policy, registry/platform rules, court or arbitral forum, and verifier policy.

