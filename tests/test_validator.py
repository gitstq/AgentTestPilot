#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Validator Tests
验证器单元测试
"""

import unittest

from agenttestpilot.core.test_case import TestCase
from agenttestpilot.core.validator import (
    ResponseValidator,
    ToolCallValidator,
    SafetyValidator,
)


class TestResponseValidator(unittest.TestCase):
    """测试响应验证器"""

    def setUp(self):
        self.validator = ResponseValidator()
        self.test = TestCase(name="Test")

    def test_assert_contains_pass(self):
        """测试包含断言-通过"""
        self.validator.assert_contains(self.test, "hello world", "world")
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_contains_fail(self):
        """测试包含断言-失败"""
        self.validator.assert_contains(self.test, "hello world", "foo")
        self.assertFalse(self.test.assertions[0].passed)

    def test_assert_json_valid_pass(self):
        """测试JSON有效断言-通过"""
        self.validator.assert_json_valid(self.test, '{"key": "value"}')
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_json_valid_fail(self):
        """测试JSON有效断言-失败"""
        self.validator.assert_json_valid(self.test, "not json")
        self.assertFalse(self.test.assertions[0].passed)

    def test_assert_json_path(self):
        """测试JSON路径断言"""
        self.validator.assert_json_path(
            self.test, '{"data": {"name": "test"}}', "data.name", "test"
        )
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_length(self):
        """测试长度断言"""
        self.validator.assert_length(self.test, "hello", min_len=3, max_len=10)
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_similarity(self):
        """测试相似度断言"""
        self.validator.assert_similarity(
            self.test, "hello world", "hello world", threshold=0.9
        )
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_regex_match(self):
        """测试正则匹配断言"""
        self.validator.assert_regex_match(self.test, "hello 123", r"\d+")
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_response_time(self):
        """测试响应时间断言"""
        self.validator.assert_response_time(self.test, 100, max_duration=500)
        self.assertTrue(self.test.assertions[0].passed)


class TestToolCallValidator(unittest.TestCase):
    """测试工具调用验证器"""

    def setUp(self):
        self.validator = ToolCallValidator()
        self.test = TestCase(name="Tool Test")

    def test_assert_tool_called(self):
        """测试工具被调用断言"""
        tool_calls = [{"name": "search"}, {"name": "calculate"}]
        self.validator.assert_tool_called(self.test, tool_calls, "search")
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_tool_order(self):
        """测试工具顺序断言"""
        tool_calls = [{"name": "a"}, {"name": "b"}]
        self.validator.assert_tool_order(self.test, tool_calls, ["a", "b"])
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_max_tool_calls(self):
        """测试最大工具调用次数断言"""
        tool_calls = [{"name": "a"}, {"name": "b"}]
        self.validator.assert_max_tool_calls(self.test, tool_calls, 3)
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_no_duplicate_calls(self):
        """测试无重复调用断言"""
        tool_calls = [{"name": "a"}, {"name": "b"}]
        self.validator.assert_no_duplicate_calls(self.test, tool_calls)
        self.assertTrue(self.test.assertions[0].passed)


class TestSafetyValidator(unittest.TestCase):
    """测试安全验证器"""

    def setUp(self):
        self.validator = SafetyValidator()
        self.test = TestCase(name="Safety Test")

    def test_assert_no_dangerous_content_pass(self):
        """测试无危险内容-通过"""
        self.validator.assert_no_dangerous_content(self.test, "Hello world")
        self.assertTrue(self.test.assertions[0].passed)

    def test_assert_no_dangerous_content_fail(self):
        """测试无危险内容-失败"""
        self.validator.assert_no_dangerous_content(
            self.test, "rm -rf / important files"
        )
        self.assertFalse(self.test.assertions[0].passed)

    def test_assert_no_pii_leak_pass(self):
        """测试无PII泄露-通过"""
        self.validator.assert_no_pii_leak(self.test, "Hello world")
        self.assertTrue(self.test.assertions[0].passed)


if __name__ == "__main__":
    unittest.main()
