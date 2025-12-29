# Claude Agent SDK Hello World（Python）

该示例与 `hello-world` 的 TypeScript 版本保持功能一致：使用 ClaudeSDKClient 搭配 ClaudeAgentOptions 配置工具白名单、工作目录、模型与 PreToolUse hooks，并输出 Claude 的文本回复。

## 安装

1. 安装 Python 依赖：

```bash
pip install -r requirements.txt
```

2. 安装 Claude Code CLI：

```bash
npm install -g @anthropic-ai/claude-code
```

## 配置

设置环境变量：

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## 目录准备

```bash
mkdir -p agent/custom_scripts
```

## 运行

```bash
python hello_world.py
```

## 说明

- 使用 `ClaudeAgentOptions` 配置 `max_turns`、`cwd`、`model` 与 `allowed_tools`，并通过 `hooks` 注入 PreToolUse 校验。
- PreToolUse hook 会拦截 `.js`/`.ts` 写入，要求只能写到 `agent/custom_scripts` 目录。
- 通过 ClaudeSDKClient 调用 `query()` 并使用 `receive_response()` 读取 `AssistantMessage`，取首个 `TextBlock` 输出。
- Python SDK 的 `query()` 不支持 hooks，因此使用 ClaudeSDKClient 来保证与 TS 版本的 hooks 行为一致。

## 常见问题

### 找不到 Claude Code CLI

如果提示 Claude Code CLI 未找到，请先确认已全局安装：

```bash
npm install -g @anthropic-ai/claude-code
```

如果 CLI 不在 PATH，可在代码中显式指定：

```python
options = ClaudeAgentOptions(cli_path="/path/to/claude", ...)
```
