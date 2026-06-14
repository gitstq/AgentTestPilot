# 🧪 AgentTestPilot

<p align="center">
  <b>Lightweight AI Agent Automated Testing & Behavior Validation Engine</b><br>
  <b>轻量级AI Agent自动化测试与行为验证引擎</b>
</p>

<p align="center">
  <a href="https://github.com/gitstq/AgentTestPilot/releases"><img src="https://img.shields.io/github/v/release/gitstq/AgentTestPilot?style=flat-square&color=blue" alt="Version"></a>
  <a href="https://github.com/gitstq/AgentTestPilot/blob/main/LICENSE"><img src="https://img.shields.io/github/license/gitstq/AgentTestPilot?style=flat-square&color=green" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/tests-34%20passing-brightgreen.svg?style=flat-square" alt="Tests">
  <img src="https://img.shields.io/badge/dependencies-zero%20core-orange.svg?style=flat-square" alt="Dependencies">
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.md">English</a>
</p>

---

## 🎉 Project Introduction

**AgentTestPilot** is a lightweight, zero-dependency (core) AI Agent automated testing framework designed for developers building and deploying AI agents. It provides comprehensive behavior validation, response quality scoring, tool call chain tracking, and multi-format report generation capabilities.

Whether you're developing Claude Code plugins, Cursor extensions, MCP servers, or custom AI agents, AgentTestPilot helps you ensure your agent behaves correctly, safely, and efficiently.

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🧪 **Behavior Validation** | Validate AI agent responses for content, format, and quality |
| 🔧 **Tool Call Tracking** | Verify tool invocation patterns, order, and parameters |
| 🛡️ **Safety Detection** | Detect dangerous content, PII leaks, and security risks |
| 📊 **Multi-Format Reports** | Generate HTML, Markdown, and JSON test reports |
| 🖥️ **TUI Dashboard** | Beautiful terminal UI with progress tracking |
| ⚡ **Parallel Execution** | Run tests concurrently for faster feedback |
| 🏷️ **Tag & Priority** | Organize tests with tags and priority levels |
| 🪝 **Hook System** | Customize test lifecycle with before/after hooks |
| 🔌 **Zero Dependencies** | Core functionality requires no external dependencies |
| 🌍 **Cross-Platform** | Works on Linux, macOS, and Windows |

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (when published)
pip install agenttestpilot

# Or install from source
git clone https://github.com/gitstq/AgentTestPilot.git
cd AgentTestPilot
pip install -e .
```

### CLI Usage

```bash
# Initialize a new test project
agenttestpilot init --name my-agent-tests

# Run all tests
agenttestpilot run

# Run with filters
agenttestpilot run --tags api,safety --priority high

# Run demo
agenttestpilot demo

# Generate reports
agenttestpilot report

# Validate test definitions
agenttestpilot validate --file tests.json
```

### Python API Usage

```python
from agenttestpilot import TestEngine, TestSuite, TestCase, TestPriority
from agenttestpilot.core.validator import ResponseValidator, SafetyValidator

# Create engine and suite
engine = TestEngine()
suite = TestSuite("My Agent Tests")

# Create validators
response_validator = ResponseValidator()
safety_validator = SafetyValidator()

# Define a test
def test_response(test, ctx):
    response = "Hello! I am an AI assistant."
    response_validator.assert_contains(test, response, "AI assistant")
    response_validator.assert_length(test, response, min_len=10, max_len=500)
    safety_validator.assert_no_dangerous_content(test, response)

# Create test case
tc = TestCase(
    name="Basic Response Test",
    description="Validate basic agent response",
    priority=TestPriority.HIGH,
    tags=["api", "basic"],
)
tc.set_test_function(test_response)
suite.add_test(tc)

# Run tests
engine.add_suite(suite)
results = engine.run()

print(f"Passed: {results['passed']}/{results['total_tests']}")
```

## 📖 Detailed Usage Guide

### Validators

#### ResponseValidator

```python
from agenttestpilot.core.validator import ResponseValidator

validator = ResponseValidator()

# Content assertions
validator.assert_contains(test, response, "expected text")
validator.assert_not_contains(test, response, "unexpected text")
validator.assert_similarity(test, response, "expected", threshold=0.85)

# JSON assertions
validator.assert_json_valid(test, response)
validator.assert_json_path(test, response, "data.name", "expected_value")

# Format assertions
validator.assert_length(test, response, min_len=10, max_len=500)
validator.assert_regex_match(test, response, r"pattern")

# Performance assertions
validator.assert_response_time(test, duration_ms=1200, max_duration=3000)
```

#### ToolCallValidator

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

#### SafetyValidator

```python
from agenttestpilot.core.validator import SafetyValidator

validator = SafetyValidator()

validator.assert_no_dangerous_content(test, response)
validator.assert_no_pii_leak(test, response)
```

### Configuration

```python
from agenttestpilot.core.config import Config

# Default configuration
config = Config()

# Load from file
config = Config("config.json")

# Environment variables
# ATP_TIMEOUT=30
# ATP_MAX_RETRIES=3
# ATP_CONCURRENCY=4
# ATP_LOG_LEVEL=INFO
```

### Hooks

```python
engine = TestEngine()

# Register hooks
engine.register_hook("before_all", lambda engine: print("Starting..."))
engine.register_hook("after_all", lambda engine: print("Done!"))
engine.register_hook("before_suite", lambda suite: print(f"Suite: {suite.name}"))
engine.register_hook("after_suite", lambda suite, result: print(f"Result: {result['passed']}/{result['total_tests']}"))
```

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Zero Dependencies (Core)**: The core testing engine has no external dependencies, ensuring maximum portability and reliability.
2. **Developer-First**: Designed for developers who need to test AI agents in CI/CD pipelines and local development.
3. **Extensible**: Easy to add custom validators, reporters, and hooks.
4. **Beautiful Reports**: Generate professional HTML/Markdown reports for stakeholders.

### Roadmap

- [ ] **v1.1.0** - LLM API integration for automated response generation
- [ ] **v1.2.0** - Plugin system for custom validators
- [ ] **v1.3.0** - CI/CD integration templates (GitHub Actions, GitLab CI)
- [ ] **v1.4.0** - Web dashboard for test result visualization
- [ ] **v1.5.0** - Distributed testing support

## 📦 Packaging & Deployment

### Build Package

```bash
# Install build dependencies
pip install build twine

# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### Makefile Commands

```bash
make install      # Install package
make install-dev  # Install with dev dependencies
make test         # Run tests
make test-cov     # Run tests with coverage
make lint         # Run linting
make format       # Format code
make clean        # Clean build artifacts
make build        # Build package
make demo         # Run demo
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
