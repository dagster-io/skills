"""Validate Python code blocks in skills markdown files.

Parses all .md files under the skills directory, extracts Python fenced code blocks,
and validates them with ruff (undefined names, syntax errors) and pyright (type checking).
Blocks that can't be checked (e.g. fragments with intentionally undefined names) opt out
via ``nocheck`` in the fence info string:

    ```python nocheck
    my_job.execute_in_process()  # my_job defined elsewhere
    ```

Blocks that only reference externally-defined names use ``nocheckundefined`` to suppress
undefined-name checks while preserving syntax and type checking:

    ```python nocheckundefined
    result = my_custom_function()  # defined in user code
    ```
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from markdown_it import MarkdownIt

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"
SKILL_DIRS = ["dagster-expert"]

# Focused rule for doc code blocks — undefined names.
# Syntax errors are always reported by ruff regardless of selection.
RUFF_SELECT = "F821"


def _collect_python_blocks() -> list[tuple[str, str, bool]]:
    """Yield (label, code, nocheckundefined) for each python fence block not marked nocheck."""
    if not SKILLS_DIR.is_dir():
        return []

    md = MarkdownIt()
    blocks: list[tuple[str, str, bool]] = []

    for skill_name in SKILL_DIRS:
        skill_dir = SKILLS_DIR / skill_name
        if not skill_dir.is_dir():
            continue
        for md_path in sorted(skill_dir.rglob("*.md")):
            tokens = md.parse(md_path.read_text())
            for token in tokens:
                if token.type != "fence":
                    continue
                info_parts = token.info.strip().split()
                if not info_parts or info_parts[0] != "python":
                    continue
                if "nocheck" in info_parts[1:]:
                    continue

                nocheckundefined = "nocheckundefined" in info_parts[1:]

                # token.map is formatted as [start_line, end_line] (0-indexed)
                line_number = (token.map[0] + 1) if token.map else 0
                rel_path = md_path.relative_to(SKILLS_DIR)
                label = f"{rel_path}:{line_number}"
                blocks.append((label, token.content, nocheckundefined))

    return blocks


def _prepare_code(code: str) -> str:
    if "import dagster" not in code:
        code = "import dagster as dg\n" + code
    return code


def _label_to_filename(label: str) -> str:
    return label.replace("/", "__").replace(":", "_L") + ".py"


VENV_DIR = Path(sys.prefix)


def _run_pyright_on_blocks(
    blocks: list[tuple[str, str]],
    pyright_config: dict | None = None,
) -> dict[str, list[str]]:
    """Run pyright once on all blocks, return {label: [error_messages]}."""
    if not blocks:
        return {}

    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            "venvPath": str(VENV_DIR.parent),
            "venv": VENV_DIR.name,
            **(pyright_config or {}),
        }
        (Path(tmpdir) / "pyrightconfig.json").write_text(json.dumps(config))

        file_to_label: dict[str, str] = {}
        for label, code in blocks:
            filename = _label_to_filename(label)
            (Path(tmpdir) / filename).write_text(_prepare_code(code))
            file_to_label[filename] = label

        result = subprocess.run(
            ["pyright", "--outputjson", "--level", "error", "--project", tmpdir],
            capture_output=True,
            text=True,
            check=False,
        )

        data = json.loads(result.stdout)

        errors_by_label: dict[str, list[str]] = {}
        for diag in data.get("generalDiagnostics", []):
            filename = Path(diag["file"]).name
            label = file_to_label.get(filename)
            if label and diag["severity"] == "error":
                line = diag["range"]["start"]["line"]
                rule = diag.get("rule", "")
                msg = f"line {line}: {diag['message']}"
                if rule:
                    msg = f"line {line} [{rule}]: {diag['message']}"
                errors_by_label.setdefault(label, []).append(msg)

        return errors_by_label


_BLOCKS = _collect_python_blocks()
_NORMAL_BLOCKS = [(label, code) for label, code, nocheck in _BLOCKS if not nocheck]
_NOCHECKUNDEFINED_BLOCKS = [(label, code) for label, code, nocheck in _BLOCKS if nocheck]


@pytest.fixture(scope="session")
def pyright_errors() -> dict[str, list[str]]:
    normal_errors = _run_pyright_on_blocks(_NORMAL_BLOCKS)
    nocheck_errors = _run_pyright_on_blocks(
        _NOCHECKUNDEFINED_BLOCKS,
        pyright_config={"reportUndefinedVariable": "none", "reportMissingImports": "none"},
    )
    return {**normal_errors, **nocheck_errors}


@pytest.mark.parametrize(
    ("label", "code"),
    _NORMAL_BLOCKS,
    ids=[b[0] for b in _NORMAL_BLOCKS],
)
def test_python_code_block_ruff(label: str, code: str) -> None:
    code = _prepare_code(code)
    result = subprocess.run(
        ["ruff", "check", "--select", RUFF_SELECT, "--stdin-filename", label, "-"],
        input=code,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize(
    "label",
    [b[0] for b in _NORMAL_BLOCKS + _NOCHECKUNDEFINED_BLOCKS],
    ids=[b[0] for b in _NORMAL_BLOCKS + _NOCHECKUNDEFINED_BLOCKS],
)
def test_python_code_block_pyright(label: str, pyright_errors: dict[str, list[str]]) -> None:
    errors = pyright_errors.get(label, [])
    assert not errors, "\n".join(errors)


# ---------------------------------------------------------------------------
# Link validation helpers and tests
# ---------------------------------------------------------------------------

_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def _extract_local_links(md_path: Path) -> list[tuple[str, Path]]:
    """Extract local file links from a markdown file, resolving them to absolute paths."""
    content = md_path.read_text()
    results: list[tuple[str, Path]] = []
    for _, raw_target in _LINK_RE.findall(content):
        if raw_target.startswith(("http://", "https://", "#")):
            continue
        # Strip anchor fragments from the target
        target = raw_target.split("#")[0]
        if not target:
            continue
        resolved = (md_path.parent / target).resolve()
        # Directory links resolve to README.md inside the directory
        if resolved.is_dir() or target.endswith("/"):
            resolved = resolved / "README.md"
        results.append((target, resolved))
    return results


def _collect_link_cases() -> list[tuple[str, str, Path]]:
    """Collect all (label, raw_link, resolved_path) for parametrized link validation."""
    cases: list[tuple[str, str, Path]] = []
    for skill_name in SKILL_DIRS:
        skill_dir = SKILLS_DIR / skill_name / "skills" / skill_name
        if not skill_dir.is_dir():
            continue
        for md_path in sorted(skill_dir.rglob("*.md")):
            content = md_path.read_text()
            for line_no, line in enumerate(content.splitlines(), 1):
                for _, target in _LINK_RE.findall(line):
                    if target.startswith(("http://", "https://", "#")):
                        continue
                    clean_target = target.split("#")[0]
                    if not clean_target:
                        continue
                    resolved = (md_path.parent / clean_target).resolve()
                    if resolved.is_dir() or clean_target.endswith("/"):
                        resolved = resolved / "README.md"
                    rel = md_path.relative_to(SKILLS_DIR)
                    label = f"{rel}:{line_no}"
                    cases.append((label, target, resolved))
    return cases


_LINK_CASES = _collect_link_cases()


@pytest.mark.parametrize(
    ("label", "raw_link", "resolved"),
    _LINK_CASES,
    ids=[f"{c[0]} -> {c[1]}" for c in _LINK_CASES],
)
def test_skill_reference_links_valid(label: str, raw_link: str, resolved: Path) -> None:
    assert (
        resolved.exists()
    ), f"{label}: link '{raw_link}' resolves to {resolved} which does not exist"


def _compute_reachable_files() -> dict[str, set[Path]]:
    """BFS from SKILL.md to find all transitively reachable files per skill."""
    result: dict[str, set[Path]] = {}
    for skill_name in SKILL_DIRS:
        skill_dir = SKILLS_DIR / skill_name / "skills" / skill_name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue

        reachable: set[Path] = set()
        queue = [skill_md.resolve()]
        visited: set[Path] = set()

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            reachable.add(current)

            if current.suffix == ".md" and current.is_file():
                for _, target_path in _extract_local_links(current):
                    resolved = target_path.resolve()
                    reachable.add(resolved)
                    if resolved.suffix == ".md" and resolved not in visited:
                        queue.append(resolved)

        result[skill_name] = reachable
    return result


_REACHABLE = _compute_reachable_files()


def _collect_reachability_cases() -> list[tuple[str, Path, set[Path]]]:
    """Collect all (label, file_path, reachable_set) for parametrized reachability test."""
    cases: list[tuple[str, Path, set[Path]]] = []
    for skill_name in SKILL_DIRS:
        skill_dir = SKILLS_DIR / skill_name / "skills" / skill_name
        if not skill_dir.is_dir():
            continue
        reachable = _REACHABLE.get(skill_name, set())
        for file_path in sorted(skill_dir.rglob("*")):
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(SKILLS_DIR)
            cases.append((str(rel), file_path.resolve(), reachable))
    return cases


_REACHABILITY_CASES = _collect_reachability_cases()


@pytest.mark.parametrize(
    ("label", "file_path", "reachable"),
    _REACHABILITY_CASES,
    ids=[c[0] for c in _REACHABILITY_CASES],
)
def test_skill_files_reachable(label: str, file_path: Path, reachable: set[Path]) -> None:
    assert file_path in reachable, f"{label}: file is not reachable from SKILL.md"
