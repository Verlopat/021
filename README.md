# 021 — Communication Abstractions for Byzantine Resilience

This repository implements a reproducible research framework for studying synchronous Byzantine algorithms by communication information.

## Run

Quick smoke/evaluation run:

```bash
python3 Main.py
```

Full finite evaluation:

```bash
python run_experiments.py --config configs/all.yaml
```

Each quick run writes to a fresh `output/testN`; the full runner writes to `results/`.

## Research status

See [docs/research_status.md](docs/research_status.md). Finite model checking is evidence for the checked parameter space, not a universal theorem.

## Abstractions

- `L0-blind`: counts of fixed message kinds, no values.
- `L0`: anonymous counts of message kind/value pairs; sender identity erased.
- `L1`: L0 plus sender-attributed certificate entries.
- `L2`: full message content.

The round engine passes protocols only the selected abstraction observation.

## Lean 4

The formal core is pinned to Lean 4.15:

```bash
cd lean
lake build
lake env lean CheckAxioms.lean
```

The core development contains no `sorry` or unfinished proof terms; axiom dependencies are reported by `CheckAxioms.lean`.

## Paper

The paper sources are under `paper/`. The generated evaluation table is reproducible from `results/resilience.csv`.
