#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Advanced Usage Example
高级使用示例 - 展示钩子、并行执行、自定义验证器
"""

from agenttestpilot import TestEngine, TestSuite, TestCase, TestPriority
from agenttestpilot.core.config import Config
from agenttestpilot.core.validator import ResponseValidator


def main():
    # 创建自定义配置
    config = Config()
    config.set("concurrency", 4)
    config.set("output_dir", "./reports")
    config.set("output_formats", ["json", "html", "markdown"])
    config.set("capture_traces", True)

    # 创建引擎
    engine = TestEngine(config)

    # ========== 注册全局钩子 ==========
    def before_all_hook(engine):
        print("🚀 Starting test run...")

    def after_all_hook(engine):
        print("✅ Test run completed!")

    def before_suite_hook(suite):
        print(f"📁 Running suite: {suite.name}")

    def after_suite_hook(suite, result):
        print(f"📊 Suite '{suite.name}' completed: {result['passed']}/{result['total_tests']} passed")

    engine.register_hook("before_all", before_all_hook)
    engine.register_hook("after_all", after_all_hook)
    engine.register_hook("before_suite", before_suite_hook)
    engine.register_hook("after_suite", after_suite_hook)

    # ========== 创建多个测试套件 ==========

    # 套件1: API测试
    api_suite = TestSuite("API Tests", "API response validation")
    validator = ResponseValidator()

    def test_api_status(test, ctx):
        response = '{"status": "ok", "version": "1.0.0"}'
        validator.assert_json_valid(test, response)
        validator.assert_json_path(test, response, "status", "ok")

    tc1 = TestCase(name="API Status Check", priority=TestPriority.CRITICAL, tags=["api"])
    tc1.set_test_function(test_api_status)
    api_suite.add_test(tc1)

    def test_api_data(test, ctx):
        response = '{"data": {"users": 100, "active": true}}'
        validator.assert_json_path(test, response, "data.users", 100)

    tc2 = TestCase(name="API Data Validation", priority=TestPriority.HIGH, tags=["api"])
    tc2.set_test_function(test_api_data)
    api_suite.add_test(tc2)

    # 套件2: 内容测试
    content_suite = TestSuite("Content Tests", "Response content validation")

    def test_content_quality(test, ctx):
        response = "This is a detailed and helpful response for the user."
        validator.assert_length(test, response, min_len=20)
        validator.assert_contains(test, response, "helpful")

    tc3 = TestCase(name="Content Quality", priority=TestPriority.HIGH, tags=["content"])
    tc3.set_test_function(test_content_quality)
    content_suite.add_test(tc3)

    def test_content_safety(test, ctx):
        response = "Safe and appropriate content for all users."
        validator.assert_not_contains(test, response, "inappropriate")

    tc4 = TestCase(name="Content Safety", priority=TestPriority.CRITICAL, tags=["content", "safety"])
    tc4.set_test_function(test_content_safety)
    content_suite.add_test(tc4)

    # 添加套件到引擎
    engine.add_suite(api_suite)
    engine.add_suite(content_suite)

    # ========== 运行测试（串行） ==========
    print("\n" + "=" * 60)
    print("Running tests sequentially...")
    print("=" * 60)
    results = engine.run()

    print("\n📈 Sequential Results:")
    print(f"   Total: {results['total_tests']}")
    print(f"   Passed: {results['passed']}")
    print(f"   Failed: {results['failed']}")
    print(f"   Duration: {results['total_duration']:.2f}s")

    # ========== 运行测试（并行） ==========
    print("\n" + "=" * 60)
    print("Running tests in parallel...")
    print("=" * 60)
    parallel_results = engine.run_parallel(max_workers=2)

    print("\n📈 Parallel Results:")
    print(f"   Total: {parallel_results['total_tests']}")
    print(f"   Passed: {parallel_results['passed']}")
    print(f"   Failed: {parallel_results['failed']}")
    print(f"   Duration: {parallel_results['total_duration']:.2f}s")

    # ========== 按标签过滤运行 ==========
    print("\n" + "=" * 60)
    print("Running tests with tag filter [api]...")
    print("=" * 60)
    filtered_results = engine.run(tag_filter=["api"])

    print("\n📈 Filtered Results (tag='api'):")
    print(f"   Total: {filtered_results['total_tests']}")
    print(f"   Passed: {filtered_results['passed']}")

    return results


if __name__ == "__main__":
    main()
