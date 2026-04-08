---
title: dg api issue
type: index
triggers:
  - "listing Dagster Plus issues, fetching a specifc Dagster Plus issue"
---

# dg api issue Reference

Commands for interacting with Dagster Plus Issues.

A Dasgster Plus Issue is a record of a problem within the Users' Dagster deployment like you would find in an issue tracking tool. Issues have the following fields: ID, title, description, status, createdBy, links to related Runs and Assets, and any previous conversations about the problem.

Some organizations do not have access to Dagster Plus Issues. If you get an Unauthorized error indicating that Issues are not available, inform the user that Issues are not enabled for their organization.

## Get a specific Dagster Plus Issue

```bash
dg api issue get <ID>
```
- `<ID>` — the ID of the Issue to get

## List Issues for a deployment.

```bash
dg api issue list
```
The response will contain a list of `limit` Issues in chronologically descending order. To fetch the next page of Issues, use the ID of the oldest Issue as the cursor.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->


<!-- END GENERATED INDEX -->