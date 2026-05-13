"""Day 2 - Serial vs async-parallel LLM calls.

Demonstrates why LLM API calls are I/O bound and why asyncio.gather
makes N concurrent calls nearly free (total time approaches the slowest call).

Usage:
    uv run python experiments/02-async-comparison/async_compare.py
"""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import AsyncOpenAI
from rich.console import Console
from rich.table import Table

load_dotenv()
console = Console()

PROMPT = "用一句话解释什么是 RAG（检索增强生成），限制 40 字以内。"


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    key_env: str
    base_url: str
    model: str


# Use the fast Zhipu flash model here so the demo doesn't take 80s on serial mode.
# Day 1 we used glm-4.6 (thinking on) which is much slower.
PROVIDERS: list[ProviderSpec] = [
    ProviderSpec(
        name="DeepSeek",
        key_env="DEEPSEEK_API_KEY",
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
    ),
    ProviderSpec(
        name="Zhipu",
        key_env="ZHIPU_API_KEY",
        base_url="https://open.bigmodel.cn/api/paas/v4",
        model="glm-4-flash-250414",
    ),
]


@dataclass
class CallResult:
    name: str
    latency_ms: int
    content: str
    error: str | None = None


def _missing(env: str) -> bool:
    v = os.getenv(env, "")
    return (not v) or v.startswith("your-") or v.startswith("YOUR-")


async def one_call(spec: ProviderSpec) -> CallResult:
    if _missing(spec.key_env):
        return CallResult(spec.name, 0, "", error=f"SKIP: {spec.key_env} not configured")
    try:
        client = AsyncOpenAI(api_key=os.environ[spec.key_env], base_url=spec.base_url)
        t0 = time.perf_counter()
        resp = await client.chat.completions.create(
            model=spec.model,
            messages=[{"role": "user", "content": PROMPT}],
        )
        dt = int((time.perf_counter() - t0) * 1000)
        return CallResult(spec.name, dt, resp.choices[0].message.content or "")
    except Exception as e:
        return CallResult(spec.name, 0, "", error=f"{type(e).__name__}: {e}")


async def run_serial(specs: list[ProviderSpec]) -> tuple[float, list[CallResult]]:
    """Call each provider one after another."""
    t0 = time.perf_counter()
    results: list[CallResult] = []
    for spec in specs:
        results.append(await one_call(spec))
    total = time.perf_counter() - t0
    return total, results


async def run_parallel(specs: list[ProviderSpec]) -> tuple[float, list[CallResult]]:
    """Fire all providers concurrently with asyncio.gather."""
    t0 = time.perf_counter()
    results = await asyncio.gather(*(one_call(s) for s in specs))
    total = time.perf_counter() - t0
    return total, list(results)


def render_summary(
    serial_total: float,
    serial_results: list[CallResult],
    parallel_total: float,
    parallel_results: list[CallResult],
) -> None:
    table = Table(title="Serial vs Parallel", show_lines=True)
    table.add_column("Mode", style="cyan", no_wrap=True)
    table.add_column("Total (ms)", justify="right", style="green")
    table.add_column("Per-provider latency (ms)", style="dim")

    def fmt(results: list[CallResult]) -> str:
        return ", ".join(
            f"{r.name}={r.latency_ms}" + (" [SKIP]" if r.error and r.error.startswith("SKIP") else "")
            for r in results
        )

    table.add_row("Serial", f"{int(serial_total * 1000)}", fmt(serial_results))
    table.add_row("Parallel", f"{int(parallel_total * 1000)}", fmt(parallel_results))
    console.print(table)

    if parallel_total > 0:
        speedup = serial_total / parallel_total
        verdict = (
            "[bold green]Free lunch![/]" if speedup > 1.5
            else "[yellow]Modest gain[/]"
        )
        console.print(f"\nSpeedup: [bold]{speedup:.2f}x[/]   {verdict}")
        console.print(
            "[dim]Theory: parallel total ~= max(individual latencies); "
            "serial total ~= sum(individual latencies).[/]"
        )


async def main() -> None:
    console.rule("[bold cyan]Day 2 - Serial vs Async-Parallel")
    console.print(f"[dim]Prompt:[/] {PROMPT}\n")

    console.print("[yellow]>>> Running SERIAL...[/]")
    serial_total, serial_results = await run_serial(PROVIDERS)

    console.print("[yellow]>>> Running PARALLEL...[/]")
    parallel_total, parallel_results = await run_parallel(PROVIDERS)

    render_summary(serial_total, serial_results, parallel_total, parallel_results)

    console.rule("[bold]Outputs (from parallel run)")
    for r in parallel_results:
        if r.error:
            console.print(f"[red]{r.name}:[/] {r.error}")
        else:
            console.print(f"[cyan]{r.name}[/] ({r.latency_ms} ms):  {r.content}")


if __name__ == "__main__":
    asyncio.run(main())
