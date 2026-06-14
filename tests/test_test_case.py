#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - TestCase & TestSuite Tests
测试用例与套件单元测试
"""

import unittest

from agenttestpilot.core.test_case import TestCase, TestSuite, TestPriority, TestStatus
from agenttestpilot.core.validator import ResponseValidator


class TestTestCase(unittest.TestCase):
    """测试测试用例类"""

    def test_create_test_case(self):
        """测试创建测试用例"""
        tc = TestCase(
            name="Test 1",
            description="A test",
            priority=TestPriority.HIGH,
            tags=["api"],
        )
        self.assertEqual(tc.name, "Test 1")
        self.assertEqual(tc.priority, TestPriority.HIGH)
        self.assertEqual(tc.tags, ["api"])
        self.assertIsNone(tc.result)

    def test_run_passing_test(self):
        """测试运行通过的测试"""
        validator = ResponseValidator()

        def test_func(test, ctx):
            response = "Hello AI assistant"
            validator.assert_contains(test, response, "AI")

        tc = TestCase(name="Passing Test")
        tc.set_test_function(test_func)
        result = tc.run()

        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertEqual(len(tc.assertions), 1)
        self.assertTrue(tc.assertions[0].passed)

    def test_run_failing_test(self):
        """测试运行失败的测试"""
        validator = ResponseValidator()

        def test_func(test, ctx):
            response = "Hello world"
            validator.assert_contains(test, response, "AI")

        tc = TestCase(name="Failing Test")
        tc.set_test_function(test_func)
        result = tc.run()

        self.assertEqual(result.status, TestStatus.FAILED)
        self.assertEqual(len(tc.assertions), 1)
        self.assertFalse(tc.assertions[0].passed)

    def test_run_with_setup_teardown(self):
        """测试带setup和teardown的测试"""
        setup_called = []
        teardown_called = []

        def setup(ctx):
            setup_called.append(True)
            ctx["value"] = 42

        def teardown(ctx):
            teardown_called.append(True)

        def test_func(test, ctx):
            self.assertEqual(ctx.get("value"), 42)

        tc = TestCase(name="Setup Test", setup_func=setup, teardown_func=teardown)
        tc.set_test_function(test_func)
        tc.run()

        self.assertTrue(setup_called)
        self.assertTrue(teardown_called)

    def test_to_dict(self):
        """测试导出为字典"""
        tc = TestCase(name="Dict Test", tags=["tag1"])
        data = tc.to_dict()
        self.assertEqual(data["name"], "Dict Test")
        self.assertEqual(data["tags"], ["tag1"])


class TestTestSuite(unittest.TestCase):
    """测试测试套件类"""

    def test_create_suite(self):
        """测试创建套件"""
        suite = TestSuite("My Suite", "Description")
        self.assertEqual(suite.name, "My Suite")
        self.assertEqual(len(suite.test_cases), 0)

    def test_add_tests(self):
        """测试添加测试"""
        suite = TestSuite("Suite")
        tc1 = TestCase(name="Test 1")
        tc2 = TestCase(name="Test 2")
        suite.add_test(tc1)
        suite.add_tests([tc2])
        self.assertEqual(len(suite.test_cases), 2)

    def test_run_suite(self):
        """测试运行套件"""
        validator = ResponseValidator()
        suite = TestSuite("Run Suite")

        def test_func(test, ctx):
            validator.assert_contains(test, "hello", "hello")

        tc = TestCase(name="Simple Test")
        tc.set_test_function(test_func)
        suite.add_test(tc)

        results = suite.run()
        self.assertEqual(results["total_tests"], 1)
        self.assertEqual(results["passed"], 1)
        self.assertEqual(results["failed"], 0)

    def test_filter_by_tags(self):
        """测试按标签过滤"""
        suite = TestSuite("Filter Suite")
        tc1 = TestCase(name="T1", tags=["api"])
        tc2 = TestCase(name="T2", tags=["ui"])
        suite.add_tests([tc1, tc2])

        filtered = suite.filter_by_tags(["api"])
        self.assertEqual(len(filtered.test_cases), 1)
        self.assertEqual(filtered.test_cases[0].name, "T1")


if __name__ == "__main__":
    unittest.main()
