.PHONY: help install lint format test clean generate-index

help:  ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	@pip install pre-commit
	@pre-commit install
	@echo "Pre-commit hooks installed successfully!"

lint:  ## Run all linting checks
	@echo "Running linting checks..."
	@cd "$(CURDIR)" && npx markdownlint-cli2 --config .markdownlint-cli2.yaml $$(git ls-files -- '*.md')
	@cd "$(CURDIR)" && npx prettier --check $$(git ls-files -- '*.md')
	@cd "$(CURDIR)" && ruff check --config dagster-skills-evals/pyproject.toml $$(git ls-files -- '*.py')
	@cd "$(CURDIR)" && ruff format --config dagster-skills-evals/pyproject.toml --check $$(git ls-files -- '*.py')

format:  ## Auto-fix formatting issues
	@echo "Formatting markdown files..."
	@npx prettier --write "**/*.md"
	@echo "Formatting Python files..."
	@ruff format dagster-skills-evals/
	@ruff check --fix dagster-skills-evals/
	@echo "Formatting complete!"

test:  ## Run all tests using tox
	@echo "Running tests..."
	@cd dagster-skills-evals && tox

generate-index:  ## Auto-generate SKILL.md index from front matter
	cd dagster-skills-evals && uv run dagster-skills generate-index ../skills/dagster-expert/skills/dagster-expert

clean:  ## Clean up cache and temporary files
	@echo "Cleaning up..."
	@rm -rf .ruff_cache
	@rm -rf node_modules
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"
