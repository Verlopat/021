from __future__ import annotations

from math import dist
from typing import Any, Iterable


def all_equal(values: Iterable[Any]) -> bool:
    values=list(values)
    return len(set(map(repr, values))) <= 1


def majority(values: Iterable[Any]) -> Any:
    values=list(values)
    if not values:
        return None
    counts={}
    for v in values:
        counts[v]=counts.get(v,0)+1
    return sorted(counts.items(), key=lambda kv:(-kv[1], repr(kv[0])))[0][0]


def vector_diameter(values: Iterable[tuple[float, ...]]) -> float:
    vals=list(values)
    if len(vals)<2:
        return 0.0
    return max(dist(a,b) for i,a in enumerate(vals) for b in vals[i+1:])
