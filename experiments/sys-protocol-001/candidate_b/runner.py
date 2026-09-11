"""JSON-lines runner: one event object per input line, one result per output line."""
from __future__ import annotations

import json
import sys

try:  # Supports both `python candidate_b/runner.py` and package import.
    from .protocol import initial, step
except ImportError:
    from protocol import initial, step


def main() -> int:
    for line in sys.stdin:
        try:
            value = json.loads(line)
            if isinstance(value, dict) and isinstance(value.get("events"), list):
                state = initial()
                results = []
                for event in value["events"]:
                    result = step(state, event)
                    state = result["snapshot"]
                    results.append(result)
                result = {"name": value.get("name"), "results": results, "snapshot": state}
            else:
                # A single event line is evaluated from its supplied state, or R01.
                result = step(value.get("state") if isinstance(value, dict) else None, value.get("event", value) if isinstance(value, dict) else value)
        except json.JSONDecodeError:
            result = {"valid": False, "code": "invalid_json", "actions": [], "state": "IDLE", "snapshot": initial()}
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
