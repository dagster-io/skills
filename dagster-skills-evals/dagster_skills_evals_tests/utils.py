import ast
import inspect
import os
import textwrap
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import cast


def write_function_body(func: Callable, filepath: str | Path) -> None:
    """Write the body of a function (excluding def line and docstring) to a file.

    Args:
        func: The function whose body to write.
        filepath: The path to write the body to.
    """

    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    func_def = cast("ast.FunctionDef", tree.body[0])
    first_stmt = func_def.body[0]
    last_stmt = func_def.body[-1]
    lines = source.splitlines()
    body = "\n".join(lines[first_stmt.lineno - 1 : last_stmt.end_lineno])
    Path(filepath).write_text(textwrap.dedent(body))


@contextmanager
def unset_virtualenv():
    _environ = os.environ.copy()
    try:
        os.environ.pop("VIRTUAL_ENV", None)
        yield
    finally:
        os.environ.clear()
        os.environ.update(_environ)
