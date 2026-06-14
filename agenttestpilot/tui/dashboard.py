#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - TUI Dashboard Module
终端用户界面仪表盘模块
"""

import os
import sys
import time
from typing import Dict, List, Any, Optional


class TUIDashboard:
    """TUI仪表盘类 - 零依赖实现"""

    # ANSI颜色码
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
    }

    def __init__(self):
        self.terminal_width = self._get_terminal_width()
        self.use_color = self._supports_color()

    def _get_terminal_width(self) -> int:
        """获取终端宽度"""
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80

    def _supports_color(self) -> bool:
        """检查终端是否支持颜色"""
        if os.environ.get("NO_COLOR"):
            return False
        if os.environ.get("FORCE_COLOR"):
            return True
        return sys.stdout.isatty()

    def _color(self, text: str, color: str) -> str:
        """添加颜色"""
        if not self.use_color:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"

    def _center(self, text: str, width: Optional[int] = None, fill: str = " ") -> str:
        """居中文字"""
        width = width or self.terminal_width
        return text.center(width, fill)

    def _hline(self, char: str = "─", width: Optional[int] = None) -> str:
        """水平分隔线"""
        width = width or self.terminal_width
        return char * width

    def clear(self):
        """清屏"""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def show_header(self):
        """显示标题头"""
        print()
        print(self._color(self._center("🧪 AgentTestPilot", fill=" "), "cyan"))
        print(self._color(self._center("AI Agent Automated Testing & Behavior Validation Engine", fill=" "), "dim"))
        print(self._color(self._hline("═"), "cyan"))
        print()

    def show_progress(self, current: int, total: int, label: str = "Progress"):
        """显示进度条"""
        width = min(50, self.terminal_width - 20)
        filled = int(width * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (width - filled)
        percent = (current / total * 100) if total > 0 else 0

        color = "green" if current == total else "yellow"
        print(f"\r{label}: [{self._color(bar, color)}] {percent:.0f}% ({current}/{total})", end="", flush=True)

        if current == total:
            print()

    def show_test_running(self, test_name: str, suite_name: str = ""):
        """显示正在运行的测试"""
        prefix = f"[{suite_name}] " if suite_name else ""
        print(f"  🔄 {prefix}{test_name} ...", end="", flush=True)

    def show_test_result(self, test_name: str, status: str, duration: float = 0):
        """显示测试结果"""
        icons = {
            "passed": "✅",
            "failed": "❌",
            "error": "⚠️",
            "skipped": "⏭️",
        }
        icon = icons.get(status, "❓")
        color = "green" if status == "passed" else "red" if status == "failed" else "yellow"

        # 清除之前的"..."
        print(f"\r  {icon} {test_name} ({duration:.2f}s)")

    def show_summary(self, results: Dict[str, Any]):
        """显示测试汇总"""
        print()
        print(self._color(self._hline("═"), "cyan"))
        print(self._color(" 📊 Test Summary ", "bold"))
        print(self._color(self._hline("═"), "cyan"))
        print()

        total = results.get("total_tests", 0)
        passed = results.get("passed", 0)
        failed = results.get("failed", 0)
        errors = results.get("errors", 0)
        skipped = results.get("skipped", 0)
        rate = results.get("success_rate", 0) * 100
        duration = results.get("total_duration", 0)

        # 统计卡片
        self._show_stat_card("Total", total, "blue")
        self._show_stat_card("Passed", passed, "green")
        self._show_stat_card("Failed", failed, "red")
        self._show_stat_card("Errors", errors, "yellow")
        self._show_stat_card("Skipped", skipped, "white")

        print()

        # 成功率
        rate_color = "green" if rate >= 90 else "yellow" if rate >= 70 else "red"
        print(f"  📈 Success Rate: {self._color(f'{rate:.1f}%', rate_color)}")
        print(f"  ⏱️  Duration: {duration:.2f}s")

        # 套件详情
        if results.get("suite_results"):
            print()
            print(self._color(" 📁 Suite Details:", "bold"))
            print()

            for suite in results["suite_results"]:
                suite_name = suite.get("suite_name", "Unknown")
                suite_passed = suite.get("passed", 0)
                suite_total = suite.get("total_tests", 0)
                suite_rate = (suite_passed / suite_total * 100) if suite_total > 0 else 0

                suite_color = "green" if suite_rate == 100 else "red" if suite_rate < 100 else "yellow"
                status_icon = "✅" if suite_rate == 100 else "❌"

                print(f"  {status_icon} {self._color(suite_name, suite_color)}")
                print(f"     Tests: {suite_total} | Passed: {suite_passed} | Rate: {suite_rate:.0f}%")

                # 显示失败的测试
                for result in suite.get("results", []):
                    test_result = result.get("result", {})
                    if test_result.get("status") in ("failed", "error"):
                        test_name = result.get("test", {}).get("name", "Unknown")
                        msg = test_result.get("message", "")
                        print(f"     ❌ {test_name}: {msg[:60]}")

                print()

        # 底部
        print(self._color(self._hline("═"), "cyan"))

        if rate == 100:
            print(self._color("  🎉 All tests passed!", "green"))
        elif failed > 0:
            print(self._color(f"  ⚠️  {failed} test(s) failed", "yellow"))
        print()

    def _show_stat_card(self, label: str, value: int, color: str):
        """显示统计卡片"""
        value_str = str(value)
        padding = 8 - len(value_str)
        print(f"  {self._color(label + ':', 'bold')} {self._color(value_str, color)}{' ' * padding}", end="")

    def show_error(self, message: str):
        """显示错误信息"""
        print(f"\n  {self._color('❌ Error:', 'red')} {message}\n")

    def show_success(self, message: str):
        """显示成功信息"""
        print(f"\n  {self._color('✅ Success:', 'green')} {message}\n")

    def show_info(self, message: str):
        """显示信息"""
        print(f"  {self._color('ℹ️', 'blue')} {message}")

    def show_spinner(self, message: str = "Loading"):
        """显示旋转器（简化版）"""
        print(f"  ⏳ {message}...")


class SimpleProgressBar:
    """简单进度条"""

    def __init__(self, total: int, width: int = 40):
        self.total = total
        self.current = 0
        self.width = width

    def update(self, increment: int = 1):
        """更新进度"""
        self.current += increment
        filled = int(self.width * self.current / self.total) if self.total > 0 else 0
        bar = "█" * filled + "░" * (self.width - filled)
        percent = (self.current / self.total * 100) if self.total > 0 else 0
        print(f"\r[{bar}] {percent:.0f}%", end="", flush=True)

    def finish(self):
        """完成进度条"""
        self.current = self.total
        self.update(0)
        print()
