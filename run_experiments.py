"""Single-command reproduction."""
from __future__ import annotations
import argparse,json,platform,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from src.analysis.experiments import run_experiments
from src.analysis.indistinguishability import build_pair_witness,check_l0_factorization
from src.analysis.reporting import summarize_matrix
from src.analysis.research_matrix import build_research_matrix,matrix_markdown
from src.reporting.io import write_csv,write_json,write_text

def load_config(path:Path):
    text=path.read_text(encoding="utf-8")
    if path.suffix in (".yaml",".yml"):
        import yaml
        return yaml.safe_load(text)
    return json.loads(text)

def plot_boundary(path:Path,boundary:list[dict])->None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(7,4.5))
    fs=sorted({b["f"] for b in boundary})
    if fs: ax.plot(fs,[3*f+1 for f in fs],"k--",label="3f+1 (theory)")
    for proto in sorted({b["protocol"] for b in boundary}):
        pts=[(b["f"],b["observed_n_min"]) for b in boundary if b["protocol"]==proto and b["observed_n_min"]]
        if pts: ax.plot(*zip(*pts),"o-",label=f"{proto} (observed)")
    ax.set_xlabel("f"); ax.set_ylabel("smallest n without counterexample")
    ax.set_title("Observed resilience boundary"); ax.legend()
    fig.tight_layout(); fig.savefig(path,dpi=160); plt.close(fig)

def run(config_path:Path,out:Path,log=print)->Path:
    cfg=load_config(config_path)
    out.mkdir(parents=True,exist_ok=True); (out/"counterexamples").mkdir(exist_ok=True); (out/"figures").mkdir(exist_ok=True)
    t0=time.time()
    write_json(out/"witnesses.json",{"information_chain":build_pair_witness(),"l0_factorization":check_l0_factorization()})
    results=run_experiments(cfg,log=log); rows,boundary=results["correctness"],results["boundary"]
    write_csv(out/"correctness.csv",["experiment","problem","protocol","abstraction","auth","n","f","n_gt_3f","mode","executions","space_size","status","violated"],
              [[r["experiment"],r["problem"],r["protocol"],r["abstraction"],r["auth"],r["n"],r["f"],r["n_gt_3f"],r["mode"],r["executions"],r["space_size"],r["status"],";".join(r.get("counterexample",{}).get("violated",[]))] for r in rows])
    write_csv(out/"communication.csv",["experiment","n","f","rounds","messages_per_execution","bytes_per_execution","certificate_entries_per_execution"],
              [[r["experiment"],r["n"],r["f"],r["rounds"],round(r["messages_per_execution"],2),round(r["bytes_per_execution"],2),round(r["certificate_entries_per_execution"],2)] for r in rows])
    write_csv(out/"resilience.csv",["problem","protocol","f","observed_n_min","theoretical_n_min","matches"],
              [[b["problem"],b["protocol"],b["f"],b["observed_n_min"],b["theoretical_n_min"],b["matches"]] for b in boundary])
    for i,r in enumerate(x for x in rows if x["status"]=="COUNTEREXAMPLE_FOUND"):
        write_json(out/"counterexamples"/f"{i:03d}_{r['protocol'].split(' ')[0]}_n{r['n']}_f{r['f']}.json",r)
    write_json(out/"model_check_summary.json",summarize_matrix(rows))
    write_json(out/"research_matrix.json",build_research_matrix())
    write_text(out/"research_matrix.md",matrix_markdown())
    if boundary:
        try: plot_boundary(out/"figures"/"resilience_boundary.png",boundary)
        except Exception as exc: log(f"plot skipped: {exc}")
    write_json(out/"manifest.json",{"config_file":str(config_path),"config":cfg,"seed":cfg.get("seed"),"python":platform.python_version(),"seconds":round(time.time()-t0,2),
                                  "theorem_policy":"model checking is evidence for the checked (n,f) only; theorems come from proofs, Lean, or matched literature"})
    log(f"done: {out}"); return out

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default="configs/all.yaml"); ap.add_argument("--out",default="results")
    a=ap.parse_args(); run(ROOT/a.config if not Path(a.config).is_absolute() else Path(a.config),ROOT/a.out)
