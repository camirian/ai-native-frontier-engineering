# Gate 1 report — MISSION-SYS-PROTOCOL-001

## Evidence summary

- Requirements freeze: `requirements.yaml` SHA-256 `ce7c7df883b3ccc0a094af10c988833bf9fa5947e8dfd92832cde3fcc8cdf043`; verified by `reproduce.sh`.
- Interpretation routing: A1 and A2 are logged in `interpretation_register.md`; C1 and C2 are classified `NO_ISSUE` in `conflict_analysis.md`.
- Candidates: A (guarded transition table), B (event-dispatch state handlers), and C (declarative rules).
- Independence: `oracle/reference.py` was authored in a separate lane before candidate integration and imports no candidate module. It is documented in `oracle/README.md`.
- Traces: 17 design traces plus 3 mutation probes, and 25 separately frozen held-out traces. `held_out_hashes.txt` validates all held-out files.
- Conformance: `results/conformance.json` records zero mismatches for all three candidates across the combined corpus.
- Mutation: `mutation_results.csv` records 12 of 12 deliberate semantic mutants killed. The harness compares validity, normalized state, and delivery observability.
- Traceability: `traceability.csv` has 36 populated requirement rows.
- Variants: `variant_impact_analysis.md` identifies impact and prevents an under-specified silent implementation of V1/V2.

## Decision

`SCIENTIFIC_RESULT = EXECUTABLE_SE_SYNTHESIS_SUPPORTED`

`GATE_1_DECISION = PASS`

`ORG_OF_ONE = PARTIALLY_SUPPORTED`

The result supports the bounded claim only. It is not evidence of production protocol correctness or formal verification. The best next action is `PRESERVE_AND_WATCH`; do not execute a follow-on gate under this mission.
