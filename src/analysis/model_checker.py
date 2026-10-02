"""Bounded model checker for closed-round protocols."""
from __future__ import annotations
import math, random
from itertools import combinations, product
from typing import Any, Sequence
from src.abstractions.registry import make_abstraction
from src.adversary.strategies import named_strategies
from src.models.message import OMIT
from src.simulation.rounds import run_execution

def _slots(protocol,byz,honest):
    return [(r,b,q) for r in range(1,protocol.rounds+1) for b in byz for q in honest]

def _alphabets(protocol,slots):
    return [list(protocol.byzantine_alphabet(r))+[OMIT] for (r,_,_) in slots]

def _table_adversary(table):
    return lambda r,b,q,outgoing: table[(r,b,q)]

def space_size(protocol,n,f,input_domain:Sequence[Any])->int:
    per=1
    for r in range(1,protocol.rounds+1):
        per *= (len(protocol.byzantine_alphabet(r))+1)**(f*(n-f))
    return math.comb(n,f)*len(input_domain)**(n-f)*per

def _avg(stats):
    e=max(1,stats["executions"])
    return {"executions":stats["executions"],"messages_per_execution":stats["messages"]/e,
            "bytes_per_execution":stats["bytes"]/e,
            "certificate_entries_per_execution":stats["certificate_entries"]/e}

def check_protocol(problem,protocol,n:int,f:int,input_domain:Sequence[Any],*,auth="B",max_exec=20000,seed=0):
    abstraction=make_abstraction(protocol.level,auth)
    total=space_size(protocol,n,f,input_domain)
    exhaustive=total<=max_exec
    rng=random.Random(seed)
    stats={"messages":0,"bytes":0,"certificate_entries":0,"executions":0}
    base={"problem":problem.name,"protocol":protocol.name,"abstraction":protocol.level,"auth":auth,
          "n":n,"f":f,"n_gt_3f":n>3*f,"rounds":protocol.rounds,"space_size":total,
          "mode":"exhaustive" if exhaustive else "sampled","seed":seed}

    fault_sets=list(combinations(range(n),f))
    def executions():
        if exhaustive:
            for byz in fault_sets:
                honest=[p for p in range(n) if p not in byz]
                slots=_slots(protocol,byz,honest)
                for ins in product(input_domain,repeat=len(honest)):
                    inputs=dict(zip(honest,ins))
                    for choice in product(*_alphabets(protocol,slots)):
                        yield byz,inputs,dict(zip(slots,choice))
        else:
            strategies=named_strategies(protocol)
            for byz in fault_sets:
                honest=[p for p in range(n) if p not in byz]
                for ins in product(input_domain,repeat=len(honest)):
                    inputs=dict(zip(honest,ins))
                    for strat in strategies.values():
                        yield byz,inputs,strat
            for _ in range(max_exec):
                byz=rng.choice(fault_sets)
                honest=[p for p in range(n) if p not in byz]
                slots=_slots(protocol,byz,honest)
                inputs={p:rng.choice(list(input_domain)) for p in honest}
                yield byz,inputs,{s:rng.choice(a) for s,a in zip(slots,_alphabets(protocol,slots))}

    for byz,inputs,table in executions():
        adversary=table if callable(table) else _table_adversary(table)
        res=run_execution(protocol,abstraction,n,byz,inputs,adversary)
        stats["executions"]+=1; stats["messages"]+=res.messages; stats["bytes"]+=res.bytes
        stats["certificate_entries"]+=res.certificate_entries
        verdict=problem.check(res.decisions,inputs,set(inputs))
        if not verdict.passed:
            replay=run_execution(protocol,abstraction,n,byz,inputs,adversary,record_trace=True)
            if callable(table):
                table={(t["round"],t["sender"],t["receiver"]):t["value"] for t in replay.trace if t["byzantine"]}
            return {**base,**_avg(stats),"status":"COUNTEREXAMPLE_FOUND",
                    "counterexample":{"byzantine":list(byz),"honest_inputs":inputs,"decisions":res.decisions,
                    "violated":[k for k in ("agreement","validity","termination") if not getattr(verdict,k)],
                    "adversary_table":[[r,b,q,v] for (r,b,q),v in table.items()],
                    "trace":replay.trace}}
    return {**base,**_avg(stats),"status":"VERIFIED_EXHAUSTIVE" if exhaustive else "NO_COUNTEREXAMPLE_SAMPLED"}

def resilience_boundary(problem,protocol_factory,f_values,input_domain,*,auth="B",max_exec=20000,seed=0):
    rows=[]
    for f in f_values:
        observed=None
        for n in range(f+1,3*f+3):
            row=check_protocol(problem,protocol_factory(n,f),n,f,input_domain,auth=auth,max_exec=max_exec,seed=seed)
            if row["status"]!="COUNTEREXAMPLE_FOUND":
                observed=n; break
        rows.append({"problem":problem.name,"f":f,"observed_n_min":observed,
                     "theoretical_n_min":3*f+1,"matches":observed==3*f+1})
    return rows
