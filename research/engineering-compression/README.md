# Engineering compression: bounded case study

This note records a bounded clean-room engineering experiment in which AI-assisted execution represented several conventional engineering roles: problem and interface definition, plant/control design, simulation, fault semantics, safety validation, and independent verification. The roles are represented in the architecture and evaluation records; this is not evidence that a complete engineering organization was replaced.

## What was tested

The experiment built a deterministic two-zone thermal-control simulation with delayed observations, actuator dynamics, fault handling, a controller contract, and a machine-readable safety/command oracle. An independent evaluator generated 30 unseen boundary and intermediate cases across ambient conditions, capacitance, coupling, passive loss, authority, lag, actuator effectiveness, delay, noise, and transient faults.

The public execution record reports 8 focused tests and 30 independently generated unseen cases passing. It also records one implementation defect: controller calls between sensor deliveries caused permanent guarded mode and broke recovery/efficiency. The defect was repaired, the original failures were replayed unchanged, and the suite then passed.

## What did not pass

The literal operating envelope contained a sustained-load corner whose permitted heat input exceeded maximum heat rejection. That corner is physically infeasible. The final disposition was `PARTIAL`, not universal safety. The controller is a conservative reference, not a formal robust-control certificate. Reordered delivery and full physical deployment were not established.

## Finding

Frontier AI materially compressed multidisciplinary engineering execution in this bounded experiment: one local execution produced an inspectable architecture, executable implementation, deterministic replay, independent unseen evaluation, and a useful feasibility finding. The compression claim is about the bounded execution workflow, not about universal productivity or team replacement.

## Claim boundary

This note does not claim universal replacement of engineering teams, a universal productivity multiplier, production safety, general autonomous engineering capability, literal 3600x productivity, or scientific proof beyond the experiment. The independent evaluator and infeasible-corner finding are part of the result, not footnotes.

## Reproducibility boundary

The public research spine contains the clean-room experiment and its reproduction instructions. It does not recreate unavailable external execution context or convert a process record into cryptographic proof of secrecy. Read [`PROVENANCE.md`](../../PROVENANCE.md) and [`PUBLIC_CLAIMS.md`](../../PUBLIC_CLAIMS.md) before reusing the claim.

## Sources in this repository

- [`Mission 001 experiment`](../../experiments/num-synth-001/README.md) and [`SYS-PROTOCOL`](../../experiments/sys-protocol-001/README.md) provide the repository's existing bounded-experiment conventions.
- The multidisciplinary execution record is summarized from the completed bounded engineering report; no private repository, employer system, customer, or proprietary artifact is included here.
