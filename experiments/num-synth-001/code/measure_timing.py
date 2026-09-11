#!/usr/bin/env python3
"""Record a transparent, non-benchmark timing sample for the public package."""
import csv
import importlib.util
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_experiment", HERE / "code" / "run_experiment.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
CASE = (64, "smooth", "mixed")
WARMUPS, REPEATS = 1, 5


def run(label, precondition):
    problem = module.problem(*CASE)
    for _ in range(WARMUPS):
        module.cg(problem, precondition)
    rows = []
    for repeat in range(1, REPEATS + 1):
        start = time.perf_counter_ns()
        result = module.cg(problem, precondition)
        rows.append({"solver": label, "repeat": repeat, "seconds": (time.perf_counter_ns() - start) / 1_000_000_000, "iterations": result["iterations"], "relative_residual": result["relative_residual"]})
    return rows


def main():
    evidence = HERE / "evidence"
    evidence.mkdir(exist_ok=True)
    rows = run("CG", False) + run("diagonal_PCG", True)
    with (evidence / "timing_raw.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    environment = {"python_version": sys.version, "numpy_version": np.__version__, "platform": platform.platform(), "architecture": platform.machine(), "case": CASE, "warmups_per_solver": WARMUPS, "repeats_per_solver": REPEATS, "clock": "time.perf_counter_ns"}
    (evidence / "timing_environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    print(json.dumps(environment, indent=2))


if __name__ == "__main__":
    main()
