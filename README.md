# AI-Native Frontier Engineering

Reproducible clean-room experiments that test what an AI-amplified engineer can generate, falsify, and verify across engineering domains.

The central observation is deliberately narrow: when candidate generation and implementation become cheap, specification quality, independent oracles, held-out evaluation, and claim boundaries become dominant engineering work. This is **partially validated across two clean-room domains**, not established as a universal law.

## Experiments

| Experiment | Apparent design-set result | Independent check | Disposition |
| --- | --- | --- | --- |
| [`num-synth-001`](experiments/num-synth-001/) | Historical exploratory run recorded a large PCG/CG timing difference | Public reproduction checks five recorded cases; an over-relaxed Jacobi control fails 8/8 design cases | No robust performance claim |
| [`gen-design-001`](experiments/gen-design-001/) | G06 was 25.27% lighter than B2_warren on the recorded design envelope | Public reproduction checks a 12.5 stress ratio for G06 under an edge load | No robust superiority |

Neither experiment describes a real bridge, building, deployed solver, or production recommendation. Both are synthetic, normalized, and bounded.

## Method

1. Freeze a problem specification and design envelope.
2. Generate candidates using separated specialist roles.
3. Evaluate with a separate deterministic oracle implementation.
4. Record the process used before opening held-out tests.
5. Preserve failures and state only claims supported by the evidence.

Read [the methodology](methodology/CLEAN_ROOM_METHOD.md), [the claim table](PUBLIC_CLAIMS.md), and the per-experiment reproduction notes before reusing results.

## Reproduce

This package is dependency-light: Python 3.12.3 and NumPy 1.26.4 are recorded for the release environment. The supplied scripts regenerate the synthetic results and deterministic SVG figures.

```bash
python3 -m pip install -r requirements.txt
python3 experiments/num-synth-001/code/run_experiment.py
python3 experiments/gen-design-001/code/run_experiment.py
python3 scripts/render_figures.py
```

Read [`PROVENANCE.md`](PROVENANCE.md), [`PUBLIC_CLAIMS.md`](PUBLIC_CLAIMS.md), and [`FRESH_REPRODUCTION.md`](FRESH_REPRODUCTION.md) before reusing results.

## Status

This package distinguishes original execution records from later public reproduction. Original held-out process records are not cryptographic proof of secrecy or independence.
