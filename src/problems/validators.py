from __future__ import annotations

from math import dist
from typing import Any, Iterable, Sequence


def all_equal(values: Iterable[Any]) -> bool:
    return len(set(map(repr, values))) <= 1


def majority(values: Iterable[Any]) -> Any:
    values = list(values)
    if not values:
        return None
    counts: dict[Any, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], repr(kv[0])))[0][0]


def vector_diameter(values: Iterable[tuple[float, ...]]) -> float:
    vals = list(values)
    if len(vals) < 2:
        return 0.0
    return max(dist(a, b) for i, a in enumerate(vals) for b in vals[i + 1:])


def in_convex_hull(point: Sequence[float], points: Sequence[Sequence[float]], tol: float = 1e-9) -> bool:
    if not points:
        return False
    d = len(point)
    if d == 1:
        xs = [p[0] for p in points]
        return min(xs) - tol <= point[0] <= max(xs) + tol
    import numpy as np
    from scipy.optimize import linprog
    P = np.array(points, dtype=float).T
    A_eq = np.vstack([P, np.ones((1, P.shape[1]))])
    b_eq = np.concatenate([np.array(point, dtype=float), [1.0]])
    res = linprog(np.zeros(P.shape[1]), A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method="highs")
    return bool(res.success)
