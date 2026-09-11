# Results ledger

## NUM-SYNTH-001

- Synthetic flux-form 2-D elliptic family; manufactured discrete right-hand side supplies the exact discrete oracle.
- The original process record lists eight design combinations and five held-out combinations. It does not cryptographically prove that the held-out set was unseen.
- Baselines: weighted Jacobi, red-black colored relaxation, and CG. Candidates: diagonal-PCG and warm-started CG.
- Historical aggregate records report 25 valid rows; public reproduction checks five cases × two solvers.
- Historical timing aggregates include diagonal-PCG `0.000167 s` and CG `0.002447 s`; this comparison is archival only, not a public benchmark claim.
- Deliberately over-relaxed weighted-Jacobi control failed `8/8` design cases.
- Boundary: timing is not a robust benchmark. SciPy was unavailable; timings are small; no 256x256 workload or independent repeated process run was recorded.

## GEN-DESIGN-001

- Synthetic normalized planar truss with a finite-element axial-bar oracle.
- Twelve generated topology families and two conventional baselines were design-evaluated.
- `B2_warren` design mass: `6.069109`; `G06` design mass: `4.535164`; apparent design-envelope reduction: `25.27%`.
- The original process record writes finalist hashes before held-out evaluation, but has no immutable precommitment and does not prove evaluator independence.
- Every baseline and finalist violated at least one held-out stress constraint. `G06` reached stress utilization `12.5` under `H_edge_down`.
- Equilibrium residuals remained near numerical precision. The conclusion is envelope brittleness, not solver failure.
- Boundary: no robust mass superiority was established.
