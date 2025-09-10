from __future__ import annotations
import os
from typing import Dict, Any


def load_text_dir(path: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    if not os.path.isdir(path):
        return data
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if os.path.isfile(full) and any(name.lower().endswith(ext) for ext in [".txt", ".md", ".markdown"]):
            with open(full, "r", encoding="utf-8") as f:
                data[name] = f.read()
    return data


def load_prompts_dir(path: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    if not os.path.isdir(path):
        return data
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if os.path.isfile(full) and any(name.lower().endswith(ext) for ext in [".txt", ".md", ".yaml", ".yml", ".json"]):
            with open(full, "r", encoding="utf-8") as f:
                data[name] = f.read()
    return data