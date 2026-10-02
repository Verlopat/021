# 021 — Communication-Abstraction Characterization for Byzantine Resilience

A reproducible research software framework implementing the supplied L0/L1/L2 communication-abstraction model, finite indistinguishability witnesses, Byzantine execution primitives, problem specifications, resilience sweeps, reporting, and a Lean core verification target.

> **Proof boundary:** this repository does not pretend that finite experiments establish general impossibility or optimal-resilience theorems. Those claims remain explicitly marked as research targets until the exact problem definitions and adversary/authentication assumptions are fixed.

## One-command workflow

```bash
python3 Main.py
```

Every invocation creates a new folder: `output/test1`, `output/test2`, ..., without overwriting prior runs.

## What the workflow executes

1. Builds an L0/L1/L2 finite information-separation witness.
2. Checks the canonical-round L0 factorization property.
3. Produces separation/theorem-status metadata.
4. Runs a deterministic finite `n,f` sweep.
5. Executes a Byzantine equivocation trace and the reusable L1 gather + decision protocol skeleton.
6. Writes JSON, CSV, JSONL trace, Markdown, manifest, log, and an optional PNG.

## Repository layout

```text
021/
├── Main.py
├── README.md
├── configs/default.json
├── src/
│   ├── abstractions/
│   ├── adversary/
│   ├── analysis/
│   ├── models/
│   ├── problems/
│   └── reporting/
├── tests/
├── lean/
├── paper/main.tex
├── docs/research_status.md
└── .github/workflows/ci.yml
```

## Environment

The runtime requires Python 3.10+ for the core package. The optional scientific/reporting stack is listed in `requirements.txt`. Lean verification uses the toolchain declared in `lean/lean-toolchain`.

## Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The core workflow uses the Python standard library and will still run when optional plotting libraries are unavailable; the plot is then skipped with a warning.

## Environment configuration

Copy `.env.example` to `.env` and override values such as `RANDOM_SEED`, `DEFAULT_N`, `DEFAULT_F`, `OUTPUT_ROOT`, and `LOG_LEVEL`.

## Tests

```bash
pytest
```

## Lean core

With Lean/Lake installed:

```bash
cd lean
lake env lean Basic.lean
```

## Research model implemented

### L0
Only canonical counts of message labels are visible. Payload values and sender identities are not exposed by `observe()`.

### L1
L0 counts are augmented with an authenticated sender/value certificate. The abstraction is deliberately structured rather than arbitrary payload semantics.

### L2
Full message contents are retained.

## Current status

The finite information witness demonstrates that the implemented observation functions distinguish histories at progressively higher levels. The broader claims `L0 < L1`, `L1 < L2`, and optimal `n > 3f` resilience for specific literature-defined problems require additional formal problem semantics and proofs.
