"""Evidence-labelled resilience matrix; OPEN remains OPEN until proved or literature-matched."""
from __future__ import annotations
from typing import Any

MATRIX=[
{"problem":"Crusader Agreement (= Connected Consensus R=1)","L0-blind":"impossible for every f, even f=0 (PROOF)","L0":"n > 3f: count-crusader, 1 round (PROOF, MC)","L1":"n > 3f (inherits L0)","L2":"n > 3f (inherits L1)","separation":"none"},
{"problem":"Connected Consensus R=2","L0-blind":"impossible, f=0","L0":"n > 3f: count-connected, 2 rounds (PROOF, MC)","L1":"n > 3f","L2":"n > 3f","separation":"none"},
{"problem":"Connected Consensus, general R","L0-blind":"impossible, f=0","L0":"OPEN for R >= 3","L1":"n > 3f via phase king (PROOF, MC)","L2":"n > 3f; impossibility at n <= 3f requires matched literature","separation":"candidate L0/L1"},
{"problem":"Multivalued Byzantine Agreement","L0-blind":"impossible for f=0 (LEAN)","L0":"OPEN; homonyms result must be matched exactly","L1":"n > 3f: phase king (PROOF, MC)","L2":"n > 3f; n <= 3f via classical oral-messages results","separation":"main L0/L1 candidate"},
{"problem":"Approximate Agreement, d=1","L0-blind":"impossible, f=0","L0":"n > 3f: trimmed midpoint (PROOF, MC)","L1":"n > 3f","L2":"n > 3f","separation":"none"},
{"problem":"Approximate Agreement, d >= 2","L0-blind":"impossible, f=0","L0":"OPEN; safe-area protocol not implemented","L1":"OPEN / expected same bound","L2":"literature-backed bound needs model mapping","separation":"none expected"},
{"problem":"Set Agreement / Vector Agreement","L0-blind":"OPEN","L0":"OPEN","L1":"OPEN","L2":"OPEN","separation":"exploratory"}]
L1_L2_NOTE=("With unrestricted (sender,kind,value) certificate entries, L1 already exposes the "
            "message content relevant to the current model, so no solvability separation is expected. "
            "A useful L1/L2 question needs bounded certificates or an explicit complexity measure.")

def build_research_matrix()->dict[str,Any]:
    return {"model":"synchronous rounds, reliable honest links, rushing adaptive adversary, authentication Model B",
            "matrix":MATRIX,"L1_vs_L2":L1_L2_NOTE}

def matrix_markdown()->str:
    cols=["problem","L0-blind","L0","L1","L2","separation"]
    lines=["| "+" | ".join(cols)+" |","|"+"---|"*len(cols)]
    for row in MATRIX: lines.append("| "+" | ".join(row[c] for c in cols)+" |")
    return "\n".join(lines)+"\n\n"+L1_L2_NOTE+"\n"
