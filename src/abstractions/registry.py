from __future__ import annotations

from .l0 import L0Blind, L0CountOnly
from .l1 import L1GatherEcho
from .l2 import L2FullContent

LEVELS = ("L0-blind", "L0", "L1", "L2")


def make_abstraction(level: str, auth: str = "B"):
    if level == "L0-blind":
        return L0Blind()
    if level == "L0":
        return L0CountOnly()
    if level == "L1":
        return L1GatherEcho(auth)
    if level == "L2":
        return L2FullContent()
    raise ValueError(f"unknown abstraction level {level!r}")
