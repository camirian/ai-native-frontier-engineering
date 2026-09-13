# Distribution copy — authority precedence

## LinkedIn

The AI did the wrong task correctly.

The system followed a locally valid instruction, produced coherent work, and still missed the objective because newer authority had superseded that instruction.

That failure is easy to misclassify as “the model made a mistake.” The deeper issue was precedence resolution:

`LOCAL INSTRUCTION → CORRECT EXECUTION → STALE AUTHORITY → WRONG OUTCOME`

The repair was to resolve current authority before task selection, record freshness conflicts and superseded actions, freeze acceptance before execution, and keep independent evaluation separate from candidate work.

Execution correctness is not objective correctness when authority changes. This is a bounded process finding, not a product claim or universal reliability guarantee.

Read the note: https://github.com/camirian/ai-native-frontier-engineering/tree/main/research/authority-precedence

## X

1/ The AI did the wrong task correctly.

2/ It followed a locally valid instruction and produced coherent work. Newer authority had already superseded that instruction, so the outcome was still wrong.

3/ The repair: resolve current authority before task selection; record freshness conflicts and superseded actions; freeze acceptance before execution; keep independent evaluation separate.

4/ Execution correctness is not objective correctness when authority changes.

https://github.com/camirian/ai-native-frontier-engineering/tree/main/research/authority-precedence
