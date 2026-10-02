from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from .base import CorrectnessResult, Problem
from .validators import in_convex_hull, vector_diameter


@dataclass(frozen=True, slots=True)
class MultidimensionalApproximateAgreement(Problem):
    dimension: int = 1
    epsilon: float = 0.25
    inputs: tuple[tuple[float, ...], ...] = ((0.0,), (1.0,))
    name: str = "Multidimensional Approximate Agreement"

    def decision_domain(self) -> Sequence:
        return self.inputs

    def check(self, decisions, correct_inputs, correct_processes) -> CorrectnessResult:
        vals = [decisions.get(p) for p in sorted(correct_processes)]
        termination = all(v is not None for v in vals)
        if not termination:
            return CorrectnessResult(False, False, False, {"decisions": vals})
        vals = [tuple(v) for v in vals]
        hull_pts = [tuple(x) for x in correct_inputs.values()]
        validity = all(in_convex_hull(v, hull_pts) for v in vals)
        diameter = vector_diameter(vals)
        return CorrectnessResult(
            diameter <= self.epsilon + 1e-12,
            validity,
            termination,
            {"diameter": diameter, "epsilon": self.epsilon, "decisions": vals},
        )
