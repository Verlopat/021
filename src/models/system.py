from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .message import Message


@dataclass(frozen=True, slots=True)
class SystemConfig:
    n: int
    f: int

    def valid(self) -> bool:
        return self.n >= 1 and 0 <= self.f < self.n


@dataclass
class Execution:
    config: SystemConfig
    messages: list[Message]

    def validate(self) -> None:
        if not self.config.valid():
            raise ValueError("invalid system configuration")
        ids = range(self.config.n)
        for m in self.messages:
            if m.sender not in ids or m.receiver not in ids:
                raise ValueError(f"process id out of range: {m}")
            if m.round < 0:
                raise ValueError("round must be non-negative")

    def round_messages(self, round_id: int, receiver: int | None = None) -> list[Message]:
        result = [m for m in self.messages if m.round == round_id]
        if receiver is not None:
            result = [m for m in result if m.receiver == receiver]
        return sorted(result, key=lambda x: (x.sender, x.receiver, x.kind, repr(x.value)))

    def senders(self, round_id: int, receiver: int) -> set[int]:
        return {m.sender for m in self.round_messages(round_id, receiver)}


def honest_processes(n: int, byzantine: Iterable[int]) -> set[int]:
    bad = set(byzantine)
    return set(range(n)) - bad
