<div align="center">
  <img width="auto" height="38px" alt="dagster-hearts-claude" src="https://github.com/user-attachments/assets/b162dddf-6a7e-459e-be06-29d34d637650" />
</div>

# Dagster Skills

AI assistant skills for building workflows and data pipelines using Dagster. It bundles the `dagster-expert` skill for authoring pipelines and the [Dagster+ MCP server](https://docs.dagster.io/getting-started/ai-tools/dagster-mcp) for access to your Dagster+ deployment.

**Compatible with Claude Code, Cursor, OpenCode, OpenAI Codex, Pi, and other Agent Skills-compatible tools.**

## Installation

### Claude Code

Install using the
[Claude plugin marketplace](https://code.claude.com/docs/en/discover-plugins#add-from-github):

```
/plugin marketplace add dagster-io/skills

/plugin install dagster-expert@dagster

/dagster-expert "What's an asset?"
```

The plugin includes the
[Dagster+ MCP server](https://docs.dagster.io/getting-started/ai-tools/dagster-mcp), giving the skill direct
access to your deployed organization: runs, assets, deployments, code locations, alert policies,
Issues, and insights metrics. Run `/mcp` to authenticate.

```
/mcp
# authenticate dagster-plus

Fetch the run logs for the most recent run failure.
```

The MCP URL points at the US region by default. If your organization is in the EU region, set the following environment variable before launching Claude Code:

```bash
export DAGSTER_CLOUD_MCP_URL=https://mcp.agent.eu.dagster.cloud/mcp
```

### Using `npx skills`

Install using the [`npx skills`](https://skills.sh/) command-line:

```bash
npx skills add dagster-io/skills
```

### Manual Installation

<details>
<summary>See full instructions...</summary>

Clone the repository and copy skills to your tool's skills directory:

**OpenCode:**

```bash
git clone https://github.com/dagster-io/skills.git
cp -r skills/skills/* ~/.config/opencode/skill/
```

**OpenAI Codex:**

```bash
git clone https://github.com/dagster-io/skills.git
cp -r skills/skills/* ~/.codex/skills/
```

**Pi Agent:**

```bash
git clone https://github.com/dagster-io/skills.git
cp -r skills/skills/* ~/.pi/agent/skills/
```

</details>

## Skills

### `dagster-expert`

Expert guidance for building production-quality Dagster projects, covering CLI commands, asset patterns, automation strategies, and implementation workflows.

**What you can do:**

- Create and scaffold projects, assets, schedules, and sensors
- Understand asset patterns (dependencies, partitions, multi-assets, metadata)
- Implement automation (declarative automation, schedules, sensors)
- Use CLI commands (launch, list, check, scaffold, logs)
- Design project structure and configure environments
- Follow implementation workflows and best practices
- Debug issues and validate project configuration

**Example prompts:**

```
Create a new Dagster project called analytics
How do I scaffold a new asset?
Show me how to set up declarative automation
What's the proper way to partition my assets?
Help me debug why my materialization failed
How should I structure my project for multiple pipelines?
Launch all assets tagged with priority=high
```

## Dagster+ MCP

Direct access to Dagster+ data about your deployment, including run logs, Insights, and select actions to remediate failures.

The MCP server uses your user permissions when determining the MCP server permissions. To use custom permissions, see the documentation for alternative authentication methods [here](https://docs.dagster.io/getting-started/ai-tools/dagster-mcp#connecting-to-the-mcp-server)

**What you can do:**

- Launch runs, materialize assets, re-run runs and backfills
- Fetch run logs
- Fetch asset definitions and metadata
- Fetch deployments and deployment information.
- Create and update alert policies and fetch their notifications
- Fetch Insights metrics for assets, jobs, and deployments

**Example prompts:**

```
Fetch the logs for run <run id>, investigate why it failed, and propose a solution.
What is the materialization success rate over the past month?
How often has the customer_returns_job failed in the past quarter?
What assets in my deployment are not covered by an alert policy?
```


## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

<div align="center">
  <img alt="dagster logo" src="https://github.com/user-attachments/assets/6fbf8876-09b7-4f4a-8778-8c0bb00c5237" width="auto" height="16px">
</div>
