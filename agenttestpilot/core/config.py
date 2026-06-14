#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Configuration Module
配置管理模块
"""

import os
import json
from typing import Dict, Any, Optional


class Config:
    """配置管理类"""

    DEFAULT_CONFIG = {
        "timeout": 30,
        "max_retries": 3,
        "retry_delay": 1.0,
        "concurrency": 4,
        "output_dir": "./reports",
        "output_formats": ["json", "html", "markdown"],
        "strict_mode": False,
        "capture_traces": True,
        "max_trace_depth": 10,
        "similarity_threshold": 0.85,
        "log_level": "INFO",
        "tui_enabled": True,
        "auto_save": True,
    }

    def __init__(self, config_path: Optional[str] = None):
        self._config = dict(self.DEFAULT_CONFIG)
        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)
        self._load_from_env()

    def _load_from_env(self):
        """从环境变量加载配置"""
        env_mappings = {
            "ATP_TIMEOUT": ("timeout", int),
            "ATP_MAX_RETRIES": ("max_retries", int),
            "ATP_CONCURRENCY": ("concurrency", int),
            "ATP_OUTPUT_DIR": ("output_dir", str),
            "ATP_STRICT_MODE": ("strict_mode", lambda x: x.lower() in ("true", "1", "yes")),
            "ATP_LOG_LEVEL": ("log_level", str),
            "ATP_TUI_ENABLED": ("tui_enabled", lambda x: x.lower() in ("true", "1", "yes")),
        }
        for env_var, (key, cast) in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                try:
                    self._config[key] = cast(value)
                except (ValueError, TypeError):
                    pass

    def load_from_file(self, path: str):
        """从JSON文件加载配置"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._config.update(data)

    def save_to_file(self, path: str):
        """保存配置到JSON文件"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """设置配置项"""
        self._config[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __setitem__(self, key: str, value: Any):
        self._config[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """导出为字典"""
        return dict(self._config)

    @classmethod
    def default(cls) -> "Config":
        """创建默认配置"""
        return cls()
