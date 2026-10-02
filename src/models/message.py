from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Message:
    sender: int
    receiver: int
    round: int
    value: Any
    kind: str = "proposal"
    authenticated: bool = True
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @property
    def label(self) -> str:
        """L0-visible message label; payload contents are intentionally hidden."""
        return self.kind

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["metadata"] = dict(self.metadata)
        return data
