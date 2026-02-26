from pathlib import Path

import typer
from pydantic import ValidationError

from dagster_skills_evals.console import console
from dagster_skills_evals.markdown import parse_frontmatter, parse_frontmatter_raw

app = typer.Typer()

_BEGIN_MARKER = "<!-- BEGIN GENERATED INDEX -->"
_END_MARKER = "<!-- END GENERATED INDEX -->"


def _format_entry(link: str, link_text: str, fm: dict) -> str:
    """Format a single reference entry as a bullet point."""
    desc = fm.get("description", "")
    triggers = fm.get("triggers", [])
    trigger_str = "; ".join(triggers) if triggers else ""
    line = f"- [{link_text}]({link}) — {desc}"
    if trigger_str:
        line += f" ({trigger_str})"
    return line


def _inject_generated_content(file_path: Path, content: str) -> str:
    """Replace content between BEGIN/END markers in a file."""
    text = file_path.read_text()
    begin_idx = text.find(_BEGIN_MARKER)
    end_idx = text.find(_END_MARKER)
    if begin_idx == -1 or end_idx == -1:
        console.print(f"[red]ERROR:[/red] Markers not found in {file_path}")
        raise typer.Exit(code=1)
    return text[: begin_idx + len(_BEGIN_MARKER)] + "\n\n" + content + "\n" + text[end_idx:]


def _validate_frontmatter(refs_dir: Path) -> list[str]:
    """Validate that all .md files have valid front matter."""
    errors: list[str] = []
    for md_file in sorted(refs_dir.rglob("*.md")):
        rel = md_file.relative_to(refs_dir)
        try:
            fm = parse_frontmatter(md_file)
        except ValidationError as exc:
            for err in exc.errors():
                loc = ".".join(str(part) for part in err["loc"])
                errors.append(f"{rel}: {loc} — {err['msg']}")
            continue
        if fm is None:
            errors.append(f"{rel}: missing YAML front matter")
    return errors


def _emit_file(path: Path, rel: Path, target: list[str], link_prefix: str) -> None:
    """Emit a bullet entry for a single .md file."""
    fm = parse_frontmatter_raw(path)
    if fm is None:
        return
    link_text = str(rel).removesuffix(".md").removesuffix("/INDEX")
    target.append(_format_entry(f"./{link_prefix}{rel}", link_text, fm))


def _collect_and_generate(refs_dir: Path) -> tuple[str, dict[Path, str]]:
    """Walk references/ and generate index content for SKILL.md and deferred INDEXs."""
    skill_lines: list[str] = []
    deferred_updates: dict[Path, str] = {}

    def walk(directory: Path, rel_prefix: Path, target: list[str], link_prefix: str) -> None:
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
            _emit_file(f, rel_prefix / f.name, target, link_prefix)

        for d in dirs:
            readme = d / "INDEX.md"
            child_rel = rel_prefix / d.name

            if not readme.exists():
                walk(d, child_rel, target, link_prefix)
                continue

            fm = parse_frontmatter_raw(readme)
            if fm is None:
                walk(d, child_rel, target, link_prefix)
                continue

            if fm.get("type") == "index":
                _emit_file(readme, child_rel / "INDEX.md", target, link_prefix)
                child_lines: list[str] = []
                walk(d, Path(), child_lines, link_prefix="")
                deferred_updates[readme] = "\n".join(child_lines)
            else:
                _emit_file(readme, child_rel / "INDEX.md", target, link_prefix)
                for sibling in sorted(d.iterdir()):
                    if sibling.name == "INDEX.md" or sibling.suffix != ".md":
                        continue
                    _emit_file(sibling, child_rel / sibling.name, target, link_prefix)

    walk(refs_dir, Path(), skill_lines, link_prefix="references/")
    return "\n".join(skill_lines), deferred_updates


@app.command("generate-index")
def generate_index(
    skill_root: Path = typer.Argument(..., help="Path to the skill root directory"),
    validate_only: bool = typer.Option(False, "--validate-only", help="Only validate front matter"),
    check: bool = typer.Option(False, "--check", help="Check generated output matches disk"),
) -> None:
    """Auto-generate SKILL.md routing index from YAML front matter."""
    refs_dir = skill_root / "references"
    skill_md = skill_root / "SKILL.md"

    if not refs_dir.is_dir():
        console.print(f"[red]ERROR:[/red] references directory not found at {refs_dir}")
        raise typer.Exit(code=1)

    errors = _validate_frontmatter(refs_dir)
    if errors:
        console.print("[red]Front matter validation errors:[/red]")
        for err in errors:
            console.print(f"  - {err}")
        raise typer.Exit(code=1)

    if validate_only:
        console.print("[green]All front matter is valid.[/green]")
        return

    skill_content, deferred = _collect_and_generate(refs_dir)
    new_skill_md = _inject_generated_content(skill_md, skill_content)

    deferred_texts: dict[Path, str] = {}
    for readme_path, child_content in deferred.items():
        deferred_texts[readme_path] = _inject_generated_content(readme_path, child_content)

    if check:
        has_drift = False
        if skill_md.read_text() != new_skill_md:
            console.print(f"[red]DRIFT:[/red] {skill_md} is out of date")
            has_drift = True
        for readme_path, new_text in deferred_texts.items():
            if readme_path.read_text() != new_text:
                console.print(f"[red]DRIFT:[/red] {readme_path} is out of date")
                has_drift = True
        if has_drift:
            console.print(
                "[yellow]Run 'dagster-skills generate-index <skill-root>' to update.[/yellow]"
            )
            raise typer.Exit(code=1)
        console.print("[green]All generated indices are up to date.[/green]")
        return

    skill_md.write_text(new_skill_md)
    console.print(f"Updated {skill_md}")
    for readme_path, new_text in deferred_texts.items():
        readme_path.write_text(new_text)
        console.print(f"Updated {readme_path}")
