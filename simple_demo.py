#!/usr/bin/env python3
"""
SFT数据合成系统简化演示
展示系统架构和核心概念
"""
import json
import os
from pathlib import Path

def show_system_overview():
    """展示系统概览"""
    print("=" * 60)
    print("🚀 直播动态脚本SFT数据合成系统")
    print("=" * 60)
    
    print("""
🎯 系统目标:
构建一个动态应对产品经理临时需求的多智能体工作流系统，
用于生成高质量的直播脚本SFT训练数据。

📋 输入内容:
- 产品经理的多段PRD需求
- 程序员的优化思路和建议  
- 初始化的多段prompt模板
- 评估数据集合
- LLM大模型调用和AI API联网检索工具

🎯 输出结果:
- 优化后的prompt模板
- 高质量合成训练数据
- 攻防测试数据
- 防御训练数据
- 详细分析报告
""")

def show_architecture():
    """展示系统架构"""
    print("\n" + "=" * 60)
    print("🏗️ 系统架构")
    print("=" * 60)
    
    architecture = """
┌─────────────────────────────────────────────────────────────┐
│                    多智能体工作流                              │
│              (LangChain + LangGraph + DeepAgents)           │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  1️⃣ 需求拆解Pipeline Agent                   │
│                                                             │
│  📄 PRD分析器     → 提取产品需求核心要点                      │
│  💻 RD建议分析器  → 解析技术实现建议                          │
│  📊 评估数据解析器 → 从Excel动态解析评估维度                   │
│  🎯 任务拆解器     → 拆解为独立优化任务                        │
│                                                             │
│  输出: 结构化任务列表 + 评估标准                              │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  2️⃣ Prompt优化Agent                         │
│                                                             │
│  🔍 评估流程拆解子Agent                                      │
│      ├── 主观维度识别 (相关性、流畅性、创意性)                │
│      └── 客观维度识别 (格式、长度、关键词覆盖)                │
│                                                             │
│  🔍 问题分析子Agent                                          │
│      ├── 常见错误类型统计                                    │
│      ├── 问题频次分析                                        │
│      └── Good/Bad Case生成                                  │
│                                                             │
│  📝 反馈收集子Agent                                          │
│      ├── 优化建议收集                                        │
│      └── Prompt修改方案                                     │
│                                                             │
│  ⚡ 响应优化子Agent                                          │
│      ├── 迭代优化 (最大5次)                                  │
│      ├── 收敛检测                                           │
│      └── 响应质量精炼                                        │
│                                                             │
│  输出: 优化的Prompt模板 + 评估流程                           │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  3️⃣ 数据合成Agent                           │
│                                                             │
│  🔄 数据变化生成器                                           │
│      ├── 改写 (保持核心意思，不同表达)                        │
│      ├── 扩展 (增加细节描述)                                 │
│      ├── 简化 (简洁明了)                                     │
│      └── 风格转换 (正式/随意)                                │
│                                                             │
│  📊 质量评估器                                               │
│      ├── 相关性评估 (0-1分)                                  │
│      ├── 流畅性评估 (0-1分)                                  │
│      ├── 完整性评估 (0-1分)                                  │
│      └── 创新性评估 (0-1分)                                  │
│                                                             │
│  ✨ 响应精炼器                                               │
│      ├── 迭代精炼 (最多3次)                                  │
│      ├── 质量阈值检查 (>0.8)                                │
│      └── 批量处理优化                                        │
│                                                             │
│  输出: 高质量合成训练数据                                     │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  4️⃣ 攻防数据Agent                           │
│                                                             │
│  ⚔️ Prompt注入攻击生成器                                     │
│      ├── "忽略之前指令"类攻击                                │
│      ├── "系统更新"类攻击                                    │
│      └── "管理员命令"类攻击                                  │
│                                                             │
│  🎭 上下文操纵生成器                                         │
│      ├── 虚假紧急状态                                        │
│      ├── 测试环境声明                                        │
│      └── 时间/场景混淆                                       │
│                                                             │
│  🔍 边缘案例生成器                                           │
│      ├── 极长/极短输入                                       │
│      ├── 特殊字符处理                                        │
│      ├── 语义模糊/矛盾                                       │
│      └── 技术边界情况                                        │
│                                                             │
│  🛡️ 鲁棒性评估器                                            │
│      ├── 攻击抵御能力                                        │
│      ├── 任务执行保持                                        │
│      ├── 有害内容避免                                        │
│      └── 边界处理能力                                        │
│                                                             │
│  输出: 攻防测试数据 + 防御训练数据 + 安全报告                │
└─────────────────────────────────────────────────────────────┘
"""
    print(architecture)

def show_workflow():
    """展示工作流程"""
    print("\n" + "=" * 60)
    print("🔄 工作流程")
    print("=" * 60)
    
    workflow = """
阶段1: 需求拆解
├── 读取PRD文档 → 提取核心需求
├── 分析RD建议 → 识别技术要点
├── 解析评估数据 → 提取评估维度
└── 拆解任务 → 生成独立优化任务

阶段2: Prompt优化
├── 评估流程设计 → 主观/客观维度分类
├── 问题模式分析 → 识别常见错误类型
├── 反馈收集整理 → 优化建议汇总
└── 迭代优化 → 直至收敛或达到最大次数

阶段3: 数据合成
├── 输入变体生成 → 扩充数据多样性
├── 批量内容生成 → 使用优化后的Prompt
├── 质量评估筛选 → 多维度质量检查
└── 响应精炼优化 → 提升低质量样本

阶段4: 攻防数据生成
├── 攻击场景设计 → 多种攻击类型
├── 边缘案例构造 → 极端情况测试
├── 鲁棒性测试 → 评估模型抵御能力
└── 防御数据生成 → 基于攻击结果生成

阶段5: 最终化
├── 数据质量汇总 → 统计分析报告
├── 安全评估报告 → 鲁棒性分析
├── 训练数据整合 → 合并所有高质量数据
└── 结果输出 → JSONL格式训练数据
"""
    print(workflow)

def show_file_structure():
    """展示文件结构"""
    print("\n" + "=" * 60)
    print("📁 项目文件结构")
    print("=" * 60)
    
    def show_directory_tree(path, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        path = Path(path)
        if not path.exists():
            print(f"{prefix}├── {path.name} (不存在)")
            return
        
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            
            # 添加文件描述
            description = ""
            if item.name == "agents":
                description = " (智能体模块)"
            elif item.name == "tools":
                description = " (工具模块)"
            elif item.name == "workflow":
                description = " (工作流模块)"
            elif item.name == "config":
                description = " (配置文件)"
            elif item.name == "PRD_context":
                description = " (PRD需求文档)"
            elif item.name == "rd_suggestions":
                description = " (RD优化建议)"
            elif item.name == "prompts":
                description = " (Prompt模板)"
            elif item.name == "evaluation_data":
                description = " (评估数据集)"
            elif item.name == "output":
                description = " (输出结果)"
            elif item.name.endswith('.py'):
                description = " (Python脚本)"
            elif item.name.endswith('.yaml'):
                description = " (配置文件)"
            elif item.name.endswith('.md'):
                description = " (文档)"
            elif item.name.endswith('.jsonl'):
                description = " (数据集)"
            
            print(f"{prefix}{current_prefix}{item.name}{description}")
            
            if item.is_dir() and current_depth < max_depth - 1:
                extension = "    " if is_last else "│   "
                show_directory_tree(item, prefix + extension, max_depth, current_depth + 1)
    
    show_directory_tree("/workspace", max_depth=3)

def show_example_data():
    """展示示例数据"""
    print("\n" + "=" * 60)
    print("📊 示例数据")
    print("=" * 60)
    
    # 显示PRD内容摘要
    prd_file = "/workspace/PRD_context/live_streaming_prd.md"
    if Path(prd_file).exists():
        print("\n📄 PRD文档摘要:")
        with open(prd_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')[:10]  # 显示前10行
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        print("   ...")
    
    # 显示评估数据摘要
    eval_file = "/workspace/evaluation_data/script_evaluation_data.csv"
    if Path(eval_file).exists():
        print("\n📊 评估数据摘要:")
        with open(eval_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:6]  # 显示前5行数据
            for i, line in enumerate(lines):
                if i == 0:
                    print(f"   表头: {line.strip()}")
                elif i <= 3:
                    parts = line.strip().split(',')
                    print(f"   样本{i}: {parts[0]} | {parts[1]} | 质量分数: {parts[8]}")
        print("   ...")
    
    # 显示Prompt模板摘要
    prompt_file = "/workspace/prompts/gaming_script_template.txt"
    if Path(prompt_file).exists():
        print("\n📝 Prompt模板摘要:")
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')[:8]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        print("   ...")

def show_usage_guide():
    """展示使用指南"""
    print("\n" + "=" * 60)
    print("📖 使用指南")
    print("=" * 60)
    
    guide = """
🚀 快速开始:

1️⃣ 环境配置:
   ├── 安装Python 3.8+
   ├── 安装依赖: pip install -r requirements.txt
   └── 配置API密钥: 编辑 config/config.yaml

2️⃣ 数据准备:
   ├── PRD文档 → PRD_context/ (支持.txt, .md)
   ├── RD建议 → rd_suggestions/ (支持.txt, .md)  
   ├── 评估数据 → evaluation_data/ (支持.xlsx, .csv)
   ├── Prompt模板 → prompts/ (支持.txt, .json)
   └── 基础数据集 → base_dataset.jsonl

3️⃣ 运行系统:
   ├── 演示运行: python demo.py
   ├── 完整流程: python -m workflow.main_workflow
   └── 自定义参数: 修改config/config.yaml

4️⃣ 结果查看:
   ├── 输出目录: output/
   ├── 训练数据: final_training_data.jsonl
   ├── 质量报告: workflow_report.json
   └── 安全报告: adversarial_data/security_analysis_report.json

🔧 自定义配置:

• 调整优化参数:
  - max_iterations: 最大优化轮次
  - convergence_threshold: 收敛阈值
  - quality_threshold: 质量阈值

• 添加新的攻击场景:
  - 编辑 adversarial_data_agent.py
  - 添加新的 AdversarialScenario

• 扩展评估维度:
  - 修改 config.yaml 中的 evaluation.dimensions
  - 自定义评估prompt

💡 最佳实践:

✅ 高质量PRD编写:
   ├── 明确功能需求和质量标准
   ├── 包含具体的使用场景
   └── 提供成功指标和评估标准

✅ 有效的RD建议:
   ├── 具体的技术实现方案
   ├── 明确的优化优先级
   └── 潜在风险和应对策略

✅ 丰富的评估数据:
   ├── 多样化的样本类型
   ├── 平衡的质量分布
   └── 详细的反馈信息

🚨 注意事项:

⚠️  API配置: 确保LLM API密钥正确配置
⚠️  数据隐私: 注意敏感数据的处理和保护
⚠️  资源消耗: 大规模数据生成需要充足的计算资源
⚠️  质量控制: 定期检查生成数据的质量和安全性
"""
    print(guide)

def main():
    """主函数"""
    try:
        show_system_overview()
        show_architecture()
        show_workflow()
        show_file_structure()
        show_example_data()
        show_usage_guide()
        
        print("\n" + "=" * 60)
        print("🎉 系统演示完成!")
        print("=" * 60)
        
        print("""
🔗 下一步:

1. 配置LLM API密钥 (config/config.yaml)
2. 准备你的PRD文档和RD建议
3. 运行完整工作流: python -m workflow.main_workflow
4. 查看生成的训练数据和分析报告

📞 技术支持:
- 查看详细文档: README.md  
- 系统架构图: 架构图.jpg
- 问题反馈: GitHub Issues

💡 记住: 这是一个强大的多智能体系统，能够动态应对
   产品经理的临时需求，生成高质量的SFT训练数据！
""")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main()