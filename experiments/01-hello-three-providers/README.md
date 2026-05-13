# 01 · Hello, Three Providers

**目的**：第一天打通三家 LLM API，对同一个 prompt 收集三家的输出和延迟，建立直观对比。

## 跑法

```bash
# 1. 在仓库根目录配置 .env
cp .env.example .env
# 填入 ANTHROPIC_API_KEY / GEMINI_API_KEY / DEEPSEEK_API_KEY

# 2. 安装依赖
uv sync

# 3. 跑！
uv run python experiments/01-hello-three-providers/hello.py
```

## 预期输出

一张表格，三行（Anthropic / Google / DeepSeek），列出 model、延迟、输出。

## 观察重点

- **延迟差异**：三家网络路径与模型规模不同，记下你看到的数值。
- **中文质量**：同一句中文 prompt，谁回答得最自然？谁最啰嗦？
- **回答风格**：Claude 更稳重、Gemini 更全面、DeepSeek 更简洁，是否符合你的体感？

## 作业（Day 1 产出）

### 我的实测结果

| Provider | Model | Latency (ms) | 我的评价 |
|---|---|---|---|
| Anthropic | (跳过)            | -     | 公司邮箱域名被拦，待用个人邮箱重注册 |
| Gemini    | gemini-2.5-pro    | 失败  | 中国大陆地区无免费 tier (limit: 0)；用智谱替代 |
| DeepSeek  | deepseek-chat     | 2398  | ⚡ 快；回答简洁 + 给了外汇交易实例 |
| Zhipu     | glm-4.6           | 39470 | 🧠 慢但准确（默认开启 thinking）；回答最精炼 |

### 关键发现（Day 1 学到的）

1. **OpenAI 兼容协议是事实标准**：DeepSeek、智谱、通义都能用 `openai` SDK 调，只换 `base_url`。这降低了多模型适配的工程成本。
2. **推理模型 vs 非推理模型的延迟差异巨大**：GLM-4.6 (thinking on) 比 DeepSeek-V3 慢 ~16 倍。任务匹配模型类型是工程决策。
3. **API key 配置的坑**：占位符前缀 `your-` 没删干净会直接 401；企业邮箱在某些 console 会被强制要求 organization。
4. **防御式编程**：`_missing()` 守卫让单个 key 缺失不会让整个脚本崩溃，多模型对比脚本必须这样写。
5. **限速错误的细节值得读**：Gemini 的 429 里 `limit: 0` 才是真问题（地区不支持），而不是"超额"。读错误信息要看细节。

## 常见坑

- **`ANTHROPIC_API_KEY` not found**：检查 `.env` 是否在仓库根目录、是否真的被 `load_dotenv()` 读到。
- **Gemini 429 / 403**：免费额度限速，过 1 分钟再试；或换 `gemini-2.5-flash`。
- **DeepSeek 余额不足**：登录 platform.deepseek.com 充值 ¥10 起。
- **网络问题**：Anthropic / Gemini 需要稳定的国际网络；DeepSeek 国内直连。
