#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Engine Tests
测试引擎单元测试
"""

import os
import tempfile
import unittest

from agenttestpilot.core.engine import TestEngine
from agenttestpilot.core.config import Config
from agenttestpilot.core.test_case import TestSuite, TestCase
from agenttestpilot.core.validator import ResponseValidator


class TestTestEngine(unittest.TestCase):
    """测试测试引擎"""

    def setUp(self):
        self.engine = TestEngine()

    def test_add_suite(self):
        """测试添加套件"""
        suite = TestSuite("Test Suite")
        self.engine.add_suite(suite)
        self.assertEqual(len(self.engine.suites), 1)

    def test_run_single_suite(self):
        """测试运行单个套件"""
        validator = ResponseValidator()
        suite = TestSuite("Run Suite")

        def test_func(test, ctx):
            validator.assert_contains(test, "hello", "hello")

        tc = TestCase(name="Simple")
        tc.set_test_function(test_func)
        suite.add_test(tc)
        self.engine.add_suite(suite)

        results = self.engine.run()
        self.assertEqual(results["total_tests"], 1)
        self.assertEqual(results["passed"], 1)

    def test_run_with_config(self):
        """测试使用配置运行"""
        config = Config()
        config.set("output_dir", tempfile.mkdtemp())
        engine = TestEngine(config)

        suite = TestSuite("Config Suite")
        tc = TestCase(name="Config Test")

        def test_func(test, ctx):
            validator = ResponseValidator()
            validator.assert_contains(test, "test", "test")

        tc.set_test_function(test_func)
        suite.add_test(tc)
        engine.add_suite(suite)

        results = engine.run()
        self.assertEqual(results["total_tests"], 1)

    def test_export_results(self):
        """测试导出结果"""
        suite = TestSuite("Export Suite")
        tc = TestCase(name="Export Test")

        def test_func(test, ctx):
            validator = ResponseValidator()
            validator.assert_contains(test, "x", "x")

        tc.set_test_function(test_func)
        suite.add_test(tc)
        self.engine.add_suite(suite)
        self.engine.run()

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            self.engine.export_results(temp_path)
            self.assertTrue(os.path.exists(temp_path))
            self.assertGreater(os.path.getsize(temp_path), 0)
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
