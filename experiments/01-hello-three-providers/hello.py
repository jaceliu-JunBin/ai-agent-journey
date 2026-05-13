"""Day 1 — say hello to multiple LLM providers and compare.

Usage:
    uv run python experiments/01-hello-three-providers/hello.py

Providers (skipped automatically if API key is missing / still a placeholder):
- Anthropic Claude
- Google Gemini
- DeepSeek (OpenAI-compatible)
- Zhipu GLM   (OpenAI-compatible, recommended for users in mainland China)
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()
console = Console()

PROMPT = (
    "用一句话解释什么是 AI Agent，并给出一个金融场景的例子。"
    "限制在 80 字以内。"
)


@dataclass
class Result:
    provider: str
    model: str
    latency_ms: int
    content: str
    error: str | None = None


def _missing(key_name: str) -> bool:
    """Return True if env var is unset, empty, or still a placeholder."""
    v = os.getenv(key_name, "")
    return (not v) or v.startswith("your-") or v.startswith("YOUR-")


def _openai_compatible_call(
    provider: str, key_env: str, base_url_env: str, model_env: str, default_model: str
) -> Result:
    """Shared helper for any OpenAI-compatible API (DeepSeek, Zhipu, Qwen, etc.)."""
    if _missing(key_env):
        return Result(provider, "?", 0, "", error=f"SKIP: {key_env} not configured")
    from openai import OpenAI

    model = os.getenv(model_env, default_model)
    client = OpenAI(api_key=os.environ[key_env], base_url=os.environ[base_url_env])
    t0 = time.perf_counter()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT}],
    )
    dt = int((time.perf_counter() - t0) * 1000)
    return Result(provider, model, dt, resp.choices[0].message.content or "")


def call_anthropic() -> Result:
    if _missing("ANTHROPIC_API_KEY"):
        return Result("Anthropic", "?", 0, "", error="SKIP: ANTHROPIC_API_KEY not configured")
    from anthropic import Anthropic

    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.perf_counter()
    msg = client.messages.create(
        model=model,
        max_tokens=200,
        messages=[{"role": "user", "content": PROMPT}],
    )
    dt = int((time.perf_counter() - t0) * 1000)
    text = "".join(b.text for b in msg.content if b.type == "text")
    return Result("Anthropic", model, dt, text)


def call_gemini() -> Result:
    if _missing("GEMINI_API_KEY"):
        return Result("Gemini", "?", 0, "", error="SKIP: GEMINI_API_KEY not configured")
    from google import genai

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    t0 = time.perf_counter()
    resp = client.models.generate_content(model=model, contents=PROMPT)
    dt = int((time.perf_counter() - t0) * 1000)
    return Result("Gemini", model, dt, resp.text or "")


def call_deepseek() -> Result:
    return _openai_compatible_call(
        provider="DeepSeek",
        key_env="DEEPSEEK_API_KEY",
        base_url_env="DEEPSEEK_BASE_URL",
        model_env="DEEPSEEK_MODEL",
        default_model="deepseek-chat",
    )


def call_zhipu() -> Result:
    return _openai_compatible_call(
        provider="Zhipu",
        key_env="ZHIPU_API_KEY",
        base_url_env="ZHIPU_BASE_URL",
        model_env="ZHIPU_MODEL",
        default_model="glm-4.6",
    )


def safe_call(fn) -> Result:
    name = fn.__name__.replace("call_", "")
    try:
        return fn()
    except Exception as e:
        return Result(name, "?", 0, "", error=f"{type(e).__name__}: {e}")


def main() -> None:
    console.rule("[bold cyan]Day 1 - Multi-Provider Hello")
    console.print(f"[dim]Prompt:[/] {PROMPT}\n")

    providers = [call_anthropic, call_gemini, call_deepseek, call_zhipu]
    results = [safe_call(fn) for fn in providers]

    table = Table(title="Provider comparison", show_lines=True)
    table.add_column("Provider", style="cyan", no_wrap=True)
    table.add_column("Model", style="magenta")
    table.add_column("Latency (ms)", justify="right", style="green")
    table.add_column("Output", overflow="fold")
    for r in results:
        out = r.error if r.error else (r.content[:300] + ("..." if len(r.content) > 300 else ""))
        style = "yellow" if r.error and r.error.startswith("SKIP") else None
        table.add_row(r.provider, r.model, str(r.latency_ms), out, style=style)
    console.print(table)

    ok = sum(1 for r in results if not r.error)
    skipped = sum(1 for r in results if r.error and r.error.startswith("SKIP"))
    failed = sum(1 for r in results if r.error and not r.error.startswith("SKIP"))
    console.print(
        f"\n[bold]Summary:[/] {ok} ok · {skipped} skipped · {failed} failed",
        style="bold green" if failed == 0 else "bold yellow",
    )


if __name__ == "__main__":
    main()
