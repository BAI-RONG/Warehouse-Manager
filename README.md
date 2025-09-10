### Multi-Agent Prompt Optimization and Data Synthesis Pipelines

This project provides a LangChain/LangGraph-based multi-agent workflow to:
- Requirement decomposition from PRD and RD inputs
- Prompt optimization with evaluators, error analysis, and iterative refinement
- Dataset synthesis using optimized prompts and response refinement
- Adversarial (攻防) data generation to create edge cases

#### Directory Layout
- `config/config.yaml`: Global configuration (models, limits, paths)
- `src/`: Source code
  - `agents/`: Agents and graphs
  - `tools/`: LLM and retrieval tools
  - `loaders/`: Data loaders for PRD/RD text and Excel evaluation sets
  - `config/`: Config loader utilities
- `evaluation_data/`: Excel evaluation sets (.xlsx)
- `prd_context/`: PM PRD materials (text/markdown)
- `rd_context/`: RD optimization notes (text/markdown)
- `prompts_init/`: Initial prompts per task (YAML/JSON or .txt)

#### Quickstart
1) Python 3.10+ recommended.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

2) Configure `config/config.yaml` and prepare input directories.

3) Run CLI:
```bash
python -m src.cli decompose --prd-dir prd_context --rd-dir rd_context --eval-dir evaluation_data
python -m src.cli optimize --task-id <TASK_ID> --prompts-dir prompts_init --eval-dir evaluation_data
python -m src.cli synthesize --dataset data/input.jsonl --out data/synth.jsonl
python -m src.cli adversarial --task-id <TASK_ID> --out data/adv.jsonl
```

See inline `--help` for more options.

#### Notes
- Providers are optional; the LLM wrapper will fall back to a local mock if keys are missing.
- Excel evaluation parsing is dynamic; expected columns are inferred. Placeholders are provided for custom metrics.