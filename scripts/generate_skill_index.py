#!/usr/bin/env python3
"""Auto-generate SKILL.md routing index from YAML front matter in reference files.

Usage:
    python scripts/generate_skill_index.py <skill-root>
    python scripts/generate_skill_index.py <skill-root> --validate-only
    python scripts/generate_skill_index.py <skill-root> --check
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

BEGIN_MARKER = "<!-- BEGIN GENERATED INDEX -->"
END_MARKER = "<!-- END GENERATED INDEX -->"


def parse_front_matter(path: Path) -> dict | None:
    """Parse YAML front matter from a markdown file."""
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def format_entry(link: str, link_text: str, fm: dict) -> str:
    """Format a single reference entry as a bullet point."""
    desc = fm.get("description", "")
    triggers = fm.get("triggers", [])
    trigger_str = "; ".join(triggers) if triggers else ""
    line = f"- [{link_text}]({link}) — {desc}"
    if trigger_str:
        line += f" *({trigger_str})*"
    return line


def inject_generated_content(file_path: Path, content: str) -> str:
    """Replace content between BEGIN/END markers in a file."""
    text = file_path.read_text()
    begin_idx = text.find(BEGIN_MARKER)
    end_idx = text.find(END_MARKER)
    if begin_idx == -1 or end_idx == -1:
        print(f"ERROR: Markers not found in {file_path}", file=sys.stderr)
        sys.exit(1)
    return (
        text[: begin_idx + len(BEGIN_MARKER)] + "\n" + content + "\n" + text[end_idx:]
    )


def validate_front_matter(refs_dir: Path) -> list[str]:
    """Validate that all .md files have valid front matter."""
    errors: list[str] = []
    for md_file in sorted(refs_dir.rglob("*.md")):
        rel = md_file.relative_to(refs_dir)
        fm = parse_front_matter(md_file)
        if fm is None:
            errors.append(f"{rel}: missing YAML front matter")
            continue
        if "description" not in fm:
            errors.append(f"{rel}: missing 'description' in front matter")
        if "triggers" not in fm:
            errors.append(f"{rel}: missing 'triggers' in front matter")
        elif not isinstance(fm["triggers"], list) or len(fm["triggers"]) == 0:
            errors.append(f"{rel}: 'triggers' must be a non-empty list")
    return errors


def emit_file(path: Path, rel: Path, target: list[str], link_prefix: str) -> None:
    """Emit a bullet entry for a single .md file."""
    fm = parse_front_matter(path)
    if fm is None:
        return
    link_text = str(rel).removesuffix(".md").removesuffix("/INDEX")
    target.append(format_entry(f"./{link_prefix}{rel}", link_text, fm))


def collect_and_generate(refs_dir: Path) -> tuple[str, dict[Path, str]]:
    """Walk references/ and generate index content for SKILL.md and deferred INDEXs."""
    skill_lines: list[str] = []
    deferred_updates: dict[Path, str] = {}

    def walk(
        directory: Path, rel_prefix: Path, target: list[str], link_prefix: str
    ) -> None:
        """Recursively walk a directory, emitting entries to target.

        Directories with a type:index INDEX become deferred fan-outs:
        one entry is emitted to the parent target, and the INDEX gets
        its own generated child index.
        """
        # Separate files and dirs for sorted processing
        files: list[Path] = []
        dirs: list[Path] = []
        for item in sorted(directory.iterdir()):
            if item.name == "INDEX.md":
                continue
            if item.is_file() and item.suffix == ".md":
                files.append(item)
            elif item.is_dir():
                dirs.append(item)

        for f in files:
            emit_file(f, rel_prefix / f.name, target, link_prefix)

        for d in dirs:
            readme = d / "INDEX.md"
            child_rel = rel_prefix / d.name

            if not readme.exists():
                # No INDEX — recurse directly
                walk(d, child_rel, target, link_prefix)
                continue

            fm = parse_front_matter(readme)
            if fm is None:
                walk(d, child_rel, target, link_prefix)
                continue

            if fm.get("type") == "index":
                # Deferred index: one entry in parent, generate child index
                emit_file(readme, child_rel / "INDEX.md", target, link_prefix)
                child_lines: list[str] = []
                walk(d, Path(), child_lines, link_prefix="")
                deferred_updates[readme] = "\n".join(child_lines)
            else:
                # Non-index INDEX: emit as leaf, plus any siblings
                emit_file(readme, child_rel / "INDEX.md", target, link_prefix)
                for sibling in sorted(d.iterdir()):
                    if sibling.name == "INDEX.md" or not sibling.suffix == ".md":
                        continue
                    emit_file(sibling, child_rel / sibling.name, target, link_prefix)

    walk(refs_dir, Path(), skill_lines, link_prefix="references/")
    return "\n".join(skill_lines), deferred_updates


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate SKILL.md routing index from YAML front matter"
    )
    parser.add_argument("skill_root", help="Path to the skill root directory")
    parser.add_argument(
        "--validate-only", action="store_true", help="Only validate front matter"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check generated output matches disk"
    )
    args = parser.parse_args()

    skill_root = Path(args.skill_root)
    refs_dir = skill_root / "references"
    skill_md = skill_root / "SKILL.md"

    if not refs_dir.is_dir():
        print(f"ERROR: references directory not found at {refs_dir}", file=sys.stderr)
        sys.exit(1)

    errors = validate_front_matter(refs_dir)
    if errors:
        print("Front matter validation errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if args.validate_only:
        print("All front matter is valid.")
        return

    skill_content, deferred = collect_and_generate(refs_dir)
    new_skill_md = inject_generated_content(skill_md, skill_content)

    deferred_texts: dict[Path, str] = {}
    for readme_path, child_content in deferred.items():
        deferred_texts[readme_path] = inject_generated_content(
            readme_path, child_content
        )

    if args.check:
        has_drift = False
        if skill_md.read_text() != new_skill_md:
            print(f"DRIFT: {skill_md} is out of date", file=sys.stderr)
            has_drift = True
        for readme_path, new_text in deferred_texts.items():
            if readme_path.read_text() != new_text:
                print(f"DRIFT: {readme_path} is out of date", file=sys.stderr)
                has_drift = True
        if has_drift:
            print(
                "Run 'python scripts/generate_skill_index.py <skill-root>' to update.",
                file=sys.stderr,
            )
            sys.exit(1)
        print("All generated indices are up to date.")
        return

    skill_md.write_text(new_skill_md)
    print(f"Updated {skill_md}")
    for readme_path, new_text in deferred_texts.items():
        readme_path.write_text(new_text)
        print(f"Updated {readme_path}")


if __name__ == "__main__":
    main()
