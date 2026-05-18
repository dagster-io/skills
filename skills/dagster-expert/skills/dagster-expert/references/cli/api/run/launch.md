---
title: dg api run launch
triggers:
  - "materializing assets or launching jobs on a Dagster Plus deployment"
  - "remote asset materialization, remote job launch"
---

`dg api run launch` launches a run on a remote Dagster Plus deployment. Use this for materializing assets or launching jobs against your deployed environment. For local in-process execution during development, use [`dg launch`](../../launch.md) instead.

```bash
dg api run launch --location <LOCATION> --job <JOB_NAME>
dg api run launch --location <LOCATION> --asset-key <KEY> [--asset-key <KEY> ...]
```

- `--location` / `-l` (required) — code location name
- `--repository` / `-r` — repository name (default: `__repository__`)
- `--job` / `-j` — name of the job to launch
- `--asset-key` — asset key to materialize. Repeatable. Use slash-separated syntax for prefixed keys (e.g. `my_prefix/my_asset`). The asset selection DSL (`group:`, `tag:`, `+upstream`) is not supported here — list explicit keys only. For DSL evaluation, use `dg launch` against a local project, or discover keys first with `dg api asset list`.
- `--partition` — single partition key. Partition ranges/backfills are not yet supported.
- `--tag` — tag to attach to the run as `key=value`. Repeatable.
- `--config-json` — JSON string of run config to use for the run
- `--wait` / `-w` — block until the run reaches a terminal status. Exits non-zero on `FAILURE` or `CANCELED`.
- `--interval` / `-i` — poll interval in seconds when `--wait` is set (default: 30)

At least one of `--job` or `--asset-key` must be provided.
