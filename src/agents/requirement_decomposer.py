from __future__ import annotations
import os
import json
import hashlib
from typing import Dict, Any, List

from src.config.config_loader import load_runtime_config, RuntimeConfig
from src.loaders.context_loaders import load_text_dir


class RequirementDecomposer:
    def __init__(self, cfg: RuntimeConfig):
        self.cfg = cfg

    def _make_task_id(self, title: str) -> str:
        h = hashlib.sha1(title.encode("utf-8")).hexdigest()[:8]
        return f"task_{h}"

    def _extract_tasks(self, prd_docs: Dict[str, str], rd_docs: Dict[str, str]) -> List[Dict[str, Any]]:
        tasks: List[Dict[str, Any]] = []
        for fname, content in prd_docs.items():
            title = os.path.splitext(fname)[0]
            task = {
                "task_id": self._make_task_id(title),
                "title": title,
                "prd_file": fname,
                "summary": content[:1000],
                "rd_notes": rd_docs.get(fname, ""),
            }
            tasks.append(task)
        if not tasks and prd_docs:
            for i, (fname, content) in enumerate(prd_docs.items()):
                title = f"PRD_{i}"
                tasks.append({
                    "task_id": self._make_task_id(title),
                    "title": title,
                    "prd_file": fname,
                    "summary": content[:1000],
                    "rd_notes": rd_docs.get(fname, ""),
                })
        return tasks

    def run(self, prd_dir: str, rd_dir: str, eval_dir: str) -> List[Dict[str, Any]]:
        prd_docs = load_text_dir(prd_dir)
        rd_docs = load_text_dir(rd_dir)

        tasks = self._extract_tasks(prd_docs, rd_docs)

        # map evaluation files by heuristic: same stem name or all
        eval_files = [f for f in os.listdir(eval_dir) if f.lower().endswith((".xlsx", ".xlsm", ".xls"))] if os.path.isdir(eval_dir) else []
        for t in tasks:
            stem = t["prd_file"].rsplit(".", 1)[0]
            matched = [e for e in eval_files if e.rsplit(".", 1)[0] == stem]
            t["evaluation_files"] = matched or eval_files
        return tasks