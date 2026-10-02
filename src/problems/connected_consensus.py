from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from src.models.message import BOT
from .base import CorrectnessResult, Problem

CENTER = (BOT, 0)


def spider_distance(a: tuple, b: tuple) -> int:
    (va, ra), (vb, rb) = a, b
    if va == vb:
        return abs(ra - rb)
    return ra + rb


@dataclass(frozen=True, slots=True)
class ConnectedConsensus(Problem):
    values: tuple[Any, ...] = ("A", "B")
    R: int = 1
    name: str = "Connected Consensus"

    def decision_domain(self) -> Sequence[Any]:
        return self.values

    def vertices(self) -> list[tuple]:
        return [CENTER] + [(v, r) for v in self.values for r in range(1, self.R + 1)]

    def check(self, decisions, correct_inputs, correct_processes) -> CorrectnessResult:
        vals = [decisions.get(p) for p in sorted(correct_processes)]
        termination = all(v is not None for v in vals)
        if not termination:
            return CorrectnessResult(False, False, False, {"decisions": vals})
        verts = set(self.vertices())
        agreement = all(spider_distance(a, b) <= 1 for a in vals for b in vals)
        inputs = set(correct_inputs.values())
        if len(inputs) == 1:
            validity = all(v == (next(iter(inputs)), self.R) for v in vals)
        else:
            validity = all(v in verts and (v == CENTER or v[0] in inputs) for v in vals)
        return CorrectnessResult(agreement, validity, termination, {"decisions": vals, "R": self.R})
