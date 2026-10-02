from __future__ import annotations

from typing import Any

from src.abstractions.l0 import L0CountOnly
from src.abstractions.l1 import L1GatherEcho
from src.abstractions.l2 import L2FullContent
from src.adversary.byzantine import ByzantineAdversary, adversarial_trace
from src.models.system import Execution, SystemConfig
from src.protocols.l1_gather_decision import L1GatherDecisionProtocol


def run_reference_simulation(n: int, f: int) -> dict[str, Any]:
    status = "outside_target_optimal-boundary" if n <= 3 * f else "inside_target_n_gt_3f_boundary"
    byzantine = set(range(f))
    trace = adversarial_trace(n, f, byzantine, round_id=1)
    execution = Execution(SystemConfig(n, f), trace)
    execution.validate()

    receiver = n - 1
    view = execution.round_messages(1, receiver)
    abstractions = {
        "L0": L0CountOnly().observe(view),
        "L1": L1GatherEcho().observe(view).to_dict(),
        "L2_size": len(L2FullContent().observe(view)),
    }

    protocol = L1GatherDecisionProtocol(quorum=n - f)
    protocol_result = protocol.run([m for m in view if m.kind == "proposal"])

    adversary = ByzantineAdversary(frozenset(byzantine))
    adversary.validate(n, f)

    return {
        "configuration": {"n": n, "f": f, "byzantine": sorted(byzantine)},
        "boundary_status": status,
        "receiver": receiver,
        "view_size": len(view),
        "abstractions": abstractions,
        "l1_protocol": protocol_result,
        "trace_sample": [m.to_dict() for m in view[: min(10, len(view))]],
    }
