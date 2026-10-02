from __future__ import annotations
from typing import Any

def summarize_matrix(rows: list[dict[str,Any]]) -> dict[str,Any]:
    summary: dict[str,dict[str,str]]={}
    for row in rows:
        key=f'{row["problem"]}::{row["protocol"]}'
        summary.setdefault(key,{})[f'n={row["n"]},f={row["f"]}']=row["status"]
    return {"entries":summary}
