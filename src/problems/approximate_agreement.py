from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from .base import CorrectnessResult, Problem
from .validators import vector_diameter
@dataclass(frozen=True, slots=True)
class MultidimensionalApproximateAgreement(Problem):
    dimension:int=2
    epsilon:float=0.25
    name:str="Multidimensional Approximate Agreement"
    def decision_domain(self)->Sequence: return ((0.0,)*self.dimension,(0.5,)*self.dimension,(1.0,)*self.dimension)
    def check(self,decisions,correct_inputs,correct_processes)->CorrectnessResult:
        vals=[tuple(decisions[p]) for p in correct_processes if p in decisions]
        if correct_inputs:
            lo=[min(tuple(x)[d] for x in correct_inputs.values()) for d in range(self.dimension)]
            hi=[max(tuple(x)[d] for x in correct_inputs.values()) for d in range(self.dimension)]
            validity=all(all(lo[d]<=x[d]<=hi[d] for d in range(self.dimension)) for x in vals)
        else: validity=True
        diameter=vector_diameter(vals)
        return CorrectnessResult(diameter<=self.epsilon,validity,len(vals)==len(correct_processes),{"diameter":diameter,"epsilon":self.epsilon})
