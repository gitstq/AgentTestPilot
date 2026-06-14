# 🧪 AgentTestPilot

<p align="center">
  <b>輕量級AI Agent自動化測試與行為驗證引擎</b><br>
  <b>Lightweight AI Agent Automated Testing & Behavior Validation Engine</b>
</p>

<p align="center">
  <a href="https://github.com/gitstq/AgentTestPilot/releases"><img src="https://img.shields.io/github/v/release/gitstq/AgentTestPilot?style=flat-square&color=blue" alt="版本"></a>
  <a href="https://github.com/gitstq/AgentTestPilot/blob/main/LICENSE"><img src="https://img.shields.io/github/license/gitstq/AgentTestPilot?style=flat-square&color=green" alt="授權"></a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/tests-34%20passing-brightgreen.svg?style=flat-square" alt="測試">
  <img src="https://img.shields.io/badge/dependencies-zero%20core-orange.svg?style=flat-square" alt="相依">
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.md">English</a>
</p>

---

## 🎉 專案介紹

**AgentTestPilot** 是一個輕量級、零相依（核心）的 AI Agent 自動化測試框架，專為建置和部署 AI Agent 的開發者設計。它提供全面的行為驗證、回應品質評分、工具呼叫鏈追蹤和多格式報告產生能力。

無論您正在開發 Claude Code 外掛、Cursor 擴充功能、MCP 伺服器還是自訂 AI Agent，AgentTestPilot 都能協助您確保 Agent 行為正確、安全且高效。

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🧪 **行為驗證** | 驗證 AI Agent 回應的內容、格式和品質 |
| 🔧 **工具呼叫追蹤** | 驗證工具呼叫模式、順序和參數 |
| 🛡️ **安全檢測** | 偵測危險內容、PII 洩露和安全風險 |
| 📊 **多格式報告** | 產生 HTML、Markdown 和 JSON 測試報告 |
| 🖥️ **TUI 儀表板** | 美觀的終端 UI，含進度追蹤 |
| ⚡ **平行執行** | 並行執行測試，獲得更快的回饋 |
| 🏷️ **標籤與優先級** | 使用標籤和優先級組織測試 |
| 🪝 **鉤子系統** | 使用 before/after 鉤子自訂測試生命週期 |
| 🔌 **零相依** | 核心功能無需外部相依 |
| 🌍 **跨平台** | 支援 Linux、macOS 和 Windows |

## 🚀 快速開始

### 安裝

```bash
# 從 PyPI 安裝（發布後）
pip install agenttestpilot

# 或從原始碼安裝
git clone https://github.com/gitstq/AgentTestPilot.git
cd AgentTestPilot
pip install -e .
```

### CLI 使用

```bash
# 初始化新測試專案
agenttestpilot init --name my-agent-tests

# 執行所有測試
agenttestpilot run

# 帶過濾條件執行
agenttestpilot run --tags api,safety --priority high

# 執行示範
agenttestpilot demo

# 產生報告
agenttestpilot report

# 驗證測試定義
agenttestpilot validate --file tests.json
```

### Python API 使用

```python
from agenttestpilot import TestEngine, TestSuite, TestCase, TestPriority
from agenttestpilot.core.validator import ResponseValidator, SafetyValidator

# 建立引擎和套件
engine = TestEngine()
suite = TestSuite("My Agent Tests")

# 建立驗證器
response_validator = ResponseValidator()
safety_validator = SafetyValidator()

# 定義測試
def test_response(test, ctx):
    response = "Hello! I am an AI assistant."
    response_validator.assert_contains(test, response, "AI assistant")
    response_validator.assert_length(test, response, min_len=10, max_len=500)
    safety_validator.assert_no_dangerous_content(test, response)

# 建立測試案例
tc = TestCase(
    name="Basic Response Test",
    description="Validate basic agent response",
    priority=TestPriority.HIGH,
    tags=["api", "basic"],
)
tc.set_test_function(test_response)
suite.add_test(tc)

# 執行測試
engine.add_suite(suite)
results = engine.run()

print(f"通過: {results['passed']}/{results['total_tests']}")
```

## 📖 詳細使用指南

### 驗證器

#### ResponseValidator（回應驗證器）

```python
from agenttestpilot.core.validator import ResponseValidator

validator = ResponseValidator()

# 內容斷言
validator.assert_contains(test, response, "expected text")
validator.assert_not_contains(test, response, "unexpected text")
validator.assert_similarity(test, response, "expected", threshold=0.85)

# JSON 斷言
validator.assert_json_valid(test, response)
validator.assert_json_path(test, response, "data.name", "expected_value")

# 格式斷言
validator.assert_length(test, response, min_len=10, max_len=500)
validator.assert_regex_match(test, response, r"pattern")

# 效能斷言
validator.assert_response_time(test, duration_ms=1200, max_duration=3000)
```

#### ToolCallValidator（工具呼叫驗證器）

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

#### SafetyValidator（安全驗證器）

```python
from agenttestpilot.core.validator import SafetyValidator

validator = SafetyValidator()

validator.assert_no_dangerous_content(test, response)
validator.assert_no_pii_leak(test, response)
```

### 配置

```python
from agenttestpilot.core.config import Config

# 預設配置
config = Config()

# 從檔案載入
config = Config("config.json")

# 環境變數
# ATP_TIMEOUT=30
# ATP_MAX_RETRIES=3
# ATP_CONCURRENCY=4
# ATP_LOG_LEVEL=INFO
```

### 鉤子

```python
engine = TestEngine()

# 註冊鉤子
engine.register_hook("before_all", lambda engine: print("開始..."))
engine.register_hook("after_all", lambda engine: print("完成!"))
engine.register_hook("before_suite", lambda suite: print(f"套件: {suite.name}"))
engine.register_hook("after_suite", lambda suite, result: print(f"結果: {result['passed']}/{result['total_tests']}"))
```

## 💡 設計思路與迭代規劃

### 設計原則

1. **零相依（核心）**：核心測試引擎無外部相依，確保最大的可攜性和可靠性。
2. **開發者優先**：專為需要在 CI/CD 流水線和本機開發中測試 AI Agent 的開發者設計。
3. **可擴展**：輕鬆新增自訂驗證器、報告產生器和鉤子。
4. **美觀報告**：為利益相關者產生專業的 HTML/Markdown 報告。

### 路線圖

- [ ] **v1.1.0** - LLM API 整合，支援自動回應產生
- [ ] **v1.2.0** - 自訂驗證器外掛系統
- [ ] **v1.3.0** - CI/CD 整合範本（GitHub Actions、GitLab CI）
- [ ] **v1.4.0** - Web 儀表板，視覺化測試結果
- [ ] **v1.5.0** - 分散式測試支援

## 📦 打包與部署

### 建置套件

```bash
# 安裝建置相依
pip install build twine

# 建置
python -m build

# 上傳到 PyPI
python -m twine upload dist/*
```

### Makefile 命令

```bash
make install      # 安裝套件
make install-dev  # 安裝開發相依
make test         # 執行測試
make test-cov     # 執行測試（含覆蓋率）
make lint         # 執行程式碼檢查
make format       # 格式化程式碼
make clean        # 清理建置產物
make build        # 建置套件
make demo         # 執行示範
```

## 🤝 貢獻指南

歡迎貢獻！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

## 📄 開源協議

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  用 ❤️ 製作 by <a href="https://github.com/gitstq">gitstq</a>
</p>
