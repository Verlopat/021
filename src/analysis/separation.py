from __future__ import annotations

from typing import Any


def build_separation_report(witness: dict[str, Any]) -> dict[str, Any]:
    claims = witness["claims"]
    return {
        "finite_witness": {
            "L0_refines_to_L1_information": bool(claims["same_L0"] and claims["different_L1"]),
            "L1_refines_to_L2_information": bool(claims["different_L1"] and claims["different_L2"]),
        },
        "theorem_status": {
            "L0_lt_L1_for_general_BA": "TARGET_NOT_PROVED",
            "L1_lt_L2_for_general_BA": "TARGET_NOT_PROVED",
            "connected_consensus_optimal_resilience": "TARGET_NOT_PROVED",
            "reason": "The package implements the abstraction definitions and finite information witnesses, but does not silently promote a toy witness into a general distributed-impossibility theorem.",
        },
        "next_formal_obligations": [
            "Specify the exact literature-compatible Connected Consensus semantics.",
            "Specify whether authentication is part of the communication abstraction or an orthogonal assumption.",
            "Prove that the selected problem is solvable at the claimed level for n > 3f.",
            "Prove impossibility at the lower level under the same scheduler and adversary assumptions.",
        ],
    }
