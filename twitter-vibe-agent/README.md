# Twitter Vibe Agent

A multi-agent system built with Claude Agent SDK that turns curated materials into high-quality Twitter posts about **LLM interview questions**.

## Quick Start

```bash
# Install dependencies (uv recommended, pip also works)
uv sync

# Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# Run the agent
uv run python -m twitter_vibe_agent.agent
```

When the agent starts, it will ask for the interview-question focus (direction/role/level/audience).
You can also create a local `.env` based on `.env.example`.

## Input & Output Locations

Provide your materials here:
- **High-quality articles** → `files/source_articles/`
- **Dialogue records** → `files/dialogue_records/`

Subagent inputs and outputs:
- **Content Organizer**
  - Inputs: `files/source_articles/`, `files/dialogue_records/`
  - Outputs: `files/organized/article_details.md`, `files/organized/dialogue_insights.md`
- **Content Generator**
  - Inputs: `files/organized/article_details.md`, `files/organized/dialogue_insights.md`
  - Outputs: `files/generated_posts/draft_posts.md`
- **Quality Optimizer**
  - Inputs: `files/generated_posts/draft_posts.md`
  - Outputs: `files/optimized_posts/final_posts.md`

## How It Works

1. **Lead Agent** asks for the focus and orchestrates the pipeline
2. Spawns **Content Organizer** to separate and structure inputs
   - Reads `files/source_articles/` and `files/dialogue_records/`
   - Outputs structured notes to `files/organized/`
3. Spawns **Content Generator** to draft tweets
   - Uses the focus + organized notes
   - Writes drafts to `files/generated_posts/draft_posts.md`
4. Spawns **Quality Optimizer** to polish
   - De-AI style cleanup + clarity improvements
   - Writes final posts to `files/optimized_posts/final_posts.md`

## Agents

| Agent | Tools | Purpose |
|-------|-------|---------|
| **Lead Agent** | `Task` | Ask for focus and coordinate subagents |
| **Content Organizer** | `Skill`, `Read`, `Write`, `Glob` | Structure source materials into question-ready signals |
| **Content Generator** | `Skill`, `Read`, `Write`, `Glob` | Draft interview-question tweets | 
| **Quality Optimizer** | `Skill`, `Read`, `Write`, `Glob` | De-AI polish and finalize style |

## Skills

Built-in skills live under `.claude/skills/`:

- `content-organizer` — extract question seeds, pitfalls, and answer points
- `twitter-writer` — enforce 250–280 Chinese characters and Thread structure
- `vibe-polish` — reduce AI tone, improve clarity and cadence

## Example Inputs

The Lead Agent will ask:
> “本次想聚焦的大语言模型面试题方向/岗位/难度/受众是什么？”

Examples:
- “偏 RAG 工程岗位，社招中高级，面向面试官视角”
- “偏对齐/安全，校招基础+进阶混合，面向求职者”
- “偏推理优化，专家级，面向技术负责人”

## Output Structure

```
files/
├── source_articles/        # Curated articles
├── dialogue_records/       # Conversation logs
├── organized/              # Structured notes
│   ├── article_details.md
│   └── dialogue_insights.md
├── generated_posts/        # Drafts
│   └── draft_posts.md
└── optimized_posts/        # Final posts
    └── final_posts.md

logs/
└── session_YYYYMMDD_HHMMSS/
    ├── transcript.txt      # Human-readable conversation
    └── tool_calls.jsonl    # Structured tool usage log
```

## Subagent Tracking with Hooks

All tool calls are tracked via SDK hooks and linked to subagents:

- **Who**: which subagent (CONTENT-ORGANIZER-1, CONTENT-GENERATOR-1, etc.)
- **What**: tool name (Read/Write/Glob/Skill)
- **When**: timestamp
- **Input/Output**: parameters and results

The `parent_tool_use_id` links tool calls to the subagent spawned by `Task`, and logs are written to `logs/session_*/tool_calls.jsonl`.

## Project Structure

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

## Writing Rules (Built-In)

- Each post centers on **one** LLM interview question
- 250–280 Chinese characters per post
- Long content is split into Thread entries, each within the range
- Use signals from organized notes (mechanisms, engineering practice, data, cases)

## Contributing

See `CONTRIBUTING.md`.

## Code of Conduct

See `CODE_OF_CONDUCT.md`.

## License

MIT License. See `LICENSE`.
