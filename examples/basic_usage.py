#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Basic Usage Example
基础使用示例
"""

from agenttestpilot import TestEngine, TestSuite, TestCase, TestPriority
from agenttestpilot.core.validator import ResponseValidator, ToolCallValidator, SafetyValidator


def main():
    # 创建测试引擎
    engine = TestEngine()

    # 创建测试套件
    suite = TestSuite(
        name="My Agent Tests",
        description="Testing my AI agent behavior",
    )

    # 创建验证器
    response_validator = ResponseValidator()
    tool_validator = ToolCallValidator()
    safety_validator = SafetyValidator()

    # ========== 测试用例 1: 基本响应验证 ==========
    def test_basic_response(test: TestCase, ctx):
        # 模拟Agent响应
        response = ctx.get("agent_response",
            "Hello! I am an AI assistant. I can help you with programming, writing, and analysis tasks.")

        # 验证响应包含关键内容
        response_validator.assert_contains(test, response, "AI assistant")

        # 验证响应长度在合理范围内
        response_validator.assert_length(test, response, min_len=10, max_len=500)

        # 验证响应与期望内容的相似度
        response_validator.assert_similarity(
            test, response,
            "I am an AI assistant",
            threshold=0.6,
        )

    tc1 = TestCase(
        name="Basic Response Validation",
        description="Validate basic agent response content and format",
        priority=TestPriority.HIGH,
        tags=["content", "basic", "api"],
    )
    tc1.set_test_function(test_basic_response)
    suite.add_test(tc1)

    # ========== 测试用例 2: JSON响应验证 ==========
    def test_json_response(test: TestCase, ctx):
        response = ctx.get("json_response",
            '{"status": "success", "data": {"answer": "42", "confidence": 0.95, "sources": ["wiki"]}}')

        # 验证是有效JSON
        response_validator.assert_json_valid(test, response)

        # 验证JSON路径值
        response_validator.assert_json_path(test, response, "status", "success")
        response_validator.assert_json_path(test, response, "data.confidence", 0.95)

    tc2 = TestCase(
        name="JSON Response Validation",
        description="Validate structured JSON responses from agent",
        priority=TestPriority.HIGH,
        tags=["json", "api", "structured"],
    )
    tc2.set_test_function(test_json_response)
    suite.add_test(tc2)

    # ========== 测试用例 3: 工具调用验证 ==========
    def test_tool_calls(test: TestCase, ctx):
        tool_calls = ctx.get("tool_calls", [
            {"name": "search", "parameters": {"query": "Python testing best practices"}},
            {"name": "calculate", "parameters": {"expression": "len([1,2,3])"}},
        ])

        # 验证特定工具被调用
        tool_validator.assert_tool_called(test, tool_calls, "search")

        # 验证工具调用次数不超过限制
        tool_validator.assert_max_tool_calls(test, tool_calls, 5)

        # 验证没有重复调用
        tool_validator.assert_no_duplicate_calls(test, tool_calls)

    tc3 = TestCase(
        name="Tool Call Validation",
        description="Validate agent tool usage patterns",
        priority=TestPriority.MEDIUM,
        tags=["tools", "behavior"],
    )
    tc3.set_test_function(test_tool_calls)
    suite.add_test(tc3)

    # ========== 测试用例 4: 安全验证 ==========
    def test_safety(test: TestCase, ctx):
        response = ctx.get("agent_response",
            "I can help you with programming questions and general knowledge.")

        # 验证没有危险内容
        safety_validator.assert_no_dangerous_content(test, response)

        # 验证没有PII泄露
        safety_validator.assert_no_pii_leak(test, response)

    tc4 = TestCase(
        name="Safety & Compliance",
        description="Check for dangerous content and PII leaks",
        priority=TestPriority.CRITICAL,
        tags=["safety", "security", "compliance"],
    )
    tc4.set_test_function(test_safety)
    suite.add_test(tc4)

    # ========== 测试用例 5: 性能验证 ==========
    def test_performance(test: TestCase, ctx):
        response_time = ctx.get("response_time_ms", 800)

        # 验证响应时间在可接受范围内
        response_validator.assert_response_time(test, response_time, max_duration=2000)

    tc5 = TestCase(
        name="Performance Check",
        description="Validate response time performance",
        priority=TestPriority.MEDIUM,
        tags=["performance", "latency"],
    )
    tc5.set_test_function(test_performance)
    suite.add_test(tc5)

    # 添加套件到引擎并运行
    engine.add_suite(suite)
    results = engine.run()

    # 打印结果
    print("\n" + "=" * 60)
    print("🧪 AgentTestPilot Results")
    print("=" * 60)
    print(f"Total Tests: {results['total_tests']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"⚠️  Errors: {results['errors']}")
    print(f"📈 Success Rate: {results['success_rate'] * 100:.1f}%")
    print(f"⏱️  Duration: {results['total_duration']:.2f}s")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
