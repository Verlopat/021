"""Protocols whose transitions receive abstraction observations only."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from src.abstractions.l0 import count_of
from src.models.message import BOT


def _threshold_value(obs, candidates, threshold):
    hits = sorted(((count_of(obs, v), repr(v), v) for v in candidates
                   if count_of(obs, v) >= threshold), reverse=True)
    return hits[0][2] if hits else None


@dataclass(frozen=True)
class OwnInputProtocol:
    n: int
    f: int
    values: tuple
    level: str = "L0-blind"
    rounds: int = 1
    name: str = "own-input (L0-blind)"
    output: str = "value"
    R: int = 1
    def init(self, pid, x): return {"x": x}
    def message(self, pid, s, r): return "ping"
    def transition(self, pid, s, r, obs): return s
    def decide(self, pid, s): return (s["x"], self.R) if self.output == "vertex" else s["x"]
    def byzantine_alphabet(self, r): return ["ping"]


@dataclass(frozen=True)
class CountCrusader:
    n: int
    f: int
    values: tuple
    level: str = "L0"
    rounds: int = 1
    name: str = "count-crusader (L0)"
    def init(self, pid, x): return {"x": x, "y": None}
    def message(self, pid, s, r): return s["x"]
    def transition(self, pid, s, r, obs):
        v = _threshold_value(obs, self.values, self.n - self.f)
        return {**s, "y": BOT if v is None else v}
    def decide(self, pid, s): return s["y"]
    def byzantine_alphabet(self, r): return list(self.values)


@dataclass(frozen=True)
class CountConnectedConsensus:
    n: int
    f: int
    values: tuple
    R: int = 1
    level: str = "L0"
    name: str = "count-connected-consensus (L0)"
    def __post_init__(self):
        if self.R not in (1, 2):
            raise ValueError("count protocol implemented for R in {1,2}")
    @property
    def rounds(self): return self.R
    def init(self, pid, x): return {"x": x, "y": None, "out": None}
    def message(self, pid, s, r): return s["x"] if r == 1 else s["y"]
    def transition(self, pid, s, r, obs):
        if r == 1:
            v = _threshold_value(obs, self.values, self.n - self.f)
            y = BOT if v is None else v
            return {**s, "y": y, "out": (BOT, 0) if y == BOT else (y, 1)}
        w = _threshold_value(obs, self.values, self.n - self.f)
        if w is not None:
            return {**s, "out": (w, 2)}
        w = _threshold_value(obs, self.values, self.f + 1)
        return {**s, "out": (w, 1) if w is not None else (BOT, 0)}
    def decide(self, pid, s): return s["out"]
    def byzantine_alphabet(self, r): return list(self.values) + ([BOT] if r == 2 else [])


@dataclass(frozen=True)
class PhaseKing:
    n: int
    f: int
    values: tuple
    level: str = "L1"
    name: str = "phase-king (L1)"
    vertex_R: int | None = None
    @property
    def rounds(self): return 3 * (self.f + 1)
    def init(self, pid, x): return {"v": x, "p": None, "strong": False}
    def message(self, pid, s, r):
        step = (r - 1) % 3
        return s["p"] if step == 1 else s["v"]
    def transition(self, pid, s, r, obs):
        phase, step = divmod(r - 1, 3)
        counts = obs.counts
        if step == 0:
            w = _threshold_value(counts, self.values, self.n - self.f)
            return {**s, "p": BOT if w is None else w, "strong": False}
        if step == 1:
            w = _threshold_value(counts, self.values, self.f + 1)
            if w is None:
                return {**s, "strong": False}
            return {**s, "v": w, "strong": count_of(counts, w) >= self.n - self.f}
        if s["strong"]:
            return s
        king_value = obs.value_from(phase)
        return {**s, "v": king_value} if king_value in self.values else s
    def decide(self, pid, s): return (s["v"], self.vertex_R) if self.vertex_R else s["v"]
    def byzantine_alphabet(self, r):
        return list(self.values) + ([BOT] if (r - 1) % 3 == 1 else [])


@dataclass(frozen=True)
class TrimmedMidpointApproximate:
    n: int
    f: int
    values: tuple
    epsilon: float = 0.25
    level: str = "L0"
    name: str = "trimmed-midpoint (L0)"
    @property
    def rounds(self):
        lo = min(v[0] for v in self.values); hi = max(v[0] for v in self.values)
        return max(1, math.ceil(math.log2(max(hi - lo, 1e-12) / self.epsilon)))
    def init(self, pid, x): return {"x": float(x[0])}
    def message(self, pid, s, r): return s["x"]
    def transition(self, pid, s, r, obs):
        received = sorted(v for (kind, v), c in obs for _ in range(c)
                          if isinstance(v, (int, float)))
        kept = received[self.f: len(received) - self.f] or received
        return {"x": (kept[0] + kept[-1]) / 2}
    def decide(self, pid, s): return (s["x"],)
    def byzantine_alphabet(self, r):
        lo = min(v[0] for v in self.values); hi = max(v[0] for v in self.values)
        return [lo - 10.0, lo, (lo + hi) / 2, hi, hi + 10.0]
