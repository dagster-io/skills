---
description: "dg plus login: authenticate with Dagster Plus."
triggers:
  - "login, authenticate, dagster plus auth"
---

# dg plus login - Dagster Plus Authentication

Authenticate with Dagster Plus. Opens a browser for interactive login.

```bash
dg plus login
```

---

## Options

| Option              | Description                                            |
| ------------------- | ------------------------------------------------------ |
| `--region <region>` | Cloud region: `us` (default) or `eu` (European region) |

---

## Examples

```bash
# Login to US region (default)
dg plus login

# Login to EU region
dg plus login --region eu
```

After login, `dg list envs` shows deployment scope status (Dev/Branch/Full) and `dg api` commands can access your deployments.

---

## See Also

- [../api/log.md](../api/log.md) - Retrieve run logs (requires authentication)
- [../list/envs.md](../list/envs.md) - `dg list envs` shows Plus deployment status after login
