from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Sequence
from src.models.message import Message

@dataclass(frozen=True, slots=True)
class ByzantineAdversary:
    faulty:frozenset[int]
    adaptive:bool=False
    def validate(self,n:int,f:int)->None:
        if any(p<0 or p>=n for p in self.faulty): raise ValueError("faulty process outside system")
        if len(self.faulty)>f: raise ValueError("fault bound exceeded")

    def equivocate(self,sender:int,receivers:Iterable[int],values:Sequence[str],round_id:int=1)->list[Message]:
        if sender not in self.faulty: raise ValueError("sender is not Byzantine")
        values=tuple(values)
        if not values: raise ValueError("values cannot be empty")
        return [Message(sender,r,round_id,values[i%len(values)],"proposal",True) for i,r in enumerate(receivers)]

    def omit(self,messages:Sequence[Message],receiver:int,sender:int)->list[Message]:
        return [m for m in messages if not (m.sender==sender and m.receiver==receiver)]

    def delay(self,messages:Sequence[Message],receiver:int,sender:int,new_round:int)->list[Message]:
        return [Message(m.sender,m.receiver,new_round if m.sender==sender and m.receiver==receiver else m.round,m.value,m.kind,m.authenticated,m.metadata) for m in messages]

def adversarial_trace(n:int,f:int,byzantine:Iterable[int],round_id:int=1)->list[Message]:
    bad=set(byzantine); result=[]
    for sender in range(n):
        for receiver in range(n):
            if sender in bad and sender!=receiver:
                value="A" if receiver%2==0 else "C"
            else:
                value="B"
            result.append(Message(sender,receiver,round_id,value,"proposal",True))
    return result
