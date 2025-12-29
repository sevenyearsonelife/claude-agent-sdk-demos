import asyncio
import html
import json
import os
import random
import string
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import gradio as gr
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query

MAX_FILE_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".pdf", ".docx", ".doc"}
OUTPUT_EXTENSIONS = {".xlsx", ".csv"}

TOOL_METADATA = {
    "Read": {"icon": "📖", "color": "#3B82F6", "description": "Reading a file"},
    "Glob": {"icon": "🔍", "color": "#3B82F6", "description": "Finding files by pattern"},
    "Grep": {"icon": "🔎", "color": "#3B82F6", "description": "Searching file contents"},
    "Write": {"icon": "✍️", "color": "#F59E0B", "description": "Writing a file"},
    "Edit": {"icon": "✏️", "color": "#F59E0B", "description": "Editing a file"},
    "NotebookEdit": {"icon": "📓", "color": "#F59E0B", "description": "Editing Jupyter notebook"},
    "Bash": {"icon": "⚙️", "color": "#8B5CF6", "description": "Running command"},
    "BashOutput": {"icon": "📊", "color": "#8B5CF6", "description": "Checking command output"},
    "KillShell": {"icon": "🛑", "color": "#EF4444", "description": "Stopping background process"},
    "Task": {"icon": "🤖", "color": "#10B981", "description": "Delegating to subagent"},
    "WebFetch": {"icon": "🌐", "color": "#06B6D4", "description": "Fetching web content"},
    "WebSearch": {"icon": "🔗", "color": "#06B6D4", "description": "Searching the web"},
    "TodoWrite": {"icon": "✅", "color": "#14B8A6", "description": "Updating task list"},
    "ExitPlanMode": {"icon": "📋", "color": "#14B8A6", "description": "Presenting plan"},
    "ListMcpResources": {"icon": "📚", "color": "#6366F1", "description": "Listing MCP resources"},
    "ReadMcpResource": {"icon": "📄", "color": "#6366F1", "description": "Reading MCP resource"},
    "Skill": {"icon": "🎯", "color": "#EC4899", "description": "Using skill"},
    "SlashCommand": {"icon": "⚡", "color": "#EC4899", "description": "Running command"},
    "AskUserQuestion": {"icon": "❓", "color": "#6B7280", "description": "Asking question"},
}

FRIENDLY_PARAM_NAMES = {
    "file_path": "File",
    "pattern": "Pattern",
    "command": "Command",
    "prompt": "Prompt",
    "description": "Description",
    "subagent_type": "Agent Type",
    "old_string": "Find",
    "new_string": "Replace",
    "content": "Content",
    "url": "URL",
    "query": "Query",
    "notebook_path": "Notebook",
    "cell_id": "Cell",
    "new_source": "Source",
    "todos": "Tasks",
    "glob": "File Filter",
    "type": "File Type",
    "path": "Path",
    "output_mode": "Output Mode",
}


def _safe_print_err(message: str) -> None:
    print(message, file=sys.stderr)


def _get_tool_metadata(name: str) -> dict[str, str]:
    return TOOL_METADATA.get(
        name,
        {"icon": "🔧", "color": "#6B7280", "description": f"Using {name}"},
    )


def _get_friendly_param_name(key: str) -> str:
    return FRIENDLY_PARAM_NAMES.get(key, key)


def _format_tool_input(input_data: dict[str, Any]) -> list[dict[str, Any]]:
    formatted: list[dict[str, Any]] = []
    for key, value in input_data.items():
        if value is None:
            continue
        truncated = False
        if isinstance(value, str):
            if len(value) > 100:
                display = value[:100] + "..."
                truncated = True
            else:
                display = value
        elif isinstance(value, (dict, list)):
            json_str = json.dumps(value, ensure_ascii=False, indent=2)
            if len(json_str) > 200:
                compact = json.dumps(value, ensure_ascii=False)
                if len(compact) > 100:
                    display = compact[:100] + "..."
                    truncated = True
                else:
                    display = compact
            else:
                display = json_str
        else:
            display = str(value)
        formatted.append({"key": key, "value": display, "truncated": truncated})
    return formatted


def _render_tool_use(block: Any) -> str:
    metadata = _get_tool_metadata(getattr(block, "name", "Tool"))
    icon = metadata["icon"]
    color = metadata["color"]
    description = metadata["description"]
    input_data = getattr(block, "input", {}) or {}
    formatted = _format_tool_input(input_data)
    has_parameters = len(formatted) > 0

    summary = f"{icon} {html.escape(block.name)} · {html.escape(description)}"
    preview = ""
    if has_parameters:
        first = formatted[0]
        preview = (
            f"<div style='margin-top:4px;font-size:12px;color:#4B5563;'>"
            f"<strong>{html.escape(_get_friendly_param_name(first['key']))}:</strong>"
            f" {html.escape(first['value'])}</div>"
        )

    param_lines: list[str] = []
    if has_parameters:
        for item in formatted:
            name = html.escape(_get_friendly_param_name(item["key"]))
            value = html.escape(item["value"])
            truncated = " (truncated)" if item["truncated"] else ""
            if "\n" in item["value"]:
                value_html = f"<pre style='margin:4px 0;padding:8px;background:#F9FAFB;border-radius:6px;white-space:pre-wrap;'>{value}</pre>"
            else:
                value_html = f"<code style='background:#F9FAFB;padding:2px 6px;border-radius:4px;font-size:12px;'>{value}</code>"
            param_lines.append(
                f"<div style='margin-bottom:8px;'>"
                f"<div style='font-size:12px;color:#6B7280;margin-bottom:2px;'>{name}</div>"
                f"<div style='font-size:13px;color:#111827;'>{value_html}<span style='font-size:11px;color:#6B7280;'>{truncated}</span></div>"
                f"</div>"
            )
    params_html = "".join(param_lines)

    details_body = ""
    if has_parameters:
        details_body = (
            "<div style='background:#FFFFFF;border-top:1px solid #E5E7EB;padding:8px;'>"
            f"{params_html}"
            "</div>"
        )

    details = (
        f"<details style='margin:8px 0;border-left:4px solid {color};border-radius:6px;overflow:hidden;'>"
        f"<summary style='list-style:none;cursor:pointer;background:#F9FAFB;padding:8px 12px;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
        f"<div style='font-size:14px;color:#374151;'>{summary}</div>"
        f"</div>"
        f"{preview}"
        "</summary>"
        f"{details_body}"
        "</details>"
    )
    return details


def _render_thinking(block: Any) -> str:
    thinking_text = getattr(block, "thinking", "") or ""
    preview = thinking_text[:100]
    more = "..." if len(thinking_text) > 100 else ""
    preview_html = html.escape(preview + more)
    full_html = html.escape(thinking_text)
    return (
        "<details style='margin:8px 0;border-left:4px solid #A855F7;border-radius:6px;overflow:hidden;'>"
        "<summary style='list-style:none;cursor:pointer;background:#F3E8FF;padding:8px 12px;'>"
        "<div style='display:flex;justify-content:space-between;align-items:center;'>"
        "<div style='font-size:14px;color:#6B21A8;'>💭 Thinking · Extended reasoning process</div>"
        "</div>"
        f"<div style='margin-top:4px;font-size:13px;color:#7C3AED;font-style:italic;'>{preview_html}</div>"
        "</summary>"
        "<div style='background:#FFFFFF;border-top:1px solid #E9D5FF;padding:8px;'>"
        f"<div style='font-size:13px;color:#374151;font-style:italic;white-space:pre-wrap;'>{full_html}</div>"
        "</div>"
        "</details>"
    )


def _validate_todos(todos: Any) -> list[dict[str, Any]] | None:
    if not isinstance(todos, list):
        return None
    valid: list[dict[str, Any]] = []
    for item in todos:
        if not isinstance(item, dict):
            return None
        if not all(k in item for k in ("id", "content", "status", "priority")):
            return None
        if item["status"] not in {"pending", "in_progress", "completed"}:
            return None
        if item["priority"] not in {"high", "medium", "low"}:
            return None
        valid.append(item)
    return valid


def _render_todos(todos: list[dict[str, Any]]) -> str:
    if not todos:
        return ""
    total = len(todos)
    completed = sum(1 for t in todos if t["status"] == "completed")
    in_progress = sum(1 for t in todos if t["status"] == "in_progress")
    pending = sum(1 for t in todos if t["status"] == "pending")

    lines = [f"### 📝 Todo List ({total} items)", ""]
    for todo in todos:
        status_icon = {"completed": "✅", "in_progress": "🔄", "pending": "⏳"}.get(todo["status"], "○")
        lines.append(f"- {status_icon} **{todo['priority']}** · {todo['content']}")
    lines.append("")
    lines.append(f"Completed: {completed} · In Progress: {in_progress} · Pending: {pending}")
    return "\n".join(lines)


def _list_output_files(output_dir: Path) -> dict[str, Path]:
    if not output_dir.exists():
        return {}
    files: dict[str, Path] = {}
    for path in output_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() in OUTPUT_EXTENSIONS:
            files[path.name] = path
    return files


def _file_to_path(file_obj: Any) -> Path:
    if isinstance(file_obj, str):
        return Path(file_obj)
    if isinstance(file_obj, dict):
        if "path" in file_obj:
            return Path(file_obj["path"])
        if "name" in file_obj:
            return Path(file_obj["name"])
    if hasattr(file_obj, "path"):
        return Path(file_obj.path)
    if hasattr(file_obj, "name"):
        return Path(file_obj.name)
    return Path(str(file_obj))


def _file_display_name(file_obj: Any, fallback: Path) -> str:
    if isinstance(file_obj, dict):
        for key in ("orig_name", "name"):
            if key in file_obj and file_obj[key]:
                return Path(file_obj[key]).name
    if hasattr(file_obj, "orig_name"):
        return Path(file_obj.orig_name).name
    if hasattr(file_obj, "name"):
        return Path(file_obj.name).name
    return fallback.name


def _save_uploaded_files(file_objs: list[Any], problems_dir: Path) -> tuple[list[tuple[str, Path]], list[str]]:
    saved: list[tuple[str, Path]] = []
    warnings: list[str] = []
    if not file_objs:
        return saved, warnings

    problems_dir.mkdir(parents=True, exist_ok=True)

    for file_obj in file_objs:
        path = _file_to_path(file_obj)
        display_name = _file_display_name(file_obj, path)
        ext = Path(display_name).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            warnings.append(f"不支持的文件格式: {display_name}")
            continue
        if not path.exists() or not path.is_file():
            warnings.append(f"文件不存在或不可用: {display_name}")
            continue
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            mb_size = round(size / 1024 / 1024)
            warnings.append(f"文件过大，已跳过: {display_name} ({mb_size}MB, 限制 10MB)")
            continue

        timestamp = int(time.time() * 1000)
        rand_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        unique_name = f"{Path(display_name).stem}_{timestamp}_{rand_suffix}{ext}"
        dest_path = problems_dir / unique_name
        dest_path.write_bytes(path.read_bytes())
        saved.append((unique_name, dest_path))

    return saved, warnings


def _build_prompt(base_prompt: str, saved_files: list[tuple[str, Path]]) -> str:
    if not saved_files:
        return base_prompt
    prompt = base_prompt
    for filename, filepath in saved_files:
        prompt += f"\n\nUploaded file: {filename} (saved to {filepath})"
    return prompt


def _build_options(agent_dir: Path) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        cwd=str(agent_dir),
        max_turns=100,
        setting_sources=["local", "project"],
        allowed_tools=[
            "Bash",
            "Create",
            "Edit",
            "Read",
            "Write",
            "MultiEdit",
            "WebSearch",
            "GrepTool",
            "Skill",
            "TodoWrite",
            "TodoEdit",
        ],
    )


def _render_assistant_message(message: AssistantMessage, current_todos: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    parts: list[str] = []
    todos = current_todos
    for block in message.content:
        block_type = type(block).__name__
        if block_type == "TextBlock":
            parts.append(getattr(block, "text", ""))
        elif block_type == "ToolUseBlock":
            if getattr(block, "name", "") == "TodoWrite":
                candidate = _validate_todos(getattr(block, "input", {}).get("todos"))
                if candidate is not None:
                    todos = candidate
            parts.append(_render_tool_use(block))
        elif block_type == "ThinkingBlock":
            parts.append(_render_thinking(block))
    return "\n\n".join([p for p in parts if p]), todos


def _format_warning_text(warnings: list[str]) -> str:
    if not warnings:
        return ""
    lines = ["**文件处理提示**", ""]
    for item in warnings:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _format_output_files(output_files: list[Path]) -> list[str]:
    return [str(path) for path in output_files]


def _open_output_folder(agent_dir: Path) -> str:
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(agent_dir)], check=False)
        elif sys.platform.startswith("win"):
            os.startfile(str(agent_dir))
        else:
            subprocess.run(["xdg-open", str(agent_dir)], check=False)
        return "已尝试打开输出目录。"
    except Exception as exc:
        return f"打开输出目录失败: {exc}"


async def _run_query(prompt: str, file_objs: list[Any], agent_dir: Path, todos: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]], list[Path], list[str]]:
    problems_dir = agent_dir / "problems"
    initial_outputs = _list_output_files(agent_dir)

    saved_files, warnings = _save_uploaded_files(file_objs, problems_dir)
    final_prompt = _build_prompt(prompt, saved_files)

    options = _build_options(agent_dir)
    assistant_chunks: list[str] = []
    current_todos = todos

    try:
        async for message in query(prompt=final_prompt, options=options):
            if isinstance(message, AssistantMessage):
                rendered, current_todos = _render_assistant_message(message, current_todos)
                if rendered:
                    assistant_chunks.append(rendered)
    except Exception as exc:
        return f"Error: {exc}", current_todos, [], warnings

    final_outputs = _list_output_files(agent_dir)
    new_outputs = [path for name, path in final_outputs.items() if name not in initial_outputs]

    return "\n\n".join(assistant_chunks).strip() or "...", current_todos, new_outputs, warnings


def _build_user_display(content: str, files: list[Any]) -> str:
    display_content = content or ""
    if files:
        names = ", ".join(_file_display_name(f, _file_to_path(f)) for f in files)
        if display_content:
            display_content = f"{display_content}\n\nFiles: {names}"
        else:
            display_content = f"Files: {names}"
    return display_content


def _ensure_api_key() -> str | None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return "未检测到 ANTHROPIC_API_KEY，请先设置环境变量。"
    return None


def handle_submit(user_input: str, files: list[Any], history: list[dict[str, str]], todos: list[dict[str, Any]]):
    if not user_input and not files:
        return history, _render_todos(todos), [], "", history, todos

    api_error = _ensure_api_key()
    if api_error:
        return history, _render_todos(todos), [], api_error, history, todos

    history = history or []
    user_display = _build_user_display(user_input.strip(), files or [])
    history.append({"role": "user", "content": user_display})
    history.append({"role": "assistant", "content": "Claude is thinking..."})

    yield history, _render_todos(todos), [], "", history, todos

    agent_dir = Path(__file__).resolve().parent / "agent"
    assistant_content, new_todos, output_files, warnings = asyncio.run(
        _run_query(user_input.strip(), files or [], agent_dir, todos),
    )
    history[-1] = {"role": "assistant", "content": assistant_content}

    warning_text = _format_warning_text(warnings)
    yield history, _render_todos(new_todos), _format_output_files(output_files), warning_text, history, new_todos


def handle_open_folder() -> str:
    agent_dir = Path(__file__).resolve().parent / "agent"
    return _open_output_folder(agent_dir)


CUSTOM_CSS = """
#app-root {
  font-family: "IBM Plex Sans", "Source Sans 3", "Helvetica Neue", sans-serif;
}
.gr-chatbot .message.user {
  background: #217346 !important;
  color: #FFFFFF !important;
}
"""


def build_app() -> gr.Blocks:
    with gr.Blocks(css=CUSTOM_CSS) as demo:
        gr.Markdown("# CLAUDE EXCEL AGENT")
        chatbot = gr.Chatbot(
            label="",
            height=520,
            show_copy_button=True,
            type="messages",
            sanitize_html=False,
        )
        todo_view = gr.Markdown()
        output_files = gr.File(label="Output Files", file_count="multiple")
        with gr.Row():
            open_folder_btn = gr.Button("📂 Open output folder")
            status = gr.Markdown()

        with gr.Row():
            user_input = gr.Textbox(
                placeholder="Type a message... (Shift+Enter for new line)",
                lines=2,
                max_lines=6,
                scale=3,
            )
            file_upload = gr.File(
                file_count="multiple",
                file_types=[".xlsx", ".xls", ".pdf", ".docx", ".doc"],
                label="Attach Files",
                scale=1,
            )
        send_btn = gr.Button("Send", variant="primary")

        history_state = gr.State([])
        todos_state = gr.State([])

        send_btn.click(
            handle_submit,
            inputs=[user_input, file_upload, history_state, todos_state],
            outputs=[chatbot, todo_view, output_files, status, history_state, todos_state],
        )
        user_input.submit(
            handle_submit,
            inputs=[user_input, file_upload, history_state, todos_state],
            outputs=[chatbot, todo_view, output_files, status, history_state, todos_state],
        )
        open_folder_btn.click(
            handle_open_folder,
            inputs=[],
            outputs=[status],
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch()
