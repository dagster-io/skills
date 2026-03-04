---
description: Creating custom state-backed components that fetch and cache external state.
triggers:
  - "create state-backed component, StateBackedComponent subclass"
  - "write_state_to_path, build_defs_from_state"
  - "defs_state_config, DefsStateConfig"
---

# Creating State-Backed Components

## Overview

State-backed components are for integrations where Dagster definitions depend on external systems (APIs, compiled artifacts) rather than just code and config files. The framework manages fetching, storing, and loading this state so that expensive operations (API calls, compilation) don't run on every code server load.

Subclasses implement three abstract members:

- **`defs_state_config`** — property returning state management configuration
- **`write_state_to_path`** — fetches external state and writes it to a local path
- **`build_defs_from_state`** — builds definitions from the cached state

## Basic Structure

```python nocheckundefined
from pathlib import Path
from typing import Optional
import dagster as dg
from dagster.components.utils.defs_state import (
    DefsStateConfig,
    DefsStateConfigArgs,
    ResolvedDefsStateConfig,
)


class MyApiComponent(dg.StateBackedComponent, dg.Model, dg.Resolvable):
    """Pulls assets from an external API."""

    api_url: str
    defs_state: ResolvedDefsStateConfig = DefsStateConfigArgs.local_filesystem()

    @property
    def defs_state_config(self) -> DefsStateConfig:
        return DefsStateConfig.from_args(self.defs_state, default_key=self.__class__.__name__)

    def write_state_to_path(self, state_path: Path) -> None:
        # Fetch from external system and persist
        data = fetch_from_api(self.api_url)
        state_path.write_text(dg.serialize_value(data))

    def build_defs_from_state(
        self, context: dg.ComponentLoadContext, state_path: Optional[Path]
    ) -> dg.Definitions:
        if state_path is None:
            return dg.Definitions()
        data = dg.deserialize_value(state_path.read_text(), MyApiData)
        # Build assets from data...
        return dg.Definitions(assets=[])
```

Corresponding YAML:

```yaml
type: my_project.MyApiComponent

attributes:
  api_url: "https://api.example.com/v1"
  defs_state:
    management_type: LOCAL_FILESYSTEM
```

## The `defs_state_config` Property

### User-configurable (recommended)

Expose a `defs_state` field so users can choose the management strategy in YAML. This is the OmniComponent pattern:

```python
from dagster.components.utils.defs_state import (
    DefsStateConfig,
    DefsStateConfigArgs,
    ResolvedDefsStateConfig,
)


class MyComponent(dg.StateBackedComponent, dg.Model, dg.Resolvable):
    defs_state: ResolvedDefsStateConfig = DefsStateConfigArgs.versioned_state_storage()

    @property
    def defs_state_config(self) -> DefsStateConfig:
        return DefsStateConfig.from_args(self.defs_state, default_key=self.__class__.__name__)
```

The `default_key` is used when the user doesn't specify a `key` in YAML. Convention: `ClassName` or `ClassName[discriminator]`.

### Hardcoded

Construct `DefsStateConfig` directly when the strategy should not be user-configurable. This is the DbtProjectComponent pattern:

```python
from dagster.components.utils.defs_state import DefsStateConfig
from dagster_shared.serdes.objects.models.defs_state_info import DefsStateManagementType


class MyToolComponent(dg.StateBackedComponent, dg.Resolvable):
    project_name: str

    @property
    def defs_state_config(self) -> DefsStateConfig:
        return DefsStateConfig(
            key=f"MyToolComponent[{self.project_name}]",
            management_type=DefsStateManagementType.LOCAL_FILESYSTEM,
            refresh_if_dev=True,
        )
```

**Key format convention:** `ClassName[discriminator]` — the discriminator distinguishes multiple instances of the same component type (e.g., different dbt projects).

## State Serialization Strategies

### Dagster serdes (for API responses)

Define typed state objects with `@whitelist_for_serdes` and `@record`, then serialize with `dg.serialize_value()` / `dg.deserialize_value()`. Best when state comes from API responses. Used by OmniComponent.

```python
from dagster_shared.record import record
from dagster_shared.serdes import whitelist_for_serdes


@whitelist_for_serdes
@record
class WorkspaceItem:
    id: str
    name: str
    item_type: str


@whitelist_for_serdes
@record
class WorkspaceData:
    items: list[WorkspaceItem]
```

Write and read state:

```python nocheckundefined
class MyComponent(dg.StateBackedComponent, dg.Model, dg.Resolvable):
    client: MyApiClient

    def write_state_to_path(self, state_path: Path) -> None:
        items = self.client.list_items()
        state = WorkspaceData(items=items)
        state_path.write_text(dg.serialize_value(state))

    def build_defs_from_state(
        self, context: dg.ComponentLoadContext, state_path: Optional[Path]
    ) -> dg.Definitions:
        if state_path is None:
            return dg.Definitions()
        state = dg.deserialize_value(state_path.read_text(), WorkspaceData)
        # Build assets from state.items...
        return dg.Definitions(assets=[])
```

### Tool's native format (for tools with existing artifacts)

Write tool artifacts directly and read them with the tool's own parser. Best when the tool already produces a well-defined artifact format. Used by DbtProjectComponent (writes dbt manifest, reads it with dbt's manifest parser).

```python nocheckundefined
class MyToolComponent(dg.StateBackedComponent, dg.Resolvable):
    tool: MyTool

    def write_state_to_path(self, state_path: Path) -> None:
        # Run the tool's build/compile step, outputting to state_path
        self.tool.compile(output_dir=state_path)

    def build_defs_from_state(
        self, context: dg.ComponentLoadContext, state_path: Optional[Path]
    ) -> dg.Definitions:
        if state_path is None:
            return dg.Definitions()
        manifest = self.tool.parse_manifest(state_path)
        # Build assets from manifest...
        return dg.Definitions(assets=[])
```

## Notes

- **Async support:** `write_state_to_path` can be `async`. The framework detects this automatically. Use async when calling async APIs (e.g., `await client.fetch(...)`).
- **Handling `state_path=None`:** `build_defs_from_state` receives `state_path=None` when no state has been written yet. Return `dg.Definitions()` (empty) in this case.
- **Do not override `build_defs`:** The base class `build_defs` manages the state lifecycle (refresh timing, storage). Override `build_defs_from_state` instead.
- **MRO:** Use `dg.StateBackedComponent, dg.Model, dg.Resolvable` for pydantic-based components, or `dg.StateBackedComponent, dg.Resolvable` with `@dataclass` for dataclass-based components.
