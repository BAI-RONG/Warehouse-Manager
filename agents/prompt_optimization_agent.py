"""
Prompt优化Agent
包含多个子代理：评估流程拆解、问题分析、反馈收集、响应优化
"""
import asyncio
import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import yaml
import numpy as np
from collections import Counter, defaultdict
import re

from tools.llm_tools import LLMTools
from agents.requirement_decomposition_agent import Task

@dataclass
class EvaluationFlow:
    """评估流程数据结构"""
    flow_id: str
    name: str
    dimensions: List[str]
    prompts: List[str]
    criteria: Dict[str, str]
    weight: float

@dataclass
class OptimizationResult:
    """优化结果数据结构"""
    task_id: str
    optimized_prompt: str
    evaluation_flows: List[EvaluationFlow]
    performance_metrics: Dict[str, float]
    iterations: int
    common_issues: List[Dict[str, Any]]
    few_shot_examples: Dict[str, List[str]]

class EvaluationFlowDecomposer:
    """评估流程拆解子代理"""
    
    def __init__(self, llm_tools: LLMTools):
        self.llm_tools = llm_tools
        
        self.system_prompt = """
你是一个评估流程设计专家，负责将复杂的评估需求拆解为具体的评估流程。

你的职责：
1. 分析PRD和RD文档中强调的评估流程
2. 识别prompt中的各个评估维度
3. 将主观维度和客观维度分类处理
4. 设计可执行的评估prompt序列

输出应包含：
- 评估维度分类（主观/客观）
- 每个维度的评估prompt
- 评估标准和权重
"""
    
    async def decompose_evaluation_flow(self, 
                                      task: Task,
                                      prd_requirements: List[str],
                                      rd_requirements: List[str]) -> List[EvaluationFlow]:
        """拆解评估流程"""
        
        decomposition_prompt = f"""
基于以下信息，设计详细的评估流程：

任务信息：
- 任务名称: {task.name}
- 任务描述: {task.description}
- 初始Prompt: {task.initial_prompt}
- 评估标准: {json.dumps(task.evaluation_criteria, ensure_ascii=False)}

PRD要求：
{chr(10).join(prd_requirements)}

RD要求：
{chr(10).join(rd_requirements)}

请设计评估流程，包含以下维度：

1. 主观维度（需要人工判断）：
   - 内容相关性
   - 语言流畅性  
   - 创意程度
   - 用户体验

2. 客观维度（可自动检测）：
   - 格式正确性
   - 长度要求
   - 关键词覆盖
   - 逻辑一致性

请以JSON格式返回评估流程：
{{
    "evaluation_flows": [
        {{
            "flow_id": "subjective_content",
            "name": "主观内容评估",
            "dimensions": ["相关性", "流畅性", "创意"],
            "prompts": [
                "评估prompt1",
                "评估prompt2"
            ],
            "criteria": {{
                "dimension": "评估标准"
            }},
            "weight": 0.4
        }}
    ]
}}
"""
        
        response = await self.llm_tools.call_llm(decomposition_prompt, self.system_prompt)
        try:
            result = json.loads(response.content)
            flows = []
            for flow_data in result.get("evaluation_flows", []):
                flow = EvaluationFlow(
                    flow_id=flow_data["flow_id"],
                    name=flow_data["name"],
                    dimensions=flow_data["dimensions"],
                    prompts=flow_data["prompts"],
                    criteria=flow_data["criteria"],
                    weight=flow_data["weight"]
                )
                flows.append(flow)
            return flows
        except Exception as e:
            print(f"评估流程拆解失败: {e}")
            return []

class ProblemAnalyzer:
    """问题分析子代理"""
    
    def __init__(self, llm_tools: LLMTools):
        self.llm_tools = llm_tools
        
        self.system_prompt = """
你是一个问题分析专家，负责分析评估结果中的常见问题。

你的职责：
1. 分析评估数据中的低分样本
2. 识别常见错误类型和模式
3. 统计问题频次和严重程度
4. 生成问题分类和描述
"""
    
    async def analyze_problems(self, 
                             evaluation_results: List[Dict[str, Any]],
                             threshold: float = 0.6) -> Dict[str, Any]:
        """分析常见问题"""
        
        # 筛选低分样本
        low_score_samples = [
            result for result in evaluation_results
            if result.get('overall_score', 1.0) < threshold
        ]
        
        if not low_score_samples:
            return {"common_issues": [], "issue_frequency": {}, "severity_analysis": {}}
        
        analysis_prompt = f"""
请分析以下低质量样本，识别常见问题：

低质量样本数量: {len(low_score_samples)}
样本示例:
{json.dumps(low_score_samples[:5], ensure_ascii=False, indent=2)}

请分析并以JSON格式返回：
{{
    "common_issues": [
        {{
            "issue_type": "问题类型",
            "description": "问题描述", 
            "frequency": 15,
            "severity": "high|medium|low",
            "examples": ["示例1", "示例2"]
        }}
    ],
    "issue_frequency": {{
        "问题类型": 频次
    }},
    "severity_analysis": {{
        "high": 5,
        "medium": 8, 
        "low": 12
    }}
}}
"""
        
        response = await self.llm_tools.call_llm(analysis_prompt, self.system_prompt)
        try:
            return json.loads(response.content)
        except:
            return {"common_issues": [], "issue_frequency": {}, "severity_analysis": {}}
    
    async def generate_few_shot_examples(self, 
                                       evaluation_results: List[Dict[str, Any]],
                                       good_threshold: float = 0.8,
                                       bad_threshold: float = 0.4) -> Dict[str, List[str]]:
        """生成Few-shot示例"""
        
        good_examples = [
            result['response'] for result in evaluation_results
            if result.get('overall_score', 0.0) > good_threshold
        ][:5]
        
        bad_examples = [
            result['response'] for result in evaluation_results  
            if result.get('overall_score', 1.0) < bad_threshold
        ][:5]
        
        return {
            "good_cases": good_examples,
            "bad_cases": bad_examples
        }

class FeedbackCollector:
    """反馈收集子代理"""
    
    def __init__(self, llm_tools: LLMTools):
        self.llm_tools = llm_tools
        
        self.system_prompt = """
你是一个反馈分析专家，负责收集和分析各种反馈信息来优化prompt。

你的职责：
1. 分析评估结果中的具体问题
2. 收集改进建议
3. 识别prompt中需要调整的部分
4. 生成具体的优化方案
"""
    
    async def collect_feedback(self, 
                             current_prompt: str,
                             evaluation_results: List[Dict[str, Any]],
                             problem_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """收集优化反馈"""
        
        feedback_prompt = f"""
基于以下信息，提供prompt优化建议：

当前Prompt:
{current_prompt}

评估结果统计:
- 总样本数: {len(evaluation_results)}
- 平均分: {np.mean([r.get('overall_score', 0.5) for r in evaluation_results]):.3f}
- 低分样本数: {len([r for r in evaluation_results if r.get('overall_score', 1.0) < 0.6])}

问题分析:
{json.dumps(problem_analysis, ensure_ascii=False, indent=2)}

请提供具体的优化建议，以JSON格式返回：
{{
    "optimization_suggestions": [
        {{
            "type": "添加指令|修改格式|增强约束|优化示例",
            "description": "具体建议描述",
            "priority": "high|medium|low",
            "implementation": "具体实现方式"
        }}
    ],
    "prompt_modifications": [
        {{
            "section": "prompt部分名称", 
            "current": "当前内容",
            "suggested": "建议修改内容",
            "reason": "修改原因"
        }}
    ]
}}
"""
        
        response = await self.llm_tools.call_llm(feedback_prompt, self.system_prompt)
        try:
            return json.loads(response.content)
        except:
            return {"optimization_suggestions": [], "prompt_modifications": []}

class ResponseOptimizer:
    """响应优化子代理"""
    
    def __init__(self, llm_tools: LLMTools):
        self.llm_tools = llm_tools
        
        self.system_prompt = """
你是一个prompt优化专家，负责根据反馈改进prompt模板。

你的职责：
1. 根据反馈建议修改prompt
2. 保持prompt的核心功能不变
3. 增强prompt的清晰度和有效性
4. 确保修改后的prompt可以解决识别出的问题
"""
    
    async def optimize_prompt(self, 
                            current_prompt: str,
                            feedback: Dict[str, Any],
                            few_shot_examples: Dict[str, List[str]]) -> str:
        """优化prompt"""
        
        optimization_prompt = f"""
请根据反馈优化以下prompt：

当前Prompt:
{current_prompt}

优化建议:
{json.dumps(feedback.get('optimization_suggestions', []), ensure_ascii=False, indent=2)}

修改建议:
{json.dumps(feedback.get('prompt_modifications', []), ensure_ascii=False, indent=2)}

Good Cases示例:
{chr(10).join(few_shot_examples.get('good_cases', [])[:2])}

Bad Cases示例:
{chr(10).join(few_shot_examples.get('bad_cases', [])[:2])}

请优化prompt，确保：
1. 解决识别出的主要问题
2. 保持原有的核心功能
3. 增加必要的约束和指导
4. 包含适当的示例

请直接返回优化后的prompt，不需要额外解释。
"""
        
        response = await self.llm_tools.call_llm(optimization_prompt, self.system_prompt)
        return response.content.strip()
    
    async def refine_responses(self, 
                             responses: List[str],
                             target_criteria: Dict[str, str]) -> List[str]:
        """精炼响应质量"""
        
        refined_responses = []
        for response in responses:
            refine_prompt = f"""
请优化以下响应，使其更好地满足要求：

原始响应:
{response}

优化标准:
{json.dumps(target_criteria, ensure_ascii=False, indent=2)}

请返回优化后的响应：
"""
            
            result = await self.llm_tools.call_llm(refine_prompt, self.system_prompt)
            refined_responses.append(result.content.strip())
        
        return refined_responses

class PromptOptimizationAgent:
    """Prompt优化主代理"""
    
    def __init__(self, config_path: str = "/workspace/config/config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.llm_tools = LLMTools(config_path)
        self.max_iterations = self.config['optimization']['max_iterations']
        self.convergence_threshold = self.config['optimization']['convergence_threshold']
        
        # 初始化子代理
        self.flow_decomposer = EvaluationFlowDecomposer(self.llm_tools)
        self.problem_analyzer = ProblemAnalyzer(self.llm_tools)
        self.feedback_collector = FeedbackCollector(self.llm_tools)
        self.response_optimizer = ResponseOptimizer(self.llm_tools)
    
    async def evaluate_prompt_performance(self, 
                                        prompt: str,
                                        test_inputs: List[str],
                                        evaluation_flows: List[EvaluationFlow]) -> List[Dict[str, Any]]:
        """评估prompt性能"""
        
        results = []
        for test_input in test_inputs:
            # 使用prompt生成响应
            response = await self.llm_tools.call_llm(test_input, prompt)
            
            # 使用评估流程评估响应
            evaluation_scores = {}
            for flow in evaluation_flows:
                flow_scores = []
                for eval_prompt in flow.prompts:
                    eval_input = eval_prompt.format(
                        response=response.content,
                        input=test_input
                    )
                    eval_result = await self.llm_tools.call_llm(eval_input)
                    
                    # 解析评分（假设返回0-1的分数）
                    try:
                        score = float(re.search(r'[\d.]+', eval_result.content).group())
                        score = min(max(score, 0.0), 1.0)  # 确保在0-1范围内
                    except:
                        score = 0.5  # 默认分数
                    
                    flow_scores.append(score)
                
                evaluation_scores[flow.flow_id] = np.mean(flow_scores) * flow.weight
            
            overall_score = sum(evaluation_scores.values())
            
            results.append({
                'input': test_input,
                'response': response.content,
                'evaluation_scores': evaluation_scores,
                'overall_score': overall_score
            })
        
        return results
    
    async def optimize_single_task(self, 
                                 task: Task,
                                 prd_requirements: List[str],
                                 rd_requirements: List[str]) -> OptimizationResult:
        """优化单个任务的prompt"""
        
        print(f"开始优化任务: {task.name}")
        
        # 1. 拆解评估流程
        evaluation_flows = await self.flow_decomposer.decompose_evaluation_flow(
            task, prd_requirements, rd_requirements
        )
        
        # 2. 准备测试数据
        test_inputs = [item.get('input', '') for item in task.related_data[:10] if item.get('input')]
        if not test_inputs:
            test_inputs = [f"测试输入 {i+1}" for i in range(5)]  # 默认测试输入
        
        current_prompt = task.initial_prompt
        best_prompt = current_prompt
        best_score = 0.0
        
        performance_history = []
        common_issues = []
        few_shot_examples = {"good_cases": [], "bad_cases": []}
        
        # 3. 迭代优化
        for iteration in range(self.max_iterations):
            print(f"  迭代 {iteration + 1}/{self.max_iterations}")
            
            # 评估当前prompt性能
            evaluation_results = await self.evaluate_prompt_performance(
                current_prompt, test_inputs, evaluation_flows
            )
            
            current_score = np.mean([r['overall_score'] for r in evaluation_results])
            performance_history.append(current_score)
            
            print(f"    当前分数: {current_score:.3f}")
            
            # 更新最佳prompt
            if current_score > best_score:
                best_score = current_score
                best_prompt = current_prompt
            
            # 检查收敛
            if iteration > 0:
                improvement = current_score - performance_history[-2]
                if abs(improvement) < self.convergence_threshold:
                    print(f"    收敛，停止优化")
                    break
            
            # 分析问题
            problem_analysis = await self.problem_analyzer.analyze_problems(evaluation_results)
            common_issues = problem_analysis.get('common_issues', [])
            
            # 生成few-shot示例
            few_shot_examples = await self.problem_analyzer.generate_few_shot_examples(evaluation_results)
            
            # 收集反馈
            feedback = await self.feedback_collector.collect_feedback(
                current_prompt, evaluation_results, problem_analysis
            )
            
            # 优化prompt
            if iteration < self.max_iterations - 1:  # 不是最后一次迭代
                current_prompt = await self.response_optimizer.optimize_prompt(
                    current_prompt, feedback, few_shot_examples
                )
        
        print(f"优化完成，最终分数: {best_score:.3f}")
        
        return OptimizationResult(
            task_id=task.task_id,
            optimized_prompt=best_prompt,
            evaluation_flows=evaluation_flows,
            performance_metrics={
                'final_score': best_score,
                'improvement': best_score - (performance_history[0] if performance_history else 0),
                'iterations': len(performance_history)
            },
            iterations=len(performance_history),
            common_issues=common_issues,
            few_shot_examples=few_shot_examples
        )
    
    async def optimize_all_tasks(self, 
                               tasks: List[Task],
                               prd_requirements: List[str],
                               rd_requirements: List[str]) -> List[OptimizationResult]:
        """优化所有任务"""
        
        # 按优先级排序
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        
        results = []
        for task in sorted_tasks:
            try:
                result = await self.optimize_single_task(task, prd_requirements, rd_requirements)
                results.append(result)
            except Exception as e:
                print(f"任务 {task.name} 优化失败: {e}")
                continue
        
        return results
    
    def save_optimization_results(self, results: List[OptimizationResult], output_path: str):
        """保存优化结果"""
        results_data = []
        for result in results:
            results_data.append({
                "task_id": result.task_id,
                "optimized_prompt": result.optimized_prompt,
                "evaluation_flows": [
                    {
                        "flow_id": flow.flow_id,
                        "name": flow.name,
                        "dimensions": flow.dimensions,
                        "prompts": flow.prompts,
                        "criteria": flow.criteria,
                        "weight": flow.weight
                    }
                    for flow in result.evaluation_flows
                ],
                "performance_metrics": result.performance_metrics,
                "iterations": result.iterations,
                "common_issues": result.common_issues,
                "few_shot_examples": result.few_shot_examples
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)