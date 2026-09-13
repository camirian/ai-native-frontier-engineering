# The AI Did the Wrong Task Correctly

This note records a transferable failure mode in agentic execution: a capable system can follow a locally valid instruction correctly after newer authority has made that instruction stale.

```text
LOCAL INSTRUCTION → CORRECT EXECUTION → STALE AUTHORITY → WRONG OUTCOME
```

The repaired path is:

```text
CURRENT AUTHORITY → PRECEDENCE RESOLUTION → TASK SELECTION → EXECUTION
```

## What happened

The original cycle selected a synthesis task from stale local state even though newer authority had already recorded that synthesis as complete and authorized one fresh bounded evaluation instead. The execution was locally coherent. The objective was wrong.

The failure was therefore not primarily a coding failure. It was an authority-resolution failure: the system treated a historical local instruction as current because it was available in the working context.

## What was repaired

The follow-up record made authority sources, dates, superseded actions, freshness conflicts, owner gates, and fixed precedence explicit. It selected one fresh externally grounded task, froze acceptance before execution, and separated candidate-local claims from independent evaluation. The bounded follow-up reached `PARTIAL`: its hidden behavioral checks passed, but native candidate-suite collection and static/type gates were unavailable in that reconstructed environment.

## Finding and limits

Execution correctness is not objective correctness when authority can change. A reliable agent workflow must resolve current authority before task selection and preserve the conflict for review.

This is a bounded process finding, not a commercial product, orchestration framework, universal reliability guarantee, or claim about all agent systems. The original stale-authority miss remains part of the evidence; it is not rewritten as success.

## Public boundary

Private repository names, employer environments, customer information, credentials, and unrelated internal terminology are intentionally omitted. The note preserves the failure pattern, repair concept, follow-up evidence, and limitations without exposing those details.
