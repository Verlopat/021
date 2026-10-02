"""Experiment registry."""
from __future__ import annotations
from typing import Any

from src.problems.approximate_agreement import MultidimensionalApproximateAgreement
from src.problems.connected_consensus import ConnectedConsensus
from src.problems.crusader_agreement import CrusaderAgreement
from src.problems.multivalued_ba import MultivaluedBA
from src.protocols.round_protocols import (
    CountConnectedConsensus, CountCrusader, OwnInputProtocol, PhaseKing,
    TrimmedMidpointApproximate,
)
from .model_checker import check_protocol, resilience_boundary


def build(problem: str, protocol: str, values: tuple, R: int = 1, epsilon: float = 0.25):
    if problem == "crusader":
        prob, dom = CrusaderAgreement(values), values
    elif problem == "connected":
        prob, dom = ConnectedConsensus(values, R), values
    elif problem == "mvba":
        prob, dom = MultivaluedBA(values), values
    elif problem == "approx":
        prob = MultidimensionalApproximateAgreement(1, epsilon)
        dom = prob.inputs
    else:
        raise ValueError(problem)
    factories = {
        "own-input": lambda n, f: OwnInputProtocol(n, f, values, output="vertex" if problem=="connected" else "value", R=R),
        "count-crusader": lambda n, f: CountCrusader(n, f, values),
        "count-connected": lambda n, f: CountConnectedConsensus(n, f, values, R),
        "phase-king": lambda n, f: PhaseKing(n, f, values, vertex_R=R if problem=="connected" else None),
        "trimmed-midpoint": lambda n, f: TrimmedMidpointApproximate(n, f, dom, epsilon),
    }
    return prob, factories[protocol], dom


def run_experiments(cfg: dict[str, Any], log=print) -> dict[str, list[dict]]:
    values=tuple(cfg.get("values",["A","B"]))
    seed,auth,max_exec=cfg.get("seed",0),cfg.get("auth","B"),cfg.get("max_exec",20000)
    correctness=[]; boundary=[]
    for exp in cfg["experiments"]:
        prob,factory,dom=build(exp["problem"],exp["protocol"],values,exp.get("R",1),exp.get("epsilon",0.25))
        for n,f in exp["configs"]:
            log(f"check {exp['problem']}/{exp['protocol']} n={n} f={f}")
            row=check_protocol(prob,factory(n,f),n,f,dom,auth=auth,
                               max_exec=exp.get("max_exec",max_exec),seed=seed)
            row["experiment"]=exp.get("name",f"{exp['problem']}/{exp['protocol']}")
            correctness.append(row)
        if exp.get("boundary_f"):
            for b in resilience_boundary(prob,factory,exp["boundary_f"],dom,auth=auth,
                                          max_exec=exp.get("max_exec",max_exec),seed=seed):
                b["protocol"]=exp["protocol"]; boundary.append(b)
    return {"correctness":correctness,"boundary":boundary}
