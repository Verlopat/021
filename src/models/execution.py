from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Iterable, Sequence

from .message import Message
from .system import Execution, SystemConfig


@dataclass(frozen=True, slots=True)
class DeliveryPolicy:
    """Finite communication-closed round policy.

    correct_sender_delivery=True models reliable delivery from correct senders.
    A Heard-Of mask may then omit only messages selected by the adversarial
    scheduler.  Byzantine senders remain unconstrained.
    """
    correct_sender_delivery: bool = True
    allow_omission: bool = False
    allow_delay: bool = False
    allow_reordering: bool = True


@dataclass(frozen=True, slots=True)
class ExecutionSpec:
    n: int
    f: int
    rounds: int = 1
    policy: DeliveryPolicy = DeliveryPolicy()

    def validate(self) -> None:
        if self.n <= 0 or self.f < 0 or self.f >= self.n:
            raise ValueError("require n > f >= 0")
        if self.rounds <= 0:
            raise ValueError("rounds must be positive")


@dataclass
class ScheduledExecution:
    spec: ExecutionSpec
    byzantine: frozenset[int]
    messages: list[Message] = field(default_factory=list)
    heard_of: dict[tuple[int, int], frozenset[int]] = field(default_factory=dict)

    def as_execution(self) -> Execution:
        e = Execution(SystemConfig(self.spec.n, self.spec.f), list(self.messages))
        e.validate()
        return e

    def receiver_view(self, receiver: int, round_id: int) -> list[Message]:
        return self.as_execution().round_messages(round_id, receiver)

    def heard_of_set(self, receiver: int, round_id: int) -> frozenset[int]:
        return self.heard_of.get((receiver, round_id), frozenset())

    def trace(self) -> list[dict]:
        return [
            {
                "sender": m.sender, "receiver": m.receiver, "round": m.round,
                "value": m.value, "kind": m.kind,
                "authenticated": m.authenticated,
                "heard_of": sorted(self.heard_of_set(m.receiver, m.round)),
            }
            for m in self.messages
        ]


def enumerate_heard_of_masks(
    n: int,
    byzantine: Iterable[int],
    *,
    allow_omission: bool,
    max_missing_per_receiver: int = 1,
) -> list[dict[int, frozenset[int]]]:
    """Enumerate finite Heard-Of choices for one round.

    The enumeration is deliberately bounded so model checking remains finite.
    Correct-sender delivery is retained unless omission is explicitly enabled.
    """
    bad = set(byzantine)
    senders = tuple(range(n))
    choices = []
    for receiver in range(n):
        allowed = list(senders)
        if not allow_omission:
            choices.append([frozenset(allowed)])
            continue
        local = []
        for mask_bits in product((0, 1), repeat=n):
            missing = sum(1 for b in mask_bits if not b)
            if missing <= max_missing_per_receiver:
                local.append(frozenset(s for s, bit in zip(senders, mask_bits) if bit))
        choices.append(local)
    result=[]
    for selected in product(*choices):
        result.append({r: selected[r] for r in range(n)})
    return result
