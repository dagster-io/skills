---
description: "dg api: general tips and patterns for interacting with `dg api` subcommands."
triggers:
  - "always read before using any `dg api` subcommand"
  - "dg api response schema, parsing dg api output, dg api workflow"
---

# dg api - General Tips and Patterns

All `dg api` subcommands have the following options / flags:

## --json

Output in JSON format.

## --response-schema

Print the JSON schema for the response of this command and exit.

## -d, --deployment

Target a specific deployment.

## -o, --organization

Target a specific organization.

## --api-token

Dagster Cloud API token (alternative to `dg plus login`).

## --view-graphql

Print GraphQL queries and responses to stderr for debugging.

## Tips

For complex debugging / analysis workflows, before running any `dg api` command for the first time in a session, run it with the `--response-schema` flag to print the JSON schema of the response. This ensures you know the exact field names, types, and valid enum values before writing any parsing logic. No other flags or options need to be supplied. Skipping this step may lead to incorrect field references and failed queries.

For complex debugging / analysis workflows, ALWAYS use the `--json` flag to output the response in a machine-readable format. This will allow you to pipe the response into other commands (e.g. `jq` [RECOMMENDED], `python`, etc.) to further process the data.

These commands only work with Dagster Plus, and typically `--deployment`/`--organization`/`--api-token` flags are not needed as they are set by default when using `dg plus login`.
