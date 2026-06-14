#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Test Engine Module
测试引擎核心模块
"""

import os
import time
import json
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import Config
from .test_case import TestSuite, TestCase, TestStatus
from .reporter import Reporter, HTMLReporter, MarkdownReporter, JSONReporter


class TestEngine:
    """测试引擎主类"""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.default()
        self.suites: List[TestSuite] = []
        self._reporters: List[Reporter] = []
        self._hooks: Dict[str, List[Callable]] = {
            "before_all": [],
            "after_all": [],
            "before_suite": [],
            "after_suite": [],
            "before_test": [],
            "after_test": [],
        }
        self._results: List[Dict[str, Any]] = []

    def add_suite(self, suite: TestSuite):
        """添加测试套件"""
        self.suites.append(suite)

    def add_reporter(self, reporter: Reporter):
        """添加报告生成器"""
        self._reporters.append(reporter)

    def register_hook(self, hook_name: str, func: Callable):
        """注册钩子函数"""
        if hook_name in self._hooks:
            self._hooks[hook_name].append(func)

    def _run_hooks(self, hook_name: str, *args, **kwargs):
        """执行钩子函数"""
        for func in self._hooks.get(hook_name, []):
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"[HOOK ERROR] {hook_name}: {e}")

    def run(self, suite_filter: Optional[str] = None,
            tag_filter: Optional[List[str]] = None,
            priority_filter: Optional[str] = None) -> Dict[str, Any]:
        """执行所有测试套件"""
        start_time = time.time()
        self._results = []

        # 全局before_all钩子
        self._run_hooks("before_all", self)

        suites_to_run = self.suites
        if suite_filter:
            suites_to_run = [s for s in suites_to_run if suite_filter in s.name]

        for suite in suites_to_run:
            # 过滤测试用例
            filtered_suite = suite
            if tag_filter:
                filtered_suite = suite.filter_by_tags(tag_filter)
            if priority_filter:
                from .test_case import TestPriority
                priority_map = {
                    "critical": TestPriority.CRITICAL,
                    "high": TestPriority.HIGH,
                    "medium": TestPriority.MEDIUM,
                    "low": TestPriority.LOW,
                }
                if priority_filter.lower() in priority_map:
                    filtered_suite = filtered_suite.filter_by_priority(
                        priority_map[priority_filter.lower()]
                    )

            # Suite级before钩子
            self._run_hooks("before_suite", filtered_suite)

            # 执行套件
            result = filtered_suite.run(self.config)
            self._results.append(result)

            # Suite级after钩子
            self._run_hooks("after_suite", filtered_suite, result)

        # 全局after_all钩子
        self._run_hooks("after_all", self)

        total_duration = time.time() - start_time

        # 汇总结果
        summary = self._generate_summary(total_duration)

        # 生成报告
        self._generate_reports(summary)

        return summary

    def run_parallel(self, max_workers: Optional[int] = None) -> Dict[str, Any]:
        """并行执行测试套件"""
        start_time = time.time()
        self._results = []
        max_workers = max_workers or self.config.get("concurrency", 4)

        self._run_hooks("before_all", self)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_suite = {}
            for suite in self.suites:
                self._run_hooks("before_suite", suite)
                future = executor.submit(suite.run, self.config)
                future_to_suite[future] = suite

            for future in as_completed(future_to_suite):
                suite = future_to_suite[future]
                try:
                    result = future.result()
                    self._results.append(result)
                    self._run_hooks("after_suite", suite, result)
                except Exception as e:
                    self._results.append({
                        "suite_name": suite.name,
                        "error": str(e),
                        "total_tests": 0,
                        "passed": 0,
                        "failed": 0,
                        "errors": 1,
                        "skipped": 0,
                        "duration": 0,
                        "success_rate": 0.0,
                        "results": [],
                    })

        self._run_hooks("after_all", self)
        total_duration = time.time() - start_time
        summary = self._generate_summary(total_duration)
        self._generate_reports(summary)
        return summary

    def _generate_summary(self, total_duration: float) -> Dict[str, Any]:
        """生成测试汇总"""
        total_tests = sum(r["total_tests"] for r in self._results)
        total_passed = sum(r["passed"] for r in self._results)
        total_failed = sum(r["failed"] for r in self._results)
        total_errors = sum(r["errors"] for r in self._results)
        total_skipped = sum(r["skipped"] for r in self._results)

        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_duration": total_duration,
            "total_suites": len(self._results),
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "errors": total_errors,
            "skipped": total_skipped,
            "success_rate": total_passed / total_tests if total_tests > 0 else 0.0,
            "suite_results": self._results,
        }

    def _generate_reports(self, summary: Dict[str, Any]):
        """生成测试报告"""
        output_dir = self.config.get("output_dir", "./reports")
        os.makedirs(output_dir, exist_ok=True)

        # 如果没有自定义reporter，使用默认
        if not self._reporters:
            formats = self.config.get("output_formats", ["json", "html", "markdown"])
            if "json" in formats:
                self._reporters.append(JSONReporter())
            if "html" in formats:
                self._reporters.append(HTMLReporter())
            if "markdown" in formats:
                self._reporters.append(MarkdownReporter())

        for reporter in self._reporters:
            try:
                filepath = os.path.join(output_dir, reporter.default_filename)
                reporter.generate(summary, filepath)
                print(f"[REPORT] Generated: {filepath}")
            except Exception as e:
                print(f"[REPORT ERROR] {type(reporter).__name__}: {e}")

    def get_results(self) -> List[Dict[str, Any]]:
        """获取所有结果"""
        return self._results

    def export_results(self, filepath: str):
        """导出结果到JSON文件"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self._results, f, indent=2, ensure_ascii=False)
