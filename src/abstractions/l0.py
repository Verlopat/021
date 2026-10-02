from __future__ import annotations

from collections import Counter
from typing import Sequence

from src.models.message import Message
from .base import CommunicationAbstraction


class L0CountOnly(CommunicationAbstraction):
    level = "L0"

    def observe(self, messages: Sequence[Message]) -> tuple[tuple[str, int], ...]:
        return self.canonicalize(messages)

    def canonicalize(self, messages: Sequence[Message]) -> tuple[tuple[str, int], ...]:
        return tuple(sorted(Counter(m.label for m in messages).items()))


L0 = L0CountOnly
