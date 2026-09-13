# AI-Native Frontier Engineering

Reproducible clean-room experiments that test what an AI-amplified engineer can generate, falsify, and verify across engineering domains.

The central observation is deliberately narrow: AI makes generation cheaper, so specification quality, independent oracles, held-out evaluation, authority resolution, and claim boundaries become more important. Evidence now spans three bounded clean-room engineering domains plus two cross-cutting case studies. This does not establish a universal law.

## Research spine

- [`Engineering compression`](research/engineering-compression/): a bounded multidisciplinary execution experiment with independent evaluation and preserved negative evidence.
- [`Authority precedence`](research/authority-precedence/): why correct execution can still produce the wrong outcome when local instructions are stale.

## Experiments

| Experiment | Apparent design-set result | Independent check | Disposition |
| --- | --- | --- | --- |
| [`num-synth-001`](experiments/num-synth-001/) | Historical exploratory run recorded a large PCG/CG timing difference | Public reproduction checks five recorded cases; an over-relaxed Jacobi control fails 8/8 design cases | No robust performance claim |
| [`gen-design-001`](experiments/gen-design-001/) | G06 was 25.27% lighter than B2_warren on the recorded design envelope | Public reproduction checks a 12.5 stress ratio for G06 under an edge load | No robust superiority |
| [`sys-protocol-001`](experiments/sys-protocol-001/) | Three executable implementations of a self-authored session protocol | Independent oracle; 12/12 mutation kills; 25 held-out traces; 36/36 traceability | Bounded Gate PASS; not production protocol correctness |

None of these experiments describes a real bridge, building, deployed solver, production protocol, or production recommendation. All are synthetic, normalized, and bounded.

## Method

1. Freeze a problem specification and design envelope.
2. Generate candidates using separated specialist roles.
3. Evaluate with a separate deterministic oracle implementation.
4. Record the process used before opening held-out tests.
5. Preserve failures and state only claims supported by the evidence.

Read [the methodology](methodology/CLEAN_ROOM_METHOD.md), [the claim table](PUBLIC_CLAIMS.md), and the per-experiment reproduction notes before reusing results.

The common thread is simple: cheaper generation increases the value of specification, authority precedence, independent evaluation, and disciplined claims.

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
