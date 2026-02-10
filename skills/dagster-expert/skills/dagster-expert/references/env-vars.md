# Environment Variables Reference

## Overview

Environment variables provide a clean separation between configuration and code, allowing the same Dagster project to work across different environments (development, staging, production) without code changes.

## How `dg` Commands Handle Environment Variables

The `dg` CLI automatically loads environment variables from `.env` files in your project root before executing commands. This means:

- No manual `export` or `source` commands needed
- Commands like `dg launch`, `dg dev`, `dg check defs` automatically use `.env` values
- Works consistently across local development and CI/CD environments

## Listing Available Environment Variables

Use the `dg list envs` command to see what environment variables your Dagster definitions reference:

```bash
dg list envs
```

This shows all `EnvVar` references in your code, helping you identify what needs to be configured.

## Basic .env File Pattern

```bash
# .env (at project root, never commit to git)
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=secret_key_here
SNOWFLAKE_ACCOUNT=myaccount
SNOWFLAKE_USER=myuser
SNOWFLAKE_PASSWORD=secret
```

**Important:** Add `.env` to your `.gitignore` to prevent committing secrets.

## Using Environment Variables in Dagster

### In Resources

```python
import dagster as dg

class DatabaseResource(dg.ConfigurableResource):
    connection_string: str = dg.EnvVar("DATABASE_URL")
    timeout: int = dg.EnvVar.int("DB_TIMEOUT")

# Dagster automatically loads DATABASE_URL and DB_TIMEOUT from .env
```

### In Component YAML Files

```yaml
# defs/my_component/defs.yaml
component: dagster_sling.SlingReplicationComponent

params:
  sling:
    connections:
      - name: MY_POSTGRES
        type: postgres
        host: "{{ env.DB_HOST }}"
        port: "{{ env.DB_PORT }}"
        database: "{{ env.DB_NAME }}"
```

## Environment-Specific Configuration

For multiple environments, use separate `.env` files:

```
my_project/
├── .env              # Local development (gitignored)
├── .env.example      # Template (committed to git)
├── .env.staging      # Staging config (gitignored)
└── .env.prod         # Production config (gitignored)
```

### .env.example Template

```bash
# .env.example (committed to git)
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=your_api_key_here
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
```

Developers copy `.env.example` to `.env` and fill in real values.

### Loading Environment-Specific Files

```bash
# Development (uses .env by default)
dg dev

# Staging
dg launch --env-file .env.staging --assets my_asset

# Production
dg launch --env-file .env.prod --assets my_asset
```

## Best Practices

1. **Never commit `.env` files** - Always add to `.gitignore`
2. **Provide `.env.example`** - Template for required variables
3. **Use descriptive names** - `SNOWFLAKE_ACCOUNT` not `ACCT`
4. **Group related vars** - Prefix related vars (e.g., `SNOWFLAKE_*`, `S3_*`)
5. **Document required vars** - List required environment variables in README
6. **Use `dg list envs`** - Verify all environment variables are configured

## References

- [CLI list reference](./cli/list.md) - `dg list envs` and other commands
- [Dagster EnvVar API](https://docs.dagster.io/api/dagster/dagster.EnvVar)
