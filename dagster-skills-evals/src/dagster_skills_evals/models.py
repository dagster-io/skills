from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


class ReferenceFrontmatter(BaseModel):
    """Validates YAML front matter in reference markdown files."""

    model_config = ConfigDict(extra="forbid")

    description: str
    triggers: list[str]
    type: Literal["index"] | None = None

    @field_validator("triggers")
    @classmethod
    def triggers_non_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("'triggers' must be a non-empty list")
        return v
