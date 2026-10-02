from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class CrusaderAgreementSpec:
    """Parameterized Crusader Agreement contract.

    The exact validity rule is intentionally exposed as a parameter because
    published formulations differ on what is required when inputs conflict.
    """

    allow_outside_when_conflict: bool = True

    def agreement(self, decisions: Iterable[T]) -> bool:
        return len(set(decisions)) <= 1

    def unanimity_validity(self, decision: T, correct_inputs: Iterable[T]) -> bool:
        inputs = list(correct_inputs)
        if not inputs:
            return True
        if len(set(inputs)) == 1:
            return decision == inputs[0]
        return self.allow_outside_when_conflict or decision in inputs

    def termination(self, decided: Iterable[bool]) -> bool:
        return all(decided)
