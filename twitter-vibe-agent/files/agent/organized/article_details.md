# 文章补充细节

## 可出题线索

### 问题种子
- 【问题种子】Codex 和 Claude Code 在 Agent 架构设计上有什么本质差异？
- 【问题种子】为什么 Claude Code 选择正则搜索而非向量数据库？
- 【问题种子】"以差异为中心"的代码修改理念具体解决了什么问题？
- 【问题种子】算法工程师如何选择适合自己项目的 AI 编码助手？
- 【问题种子】Codex 的 GitHub 集成与 Claude Code 的 GitHub 集成有何本质区别？
- 【问题种子】"懒加载" vs "主动扫描"：两种上下文策略适用于什么场景？
- 【问题种子】h2A 异步消息队列如何实现实时转向？
- 【问题种子】wU2 压缩器在上下文窗口达到多少百分比时自动触发？
- 【问题种子】为什么 Claude Code 限制最多一个子代理分支？
- 【问题种子】Claude.md 和 AGENTS.md 两种配置文件标准的差异是什么？

### 考察点
- 【考察点】对 Agent 工程架构的理解（单线程 ReAct 循环 vs 多智能体蜂群）
- 【考察点】对 Token 效率和成本优化的认知
- 【考察点】对沙箱安全机制的对比（OS 级 vs 应用级）
- 【考察点】对上下文管理策略的理解（懒加载 vs 主动扫描）
- 【考察点】对 "激进简单性" 设计哲学的理解
- 【考察点】对实时转向（Steering）技术实现的了解
- 【考察点】对配置文件最佳实践的掌握

### 回答要点
- 【回答要点】Codex：单代理 ReAct 循环、Shell 优先设计、apply_patch 差异修改、懒加载、OS 级沙箱
- 【回答要点】Claude Code：nO 主循环引擎、h2A 异步队列、wU2 压缩器、主动扫描、显式规划（TodoWrite）
- 【回答要点】两者共同理念：以差异为中心（diff-centric）、最小化可审查修改
- 【回答要点】选择标准：大型重构选 Claude Code，外科手术式编辑选 Codex

### 常见误区
- 【常见误区】认为 Claude Code 使用向量数据库（实际使用正则表达式 GrepTool）
- 【常见误区】认为 Codex 的隐式规划不如显式规划（隐式规划在快速迭代场景更优）
- 【常见误区】认为多智能体蜂群架构一定优于单线程（Claude Code 有意拒绝蜂群架构）
- 【常见误区】混淆 Claude.md 和 AGENTS.md 标准（两者不兼容）

### 可追问
- 【可追问】如果让你设计一个 AI 编码助手，你会选择哪种架构？为什么？
- 【可追问】在 Token 预算有限的情况下，如何优化上下文加载策略？
- 【可追问】你如何看待 "激进简单性" 这个设计哲学？
- 【可追问】你的项目中是否会使用 Claude.md/AGENTS.md？会包含哪些内容？

### 边界条件
- 【边界条件】对比结论基于 2025 年 9 月的文章，产品可能已更新
- 【边界条件】用户反馈具有主观性，实际体验可能因人而异
- 【边界条件】文中提到的性能数据（如 GPT-5 成本）需结合实际业务验证

### 层级区分
- 【基础】能够说出 Codex 和 Claude Code 的基本特点和差异
- 【进阶】能够解释背后的架构设计哲学和权衡
- 【专家】能够结合实际项目场景做出工具选择决策，并理解逆向工程技术细节

## 机制/原理要点

### Codex CLI 核心架构
- 单代理 ReAct 循环：`Think -> Tool Call -> Observe -> Repeat`
- 系统提示词教授"微型 API"，强制使用 apply_patch 进行外科手术式修改
- Shell 优先设计：使用 cat、grep、find 等 Unix 工具
- 隐式规划：通过迭代试错而非预先生成任务清单

### Claude Code 核心架构（代号）
- **nO（主循环引擎）**：单线程异步生成器，`while(tool_call) -> execute -> observe -> repeat`
- **h2A（异步消息队列）**：双重缓冲 + Promise 机制，支持每秒 10,000+ 条消息吞吐
- **wU2（压缩器）**：在上下文窗口达到 92% 时自动触发，基于重要性评分压缩
- **I2A（子代理/Task Agent）**：通过 dispatch_agent 调用，深度限制（禁止递归）

### 实时转向（Real-time Steering）
- 零延迟路径：当 nO 正在等待时，消息直接通过 Promise 传递
- 缓冲路径：当 nO 忙碌时，消息进入 primaryBuffer 排队
- 背压控制：防止内存溢出

### 以差异为中心（Diff-centric）
- 生成统一差异格式（Unified Diffs）
- 红色表示删除，绿色表示新增
- 用户审查后批准/拒绝/编辑，再应用到文件

## 工程实践/经验

### 配置文件最佳实践（基于 328 个项目实证研究）
- 软件架构（Software Architecture）：出现率 72.6%
- 开发指南（Development Guidelines）：44.8%
- 项目概览（Project Overview）：39%
- 测试（Testing）：35.4%
- 常用命令（Commands）：33.2%

### 常见配置模式（21.6% 的项目采用）
- 架构 + 依赖 + 项目概述 = "最小可行上下文"

### Claude Code 使用建议
- 使用 --dangerously-skip-permissions 跳过权限确认（但存在风险）
- 配置 CLAUDE.md 定义项目架构、代码风格、测试命令

### Codex 使用建议
- 配置 AGENTS.md 支持分层（Global -> Repo -> Subfolder）
- 利用 Git 信息聚焦当前修改的文件

## 数据/指标/对比

### 成本效率
- GPT-5 成本约为 Claude Sonnet 的一半
- GPT-5 成本约为 Claude Opus 的十分之一

### 用户满意度
- Builder.io 用户评分：GPT-5 比 Claude Sonnet 高 40%

### Token 限制痛点
- Claude Code 用户更频繁遇到额度限制
- Codex Pro 用户"几乎从未听说有人碰到限制"

### 上下文管理
- Codex：懒加载，Token 消耗低
- Claude Code：主动扫描，Token 消耗高

### wU2 压缩器
- 触发阈值：上下文窗口 92%
- 目标压缩比：约 30%（preserveRatio: 0.3）

## 案例/比喻

### nO 主循环引擎
- 类比：米其林餐厅的主厨
  - 单线程专注工作
  - 每完成一道菜才做下一道
  - 传菜员（h2A）可随时递送顾客紧急字条

### h2A 异步队列
- 类比：GPS 实时重路由
  - 传统 Agent：纸质地图，改路线需停车重画
  - Claude Code：智能 GPS，毫秒级重新计算

### Codex vs Claude Code
- 类比：急诊科医生 vs 城市规划师
  - Codex：急诊医生，直接处理伤口，快速高效
  - Claude Code：规划师，先看全貌再制定计划

### 懒加载 vs 主动扫描
- 类比：点菜 vs 自助餐
  - Codex：看菜单点菜，只付点的菜
  - Claude Code：自助餐，所有盘子端上来

### 配置文件
- 类比：新员工入职指南
  - CLAUDE.md：给高级外包开发的一页说明

### wU2 压缩器
- 类比：会议记录员
  - 白板写满 92% 时暂停
  - 总结关键点到笔记本
  - 擦掉大部分内容继续讨论

### 正则搜索 vs 向量数据库
- 类比：敏锐的图书管理员 vs 数字化目录
  - Claude Code：过目不忘的管理员，直接写检索条
  - 竞争对手：维护数字化目录系统

## 关键术语解释

- **ReAct 循环**：Reasoning + Acting，一种 Agent 模式，思考后行动，观察结果后重复
- **apply_patch**：Codex 使用的特殊命令，生成统一差异格式
- **激进简单性（Radical Simplicity）**：Claude Code 的设计哲学，选择简单方案而非复杂方案
- **受控并行（Controlled Parallelism）**：允许最多一个子代理分支，禁止递归
- **实时转向（Real-time Steering）**：用户可在 Agent 执行任务中途插入指令
- **懒加载（Lazy Loading）**：只读取明确请求的文件，默认不预加载
- **主动扫描（Proactive Scanning）**：自动加载相关文件建立跨文件上下文
- **AGENTS.md**：OpenAI/Cursor/Builder.io 支持的通用配置标准
- **CLAUDE.md**：Claude Code 专用的配置文件格式（不兼容 AGENTS.md）
- **Shell 优先**：优先使用 Unix 标准工具而非自定义 API
- **差异优先（Diff-first）**：只输出修改部分而非整个文件
- **Seatbelt**：macOS 的沙箱机制（Codex 使用）
- **h2A**：Claude Code 的异步双缓冲消息队列代号
- **nO**：Claude Code 的主循环引擎代号
- **wU2**：Claude Code 的上下文压缩器代号
- **I2A**：Claude Code 的子代理（Task Agent）代号
- **递归爆炸（Recursive Explosion）**：子代理无限自我复制导致系统崩溃
- **审计跟踪（Audit Trail）**：清晰的线性操作记录，便于调试
