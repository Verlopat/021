from __future__ import annotations

from dataclasses import dataclass
from math import dist
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ApproximateAgreementSpec:
    epsilon: float

    def agreement(self, outputs: Iterable[tuple[float, ...]]) -> bool:
        points = list(outputs)
        return all(dist(a, b) <= self.epsilon for i, a in enumerate(points) for b in points[i + 1 :])

    def validity_coordinatewise(self, output: tuple[float, ...], correct_inputs: Iterable[tuple[float, ...]]) -> bool:
        inputs = list(correct_inputs)
        if not inputs:
            return True
        if any(len(x) != len(output) for x in inputs):
            return False
        for j, value in enumerate(output):
            lo = min(x[j] for x in inputs)
            hi = max(x[j] for x in inputs)
            if value < lo or value > hi:
                return False
        return True
