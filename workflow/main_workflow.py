"""
主工作流程 - 整合所有Agent的完整数据合成流程
使用LangChain、LangGraph和DeepAgents架构
"""
import asyncio
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import yaml
import logging
from datetime import datetime

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

# 本地Agent imports
from agents.requirement_decomposition_agent import RequirementDecompositionAgent, Task
from agents.prompt_optimization_agent import PromptOptimizationAgent, OptimizationResult
from agents.data_synthesis_agent import DataSynthesisAgent, SynthesisTask, SynthesizedData
from agents.adversarial_data_agent import AdversarialDataAgent, AdversarialData
from tools.llm_tools import LLMTools

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WorkflowState:
    """工作流状态"""
    stage: str = "init"
    prd_files: List[str] = None
    rd_files: List[str] = None
    evaluation_files: List[str] = None
    prompt_files: List[str] = None
    base_dataset: List[Dict[str, Any]] = None
    
    # 中间结果
    tasks: List[Task] = None
    optimization_results: List[OptimizationResult] = None
    synthesized_data: Dict[str, List[SynthesizedData]] = None
    adversarial_data: List[AdversarialData] = None
    defensive_data: List[SynthesizedData] = None
    
    # 配置
    config: Dict[str, Any] = None
    output_dir: str = "/workspace/output"
    
    # 错误处理
    errors: List[str] = None
    
    def __post_init__(self):
        if self.prd_files is None:
            self.prd_files = []
        if self.rd_files is None:
            self.rd_files = []
        if self.evaluation_files is None:
            self.evaluation_files = []
        if self.prompt_files is None:
            self.prompt_files = []
        if self.base_dataset is None:
            self.base_dataset = []
        if self.errors is None:
            self.errors = []

class SFTDataSynthesisWorkflow:
    """SFT数据合成主工作流"""
    
    def __init__(self, config_path: str = "/workspace/config/config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 初始化所有Agent
        self.requirement_agent = RequirementDecompositionAgent(config_path)
        self.prompt_optimization_agent = PromptOptimizationAgent(config_path)
        self.data_synthesis_agent = DataSynthesisAgent(config_path)
        self.adversarial_agent = AdversarialDataAgent(config_path)
        
        # 创建LangGraph工作流
        self.graph = self._create_workflow_graph()
        
        logger.info("SFT数据合成工作流初始化完成")
    
    def _create_workflow_graph(self) -> StateGraph:
        """创建LangGraph工作流图"""
        
        workflow = StateGraph(WorkflowState)
        
        # 添加节点
        workflow.add_node("requirement_decomposition", self._requirement_decomposition_node)
        workflow.add_node("prompt_optimization", self._prompt_optimization_node)
        workflow.add_node("data_synthesis", self._data_synthesis_node)
        workflow.add_node("adversarial_generation", self._adversarial_generation_node)
        workflow.add_node("finalization", self._finalization_node)
        
        # 定义流程
        workflow.set_entry_point("requirement_decomposition")
        workflow.add_edge("requirement_decomposition", "prompt_optimization")
        workflow.add_edge("prompt_optimization", "data_synthesis")
        workflow.add_edge("data_synthesis", "adversarial_generation")
        workflow.add_edge("adversarial_generation", "finalization")
        workflow.add_edge("finalization", END)
        
        # 添加检查点保存器
        checkpointer = MemorySaver()
        app = workflow.compile(checkpointer=checkpointer)
        
        return app
    
    async def _requirement_decomposition_node(self, state: WorkflowState) -> WorkflowState:
        """需求拆解节点"""
        logger.info("执行需求拆解阶段...")
        state.stage = "requirement_decomposition"
        
        try:
            # 运行需求拆解流程
            tasks = await self.requirement_agent.run_pipeline(
                state.prd_files,
                state.rd_files,
                state.evaluation_files,
                state.prompt_files
            )
            
            state.tasks = tasks
            logger.info(f"需求拆解完成，识别出 {len(tasks)} 个优化任务")
            
            # 保存任务
            tasks_file = Path(state.output_dir) / "decomposed_tasks.json"
            tasks_file.parent.mkdir(parents=True, exist_ok=True)
            self.requirement_agent.save_tasks(tasks, str(tasks_file))
            
        except Exception as e:
            error_msg = f"需求拆解失败: {str(e)}"
            logger.error(error_msg)
            state.errors.append(error_msg)
        
        return state
    
    async def _prompt_optimization_node(self, state: WorkflowState) -> WorkflowState:
        """Prompt优化节点"""
        logger.info("执行Prompt优化阶段...")
        state.stage = "prompt_optimization"
        
        if not state.tasks:
            error_msg = "没有可优化的任务"
            logger.error(error_msg)
            state.errors.append(error_msg)
            return state
        
        try:
            # 提取PRD和RD要求
            prd_requirements = []
            rd_requirements = []
            
            for prd_file in state.prd_files:
                if Path(prd_file).exists():
                    with open(prd_file, 'r', encoding='utf-8') as f:
                        prd_requirements.append(f.read())
            
            for rd_file in state.rd_files:
                if Path(rd_file).exists():
                    with open(rd_file, 'r', encoding='utf-8') as f:
                        rd_requirements.append(f.read())
            
            # 运行Prompt优化
            optimization_results = await self.prompt_optimization_agent.optimize_all_tasks(
                state.tasks, prd_requirements, rd_requirements
            )
            
            state.optimization_results = optimization_results
            logger.info(f"Prompt优化完成，优化了 {len(optimization_results)} 个任务")
            
            # 保存优化结果
            results_file = Path(state.output_dir) / "optimization_results.json"
            self.prompt_optimization_agent.save_optimization_results(optimization_results, str(results_file))
            
        except Exception as e:
            error_msg = f"Prompt优化失败: {str(e)}"
            logger.error(error_msg)
            state.errors.append(error_msg)
        
        return state
    
    async def _data_synthesis_node(self, state: WorkflowState) -> WorkflowState:
        """数据合成节点"""
        logger.info("执行数据合成阶段...")
        state.stage = "data_synthesis"
        
        if not state.optimization_results:
            error_msg = "没有优化结果可用于数据合成"
            logger.error(error_msg)
            state.errors.append(error_msg)
            return state
        
        try:
            # 准备合成任务
            target_count = self.config['data_synthesis']['batch_size']
            synthesis_tasks = await self.data_synthesis_agent.prepare_synthesis_tasks(
                state.optimization_results, state.base_dataset, target_count
            )
            
            # 执行数据合成
            synthesized_data = await self.data_synthesis_agent.synthesize_all_data(synthesis_tasks)
            
            state.synthesized_data = synthesized_data
            
            # 统计信息
            total_samples = sum(len(data_list) for data_list in synthesized_data.values())
            logger.info(f"数据合成完成，生成了 {total_samples} 个训练样本")
            
            # 保存合成数据
            synthesis_dir = Path(state.output_dir) / "synthesized_data"
            self.data_synthesis_agent.save_synthesized_data(synthesized_data, str(synthesis_dir))
            
        except Exception as e:
            error_msg = f"数据合成失败: {str(e)}"
            logger.error(error_msg)
            state.errors.append(error_msg)
        
        return state
    
    async def _adversarial_generation_node(self, state: WorkflowState) -> WorkflowState:
        """攻防数据生成节点"""
        logger.info("执行攻防数据生成阶段...")
        state.stage = "adversarial_generation"
        
        if not state.optimization_results:
            error_msg = "没有优化结果可用于攻防数据生成"
            logger.error(error_msg)
            state.errors.append(error_msg)
            return state
        
        try:
            # 准备基础输入
            base_inputs = []
            if state.synthesized_data:
                for data_list in state.synthesized_data.values():
                    base_inputs.extend([item.input for item in data_list[:10]])  # 每个任务取10个样本
            
            if not base_inputs:
                base_inputs = ["示例输入1", "示例输入2", "示例输入3"]  # 默认输入
            
            # 运行攻防数据生成流程
            adversarial_data, defensive_data = await self.adversarial_agent.run_adversarial_pipeline(
                state.optimization_results, base_inputs
            )
            
            state.adversarial_data = adversarial_data
            state.defensive_data = defensive_data
            
            logger.info(f"攻防数据生成完成:")
            logger.info(f"- 攻击测试数据: {len(adversarial_data)} 条")
            logger.info(f"- 防御训练数据: {len(defensive_data)} 条")
            
            # 保存攻防数据
            adversarial_dir = Path(state.output_dir) / "adversarial_data"
            self.adversarial_agent.save_adversarial_data(
                adversarial_data, defensive_data, str(adversarial_dir)
            )
            
        except Exception as e:
            error_msg = f"攻防数据生成失败: {str(e)}"
            logger.error(error_msg)
            state.errors.append(error_msg)
        
        return state
    
    async def _finalization_node(self, state: WorkflowState) -> WorkflowState:
        """最终化节点"""
        logger.info("执行最终化阶段...")
        state.stage = "finalization"
        
        try:
            # 生成工作流报告
            report = self._generate_workflow_report(state)
            
            # 保存报告
            report_file = Path(state.output_dir) / "workflow_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            # 合并所有训练数据
            all_training_data = []
            
            # 添加合成数据
            if state.synthesized_data:
                for data_list in state.synthesized_data.values():
                    for item in data_list:
                        all_training_data.append({
                            "input": item.input,
                            "output": item.output,
                            "data_type": "synthesized",
                            "task_id": item.task_id,
                            "quality_score": item.quality_score,
                            "metadata": item.metadata
                        })
            
            # 添加防御数据
            if state.defensive_data:
                for item in state.defensive_data:
                    all_training_data.append({
                        "input": item.input,
                        "output": item.output,
                        "data_type": "defensive",
                        "task_id": item.task_id,
                        "quality_score": item.quality_score,
                        "metadata": item.metadata
                    })
            
            # 保存最终训练数据
            if all_training_data:
                final_data_file = Path(state.output_dir) / "final_training_data.jsonl"
                with open(final_data_file, 'w', encoding='utf-8') as f:
                    for item in all_training_data:
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                
                logger.info(f"最终训练数据保存完成: {len(all_training_data)} 条样本")
            
            logger.info(f"工作流执行完成，结果保存在: {state.output_dir}")
            
        except Exception as e:
            error_msg = f"最终化阶段失败: {str(e)}"
            logger.error(error_msg)
            state.errors.append(error_msg)
        
        return state
    
    def _generate_workflow_report(self, state: WorkflowState) -> Dict[str, Any]:
        """生成工作流报告"""
        
        # 统计信息
        task_count = len(state.tasks) if state.tasks else 0
        optimization_count = len(state.optimization_results) if state.optimization_results else 0
        
        synthesized_count = 0
        if state.synthesized_data:
            synthesized_count = sum(len(data_list) for data_list in state.synthesized_data.values())
        
        adversarial_count = len(state.adversarial_data) if state.adversarial_data else 0
        defensive_count = len(state.defensive_data) if state.defensive_data else 0
        
        # 质量分析
        quality_analysis = {}
        if state.synthesized_data:
            all_scores = []
            for data_list in state.synthesized_data.values():
                all_scores.extend([item.quality_score for item in data_list])
            
            if all_scores:
                quality_analysis = {
                    "avg_quality_score": sum(all_scores) / len(all_scores),
                    "min_quality_score": min(all_scores),
                    "max_quality_score": max(all_scores),
                    "high_quality_ratio": len([s for s in all_scores if s >= 0.8]) / len(all_scores)
                }
        
        # 安全分析
        security_analysis = {}
        if state.adversarial_data:
            robustness_scores = [data.robustness_score for data in state.adversarial_data]
            successful_attacks = len([data for data in state.adversarial_data if data.attack_success])
            
            security_analysis = {
                "total_security_tests": len(state.adversarial_data),
                "successful_attacks": successful_attacks,
                "attack_success_rate": successful_attacks / len(state.adversarial_data),
                "avg_robustness_score": sum(robustness_scores) / len(robustness_scores),
                "security_level": "high" if sum(robustness_scores) / len(robustness_scores) > 0.8 else "medium"
            }
        
        report = {
            "workflow_summary": {
                "execution_time": datetime.now().isoformat(),
                "total_tasks": task_count,
                "optimized_prompts": optimization_count,
                "synthesized_samples": synthesized_count,
                "adversarial_tests": adversarial_count,
                "defensive_samples": defensive_count,
                "total_training_samples": synthesized_count + defensive_count,
                "errors": state.errors
            },
            "quality_analysis": quality_analysis,
            "security_analysis": security_analysis,
            "file_paths": {
                "tasks": "decomposed_tasks.json",
                "optimization_results": "optimization_results.json",
                "synthesized_data": "synthesized_data/",
                "adversarial_data": "adversarial_data/",
                "final_training_data": "final_training_data.jsonl"
            },
            "recommendations": self._generate_recommendations(state)
        }
        
        return report
    
    def _generate_recommendations(self, state: WorkflowState) -> List[str]:
        """生成改进建议"""
        
        recommendations = []
        
        # 基于错误的建议
        if state.errors:
            recommendations.append("存在执行错误，建议检查输入数据和配置")
        
        # 基于质量的建议
        if state.synthesized_data:
            all_scores = []
            for data_list in state.synthesized_data.values():
                all_scores.extend([item.quality_score for item in data_list])
            
            if all_scores:
                avg_score = sum(all_scores) / len(all_scores)
                if avg_score < 0.7:
                    recommendations.append("数据质量偏低，建议优化prompt模板或增加精炼迭代")
                elif avg_score > 0.9:
                    recommendations.append("数据质量很高，可以考虑增加数据量")
        
        # 基于安全性的建议
        if state.adversarial_data:
            successful_attacks = len([data for data in state.adversarial_data if data.attack_success])
            attack_rate = successful_attacks / len(state.adversarial_data)
            
            if attack_rate > 0.3:
                recommendations.append("攻击成功率较高，建议增强安全防护和鲁棒性训练")
            elif attack_rate < 0.1:
                recommendations.append("安全性表现良好，可以考虑增加更多攻击场景测试")
        
        if not recommendations:
            recommendations.append("工作流执行良好，可以继续使用当前配置")
        
        return recommendations
    
    async def run_workflow(self, 
                         prd_files: List[str],
                         rd_files: List[str],
                         evaluation_files: List[str],
                         prompt_files: List[str],
                         base_dataset: Optional[List[Dict[str, Any]]] = None,
                         output_dir: str = "/workspace/output") -> WorkflowState:
        """运行完整工作流"""
        
        logger.info("开始执行SFT数据合成工作流...")
        
        # 初始化状态
        initial_state = WorkflowState(
            prd_files=prd_files,
            rd_files=rd_files,
            evaluation_files=evaluation_files,
            prompt_files=prompt_files,
            base_dataset=base_dataset or [],
            config=self.config,
            output_dir=output_dir
        )
        
        # 运行工作流
        config = {"configurable": {"thread_id": "sft_workflow"}}
        final_state = await self.graph.ainvoke(initial_state, config)
        
        if final_state.errors:
            logger.warning(f"工作流执行完成，但存在 {len(final_state.errors)} 个错误")
            for error in final_state.errors:
                logger.warning(f"- {error}")
        else:
            logger.info("工作流执行成功完成")
        
        return final_state

# 便捷函数
async def run_sft_data_synthesis(
    prd_dir: str = "/workspace/PRD_context",
    rd_dir: str = "/workspace/rd_suggestions", 
    evaluation_dir: str = "/workspace/evaluation_data",
    prompt_dir: str = "/workspace/prompts",
    dataset_file: Optional[str] = None,
    output_dir: str = "/workspace/output",
    config_path: str = "/workspace/config/config.yaml"
) -> Dict[str, Any]:
    """
    运行SFT数据合成的便捷函数
    
    Args:
        prd_dir: PRD文档目录
        rd_dir: RD建议目录
        evaluation_dir: 评估数据目录
        prompt_dir: Prompt模板目录
        dataset_file: 基础数据集文件
        output_dir: 输出目录
        config_path: 配置文件路径
    
    Returns:
        工作流执行结果报告
    """
    
    # 收集输入文件
    prd_files = list(Path(prd_dir).glob("*.txt")) + list(Path(prd_dir).glob("*.md"))
    rd_files = list(Path(rd_dir).glob("*.txt")) + list(Path(rd_dir).glob("*.md"))
    evaluation_files = list(Path(evaluation_dir).glob("*.xlsx")) + list(Path(evaluation_dir).glob("*.csv"))
    prompt_files = list(Path(prompt_dir).glob("*.txt")) + list(Path(prompt_dir).glob("*.json"))
    
    # 转换为字符串路径
    prd_files = [str(f) for f in prd_files]
    rd_files = [str(f) for f in rd_files]
    evaluation_files = [str(f) for f in evaluation_files]
    prompt_files = [str(f) for f in prompt_files]
    
    # 加载基础数据集
    base_dataset = []
    if dataset_file and Path(dataset_file).exists():
        if dataset_file.endswith('.jsonl'):
            with open(dataset_file, 'r', encoding='utf-8') as f:
                for line in f:
                    base_dataset.append(json.loads(line.strip()))
        elif dataset_file.endswith('.json'):
            with open(dataset_file, 'r', encoding='utf-8') as f:
                base_dataset = json.load(f)
    
    # 创建并运行工作流
    workflow = SFTDataSynthesisWorkflow(config_path)
    final_state = await workflow.run_workflow(
        prd_files, rd_files, evaluation_files, prompt_files, base_dataset, output_dir
    )
    
    # 生成报告
    report = workflow._generate_workflow_report(final_state)
    return report

if __name__ == "__main__":
    # 示例用法
    async def main():
        report = await run_sft_data_synthesis()
        print("工作流执行完成!")
        print(f"报告: {json.dumps(report, ensure_ascii=False, indent=2)}")
    
    asyncio.run(main())