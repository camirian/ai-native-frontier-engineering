# Held-out requirement variant impact analysis

## V1 — transmit window of two outstanding DATA items

Status: **impact analyzed; not implemented**. The one-line change is not an executable requirement set without a routing decision for ACK order, timeout ownership, and duplicate-ACK identity.

| Area | Impact |
|---|---|
| Affected requirements | R07–R12, R19, R29–R30, R33, R36 |
| State variables | Replace `outstanding` with an ordered window; add per-item retry state or a specified shared timer; retain a history sufficient to classify duplicate ACKs. |
| Transitions | LOCAL DATA admits when window length is below 2; DATA_ACK removes the specified in-window item; timeout identifies exactly one unacknowledged item. |
| Tests | Add two sends before ACK, in-order and reverse-order ACK tests, one/two outstanding close rejection, independent timeout/retry tests, and post-reset empty-window tests. |
| Implementation changes | Candidate A table gets window guards and item-indexed timer effects; B handlers replace the scalar slot; C rule facts change cardinality and ACK predicates; oracle model mirrors the selected policy. |

Open interpretation: the base requirements define one outstanding item and a singular `DATA timeout`. They do not say whether two outstanding items may be acknowledged out of order or how timers are named. Implementing V1 would require an additional interpretation register entry, so no candidate was silently extended.

## V2 — automatic CLOSED cleanup event

Status: **impact analyzed; not implemented**. It adds a deterministic cleanup event absent from the frozen event alphabet.

| Area | Impact |
|---|---|
| Affected requirements | R01–R03, R24–R26, R35–R36 |
| State variables | Session-clear operation and a cleanup-pending marker only if cleanup is asynchronous. |
| Transitions | Add `CLEANUP` from CLOSED to IDLE; decide ordering against duplicate CLOSE_ACK. |
| Tests | Deterministic cleanup, duplicate CLOSE_ACK before/after cleanup, stale old-session events, and next-session isolation. |
| Implementation changes | Add one rule/handler/table row in every candidate and oracle; retain RESET from ABORTED. |

V2 is also under-specified: the event name, trigger point, and its order relative to a duplicate CLOSE_ACK are not supplied.
