"""Event-dispatch implementation of the frozen session-protocol requirements.

This module deliberately uses state-specific handlers rather than a transition
table.  ``Protocol.step`` is also an importable deterministic API.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any, Callable


STATES = {"IDLE", "OPEN_SENT", "OPEN", "CLOSE_SENT", "CLOSED", "ABORTED"}


@dataclass
class SessionState:
    state: str = "IDLE"
    session_id: int | None = None
    next_tx_seq: int = 0
    expected_rx_seq: int = 0
    outstanding: dict[str, Any] | None = None
    last_acked_seq: int | None = None
    last_delivered_seq: int | None = None
    retries: dict[str, int] = field(
        default_factory=lambda: {"open_timer": 0, "data_timer": 0, "close_timer": 0}
    )


class Protocol:
    """A single LOCAL endpoint. Events are JSON-compatible mappings."""

    def __init__(self) -> None:
        self.data = SessionState()
        self._handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
            "IDLE": self._idle,
            "OPEN_SENT": self._open_sent,
            "OPEN": self._open,
            "CLOSE_SENT": self._close_sent,
            "CLOSED": self._closed,
            "ABORTED": self._aborted,
        }

    @classmethod
    def from_snapshot(cls, snapshot: dict[str, Any] | None) -> "Protocol":
        """Build an endpoint from an API snapshot, without sharing caller state."""
        machine = cls()
        if snapshot is None:
            return machine
        if not isinstance(snapshot, dict):
            raise ValueError("state must be an object or null")
        values = {key: deepcopy(snapshot.get(key, getattr(machine.data, key))) for key in SessionState.__dataclass_fields__}
        if values["state"] not in STATES:
            raise ValueError("unknown protocol state")
        if not isinstance(values["retries"], dict):
            raise ValueError("retries must be an object")
        machine.data = SessionState(**values)
        return machine

    def snapshot(self) -> dict[str, Any]:
        return asdict(self.data)

    def transmit_data(self, payload_id: Any) -> dict[str, Any]:
        """Locally transmit the next DATA item while OPEN (R07--R09).

        The frozen event list has no distinct local-send event, while ``DATA``
        is required to model received delivery.  This command API makes the
        local action explicit without inventing another wire event.
        """
        if self.data.state != "OPEN":
            return {"valid": False, "code": "transmit_data_requires_open", "actions": [], "state": self.data.state, "snapshot": self.snapshot()}
        if self.data.outstanding is not None:
            return {"valid": False, "code": "outstanding_data_ack", "actions": [], "state": self.data.state, "snapshot": self.snapshot()}
        seq = self.data.next_tx_seq
        self.data.next_tx_seq += 1
        self.data.outstanding = {"seq": seq, "payload_id": payload_id}
        self.data.retries["data_timer"] = 0
        return self._result([
            {"action": "SEND_DATA", "session_id": self.data.session_id, "seq": seq, "payload_id": payload_id},
            {"action": "START_TIMER", "timer": "data_timer"},
        ]) | {"code": "ok", "state": self.data.state, "snapshot": self.snapshot()}

    def step(self, event: dict[str, Any]) -> dict[str, Any]:
        """Apply one event and return a deterministic, JSON-safe result."""
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            return self._invalid("malformed_event") | {"code": "malformed_event", "state": self.data.state, "snapshot": self.snapshot()}
        before = deepcopy(self.data)
        result = self._handlers[self.data.state](event)
        if not result["valid"]:
            # R34: invalid input cannot leave a partial mutation behind.
            self.data = before
        result["code"] = "ok" if result["valid"] else result.pop("reason")
        result["state"] = self.data.state
        result["snapshot"] = self.snapshot()
        return result

    def _result(self, actions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        return {"valid": True, "actions": actions or []}

    def _invalid(self, reason: str) -> dict[str, Any]:
        return {"valid": False, "reason": reason, "actions": []}

    def _same_session(self, event: dict[str, Any]) -> bool:
        return event.get("session_id") == self.data.session_id

    def _clear_session(self) -> None:
        self.data = SessionState()

    def _abort(self, reason: str) -> dict[str, Any]:
        self.data.state = "ABORTED"
        return self._result([{"action": "ABORTED", "reason": reason}])

    def _idle(self, e: dict[str, Any]) -> dict[str, Any]:
        if e["type"] != "OPEN_REQ" or not self._positive_id(e.get("session_id")):
            return self._invalid("event_not_valid_in_idle")
        self.data.session_id = e["session_id"]
        self.data.state = "OPEN_SENT"
        self.data.retries["open_timer"] = 0
        return self._result([
            {"action": "SEND_OPEN_REQ", "session_id": self.data.session_id},
            {"action": "START_TIMER", "timer": "open_timer"},
        ])

    def _open_sent(self, e: dict[str, Any]) -> dict[str, Any]:
        if e["type"] == "ABORT":
            return self._abort(str(e.get("reason", "abort")))
        if e["type"] == "OPEN_ACK":
            if not self._same_session(e):
                return self._invalid("nonmatching_open_ack")
            self.data.state = "OPEN"
            self.data.retries["open_timer"] = 0
            return self._result([{"action": "STOP_TIMER", "timer": "open_timer"}])
        return self._timeout(e, "open_timer", "SEND_OPEN_REQ", None)

    def _open(self, e: dict[str, Any]) -> dict[str, Any]:
        kind = e["type"]
        if kind == "ABORT":
            return self._abort(str(e.get("reason", "abort")))
        if kind == "DATA":
            return self._data(e)
        if kind == "DATA_ACK":
            return self._data_ack(e)
        if kind == "CLOSE_REQ":
            if not self._same_session(e):
                return self._invalid("nonmatching_session")
            if self.data.outstanding is not None:
                return self._invalid("outstanding_data_ack")
            self.data.state = "CLOSE_SENT"
            self.data.retries["close_timer"] = 0
            return self._result([
                {"action": "SEND_CLOSE_REQ", "session_id": self.data.session_id},
                {"action": "START_TIMER", "timer": "close_timer"},
            ])
        return self._timeout(e, "data_timer", "RETRANSMIT_DATA", self.data.outstanding)

    def _close_sent(self, e: dict[str, Any]) -> dict[str, Any]:
        if e["type"] == "ABORT":
            return self._abort(str(e.get("reason", "abort")))
        if e["type"] == "CLOSE_ACK":
            if not self._same_session(e):
                return self._invalid("nonmatching_close_ack")
            self.data.state = "CLOSED"
            self.data.retries["close_timer"] = 0
            return self._result([{"action": "STOP_TIMER", "timer": "close_timer"}])
        return self._timeout(e, "close_timer", "SEND_CLOSE_REQ", None)

    def _closed(self, e: dict[str, Any]) -> dict[str, Any]:
        if e["type"] == "RESET":
            self._clear_session()
            return self._result([{"action": "RESET"}])
        if e["type"] == "CLOSE_ACK" and self._same_session(e):
            return self._result([{"action": "IGNORE_DUPLICATE_CLOSE_ACK"}])
        return self._invalid("event_not_valid_in_closed")

    def _aborted(self, e: dict[str, Any]) -> dict[str, Any]:
        if e["type"] != "RESET":
            return self._invalid("aborted_is_terminal")
        self._clear_session()
        return self._result([{"action": "RESET"}])

    def _data(self, e: dict[str, Any]) -> dict[str, Any]:
        if not self._same_session(e):
            return self._invalid("nonmatching_session")
        seq = e.get("seq")
        if not isinstance(seq, int) or seq < 0:
            return self._invalid("invalid_sequence")
        if e.get("direction") == "LOCAL":
            if self.data.outstanding is not None:
                return self._invalid("local_data_already_outstanding")
            if seq != self.data.next_tx_seq:
                return self._invalid("local_sequence_must_equal_next_send")
            self.data.next_tx_seq += 1
            self.data.outstanding = {"seq": seq, "payload_id": e.get("payload_id")}
            self.data.retries["data_timer"] = 0
            return self._result([
                {"action": "SEND_DATA", "session_id": self.data.session_id, "seq": seq, "payload_id": e.get("payload_id")},
                {"action": "START_TIMER", "timer": "data_timer"},
            ])
        if e.get("direction") != "PEER":
            return self._invalid("data_direction_must_be_LOCAL_or_PEER")
        if seq == self.data.expected_rx_seq:
            self.data.last_delivered_seq = seq
            self.data.expected_rx_seq += 1
            return self._result([
                {"action": "DELIVER_DATA", "seq": seq, "payload_id": e.get("payload_id")},
                {"action": "SEND_DATA_ACK", "seq": seq},
            ])
        if seq == self.data.expected_rx_seq - 1:
            return self._result([{"action": "SEND_DATA_ACK", "seq": seq}, {"action": "DUPLICATE_NOT_DELIVERED"}])
        # A2: only the immediately preceding sequence is specified as duplicate.
        return self._invalid("future_or_older_duplicate_data")

    def _data_ack(self, e: dict[str, Any]) -> dict[str, Any]:
        if not self._same_session(e):
            return self._invalid("nonmatching_session")
        seq = e.get("seq")
        if not isinstance(seq, int) or seq < 0:
            return self._invalid("invalid_sequence")
        if self.data.outstanding and seq == self.data.outstanding["seq"]:
            self.data.last_acked_seq = seq
            self.data.outstanding = None
            self.data.retries["data_timer"] = 0
            return self._result([{"action": "STOP_TIMER", "timer": "data_timer"}])
        if seq == self.data.last_acked_seq:
            return self._result([{"action": "IGNORE_DUPLICATE_DATA_ACK", "seq": seq}])
        return self._invalid("future_or_unexpected_data_ack")

    def _timeout(self, e: dict[str, Any], timer: str, action: str, item: dict[str, Any] | None) -> dict[str, Any]:
        if e["type"] != "TIMEOUT" or e.get("timer_name") != timer:
            return self._invalid("event_not_valid_in_state")
        if timer == "data_timer" and item is None:
            return self._invalid("no_outstanding_data")
        # A1: the third consecutive timeout itself aborts; it is not retransmitted.
        self.data.retries[timer] += 1
        if self.data.retries[timer] >= 3:
            return self._abort(f"{timer}_retry_exhausted")
        payload: dict[str, Any] = {"action": action, "session_id": self.data.session_id}
        if item is not None:
            payload.update(item)
        return self._result([payload, {"action": "RESTART_TIMER", "timer": timer}])

    @staticmethod
    def _positive_id(value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool) and value > 0


def initial() -> dict[str, Any]:
    """Return a fresh JSON-compatible R01 state for the trace runner API."""
    return Protocol().snapshot()


def step(state: dict[str, Any] | None, event: dict[str, Any]) -> dict[str, Any]:
    """Pure trace API: ``step(state, event) -> result`` with next state in snapshot."""
    try:
        machine = Protocol.from_snapshot(state)
    except ValueError as exc:
        return {"valid": False, "code": "invalid_state", "actions": [], "snapshot": initial(), "state": "IDLE", "detail": str(exc)}
    return machine.step(event)
