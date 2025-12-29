# Claude Agent SDK 演示

> ⚠️ **重要**：这些是 Anthropic 提供的演示应用，仅用于本地开发。请勿部署到生产环境或用于规模化使用。

本仓库包含多个 [Claude Agent SDK](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-overview) 的演示，展示了使用 Claude 构建 AI 应用的不同方式。

## 可用演示

### 📧 [Email Agent](./email-agent)
一个正在开发中的 IMAP 邮件助手，能够：
- 展示你的收件箱
- 进行智能搜索以查找邮件
- 提供 AI 驱动的邮件辅助

### 📊 [Excel Demo](./excel-demo)
演示如何使用 Claude 处理电子表格和 Excel 文件。

### 👋 [Hello World](./hello-world)
一个简单的入门示例，帮助你理解 Claude Agent SDK 的基础。

### 🔬 [Research Agent](./research-agent)
一个多智能体研究系统，协调专门的子智能体进行主题研究并生成综合报告：
- 将研究请求拆分为子主题
- 并行启动研究型智能体进行网页搜索
- 汇总研究结果形成详细报告
- 展示详细的子智能体活动追踪

## 快速开始

每个演示都有自己的目录和专门的设置说明。进入具体演示目录，并参考其 README 获取安装与使用细节。

## 前置条件

- [Bun](https://bun.sh) 运行时（或 Node.js 18+）
- Anthropic API key（[在此获取](https://console.anthropic.com)）

## 开始使用

1. **克隆仓库**
```bash
git clone https://github.com/anthropics/claude-code-sdk-demos.git
cd claude-code-sdk-demos
```

2. **选择一个演示并进入其目录**
```bash
cd email-agent  # 或 excel-demo，或 hello-world
```

3. **按照演示专用 README** 进行配置和使用

## 资源

- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-overview)
- [API Reference](https://docs.anthropic.com/claude)
- [GitHub Issues](https://github.com/anthropics/sdk-demos/issues)

## 支持

这些演示应用按“原样”提供。相关问题可参考：
- **Claude Agent SDK**： [SDK Documentation](https://docs.anthropic.com/claude-code)
- **演示问题**： [GitHub Issues](https://github.com/anthropics/sdk-demos/issues)
- **API 问题**： [Anthropic Support](https://support.anthropic.com)

## 许可

MIT - 这是用于演示目的的示例代码。
