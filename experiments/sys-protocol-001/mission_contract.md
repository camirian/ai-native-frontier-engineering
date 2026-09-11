# Mission contract — MISSION-SYS-PROTOCOL-001

## Authority and boundary

**Mission:** Requirements-to-Executable Protocol Synthesis Under Held-Out Traces  
**Authorization:** `GATE_1_AUTHORIZED`  
**Type:** clean-room executable systems-engineering experiment

The frozen source is the owner-provided mission text at
`mission brief supplied to the execution environment`.
Requirements R01–R36 in `requirements.yaml` preserve that text exactly in
`original_text`. The YAML normalization is an implementation-facing restatement,
not an amendment. Its SHA-256 is recorded in `requirements_hash.txt` before
implementation work.

## In scope

- A self-authored, generic bidirectional protocol model with states `IDLE`,
  `OPEN_SENT`, `OPEN`, `CLOSE_SENT`, `CLOSED`, and `ABORTED`.
- Positive and negative behavioral conformance under the frozen requirements.
- Traceability, independent-oracle evidence, mutation testing, held-out traces,
  and bounded requirement-change impact analysis.

## Non-negotiable controls

- Do not silently modify, repair, or reinterpret frozen requirements after the
  freeze. Log all interpretations in `interpretation_register.md`.
- Keep candidate implementations structurally separate from the oracle; the
  oracle must not import, call, or copy candidate behavior after candidate
  architecture freezes.
- Freeze design and held-out trace hashes before their respective evaluation
  boundaries. Candidate implementers may not inspect held-out traces.
- Do not publish, contact external parties, create a GitHub repository, modify
  `_project_triage`, modify Strategy Vault, or execute a follow-on gate.

## Lane-A/F evidence role

This lane owns requirements normalization, interpretation/conflict records, the
requirements hash, and initial traceability rows. It does not implement a
protocol, oracle, trace suite, mutant, candidate, or result claim.

## Current gate posture

Requirements are frozen only once `requirements_hash.txt` has been generated.
No scientific result or Gate PASS/ PARTIAL / STOP decision is asserted by this
artifact.
