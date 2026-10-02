from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Sequence

from src.crypto.auth import AuthenticationKey, verify
from src.models.message import Message
from .base import CommunicationAbstraction
from .l0 import L0CountOnly


@dataclass(frozen=True, slots=True)
class CertificateEntry:
    sender: int
    kind: str
    value: Any


@dataclass(frozen=True, slots=True)
class L1Observation:
    counts: tuple
    certificate: tuple[CertificateEntry, ...]

    def value_from(self, sender: int, kind: str = "msg"):
        for e in self.certificate:
            if e.sender == sender and e.kind == kind:
                return e.value
        return None

    def to_dict(self) -> dict:
        return {"counts": [list(x) for x in self.counts],
                "certificate": [asdict(x) for x in self.certificate]}


def process_key(pid: int) -> AuthenticationKey:
    return AuthenticationKey(pid, f"process-{pid}-secret".encode())


class L1GatherEcho(CommunicationAbstraction):
    level = "L1"

    def __init__(self, auth: str = "B"):
        if auth not in ("A", "B"):
            raise ValueError("auth must be A or B")
        self.auth = auth

    def _valid(self, m: Message) -> bool:
        if self.auth == "B":
            return m.authenticated
        return m.signature is not None and verify(
            process_key(m.sender), m.signature, m.sender, m.round, m.value, m.kind)

    def certificate(self, messages: Sequence[Message]) -> tuple[CertificateEntry, ...]:
        entries = {
            CertificateEntry(m.sender, m.kind, m.value)
            for m in messages if self._valid(m)
        }
        return tuple(sorted(entries, key=lambda e: (e.sender, e.kind, repr(e.value))))

    def observe(self, messages: Sequence[Message]) -> L1Observation:
        return self.canonicalize(messages)

    def canonicalize(self, messages: Sequence[Message]) -> L1Observation:
        return L1Observation(L0CountOnly().observe(messages), self.certificate(messages))


L1 = L1GatherEcho
