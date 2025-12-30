# Twitter Vibe Agent

基于 Claude Agent SDK 的多智能体系统，用于把你提供的资料整理成高质量的**大语言模型面试题**主题 Twitter 帖子。

## 快速开始

```bash
# 安装依赖（推荐 uv，也可用 pip）
uv sync

# 设置 API Key
export ANTHROPIC_API_KEY="your-api-key"

# 启动主 Agent
uv run python -m twitter_vibe_agent.agent
```

启动后，主 Agent 会先询问本次面试题的方向/岗位/难度/受众。
也可以基于 `.env.example` 创建本地 `.env`。

## 输入与输出位置

请将材料放在以下目录：
- **高质量文章** → `files/user/source_articles/`
- **对话记录** → `files/user/dialogue_records/`

子 Agent 的输入与输出：
- **Content Organizer**
  - 输入：`files/user/source_articles/`, `files/user/dialogue_records/`
  - 输出：`files/agent/organized/article_details.md`, `files/agent/organized/dialogue_insights.md`
- **Content Generator**
  - 输入：`files/agent/organized/article_details.md`, `files/agent/organized/dialogue_insights.md`
  - 输出：`files/agent/generated_posts/draft_posts.md`
- **Quality Optimizer**
  - 输入：`files/agent/generated_posts/draft_posts.md`
  - 输出：`files/agent/optimized_posts/final_posts.md`

## 工作流程

1. **Lead Agent** 询问主题并编排流程
2. 生成 **Content Organizer**：
   - 读取 `files/user/source_articles/` 与 `files/user/dialogue_records/`
   - 输出整理结果到 `files/agent/organized/`
3. 生成 **Content Generator**：
   - 根据主题与整理资料生成草稿
   - 写入 `files/agent/generated_posts/draft_posts.md`
4. 生成 **Quality Optimizer**：
   - 去 AI 化与风格优化
   - 写入 `files/agent/optimized_posts/final_posts.md`

## Agents

| Agent | Tools | 作用 |
|-------|-------|------|
| **Lead Agent** | `Task` | 询问主题并协调子 Agent |
| **Content Organizer** | `Skill`, `Read`, `Write`, `Glob` | 结构化整理资料并抽取出题线索 |
| **Content Generator** | `Skill`, `Read`, `Write`, `Glob` | 生成面试题帖子草稿 | 
| **Quality Optimizer** | `Skill`, `Read`, `Write`, `Glob` | 去 AI 化与风格优化 |

## Skills

内置 Skills 位于 `.claude/skills/`：

- `content-organizer`：提取出题线索、考察点、误区与要点
- `twitter-writer`：控制 250–280 字与 Thread 结构
- `vibe-polish`：去 AI 化与语言润色

## 示例输入

主 Agent 会询问：
> “本次想聚焦的大语言模型面试题方向/岗位/难度/受众是什么？”

示例：
- “偏 RAG 工程岗位，社招中高级，面向面试官视角”
- “偏对齐/安全，校招基础+进阶混合，面向求职者”
- “偏推理优化，专家级，面向技术负责人”

## 输出结构

```
files/
├── source_articles/        # 高质量文章
├── dialogue_records/       # 对话记录
├── organized/              # 整理结果
│   ├── article_details.md
│   └── dialogue_insights.md
├── generated_posts/        # 草稿
│   └── draft_posts.md
└── optimized_posts/        # 最终版本
    └── final_posts.md

logs/
└── session_YYYYMMDD_HHMMSS/
    ├── transcript.txt      # 会话记录
    └── tool_calls.jsonl    # 工具调用日志
```

## 子 Agent 追踪（Hooks）

系统通过 SDK hooks 追踪所有工具调用，并关联到子 Agent：

- **谁**：哪个子 Agent（CONTENT-ORGANIZER-1、CONTENT-GENERATOR-1 等）
- **做了什么**：工具名称（Read/Write/Glob/Skill）
- **何时**：时间戳
- **输入/输出**：参数与结果

`parent_tool_use_id` 将工具调用与 `Task` 创建的子 Agent 绑定，日志保存在 `logs/session_*/tool_calls.jsonl`。

## 目录结构

```
twitter-vibe-agent/
├── twitter_vibe_agent/
│   ├── agent.py
│   ├── prompts/
│   └── utils/
├── .claude/
│   └── skills/
├── files/
└── logs/
```

## 内置写作规则

- 每条帖子围绕 1 道高质量面试题
- 每条 250–280 个中文字符
- 超长内容拆分 Thread，逐条满足字数范围
- 优先使用整理资料中的机制/工程实践/数据/案例

## 贡献指南

参见 `CONTRIBUTING.md`。

## 行为准则

参见 `CODE_OF_CONDUCT.md`。

## 许可证

MIT License，参见 `LICENSE`。
