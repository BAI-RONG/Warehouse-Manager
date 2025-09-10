#!/usr/bin/env python3
"""
SFT数据合成系统演示脚本
展示完整的工作流程
"""
import asyncio
import json
import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.append('/workspace')

async def main():
    """主演示函数"""
    print("=" * 60)
    print("🚀 SFT数据合成系统演示")
    print("=" * 60)
    
    try:
        # 导入工作流模块
        from workflow.main_workflow import run_sft_data_synthesis
        
        print("\n📁 检查输入文件...")
        
        # 检查输入文件是否存在
        input_files = {
            "PRD文档": "/workspace/PRD_context/live_streaming_prd.md",
            "RD建议": "/workspace/rd_suggestions/technical_optimization.md", 
            "评估数据": "/workspace/evaluation_data/script_evaluation_data.csv",
            "Prompt模板": "/workspace/prompts/gaming_script_template.txt",
            "基础数据集": "/workspace/base_dataset.jsonl"
        }
        
        for name, path in input_files.items():
            if Path(path).exists():
                print(f"✅ {name}: {path}")
            else:
                print(f"❌ {name}: {path} (不存在)")
        
        print(f"\n🔧 配置文件: /workspace/config/config.yaml")
        print(f"📤 输出目录: /workspace/output")
        
        # 创建输出目录
        output_dir = Path("/workspace/output")
        output_dir.mkdir(exist_ok=True)
        
        print("\n⚠️  注意: 由于这是演示环境，LLM调用将被模拟")
        print("在实际使用中，请配置正确的API密钥")
        
        print("\n🎯 开始执行工作流...")
        print("=" * 40)
        
        # 运行工作流（注意：在演示环境中可能会因为缺少API密钥而失败）
        try:
            report = await run_sft_data_synthesis(
                prd_dir="/workspace/PRD_context",
                rd_dir="/workspace/rd_suggestions",
                evaluation_dir="/workspace/evaluation_data", 
                prompt_dir="/workspace/prompts",
                dataset_file="/workspace/base_dataset.jsonl",
                output_dir="/workspace/output"
            )
            
            print("\n✅ 工作流执行完成！")
            print("\n📊 执行报告:")
            print(json.dumps(report, ensure_ascii=False, indent=2))
            
        except Exception as e:
            print(f"\n⚠️  工作流执行遇到问题: {e}")
            print("\n这通常是因为缺少LLM API配置。")
            print("请在config.yaml中配置正确的API密钥后重试。")
            
            # 展示系统架构
            print("\n" + "=" * 40)
            print("📋 系统架构概览:")
            print("=" * 40)
            
            architecture = """
🏗️ 系统架构:

1️⃣ 需求拆解Agent (RequirementDecompositionAgent)
   ├── 分析PRD文档和RD建议
   ├── 解析评估数据集
   └── 拆解为具体优化任务

2️⃣ Prompt优化Agent (PromptOptimizationAgent)
   ├── 评估流程拆解子Agent
   ├── 问题分析子Agent  
   ├── 反馈收集子Agent
   └── 响应优化子Agent

3️⃣ 数据合成Agent (DataSynthesisAgent)
   ├── 数据变化生成器
   ├── 质量评估器
   └── 响应精炼器

4️⃣ 攻防数据Agent (AdversarialDataAgent)
   ├── Prompt注入攻击生成器
   ├── 上下文操纵生成器
   ├── 边缘案例生成器
   └── 鲁棒性评估器

🔄 工作流程:
需求拆解 → Prompt优化 → 数据合成 → 攻防数据生成 → 最终化

📊 输出结果:
├── 优化后的Prompt模板
├── 高质量合成训练数据
├── 攻防测试数据
├── 防御训练数据
└── 详细分析报告
"""
            print(architecture)
        
        print("\n" + "=" * 60)
        print("📁 生成的文件结构:")
        print("=" * 60)
        
        # 展示文件结构
        def show_directory_tree(path, prefix="", max_depth=3, current_depth=0):
            if current_depth >= max_depth:
                return
            
            path = Path(path)
            if not path.exists():
                return
                
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and current_depth < max_depth - 1:
                    extension = "    " if is_last else "│   "
                    show_directory_tree(item, prefix + extension, max_depth, current_depth + 1)
        
        print("\n📂 项目结构:")
        show_directory_tree("/workspace", max_depth=3)
        
        print("\n" + "=" * 60)
        print("🎉 演示完成！")
        print("=" * 60)
        
        print("""
📖 使用说明:

1. 配置LLM API密钥在 config/config.yaml
2. 准备输入数据:
   - PRD文档放入 PRD_context/
   - RD建议放入 rd_suggestions/
   - 评估数据放入 evaluation_data/
   - Prompt模板放入 prompts/
3. 运行: python demo.py 或 python -m workflow.main_workflow
4. 查看结果在 output/ 目录

🔧 自定义配置:
- 修改 config/config.yaml 调整参数
- 修改各Agent的提示词模板
- 调整评估标准和质量阈值

💡 扩展建议:
- 集成更多LLM提供商
- 添加更多攻击场景
- 增加多模态数据支持
- 集成人工反馈循环
""")
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保所有依赖都已安装")
    except Exception as e:
        print(f"❌ 运行错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())