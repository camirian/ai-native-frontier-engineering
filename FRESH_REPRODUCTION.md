# Fresh public-package reproduction

Status: PASS on 2026-09-11.

The release check created a temporary copy of this package, created a virtual environment, installed only `requirements.txt`, verified `CHECKSUMS.sha256` before generated outputs changed, then ran both experiment scripts, the transparent timing sampler, and SVG renderer. The complete captured output is in `FRESH_REPRODUCTION.log`.

The results reproduced the five packaged numerical cases, the eight adverse Jacobi failures, the G06 `H_edge_down` stress ratio of `12.5`, and all deterministic SVG outputs. This proves package reproducibility, not historical held-out secrecy or benchmark validity.
