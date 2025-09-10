import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import yaml


class RuntimeConfig(BaseSettings):
    prd_dir: str
    rd_dir: str
    eval_dir: str
    prompts_init_dir: str
    outputs_dir: str

    default_model: str
    embed_model: str
    temperature: float = 0.3
    max_tokens: int = 2048

    max_iterations: int = 4
    improvement_threshold: float = 0.01
    batch_size: int = 16

    refinement_passes: int = 2
    adversarial_num_variants: int = 8

    log_level: str = Field(default="INFO")


def load_runtime_config() -> RuntimeConfig:
    load_dotenv(override=False)
    with open(os.path.join("config", "config.yaml"), "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    paths = raw.get("paths", {})
    llm = raw.get("llm", {})
    opt = raw.get("prompt_optimization", {})
    syn = raw.get("synthesis", {})
    adv = raw.get("adversarial", {})
    log = raw.get("logging", {})

    # env-style substitution already supported via .env, fill defaults
    return RuntimeConfig(
        prd_dir=paths.get("prd_dir", "prd_context"),
        rd_dir=paths.get("rd_dir", "rd_context"),
        eval_dir=paths.get("eval_dir", "evaluation_data"),
        prompts_init_dir=paths.get("prompts_init_dir", "prompts_init"),
        outputs_dir=paths.get("outputs_dir", "outputs"),
        default_model=llm.get("default_model", os.getenv("DEFAULT_MODEL", "openai:gpt-4o-mini")),
        embed_model=llm.get("embed_model", os.getenv("EMBED_MODEL", "openai:text-embedding-3-small")),
        temperature=llm.get("temperature", 0.3),
        max_tokens=llm.get("max_tokens", 2048),
        max_iterations=opt.get("max_iterations", 4),
        improvement_threshold=opt.get("improvement_threshold", 0.01),
        batch_size=opt.get("batch_size", 16),
        refinement_passes=syn.get("refinement_passes", 2),
        adversarial_num_variants=adv.get("num_variants", 8),
        log_level=log.get("level", "INFO"),
    )