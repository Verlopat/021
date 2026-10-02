from __future__ import annotations

from collections import Counter
from typing import Sequence

from src.models.message import Message
from .base import CommunicationAbstraction


class L0Blind(CommunicationAbstraction):
    """Heard-Of only: counts of protocol-fixed kinds, never values."""
    level = "L0-blind"

    def observe(self, messages: Sequence[Message]):
        return self.canonicalize(messages)

    def canonicalize(self, messages: Sequence[Message]):
        return tuple(sorted(Counter(m.kind for m in messages).items()))


class L0CountOnly(CommunicationAbstraction):
    """Anonymous counting: multiset of (kind, value), sender identity erased."""
    level = "L0"

    def observe(self, messages: Sequence[Message]):
        return self.canonicalize(messages)

    def canonicalize(self, messages: Sequence[Message]):
        return tuple(sorted(Counter((m.kind, m.value) for m in messages).items(), key=repr))


def count_of(observation, value, kind: str = "msg") -> int:
    for (k, v), c in observation:
        if k == kind and v == value:
            return c
    return 0


L0 = L0CountOnly
