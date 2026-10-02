from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

BOT = "<bot>"
OMIT = "<omit>"


@dataclass(frozen=True, slots=True)
class Message:
    sender: int
    receiver: int
    round: int
    value: Any
    kind: str = "msg"
    authenticated: bool = True
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    signature: str | None = None

    @property
    def label(self) -> str:
        """L0-blind label: the message kind only, payload hidden."""
        return self.kind

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["metadata"] = dict(self.metadata)
        return data
