"""Unified research workflow entry point.

Run with: python3 Main.py
Every execution creates output/testN and stores deterministic, replayable artifacts.
"""
from __future__ import annotations

import json
import logging
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.analysis.indistinguishability import build_pair_witness, check_l0_factorization
from src.analysis.resilience import run_resilience_sweep
from src.analysis.separation import build_separation_report
from src.analysis.research_matrix import build_research_matrix
from src.reporting.io import write_json, write_text, write_csv
from src.reporting.report import render_markdown_report, render_plot
from src.simulation.engine import run_reference_simulation


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def setup_logging(level: str, log_path: Path) -> logging.Logger:
    logger = logging.getLogger("communication_abstraction")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(stream)
    logger.addHandler(file_handler)
    return logger


def next_run_dir(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(r"test(\d+)$")
    numbers = []
    for child in root.iterdir():
        if child.is_dir():
            m = pattern.fullmatch(child.name)
            if m:
                numbers.append(int(m.group(1)))
    return root / f"test{max(numbers, default=0) + 1}"


def load_config() -> dict[str, Any]:
    cfg = json.loads((ROOT / "configs" / "default.json").read_text(encoding="utf-8"))
    env = load_dotenv(ROOT / ".env")
    seed = int(os.getenv("RANDOM_SEED", env.get("RANDOM_SEED", cfg["seed"])))
    cfg["seed"] = seed
    cfg["output_root"] = os.getenv("OUTPUT_ROOT", env.get("OUTPUT_ROOT", cfg["output_root"]))
    cfg["n"] = int(os.getenv("DEFAULT_N", env.get("DEFAULT_N", cfg["n"])))
    cfg["f"] = int(os.getenv("DEFAULT_F", env.get("DEFAULT_F", cfg["f"])))
    return cfg


def run() -> Path:
    cfg = load_config()
    random.seed(cfg["seed"])
    out = next_run_dir(ROOT / cfg["output_root"])
    out.mkdir(parents=True, exist_ok=False)
    logger = setup_logging(os.getenv("LOG_LEVEL", "INFO"), out / "run.log")
    started = datetime.now(timezone.utc).isoformat()
    logger.info("starting research workflow: output=%s", out)

    witness = build_pair_witness()
    factorization = check_l0_factorization()
    write_json(out / "l0_l1_l2_witness.json", witness)
    write_json(out / "factorization_check.json", factorization)
    write_text(out / "execution_trace.jsonl", "\n".join(witness["execution_trace"]) + "\n")

    separation = build_separation_report(witness)
    write_json(out / "separation_report.json", separation)
    write_json(out / "research_matrix.json", build_research_matrix())

    sweep = run_resilience_sweep(max_n=cfg["sweep_max_n"], seed=cfg["seed"])
    write_json(out / "resilience_sweep.json", sweep)
    rows = []
    for row in sweep["rows"]:
        rows.append([row["n"], row["f"], row["abstraction"], row["witness_pass"], row["notes"]])
    write_csv(out / "resilience_sweep.csv", ["n", "f", "abstraction", "witness_pass", "notes"], rows)

    simulation = run_reference_simulation(n=cfg["n"], f=cfg["f"])
    write_json(out / "simulation_summary.json", simulation)

    report = render_markdown_report(cfg, witness, factorization, separation, sweep)
    write_text(out / "README.md", report)
    if cfg.get("generate_plot", True):
        try:
            render_plot(out / "resilience_boundary.png", sweep)
        except Exception as exc:
            logger.warning("plot generation skipped: %s", exc)

    manifest = {
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "seed": cfg["seed"],
        "n": cfg["n"],
        "f": cfg["f"],
        "output_dir": str(out.relative_to(ROOT)),
        "artifacts": sorted(p.name for p in out.iterdir()),
        "research_status": "finite-witness-and-framework; broad lattice theorems remain targets",
    }
    write_json(out / "manifest.json", manifest)
    logger.info("completed research workflow: output=%s", out)
    print(f"\nCompleted. Artifacts: {out.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    run()
