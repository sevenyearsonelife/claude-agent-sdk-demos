import asyncio
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    HookContext,
    HookMatcher,
    TextBlock,
)

PROMPT = "Hello, Claude! Please introduce yourself in one sentence."
ALLOWED_TOOLS = [
    "Task",
    "Bash",
    "Glob",
    "Grep",
    "LS",
    "ExitPlanMode",
    "Read",
    "Edit",
    "MultiEdit",
    "Write",
    "NotebookEdit",
    "WebFetch",
    "TodoWrite",
    "WebSearch",
    "BashOutput",
    "KillBash",
]
AGENT_DIR = Path.cwd() / "agent"


async def enforce_script_location(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    tool_name = input_data.get("tool_name")
    if tool_name not in {"Write", "Edit", "MultiEdit"}:
        return {"continue_": True}

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path") or ""
    if not file_path:
        return {"continue_": True}

    ext = Path(file_path).suffix.lower()
    if ext not in {".js", ".ts"}:
        return {"continue_": True}

    custom_scripts_dir = Path.cwd() / "agent" / "custom_scripts"
    custom_scripts_path = str(custom_scripts_dir)
    if not file_path.startswith(custom_scripts_path):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "Script files (.js and .ts) must be written to the custom_scripts directory. "
                    f"Please use the path: {custom_scripts_path}/{Path(file_path).name}"
                ),
            }
        }

    return {"continue_": True}


async def main() -> None:
    hooks = {
        "PreToolUse": [
            HookMatcher(matcher="Write|Edit|MultiEdit", hooks=[enforce_script_location])
        ]
    }
    options = ClaudeAgentOptions(
        max_turns=100,
        cwd=AGENT_DIR,
        model="opus",
        allowed_tools=ALLOWED_TOOLS,
        hooks=hooks,
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt=PROMPT)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                text_block = next(
                    (block for block in message.content if isinstance(block, TextBlock)),
                    None,
                )
                if text_block:
                    print("Claude says:", text_block.text)


if __name__ == "__main__":
    asyncio.run(main())
