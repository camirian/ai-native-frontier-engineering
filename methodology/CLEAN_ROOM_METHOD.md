# Clean-room method

Each mission is a bounded synthetic experiment, not a product benchmark.

**Specification first.** Freeze the operator or structural model, validity limits, design cases, and what the search cannot see.

**Separation of roles.** Candidate generation may be parallelized, but the oracle owns validity decisions. The candidate-selection process cannot alter held-out cases.

**Finalist freeze.** Persist candidate bytes and evaluator hash before held-out evaluation. A held-out failure changes the interpretation of the design-set result; it is not discarded.

**Bounded claims.** Report both the apparent result and the strongest falsifier. Do not generalize from this package to real structures, deployed numerical workloads, or the capabilities of AI systems broadly.

The organization-of-one observation is `PARTIALLY_SUPPORTED`: the workflow was operated by an AI-amplified engineer across three bounded missions, with two partial/inconclusive outcomes and one predefined Gate PASS. It is not a productivity or economic claim.
