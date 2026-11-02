.PHONY: help install dev test lint format clean docker-build docker-run scan apply

help:
	@echo "DepShield - Zero-critical-vulnerabilities pipeline"
	@echo ""
	@echo "Available targets:"
	@echo "  make install        - Install dependencies"
	@echo "  make dev            - Install dev dependencies"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linters"
	@echo "  make format         - Format code"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run DepShield in Docker"
	@echo "  make scan           - Run scan in dry-run mode"
	@echo "  make apply          - Run remediation (apply mode)"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=harness

lint:
	ruff check harness/ tests/
	mypy harness/

format:
	black harness/ tests/
	ruff check --fix harness/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .coverage

docker-build:
	docker build -t depshield:latest -f docker/Dockerfile .

docker-run:
	docker-compose -f docker/docker-compose.yml up

scan:
	depshield --repos ./ --output ./depshield-output --dry-run --verbose

apply:
	depshield --repos ./ --output ./depshield-output --no-dry-run --apply --verbose
