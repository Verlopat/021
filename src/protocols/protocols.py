from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Any, Sequence
from src.abstractions.l0 import L0CountOnly
from src.abstractions.l1 import L1GatherEcho
from src.abstractions.l2 import L2FullContent
from src.models.message import Message

@dataclass(frozen=True, slots=True)
class ProtocolResult:
    decisions:dict[int,Any]
    observations:dict[int,Any]
    metadata:dict[str,Any]

class CountOnlyProtocol:
    level="L0"
    def decide(self,messages:Sequence[Message],processes:Sequence[int],domain:Sequence[Any])->ProtocolResult:
        obs={p:L0CountOnly().observe([m for m in messages if m.receiver==p]) for p in processes}
        fallback=domain[0] if domain else None
        return ProtocolResult({p:fallback for p in processes},obs,{"level":"L0","rule":"canonical-label-only"})

class CertificateProtocol:
    level="L1"
    def __init__(self,quorum:int): self.quorum=quorum
    def decide(self,messages,processes,domain)->ProtocolResult:
        abstraction=L1GatherEcho(); decisions={}; observations={}
        for p in processes:
            view=[m for m in messages if m.receiver==p]
            observations[p]=abstraction.observe(view).to_dict()
            counts=Counter(e.value for e in abstraction.certificate(view) if e.authenticated and e.value in domain)
            qualified=[(c,v) for v,c in counts.items() if c>=self.quorum]
            decisions[p]=sorted(qualified,key=lambda x:(-x[0],repr(x[1])))[0][1] if qualified else (sorted(counts,key=repr)[0] if counts else (domain[0] if domain else None))
        return ProtocolResult(decisions,observations,{"level":"L1","quorum":self.quorum})

class FullContentProtocol:
    level="L2"
    def decide(self,messages,processes,domain)->ProtocolResult:
        abstraction=L2FullContent(); decisions={}; observations={}
        for p in processes:
            view=[m for m in messages if m.receiver==p]
            observations[p]=[m.to_dict() for m in abstraction.observe(view)]
            vals=[m.value for m in view if m.kind=="proposal" and m.value in domain]
            decisions[p]=Counter(vals).most_common(1)[0][0] if vals else (domain[0] if domain else None)
        return ProtocolResult(decisions,observations,{"level":"L2","rule":"majority/full-content"})

def protocol_for(level:str,n:int,f:int):
    if level=="L0": return CountOnlyProtocol()
    if level=="L1": return CertificateProtocol(max(1,2*f+1))
    if level=="L2": return FullContentProtocol()
    raise ValueError(level)
