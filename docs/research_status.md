# Research Status and Proof Boundary

## Implemented end-to-end

- L0 count-only abstraction.
- L1 gather/echo certificate abstraction.
- L2 full-content abstraction.
- Explicit message and execution models.
- Finite Heard-Of mask generation.
- Byzantine equivocation generator.
- Omission and delay/reordering strategy descriptors.
- Six problem contracts and correctness predicates.
- L0/L1/L2 executable protocol implementations.
- Bounded exhaustive model checker.
- Observation-separation search.
- Resilience sweep and result classification.
- Replayable execution traces.
- Fresh output/testN artifact generation.
- Lean factorization and equivalence proofs.
- CI for Python tests, Main.py, and Lean.

## What is now automated

For every bounded configuration the model checker records:

- problem
- abstraction
- n
- f
- Byzantine set
- correct inputs
- protocol decisions
- correctness result
- complete message trace

Counterexamples are therefore concrete, replayable research artifacts.

## What remains a mathematical theorem obligation

The following are not hard-coded as facts:

1. A universal L0/L1 separation theorem.
2. A universal L1/L2 separation theorem.
3. Optimal n > 3f resilience for every listed problem.
4. A universal minimum-abstraction theorem L*(Pi).
5. Equivalence of this project's exact models with any external literature definition.

The implementation now provides the machinery needed to search for these results and to encode successful proof obligations.

## Authentication

Authentication is explicit on messages and certificates. Before comparing resilience results across abstractions, the paper must fix whether authentication is:

- an independent system assumption, or
- part of the communication abstraction.

Changing this choice changes the problem being characterized.

## Interpretation of finite results

COUNTEREXAMPLE_FOUND means the implemented protocol violates its specified property in a concrete finite execution.

NO_COUNTEREXAMPLE_IN_FINITE_SPACE means only that the configured bounded search did not find a violation.

TARGET_NOT_PROVED means the corresponding general theorem has not been machine-checked.

No finite search result is represented as a universal impossibility theorem.

## Reproducibility

All generated artifacts are written below a unique output/testN directory and include the experiment seed and configuration.
