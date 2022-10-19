"""Graphic Output Tools."""

from pathlib import Path

from beartype import beartype
from code2flow.engine import code2flow

# ---------------- code2flow ----------------


@beartype
def run_code2flow(
    arg_path: Path,
    output_image: Path,
    **kwargs,
) -> None:
    """Run code2flow to generate a call graph.

    - Based on: https://github.com/scottrogowski/code2flow/blob/7cfc8204bcbff39d1f3e8e5359a97ed1ffe1aeca/code2flow/engine.py#L860-L875

    Args:
        arg_path: "Directory containing source files to analyze, or multiple file paths"

    """
    code2flow(raw_source_paths=[arg_path], output_file=output_image.as_posix(), **kwargs)


# ---------------- TODO: pylint.pyreverse ----------------
# See: https://github.com/PyCQA/pylint/blob/c2989ad5c71b3e1be0f0a7e5297f9b7e47fa2766/tests/pyreverse/conftest.py

# ---------------- TODO: pycg ----------------
