# Provenance and evidence limits

This repository distinguishes records created during the original clean-room missions from public reproductions run after package assembly. Neither mission has a signed precommitment, remote timestamp, independent evaluator artifact, or Git history that can cryptographically prove candidates were hidden from held-out cases.

## Held-out provenance

`HELD_OUT_PROVENANCE = MIXED`: NUM-SYNTH and GEN-DESIGN remain process-recorded and not cryptographically proven; SYS-PROTOCOL includes a reproducible held-out hash manifest, but this public package still cannot prove historical sequestration retrospectively.

The original scripts and local file ordering record a procedure in which manifests/candidate hashes were written before held-out evaluations. Because held-out cases were plaintext in the same scripts and records lack an immutable commitment, this is a process record, not independent proof of sequestration.

## Original execution evidence

The unmodified source records are packaged under each experiment’s `evidence/original_execution/` directory. Their file hashes, observed local timestamps, and known limitations appear in the companion `experiment_manifest.json` files.

## Public reproduction evidence

The public scripts deterministically reproduce the packaged solver-validity and synthetic truss calculations. They do not recreate historical agent routing, candidate generation, timing conditions, or held-out secrecy.

SYS-PROTOCOL public reproduction runs the three packaged candidates against the independent oracle, validates 25 held-out trace hashes, checks 12 mutation kills, and verifies the 36-row traceability matrix. This is a public reproduction record distinct from the original execution record.

## Asset authorship

See `THIRD_PARTY.md`. The package contains owner-authored clean-room code/data and generated SVGs only; no third-party source/assets are redistributed.
