from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from src.abstractions.l1 import L1GatherEcho
from src.models.message import Message
from src.problems.connected_consensus import ConnectedDomain, connected_consensus_decision
@dataclass(frozen=True, slots=True)
class L1GatherDecisionProtocol:
    quorum:int
    domain:ConnectedDomain=ConnectedDomain()
    def observe(self,messages:list[Message])->dict[str,Any]: return L1GatherEcho().observe(messages).to_dict()
    def decide(self,messages:list[Message])->str:
        cert=L1GatherEcho().certificate(messages); counts={}
        for e in cert:
            if e.authenticated and isinstance(e.value,str) and e.value in self.domain.vertices: counts[e.value]=counts.get(e.value,0)+1
        qualified=[(c,v) for v,c in counts.items() if c>=self.quorum]
        return sorted(qualified,key=lambda x:(-x[0],repr(x[1])))[0][1] if qualified else connected_consensus_decision(counts.keys(),self.domain)
    def run(self,messages:list[Message])->dict[str,Any]:
        return {"observation":self.observe(messages),"decision":self.decide(messages),"quorum":self.quorum,"assumption":"authenticated gather/certificate delivery"}
