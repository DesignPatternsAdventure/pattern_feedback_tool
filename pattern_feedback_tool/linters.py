"""Linting Feedback Tools."""

from collections.abc import Callable
from pathlib import Path
from typing import Literal, TypeAlias

from beartype import beartype
from beartype.typing import Protocol
from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.complexity import LINES

# ---------------- Radon ----------------


class _HarvesterProtocol(Protocol):
    def as_md(self) -> str:
        ...


_HARV_TYPE: TypeAlias = Callable[[list[str], Config], _HarvesterProtocol]


@beartype
def run_radon(
    arg_path: Path,
    *,
    min_score: Literal['A', 'B', 'C', 'D', 'E', 'F'] = 'A',
    radon_harvester: _HARV_TYPE | None = None,
) -> str:
    """Run radon to check cyclomatic complexity.

    - Based on: https://github.com/rubik/xenon/blob/b63601f6a0aba48150d92913c3522e19e33870f8/xenon/core.py
    - Radon Documentation: https://radon.readthedocs.io/en/latest/intro.html
    - Radon Source Code: https://github.com/rubik/radon/blob/941f8e20bdd8672d39fc395ebe893e43c1619cdf/radon/cli/__init__.py

    Args:
        arg_path: "Directory containing source files to analyze, or multiple file paths"
        min_score: minimum score to log. Default is 'A'
        radon_harvester: Alternatives are HCHarvester, MIHarvester, and RawHarvester. Default is CCHarvester

    Returns:
        str: markdown-formatted table

    """
    harvester: _HARV_TYPE = radon_harvester or CCHarvester
    config = Config(
        exclude='',
        ignore='',
        order=LINES,
        no_assert=False,
        show_closures=False,
        min=min_score,
        max='F',
        show_complexity=True,
    )
    return harvester([arg_path.as_posix()], config).as_md()
