# Phase -1 · Python 基础（14 天）

> 为零基础的网络工程师设计 —— 不学全 Python，只学"能看懂 AI Agent 代码"所需的最小集合。

## 学习契约

1. **每天敲代码，不复制粘贴**。手敲是肌肉记忆，复制是欺骗自己。
2. **每天 commit**，哪怕只写了 3 行能跑的代码。GitHub 绿格子继续亮。
3. **卡住先 Google 10 分钟**，10 分钟后还卡才问。把每一个查的问题写到 `notes/questions.md`。
4. **不偷看后面的 day**。一天一个主题，循序渐进。
5. **第 14 天必须独立读懂 `experiments/01-hello-three-providers/hello.py` 的每一行**。这是出关考试。

## 时间预算

| 时段 | 时长 |
|---|---|
| 工作日晚上 | 2h |
| 工作日空档 | 2-3h |
| 周末 | 4h |
| **每周** | **~30h** |
| **14 天总计** | **~60h** |

## 主推荐资源（按使用频率）

| 资源 | 用法 | 链接 |
|---|---|---|
| 廖雪峰 Python 教程 | 主线读物，中文最经典 | https://liaoxuefeng.com/books/python/introduction/index.html |
| Python Tutor（可视化） | 看代码怎么一行行跑的 | https://pythontutor.com/ |
| Mosh 4-hour Python（视频） | 通勤 / 跑步时听 | https://www.youtube.com/watch?v=K5KVEU3aaeQ |
| Python 官方文档 | 查具体 API 时用 | https://docs.python.org/zh-cn/3/ |
| ChatGPT / Claude | 问"这段代码为什么不能跑"，**但不能让它替你写**！ | — |

## 14 天日级清单

| Day | 主题 | 核心概念 | 当日产出 |
|---|---|---|---|
| 1 | Python 是什么 + Hello World | 解释器、print、注释 | 第一个 .py 文件 + commit |
| 2 | 变量 + 基本数据类型 | int / float / str / bool / 类型转换 | 简单计算器 |
| 3 | 字符串操作 | 切片、f-string、常用方法 | 把姓名拆分 + 格式化打印 |
| 4 | 列表 list | append / pop / 遍历 / 索引 | 简易 TODO list |
| 5 | 字典 dict | key-value、嵌套结构 | 内存版"通讯录" |
| 6 | 条件 if / elif / else | 布尔逻辑、缩进规则 | 简单决策程序 |
| 7 | **周复盘 + 综合练习** | 整合 Day 1-6 | 迷你成绩管理系统 |
| 8 | 循环 for / while | range / break / continue | 九九乘法表 + 累加器 |
| 9 | 函数 def | 参数 / return / 作用域 | 把 Day 5 通讯录改写成函数版 |
| 10 | 模块 + import | os / json / datetime 标准库 | 读写 JSON 文件 |
| 11 | 文件操作 + with | open / read / write | 把通讯录持久化到磁盘 |
| 12 | 异常处理 try / except | 错误捕获、raise | 让通讯录"不会崩" |
| 13 | 类 class（轻量） | __init__ / self / 方法 | 用类重写通讯录 |
| 14 | **出关考试 · 回到 hello.py** | 综合应用 | 给 hello.py 加中文行内注释 |

## 每周打卡

### Week 1（Day 1-7）
- [ ] Day 1 · Hello World
- [ ] Day 2 · 变量 + 基本类型
- [ ] Day 3 · 字符串操作
- [ ] Day 4 · 列表 list
- [ ] Day 5 · 字典 dict
- [ ] Day 6 · 条件 if/elif/else
- [ ] Day 7 · 周复盘 + 综合练习

### Week 2（Day 8-14）
- [ ] Day 8 · 循环 for/while
- [ ] Day 9 · 函数 def
- [ ] Day 10 · 模块 + import
- [ ] Day 11 · 文件操作
- [ ] Day 12 · 异常处理
- [ ] Day 13 · 类 class
- [ ] Day 14 · 出关考试

## 工作流（每一天都这样）

```
1. 看 1 节廖雪峰对应章节       (~30 分钟)
2. 在 pythontutor.com 跑一遍示例代码，看变量怎么变    (~15 分钟)
3. 打开当天的练习目录 python-basics/day-XX/
4. 按 exercise.md 里的题目，自己写代码                (~60-90 分钟)
5. 跑通 → git commit -m "练习 day-XX"               (~5 分钟)
6. 在 notes/questions.md 记下今天遇到的问题（如有）
```

## 不学的东西（避免新手陷阱）

下面这些**先不要碰**，等真正用到再说：

- 装饰器 `@`（看到就跳过）
- 多线程 / 多进程
- async / await（Phase 1 才用）
- 元类、抽象基类
- `*args` / `**kwargs` 高级用法
- 复杂的继承、多继承、方法解析顺序
- 上下文管理器自实现（用 `with` 即可，不用知道怎么写一个）
- 类型注解的高级用法（基础的 `int`, `str`, `list[int]` 够用）

记住：**你的目标是看懂 AI Agent 代码并能修改**，不是当 Python 大神。

## 学完之后

完成 Day 14 后，你回到 `experiments/01-hello-three-providers/hello.py`，
**每一行你都能用中文讲清楚在干什么**。这时候你才算真正"做完了 Day 1"。

然后我们正式进入 Phase 0 → Phase 1 的 AI Agent 主线。
