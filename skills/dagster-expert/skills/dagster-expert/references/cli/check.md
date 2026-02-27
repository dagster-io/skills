---
description: "dg check command: validate project configuration and definitions."
triggers:
  - "validate yaml, validate definitions, check, verify"
  - "validate project config"
  - "dg check"
---

# dg check - Project Validation

Validate project configuration and definitions.

---

## dg check defs

Verify all definitions load without errors.

```bash
dg check defs
dg check defs --verbose    # Detailed output
```

**Use after:**

- Scaffolding new definitions
- Modifying existing definitions
- Installing new dependencies
- Before deploying

---

## dg check yaml

Validate YAML files in the project.

```bash
dg check yaml
```

Checks `defs.yaml` files for syntax errors and valid component configuration.

---

## dg check toml

Validate TOML configuration files.

```bash
dg check toml
```

Checks `pyproject.toml` and `dg.toml` for syntax errors.

---

## Validation Workflow

```bash
# After making changes
dg check yaml           # Config syntax
dg check defs           # Definitions load
dg list defs            # Verify expected definitions appear
```
