# 02 · Async Concurrency + Structured Output

**Day 2 主题**：把同步 → 异步、把字符串 → 类型安全的结构化数据。

## 为什么这两件事必须现在学

LLM 调用的本质是**网络 I/O**（每次 2-5 秒等模型返回）。两个工程事实：

1. **N 个独立 LLM 调用并发**几乎免费 —— async 让总耗时从 `sum(latencies)` 降到 `max(latencies)`。
   - 你 Day 1 看到 DeepSeek 2.4s + GLM-4.6 39.5s = 串行 42s
   - 并发后 ≈ 39.5s（被最慢的拖）
   - 真正生产场景你常常要并发 10-100 次（批量打分、多 Agent、检索 N 个候选）

2. **Agent 的工具调用 100% 依赖结构化输出**。LLM 返回的不能是"自由作文"，必须是机器能解析、能验证、能 fail-fast 的 JSON。Pydantic 就是 Python 里做这件事的事实标准。
   - Function Calling → JSON Schema
   - MCP Tool → JSON Schema
   - Agent State → Pydantic Model
   - 业务输出 → Pydantic Model

**今天这两个文件，是你后面所有 Agent 代码的基石。**

## 文件说明

| 文件 | 演示什么 |
|---|---|
| `async_compare.py` | 同样 N 个调用，串行 vs `asyncio.gather` 并发的速度对比 |
| `structured_output.py` | 用 Pydantic 定义"金融公告事件"schema，让 DeepSeek 和 GLM 抽取一段公告，并自动验证返回值 |

## 跑法

```bash
# 在仓库根目录
uv run python experiments/02-async-comparison/async_compare.py
uv run python experiments/02-async-comparison/structured_output.py
```

## Day 2 作业（必须产出）

### 1. async_compare 实测表

| 模式 | 总耗时 (ms) | 各家延迟 (ms) |
|---|---|---|
| 串行 (serial) |  |  |
| 并发 (parallel) |  |  |
| **加速比** | `serial / parallel` = ?x |  |

### 2. structured_output 抽取对比

| Provider | 公司名 | 股票代码 | 事件类型 | 金额 (元) | 日期 | 摘要 | 验证通过? |
|---|---|---|---|---|---|---|---|
| DeepSeek |  |  |  |  |  |  |  |
| Zhipu    |  |  |  |  |  |  |  |

### 3. 思考题（写到 notes 里）

- 假如你要并发 100 个 LLM 调用，async 还够吗？还需要补什么？（提示：限流、信号量）
- Pydantic schema 里把 `event_type` 限制成 Literal 而不是 str，工程上的好处是什么？
- 如果 LLM 返回的 JSON 漏了 `summary` 字段，会发生什么？怎么让 Agent 优雅恢复？

## 关键概念速查

- **asyncio.gather(*coros)**：把多个 coroutine 同时跑，等所有完成
- **AsyncOpenAI**：openai SDK 的异步 client（DeepSeek/Zhipu 都用它，因为是 OpenAI 兼容）
- **Pydantic BaseModel**：声明式数据校验，自动生成 JSON Schema
- **response_format={"type": "json_object"}**：强制 LLM 返回合法 JSON
- **model_validate_json(raw)**：把 LLM 返回的 JSON 字符串解析 + 校验成 Pydantic 对象
