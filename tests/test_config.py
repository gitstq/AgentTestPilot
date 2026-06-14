#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Config Tests
配置模块单元测试
"""

import os
import json
import tempfile
import unittest

from agenttestpilot.core.config import Config


class TestConfig(unittest.TestCase):
    """测试配置类"""

    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        self.assertEqual(config.get("timeout"), 30)
        self.assertEqual(config.get("max_retries"), 3)
        self.assertEqual(config.get("concurrency"), 4)
        self.assertEqual(config.get("log_level"), "INFO")

    def test_custom_value(self):
        """测试自定义值"""
        config = Config()
        config.set("timeout", 60)
        self.assertEqual(config.get("timeout"), 60)

    def test_load_from_file(self):
        """测试从文件加载"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"timeout": 45, "custom_key": "value"}, f)
            temp_path = f.name

        try:
            config = Config(temp_path)
            self.assertEqual(config.get("timeout"), 45)
            self.assertEqual(config.get("custom_key"), "value")
        finally:
            os.unlink(temp_path)

    def test_save_to_file(self):
        """测试保存到文件"""
        config = Config()
        config.set("test_key", "test_value")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            config.save_to_file(temp_path)
            with open(temp_path, "r") as f:
                data = json.load(f)
            self.assertEqual(data["test_key"], "test_value")
        finally:
            os.unlink(temp_path)

    def test_to_dict(self):
        """测试导出为字典"""
        config = Config()
        data = config.to_dict()
        self.assertIn("timeout", data)
        self.assertIn("max_retries", data)


if __name__ == "__main__":
    unittest.main()
