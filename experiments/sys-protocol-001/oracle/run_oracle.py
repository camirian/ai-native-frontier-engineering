#!/usr/bin/env python3
"""Run the clean-room reference oracle over one JSON trace or a directory."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from reference import run


def evaluate(path: Path) -> bool:
    trace = json.loads(path.read_text())
    actual = run(trace["events"])
    expected = trace.get("oracle_expectations", [])
    compact = [{"result": r["result"], "state": r["state"], "action": r["detail"].get("action")}
               for r in actual]
    ok = not expected or compact == expected
    print(json.dumps({"trace": path.name, "pass": ok, "actual": compact}, sort_keys=True))
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    paths = sorted(args.path.glob("*.json")) if args.path.is_dir() else [args.path]
    return 0 if all(evaluate(path) for path in paths) else 1


if __name__ == "__main__":
    raise SystemExit(main())
