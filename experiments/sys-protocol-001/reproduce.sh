#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c requirements_hash.txt
sha256sum -c held_out_hashes.txt
python3 -m py_compile candidate_a/*.py candidate_b/*.py candidate_c/*.py oracle/*.py mutants/*.py scripts/conformance.py
python3 scripts/conformance.py
