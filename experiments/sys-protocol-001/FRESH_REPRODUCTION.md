# Fresh reproduction record

Run `./reproduce.sh` from this directory in a disposable copy. The verified run on 2026-09-11 validated the requirements and held-out SHA-256 manifests, compiled all three candidates and the independent oracle, and reported:

```text
candidate_failures: candidate_a=0, candidate_b=0, candidate_c=0
mutants_killed: 12/12
held_out_traces: 25
traceability_rows: 36
```

This is a public reproduction record. It does not recreate the original agent routing, historical wall-clock conditions, or retrospective proof that held-out traces were secret during candidate generation.
