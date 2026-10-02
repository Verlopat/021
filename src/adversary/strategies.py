from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence

from src.models.message import Message


@dataclass(frozen=True, slots=True)
class AdversaryStrategy:
    name: str
    description: str
    supports_adaptation: bool = False


STATIC_EQUIVOCATION = AdversaryStrategy(
    "static-equivocation",
    "Byzantine senders choose receiver-specific payloads in a fixed round.",
)
OMISSION = AdversaryStrategy(
    "omission",
    "The scheduler may suppress selected deliveries.",
)
DELAY_REORDER = AdversaryStrategy(
    "delay-reorder",
    "The scheduler varies delivery order and may defer messages to a later round.",
)
ADAPTIVE = AdversaryStrategy(
    "adaptive",
    "The adversary chooses later messages after observing prior delivered views.",
    True,
)


def generate_equivocation(
    n: int,
    byzantine: Iterable[int],
    honest_value: str,
    alternate_value: str,
    round_id: int = 1,
) -> list[Message]:
    bad = set(byzantine)
    result: list[Message] = []
    for sender in range(n):
        for receiver in range(n):
            if sender in bad and sender != receiver:
                value = alternate_value if receiver % 2 else honest_value
            else:
                value = honest_value
            result.append(Message(sender, receiver, round_id, value, "proposal", True))
    return result


def enumerate_byzantine_values(
    n: int,
    byzantine: Sequence[int],
    values: Sequence[str],
    *,
    round_id: int = 1,
) -> list[list[Message]]:
    """Finite exhaustive receiver-specific Byzantine payload generator."""
    honest = [p for p in range(n) if p not in set(byzantine)]
    executions: list[list[Message]] = []
    receiver_pairs = [(b, r) for b in byzantine for r in range(n) if r != b]
    for assignment in product(values, repeat=len(receiver_pairs)):
        table = dict(zip(receiver_pairs, assignment))
        msgs=[]
        for sender in range(n):
            for receiver in range(n):
                if sender in byzantine:
                    value = table.get((sender, receiver), values[0])
                else:
                    value = values[0]
                msgs.append(Message(sender, receiver, round_id, value, "proposal", True))
        executions.append(msgs)
    return executions
