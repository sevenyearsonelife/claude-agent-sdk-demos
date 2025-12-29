import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AgentDefinition,
    HookMatcher,
)

from twitter_vibe_agent.utils.message_handler import process_assistant_message
from twitter_vibe_agent.utils.subagent_tracker import SubagentTracker
from twitter_vibe_agent.utils.transcript import setup_session, TranscriptWriter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def ensure_dirs() -> None:
    (PROJECT_ROOT / "files" / "source_articles").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "files" / "dialogue_records").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "files" / "organized").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "files" / "generated_posts").mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "files" / "optimized_posts").mkdir(parents=True, exist_ok=True)


async def chat() -> None:
    load_dotenv()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n错误：未找到 ANTHROPIC_API_KEY。")
        print("请在 .env 中设置或在终端导出该变量。\n")
        return

    ensure_dirs()

    transcript_file, session_dir = setup_session()
    transcript = TranscriptWriter(transcript_file)

    lead_agent_prompt = load_prompt("lead_agent_zh.txt")
    content_organizer_prompt = load_prompt("content_organizer_zh.txt")
    content_generator_prompt = load_prompt("content_generator_zh.txt")
    quality_optimizer_prompt = load_prompt("quality_optimizer_zh.txt")

    agents = {
        "content-organizer": AgentDefinition(
            description=(
                "整理资料：分别处理高质量文章与对话记录，输出可用细节与用户理解/困惑点。"
            ),
            tools=["Skill", "Read", "Write", "Glob"],
            prompt=content_organizer_prompt,
            model="haiku",
        ),
        "content-generator": AgentDefinition(
            description=(
                "生成内容：基于整理资料与主题生成 Twitter 帖子草稿，必要时拆分为 Thread。"
            ),
            tools=["Skill", "Read", "Write", "Glob"],
            prompt=content_generator_prompt,
            model="haiku",
        ),
        "quality-optimizer": AgentDefinition(
            description=(
                "质量优化：对草稿进行去 AI 化与风格优化，输出最终可发布版本。"
            ),
            tools=["Skill", "Read", "Write", "Glob"],
            prompt=quality_optimizer_prompt,
            model="haiku",
        ),
    }

    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)

    hooks = {
        "PreToolUse": [
            HookMatcher(matcher=None, hooks=[tracker.pre_tool_use_hook]),
        ],
        "PostToolUse": [
            HookMatcher(matcher=None, hooks=[tracker.post_tool_use_hook]),
        ],
    }

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["user", "project"],
        system_prompt=lead_agent_prompt,
        allowed_tools=["Task"],
        agents=agents,
        model="haiku",
        cwd=PROJECT_ROOT,
        hooks=hooks,
    )

    transcript.write("\n" + "=" * 52)
    transcript.write("  Twitter Vibe Agent")
    transcript.write("=" * 52)
    transcript.write("\n输入你的需求，主 Agent 会先询问主题。")
    transcript.write("输入 'exit' 退出。\n")

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                if not user_input or user_input.lower() in {"exit", "quit", "q"}:
                    break

                transcript.write_to_file(f"\nYou: {user_input}\n")

                await client.query(prompt=user_input)

                transcript.write("\nAgent: ", end="")
                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        process_assistant_message(message, tracker, transcript)

                transcript.write("\n")
    finally:
        transcript.write("\n\nGoodbye!\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


if __name__ == "__main__":
    asyncio.run(chat())
