#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentTestPilot - Setup Configuration
轻量级AI Agent自动化测试与行为验证引擎
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="agenttestpilot",
    version="1.0.0",
    description="🧪 Lightweight AI Agent Automated Testing & Behavior Validation Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="gitstq",
    author_email="",
    url="https://github.com/gitstq/AgentTestPilot",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "agenttestpilot": ["templates/*.html", "templates/*.md"],
    },
    entry_points={
        "console_scripts": [
            "agenttestpilot=agenttestpilot.cli:main",
            "atp=agenttestpilot.cli:main",
        ],
    },
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="ai agent testing validation automation llm mcp claude cursor",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/AgentTestPilot/issues",
        "Source": "https://github.com/gitstq/AgentTestPilot",
        "Documentation": "https://github.com/gitstq/AgentTestPilot#readme",
    },
)
