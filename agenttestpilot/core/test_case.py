#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Test Case & Test Suite Module
测试用例与测试套件模块
"""

import time
import uuid
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field


class TestStatus(Enum):
    """测试状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestPriority(Enum):
    """测试优先级枚举"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TestResult:
    """测试结果数据类"""
    status: TestStatus
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0
    timestamp: float = field(default_factory=time.time)
    trace_log: List[str] = field(default_factory=list)
    score: float = 0.0  # 0.0 - 1.0


@dataclass
class AssertionResult:
    """断言结果数据类"""
    passed: bool
    assertion_type: str
    expected: Any
    actual: Any
    message: str = ""
    diff: str = ""


class TestCase:
    """测试用例类"""

    def __init__(
        self,
        name: str,
        description: str = "",
        priority: TestPriority = TestPriority.MEDIUM,
        tags: Optional[List[str]] = None,
        timeout: Optional[float] = None,
        setup_func: Optional[Callable] = None,
        teardown_func: Optional[Callable] = None,
    ):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.description = description
        self.priority = priority
        self.tags = tags or []
        self.timeout = timeout
        self.setup_func = setup_func
        self.teardown_func = teardown_func
        self.result: Optional[TestResult] = None
        self.assertions: List[AssertionResult] = []
        self._test_func: Optional[Callable] = None
        self._metadata: Dict[str, Any] = {}

    def set_test_function(self, func: Callable):
        """设置测试执行函数"""
        self._test_func = func

    def add_assertion(self, result: AssertionResult):
        """添加断言结果"""
        self.assertions.append(result)

    def run(self, context: Optional[Dict[str, Any]] = None) -> TestResult:
        """执行测试用例"""
        start_time = time.time()
        context = context or {}
        trace_log = []

        try:
            # 执行setup
            if self.setup_func:
                trace_log.append(f"[SETUP] Running setup for '{self.name}'")
                self.setup_func(context)

            trace_log.append(f"[RUN] Executing test '{self.name}'")
            self.result = TestResult(status=TestStatus.RUNNING)

            # 执行测试函数
            if self._test_func:
                self._test_func(self, context)

            # 判断结果
            all_passed = all(a.passed for a in self.assertions)
            duration = time.time() - start_time

            if all_passed:
                self.result = TestResult(
                    status=TestStatus.PASSED,
                    message=f"All {len(self.assertions)} assertions passed",
                    duration=duration,
                    trace_log=trace_log,
                    score=1.0,
                )
            else:
                failed = [a for a in self.assertions if not a.passed]
                self.result = TestResult(
                    status=TestStatus.FAILED,
                    message=f"{len(failed)}/{len(self.assertions)} assertions failed",
                    duration=duration,
                    trace_log=trace_log,
                    score=len([a for a in self.assertions if a.passed]) / len(self.assertions) if self.assertions else 0.0,
                )

        except Exception as e:
            duration = time.time() - start_time
            self.result = TestResult(
                status=TestStatus.ERROR,
                message=str(e),
                duration=duration,
                trace_log=trace_log,
                score=0.0,
            )

        finally:
            # 执行teardown
            if self.teardown_func:
                try:
                    trace_log.append(f"[TEARDOWN] Running teardown for '{self.name}'")
                    self.teardown_func(context)
                except Exception as e:
                    trace_log.append(f"[TEARDOWN ERROR] {e}")

            if self.result:
                self.result.trace_log = trace_log

        return self.result

    def to_dict(self) -> Dict[str, Any]:
        """导出为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority.value,
            "tags": self.tags,
            "timeout": self.timeout,
            "assertions": [
                {
                    "passed": a.passed,
                    "type": a.assertion_type,
                    "expected": str(a.expected),
                    "actual": str(a.actual),
                    "message": a.message,
                }
                for a in self.assertions
            ],
            "result": {
                "status": self.result.status.value if self.result else None,
                "message": self.result.message if self.result else "",
                "duration": self.result.duration if self.result else 0.0,
                "score": self.result.score if self.result else 0.0,
            } if self.result else None,
        }


class TestSuite:
    """测试套件类"""

    def __init__(self, name: str, description: str = ""):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.description = description
        self.test_cases: List[TestCase] = []
        self._setup_func: Optional[Callable] = None
        self._teardown_func: Optional[Callable] = None
        self._context: Dict[str, Any] = {}

    def add_test(self, test_case: TestCase):
        """添加测试用例"""
        self.test_cases.append(test_case)

    def add_tests(self, test_cases: List[TestCase]):
        """批量添加测试用例"""
        self.test_cases.extend(test_cases)

    def set_setup(self, func: Callable):
        """设置套件级setup"""
        self._setup_func = func

    def set_teardown(self, func: Callable):
        """设置套件级teardown"""
        self._teardown_func = func

    def run(self, config: Optional[Any] = None) -> Dict[str, Any]:
        """执行整个测试套件"""
        import time
        start_time = time.time()
        results = []

        # 套件级setup
        if self._setup_func:
            self._setup_func(self._context)

        for test in self.test_cases:
            result = test.run(self._context)
            results.append({
                "test": test.to_dict(),
                "result": {
                    "status": result.status.value,
                    "message": result.message,
                    "duration": result.duration,
                    "score": result.score,
                }
            })

        # 套件级teardown
        if self._teardown_func:
            self._teardown_func(self._context)

        total_duration = time.time() - start_time
        passed = sum(1 for r in results if r["result"]["status"] == "passed")
        failed = sum(1 for r in results if r["result"]["status"] == "failed")
        errors = sum(1 for r in results if r["result"]["status"] == "error")
        skipped = sum(1 for r in results if r["result"]["status"] == "skipped")

        return {
            "suite_id": self.id,
            "suite_name": self.name,
            "total_tests": len(self.test_cases),
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "duration": total_duration,
            "success_rate": passed / len(self.test_cases) if self.test_cases else 0.0,
            "results": results,
        }

    def filter_by_tags(self, tags: List[str]) -> "TestSuite":
        """按标签过滤测试用例"""
        filtered = TestSuite(f"{self.name} (filtered)", self.description)
        for test in self.test_cases:
            if any(tag in test.tags for tag in tags):
                filtered.add_test(test)
        return filtered

    def filter_by_priority(self, min_priority: TestPriority) -> "TestSuite":
        """按优先级过滤测试用例"""
        priority_order = {
            TestPriority.CRITICAL: 4,
            TestPriority.HIGH: 3,
            TestPriority.MEDIUM: 2,
            TestPriority.LOW: 1,
        }
        filtered = TestSuite(f"{self.name} (filtered)", self.description)
        min_level = priority_order.get(min_priority, 0)
        for test in self.test_cases:
            if priority_order.get(test.priority, 0) >= min_level:
                filtered.add_test(test)
        return filtered
