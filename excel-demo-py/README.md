# Excel Demo（Python 版）

这是 `excel-demo` 的 Python 版本，功能与原 Electron 应用对齐：支持聊天、文件上传、工具/思考块展示、Todo 列表、输出文件检测与下载、打开输出目录。

## 安装

1. 安装 Python 依赖：

```bash
pip install -r requirements.txt
```

2. 安装 Claude Code CLI：

```bash
npm install -g @anthropic-ai/claude-code
```

3. 设置环境变量：

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## 可选：安装 Excel Agent 依赖

如果需要让 Agent 运行本地 Python 脚本生成或处理 Excel：

```bash
cd agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 运行

```bash
python excel_demo.py
```

启动后会在本地打开一个 Web 界面（终端会显示访问地址）。

## 使用说明

- 支持上传文件：`.xlsx` / `.xls` / `.pdf` / `.docx` / `.doc`（单个文件最大 10MB）。
- 新生成的 `.xlsx` / `.csv` 会保存在 `agent/` 目录，并在界面中显示下载入口。
- 点击 “Open output folder” 可在系统中打开输出目录。
