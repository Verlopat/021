from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from .base import CorrectnessResult, Problem
from .validators import all_equal


@dataclass(frozen=True, slots=True)
class MultivaluedBA(Problem):
    values: tuple[Any, ...] = ("A", "B", "C")
    name: str = "Multivalued Byzantine Agreement"

    def decision_domain(self) -> Sequence[Any]:
        return self.values

    def check(self, decisions, correct_inputs, correct_processes) -> CorrectnessResult:
        vals = [decisions.get(p) for p in sorted(correct_processes)]
        termination = all(v is not None for v in vals)
        validity = all(v in self.values for v in vals)
        inputs = set(correct_inputs.values())
        if len(inputs) == 1:
            validity &= all(v == next(iter(inputs)) for v in vals)
        return CorrectnessResult(all_equal(vals), validity, termination, {"decisions": vals})
