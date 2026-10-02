from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Sequence
from .base import CorrectnessResult, Problem
from .validators import all_equal
@dataclass(frozen=True, slots=True)
class CrusaderAgreement(Problem):
    name:str="Crusader Agreement"
    values:tuple[Any,...]=("A","B","C")
    def decision_domain(self)->Sequence[Any]: return self.values
    def check(self,decisions,correct_inputs,correct_processes)->CorrectnessResult:
        vals=[decisions[p] for p in correct_processes if p in decisions]
        validity=all(v in self.values for v in vals)
        if correct_inputs and len(set(correct_inputs.values()))==1: validity &= all(v==next(iter(correct_inputs.values())) for v in vals)
        return CorrectnessResult(all_equal(vals),validity,len(vals)==len(correct_processes),{"decisions":vals})
