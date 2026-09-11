# NUM-SYNTH-001: elliptic solver synthesis under distribution shift

A synthetic flux-form 2-D elliptic family uses a manufactured discrete right-hand side, so the exact discrete solution supplies a deterministic correctness check. The original process record names five held-out instances, but does not cryptographically prove they were hidden.

`code/run_experiment.py` contains the operator, solvers, validity checks, held-out cases, and adversarial over-relaxed Jacobi control. It writes a fresh `reproduced/` directory.

Historical aggregate timing records are packaged for transparency. Their approximately 14.6x diagonal-PCG/CG ratio is archival and exploratory only; it is not a public benchmark headline.
