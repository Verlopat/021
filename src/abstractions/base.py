from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from src.models.message import Message


class CommunicationAbstraction(ABC):
    level: str

    @abstractmethod
    def observe(self, messages: Sequence[Message]) -> Any:
        raise NotImplementedError

    @abstractmethod
    def canonicalize(self, messages: Sequence[Message]) -> Any:
        raise NotImplementedError

    def information_level(self) -> str:
        return self.level


def transition_factors_through(
    abstraction: CommunicationAbstraction,
    transition,
    states: Sequence[Any],
    histories: Sequence[Sequence[Message]],
) -> bool:
    """Executable factorization check for finite states/histories."""
    for state in states:
        for left in histories:
            for right in histories:
                if abstraction.observe(left) == abstraction.observe(right):
                    if transition(state, left) != transition(state, right):
                        return False
    return True
