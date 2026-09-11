# Candidate B: event-dispatch state handlers

Candidate B is a deterministic, in-memory endpoint model. The standard importable
trace API is `initial()` and `step(state, event) -> {valid, code, actions,
snapshot}`; `python candidate_b/runner.py` accepts either one event object per
line or a trace object with `name` and `events`, and writes JSON lines. Each event
result includes the post-event state and a complete JSON-safe snapshot. Invalid
results roll back to the pre-event snapshot.

## Architecture

`Protocol` dispatches each event to a handler selected by the current state:
`_idle`, `_open_sent`, `_open`, `_close_sent`, `_closed`, or `_aborted`. Those
handlers use focused helpers for DATA receive, DATA_ACK, and timeout behavior.
State is held in `SessionState`, including session identity, transmit/receive
sequence numbers, the sole outstanding transmit item, acknowledgement history,
and retry counters. Actions model sends, timer control, delivery, and terminal
outcomes; the runner never performs network I/O.

Locally transmitted DATA is represented by an outstanding item. This minimal
event vocabulary has no separate transmit-DATA event, so tests/integrators may
set an outstanding item through their harness when exercising DATA_ACK/DATA
timeout rules. Receive-DATA behavior is fully event-driven.

## Frozen interpretation decisions

- **A1 — third timeout abort:** the third consecutive matching timeout performs
  the transition to `ABORTED` immediately. It does not emit an additional
  retransmission action. A matching acknowledgement resets its matching counter.
- **A2 — older duplicate:** only `expected_rx_seq - 1` is the specified exact
  duplicate and is acknowledged without delivery. An older sequence is invalid;
  it is not generalized into a duplicate acknowledgement rule.
- **C2 — inbound DATA and close:** a received but unacknowledged inbound item
  does not block local close. The model acknowledges each valid inbound DATA in
  the same event, and R19 constrains only a locally transmitted outstanding DATA
  acknowledgement.

`RESET` is accepted only in `CLOSED` and `ABORTED`, clears all session fields,
and therefore resolves the R23/R34 tension without treating RESET as invalid in
the states explicitly authorized by R24–R25.
