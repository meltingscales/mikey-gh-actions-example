.PHONY: help install install-dev run run-with-secret test lint format clean setup

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup - install uv and create virtual environment
	@echo "Setting up project with uv..."
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "uv is already installed"; \
	fi
	uv sync

install: ## Install production dependencies
	uv sync --no-dev

install-dev: ## Install all dependencies (including dev dependencies)
	uv sync

run: ## Run the daily request script locally (requires MIKEY_SECRET env var)
	@if [ -z "$(MIKEY_SECRET)" ]; then \
		echo "Error: MIKEY_SECRET environment variable not set"; \
		echo "Set it with: export MIKEY_SECRET=your_secret_here"; \
		echo "Or run with: MIKEY_SECRET=your_secret make run"; \
		exit 1; \
	fi
	@if uv --version >/dev/null 2>&1; then \
		uv run python scripts/daily_request.py; \
	else \
		echo "uv not available, using nix-shell..."; \
		nix-shell -p python312 python312Packages.requests --run "MIKEY_SECRET=$(MIKEY_SECRET) python scripts/daily_request.py"; \
	fi

test: ## Run tests
	uv run pytest

lint: ## Run linting checks
	uv run flake8 scripts/ tests/
	uv run black --check scripts/ tests/

format: ## Format code with black
	uv run black scripts/ tests/

clean: ## Clean up generated files
	rm -rf response.txt
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

test-local: ## Test the script locally with a mock response
	@echo "Testing script with mock MIKEY_SECRET..."
	@if uv --version >/dev/null 2>&1; then \
		MIKEY_SECRET=test_secret uv run python scripts/daily_request.py; \
	else \
		echo "uv not available, using nix-shell..."; \
		nix-shell -p python312 python312Packages.requests --run "MIKEY_SECRET=test_secret python scripts/daily_request.py"; \
	fi

run-with-secret: ## Run the script with a secret (usage: make run-with-secret SECRET=your_secret)
	@if [ -z "$(SECRET)" ]; then \
		echo "Error: SECRET parameter not provided"; \
		echo "Usage: make run-with-secret SECRET=your_secret_here"; \
		exit 1; \
	fi
	@if uv --version >/dev/null 2>&1; then \
		MIKEY_SECRET=$(SECRET) uv run python scripts/daily_request.py; \
	else \
		echo "uv not available, using nix-shell..."; \
		nix-shell -p python312 python312Packages.requests --run "MIKEY_SECRET=$(SECRET) python scripts/daily_request.py"; \
	fi

check: ## Run all checks (lint, format, test)
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) test

# Development workflow
dev-setup: setup install-dev ## Complete development setup
	@echo "Development environment ready!"

# GitHub Actions specific
validate-workflow: ## Validate the GitHub Actions workflow syntax
	@echo "Validating workflow syntax..."
	@if command -v act >/dev/null 2>&1; then \
		echo "Using act to validate workflow..."; \
		act --list; \
	else \
		echo "act not installed. Install with: brew install act"; \
		echo "Or validate manually in GitHub Actions tab"; \
	fi 