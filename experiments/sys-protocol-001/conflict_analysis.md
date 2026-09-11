# Specification ambiguity and conflict analysis

## Classification rule

- **AMBIGUITY:** the authoritative text permits materially different observable
  behavior and does not select one.
- **CONFLICT:** two authoritative requirements prescribe incompatible behavior
  for the same condition.
- **REDUNDANCY:** two requirements prescribe compatible overlapping behavior.
- **NO_ISSUE:** apparent tension resolves through scope, state, or an explicit
  exception.

## Findings

| Finding | Requirements | Classification | Evidence-grounded analysis | Operational disposition |
|---|---|---|---|---|
| A1 timeout boundary | R27–R32 | AMBIGUITY | R27/R29/R31 require retransmission on timeout; R28/R30/R32 say “After three consecutive … timeouts” but do not specify whether the third event retransmits then aborts, or aborts immediately. | Interpretation A1: abort on the third timeout. |
| A2 older duplicate DATA | R14–R16 | AMBIGUITY | R15 covers exactly the most recently delivered sequence. It does not state behavior for `seq < expected_seq - 1`. R16 names future/out-of-order data but is not explicit about older duplicates. | Interpretation A2: invalid; no ACK, delivery, or receive advance. |
| C1 terminal ABORTED vs invalid-event rule | R23, R24, R26, R34 | NO_ISSUE | R23 explicitly makes RESET the exception to terminal behavior. R24 defines RESET from ABORTED as valid. R34 applies only to events not valid in their current state, so it governs all non-RESET events in ABORTED. | Model RESET in ABORTED as valid; return explicit invalid/no mutation for other events. |
| C2 close while inbound DATA acknowledgment might be pending | R18–R20 | NO_ISSUE | R19 restricts close on a **locally transmitted** item awaiting `DATA_ACK`. No requirement defines an inbound outstanding/ack-pending variable, and R14/R15 make inbound delivery/duplicate handling immediate. | Do not add an inbound-pending-close constraint. |

## Redundancies noted

- R18 and R19 are compatible cumulative guards for valid local `CLOSE_REQ`; R20
  supplies their effect. This is intentional guard-and-effect decomposition,
  not a conflict.
- R23/R24/R26 and R34 jointly specify RESET validity and invalid-event handling
  across states. They overlap but remain compatible.

## Frozen decision boundary

No finding above authorizes a rewrite of R01–R36. A1/A2 are registered
interpretations. C1/C2 are classified `NO_ISSUE`; neither is an active
conflict. Future changes require a new requirement version and SHA-256.
