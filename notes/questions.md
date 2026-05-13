# Open Questions

> 学习过程中遇到的不懂的概念、卡住的问题，都先记到这里。
> 每周复盘时回头看，能消化掉的标 ✅ 并补一句话答案。
> 没消化的留下来下周继续，避免被一个点卡住停滞不前。

## 模板

```
- [ ] YYYY-MM-DD · 主题 · 一句话描述问题
      上下文（看的什么资料、卡在哪一段）
      尝试过的查找路径
```

## 当前问题

- [✅] 2026-05-13 · uv · 什么是 uv？
      上下文：Day 1 跑 hello.py 用到 `uv sync` / `uv run python`，想理解工具角色
      答：Python 的"项目管家"（Rust 写，Astral 出品），一站式做 ——
      装 Python / 创建虚拟环境 `.venv` / 解析 + 下载依赖 / 生成 `uv.lock` /
      跑脚本（`uv run` 自动用 `.venv` 的 Python，不用手动 activate）。
      比 pip + venv + pyenv + pip-tools 组合快 10-100 倍，一个工具替代过去 4-5 个。

- [✅] 2026-05-13 · 依赖 · 什么是依赖（dependency）？
      上下文：Day 1 看到 pyproject.toml 里 `dependencies = [...]`，想理解为什么这么写
      答：代码里 `from xxx import yyy` 用到的、由别人写好开源在 PyPI（Python 公共仓库）
      的库，统称依赖。`pyproject.toml` 声明你要哪些依赖 + 版本约束（如 `anthropic>=0.40.0`），
      `uv.lock` 锁定每个依赖的精确版本（含传递依赖），`.venv\` 是本项目专属环境
      （与系统 Python / 其他项目互相隔离）。
      价值：不重复造轮子 + 版本可控 + 任何人 clone 后能 1:1 复现你的环境。

<!-- 在下面追加新问题，例如：

- [ ] 2026-05-14 · Tokenizer · 为什么中文比英文 token 多？
      看 Karpathy "Build the Tokenizer" 第 12 分钟
      已查：BPE 维基，但还不理解为什么中文倾向于按字符切

-->
