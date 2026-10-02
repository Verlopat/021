from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, asdict
from typing import Sequence, Any

from src.models.message import Message
from .base import CommunicationAbstraction


@dataclass(frozen=True, slots=True)
class CertificateEntry:
    sender: int
    value: Any
    authenticated: bool


@dataclass(frozen=True, slots=True)
class L1Observation:
    counts: tuple[tuple[str, int], ...]
    certificate: tuple[CertificateEntry, ...]

    def to_dict(self) -> dict:
        return {
            "counts": [list(x) for x in self.counts],
            "certificate": [asdict(x) for x in self.certificate],
        }


class L1GatherEcho(CommunicationAbstraction):
    level = "L1"

    def certificate(self, messages: Sequence[Message]) -> tuple[CertificateEntry, ...]:
        entries = {
            (m.sender, repr(m.value), m.authenticated): CertificateEntry(
                sender=m.sender, value=m.value, authenticated=m.authenticated
            )
            for m in messages
            if m.kind == "proposal"
        }
        return tuple(sorted(entries.values(), key=lambda e: (e.sender, repr(e.value), e.authenticated)))

    def observe(self, messages: Sequence[Message]) -> L1Observation:
        return self.canonicalize(messages)

    def canonicalize(self, messages: Sequence[Message]) -> L1Observation:
        counts = tuple(sorted(Counter(m.label for m in messages).items()))
        return L1Observation(counts, self.certificate(messages))


L1 = L1GatherEcho
