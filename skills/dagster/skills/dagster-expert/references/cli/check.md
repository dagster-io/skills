---
title: dg check
triggers:
  - "validating project configuration or definitions"
---

## dg check defs

Verify all definitions load without errors.

```bash
dg check defs
dg check defs --verbose    # Detailed output
```

## dg check yaml

Validate `defs.yaml` files for syntax errors and valid component configuration.

```bash
dg check yaml
```

## dg check toml

Validate `pyproject.toml` and `dg.toml` for syntax errors.

```bash
dg check toml
```
