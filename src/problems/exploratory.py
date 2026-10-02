from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class SetAgreementSpec:
    max_set_size: int

    def valid(self, decision_set: Iterable[T], correct_inputs: Iterable[T]) -> bool:
        decided = set(decision_set)
        return len(decided) <= self.max_set_size and decided.issubset(set(correct_inputs))


@dataclass(frozen=True, slots=True)
class VectorAgreementSpec:
    epsilon: float

    def coordinate_bound(self, vectors: Iterable[tuple[float, ...]]) -> float:
        values = list(vectors)
        if len(values) < 2:
            return 0.0
        return max(abs(a[j] - b[j]) for a in values for b in values for j in range(len(a)))

    def agreement(self, outputs: Iterable[tuple[float, ...]]) -> bool:
        return self.coordinate_bound(outputs) <= self.epsilon
