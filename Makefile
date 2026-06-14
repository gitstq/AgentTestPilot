.PHONY: help install install-dev test test-cov lint format clean build upload demo

PYTHON := python3
PIP := pip3

help:
	@echo "AgentTestPilot - Available Commands:"
	@echo "  make install      Install package"
	@echo "  make install-dev  Install with dev dependencies"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage"
	@echo "  make lint         Run linting"
	@echo "  make format       Format code"
	@echo "  make clean        Clean build artifacts"
	@echo "  make build        Build package"
	@echo "  make demo         Run demo"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/ -v

test-cov:
	$(PYTHON) -m pytest tests/ -v --cov=agenttestpilot --cov-report=term-missing --cov-report=html

lint:
	$(PYTHON) -m flake8 agenttestpilot/ tests/

format:
	$(PYTHON) -m black agenttestpilot/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf reports/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

demo:
	$(PYTHON) -m agenttestpilot.cli demo
