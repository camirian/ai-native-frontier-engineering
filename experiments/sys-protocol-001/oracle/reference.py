"""Independent symbolic reference model for MISSION-SYS-PROTOCOL-001.

This module was authored from the frozen mission contract only.  It does not
import, call, or encode any candidate architecture or candidate transition
table.  It interprets event traces against explicit protocol state.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


ACTIVE = {"OPEN_SENT", "OPEN", "CLOSE_SENT"}


@dataclass
class Model:
    state: str = "IDLE"
    session_id: int | None = None
    next_send: int = 0
    expected_recv: int = 0
    last_delivered: int | None = None
    last_acked: int | None = None
    outstanding: dict[str, Any] | None = None
    open_retries: int = 0
    data_retries: int = 0
    close_retries: int = 0

    def snapshot(self) -> dict[str, Any]:
        return asdict(self)

    def reset(self) -> None:
        self.__dict__.update(Model().__dict__)


def _reply(kind: str, model: Model, **detail: Any) -> dict[str, Any]:
    return {"result": kind, "state": model.state, "detail": detail,
            "snapshot": model.snapshot()}


def step(model: Model, event: dict[str, Any]) -> dict[str, Any]:
    """Apply one event.  ``OK``, ``INVALID``, and ``IGNORED`` are explicit."""
    before = model.snapshot()
    kind = event.get("type")
    sid = event.get("session_id")

    def invalid(reason: str) -> dict[str, Any]:
        assert model.snapshot() == before, "invalid event mutated oracle state"
        return _reply("INVALID", model, reason=reason)

    if kind == "RESET":
        if model.state in {"ABORTED", "CLOSED"}:
            model.reset()
            return _reply("OK", model, action="reset")
        return invalid("reset_allowed_only_from_terminal_state")

    if kind == "ABORT":
        if model.state in ACTIVE:
            model.state = "ABORTED"
            return _reply("OK", model, action="abort")
        return invalid("abort_not_valid_in_state")

    if kind == "OPEN_REQ":
        if model.state != "IDLE":
            return invalid("open_requires_idle")
        if not isinstance(sid, int) or sid <= 0:
            return invalid("session_id_must_be_positive_integer")
        model.session_id, model.state, model.open_retries = sid, "OPEN_SENT", 0
        return _reply("OK", model, action="open_sent")

    if kind == "OPEN_ACK":
        if model.state != "OPEN_SENT":
            return invalid("open_ack_not_valid_in_state")
        if sid != model.session_id:
            return invalid("open_ack_session_mismatch")
        model.state, model.open_retries = "OPEN", 0
        return _reply("OK", model, action="opened")

    if kind == "DATA":
        direction = event.get("direction")
        if model.state != "OPEN":
            return invalid("data_requires_open")
        if sid != model.session_id:
            return invalid("data_session_mismatch")
        seq = event.get("seq")
        if not isinstance(seq, int) or seq < 0:
            return invalid("sequence_must_be_nonnegative_integer")
        if direction == "LOCAL":
            if model.outstanding is not None:
                return invalid("local_data_already_outstanding")
            if seq != model.next_send:
                return invalid("local_sequence_must_equal_next_send")
            model.outstanding = {"seq": seq, "payload_id": event.get("payload_id")}
            model.next_send += 1
            model.data_retries = 0
            return _reply("OK", model, action="data_transmitted")
        if direction == "PEER":
            if seq == model.expected_recv:
                model.last_delivered = seq
                model.expected_recv += 1
                return _reply("OK", model, action="data_delivered_and_acked")
            if seq == model.expected_recv - 1:
                return _reply("OK", model, action="duplicate_acked_not_delivered")
            # A2 routing: an older-than-most-recent duplicate is invalid.
            return invalid("received_data_out_of_order_or_old_duplicate")
        return invalid("data_direction_must_be_LOCAL_or_PEER")

    if kind == "DATA_ACK":
        if model.state != "OPEN":
            return invalid("data_ack_requires_open")
        if sid != model.session_id:
            return invalid("data_ack_session_mismatch")
        seq = event.get("seq")
        if model.outstanding is not None and seq == model.outstanding["seq"]:
            model.last_acked = seq
            model.outstanding = None
            model.data_retries = 0
            return _reply("OK", model, action="outstanding_data_acked")
        if model.outstanding is None and seq == model.last_acked:
            return _reply("OK", model, action="duplicate_ack_idempotent")
        return invalid("future_or_nonrecent_data_ack")

    if kind == "CLOSE_REQ":
        if model.state != "OPEN":
            return invalid("close_requires_open")
        if sid != model.session_id:
            return invalid("close_session_mismatch")
        if model.outstanding is not None:
            return invalid("close_requires_no_local_outstanding_data")
        model.state, model.close_retries = "CLOSE_SENT", 0
        return _reply("OK", model, action="close_sent")

    if kind == "CLOSE_ACK":
        if model.state == "CLOSED" and sid == model.session_id:
            return _reply("IGNORED", model, action="duplicate_close_ack")
        if model.state != "CLOSE_SENT":
            return invalid("close_ack_not_valid_in_state")
        if sid != model.session_id:
            return invalid("close_ack_session_mismatch")
        model.state, model.close_retries = "CLOSED", 0
        return _reply("OK", model, action="closed")

    if kind == "TIMEOUT":
        timer = event.get("timer_name")
        if model.state == "OPEN_SENT" and timer == "open_timer":
            model.open_retries += 1
            if model.open_retries == 3:  # A1: abort on receipt of third timeout.
                model.state = "ABORTED"
                return _reply("OK", model, action="open_timeout_abort")
            return _reply("OK", model, action="retransmit_open")
        if model.state == "OPEN" and timer == "data_timer" and model.outstanding is not None:
            model.data_retries += 1
            if model.data_retries == 3:
                model.state = "ABORTED"
                return _reply("OK", model, action="data_timeout_abort")
            return _reply("OK", model, action="retransmit_data")
        if model.state == "CLOSE_SENT" and timer == "close_timer":
            model.close_retries += 1
            if model.close_retries == 3:
                model.state = "ABORTED"
                return _reply("OK", model, action="close_timeout_abort")
            return _reply("OK", model, action="retransmit_close")
        return invalid("timeout_not_active_for_state")

    return invalid("unknown_event")


def run(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    model = Model()
    return [step(model, event) for event in events]
