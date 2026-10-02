from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Sequence
from .base import CorrectnessResult, Problem
from .validators import all_equal, vector_diameter
@dataclass(frozen=True, slots=True)
class SetAgreement(Problem):
    k:int=1
    name:str="Set Agreement"
    def decision_domain(self)->Sequence[Any]: return ("A","B","C")
    def check(self,decisions,correct_inputs,correct_processes)->CorrectnessResult:
        vals=[decisions[p] for p in correct_processes if p in decisions]
        return CorrectnessResult(len(set(map(repr,vals)))<=self.k,all(v in correct_inputs.values() for v in vals),len(vals)==len(correct_processes),{"distinct":len(set(map(repr,vals)))})
@dataclass(frozen=True, slots=True)
class VectorAgreement(Problem):
    dimension:int=2
    epsilon:float=0.25
    name:str="Vector Agreement"
    def decision_domain(self)->Sequence[Any]: return ((0.0,)*self.dimension,(0.5,)*self.dimension,(1.0,)*self.dimension)
    def check(self,decisions,correct_inputs,correct_processes)->CorrectnessResult:
        vals=[tuple(decisions[p]) for p in correct_processes if p in decisions]
        return CorrectnessResult(vector_diameter(vals)<=self.epsilon,True,len(vals)==len(correct_processes),{"diameter":vector_diameter(vals)})
