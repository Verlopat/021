"""Communication-closed synchronous round engine."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from src.abstractions.l1 import process_key
from src.crypto.auth import sign
from src.models.message import OMIT, Message

Adversary = Callable[[int, int, int, dict[int, Any]], Any]


@dataclass
class RunResult:
    decisions: dict[int, Any]
    trace: list[dict] = field(default_factory=list)
    messages: int = 0
    bytes: int = 0
    rounds: int = 0
    certificate_entries: int = 0


def _signed(sender: int, receiver: int, r: int, value: Any, bad_signature: bool = False) -> Message:
    sig = sign(process_key(sender), sender, r, value, "msg")
    if bad_signature:
        sig = "0" * len(sig)
    return Message(sender, receiver, r, value, "msg", True, (), sig)


def run_execution(protocol, abstraction, n: int, byzantine: Sequence[int], inputs: dict[int, Any],
                  adversary: Adversary, *, record_trace: bool = False) -> RunResult:
    byz = sorted(byzantine)
    honest = [p for p in range(n) if p not in set(byz)]
    states = {p: protocol.init(p, inputs[p]) for p in honest}
    out = RunResult(decisions={})
    for r in range(1, protocol.rounds + 1):
        outgoing = {p: protocol.message(p, states[p], r) for p in honest}
        new_states = {}
        for q in honest:
            delivered = [_signed(p, q, r, outgoing[p]) for p in honest]
            for b in byz:
                v = adversary(r, b, q, outgoing)
                if v is not OMIT:
                    delivered.append(_signed(b, q, r, v))
            obs = abstraction.observe(delivered)
            if hasattr(obs, "certificate"):
                out.certificate_entries += len(obs.certificate)
            new_states[q] = protocol.transition(q, states[q], r, obs)
            out.messages += len(delivered)
            out.bytes += sum(len(json.dumps(m.value, default=str)) for m in delivered)
            if record_trace:
                out.trace.extend({"round": r, "sender": m.sender, "receiver": m.receiver,
                                  "value": m.value, "byzantine": m.sender in byz} for m in delivered)
        states = new_states
    out.rounds = protocol.rounds
    out.decisions = {p: protocol.decide(p, states[p]) for p in honest}
    return out
