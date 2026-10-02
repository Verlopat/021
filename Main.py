"""Quick reproducible run: python3 Main.py."""
from __future__ import annotations
import os,re
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import run_experiments

def next_run_dir(root:Path)->Path:
    root.mkdir(parents=True,exist_ok=True)
    nums=[int(m.group(1)) for p in root.iterdir() if p.is_dir() and (m:=re.fullmatch(r"test(\d+)",p.name))]
    return root/f"test{max(nums,default=0)+1}"

def run()->Path:
    config=ROOT/os.getenv("CONFIG","configs/quick.yaml")
    out=next_run_dir(ROOT/os.getenv("OUTPUT_ROOT","output"))
    quiet=os.getenv("LOG_LEVEL","INFO").upper() in ("WARNING","ERROR")
    return run_experiments.run(config,out,log=(lambda *_:None) if quiet else print)

if __name__=="__main__": run()
