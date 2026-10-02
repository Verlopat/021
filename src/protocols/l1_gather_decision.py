from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from src.abstractions.l1 import L1GatherEcho
from src.models.message import Message
from src.problems.connected_consensus import ConnectedDomain

@dataclass(frozen=True, slots=True)
class L1GatherDecisionProtocol:
    quorum:int
    domain:ConnectedDomain=ConnectedDomain()
    def observe(self,messages:list[Message])->dict[str,Any]:
        return L1GatherEcho().observe(messages).to_dict()
    def decide(self,messages:list[Message])->str:
        cert=L1GatherEcho().certificate(messages)
        counts={}
        for e in cert:
            if e.authenticated and isinstance(e.value,str) and e.value in self.domain.vertices:
                counts[e.value]=counts.get(e.value,0)+1
        qualified=[(c,v) for v,c in counts.items() if c>=self.quorum]
        if qualified:
            return sorted(qualified,key=lambda x:(-x[0],repr(x[1])))[0][1]
        if counts:
            # Deterministic connected-domain fallback: choose the median
            # ordered value when no certificate reaches quorum.
            ordered=sorted(counts,key=repr)
            return ordered[len(ordered)//2]
        return self.domain.vertices[0]
    def run(self,messages:list[Message])->dict[str,Any]:
        return {"observation":self.observe(messages),"decision":self.decide(messages),"quorum":self.quorum,"assumption":"authenticated gather/certificate delivery"}
