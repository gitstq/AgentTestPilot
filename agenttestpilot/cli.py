#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - CLI Module
命令行接口模块
"""

import sys
import os
import json
import argparse
from typing import Optional

from .core.engine import TestEngine
from .core.config import Config
from .core.test_case import TestSuite, TestCase, TestPriority
from .core.validator import ResponseValidator, ToolCallValidator, SafetyValidator
from .tui.dashboard import TUIDashboard


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="agenttestpilot",
        description="🧪 AgentTestPilot - Lightweight AI Agent Automated Testing & Behavior Validation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s init                          Initialize a new test project
  %(prog)s run                           Run all tests
  %(prog)s run --suite my_suite          Run specific suite
  %(prog)s run --tags api,safety         Run tests with specific tags
  %(prog)s run --priority high           Run tests with priority >= high
  %(prog)s run --config config.json      Use custom config file
  %(prog)s report                        Generate reports from last run
  %(prog)s validate --file test.json     Validate a test definition file
  %(prog)s --version                     Show version
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="Path to configuration file (JSON)",
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./reports",
        help="Output directory for reports",
    )

    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["json", "html", "markdown", "all"],
        default="all",
        help="Report format",
    )

    parser.add_argument(
        "--no-tui",
        action="store_true",
        help="Disable TUI dashboard",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new test project")
    init_parser.add_argument("--name", type=str, default="my-agent-tests", help="Project name")

    # run command
    run_parser = subparsers.add_parser("run", help="Run tests")
    run_parser.add_argument("--suite", "-s", type=str, help="Run specific suite")
    run_parser.add_argument("--tags", "-t", type=str, help="Filter by tags (comma-separated)")
    run_parser.add_argument("--priority", "-p", type=str,
                            choices=["critical", "high", "medium", "low"],
                            help="Minimum priority level")
    run_parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    run_parser.add_argument("--file", type=str, help="Run tests from JSON file")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_parser.add_argument("--input", "-i", type=str, help="Input results file")

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate test definitions")
    validate_parser.add_argument("--file", type=str, required=True, help="Test definition file")

    # demo command
    subparsers.add_parser("demo", help="Run demo tests")

    return parser


def cmd_init(args):
    """初始化项目命令"""
    project_name = args.name
    if os.path.exists(project_name):
        print(f"❌ Directory '{project_name}' already exists")
        return 1

    os.makedirs(project_name)
    os.makedirs(os.path.join(project_name, "tests"))
    os.makedirs(os.path.join(project_name, "reports"))

    # 创建示例测试文件
    example_test = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example AgentTestPilot Test Suite
"""

from agenttestpilot import TestSuite, TestCase, TestPriority
from agenttestpilot.core.validator import ResponseValidator, SafetyValidator

# 创建测试套件
suite = TestSuite("My Agent Tests", "Example test suite for my AI agent")

# 创建响应验证器
response_validator = ResponseValidator()
safety_validator = SafetyValidator()

# 定义测试用例 1: 基本响应测试
def test_basic_response(test: TestCase, ctx):
    response = ctx.get("agent_response", "Hello, I am an AI assistant.")
    response_validator.assert_contains(test, response, "AI")
    response_validator.assert_length(test, response, min_len=5, max_len=500)

# 定义测试用例 2: 安全测试
def test_safety(test: TestCase, ctx):
    response = ctx.get("agent_response", "")
    safety_validator.assert_no_dangerous_content(test, response)
    safety_validator.assert_no_pii_leak(test, response)

# 定义测试用例 3: JSON响应测试
def test_json_response(test: TestCase, ctx):
    response = ctx.get("json_response", '{"status": "ok", "data": []}')
    response_validator.assert_json_valid(test, response)
    response_validator.assert_json_path(test, response, "status", "ok")

# 创建并添加测试用例
test1 = TestCase(
    name="Basic Response Validation",
    description="Validate basic agent response",
    priority=TestPriority.HIGH,
    tags=["api", "basic"],
)
test1.set_test_function(test_basic_response)
suite.add_test(test1)

test2 = TestCase(
    name="Safety Check",
    description="Check for dangerous content",
    priority=TestPriority.CRITICAL,
    tags=["safety", "security"],
)
test2.set_test_function(test_safety)
suite.add_test(test2)

test3 = TestCase(
    name="JSON Response Validation",
    description="Validate JSON response format",
    priority=TestPriority.MEDIUM,
    tags=["api", "json"],
)
test3.set_test_function(test_json_response)
suite.add_test(test3)

if __name__ == "__main__":
    from agenttestpilot import TestEngine
    engine = TestEngine()
    engine.add_suite(suite)
    results = engine.run()
    print(f"\\n✅ Tests completed: {results['passed']}/{results['total_tests']} passed")
'''

    with open(os.path.join(project_name, "tests", "test_example.py"), "w", encoding="utf-8") as f:
        f.write(example_test)

    # 创建配置文件
    config = {
        "timeout": 30,
        "max_retries": 3,
        "concurrency": 4,
        "output_dir": "./reports",
        "output_formats": ["json", "html", "markdown"],
        "strict_mode": False,
        "capture_traces": True,
        "log_level": "INFO",
        "tui_enabled": True,
    }

    with open(os.path.join(project_name, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # 创建README
    readme = f"""# {project_name}

AgentTestPilot Test Project

## Quick Start

```bash
# Install AgentTestPilot
pip install agenttestpilot

# Run tests
agenttestpilot run

# Or with Python
python tests/test_example.py
```

## Project Structure

```
{project_name}/
├── tests/           # Test files
├── reports/         # Generated reports
├── config.json      # Configuration
└── README.md        # This file
```
"""

    with open(os.path.join(project_name, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"✅ Project '{project_name}' initialized successfully!")
    print(f"   cd {project_name}")
    print(f"   agenttestpilot run")
    return 0


def cmd_run(args):
    """运行测试命令"""
    config = Config(args.config) if args.config else Config.default()
    config.set("output_dir", args.output)

    if args.no_tui:
        config.set("tui_enabled", False)

    # 设置输出格式
    formats = []
    if args.format == "all":
        formats = ["json", "html", "markdown"]
    else:
        formats = [args.format]
    config.set("output_formats", formats)

    engine = TestEngine(config)

    # 从文件加载测试
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ Test file not found: {args.file}")
            return 1
        # 这里可以实现从JSON加载测试套件的逻辑
        print(f"📄 Loading tests from: {args.file}")

    # 如果没有指定文件，运行演示测试
    if not args.file:
        demo_suite = create_demo_suite()
        engine.add_suite(demo_suite)

    # 解析标签过滤
    tags = None
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",")]

    # 显示TUI
    if config.get("tui_enabled") and not args.no_tui:
        dashboard = TUIDashboard()
        dashboard.show_header()

    # 执行测试
    if args.parallel:
        results = engine.run_parallel()
    else:
        results = engine.run(
            suite_filter=args.suite,
            tag_filter=tags,
            priority_filter=args.priority,
        )

    # 显示结果
    if config.get("tui_enabled") and not args.no_tui:
        dashboard = TUIDashboard()
        dashboard.show_summary(results)
    else:
        print_summary(results)

    # 返回码
    if results.get("failed", 0) > 0 or results.get("errors", 0) > 0:
        return 1
    return 0


def cmd_report(args):
    """生成报告命令"""
    input_file = args.input or "./reports/report.json"
    if not os.path.exists(input_file):
        print(f"❌ Results file not found: {input_file}")
        return 1

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 生成报告
    from .core.reporter import HTMLReporter, MarkdownReporter

    output_dir = args.output or "./reports"
    os.makedirs(output_dir, exist_ok=True)

    html_reporter = HTMLReporter()
    html_reporter.generate(data, os.path.join(output_dir, "report.html"))
    print(f"✅ HTML report generated: {os.path.join(output_dir, 'report.html')}")

    md_reporter = MarkdownReporter()
    md_reporter.generate(data, os.path.join(output_dir, "report.md"))
    print(f"✅ Markdown report generated: {os.path.join(output_dir, 'report.md')}")

    return 0


def cmd_validate(args):
    """验证测试定义命令"""
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return 1

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 基本结构验证
        required_fields = ["name", "test_cases"]
        for field in required_fields:
            if field not in data:
                print(f"❌ Missing required field: '{field}'")
                return 1

        # 验证测试用例
        for i, tc in enumerate(data.get("test_cases", [])):
            if "name" not in tc:
                print(f"❌ Test case #{i} missing 'name' field")
                return 1

        print(f"✅ Test definition file is valid: {filepath}")
        print(f"   Suite: {data['name']}")
        print(f"   Test cases: {len(data.get('test_cases', []))}")
        return 0

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return 1


def cmd_demo(args):
    """运行演示测试"""
    print("🧪 AgentTestPilot Demo")
    print("=" * 50)

    engine = TestEngine()
    demo_suite = create_demo_suite()
    engine.add_suite(demo_suite)

    dashboard = TUIDashboard()
    dashboard.show_header()

    results = engine.run()
    dashboard.show_summary(results)

    return 0


def create_demo_suite() -> TestSuite:
    """创建演示测试套件"""
    suite = TestSuite("Demo Suite", "AgentTestPilot demonstration tests")

    response_validator = ResponseValidator()
    tool_validator = ToolCallValidator()
    safety_validator = SafetyValidator()

    # 测试1: 基本响应验证
    def test1(test: TestCase, ctx):
        response = "Hello! I am an AI assistant ready to help you with your questions."
        response_validator.assert_contains(test, response, "AI assistant")
        response_validator.assert_length(test, response, min_len=10, max_len=200)
        response_validator.assert_similarity(
            test, response,
            "I am an AI assistant ready to help",
            threshold=0.7,
        )

    tc1 = TestCase(
        name="Response Content Validation",
        description="Validate agent response content and format",
        priority=TestPriority.HIGH,
        tags=["content", "basic"],
    )
    tc1.set_test_function(test1)
    suite.add_test(tc1)

    # 测试2: JSON响应验证
    def test2(test: TestCase, ctx):
        response = '{"status": "success", "data": {"answer": "42", "confidence": 0.95}}'
        response_validator.assert_json_valid(test, response)
        response_validator.assert_json_path(test, response, "status", "success")
        response_validator.assert_json_path(test, response, "data.confidence", 0.95)

    tc2 = TestCase(
        name="JSON Response Validation",
        description="Validate structured JSON responses",
        priority=TestPriority.HIGH,
        tags=["json", "api"],
    )
    tc2.set_test_function(test2)
    suite.add_test(tc2)

    # 测试3: 工具调用验证
    def test3(test: TestCase, ctx):
        tool_calls = [
            {"name": "search", "parameters": {"query": "Python testing"}},
            {"name": "calculate", "parameters": {"expression": "2+2"}},
        ]
        tool_validator.assert_tool_called(test, tool_calls, "search")
        tool_validator.assert_max_tool_calls(test, tool_calls, 3)
        tool_validator.assert_no_duplicate_calls(test, tool_calls)

    tc3 = TestCase(
        name="Tool Call Validation",
        description="Validate agent tool usage patterns",
        priority=TestPriority.MEDIUM,
        tags=["tools", "behavior"],
    )
    tc3.set_test_function(test3)
    suite.add_test(tc3)

    # 测试4: 安全验证
    def test4(test: TestCase, ctx):
        response = "I can help you with programming questions and general knowledge."
        safety_validator.assert_no_dangerous_content(test, response)
        safety_validator.assert_no_pii_leak(test, response)

    tc4 = TestCase(
        name="Safety & Compliance Check",
        description="Check for dangerous content and PII leaks",
        priority=TestPriority.CRITICAL,
        tags=["safety", "security", "compliance"],
    )
    tc4.set_test_function(test4)
    suite.add_test(tc4)

    # 测试5: 响应时间验证
    def test5(test: TestCase, ctx):
        response_validator.assert_response_time(test, 1200, max_duration=3000)

    tc5 = TestCase(
        name="Performance Check",
        description="Validate response time performance",
        priority=TestPriority.MEDIUM,
        tags=["performance", "latency"],
    )
    tc5.set_test_function(test5)
    suite.add_test(tc5)

    return suite


def print_summary(results: dict):
    """打印测试汇总"""
    print("\n" + "=" * 60)
    print("🧪 AgentTestPilot Test Results")
    print("=" * 60)
    print(f"Total Tests:    {results.get('total_tests', 0)}")
    print(f"✅ Passed:      {results.get('passed', 0)}")
    print(f"❌ Failed:      {results.get('failed', 0)}")
    print(f"⚠️  Errors:      {results.get('errors', 0)}")
    print(f"⏭️  Skipped:     {results.get('skipped', 0)}")
    print(f"📈 Success Rate: {results.get('success_rate', 0) * 100:.1f}%")
    print(f"⏱️  Duration:    {results.get('total_duration', 0):.2f}s")
    print("=" * 60)


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "init": cmd_init,
        "run": cmd_run,
        "report": cmd_report,
        "validate": cmd_validate,
        "demo": cmd_demo,
    }

    handler = commands.get(args.command)
    if handler:
        try:
            return handler(args)
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user")
            return 130
        except Exception as e:
            print(f"❌ Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
