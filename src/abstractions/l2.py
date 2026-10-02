from __future__ import annotations

from typing import Sequence

from src.models.message import Message
from .base import CommunicationAbstraction


class L2FullContent(CommunicationAbstraction):
    level = "L2"

    def observe(self, messages: Sequence[Message]) -> tuple[Message, ...]:
        return self.canonicalize(messages)

    def canonicalize(self, messages: Sequence[Message]) -> tuple[Message, ...]:
        return tuple(sorted(messages, key=lambda m: (m.sender, m.receiver, m.round, m.kind, repr(m.value), m.authenticated)))


L2 = L2FullContent
