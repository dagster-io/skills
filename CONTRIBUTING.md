# Contributing to Dagster Skills

Thank you for your interest in contributing to Dagster Skills! This document provides guidelines and
instructions for contributing to this monorepo.

## Development Setup

This repository contains AI assistant skills for Dagster development. Each plugin is located in
the `plugins/` directory:

- `dagster` - Comprehensive Dagster development guidance (includes integrations)
- `dagster-expert` - Deprecated stub that points users at the `dagster` plugin

These skills work with Claude Code, OpenCode, OpenAI Codex, Pi, and other Agent Skills-compatible
tools.

### Local Development

1. Clone the repository:

   ```bash
   git clone https://github.com/dagster-io/skills.git
   cd skills
   ```

2. Make your changes to the relevant skill(s)

3. Test your changes locally. The `dagster` marketplace entry points at the `release-stable`
   branch on GitHub, so adding this checkout as a marketplace does not load your edits; use
   `claude --plugin-dir plugins/dagster` instead.

### Testing Skills

The `dagster-skills-evals` module provides an evaluation framework for testing that skills are called as expected. Requires a logged-in Claude account.

**Running tests:**

```bash
make test  # Run all tests in a tox environment
```

**Developing new tests:**

```bash
cd dagster-skills-evals
uv sync --all-extras
source .venv/bin/activate
# Develop your tests here
```

## Making Changes

### Adding Features or Fixes

1. **Create a branch** for your changes:

   ```bash
   git checkout -b your-feature-name
   ```

2. **Make your changes** to the relevant skill(s)

3. **Update CHANGELOG.md** - Add your changes under the `[Unreleased]` section:

   ```markdown
   ## [Unreleased]

   ### Added

   - **skill-name**: Description of new feature

   ### Fixed

   - **skill-name**: Description of bug fix

   ### Changed

   - **skill-name**: Description of modification
   ```

   Use the appropriate category:
   - **Added** - New features, new skill capabilities
   - **Changed** - Changes to existing functionality
   - **Deprecated** - Features that will be removed in future versions
   - **Removed** - Removed features
   - **Fixed** - Bug fixes
   - **Security** - Security improvements or fixes

4. **Commit your changes**:

   ```bash
   git add -A
   git commit -m "Description of your changes"
   ```

5. **Push and create a pull request**:
   ```bash
   git push origin your-feature-name
   ```

## Releases

Skills are released weekly as part of the Dagster OSS release. There is no release workflow in
this repository; the release job in the internal monorepo does the following:

1. Sets `version` in every `plugins/*/{.claude-plugin,.cursor-plugin,.codex-plugin}/plugin.json`
   to the Dagster version being released and commits it on the release branch.
2. Syncs the release branch here as `release-<version>`, tags it `v<version>`, and moves
   `release-stable` to that commit.
3. Publishes a GitHub release for the tag.

What that means for contributors:

- Plugin versions track Dagster versions (for example `1.13.21`). Don't edit `version` fields by
  hand; the release job overwrites them.
- `master` is not bumped, so the `version` fields on `master` lag the latest release. Install from
  `release-stable` or a `v*` tag to get a released version.
- Keep adding entries under `[Unreleased]` in CHANGELOG.md. The release job doesn't rotate it, so
  a maintainer moves entries under a version heading when there is something worth calling out.

## Code Quality

This repository uses automated linting and formatting tools to maintain code quality and
consistency. All pull requests must pass linting checks in CI.

### Quick Start with Make

The repository includes a Makefile for common development tasks:

```bash
make help      # Show available commands
make install   # Install pre-commit hooks
make lint      # Run all linting checks
make format    # Auto-fix formatting issues
make clean     # Clean up cache and temporary files
```

### Setup Pre-commit Hooks

Install and enable pre-commit hooks to automatically check your changes before committing:

```bash
# Using Make (recommended)
make install
```

Or manually:

```bash
# Install pre-commit (requires Python 3.11+)
pip install pre-commit

# Install git hooks
pre-commit install
```

Now pre-commit will run automatically on `git commit`. The hooks will:

- Check and format markdown files
- Lint and format Python code
- Validate JSON and YAML syntax
- Remove trailing whitespace and fix line endings

### Running Linters Manually

To run all linters on all files:

```bash
make lint
```

Or directly with pre-commit:

```bash
pre-commit run --all-files
```

To run linters on specific files:

```bash
pre-commit run --files path/to/file.md path/to/script.py
```

### Auto-fixing Issues

Most linting issues can be automatically fixed:

**Auto-fix all files:**

```bash
make format
```

**Or manually:**

Markdown formatting:

```bash
npx prettier --write "**/*.md"
```

Python formatting:

```bash
ruff format scripts/
ruff check --fix scripts/
```

### Linting Tools Used

- **markdownlint-cli2**: Semantic/structural markdown rules
- **Prettier**: Automated markdown formatting
- **Ruff**: Python linting and formatting (replaces Black, isort, Flake8)
- **pre-commit-hooks**: JSON/YAML validation, trailing whitespace, etc.

### CI Requirements

All pull requests must pass the linting workflow in GitHub Actions. The workflow runs:

```bash
pre-commit run --all-files
```

If the linting check fails:

1. Run `pre-commit run --all-files` locally to see the errors
2. Fix the issues (many can be auto-fixed)
3. Commit the fixes and push again

You can view the linting workflow status in the "Checks" tab of your pull request.

## Code Standards

### Python Code

For Python code in skills, follow these standards:

- Use type annotations with modern syntax (`list[str]`, `str | None`)
- Follow LBYL (Look Before You Leap) exception handling
- Use pathlib for file operations
- Use ABC-based interfaces for abstractions

All Python code is automatically checked with Ruff (linting + formatting).

### Documentation

- Keep documentation clear and concise
- Include examples where helpful
- Update CHANGELOG.md with all changes
- All markdown is automatically formatted with Prettier and checked with markdownlint

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Reference issue numbers if applicable

## Questions?

If you have questions or need help:

- Open an issue on GitHub
- Check existing issues and discussions

Thank you for contributing to Dagster Skills!
