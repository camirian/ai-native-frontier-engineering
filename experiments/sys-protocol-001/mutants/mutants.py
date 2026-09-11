"""Named semantic defects for Candidate B mutation testing.

Each mutant subclasses Candidate B and changes one protocol rule.  This module
is intentionally a mutation target, not an oracle or test suite.
"""
from __future__ import annotations

from typing import Any

from candidate_b.protocol import Protocol


class M01AcceptWrongSessionOpenAck(Protocol):
    def _open_sent(self, e: dict[str, Any]) -> dict[str, Any]:
        if e.get("type") == "OPEN_ACK":
            e = {**e, "session_id": self.data.session_id}
        return super()._open_sent(e)


class M02DoubleDeliverDuplicateData(Protocol):
    def _data(self, e: dict[str, Any]) -> dict[str, Any]:
        if e.get("seq") == self.data.expected_rx_seq - 1:
            self.data.expected_rx_seq = e["seq"]
        return super()._data(e)


class M03AcceptFutureData(Protocol):
    def _data(self, e: dict[str, Any]) -> dict[str, Any]:
        if isinstance(e.get("seq"), int) and e["seq"] > self.data.expected_rx_seq:
            self.data.expected_rx_seq = e["seq"]
        return super()._data(e)


class M04AllowCloseWithOutstanding(Protocol):
    def _open(self, e: dict[str, Any]) -> dict[str, Any]:
        if e.get("type") == "CLOSE_REQ":
            self.data.outstanding = None
        return super()._open(e)


class M05DoNotResetRetryOnAck(Protocol):
    def _open_sent(self, e: dict[str, Any]) -> dict[str, Any]:
        old = self.data.retries["open_timer"]
        result = super()._open_sent(e)
        if e.get("type") == "OPEN_ACK" and result["valid"]:
            self.data.retries["open_timer"] = old
        return result


class M06AbortOnFourthTimeout(Protocol):
    def _timeout(self, e: dict[str, Any], timer: str, action: str, item: dict[str, Any] | None) -> dict[str, Any]:
        if e.get("type") == "TIMEOUT" and e.get("timer_name") == timer and self.data.retries[timer] == 2:
            self.data.retries[timer] = 1
        return super()._timeout(e, timer, action, item)


class M07ResetFromOpen(Protocol):
    def _open(self, e: dict[str, Any]) -> dict[str, Any]:
        if e.get("type") == "RESET":
            self._clear_session()
            return self._result([{"action": "RESET"}])
        return super()._open(e)


class M08LeakSequenceAcrossReset(Protocol):
    def _clear_session(self) -> None:
        next_tx, expected_rx = self.data.next_tx_seq, self.data.expected_rx_seq
        super()._clear_session()
        self.data.next_tx_seq, self.data.expected_rx_seq = next_tx, expected_rx


class M09ReopenOnDuplicateCloseAck(Protocol):
    def _closed(self, e: dict[str, Any]) -> dict[str, Any]:
        if e.get("type") == "CLOSE_ACK" and self._same_session(e):
            self.data.state = "OPEN"
            return self._result([{"action": "REOPENED"}])
        return super()._closed(e)


class M10AcceptFutureDataAck(Protocol):
    def _data_ack(self, e: dict[str, Any]) -> dict[str, Any]:
        if self.data.outstanding and isinstance(e.get("seq"), int) and e["seq"] > self.data.outstanding["seq"]:
            e = {**e, "seq": self.data.outstanding["seq"]}
        return super()._data_ack(e)


class M11AcknowledgeOlderDuplicate(Protocol):
    def _data(self, e: dict[str, Any]) -> dict[str, Any]:
        if isinstance(e.get("seq"), int) and e["seq"] < self.data.expected_rx_seq - 1:
            return self._result([{"action": "SEND_DATA_ACK", "seq": e["seq"]}, {"action": "OLD_DUPLICATE_ACCEPTED"}])
        return super()._data(e)


class M12AllowDataOutsideOpen(Protocol):
    def _open_sent(self, e: dict[str, Any]) -> dict[str, Any]:
        if e.get("type") == "DATA":
            return self._data(e)
        return super()._open_sent(e)


MUTANTS: dict[str, type[Protocol]] = {
    "M01": M01AcceptWrongSessionOpenAck,
    "M02": M02DoubleDeliverDuplicateData,
    "M03": M03AcceptFutureData,
    "M04": M04AllowCloseWithOutstanding,
    "M05": M05DoNotResetRetryOnAck,
    "M06": M06AbortOnFourthTimeout,
    "M07": M07ResetFromOpen,
    "M08": M08LeakSequenceAcrossReset,
    "M09": M09ReopenOnDuplicateCloseAck,
    "M10": M10AcceptFutureDataAck,
    "M11": M11AcknowledgeOlderDuplicate,
    "M12": M12AllowDataOutsideOpen,
}


def build_mutant(name: str) -> Protocol:
    """Return a fresh named mutant; raises KeyError for an unknown identifier."""
    return MUTANTS[name]()
