<div align="center">
  <img width="auto" height="38px" alt="dagster-hearts-claude" src="https://github.com/user-attachments/assets/b162dddf-6a7e-459e-be06-29d34d637650" />
</div>

# Dagster Skills

AI assistant skills for building workflows and data pipelines using Dagster.

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

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

<div align="center">
  <img alt="dagster logo" src="https://github.com/user-attachments/assets/6fbf8876-09b7-4f4a-8778-8c0bb00c5237" width="auto" height="16px">
</div>
