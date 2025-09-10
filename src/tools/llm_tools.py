from __future__ import annotations
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential

import httpx

try:
    import openai as openai_lib
except Exception:
    openai_lib = None

try:
    import anthropic as anthropic_lib
except Exception:
    anthropic_lib = None

try:
    import groq as groq_lib
except Exception:
    groq_lib = None


@dataclass
class LLMConfig:
    default_model: str
    temperature: float
    max_tokens: int


class LLMTools:
    def __init__(self, config: LLMConfig):
        self.config = config

    def _parse_provider(self, model_id: str) -> Tuple[str, str]:
        if ":" in model_id:
            provider, model = model_id.split(":", 1)
            return provider, model
        return "openai", model_id

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=6))
    def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None, temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        provider, model_name = self._parse_provider(model or self.config.default_model)
        temp = temperature if temperature is not None else self.config.temperature
        max_toks = max_tokens if max_tokens is not None else self.config.max_tokens

        if provider == "openai" and openai_lib and os.getenv("OPENAI_API_KEY"):
            client = openai_lib.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            resp = client.chat.completions.create(model=model_name, messages=messages, temperature=temp, max_tokens=max_toks)
            return resp.choices[0].message.content
        if provider == "anthropic" and anthropic_lib and os.getenv("ANTHROPIC_API_KEY"):
            client = anthropic_lib.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            resp = client.messages.create(model=model_name, max_tokens=max_toks, temperature=temp, messages=messages)
            return "\n".join([b.get("text", "") if isinstance(b, dict) else str(b) for b in getattr(resp, "content", [])])
        if provider == "groq" and groq_lib and os.getenv("GROQ_API_KEY"):
            client = groq_lib.Groq(api_key=os.getenv("GROQ_API_KEY"))
            resp = client.chat.completions.create(model=model_name, messages=messages, temperature=temp, max_tokens=max_toks)
            return resp.choices[0].message.content

        # Fallback mock
        return self._mock_chat(messages)

    def _mock_chat(self, messages: List[Dict[str, str]]) -> str:
        last = messages[-1]["content"] if messages else ""
        return f"[MOCK_MODEL_OUTPUT] {last[:200]}"

    def embed(self, texts: List[str]) -> List[List[float]]:
        # Lightweight deterministic mock embeddings (Jaccard-like hashing)
        vectors: List[List[float]] = []
        for text in texts:
            buckets = [0.0] * 64
            for token in text.split():
                idx = hash(token) % 64
                buckets[idx] += 1.0
            norm = sum(v * v for v in buckets) ** 0.5 or 1.0
            vectors.append([v / norm for v in buckets])
        return vectors