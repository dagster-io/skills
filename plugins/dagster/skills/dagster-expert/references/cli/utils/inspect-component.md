---
title: dg utils inspect-component
triggers:
  - "inspecting a component type's description, schema, or examples"
---

# dg utils inspect-component

Get detailed information about a registered component type, including its description, scaffold parameters, and configuration schema.

## Usage

```bash
dg utils inspect-component <COMPONENT_TYPE>
```

## Flags

All flags are mutually exclusive — only one can be used at a time.

- **`--description`** — Print the component's description text only.
- **`--scaffold-params-schema`** — Print the JSON schema for scaffold parameters (i.e. what flags/params `dg scaffold defs` accepts for this component type).
- **`--defs-yaml-json-schema`** — Print the full JSON schema for the component's `defs.yaml` file. This covers `type`, `attributes`, `template_vars_module`, `requirements`, and `post_processing`.
- **`--defs-yaml-schema`** — Print an LLM-optimized YAML template with inline documentation and type hints. Useful for understanding the structure at a glance.
- **`--defs-yaml-example-values`** — Print a YAML template populated with example values, useful for code generation.

With no flags, all available metadata is printed (description + scaffold params schema + component schema).
