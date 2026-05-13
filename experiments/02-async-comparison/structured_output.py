"""Day 2 - Pydantic + LLM structured output: financial announcement extraction.

Goal: extract a typed, validated event record from a Chinese-language
corporate announcement. This is the foundation of every Agent tool call:
the LLM returns JSON, we parse & validate it as a Pydantic object, and
business code consumes the typed object (never the raw string).

Usage:
    uv run python experiments/02-async-comparison/structured_output.py
"""

from __future__ import annotations

import json
import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()


# --------- 1. Pydantic schema ---------

EventType = Literal[
    "收购",
    "股权变动",
    "业绩公告",
    "分红",
    "诉讼",
    "高管变动",
    "其他",
]


class AnnouncementEvent(BaseModel):
    """A single structured event extracted from a corporate announcement."""

    company: str = Field(description="公司全称")
    stock_code: str | None = Field(default=None, description="A 股股票代码（6 位数字）；没有则为 null")
    event_type: EventType = Field(description="事件类型，必须是给定枚举之一")
    amount_cny: float | None = Field(default=None, description="涉及金额，单位人民币元（注意亿元要换算）；没有则为 null")
    event_date: str | None = Field(default=None, description="事件发生日期，格式 YYYY-MM-DD；没有则为 null")
    summary: str = Field(description="一句话摘要，不超过 50 个中文字符")


# --------- 2. Sample announcement (synthetic, not a real company) ---------

SAMPLE_ANNOUNCEMENT = """
【星河智能股份有限公司关于现金收购杭州智云科技有限公司 100% 股权的公告】

证券代码：300999    证券简称：星河智能    公告编号：2025-018

本公司及董事会全体成员保证信息披露的内容真实、准确、完整，没有虚假记载、
误导性陈述或重大遗漏。

一、交易概述
公司董事会于 2025 年 3 月 18 日召开第十二届董事会第三次会议，审议通过了
《关于以现金方式收购杭州智云科技有限公司 100% 股权的议案》。本次交易作价
人民币 12.6 亿元，资金来源为公司自有资金及银行并购贷款。交易完成后，
杭州智云将成为本公司的全资子公司。

二、交易目的
本次收购旨在加强公司在 AI Agent 领域的技术布局，提升公司在大模型应用
工程化方向的核心竞争力。
"""


# --------- 3. Provider config ---------

PROVIDERS = [
    {
        "name": "DeepSeek",
        "key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    {
        "name": "Zhipu",
        "key_env": "ZHIPU_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4.6",
    },
]


def _missing(env: str) -> bool:
    v = os.getenv(env, "")
    return (not v) or v.startswith("your-") or v.startswith("YOUR-")


def build_prompt() -> str:
    """Build a prompt that embeds the Pydantic-generated JSON schema."""
    schema_json = json.dumps(
        AnnouncementEvent.model_json_schema(),
        indent=2,
        ensure_ascii=False,
    )
    return f"""你是一名金融公告信息抽取专家。请从下面的公告原文中抽取一条关键事件，
**严格按照给定的 JSON Schema 返回**。要求：
1. 只输出 JSON 对象，不要任何解释文字、不要 markdown 代码块包裹。
2. 金额必须换算为以元为单位的数字（例：12.6 亿元 -> 1260000000）。
3. 日期格式必须是 YYYY-MM-DD。
4. event_type 必须从 schema 中给定的枚举里选一个。

JSON Schema:
{schema_json}

公告原文:
{SAMPLE_ANNOUNCEMENT}
""".strip()


def extract(provider: dict) -> tuple[str, AnnouncementEvent | None, str | None]:
    """Call one provider and try to parse the response into AnnouncementEvent.

    Returns: (raw_response, parsed_event_or_None, error_message_or_None)
    """
    if _missing(provider["key_env"]):
        return ("", None, f"SKIP: {provider['key_env']} not configured")

    try:
        client = OpenAI(
            api_key=os.environ[provider["key_env"]],
            base_url=provider["base_url"],
        )
        resp = client.chat.completions.create(
            model=provider["model"],
            messages=[{"role": "user", "content": build_prompt()}],
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        raw = resp.choices[0].message.content or ""
    except Exception as e:
        return ("", None, f"{type(e).__name__}: {e}")

    try:
        event = AnnouncementEvent.model_validate_json(raw)
        return (raw, event, None)
    except ValidationError as ve:
        return (raw, None, f"Pydantic validation failed: {ve}")
    except Exception as e:
        return (raw, None, f"JSON parse failed: {type(e).__name__}: {e}")


def render_result(name: str, raw: str, event: AnnouncementEvent | None, err: str | None) -> None:
    console.rule(f"[bold magenta]{name}")
    if err and err.startswith("SKIP"):
        console.print(f"[yellow]{err}[/yellow]")
        return
    if err:
        console.print(Panel(raw or "(empty)", title="Raw response", border_style="red"))
        console.print(f"[red]{err}[/red]")
        return
    assert event is not None
    pretty = event.model_dump_json(indent=2)
    console.print(Panel(pretty, title=f"{name} - validated AnnouncementEvent", border_style="green"))


def main() -> None:
    console.rule("[bold cyan]Day 2 - Structured Output: Financial Announcement")
    console.print(Panel(SAMPLE_ANNOUNCEMENT.strip(), title="原文 (合成样本)", border_style="dim"))

    for provider in PROVIDERS:
        raw, event, err = extract(provider)
        render_result(provider["name"], raw, event, err)

    console.rule("[bold]Tip")
    console.print(
        "[dim]The fact that you get a typed AnnouncementEvent (not a string) is the whole point.\n"
        "Downstream Agent code can do: if event.event_type == '收购': trigger_workflow(event).[/]"
    )


if __name__ == "__main__":
    main()
