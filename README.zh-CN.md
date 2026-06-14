# 🧪 AgentTestPilot

<p align="center">
  <b>轻量级AI Agent自动化测试与行为验证引擎</b><br>
  <b>Lightweight AI Agent Automated Testing & Behavior Validation Engine</b>
</p>

<p align="center">
  <a href="https://github.com/gitstq/AgentTestPilot/releases"><img src="https://img.shields.io/github/v/release/gitstq/AgentTestPilot?style=flat-square&color=blue" alt="版本"></a>
  <a href="https://github.com/gitstq/AgentTestPilot/blob/main/LICENSE"><img src="https://img.shields.io/github/license/gitstq/AgentTestPilot?style=flat-square&color=green" alt="许可证"></a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/tests-34%20passing-brightgreen.svg?style=flat-square" alt="测试">
  <img src="https://img.shields.io/badge/dependencies-zero%20core-orange.svg?style=flat-square" alt="依赖">
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.md">English</a>
</p>

---

## 🎉 项目介绍

**AgentTestPilot** 是一个轻量级、零依赖（核心）的 AI Agent 自动化测试框架，专为构建和部署 AI Agent 的开发者设计。它提供全面的行为验证、响应质量评分、工具调用链追踪和多格式报告生成能力。

无论您正在开发 Claude Code 插件、Cursor 扩展、MCP 服务器还是自定义 AI Agent，AgentTestPilot 都能帮助您确保 Agent 行为正确、安全且高效。

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🧪 **行为验证** | 验证 AI Agent 响应的内容、格式和质量 |
| 🔧 **工具调用追踪** | 验证工具调用模式、顺序和参数 |
| 🛡️ **安全检测** | 检测危险内容、PII 泄露和安全风险 |
| 📊 **多格式报告** | 生成 HTML、Markdown 和 JSON 测试报告 |
| 🖥️ **TUI 仪表盘** | 美观的终端 UI，带进度追踪 |
| ⚡ **并行执行** | 并发运行测试，获得更快反馈 |
| 🏷️ **标签与优先级** | 使用标签和优先级组织测试 |
| 🪝 **钩子系统** | 使用 before/after 钩子自定义测试生命周期 |
| 🔌 **零依赖** | 核心功能无需外部依赖 |
| 🌍 **跨平台** | 支持 Linux、macOS 和 Windows |

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装（发布后）
pip install agenttestpilot

# 或从源码安装
git clone https://github.com/gitstq/AgentTestPilot.git
cd AgentTestPilot
pip install -e .
```

### CLI 使用

```bash
# 初始化新测试项目
agenttestpilot init --name my-agent-tests

# 运行所有测试
agenttestpilot run

# 带过滤条件运行
agenttestpilot run --tags api,safety --priority high

# 运行演示
agenttestpilot demo

# 生成报告
agenttestpilot report

# 验证测试定义
agenttestpilot validate --file tests.json
```

### Python API 使用

```python
from agenttestpilot import TestEngine, TestSuite, TestCase, TestPriority
from agenttestpilot.core.validator import ResponseValidator, SafetyValidator

# 创建引擎和套件
engine = TestEngine()
suite = TestSuite("My Agent Tests")

# 创建验证器
response_validator = ResponseValidator()
safety_validator = SafetyValidator()

# 定义测试
def test_response(test, ctx):
    response = "Hello! I am an AI assistant."
    response_validator.assert_contains(test, response, "AI assistant")
    response_validator.assert_length(test, response, min_len=10, max_len=500)
    safety_validator.assert_no_dangerous_content(test, response)

# 创建测试用例
tc = TestCase(
    name="Basic Response Test",
    description="Validate basic agent response",
    priority=TestPriority.HIGH,
    tags=["api", "basic"],
)
tc.set_test_function(test_response)
suite.add_test(tc)

# 运行测试
engine.add_suite(suite)
results = engine.run()

print(f"通过: {results['passed']}/{results['total_tests']}")
```

## 📖 详细使用指南

### 验证器

#### ResponseValidator（响应验证器）

```python
from agenttestpilot.core.validator import ResponseValidator

validator = ResponseValidator()

# 内容断言
validator.assert_contains(test, response, "expected text")
validator.assert_not_contains(test, response, "unexpected text")
validator.assert_similarity(test, response, "expected", threshold=0.85)

# JSON 断言
validator.assert_json_valid(test, response)
validator.assert_json_path(test, response, "data.name", "expected_value")

# 格式断言
validator.assert_length(test, response, min_len=10, max_len=500)
validator.assert_regex_match(test, response, r"pattern")

# 性能断言
validator.assert_response_time(test, duration_ms=1200, max_duration=3000)
```

#### ToolCallValidator（工具调用验证器）

```python
from agenttestpilot.core.validator import ToolCallValidator

validator = ToolCallValidator()

tool_calls = [
    {"name": "search", "parameters": {"query": "python"}},
    {"name": "calculate", "parameters": {"expr": "1+1"}},
]

validator.assert_tool_called(test, tool_calls, "search")
validator.assert_tool_order(test, tool_calls, ["search", "calculate"])
validator.assert_max_tool_calls(test, tool_calls, 5)
validator.assert_no_duplicate_calls(test, tool_calls)
```

#### SafetyValidator（安全验证器）

```python
from agenttestpilot.core.validator import SafetyValidator

validator = SafetyValidator()

validator.assert_no_dangerous_content(test, response)
validator.assert_no_pii_leak(test, response)
```

### 配置

```python
from agenttestpilot.core.config import Config

# 默认配置
config = Config()

# 从文件加载
config = Config("config.json")

# 环境变量
# ATP_TIMEOUT=30
# ATP_MAX_RETRIES=3
# ATP_CONCURRENCY=4
# ATP_LOG_LEVEL=INFO
```

### 钩子

```python
engine = TestEngine()

# 注册钩子
engine.register_hook("before_all", lambda engine: print("开始..."))
engine.register_hook("after_all", lambda engine: print("完成!"))
engine.register_hook("before_suite", lambda suite: print(f"套件: {suite.name}"))
engine.register_hook("after_suite", lambda suite, result: print(f"结果: {result['passed']}/{result['total_tests']}"))
```

## 💡 设计思路与迭代规划

### 设计原则

1. **零依赖（核心）**：核心测试引擎无外部依赖，确保最大的可移植性和可靠性。
2. **开发者优先**：专为需要在 CI/CD 流水线和本地开发中测试 AI Agent 的开发者设计。
3. **可扩展**：轻松添加自定义验证器、报告生成器和钩子。
4. **美观报告**：为利益相关者生成专业的 HTML/Markdown 报告。

### 路线图

- [ ] **v1.1.0** - LLM API 集成，支持自动响应生成
- [ ] **v1.2.0** - 自定义验证器插件系统
- [ ] **v1.3.0** - CI/CD 集成模板（GitHub Actions、GitLab CI）
- [ ] **v1.4.0** - Web 仪表盘，可视化测试结果
- [ ] **v1.5.0** - 分布式测试支持

## 📦 打包与部署

### 构建包

```bash
# 安装构建依赖
pip install build twine

# 构建
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

### Makefile 命令

```bash
make install      # 安装包
make install-dev  # 安装开发依赖
make test         # 运行测试
make test-cov     # 运行测试（带覆盖率）
make lint         # 运行代码检查
make format       # 格式化代码
make clean        # 清理构建产物
make build        # 构建包
make demo         # 运行演示
```

## 🤝 贡献指南

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

## 📄 开源协议

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  用 ❤️ 制作 by <a href="https://github.com/gitstq">gitstq</a>
</p>
