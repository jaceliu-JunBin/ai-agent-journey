# AI Agent Journey

> 6 个月从零到资深 AI Agent 工程师的公开学习记录。
> 目标岗位：上海百亿私募 AI Agent 工程师。

## 路线总览

| Phase | 主题 | 周次 | 状态 |
|---|---|---|---|
| 0 | 基础准备（Python / 环境 / API） | W1 | ⏳ 进行中 |
| 1 | LLM 基础与 API 使用 | W2–W4 | ⬜ |
| 2 | Prompt Engineering 深入 | W5–W6 | ⬜ |
| 3 | Tool Use / Function Calling / MCP | W7–W8 | ⬜ |
| 4 | RAG（检索增强生成） | W9–W11 | ⬜ |
| 5 | Agent 原理与框架 | W12–W15 | ⬜ |
| 6 | 多 Agent 系统与 Workflow | W16–W18 | ⬜ |
| 7 | 评测体系（Eval） | W19–W20 | ⬜ |
| 8 | 工程落地（部署 / 监控 / 成本 / 安全） | W21–W22 | ⬜ |
| 9 | 金融领域应用 | W23 | ⬜ |
| 10 | 作品集 + 面试冲刺 | W24 | ⬜ |

## 第 1 周任务清单（Phase 0）

- [ ] Day 1 — 三家 API 打通（Claude / Gemini / DeepSeek）
- [ ] Day 2 — async / Pydantic 补强 + 并发调用对比
- [ ] Day 3 — Karpathy《Intro to LLMs》笔记
- [ ] Day 4 — Transformer 直觉建立（3B1B + Illustrated Transformer）
- [ ] Day 5 — Streaming + Structured Output 实战
- [ ] Day 6 — 采样参数实验（temperature / top_p）
- [ ] Day 7 — 周复盘 + 第一篇公开博客

## 第 2 周任务清单（Phase 1 第一周）

- [ ] Day 8 — Tokenization 深入（Karpathy "Build the Tokenizer"）
- [ ] Day 9 — Context Window 与长文本策略
- [ ] Day 10 — Prompt Caching 实战
- [ ] Day 11 — Vision / 多模态
- [ ] Day 12 — 五模型 micro-benchmark
- [ ] Day 13 — 《Attention Is All You Need》前半 + 论文阅读法
- [ ] Day 14 — 周复盘 + 第二篇公开博客

## 仓库结构

```
ai-agent-journey/
├── README.md                  # 本文件（总进度）
├── .env.example               # API key 模板
├── .gitignore
├── pyproject.toml             # uv / pip 依赖
├── notes/                     # 学习笔记
│   └── questions.md           # 累积疑问，定期回填
├── weekly/                    # 每周复盘
│   └── week-01.md
└── experiments/               # 实验代码（按日期/主题）
    └── 01-hello-three-providers/
        ├── README.md
        └── hello.py
```

## 守则（贯穿全程）

1. 每天必须 commit，哪怕只是一行笔记。
2. 不懂的概念立刻记到 `notes/questions.md`，定期回填。
3. 每周必须公开输出一次（博客 / 即刻 / 小红书 / X 任选）。

## 快速开始

```bash
# 1. 安装 uv (https://docs.astral.sh/uv/)
# Windows PowerShell:
#   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. 装依赖
uv sync

# 3. 配置 API key
cp .env.example .env
# 然后编辑 .env，填入真实 key

# 4. 跑 Day 1 实验
uv run python experiments/01-hello-three-providers/hello.py
```
