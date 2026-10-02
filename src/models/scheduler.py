from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable,Sequence
from .message import Message

@dataclass(frozen=True,slots=True)
class HeardOfRound:
    round_id:int
    receiver:int
    senders:frozenset[int]

@dataclass
class RoundScheduler:
    allow_omission:bool=False
    allow_delay:bool=False
    delayed:list[Message]|None=None
    def deliver(self,messages:Sequence[Message],receiver:int,round_id:int,heard_of:Iterable[int]|None=None)->list[Message]:
        selected=set(heard_of) if heard_of is not None else {m.sender for m in messages if m.receiver==receiver and m.round==round_id}
        out=[m for m in messages if m.receiver==receiver and m.round==round_id and m.sender in selected]
        if self.allow_omission and out:
            out=out[:-1]
        if self.allow_delay:
            self.delayed=(self.delayed or [])+[m for m in messages if m.receiver==receiver and m.round==round_id and m.sender not in selected]
        return sorted(out,key=lambda m:(m.sender,m.kind,repr(m.value)))
