from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class MultivaluedBA:
    values: tuple[T, ...]

    def agreement(self, decisions: Iterable[T]) -> bool:
        return len(set(decisions)) <= 1

    def validity(self, decision: T, correct_inputs: Iterable[T]) -> bool:
        correct = list(correct_inputs)
        if not correct:
            return True
        if len(set(correct)) == 1:
            return decision == correct[0]
        return decision in self.values

    @staticmethod
    def quorum(n: int, f: int) -> int:
        if not (0 <= f < n):
            raise ValueError("invalid n/f")
        return n - f
