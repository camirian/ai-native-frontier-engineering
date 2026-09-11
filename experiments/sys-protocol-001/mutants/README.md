# Semantic mutation targets

`mutants.py` contains twelve named, executable semantic defects layered over
Candidate B. Use `build_mutant("M01")` to obtain a fresh endpoint with the
named defect. `mutation_manifest.yaml` binds every defect to its intended
requirements, including A1 and A2 where applicable.

These are deliberately not tests and do not inspect the independent oracle or
held-out traces. A separate test/oracle lane should execute the same frozen
design traces against each implementation, record the first divergence, and
mark any survivor with a documented coverage gap.
