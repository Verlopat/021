"""Named Byzantine strategies."""
from __future__ import annotations
from typing import Callable
from src.models.message import OMIT

def _honest_rank(q, outgoing): return sorted(outgoing).index(q)

def named_strategies(protocol) -> dict[str, Callable]:
    def alpha(r): return list(protocol.byzantine_alphabet(r))
    def split(r,b,q,out):
        a=alpha(r); return a[0] if _honest_rank(q,out)<(len(out)+1)//2 else a[-1]
    def split_rev(r,b,q,out):
        a=alpha(r); return a[-1] if _honest_rank(q,out)<(len(out)+1)//2 else a[0]
    def mirror(r,b,q,out):
        v=out[q]; a=alpha(r); return v if v in a else a[0]
    def anti_mirror(r,b,q,out):
        a=alpha(r); others=[v for v in a if v!=out[q]]; return others[0] if others else a[0]
    def omit(r,b,q,out): return OMIT
    def late_flip(r,b,q,out): return split(r,b,q,out) if r==protocol.rounds else mirror(r,b,q,out)
    strategies={"split":split,"split-reversed":split_rev,"mirror":mirror,"anti-mirror":anti_mirror,"omit":omit,"late-flip":late_flip}
    for i in range(len(alpha(1))):
        strategies[f"constant-{i}"]=(lambda i: lambda r,b,q,out: alpha(r)[min(i,len(alpha(r))-1)])(i)
    return strategies
