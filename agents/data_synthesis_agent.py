"""
数据合成Agent
利用优化后的prompts和数据集合成训练数据，并进行响应精炼
"""
import asyncio
import json
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import yaml
import numpy as np
from pathlib import Path
import hashlib
from datetime import datetime

from tools.llm_tools import LLMTools, DataProcessor
from agents.prompt_optimization_agent import OptimizationResult

@dataclass
class SynthesisTask:
    """数据合成任务"""
    task_id: str
    prompt_template: str
    input_data: List[Dict[str, Any]]
    target_count: int
    quality_threshold: float
    refinement_iterations: int

@dataclass
class SynthesizedData:
    """合成数据"""
    data_id: str
    task_id: str
    input: str
    output: str
    quality_score: float
    metadata: Dict[str, Any]
    created_at: str

class DataVariationGenerator:
    """数据变化生成器"""
    
    def __init__(self, llm_tools: LLMTools):
        self.llm_tools = llm_tools
        
        self.variation_prompts = {
            "paraphrase": "请将以下文本改写，保持核心意思不变但使用不同的表达方式：\n{text}",
            "expand": "请扩展以下文本，增加更多细节和描述：\n{text}",
            "simplify": "请简化以下文本，使其更加简洁明了：\n{text}",
            "formalize": "请将以下文本改写为更正式的表达：\n{text}",
            "casual": "请将以下文本改写为更随意的表达：\n{text}"
        }
    
    async def generate_variations(self, 
                                original_text: str, 
                                variation_types: List[str],
                                count_per_type: int = 2) -> List[str]:
        """生成文本变体"""
        
        variations = []
        tasks = []
        
        for variation_type in variation_types:
            if variation_type in self.variation_prompts:
                prompt = self.variation_prompts[variation_type].format(text=original_text)
                for _ in range(count_per_type):
                    tasks.append(self.llm_tools.call_llm(prompt))
        
        if tasks:
            responses = await asyncio.gather(*tasks)
            variations = [response.content.strip() for response in responses]
        
        return variations
    
    async def generate_input_variations(self, 
                                      base_inputs: List[str],
                                      target_count: int) -> List[str]:
        """生成输入变体"""
        
        if len(base_inputs) >= target_count:
            return random.sample(base_inputs, target_count)
        
        variations = list(base_inputs)
        needed = target_count - len(base_inputs)
        
        variation_types = ["paraphrase", "expand", "simplify"]
        per_input = max(1, needed // len(base_inputs))
        
        for base_input in base_inputs:
            if len(variations) >= target_count:
                break
            
            new_variations = await self.generate_variations(
                base_input, variation_types, per_input
            )
            variations.extend(new_variations)
        
        return variations[:target_count]

class QualityEvaluator:
    """质量评估器"""
    
    def __init__(self, llm_tools: LLMTools):
        self.llm_tools = llm_tools
        
        self.evaluation_prompt = """
请评估以下生成内容的质量，从以下维度给出0-1的分数：

输入：{input}
输出：{output}

评估维度：
1. 相关性 (0-1): 输出与输入的相关程度
2. 流畅性 (0-1): 语言表达的流畅程度
3. 完整性 (0-1): 内容的完整程度
4. 准确性 (0-1): 信息的准确程度
5. 创新性 (0-1): 内容的创新程度

请以JSON格式返回评分：
{{
    "relevance": 0.8,
    "fluency": 0.9,
    "completeness": 0.7,
    "accuracy": 0.8,
    "creativity": 0.6,
    "overall": 0.76
}}
"""
    
    async def evaluate_quality(self, input_text: str, output_text: str) -> Dict[str, float]:
        """评估单个样本质量"""
        
        prompt = self.evaluation_prompt.format(input=input_text, output=output_text)
        response = await self.llm_tools.call_llm(prompt)
        
        try:
            scores = json.loads(response.content)
            # 确保所有分数在0-1范围内
            for key, value in scores.items():
                scores[key] = max(0.0, min(1.0, float(value)))
            return scores
        except:
            # 返回默认分数
            return {
                "relevance": 0.5,
                "fluency": 0.5,
                "completeness": 0.5,
                "accuracy": 0.5,
                "creativity": 0.5,
                "overall": 0.5
            }
    
    async def batch_evaluate(self, 
                           inputs: List[str], 
                           outputs: List[str]) -> List[Dict[str, float]]:
        """批量评估质量"""
        
        tasks = [
            self.evaluate_quality(inp, out)
            for inp, out in zip(inputs, outputs)
        ]
        
        return await asyncio.gather(*tasks)

class ResponseRefiner:
    """响应精炼器"""
    
    def __init__(self, llm_tools: LLMTools):
        self.llm_tools = llm_tools
    
    async def refine_response(self, 
                            original_input: str,
                            original_output: str,
                            quality_issues: List[str],
                            target_criteria: Dict[str, str]) -> str:
        """精炼单个响应"""
        
        refinement_prompt = f"""
请改进以下响应，解决识别出的质量问题：

原始输入：
{original_input}

原始输出：
{original_output}

识别的问题：
{chr(10).join(quality_issues)}

改进标准：
{json.dumps(target_criteria, ensure_ascii=False, indent=2)}

请生成改进后的响应：
"""
        
        response = await self.llm_tools.call_llm(refinement_prompt)
        return response.content.strip()
    
    async def iterative_refinement(self,
                                 input_text: str,
                                 output_text: str,
                                 quality_evaluator: QualityEvaluator,
                                 target_score: float = 0.8,
                                 max_iterations: int = 3) -> Tuple[str, Dict[str, float]]:
        """迭代精炼响应"""
        
        current_output = output_text
        best_output = output_text
        best_score = 0.0
        
        for iteration in range(max_iterations):
            # 评估当前质量
            quality_scores = await quality_evaluator.evaluate_quality(input_text, current_output)
            current_score = quality_scores.get('overall', 0.0)
            
            if current_score > best_score:
                best_score = current_score
                best_output = current_output
            
            # 如果达到目标质量，停止精炼
            if current_score >= target_score:
                break
            
            # 识别需要改进的方面
            issues = []
            for dimension, score in quality_scores.items():
                if dimension != 'overall' and score < 0.7:
                    issues.append(f"{dimension}: {score:.2f} (需要改进)")
            
            if not issues:
                break
            
            # 精炼响应
            target_criteria = {
                "相关性": "确保内容与输入高度相关",
                "流畅性": "使用自然流畅的语言表达",
                "完整性": "提供完整的信息和答案",
                "准确性": "确保信息的准确性",
                "创新性": "在准确的基础上增加创新元素"
            }
            
            current_output = await self.refine_response(
                input_text, current_output, issues, target_criteria
            )
        
        final_scores = await quality_evaluator.evaluate_quality(input_text, best_output)
        return best_output, final_scores

class DataSynthesisAgent:
    """数据合成主代理"""
    
    def __init__(self, config_path: str = "/workspace/config/config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.llm_tools = LLMTools(config_path)
        self.data_processor = DataProcessor()
        
        # 初始化子组件
        self.variation_generator = DataVariationGenerator(self.llm_tools)
        self.quality_evaluator = QualityEvaluator(self.llm_tools)
        self.response_refiner = ResponseRefiner(self.llm_tools)
        
        # 配置参数
        self.batch_size = self.config['data_synthesis']['batch_size']
        self.quality_threshold = self.config['data_synthesis']['quality_threshold']
    
    async def prepare_synthesis_tasks(self, 
                                    optimization_results: List[OptimizationResult],
                                    base_dataset: List[Dict[str, Any]],
                                    target_count_per_task: int = 100) -> List[SynthesisTask]:
        """准备数据合成任务"""
        
        tasks = []
        for result in optimization_results:
            # 筛选相关数据
            task_data = [
                item for item in base_dataset
                if item.get('task_id') == result.task_id or 
                   any(keyword in str(item.get('input', '')).lower() 
                       for keyword in result.task_id.lower().split('_'))
            ]
            
            if not task_data:
                # 使用默认数据
                task_data = base_dataset[:10] if base_dataset else []
            
            task = SynthesisTask(
                task_id=result.task_id,
                prompt_template=result.optimized_prompt,
                input_data=task_data,
                target_count=target_count_per_task,
                quality_threshold=self.quality_threshold,
                refinement_iterations=3
            )
            tasks.append(task)
        
        return tasks
    
    async def synthesize_data_for_task(self, task: SynthesisTask) -> List[SynthesizedData]:
        """为单个任务合成数据"""
        
        print(f"开始合成任务数据: {task.task_id}")
        
        # 1. 准备输入数据
        base_inputs = [item.get('input', '') for item in task.input_data if item.get('input')]
        if not base_inputs:
            base_inputs = [f"示例输入 {i+1}" for i in range(5)]
        
        # 2. 生成输入变体
        varied_inputs = await self.variation_generator.generate_input_variations(
            base_inputs, task.target_count
        )
        
        synthesized_data = []
        
        # 3. 批量生成数据
        for i in range(0, len(varied_inputs), self.batch_size):
            batch_inputs = varied_inputs[i:i + self.batch_size]
            print(f"  处理批次 {i//self.batch_size + 1}/{(len(varied_inputs) + self.batch_size - 1)//self.batch_size}")
            
            # 生成响应
            batch_outputs = []
            for inp in batch_inputs:
                try:
                    response = await self.llm_tools.call_llm(inp, task.prompt_template)
                    batch_outputs.append(response.content.strip())
                except Exception as e:
                    print(f"    生成失败: {e}")
                    batch_outputs.append("生成失败")
            
            # 评估质量
            quality_scores = await self.quality_evaluator.batch_evaluate(batch_inputs, batch_outputs)
            
            # 精炼低质量响应
            for j, (inp, out, scores) in enumerate(zip(batch_inputs, batch_outputs, quality_scores)):
                current_output = out
                current_scores = scores
                
                # 如果质量不达标，进行精炼
                if scores.get('overall', 0.0) < task.quality_threshold:
                    try:
                        refined_output, refined_scores = await self.response_refiner.iterative_refinement(
                            inp, out, self.quality_evaluator, task.quality_threshold, task.refinement_iterations
                        )
                        current_output = refined_output
                        current_scores = refined_scores
                    except Exception as e:
                        print(f"    精炼失败: {e}")
                
                # 创建合成数据
                data_id = hashlib.md5(f"{task.task_id}_{i+j}_{inp}".encode()).hexdigest()[:8]
                synthesized_item = SynthesizedData(
                    data_id=data_id,
                    task_id=task.task_id,
                    input=inp,
                    output=current_output,
                    quality_score=current_scores.get('overall', 0.0),
                    metadata={
                        'batch_id': i // self.batch_size,
                        'quality_scores': current_scores,
                        'refined': scores.get('overall', 0.0) < task.quality_threshold,
                        'original_output': out if current_output != out else None
                    },
                    created_at=datetime.now().isoformat()
                )
                synthesized_data.append(synthesized_item)
        
        # 4. 过滤高质量数据
        high_quality_data = [
            item for item in synthesized_data
            if item.quality_score >= task.quality_threshold
        ]
        
        print(f"  合成完成: {len(synthesized_data)} 总样本, {len(high_quality_data)} 高质量样本")
        return high_quality_data
    
    async def synthesize_all_data(self, 
                                synthesis_tasks: List[SynthesisTask]) -> Dict[str, List[SynthesizedData]]:
        """合成所有任务的数据"""
        
        all_synthesized_data = {}
        
        for task in synthesis_tasks:
            try:
                task_data = await self.synthesize_data_for_task(task)
                all_synthesized_data[task.task_id] = task_data
            except Exception as e:
                print(f"任务 {task.task_id} 数据合成失败: {e}")
                all_synthesized_data[task.task_id] = []
        
        return all_synthesized_data
    
    def save_synthesized_data(self, 
                            synthesized_data: Dict[str, List[SynthesizedData]],
                            output_dir: str):
        """保存合成数据"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存每个任务的数据
        for task_id, data_list in synthesized_data.items():
            task_file = output_path / f"{task_id}_synthesized.jsonl"
            
            jsonl_data = []
            for item in data_list:
                jsonl_data.append({
                    'data_id': item.data_id,
                    'task_id': item.task_id,
                    'input': item.input,
                    'output': item.output,
                    'quality_score': item.quality_score,
                    'metadata': item.metadata,
                    'created_at': item.created_at
                })
            
            self.data_processor.save_jsonl(jsonl_data, str(task_file))
        
        # 保存汇总数据
        all_data = []
        for data_list in synthesized_data.values():
            for item in data_list:
                all_data.append({
                    'data_id': item.data_id,
                    'task_id': item.task_id,
                    'input': item.input,
                    'output': item.output,
                    'quality_score': item.quality_score,
                    'metadata': item.metadata,
                    'created_at': item.created_at
                })
        
        summary_file = output_path / "all_synthesized_data.jsonl"
        self.data_processor.save_jsonl(all_data, str(summary_file))
        
        # 保存统计信息
        stats = {
            'total_tasks': len(synthesized_data),
            'total_samples': len(all_data),
            'task_statistics': {}
        }
        
        for task_id, data_list in synthesized_data.items():
            stats['task_statistics'][task_id] = {
                'sample_count': len(data_list),
                'avg_quality_score': np.mean([item.quality_score for item in data_list]) if data_list else 0,
                'high_quality_count': len([item for item in data_list if item.quality_score >= self.quality_threshold]),
                'refined_count': len([item for item in data_list if item.metadata.get('refined', False)])
            }
        
        stats_file = output_path / "synthesis_statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"数据合成完成，共生成 {len(all_data)} 个样本")
        print(f"数据保存至: {output_dir}")
        
        return stats
    
    def load_synthesized_data(self, input_dir: str) -> Dict[str, List[SynthesizedData]]:
        """加载合成数据"""
        
        input_path = Path(input_dir)
        synthesized_data = {}
        
        for jsonl_file in input_path.glob("*_synthesized.jsonl"):
            task_id = jsonl_file.stem.replace("_synthesized", "")
            data_list = self.data_processor.load_jsonl(str(jsonl_file))
            
            task_data = []
            for item in data_list:
                synthesized_item = SynthesizedData(
                    data_id=item['data_id'],
                    task_id=item['task_id'],
                    input=item['input'],
                    output=item['output'],
                    quality_score=item['quality_score'],
                    metadata=item['metadata'],
                    created_at=item['created_at']
                )
                task_data.append(synthesized_item)
            
            synthesized_data[task_id] = task_data
        
        return synthesized_data