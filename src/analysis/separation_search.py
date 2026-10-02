from __future__ import annotations
from itertools import product
from typing import Sequence
from src.abstractions.l0 import L0CountOnly
from src.abstractions.l1 import L1GatherEcho
from src.models.message import Message

def search_observation_separation(n:int=4,values:Sequence[str]=("A","B","C")):
    histories=[[Message(i,n-1,1,payloads[i],"proposal",True) for i in range(n)] for payloads in product(values,repeat=n)]
    l0=L0CountOnly(); l1=L1GatherEcho(); strict=[]; reverse=0
    for i,a in enumerate(histories):
        for b in histories[i+1:]:
            if l0.observe(a)==l0.observe(b) and l1.observe(a)!=l1.observe(b):
                strict.append((a,b))
                if len(strict)>=8: break
        if len(strict)>=8: break
    for i,a in enumerate(histories):
        for b in histories[i+1:]:
            if l1.observe(a)==l1.observe(b) and a!=b:
                reverse+=1; break
    return {"L0_to_L1":{"pairs_found":len(strict),"strict_observation_gain":bool(strict)},"L1_to_L2":{"certificate_collisions_found":reverse,"strictness_requires_richer_L1_or_problem":True}}
