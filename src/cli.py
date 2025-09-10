import os
import json
import typer
from typing import Optional

from src.config.config_loader import load_runtime_config
from src.agents.requirement_decomposer import RequirementDecomposer
from src.agents.prompt_optimizer.graph import PromptOptimizationGraph
from src.agents.synthesis_pipeline import SynthesisPipeline
from src.agents.adversarial_agent import AdversarialAgent

app = typer.Typer(add_completion=False)


@app.command()
def decompose(
    prd_dir: str = typer.Option("prd_context", help="Directory with PRD docs"),
    rd_dir: str = typer.Option("rd_context", help="Directory with RD optimization notes"),
    eval_dir: str = typer.Option("evaluation_data", help="Directory with Excel evaluation sets"),
    out: str = typer.Option("outputs/decomposition.json", help="Output JSON file for tasks"),
):
    cfg = load_runtime_config()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    agent = RequirementDecomposer(cfg)
    tasks = agent.run(prd_dir=prd_dir, rd_dir=rd_dir, eval_dir=eval_dir)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    typer.echo(f"Saved tasks to {out}")


@app.command()
def optimize(
    task_id: Optional[str] = typer.Option(None, help="Task ID to optimize; if None, optimize all"),
    prompts_dir: str = typer.Option("prompts_init", help="Directory with initial prompts"),
    eval_dir: str = typer.Option("evaluation_data", help="Directory with Excel evaluation sets"),
    tasks_json: str = typer.Option("outputs/decomposition.json", help="Tasks JSON from decompose step"),
    out_dir: str = typer.Option("outputs/optimized", help="Directory to save optimized prompts and flows"),
):
    cfg = load_runtime_config()
    os.makedirs(out_dir, exist_ok=True)
    with open(tasks_json, "r", encoding="utf-8") as f:
        tasks = json.load(f)
    graph = PromptOptimizationGraph(cfg)
    _ = graph.run(tasks=tasks, task_id=task_id, prompts_dir=prompts_dir, eval_dir=eval_dir, out_dir=out_dir)
    typer.echo(f"Optimization complete. Saved to {out_dir}")


@app.command()
def synthesize(
    dataset: str = typer.Option(..., help="Input dataset (jsonl) to synthesize against"),
    out: str = typer.Option("outputs/synthesized.jsonl", help="Output synthesized dataset"),
    optimized_dir: str = typer.Option("outputs/optimized", help="Optimized prompts/templates directory"),
):
    cfg = load_runtime_config()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pipeline = SynthesisPipeline(cfg, optimized_dir=optimized_dir)
    num_written = pipeline.run(input_path=dataset, output_path=out)
    typer.echo(f"Wrote {num_written} synthesized records to {out}")


@app.command()
def adversarial(
    task_id: Optional[str] = typer.Option(None, help="Task ID for adversarial generation"),
    out: str = typer.Option("outputs/adversarial.jsonl", help="Output adversarial data"),
    optimized_dir: str = typer.Option("outputs/optimized", help="Optimized prompts/templates directory"),
):
    cfg = load_runtime_config()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    agent = AdversarialAgent(cfg, optimized_dir=optimized_dir)
    num_written = agent.run(task_id=task_id, output_path=out)
    typer.echo(f"Wrote {num_written} adversarial records to {out}")


if __name__ == "__main__":
    app()