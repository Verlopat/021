from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from src.models.message import BOT
from .base import CorrectnessResult, Problem


@dataclass(frozen=True, slots=True)
class CrusaderAgreement(Problem):
    values: tuple[Any, ...] = ("A", "B")
    name: str = "Crusader Agreement"

    def decision_domain(self) -> Sequence[Any]:
        return self.values

    def check(self, decisions, correct_inputs, correct_processes) -> CorrectnessResult:
        vals = [decisions.get(p) for p in sorted(correct_processes)]
        termination = all(v is not None for v in vals)
        non_bot = {v for v in vals if v not in (BOT, None)}
        agreement = len(non_bot) <= 1
        inputs = set(correct_inputs.values())
        validity = all(v in self.values or v == BOT for v in vals)
        if len(inputs) == 1:
            validity &= all(v == next(iter(inputs)) for v in vals)
        return CorrectnessResult(agreement, validity, termination, {"decisions": vals})
