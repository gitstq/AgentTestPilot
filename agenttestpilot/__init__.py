#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot 🧪
轻量级AI Agent自动化测试与行为验证引擎

一个零依赖(核心)、跨平台的AI Agent测试框架，支持：
- 行为一致性验证
- 响应质量评分
- 工具调用链追踪
- 多格式报告生成
- TUI仪表盘

Author: gitstq
License: MIT
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .core.engine import TestEngine
from .core.test_case import TestCase, TestSuite
from .core.validator import ResponseValidator, ToolCallValidator
from .core.reporter import Reporter, HTMLReporter, MarkdownReporter, JSONReporter
from .core.config import Config

__all__ = [
    "TestEngine",
    "TestCase",
    "TestSuite",
    "ResponseValidator",
    "ToolCallValidator",
    "Reporter",
    "HTMLReporter",
    "MarkdownReporter",
    "JSONReporter",
    "Config",
]
