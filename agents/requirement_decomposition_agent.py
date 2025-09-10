"""
需求拆解Pipeline Agent
分析PRD、RD建议和评估数据，拆解优化任务
"""
import asyncio
import json
import pandas as pd
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import os
import yaml
from pathlib import Path

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_core.messages import HumanMessage, SystemMessage

from tools.llm_tools import LLMTools, DataProcessor, SearchTools

@dataclass
class Task:
    """任务数据结构"""
    task_id: str
    name: str
    description: str
    priority: int
    requirements: List[str]
    evaluation_criteria: Dict[str, Any]
    initial_prompt: str
    rd_suggestions: List[str]
    related_data: List[Dict[str, Any]]

class RequirementDecompositionAgent:
    """需求拆解代理"""
    
    def __init__(self, config_path: str = "/workspace/config/config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.llm_tools = LLMTools(config_path)
        self.data_processor = DataProcessor()
        
        # 系统prompt
        self.system_prompt = """
你是一个专业的需求分析专家，负责将复杂的产品需求文档(PRD)和研发建议拆解为具体的优化任务。

你的职责：
1. 分析PRD文档，理解产品需求的核心要点
2. 结合RD的技术建议，识别技术实现要点
3. 从评估数据中提取相关的评估维度和标准
4. 将复杂需求拆解为可独立优化的子任务
5. 为每个任务分配优先级和评估标准

输出格式：
- 任务列表，每个任务包含：任务ID、名称、描述、优先级、需求列表、评估标准、初始prompt、RD建议、相关数据
"""
    
    async def analyze_prd(self, prd_content: str) -> Dict[str, Any]:
        """分析PRD文档"""
        analysis_prompt = f"""
请分析以下PRD文档，提取关键信息：

PRD内容：
{prd_content}

请提取以下信息并以JSON格式返回：
{{
    "core_requirements": ["需求1", "需求2", ...],
    "functional_modules": ["模块1", "模块2", ...],
    "quality_standards": ["标准1", "标准2", ...],
    "priority_features": ["高优先级功能1", "高优先级功能2", ...],
    "success_metrics": ["成功指标1", "成功指标2", ...]
}}
"""
        
        response = await self.llm_tools.call_llm(analysis_prompt, self.system_prompt)
        try:
            return json.loads(response.content)
        except:
            return {"core_requirements": [], "functional_modules": [], "quality_standards": [], "priority_features": [], "success_metrics": []}
    
    async def analyze_rd_suggestions(self, rd_content: str) -> Dict[str, Any]:
        """分析RD建议"""
        analysis_prompt = f"""
请分析以下RD技术建议，提取关键信息：

RD建议内容：
{rd_content}

请提取以下信息并以JSON格式返回：
{{
    "technical_approaches": ["技术方案1", "技术方案2", ...],
    "optimization_points": ["优化点1", "优化点2", ...],
    "implementation_priorities": ["实现优先级1", "实现优先级2", ...],
    "potential_challenges": ["挑战1", "挑战2", ...],
    "quality_improvements": ["质量改进1", "质量改进2", ...]
}}
"""
        
        response = await self.llm_tools.call_llm(analysis_prompt, self.system_prompt)
        try:
            return json.loads(response.content)
        except:
            return {"technical_approaches": [], "optimization_points": [], "implementation_priorities": [], "potential_challenges": [], "quality_improvements": []}
    
    async def analyze_evaluation_data(self, evaluation_file_path: str) -> Dict[str, Any]:
        """分析评估数据"""
        eval_data = self.data_processor.load_excel(evaluation_file_path)
        
        if not eval_data["data"]:
            return {"evaluation_dimensions": [], "data_categories": [], "quality_metrics": []}
        
        # 分析评估数据的结构和内容
        analysis_prompt = f"""
请分析以下评估数据的结构和内容，提取评估维度：

数据列名：{eval_data["columns"]}
数据样本（前5行）：{str(eval_data["data"][:5])}
数据形状：{eval_data["shape"]}

请提取以下信息并以JSON格式返回：
{{
    "evaluation_dimensions": ["维度1", "维度2", ...],
    "data_categories": ["类别1", "类别2", ...],
    "quality_metrics": ["指标1", "指标2", ...],
    "data_distribution": {{"category": "count", ...}}
}}
"""
        
        response = await self.llm_tools.call_llm(analysis_prompt, self.system_prompt)
        try:
            analysis_result = json.loads(response.content)
            analysis_result["raw_data"] = eval_data
            return analysis_result
        except:
            return {"evaluation_dimensions": [], "data_categories": [], "quality_metrics": [], "raw_data": eval_data}
    
    async def decompose_tasks(self, 
                            prd_analysis: Dict[str, Any],
                            rd_analysis: Dict[str, Any], 
                            eval_analysis: Dict[str, Any],
                            initial_prompts: Dict[str, str]) -> List[Task]:
        """拆解任务"""
        
        decomposition_prompt = f"""
基于以下分析结果，将需求拆解为具体的优化任务：

PRD分析结果：
{json.dumps(prd_analysis, ensure_ascii=False, indent=2)}

RD分析结果：
{json.dumps(rd_analysis, ensure_ascii=False, indent=2)}

评估分析结果：
{json.dumps(eval_analysis, ensure_ascii=False, indent=2)}

初始Prompt模板：
{json.dumps(initial_prompts, ensure_ascii=False, indent=2)}

请将需求拆解为独立的优化任务，每个任务应该：
1. 有明确的优化目标
2. 可以独立进行prompt优化
3. 有对应的评估标准
4. 有相关的训练数据

请以JSON格式返回任务列表：
{{
    "tasks": [
        {{
            "task_id": "task_001",
            "name": "任务名称",
            "description": "任务描述",
            "priority": 1,
            "requirements": ["需求1", "需求2"],
            "evaluation_criteria": {{"维度1": "标准1", "维度2": "标准2"}},
            "initial_prompt_key": "对应的初始prompt键名",
            "rd_suggestions": ["建议1", "建议2"],
            "related_data_filters": {{"column": "value"}}
        }}
    ]
}}
"""
        
        response = await self.llm_tools.call_llm(decomposition_prompt, self.system_prompt)
        try:
            decomposition_result = json.loads(response.content)
            tasks = []
            
            for task_data in decomposition_result.get("tasks", []):
                # 获取相关数据
                related_data = self._filter_evaluation_data(
                    eval_analysis.get("raw_data", {}).get("data", []),
                    task_data.get("related_data_filters", {})
                )
                
                task = Task(
                    task_id=task_data["task_id"],
                    name=task_data["name"],
                    description=task_data["description"],
                    priority=task_data["priority"],
                    requirements=task_data["requirements"],
                    evaluation_criteria=task_data["evaluation_criteria"],
                    initial_prompt=initial_prompts.get(task_data.get("initial_prompt_key", ""), ""),
                    rd_suggestions=task_data["rd_suggestions"],
                    related_data=related_data
                )
                tasks.append(task)
            
            return tasks
        except Exception as e:
            print(f"任务拆解失败: {e}")
            return []
    
    def _filter_evaluation_data(self, data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """根据过滤条件筛选评估数据"""
        if not filters or not data:
            return data[:10]  # 返回前10条作为示例
        
        filtered_data = []
        for item in data:
            match = True
            for key, value in filters.items():
                if key in item and item[key] != value:
                    match = False
                    break
            if match:
                filtered_data.append(item)
        
        return filtered_data[:20]  # 最多返回20条
    
    async def run_pipeline(self, 
                          prd_files: List[str],
                          rd_files: List[str], 
                          evaluation_files: List[str],
                          prompt_files: List[str]) -> List[Task]:
        """运行需求拆解流程"""
        
        # 读取所有文件内容
        prd_content = ""
        for file_path in prd_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    prd_content += f.read() + "\n\n"
        
        rd_content = ""
        for file_path in rd_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    rd_content += f.read() + "\n\n"
        
        # 读取初始prompts
        initial_prompts = {}
        for file_path in prompt_files:
            if os.path.exists(file_path):
                if file_path.endswith('.json'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        prompts = json.load(f)
                        initial_prompts.update(prompts)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        filename = Path(file_path).stem
                        initial_prompts[filename] = f.read()
        
        # 并行分析
        analysis_tasks = [
            self.analyze_prd(prd_content),
            self.analyze_rd_suggestions(rd_content)
        ]
        
        # 分析评估数据
        eval_analyses = []
        for eval_file in evaluation_files:
            if os.path.exists(eval_file):
                eval_analysis = await self.analyze_evaluation_data(eval_file)
                eval_analyses.append(eval_analysis)
        
        prd_analysis, rd_analysis = await asyncio.gather(*analysis_tasks)
        
        # 合并评估分析结果
        combined_eval_analysis = {
            "evaluation_dimensions": [],
            "data_categories": [],
            "quality_metrics": [],
            "raw_data": {"data": [], "columns": [], "shape": (0, 0)}
        }
        
        for eval_analysis in eval_analyses:
            combined_eval_analysis["evaluation_dimensions"].extend(eval_analysis.get("evaluation_dimensions", []))
            combined_eval_analysis["data_categories"].extend(eval_analysis.get("data_categories", []))
            combined_eval_analysis["quality_metrics"].extend(eval_analysis.get("quality_metrics", []))
            if eval_analysis.get("raw_data", {}).get("data"):
                combined_eval_analysis["raw_data"]["data"].extend(eval_analysis["raw_data"]["data"])
        
        # 拆解任务
        tasks = await self.decompose_tasks(prd_analysis, rd_analysis, combined_eval_analysis, initial_prompts)
        
        return tasks
    
    def save_tasks(self, tasks: List[Task], output_path: str):
        """保存任务到文件"""
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "task_id": task.task_id,
                "name": task.name,
                "description": task.description,
                "priority": task.priority,
                "requirements": task.requirements,
                "evaluation_criteria": task.evaluation_criteria,
                "initial_prompt": task.initial_prompt,
                "rd_suggestions": task.rd_suggestions,
                "related_data": task.related_data
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)
    
    def load_tasks(self, input_path: str) -> List[Task]:
        """从文件加载任务"""
        with open(input_path, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)
        
        tasks = []
        for task_data in tasks_data:
            task = Task(
                task_id=task_data["task_id"],
                name=task_data["name"],
                description=task_data["description"],
                priority=task_data["priority"],
                requirements=task_data["requirements"],
                evaluation_criteria=task_data["evaluation_criteria"],
                initial_prompt=task_data["initial_prompt"],
                rd_suggestions=task_data["rd_suggestions"],
                related_data=task_data["related_data"]
            )
            tasks.append(task)
        
        return tasks