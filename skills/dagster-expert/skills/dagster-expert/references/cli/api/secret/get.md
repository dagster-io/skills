---
description: "dg api secret get: retrieve details for a specific secret from Dagster Plus."
triggers:
  - "secret details, get secret, secret info"
  - "secret value, secret configuration"
---

# dg api secret get

```bash
dg api secret get <SECRET_NAME>
```

## General

Retrieve details for a specific secret by name from Dagster Plus.

<!-- TODO: Add tips for secret workflows -->

For shared flags (`--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, `--view-graphql`), see [general.md](../general.md).

## --location

Filter by code location.

## --show-value

Include the secret value in the response.
