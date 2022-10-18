"""Linting Feedback Tools."""

from pathlib import Path

from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.complexity import SCORE


def run_radon(arg_path: Path) -> dict:
    """Run radon to check cyclomatic complexity.

    Args:
        arg_path: "Directory containing source files to analyze, or multiple file paths"

    """
    config = Config(
        exclude='',
        ignore='',
        order=SCORE,
        no_assert=False,
        show_closures=False,
        min='A',
        max='F',
    )
    harv = CCHarvester([arg_path.as_posix()], config)
    return harv._to_dicts()
