from __future__ import annotations
from typing import Any
from src.abstractions.registry import make_abstraction
from src.models.message import Message

def _pairs():
    return {
        "L0-blind_vs_L0":([Message(0,3,1,"A"),Message(1,3,1,"A")],[Message(0,3,1,"B"),Message(1,3,1,"B")]),
        "L0_vs_L1":([Message(0,3,1,"A"),Message(1,3,1,"B")],[Message(0,3,1,"B"),Message(1,3,1,"A")]),
        "L1_vs_L2":([Message(0,3,1,"A",metadata=(("proof","x"),))],[Message(0,3,1,"A",metadata=(("proof","y"),))]),
    }

def build_pair_witness()->dict[str,Any]:
    levels=("L0-blind","L0","L1","L2"); result={}
    for name,(left,right) in _pairs().items():
        result[name]={lvl:make_abstraction(lvl).observe(left)==make_abstraction(lvl).observe(right) for lvl in levels}
    return {"description":"True means the level cannot distinguish the pair","pairs":result,
            "strict_chain":(result["L0-blind_vs_L0"]["L0-blind"] and not result["L0-blind_vs_L0"]["L0"]
                            and result["L0_vs_L1"]["L0"] and not result["L0_vs_L1"]["L1"]
                            and result["L1_vs_L2"]["L1"] and not result["L1_vs_L2"]["L2"])}

def check_l0_factorization()->dict[str,Any]:
    from src.protocols.round_protocols import CountCrusader
    proto=CountCrusader(4,1,("A","B")); abstraction=make_abstraction("L0")
    left=[Message(0,3,1,"A"),Message(1,3,1,"A"),Message(2,3,1,"A"),Message(3,3,1,"B")]
    right=[Message(3,3,1,"A"),Message(2,3,1,"A"),Message(1,3,1,"A"),Message(0,3,1,"B")]
    state=proto.init(3,"A")
    same_obs=abstraction.observe(left)==abstraction.observe(right)
    same_t=proto.transition(3,state,1,abstraction.observe(left))==proto.transition(3,state,1,abstraction.observe(right))
    return {"property":"A0(M1)=A0(M2) implies equal transition states","same_observation":same_obs,
            "same_transition":same_t,"passed":(not same_obs) or same_t}
