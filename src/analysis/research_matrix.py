from __future__ import annotations

from typing import Any

PROBLEMS = (
    "Crusader Agreement",
    "Connected Consensus",
    "Multidimensional Approximate Agreement",
    "Multivalued Byzantine Agreement",
    "Set Agreement",
    "Vector Agreement",
)

LEVELS = ("L0", "L1", "L2")


def build_research_matrix() -> dict[str, Any]:
    return {
        "scope": "candidate resilience characterization; cells are research status, not established thresholds",
        "target_boundary": "n > 3f",
        "matrix": [
            {
                "problem": problem,
                "L0": "TARGET",
                "L1": "TARGET",
                "L2": "TARGET",
                "separation_target": (
                    "L0/L1" if problem in ("Crusader Agreement", "Connected Consensus")
                    else "L1/L2" if problem in ("Multidimensional Approximate Agreement", "Multivalued Byzantine Agreement")
                    else "exploratory"
                ),
            }
            for problem in PROBLEMS
        ],
        "rule": "A cell may be promoted from TARGET only after a constructive protocol, impossibility proof, or exact literature-matched result is attached.",
    }
