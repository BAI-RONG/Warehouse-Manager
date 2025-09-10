from __future__ import annotations
import os
import json
import random
from typing import Dict, Any, List, Optional

from src.config.config_loader import RuntimeConfig
from src.tools.llm_tools import LLMTools, LLMConfig


EDGE_CASE_MUTATIONS = [
    ("time_shift", "将描述中的时间从晚上改为早上或反之"),
    ("negation", "引入否定或双重否定以混淆判断"),
    ("role_conflict", "改变角色身份或权限边界"),
    ("format_noise", "插入表情、口语、乱码等噪声"),
]


class AdversarialAgent:
    def __init__(self, cfg: RuntimeConfig, optimized_dir: str):
        self.cfg = cfg
        self.optimized_dir = optimized_dir
        self.llm = LLMTools(LLMConfig(default_model=cfg.default_model, temperature=cfg.temperature, max_tokens=cfg.max_tokens))

    def _load_templates(self) -> Dict[str, str]:
        templates: Dict[str, str] = {}
        if not os.path.isdir(self.optimized_dir):
            return templates
        for task_id in os.listdir(self.optimized_dir):
            pt = os.path.join(self.optimized_dir, task_id, "prompt_template.txt")
            if os.path.isfile(pt):
                with open(pt, "r", encoding="utf-8") as f:
                    templates[task_id] = f.read()
        return templates

    def _mutate(self, template: str, mutation: str, description: str, seed: int) -> str:
        random.seed(seed)
        prompt = (
            f"你是攻防数据生成器。\n基础模板：\n{template}\n\n"
            f"请基于该模板进行{description}，输出一个新的模板，要求仍然保留{{input}}占位符并能触发边缘行为。"
        )
        res = self.llm.chat([{"role": "user", "content": prompt}])
        if "{{input}}" not in res:
            res = res + "\n\n输入：{{input}}"
        return res

    def run(self, task_id: Optional[str], output_path: str) -> int:
        templates = self._load_templates()
        ids = [task_id] if task_id else list(templates.keys())
        written = 0
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fout:
            for tid in ids:
                base = templates.get(tid)
                if not base:
                    continue
                for i in range(self.cfg.adversarial_num_variants):
                    m_key, m_desc = EDGE_CASE_MUTATIONS[i % len(EDGE_CASE_MUTATIONS)]
                    adv_template = self._mutate(base, m_key, m_desc, seed=i)
                    rec = {
                        "task_id": tid,
                        "mutation": m_key,
                        "prompt_template": adv_template,
                    }
                    fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    written += 1
        return written