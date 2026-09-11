# Interpretation register

Frozen requirements remain in `requirements.yaml`. This register records the
working interpretations supplied to downstream lanes; it does not change them.

| ID | Related requirements | Classification | Decision | Rationale | Falsifier / routing trigger |
|---|---|---|---|---|---|
| A1 | R27–R32, R33 | AMBIGUITY | **Use “abort on the third timeout.”** The first and second timeouts retransmit; the third transitions immediately to `ABORTED` (no fourth timeout). | “After three consecutive … timeouts” most directly sets the threshold at the third observed timeout. This is a chosen operational interpretation, not a textual correction. | Owner direction selecting “three retries plus one additional timeout,” or an authoritative requirement amendment, requires a new freeze/version and re-execution of affected traces. |
| A2 | R14–R16 | AMBIGUITY | **Older duplicate (`seq < expected_seq - 1`) is invalid, with no acknowledgment, delivery, or receive-sequence advance.** Only `seq = expected_seq - 1` receives R15 duplicate handling. | R15 expressly mandates treatment only for the most recently delivered sequence. The requirements do not mandate acknowledgment of an older duplicate; extending R15 would silently generalize it. | Owner direction to acknowledge all prior duplicates requires a new freeze/version and updates to R15/R16 coverage. |
| C1 | R23, R24, R26, R34 | NO_ISSUE (apparent tension rejected) | RESET is valid in `ABORTED`; it transitions to `IDLE` and clears state. Other events in `ABORTED` are invalid and non-mutating. | R23’s explicit exception supplies the validity condition; R34 only governs events that are not valid in the current state. | A requirement asserting RESET itself is invalid in `ABORTED` would create an actual conflict with R24. |
| C2 | R18–R20 | NO_ISSUE (apparent tension rejected) | A received-but-unacknowledged inbound DATA item does **not** constrain local CLOSE_REQ. Only `tx_outstanding` (locally transmitted DATA awaiting `DATA_ACK`) is relevant. | R19 scopes its condition to “transmitted DATA acknowledgment,” while R14/R15 govern received DATA. No inbound pending-ack state is specified. | Owner adds an inbound-delivery acknowledgment state/requirement or states that an inbound item blocks close. |

## Routing record

- Human routing events required by this lane: **0**. A1 and A2 have explicit
  working decisions so implementation can proceed without silent choice.
- Any change to an `original_text` value is a new requirement version, not an
  edit to this register. Downstream results must identify which hash they used.
