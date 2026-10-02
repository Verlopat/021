from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable, Sequence


@dataclass(frozen=True, slots=True)
class CorrectnessResult:
    agreement: bool
    validity: bool
    termination: bool
    details: dict[str, Any]

    @property
    def passed(self) -> bool:
        return self.agreement and self.validity and self.termination


class Problem(ABC):
    name: str

    @abstractmethod
    def check(
        self,
        decisions: dict[int, Any],
        correct_inputs: dict[int, Any],
        correct_processes: set[int],
    ) -> CorrectnessResult:
        raise NotImplementedError

    @abstractmethod
    def decision_domain(self) -> Sequence[Any]:
        raise NotImplementedError
