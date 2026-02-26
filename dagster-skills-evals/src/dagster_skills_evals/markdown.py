import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from dagster_skills_evals.models import ReferenceFrontmatter

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> ReferenceFrontmatter | None:
    """Parse and validate YAML front matter from a markdown file.

    Returns a validated ReferenceFrontmatter model, or None if no front matter is found.
    Raises ValidationError if front matter is present but invalid.
    """
    text = path.read_text()
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1))
    if data is None:
        return None
    return ReferenceFrontmatter.model_validate(data)


def parse_frontmatter_raw(path: Path) -> dict | None:
    """Parse YAML front matter without strict validation.

    Useful for INDEX.md files that may have extra fields like ``type``.
    """
    text = path.read_text()
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


@dataclass(frozen=True)
class ResolvedLink:
    """A local markdown link resolved to an absolute path."""

    source_file: Path
    line_number: int
    raw_target: str
    resolved_path: Path


def extract_local_links(md_path: Path) -> list[ResolvedLink]:
    """Extract local file links from a markdown file, resolving them to absolute paths."""
    content = md_path.read_text()
    results: list[ResolvedLink] = []
    for line_no, line in enumerate(content.splitlines(), 1):
        for _, raw_target in _LINK_RE.findall(line):
            if raw_target.startswith(("http://", "https://", "#")):
                continue
            target = raw_target.split("#")[0]
            if not target:
                continue
            resolved = (md_path.parent / target).resolve()
            if resolved.is_dir() or target.endswith("/"):
                resolved = resolved / "README.md"
            results.append(
                ResolvedLink(
                    source_file=md_path,
                    line_number=line_no,
                    raw_target=raw_target,
                    resolved_path=resolved,
                )
            )
    return results
