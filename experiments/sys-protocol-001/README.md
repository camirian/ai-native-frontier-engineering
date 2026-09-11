# SYS-PROTOCOL-001

Bounded clean-room experiment: requirements → three executable session-protocol implementations → independent oracle → mutation testing → held-out conformance → traceability.

Run from this directory with `./reproduce.sh`. The run validates the frozen requirements hash and 25 held-out trace hashes, executes all three candidates, and checks 12/12 deliberate mutants. The result is bounded to this self-authored protocol and is not production correctness, standards compliance, formal verification, or a claim that AI replaces systems engineers.

The original execution record and public reproduction record are distinct. See `gate1_report.md`, `claim_boundary.md`, `variant_impact_analysis.md`, and `owner_learning_return.md`.
