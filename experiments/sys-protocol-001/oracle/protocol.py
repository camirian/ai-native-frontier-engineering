"""Public oracle adapter: JSON state in, event result and JSON state out.

The adapter deliberately exposes a small functional shape suitable for an
external conformance harness.  The behavioral model remains in `reference.py`.
"""
from __future__ import annotations

from typing import Any
from reference import Model, step as reference_step


def initial() -> dict[str, Any]:
    """Return a fresh serializable oracle state."""
    return Model().snapshot()


def step(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    """Interpret one event without relying on any candidate implementation.

    Result shape is intentionally stable for the integration harness:
    `{valid, code, actions, snapshot}`.  `IGNORED` is valid and has no state
    transition; `INVALID` is not valid and is mutation-free.
    """
    model = Model(**state)
    result = reference_step(model, event)
    code = result["result"]
    action = result["detail"].get("action")
    return {
        "valid": code != "INVALID",
        "code": code,
        "actions": [] if action is None else [action],
        "snapshot": result["snapshot"],
    }
