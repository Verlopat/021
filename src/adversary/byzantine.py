from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.models.message import Message
from src.models.system import Execution, SystemConfig


@dataclass(frozen=True, slots=True)
class ByzantineAdversary:
    byzantine: frozenset[int]

    def validate(self, n: int, f: int) -> None:
        if len(self.byzantine) > f:
            raise ValueError("adversary exceeds configured Byzantine budget")
        if not self.byzantine.issubset(set(range(n))):
            raise ValueError("unknown Byzantine process id")

    def equivocate(self, n: int, round_id: int, sender: int, values: dict[int, object], *, authenticated: bool = True) -> Execution:
        config = SystemConfig(n=n, f=len(self.byzantine))
        self.validate(n, config.f)
        messages = [Message(sender, receiver, round_id, value, authenticated=authenticated) for receiver, value in values.items()]
        return Execution(config, messages)


def adversarial_trace(n: int, f: int, byzantine: Iterable[int], round_id: int = 1) -> list[Message]:
    """Build a deterministic equivocation trace used by the finite witness tests."""
    bad = set(byzantine)
    if len(bad) > f:
        raise ValueError("too many Byzantine processes")
    trace: list[Message] = []
    for sender in range(n):
        for receiver in range(n):
            if sender in bad:
                value = "A" if receiver % 2 == 0 else "C"
            else:
                value = "B"
            trace.append(Message(sender, receiver, round_id, value, authenticated=True))
    return trace
