from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Sequence

@dataclass(frozen=True, slots=True)
class LatticeSpec:
    levels:tuple[str,...]=("L0","L1","L2")
    target_boundary:str="n > 3f"
    theorem_status:str="candidate; requires problem-specific proof"

@dataclass(frozen=True, slots=True)
class FactorizationWitness:
    abstraction:str
    same_observation:bool
    same_transition:bool
    valid:bool
    details:dict[str,Any]

def factorization_witness(observe:Callable,transition:Callable,state:Any,left:Sequence,right:Sequence)->FactorizationWitness:
    same=observe(left)==observe(right)
    same_t=transition(state,left)==transition(state,right)
    return FactorizationWitness("L0",same,same_t,(not same) or same_t,{"observation_left":repr(observe(left)),"observation_right":repr(observe(right))})
