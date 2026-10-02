from __future__ import annotations

from typing import Any

from src.abstractions.l0 import L0CountOnly
from src.abstractions.l1 import L1GatherEcho
from src.abstractions.l2 import L2FullContent
from src.models.message import Message


def witness_pass(n: int, f: int, abstraction: str) -> tuple[bool, str]:
    """Finite witness criterion, not a general Byzantine resilience theorem."""
    if abstraction not in {"L0", "L1", "L2"}:
        raise ValueError("unknown abstraction")
    if f < 0 or n <= f:
        return False, "invalid configuration"
    left = [Message(0, n - 1, 1, "A") for _ in range(max(1, n - f))]
    right = [Message(0, n - 1, 1, "C") for _ in range(max(1, n - f))]
    if abstraction == "L0":
        return L0CountOnly().observe(left) != L0CountOnly().observe(right), "L0 cannot distinguish payload values"
    if abstraction == "L1":
        return L1GatherEcho().observe(left) != L1GatherEcho().observe(right), "L1 certificate records sender/value"
    return L2FullContent().observe(left) != L2FullContent().observe(right), "L2 retains full content"


def run_resilience_sweep(max_n: int, seed: int = 0) -> dict[str, Any]:
    rows = []
    for n in range(4, max_n + 1):
        for f in range(1, n // 2 + 1):
            for abstraction in ("L0", "L1", "L2"):
                passed, note = witness_pass(n, f, abstraction)
                rows.append({"n": n, "f": f, "abstraction": abstraction, "witness_pass": passed, "notes": note})
    return {
        "seed": seed,
        "scope": "finite information witness only",
        "rows": rows,
        "theoretical_boundary": "n > 3f (target to be proven for selected problems)",
    }
