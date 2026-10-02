from __future__ import annotations
from dataclasses import dataclass, asdict
from itertools import combinations, product
from typing import Any, Iterable, Sequence
from src.models.message import Message
from src.protocols.protocols import protocol_for
from src.problems.base import Problem

@dataclass(frozen=True, slots=True)
class Counterexample:
    problem:str
    abstraction:str
    n:int
    f:int
    byzantine:tuple[int,...]
    correct_inputs:dict[int,Any]
    decisions:dict[int,Any]
    reason:str
    trace:tuple[dict,...]

def all_fault_sets(n:int,f:int)->Iterable[frozenset[int]]:
    return (frozenset(x) for x in combinations(range(n),f))

def enumerate_equivocating_executions(n:int,f:int,byzantine:Sequence[int],inputs:dict[int,Any],values:Sequence[Any]):
    pairs=[(b,r) for b in byzantine for r in range(n) if r!=b]
    for assignment in product(values,repeat=len(pairs)):
        table=dict(zip(pairs,assignment)); msgs=[]
        for s in range(n):
            for r in range(n):
                value=table.get((s,r),inputs[s] if s not in byzantine else values[0])
                msgs.append(Message(s,r,1,value,"proposal",True))
        yield msgs

def check_protocol(problem:Problem,level:str,n:int,f:int,values:Sequence[Any],*,max_exec:int=256):
    correct=set(range(n))
    for byz in all_fault_sets(n,f):
        for common in values:
            inputs={p:common for p in correct}
            for idx,messages in enumerate(enumerate_equivocating_executions(n,f,tuple(byz),inputs,values)):
                if idx>=max_exec: break
                result=protocol_for(level,n,f).decide(messages,range(n),values)
                check=problem.check(result.decisions,inputs,correct)
                if not check.passed:
                    ce=Counterexample(problem.name,level,n,f,tuple(sorted(byz)),inputs,result.decisions,repr(check.details),tuple(m.to_dict() for m in messages))
                    return {"status":"COUNTEREXAMPLE_FOUND","counterexample":asdict(ce),"checked_executions":idx+1}
    return {"status":"NO_COUNTEREXAMPLE_IN_FINITE_SPACE","checked_executions":max_exec,"problem":problem.name,"abstraction":level,"n":n,"f":f}

def run_matrix(problems:Sequence[Problem],max_n:int=5,max_exec:int=256)->dict:
    rows=[]
    for problem in problems:
        domain=problem.decision_domain() or ("A","B","C")
        for n in range(3,max_n+1):
            for f in range(0,min(2,n-1)+1):
                for level in ("L0","L1","L2"):
                    rows.append({**check_protocol(problem,level,n,f,domain,max_exec=max_exec),"target_boundary":n>3*f})
    return {"scope":"bounded exhaustive model checking of implemented finite protocols","rows":rows}
