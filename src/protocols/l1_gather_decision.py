from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.abstractions.l1 import L1GatherEcho
from src.models.message import Message
from src.problems.connected_consensus import CertificateDecisionRule, ConnectedDomain


@dataclass(frozen=True, slots=True)
class L1GatherDecisionProtocol:
    """Reusable L1 gather + problem-specific decision rule.

    This is a protocol skeleton for the supplied research program. It assumes
    the gather layer has delivered authenticated sender/value records; it does
    not claim to implement a complete Byzantine reliable-broadcast protocol.
    """

    quorum: int
    domain: ConnectedDomain = ConnectedDomain()

    def observe(self, messages: list[Message]) -> dict[str, Any]:
        obs = L1GatherEcho().observe(messages)
        return obs.to_dict()

    def decide(self, messages: list[Message]) -> str:
        certificate = L1GatherEcho().certificate(messages)
        values = {
            entry.sender: entry.value
            for entry in certificate
            if entry.authenticated and isinstance(entry.value, str)
        }
        return CertificateDecisionRule(self.quorum).decide(values, self.domain)

    def run(self, messages: list[Message]) -> dict[str, Any]:
        return {
            "observation": self.observe(messages),
            "decision": self.decide(messages),
            "quorum": self.quorum,
            "assumption": "authenticated gather/certificate delivery",
        }
