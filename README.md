# 021 — Complete Communication-Abstraction Research Framework

This repository is the executable implementation of the proposed L0/L1/L2 Byzantine-resilience research program. It contains the communication abstractions, explicit round/execution model, Byzantine strategy generators, six problem specifications, executable protocols, bounded exhaustive model checking, observation-separation search, simulation, Lean verification, paper sources, and reproducible reporting.

## One-command workflow

```bash
python3 Main.py
```

Every invocation creates a new output/testN directory. No previous run is overwritten.

## What Main.py runs

1. L0/L1/L2 information witness.
2. L0 factorization check.
3. L0/L1 observation-separation search.
4. Finite resilience sweep.
5. Six-problem bounded exhaustive model checking.
6. Byzantine equivocation simulation.
7. L1 certificate protocol execution.
8. JSON/CSV/JSONL/Markdown/PNG reporting.
9. Run manifest and structured logging.

## Important scientific boundary

The implementation is complete as an experimental/formal framework, but finite model checking is not silently promoted to a universal theorem. A result is reported as one of:

- COUNTEREXAMPLE_FOUND
- NO_COUNTEREXAMPLE_IN_FINITE_SPACE
- TARGET_NOT_PROVED

A universal claim such as L0 < L1 or optimal n > 3f is promoted to a theorem only after the corresponding problem semantics, adversary model, authentication assumptions, and proof are formalized.

## Architecture

```text
Main.py
  ├── abstractions: L0 / L1 / L2
  ├── models: messages / rounds / executions / Heard-Of
  ├── adversary: equivocation / omission / delay / adaptive strategy descriptors
  ├── problems: Crusader / Connected / Approximate / MVBA / Set / Vector
  ├── protocols: L0 count-only / L1 certificate / L2 full-content
  ├── analysis: separation / model checking / resilience characterization
  ├── simulation: replayable Byzantine executions
  ├── formal: Python-side theorem specifications
  └── Lean: machine-checked abstraction core
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
```

Supported overrides include:

```text
RANDOM_SEED
DEFAULT_N
DEFAULT_F
OUTPUT_ROOT
FULL_MATRIX_MAX_N
MODEL_CHECK_MAX_EXEC
LOG_LEVEL
```

## Tests

```bash
pytest
```

## Lean

```bash
cd lean
lake env lean Basic.lean
```

## Output

Each run contains:

```text
output/testN/
├── README.md
├── manifest.json
├── run.log
├── l0_l1_l2_witness.json
├── factorization_check.json
├── observation_separation_search.json
├── separation_report.json
├── research_matrix.json
├── resilience_sweep.json
├── resilience_sweep.csv
├── full_model_check.json
├── full_model_check_summary.json
├── simulation_summary.json
├── execution_trace.jsonl
└── resilience_boundary.png
```

## Research artifacts

The bounded model checker enumerates Byzantine fault sets and finite receiver-specific Byzantine payload assignments. It executes the implemented protocol for each abstraction and evaluates agreement, validity, termination, and approximate/vector constraints where applicable.

This gives reproducible counterexamples and finite evidence. It does not claim infinite-state impossibility from finite search.

## Formal core

The Lean development formalizes:

```text
FactorsThrough
Indistinguishable
L0 transition invariance
reflexivity
symmetry
transitivity
```

The Lean proof is deliberately independent of Python representation details so the abstraction theorem can later be instantiated with a richer formal message model.

## Paper

The paper directory contains the formal definitions, theorem statements, protocol construction, evaluation methodology, and bibliography skeleton. It is designed to consume generated artifacts from output/testN.

## Development principle

The system is intentionally capable of disproving the proposed lattice. If a counterexample invalidates a candidate theorem, the software records it instead of forcing the expected result.
