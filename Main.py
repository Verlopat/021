"""Unified research-grade workflow.
Run: python3 Main.py
Every run creates output/testN. Finite search is never promoted to a universal theorem.
"""
from __future__ import annotations
import json, logging, os, random, re, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from src.analysis.indistinguishability import build_pair_witness, check_l0_factorization
from src.analysis.resilience import run_resilience_sweep
from src.analysis.resilience_full import run_full_characterization
from src.analysis.separation import build_separation_report
from src.analysis.separation_search import search_observation_separation
from src.analysis.research_matrix import build_research_matrix
from src.analysis.reporting import summarize_matrix
from src.reporting.io import write_json, write_text, write_csv
from src.reporting.report import render_markdown_report, render_plot
from src.simulation.engine import run_reference_simulation

def load_dotenv(path:Path)->dict[str,str]:
    result={}
    if not path.exists(): return result
    for line in path.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if line and not line.startswith("#") and "=" in line:
            k,v=line.split("=",1); result[k.strip()]=v.strip().strip('"').strip("'")
    return result

def setup_logging(level:str,path:Path)->logging.Logger:
    log=logging.getLogger("communication_abstraction")
    log.handlers.clear(); log.setLevel(getattr(logging,level.upper(),logging.INFO))
    fmt=logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    sh=logging.StreamHandler(sys.stdout); sh.setFormatter(fmt)
    fh=logging.FileHandler(path,encoding="utf-8"); fh.setFormatter(fmt)
    log.addHandler(sh); log.addHandler(fh); return log

def next_run_dir(root:Path)->Path:
    root.mkdir(parents=True,exist_ok=True)
    nums=[]
    for p in root.iterdir():
        m=re.fullmatch(r"test(\d+)",p.name)
        if p.is_dir() and m: nums.append(int(m.group(1)))
    return root/f"test{max(nums,default=0)+1}"

def load_config()->dict[str,Any]:
    cfg=json.loads((ROOT/"configs/default.json").read_text(encoding="utf-8"))
    env=load_dotenv(ROOT/".env")
    for key in ("RANDOM_SEED","OUTPUT_ROOT","DEFAULT_N","DEFAULT_F","FULL_MATRIX_MAX_N","MODEL_CHECK_MAX_EXEC"):
        if key in os.environ: env[key]=os.environ[key]
    cfg["seed"]=int(env.get("RANDOM_SEED",cfg["seed"]))
    cfg["output_root"]=env.get("OUTPUT_ROOT",cfg["output_root"])
    cfg["n"]=int(env.get("DEFAULT_N",cfg["n"])); cfg["f"]=int(env.get("DEFAULT_F",cfg["f"]))
    cfg["full_matrix_max_n"]=int(env.get("FULL_MATRIX_MAX_N",cfg.get("full_matrix_max_n",5)))
    cfg["model_check_max_exec"]=int(env.get("MODEL_CHECK_MAX_EXEC",cfg.get("model_check_max_exec",256)))
    return cfg

def run()->Path:
    cfg=load_config(); random.seed(cfg["seed"])
    out=next_run_dir(ROOT/cfg["output_root"]); out.mkdir()
    logger=setup_logging(os.getenv("LOG_LEVEL","INFO"),out/"run.log")
    started=datetime.now(timezone.utc).isoformat()
    logger.info("starting complete research workflow")

    witness=build_pair_witness(); factorization=check_l0_factorization()
    write_json(out/"l0_l1_l2_witness.json",witness)
    write_json(out/"factorization_check.json",factorization)
    write_text(out/"execution_trace.jsonl","\n".join(witness["execution_trace"])+"\n")

    separation=build_separation_report(witness)
    obs_search=search_observation_separation()
    write_json(out/"separation_report.json",separation)
    write_json(out/"observation_separation_search.json",obs_search)
    write_json(out/"research_matrix.json",build_research_matrix())

    sweep=run_resilience_sweep(max_n=cfg["sweep_max_n"],seed=cfg["seed"])
    write_json(out/"resilience_sweep.json",sweep)
    write_csv(out/"resilience_sweep.csv",["n","f","abstraction","witness_pass","notes"],
              [[r["n"],r["f"],r["abstraction"],r["witness_pass"],r["notes"]] for r in sweep["rows"]])

    logger.info("running bounded exhaustive model checker")
    matrix=run_full_characterization(max_n=cfg["full_matrix_max_n"],max_exec=cfg["model_check_max_exec"])
    write_json(out/"full_model_check.json",matrix)
    write_json(out/"full_model_check_summary.json",summarize_matrix(matrix))

    simulation=run_reference_simulation(cfg["n"],cfg["f"])
    write_json(out/"simulation_summary.json",simulation)

    report=render_markdown_report(cfg,witness,factorization,separation,sweep)
    report += "\n\n## Full model-checking status\n\n"
    report += "The matrix is a bounded executable search, not a universal theorem. See full_model_check.json.\n"
    write_text(out/"README.md",report)
    if cfg.get("generate_plot",True):
        try: render_plot(out/"resilience_boundary.png",sweep)
        except Exception as exc: logger.warning("plot generation skipped: %s",exc)

    manifest={"started_at":started,"finished_at":datetime.now(timezone.utc).isoformat(),
              "seed":cfg["seed"],"n":cfg["n"],"f":cfg["f"],
              "output_dir":str(out.relative_to(ROOT)),
              "artifacts":sorted(p.name for p in out.iterdir()),
              "workflow":"full bounded model-checking + simulation + separation search",
              "model_check_max_exec":cfg["model_check_max_exec"],
              "theorem_policy":"finite evidence is never promoted to a universal theorem"}
    write_json(out/"manifest.json",manifest)
    logger.info("completed research workflow: %s",out)
    print(f"\nCompleted: {out.relative_to(ROOT)}")
    return out

if __name__=="__main__":
    run()
