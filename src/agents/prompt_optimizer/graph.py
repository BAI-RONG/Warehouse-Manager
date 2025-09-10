from __future__ import annotations
import os
import json
from typing import Dict, Any, List, Optional, Tuple

from src.config.config_loader import RuntimeConfig
from src.loaders.eval_excel_loader import load_eval_excel
from src.loaders.context_loaders import load_prompts_dir
from src.tools.llm_tools import LLMTools, LLMConfig


class DimensionExtractor:
    def __init__(self, llm: LLMTools):
        self.llm = llm

    def extract(self, prd: str, rd: str, prompt: str) -> Dict[str, List[str]]:
        msg = [
            {"role": "system", "content": "你是评价维度抽取助手。将维度分为主观维度、客观维度、Prompt剩余维度。"},
            {"role": "user", "content": f"PRD要点:\n{prd[:3000]}\n\nRD建议:\n{rd[:3000]}\n\n初始Prompt:\n{prompt[:2000]}\n\n请输出JSON，包含keys: subjective, objective, prompt_leftover，每个为字符串数组。"}
        ]
        try:
            res = self.llm.chat(msg)
            data = json.loads(res)
            return {
                "subjective": list(map(str, data.get("subjective", []))),
                "objective": list(map(str, data.get("objective", []))),
                "prompt_leftover": list(map(str, data.get("prompt_leftover", []))),
            }
        except Exception:
            # fallback heuristic
            return {
                "subjective": ["清晰度", "一致性"],
                "objective": ["正确率", "覆盖率"],
                "prompt_leftover": ["格式约束", "边界条件"],
            }


class PromptEvaluator:
    def __init__(self, llm: LLMTools):
        self.llm = llm

    def evaluate(self, prompt_template: str, eval_rows: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        total = len(eval_rows)
        errors: List[Dict[str, Any]] = []
        correct = 0
        prompts_used: List[Dict[str, Any]] = []
        for row in eval_rows:
            user_prompt = prompt_template.replace("{{input}}", str(row["input"]))
            output = self.llm.chat([{"role": "user", "content": user_prompt}])
            expected = str(row.get("expected", "")).strip()
            prompts_used.append({"type": "inference", "user": user_prompt})
            if output.strip() == expected:
                correct += 1
            else:
                errors.append({"input": row["input"], "expected": expected, "output": output})
        return {"metric": correct / max(total, 1), "errors": errors}, prompts_used


class ErrorAnalyzer:
    def __init__(self, llm: LLMTools):
        self.llm = llm

    def summarize(self, errors: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        if not errors:
            return {"common_types": [], "few_shot": {"good": [], "bad": []}}, []
        sample = errors[:20]
        text = json.dumps(sample, ensure_ascii=False)
        msgs = [
            {"role": "system", "content": "你是错误分析助手，归纳错误类型与频次，并给出代表性示例。"},
            {"role": "user", "content": f"请总结以下错误：{text}"},
        ]
        analysis = self.llm.chat(msgs)
        few_shot = {
            "bad": sample[:5],
            "good": [{"input": e["input"], "expected": e["expected"], "output": e["expected"]} for e in sample[:5]],
        }
        return {"analysis": analysis, "common_types": ["mismatch", "format"], "few_shot": few_shot}, msgs


class PromptRefiner:
    def __init__(self, llm: LLMTools):
        self.llm = llm

    def improve_prompt(self, base_prompt: str, rd_notes: str, prd_summary: str, error_summary: str) -> Tuple[str, List[Dict[str, Any]]]:
        msg = [
            {"role": "system", "content": "你是Prompt优化专家，结合PRD/RD与错误分析迭代优化，保持{{input}}占位符。"},
            {"role": "user", "content": f"基础Prompt:\n{base_prompt}\n\nRD建议:\n{rd_notes}\n\nPRD摘要:\n{prd_summary}\n\n错误分析:\n{error_summary}\n\n请输出仅包含改进后的Prompt模板文本。"}
        ]
        return self.llm.chat(msg), msg


class ResponseRefiner:
    def __init__(self, llm: LLMTools):
        self.llm = llm

    def improve_response(self, prompt: str, output: str, expected: str) -> Tuple[str, List[Dict[str, Any]]]:
        msg = [
            {"role": "system", "content": "你是响应修复助手，进行最小必要改动使输出更接近期望。"},
            {"role": "user", "content": f"Prompt:{prompt}\n输出:{output}\n期望:{expected}\n请输出改良后的响应。"}
        ]
        return self.llm.chat(msg), msg


class PromptOptimizationGraph:
    def __init__(self, cfg: RuntimeConfig):
        self.cfg = cfg
        self.llm = LLMTools(LLMConfig(default_model=cfg.default_model, temperature=cfg.temperature, max_tokens=cfg.max_tokens))
        self.dim_extractor = DimensionExtractor(self.llm)
        self.evaluator = PromptEvaluator(self.llm)
        self.analyzer = ErrorAnalyzer(self.llm)
        self.prompt_refiner = PromptRefiner(self.llm)
        self.response_refiner = ResponseRefiner(self.llm)

    def _load_eval_rows(self, eval_dir: str, eval_files: List[str]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for f in eval_files:
            path = os.path.join(eval_dir, f)
            try:
                rows.extend(load_eval_excel(path))
            except Exception:
                continue
        return rows

    def run(self, tasks: List[Dict[str, Any]], task_id: Optional[str], prompts_dir: str, eval_dir: str, out_dir: str) -> Dict[str, Any]:
        os.makedirs(out_dir, exist_ok=True)
        init_prompts = load_prompts_dir(prompts_dir)
        results: Dict[str, Any] = {}

        for task in tasks:
            if task_id and task["task_id"] != task_id:
                continue
            base_name = f"{task['title']}"
            init_candidates = [v for k, v in init_prompts.items() if base_name in k]
            base_prompt = init_candidates[0] if init_candidates else next(iter(init_prompts.values()), "请基于输入完成任务：{{input}}")

            eval_rows = self._load_eval_rows(eval_dir, task.get("evaluation_files", []))

            # Extract dimensions once per task
            dimensions = self.dim_extractor.extract(task.get("summary", ""), task.get("rd_notes", ""), base_prompt)

            best_prompt = base_prompt
            best_metric = -1.0
            history: List[Dict[str, Any]] = []
            prompts_used: List[Dict[str, Any]] = []
            few_shot_accum: Dict[str, Any] = {"good": [], "bad": []}

            for it in range(self.cfg.max_iterations):
                eval_res, used_infer = self.evaluator.evaluate(best_prompt, eval_rows)
                prompts_used.extend(used_infer)
                metric = eval_res["metric"]
                history.append({"iter": it, "metric": metric, "num_errors": len(eval_res["errors"])})
                improve_gain = (metric - best_metric) if best_metric >= 0 else metric
                if it > 0 and improve_gain < self.cfg.improvement_threshold:
                    break
                if metric > best_metric:
                    best_metric = metric
                if not eval_res["errors"]:
                    break
                analysis, analysis_msgs = self.analyzer.summarize(eval_res["errors"])  # includes few-shot
                prompts_used.extend(analysis_msgs)
                # collect few-shot
                few_shot_accum["bad"].extend(analysis.get("few_shot", {}).get("bad", [])[:5])
                few_shot_accum["good"].extend(analysis.get("few_shot", {}).get("good", [])[:5])

                improved, refine_msgs = self.prompt_refiner.improve_prompt(best_prompt, task.get("rd_notes", ""), task.get("summary", ""), json.dumps(analysis, ensure_ascii=False))
                prompts_used.extend(refine_msgs)
                best_prompt = improved or best_prompt

            out_task_dir = os.path.join(out_dir, task["task_id"])
            os.makedirs(out_task_dir, exist_ok=True)
            with open(os.path.join(out_task_dir, "prompt_template.txt"), "w", encoding="utf-8") as f:
                f.write(best_prompt)
            with open(os.path.join(out_task_dir, "history.json"), "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            with open(os.path.join(out_task_dir, "eval_flow.json"), "w", encoding="utf-8") as f:
                json.dump({"evaluator": "exact_match", "analyzer": "llm_summarize_errors", "response_refiner": True, "dimensions": dimensions}, f, ensure_ascii=False, indent=2)
            with open(os.path.join(out_task_dir, "prompts_used.json"), "w", encoding="utf-8") as f:
                json.dump(prompts_used, f, ensure_ascii=False, indent=2)
            with open(os.path.join(out_task_dir, "few_shot.json"), "w", encoding="utf-8") as f:
                json.dump(few_shot_accum, f, ensure_ascii=False, indent=2)

            results[task["task_id"]] = {"prompt": best_prompt, "metric": best_metric, "dimensions": dimensions}

        return results