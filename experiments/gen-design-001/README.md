# GEN-DESIGN-001: synthetic truss design under held-out loads

This experiment searches and sizes members in a fixed 2-D synthetic normalized lattice. It is not a bridge or building design.

`code/run_experiment.py` implements a deterministic axial-bar finite-element calculation and rechecks recorded held-out cases for the two figure-relevant candidate bytes. The original process record is packaged separately; it does not cryptographically prove held-out secrecy or independent evaluator separation.

Run `python3 code/run_experiment.py` from this directory. It writes a fresh `reproduced/` directory without changing the frozen data.

Result: G06 was lighter on the design envelope, but every finalist and baseline failed a held-out requirement. The held-out failure is the principal result.
