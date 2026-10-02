from __future__ import annotations
from collections import defaultdict
from typing import Any

def summarize_matrix(result:dict[str,Any])->dict[str,Any]:
    summary=defaultdict(dict)
    for row in result.get("rows",[]):
        summary[(row["problem"],row["abstraction"])][f'n={row["n"]},f={row["f"]}']=row["status"]
    return {"entries":{f"{p}::{a}":v for (p,a),v in summary.items()}}
