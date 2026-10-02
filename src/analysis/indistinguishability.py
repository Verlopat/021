from __future__ import annotations

import json
from typing import Any

from src.abstractions.l0 import L0CountOnly
from src.abstractions.l1 import L1GatherEcho
from src.abstractions.l2 import L2FullContent
from src.models.message import Message


def build_pair_witness() -> dict[str, Any]:
    """Finite witness: same L0 label multiset, different L1 certificates."""
    m_a = [
        Message(0, 2, 1, "A"),
        Message(1, 2, 1, "A"),
        Message(2, 2, 1, "B"),
    ]
    m_c = [
        Message(0, 2, 1, "C"),
        Message(1, 2, 1, "C"),
        Message(2, 2, 1, "B"),
    ]
    l0, l1, l2 = L0CountOnly(), L1GatherEcho(), L2FullContent()
    trace = [json.dumps({"execution": "E_A", "message": m.to_dict()}, sort_keys=True) for m in m_a]
    trace += [json.dumps({"execution": "E_C", "message": m.to_dict()}, sort_keys=True) for m in m_c]
    return {
        "description": "Finite communication-information separation witness",
        "E_A": {"L0": l0.observe(m_a), "L1": l1.observe(m_a).to_dict(), "L2_size": len(l2.observe(m_a))},
        "E_C": {"L0": l0.observe(m_c), "L1": l1.observe(m_c).to_dict(), "L2_size": len(l2.observe(m_c))},
        "claims": {
            "same_L0": l0.observe(m_a) == l0.observe(m_c),
            "different_L1": l1.observe(m_a) != l1.observe(m_c),
            "different_L2": l2.observe(m_a) != l2.observe(m_c),
        },
        "execution_trace": trace,
    }


def check_l0_factorization() -> dict[str, Any]:
    """Check the operational definition: an L0 transition depends only on A0."""
    abstraction = L0CountOnly()
    histories = [
        [Message(0, 2, 1, "A")],
        [Message(0, 2, 1, "C")],
        [Message(0, 2, 1, "A"), Message(1, 2, 1, "C")],
        [Message(0, 2, 1, "B"), Message(1, 2, 1, "C")],
    ]

    def transition(state: str, msgs: list[Message]) -> str:
        labels = abstraction.observe(msgs)
        return f"{state}|{labels}"

    violations = []
    for i, left in enumerate(histories):
        for j, right in enumerate(histories):
            if abstraction.observe(left) == abstraction.observe(right) and transition("s", left) != transition("s", right):
                violations.append((i, j))
    return {
        "property": "A0(M1)=A0(M2) implies T(S,M1)=T(S,M2) for the canonical transition",
        "passed": not violations,
        "violations": violations,
    }
