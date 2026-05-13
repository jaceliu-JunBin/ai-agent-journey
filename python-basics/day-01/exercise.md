# Day 1 · Hello, Python

**目标**：跑通你写的**第一个** Python 程序，理解"解释器"和"注释"是什么。

预计用时：2-2.5 小时。

---

## 1. 先看（30 分钟）

打开廖雪峰教程，按顺序看完这 3 节：

1. https://liaoxuefeng.com/books/python/introduction/index.html （Python 简介）
2. https://liaoxuefeng.com/books/python/install/index.html （安装 Python —— 你已经用 uv 装好了，扫一眼跳过即可）
3. https://liaoxuefeng.com/books/python/first-program/index.html （第一个 Python 程序）

## 2. 再做（90 分钟）

### 练习 1.1 · 经典 Hello World

在 `python-basics/day-01/` 目录下新建 `01_hello.py`，用记事本或 VSCode 打开，写下这一行：

```python
print("Hello, AI Agent!")
```

在 PowerShell 跑：

```powershell
cd "D:\Claude Code\ai-agent-journey"
uv run python python-basics\day-01\01_hello.py
```

**预期输出**：`Hello, AI Agent!`

**思考**（写到下面 Tips 段下方的"我的笔记"）：
- `print` 是什么？为什么后面要加括号？
- 为什么字符串要用引号包起来？
- 不加引号会怎样？（去掉引号试试，看报错）

---

### 练习 1.2 · 多行 + 注释

新建 `02_intro.py`：

```python
# 这是一个单行注释，Python 会忽略它
# 注释的作用：告诉读代码的人（包括三天后的你自己）这段代码在干嘛

print("我叫 Jace")
print("我是网络工程师，正在学 AI Agent")
print("今天是 Python 第 1 天")

"""
这是多行注释（其实是字符串，但放在这里 Python 不会执行它）
通常用来写函数的说明文档
"""

print("=" * 30)   # 这一行会打印 30 个等号
print("END")
```

跑一下：

```powershell
uv run python python-basics\day-01\02_intro.py
```

**思考**：
- `"=" * 30` 为什么会出现 30 个等号？这说明 Python 里**字符串可以"乘以"数字**，这是后面会大量用到的特性。
- `#` 注释和 `"""..."""` 注释的区别是什么？

---

### 练习 1.3 · 改造练习（这是最重要的一步）

把 `02_intro.py` 改成你自己的版本：

- 改成 5 行 print，介绍**你自己**
- 加一行注释解释为什么写这个文件
- 最下面用 `*` 而不是 `=` 打印 40 个分隔符

**禁止使用 AI 帮你写**。卡住就回头看 1.2 的代码，照着改。

---

## 3. Tips 给新手

- **PowerShell 里反斜杠 `\` 用来分隔路径**（Windows 风格），写代码时字符串里出现 `\` 要写成 `\\` 或用 `r"..."` 原始字符串。新手暂时遇不到，但看到时不要慌。
- **Python 文件名建议小写 + 下划线**（如 `01_hello.py`），不要用中文、空格、连字符。
- **每次只改一行，立刻跑**。一次改 10 行出错你根本不知道哪行的锅。
- **报错信息从下往上读**，最底下那行通常告诉你"哪个文件、第几行、什么错"。

---

## 4. 自测 checklist

跑通三个练习后，看看你能不能口头回答：

- [ ] `print` 和"代码"的区别是什么？（提示：`print` 是 Python 提供的功能；"代码"是任何 Python 指令）
- [ ] 注释会被执行吗？（不会）
- [ ] 字符串的两个表示方法是什么？（`"..."` 和 `'...'`，等价）
- [ ] 一个 `.py` 文件可以被运行多次吗？（可以）
- [ ] `print("a" * 3)` 输出什么？（`aaa`）

全部能答上来 → Day 1 通过。

---

## 5. 我的笔记（写到下面）

> 学完后在这里写下你今天的 3 个发现 / 困惑。诚实写，不要写"我懂了"。

1. 
2. 
3. 

---

## 6. 完成后

```powershell
cd "D:\Claude Code\ai-agent-journey"
git add python-basics/
git commit -m "feat: python basics day 1 - hello world"
git push
```

回到 `python-basics/README.md` 把 Day 1 的 checkbox 打勾 `[x]`。

明天来 Day 2（变量 + 基本数据类型）。
