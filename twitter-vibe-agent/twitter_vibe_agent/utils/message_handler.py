"""Message handling for processing agent responses."""

from typing import Any


_tool_just_used = False


def process_assistant_message(msg: Any, tracker: Any, transcript: Any) -> None:
    """Process an AssistantMessage and write output to transcript.

    Args:
        msg: AssistantMessage to process
        tracker: SubagentTracker instance
        transcript: TranscriptWriter instance
    """
    global _tool_just_used

    parent_id = getattr(msg, "parent_tool_use_id", None)
    tracker.set_current_context(parent_id)

    for block in msg.content:
        block_type = type(block).__name__

        if block_type == "TextBlock":
            if _tool_just_used:
                transcript.write("\n", end="")
                _tool_just_used = False
            transcript.write(block.text, end="")

        elif block_type == "ToolUseBlock":
            _tool_just_used = True

            if block.name == "Task":
                subagent_type = block.input.get("subagent_type", "unknown")
                description = block.input.get("description", "no description")
                prompt = block.input.get("prompt", "")

                subagent_id = tracker.register_subagent_spawn(
                    tool_use_id=block.id,
                    subagent_type=subagent_type,
                    description=description,
                    prompt=prompt,
                )

                transcript.write(
                    f"\n\n[🚀 Spawning {subagent_id}: {description}]\n",
                    end="",
                )
