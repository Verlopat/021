from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Sequence
from .base import CorrectnessResult, Problem
from .validators import all_equal, majority
@dataclass(frozen=True, slots=True)
class ConnectedDomain:
    vertices: tuple[str,...]=("A","B","C")
    edges: tuple[tuple[str,str],...]=(("A","B"),("B","C"))
    def __post_init__(self):
        v=set(self.vertices)
        if any(a not in v or b not in v for a,b in self.edges): raise ValueError("edge references unknown vertex")
    def connected_hull(self,values:Iterable[str])->set[str]:
        vals=set(values)
        if not vals: return set(self.vertices)
        if not vals.issubset(set(self.vertices)): raise ValueError("value outside domain")
        idx={v:i for i,v in enumerate(self.vertices)}
        lo=min(idx[v] for v in vals); hi=max(idx[v] for v in vals)
        return set(self.vertices[lo:hi+1])
@dataclass(frozen=True, slots=True)
class ConnectedConsensus(Problem):
    domain: ConnectedDomain=ConnectedDomain()
    name:str="Connected Consensus"
    def decision_domain(self)->Sequence[str]: return self.domain.vertices
    def check(self,decisions,correct_inputs,correct_processes)->CorrectnessResult:
        vals=[decisions[p] for p in correct_processes if p in decisions]
        hull=self.domain.connected_hull(correct_inputs.values())
        return CorrectnessResult(all_equal(vals),all(v in hull for v in vals),len(vals)==len(correct_processes),{"hull":sorted(hull),"decisions":vals})
def connected_consensus_decision(values:Iterable[str],domain:ConnectedDomain)->str:
    vals=[v for v in values if v in domain.vertices]
    return majority(vals) if vals else domain.vertices[0]
