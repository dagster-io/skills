# dg api / dg plus

API access and Dagster Plus authentication.

## dg api

Query and interact with Dagster deployments.

### dg api log get

Retrieve run logs.

```bash
dg api log get <run-id>
dg api log get <run-id> --json
dg api log get <run-id> --level ERROR
dg api log get <run-id> --limit 100
```

**Options:**

| Option            | Description                                   |
| ----------------- | --------------------------------------------- |
| `--json`          | Output as JSON                                |
| `--level <level>` | Filter: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `--limit <n>`     | Maximum entries to return                     |

---

## dg plus login

Authenticate with Dagster Plus.

```bash
dg plus login
```

After login, `dg list envs` shows deployment scope status (Dev/Branch/Full).

---

## See Also

- [launch.md](./launch.md) - Launch assets (returns run ID for log retrieval)
- [list.md](./list.md) - `dg list envs` shows Plus deployment status after login
