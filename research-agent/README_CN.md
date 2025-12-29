# 多智能体研究系统

一个多智能体研究系统，协调专业子代理研究任意主题，并生成带数据可视化的完整 PDF 报告。

## 快速开始

```bash
# Install dependencies
uv sync

# Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# Run the agent
uv run python research_agent/agent.py
```

然后询问："研究 2025 年量子计算的发展"

## 工作原理

1. **Lead Agent** 将请求拆分为 2-4 个子主题
2. 并行生成 **Researcher** 子代理进行网络搜索
3. 每个 Researcher 将发现保存到 `files/research_notes/`
4. 生成 **Data Analyst** 提取指标并在 `files/charts/` 生成图表
5. 生成 **Report Writer** 在 `files/reports/` 生成最终 PDF 报告

## 代理

| 代理 | 工具 | 目的 |
|------|------|------|
| **Lead Agent** | `Task` | 协调研究并向子代理分配任务 |
| **Researcher** | `mcp__tavily__tavily-search`, `Write` | 通过 Tavily MCP 从网络收集信息 |
| **Data Analyst** | `Glob`, `Read`, `Bash`, `Write` | 提取指标并生成图表 |
| **Report Writer** | `Skill`, `Write`, `Glob`, `Read`, `Bash` | 生成包含可视化的 PDF 报告 |

## 斜杠命令

| 命令 | 说明 |
|------|------|
| `/research <topic>` | 开始对任意主题的聚焦研究 |
| `/competitive-analysis <company>` | 分析公司或产品 |
| `/market-trends <industry>` | 研究行业趋势 |
| `/fact-check <claim>` | 验证主张与陈述 |
| `/summarize` | 汇总当前研究成果 |

## 示例查询

- "研究量子计算的发展"
- "可再生能源的当前趋势是什么？"
- `/competitive-analysis Tesla`
- `/market-trends artificial intelligence`

## 输出结构

```
files/
├── research_notes/     # 来自研究员的 Markdown 文件
├── data/               # 分析员的数据汇总
├── charts/             # PNG 可视化图表
└── reports/            # 最终 PDF 报告

logs/
└── session_YYYYMMDD_HHMMSS/
    ├── transcript.txt      # 可读的对话文本
    └── tool_calls.jsonl    # 结构化的工具调用日志
```

## 使用 Hooks 进行子代理追踪

系统通过 SDK hooks 跟踪所有工具调用。

### 追踪内容

- **谁**：哪个代理（RESEARCHER-1、DATA-ANALYST-1 等）
- **什么**：工具名称（mcp__tavily__tavily-search、Write、Bash 等）
- **何时**：时间戳
- **输入/输出**：参数与结果

### 工作方式

Hooks 在工具调用执行前后进行拦截：

```python
hooks = Hooks(
    pre_tool_use=[tracker.pre_tool_use_hook],
    post_tool_use=[tracker.post_tool_use_hook]
)
```

`parent_tool_use_id` 将工具调用关联到对应的子代理：
- Lead Agent 通过 `Task` 工具生成 Researcher → 获得 ID "task_123"
- 该 Researcher 的所有工具调用都包含 `parent_tool_use_id = "task_123"`
- Hooks 使用该 ID 识别具体发起调用的子代理

### 日志输出

**transcript.txt** - 可读文本：
```
[RESEARCHER-1] → mcp__tavily__tavily-search
    Input: query='quantum computing 2025'
[DATA-ANALYST-1] → Bash
    Input: python matplotlib chart generation
```

**tool_calls.jsonl** - 结构化 JSON：
```json
{"event":"tool_call_start","agent_id":"RESEARCHER-1","tool_name":"mcp__tavily__tavily-search",...}
{"event":"tool_call_complete","success":true,"output_size":15234}
```
