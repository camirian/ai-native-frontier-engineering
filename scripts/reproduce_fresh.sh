#!/usr/bin/env bash
set -euo pipefail
source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
cp -a "$source_dir" "$scratch/package"
cd "$scratch/package"
sha256sum -c CHECKSUMS.sha256
python3 -m venv "$scratch/venv"
"$scratch/venv/bin/python" -m pip install --disable-pip-version-check -r requirements.txt
"$scratch/venv/bin/python" experiments/num-synth-001/code/run_experiment.py
"$scratch/venv/bin/python" experiments/num-synth-001/code/measure_timing.py
"$scratch/venv/bin/python" experiments/gen-design-001/code/run_experiment.py
"$scratch/venv/bin/python" scripts/render_figures.py
if command -v rg >/dev/null && rg -n '/home/|github.com|BEGIN (RSA|OPENSSH) PRIVATE KEY|AKIA[0-9A-Z]{16}' --glob '!scripts/reproduce_fresh.sh' .; then
  echo 'sanitization scan found a forbidden pattern' >&2; exit 1
fi
find media -name '*.svg' -type f -print
echo "Fresh disposable reproduction passed: $scratch/package"
