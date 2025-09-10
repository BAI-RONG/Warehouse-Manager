from __future__ import annotations
import os
from typing import List, Dict, Any
import pandas as pd

REQUIRED_HINTS = [
    ("input", ["input", "query", "question", "prompt"]),
    ("expected", ["expected", "answer", "label", "target"]),
]


def _infer_column(df: pd.DataFrame, candidates: List[str]) -> str:
    lower_cols = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lower_cols:
            return lower_cols[c]
    for c in candidates:
        for col in df.columns:
            if c in col.lower():
                return col
    return df.columns[0]


def load_eval_excel(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    df = pd.read_excel(path)
    input_col = _infer_column(df, REQUIRED_HINTS[0][1])
    expected_col = _infer_column(df, REQUIRED_HINTS[1][1])

    extras = [c for c in df.columns if c not in {input_col, expected_col}]

    rows: List[Dict[str, Any]] = []
    for _, r in df.iterrows():
        item = {
            "input": r.get(input_col, ""),
            "expected": r.get(expected_col, ""),
            "meta": {k: r.get(k, None) for k in extras},
        }
        rows.append(item)
    return rows