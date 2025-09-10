from __future__ import annotations
import os
import json
from typing import Dict, Any, List

from src.config.config_loader import RuntimeConfig
from src.tools.llm_tools import LLMTools, LLMConfig


class SynthesisPipeline:
    def __init__(self, cfg: RuntimeConfig, optimized_dir: str):
        self.cfg = cfg
        self.optimized_dir = optimized_dir
        self.llm = LLMTools(LLMConfig(default_model=cfg.default_model, temperature=cfg.temperature, max_tokens=cfg.max_tokens))

    def _load_optimized_prompts(self) -> Dict[str, str]:
        prompts: Dict[str, str] = {}
        if not os.path.isdir(self.optimized_dir):
            return prompts
        for task_id in os.listdir(self.optimized_dir):
            pt = os.path.join(self.optimized_dir, task_id, "prompt_template.txt")
            if os.path.isfile(pt):
                with open(pt, "r", encoding="utf-8") as f:
                    prompts[task_id] = f.read()
        return prompts

    def run(self, input_path: str, output_path: str) -> int:
        prompts = self._load_optimized_prompts()
        written = 0
        with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                task_id = obj.get("task_id") or next(iter(prompts.keys()), None)
                template = prompts.get(task_id)
                if not template:
                    continue
                content = obj.get("input") or obj.get("query") or obj.get("text") or ""
                prompt = template.replace("{{input}}", str(content))
                output = self.llm.chat([{"role": "user", "content": prompt}])
                # refinement passes
                for _ in range(max(0, self.cfg.refinement_passes - 1)):
                    prompt_refine = f"请在不改变事实的前提下润色以下回答，使其更清晰：\n{output}"
                    output = self.llm.chat([{"role": "user", "content": prompt_refine}])
                rec = {
                    "task_id": task_id,
                    "input": content,
                    "prompt": prompt,
                    "response": output,
                }
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                written += 1
        return written