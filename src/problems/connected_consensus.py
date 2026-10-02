"""Finite connected-domain agreement model.

This module intentionally uses a graph-connected specification as an executable
research model; it is not presented as a proof that every literature definition
of connected consensus has the same thresholds.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ConnectedDomain:
    vertices: tuple[str, ...] = ("A", "B", "C")
    edges: tuple[tuple[str, str], ...] = (("A", "B"), ("B", "C"))

    def __post_init__(self) -> None:
        v = set(self.vertices)
        if any(a not in v or b not in v for a, b in self.edges):
            raise ValueError("edge references unknown vertex")

    def connected_hull(self, values: Iterable[str]) -> set[str]:
        values = set(values)
        if not values:
            return set(self.vertices)
        if not values.issubset(set(self.vertices)):
            raise ValueError("value outside connected domain")
        index = {v: i for i, v in enumerate(self.vertices)}
        lo, hi = min(index[v] for v in values), max(index[v] for v in values)
        return set(self.vertices[lo : hi + 1])


@dataclass(frozen=True, slots=True)
class ConnectedConsensusSpec:
    domain: ConnectedDomain = ConnectedDomain()

    def validity(self, decision: str, correct_inputs: Iterable[str]) -> bool:
        return decision in self.domain.connected_hull(correct_inputs)

    def agreement(self, decisions: Iterable[str]) -> bool:
        decisions = list(decisions)
        return len(set(decisions)) <= 1

    def all_same_validity(self, decision: str, value: str) -> bool:
        return decision == value


@dataclass(frozen=True, slots=True)
class CertificateDecisionRule:
    quorum: int

    def decide(self, certificate_values: dict[int, str], domain: ConnectedDomain) -> str:
        counts: dict[str, int] = {}
        for value in certificate_values.values():
            if value not in domain.vertices:
                continue
            counts[value] = counts.get(value, 0) + 1
        qualified = sorted(((-count, value) for value, count in counts.items() if count >= self.quorum))
        if qualified:
            return qualified[0][1]
        if counts:
            ordered = sorted(counts)
            return ordered[len(ordered) // 2]
        return domain.vertices[0]
