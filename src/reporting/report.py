from __future__ import annotations

from pathlib import Path
from typing import Any


def render_markdown_report(cfg: dict[str, Any], witness: dict[str, Any], factorization: dict[str, Any], separation: dict[str, Any], sweep: dict[str, Any]) -> str:
    claims = witness["claims"]
    return f"""# Communication-Abstraction Research Run

## Scope

This run executes the finite, reproducible core of the proposed L0/L1/L2 research framework. It is deliberately conservative: finite information-separation witnesses are reported as such, while general Byzantine-resilience theorems remain explicit research targets.

## Configuration

- Seed: `{cfg['seed']}`
- Default system: `n={cfg['n']}`, `f={cfg['f']}`
- Sweep: `n=4..{cfg['sweep_max_n']}`

## L0/L1/L2 witness

- Same L0 observation: **{claims['same_L0']}**
- Different L1 observation: **{claims['different_L1']}**
- Different L2 observation: **{claims['different_L2']}**

The witness establishes that the implemented observation functions are informationally distinct on the selected finite histories. It does not, by itself, prove a distributed impossibility theorem.

## Canonical-round factorization

- Executable factorization property: **{factorization['passed']}**

## Separation status

- L0 < L1 general Byzantine agreement: `{separation['theorem_status']['L0_lt_L1_for_general_BA']}`
- L1 < L2 general Byzantine agreement: `{separation['theorem_status']['L1_lt_L2_for_general_BA']}`
- Connected Consensus optimal resilience: `{separation['theorem_status']['connected_consensus_optimal_resilience']}`

## Resilience sweep

The CSV/JSON sweep enumerates finite witness distinguishability, not a claim that the resulting rows equal formal Byzantine resilience thresholds. The target theoretical boundary is `{sweep['theoretical_boundary']}`.

## Reproducibility

All artifacts are deterministic for a fixed seed. The run writes `execution_trace.jsonl`, machine-readable result files, a Markdown report, and an optional plot.
"""


def render_plot(path: Path, sweep: dict[str, Any]) -> None:
    import matplotlib.pyplot as plt

    rows = sweep["rows"]
    abstractions = ("L0", "L1", "L2")
    fig, ax = plt.subplots(figsize=(8, 5))
    for abstraction in abstractions:
        subset = [r for r in rows if r["abstraction"] == abstraction]
        xs = [r["n"] for r in subset if r["witness_pass"]]
        ys = [r["f"] for r in subset if r["witness_pass"]]
        if xs:
            ax.scatter(xs, ys, label=abstraction)
    ax.set_xlabel("n")
    ax.set_ylabel("f")
    ax.set_title("Finite information-witness distinguishability")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
