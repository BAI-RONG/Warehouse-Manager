# 直播动态脚本SFT数据合成系统

一个基于多智能体工作流的动态直播脚本SFT数据合成系统，能够根据产品经理的PRD需求、程序员的优化建议和评估数据，自动生成高质量的训练数据。

## 🎯 系统概述

本系统采用LangChain、LangGraph和DeepAgents架构，通过四个核心智能体协同工作，实现从需求分析到数据合成的全流程自动化：

1. **需求拆解Agent** - 分析PRD、RD建议和评估数据，拆解优化任务
2. **Prompt优化Agent** - 多轮优化prompt模板，包含评估流程拆解、问题分析等子代理
3. **数据合成Agent** - 使用优化后的prompt生成高质量训练数据
4. **攻防数据Agent** - 生成边缘case和极端情况的鲁棒性训练数据

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    SFT数据合成工作流                          │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  1. 需求拆解Agent                            │
│  ├── PRD分析器                                              │
│  ├── RD建议分析器                                           │
│  ├── 评估数据解析器                                          │
│  └── 任务拆解器                                             │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  2. Prompt优化Agent                         │
│  ├── 评估流程拆解子Agent                                     │
│  ├── 问题分析子Agent                                        │
│  ├── 反馈收集子Agent                                        │
│  └── 响应优化子Agent                                        │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  3. 数据合成Agent                           │
│  ├── 数据变化生成器                                          │
│  ├── 质量评估器                                             │
│  └── 响应精炼器                                             │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  4. 攻防数据Agent                           │
│  ├── Prompt注入攻击生成器                                   │
│  ├── 上下文操纵生成器                                        │
│  ├── 边缘案例生成器                                          │
│  └── 鲁棒性评估器                                           │
└─────────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
workspace/
├── agents/                          # 智能体模块
│   ├── requirement_decomposition_agent.py    # 需求拆解代理
│   ├── prompt_optimization_agent.py          # Prompt优化代理
│   ├── data_synthesis_agent.py               # 数据合成代理
│   └── adversarial_data_agent.py             # 攻防数据代理
├── tools/                           # 工具模块
│   └── llm_tools.py                 # LLM工具类和API接口
├── workflow/                        # 工作流模块
│   └── main_workflow.py             # 主工作流程
├── config/                          # 配置文件
│   └── config.yaml                  # 系统配置
├── PRD_context/                     # PRD文档目录
│   └── live_streaming_prd.md        # 直播脚本PRD示例
├── rd_suggestions/                  # RD建议目录
│   └── technical_optimization.md    # 技术优化建议示例
├── prompts/                         # Prompt模板目录
│   ├── gaming_script_template.txt   # 游戏直播脚本模板
│   └── beauty_script_template.txt   # 美妆直播脚本模板
├── evaluation_data/                 # 评估数据目录
│   └── script_evaluation_data.csv   # 评估数据示例
├── output/                          # 输出目录
├── base_dataset.jsonl               # 基础数据集
├── demo.py                          # 演示脚本
├── requirements.txt                 # Python依赖
└── README.md                        # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
cd /workspace

# 安装依赖（需要Python 3.8+）
pip install -r requirements.txt
```

### 2. 配置设置

编辑 `config/config.yaml` 配置文件：

```yaml
llm:
  model: "gpt-4-turbo-preview"
  temperature: 0.7
  max_tokens: 2048
  api_key: "your-openai-api-key"  # 配置你的API密钥

optimization:
  max_iterations: 5
  convergence_threshold: 0.05
  evaluation_batch_size: 10
```

### 3. 准备输入数据

将以下文件放入对应目录：

- **PRD文档**: 放入 `PRD_context/` 目录（支持.txt, .md格式）
- **RD建议**: 放入 `rd_suggestions/` 目录（支持.txt, .md格式）
- **评估数据**: 放入 `evaluation_data/` 目录（支持.xlsx, .csv格式）
- **Prompt模板**: 放入 `prompts/` 目录（支持.txt, .json格式）
- **基础数据集**: 根目录的 `base_dataset.jsonl`

### 4. 运行系统

```bash
# 运行演示
python demo.py

# 或者直接运行工作流
python -m workflow.main_workflow
```

## 📊 输出结果

系统执行完成后，会在 `output/` 目录生成以下文件：

```
output/
├── decomposed_tasks.json           # 拆解的任务列表
├── optimization_results.json       # Prompt优化结果
├── synthesized_data/               # 合成的训练数据
│   ├── task_001_synthesized.jsonl
│   ├── task_002_synthesized.jsonl
│   └── all_synthesized_data.jsonl
├── adversarial_data/               # 攻防测试数据
│   ├── adversarial_test_data.jsonl
│   ├── defensive_training_data.jsonl
│   └── security_analysis_report.json
├── final_training_data.jsonl       # 最终训练数据
└── workflow_report.json            # 工作流执行报告
```

## 🎛️ 核心功能

### 需求拆解Pipeline

- **PRD分析**: 自动提取产品需求的核心要点
- **RD建议分析**: 解析技术实现建议和优化点
- **评估数据解析**: 从Excel/CSV中提取评估维度和标准
- **任务拆解**: 将复杂需求拆解为可独立优化的子任务

### Prompt优化系统

- **评估流程拆解**: 设计多维度评估体系（主观/客观维度）
- **问题分析**: 识别常见错误类型和模式，生成few-shot示例
- **反馈收集**: 收集优化建议和改进方案
- **迭代优化**: 多轮优化直至达到质量阈值或收敛

### 数据合成引擎

- **输入变体生成**: 通过改写、扩展、简化等方式生成数据变体
- **质量评估**: 多维度质量评估（相关性、流畅性、创意性等）
- **响应精炼**: 迭代改进低质量响应
- **批量处理**: 高效的批量数据生成和处理

### 攻防数据生成

- **Prompt注入攻击**: 生成各种注入攻击测试用例
- **上下文操纵**: 测试模型对虚假上下文的抵抗能力
- **边缘案例**: 生成极端和边界情况的测试数据
- **防御数据**: 基于攻击结果生成防御性训练数据

## ⚙️ 配置选项

### LLM配置

```yaml
llm:
  model: "gpt-4-turbo-preview"     # 模型名称
  temperature: 0.7                 # 生成温度
  max_tokens: 2048                 # 最大令牌数
  api_base: ""                     # API基础URL
  api_key: ""                      # API密钥
```

### 优化配置

```yaml
optimization:
  max_iterations: 5                # 最大优化迭代次数
  convergence_threshold: 0.05      # 收敛阈值
  evaluation_batch_size: 10        # 评估批次大小
```

### 数据合成配置

```yaml
data_synthesis:
  output_format: "jsonl"           # 输出格式
  batch_size: 100                  # 批处理大小
  quality_threshold: 0.8           # 质量阈值
```

## 🔧 自定义扩展

### 添加新的Agent

1. 在 `agents/` 目录下创建新的Agent类
2. 继承基础Agent类并实现必要方法
3. 在主工作流中注册新的Agent

### 添加新的攻击场景

```python
new_scenario = AdversarialScenario(
    scenario_id="new_attack",
    name="新攻击类型",
    description="攻击描述",
    attack_type="attack_type",
    template_modifications={},
    expected_behavior="预期行为"
)
```

### 自定义评估维度

在配置文件中添加新的评估维度：

```yaml
evaluation:
  dimensions:
    subjective:
      - "新主观维度"
    objective:
      - "新客观维度"
```

## 📈 性能优化

- **并行处理**: 支持批量并行生成和评估
- **缓存机制**: 缓存常用模板和中间结果
- **增量更新**: 支持增量数据更新和模型优化
- **资源管理**: 智能资源分配和负载均衡

## 🔒 安全特性

- **多层安全检测**: 内容安全、格式检查、逻辑一致性
- **攻防测试**: 全面的鲁棒性和安全性测试
- **数据加密**: 敏感数据传输和存储加密
- **访问控制**: 严格的权限管理和审计日志

## 🤝 贡献指南

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue: [GitHub Issues](https://github.com/your-repo/issues)
- 邮箱: your-email@example.com

## 🙏 致谢

感谢以下开源项目的支持：

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [OpenAI API](https://openai.com/api/)

---

**注意**: 这是一个演示系统，在生产环境使用前请确保：
1. 配置正确的LLM API密钥
2. 根据实际需求调整配置参数
3. 进行充分的测试和验证
4. 遵守相关的数据安全和隐私规定