from __future__ import annotations

from dataclasses import dataclass

from monstr.event.event import Event


ORIGIN_KIND = 31415
CONTROL_EVENT_KIND = 31416

ACTION_INITIATE = "initiate"
ACTION_ACCEPT = "accept"
ACTION_TERMINATE = "terminate"
ACTION_ATTEST = "attest"
ACTION_ENCUMBER = "encumber"
ACTION_DISCHARGE = "discharge"
ACTION_REDEEM = "redeem"

CONTROL_ACTIONS = {
    ACTION_INITIATE,
    ACTION_ACCEPT,
    ACTION_TERMINATE,
    ACTION_ATTEST,
    ACTION_ENCUMBER,
    ACTION_DISCHARGE,
    ACTION_REDEEM,
}
CONTROLLER_STATE_ACTIONS = {ACTION_INITIATE, ACTION_TERMINATE}
LIFECYCLE_STATE_ACTIONS = {ACTION_INITIATE, ACTION_REDEEM, ACTION_TERMINATE}


@dataclass(frozen=True)
class ControlActionSpec:
    action: str
    label: str
    d_suffix: str
    marker: str
    participant_label: str | None = None
    changes_controller: bool = False
    terminates: bool = False
    redemption_pending: bool = False


ACTION_SPECS = {
    ACTION_INITIATE: ControlActionSpec(
        action=ACTION_INITIATE,
        label="transfer initiate",
        d_suffix=ACTION_INITIATE,
        marker="->",
        participant_label="transferee",
        changes_controller=True,
    ),
    ACTION_ACCEPT: ControlActionSpec(
        action=ACTION_ACCEPT,
        label="transfer accept",
        d_suffix=ACTION_ACCEPT,
        marker="->",
        participant_label="counterparty",
    ),
    ACTION_TERMINATE: ControlActionSpec(
        action=ACTION_TERMINATE,
        label="terminate",
        d_suffix=ACTION_TERMINATE,
        marker="--",
        terminates=True,
    ),
    ACTION_ATTEST: ControlActionSpec(
        action=ACTION_ATTEST,
        label="attest",
        d_suffix=ACTION_ATTEST,
        marker="=>",
        participant_label="subject",
    ),
    ACTION_ENCUMBER: ControlActionSpec(
        action=ACTION_ENCUMBER,
        label="encumber",
        d_suffix=ACTION_ENCUMBER,
        marker="+$",
        participant_label="beneficiary",
    ),
    ACTION_DISCHARGE: ControlActionSpec(
        action=ACTION_DISCHARGE,
        label="discharge",
        d_suffix=ACTION_DISCHARGE,
        marker="-$",
        participant_label="releasing party",
    ),
    ACTION_REDEEM: ControlActionSpec(
        action=ACTION_REDEEM,
        label="redeem",
        d_suffix=ACTION_REDEEM,
        marker="**",
        participant_label="obligor",
        redemption_pending=True,
    ),
}


def first_tag_value(event: Event, tag_name: str) -> str | None:
    values = event.get_tags_value(tag_name)
    return values[0] if values else None


def control_action(event: Event) -> str | None:
    action = first_tag_value(event, "action")
    if action is None:
        return None
    return action.strip().lower()


def action_spec(action: str | None) -> ControlActionSpec:
    return ACTION_SPECS.get(
        action or "",
        ControlActionSpec(
            action=action or "unknown",
            label="control event",
            d_suffix=action or "unknown",
            marker="->",
            participant_label="participant",
        ),
    )


def action_d_value(object_digest: str, action: str) -> str:
    return f"{object_digest}:{action_spec(action).d_suffix}"


def is_controller_state_action(action: str | None) -> bool:
    return action in CONTROLLER_STATE_ACTIONS


def is_lifecycle_state_action(action: str | None) -> bool:
    return action in LIFECYCLE_STATE_ACTIONS


def is_valid_pubkey_hex(value: str | None) -> bool:
    if value is None or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def first_p_tag_pubkey(event: Event) -> str | None:
    candidate = first_tag_value(event, "p")
    if not is_valid_pubkey_hex(candidate):
        return None
    return candidate.lower()
