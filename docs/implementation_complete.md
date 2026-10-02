# Implementation Coverage

This document maps the supplied research specification to the implementation.

| Specification area | Implementation |
|---|---|
| L0 Heard-Of/count-only | src/abstractions/l0.py |
| L1 gather/echo | src/abstractions/l1.py |
| L2 full content | src/abstractions/l2.py |
| Quotient/factorization | src/abstractions/base.py, src/formal/specification.py, lean/Basic.lean |
| Byzantine model | src/adversary/byzantine.py, src/adversary/strategies.py |
| Round/execution model | src/models/execution.py, src/models/system.py |
| Heard-Of delivery | src/models/scheduler.py |
| Authentication/digest/signature | src/crypto/auth.py |
| Connected Consensus | src/problems/connected_consensus.py |
| Crusader Agreement | src/problems/crusader_agreement.py |
| Multidimensional Approximate Agreement | src/problems/approximate_agreement.py |
| Multivalued Byzantine Agreement | src/problems/multivalued_ba.py |
| Set Agreement | src/problems/exploratory.py |
| Vector Agreement | src/problems/exploratory.py |
| L0 protocol | src/protocols/protocols.py |
| L1 protocol | src/protocols/protocols.py and l1_gather_decision.py |
| L2 protocol | src/protocols/protocols.py |
| Adversarial exhaustive search | src/analysis/model_checker.py |
| Observation separation | src/analysis/separation_search.py |
| Resilience characterization | src/analysis/resilience_full.py |
| Replayable simulation | src/simulation/engine.py |
| Machine-checked core | lean/Basic.lean and lean/Research.lean |
| Research matrix | src/analysis/research_matrix.py |
| Reproducible outputs | Main.py and src/reporting |
| Tests | tests/ |
| Paper package | paper/ |

## Important distinction

The software implementation is complete as a research framework and finite model checker. A mathematical theorem is a separate artifact.

For example, an exhaustive search can establish the status COUNTEREXAMPLE_FOUND for a concrete protocol and bounded configuration.

It cannot establish a universal impossibility theorem without a mathematical proof.

The implementation therefore records theorem status independently from experiment status.

## Full workflow

Main.py executes all implemented components in one run:

1. configuration loading
2. L0/L1/L2 witness construction
3. L0 factorization validation
4. observation-separation search
5. finite resilience sweep
6. six-problem bounded model checking
7. Byzantine reference simulation
8. report generation
9. plot generation
10. manifest/log creation

## Reproducibility

Every run receives a fresh numeric output/testN directory. The manifest records seed, n, f, artifacts, and theorem-policy metadata.

## Formal verification boundary

Lean proves the abstraction-level lemmas and concrete finite observation witness. The remaining problem-specific separation theorems are represented as proof obligations rather than false axioms.

## Future theorem promotion

A candidate theorem can be promoted only when:

1. the problem specification is fixed;
2. authentication and scheduler assumptions are fixed;
3. the adversary model is fixed;
4. a mathematical proof exists;
5. the relevant Lean proof compiles without sorry/admitted axioms;
6. the executable model has no contradictory counterexample under the same assumptions.
