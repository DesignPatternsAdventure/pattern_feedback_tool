"""DoIt tasks."""

from functools import partial
from pathlib import Path

from beartype import beartype
from calcipy.doit_tasks.base import debug_task
from calcipy.doit_tasks.doit_globals import DoitAction, DoitTask
from calcipy.doit_tasks.summary_reporter import SummaryReporter
from calcipy.file_helpers import if_found_unlink
from doit.tools import Interactive
from rich.console import Console

from .lint_parsers import display_lint_logs, parse_flake8_logs, parse_pylint_json_logs
from .settings import SETTINGS

# ================== Core Interaction Tasks ==================


@beartype
def task_play() -> DoitTask:
    """Launch and play the game!

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        Interactive('poetry run python -m game.play'),
    ])


@beartype
def task_next_task() -> DoitTask:
    """Ask for the next task!

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        (SETTINGS.next_task, ()),
    ])


# TODO: We probably need commands related to choose_task where the user can undo next_task


# ================== Feedback and Pass/Fail Tasks ==================


@beartype
def task_format() -> DoitTask:
    """Format code with black.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir().as_posix()
    return debug_task([
        Interactive(f'poetry run black "{task_dir}"'),
        Interactive(f'poetry run isort "{task_dir}"'),
    ])


@beartype
def task_test() -> DoitTask:
    """Run tests with Pytest.

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        Interactive(f'poetry run pytest tests {SETTINGS.ARGS_PYTEST}'),
    ])


@beartype
def _merge_linting_logs(flake8_log_path: Path, pylint_log_path: Path) -> None:  # noqa: CCR001
    """Merge pylint and flake8 linting errors for a combined report.

    Args:
        flake8_log_path: path to flake8 log file created with flag: `--output-file=...`
        pylint_log_path: path to pylint log file created with flag: `--output-format=json --output=...`

    Raises:
        RuntimeError: if flake8 and/or pylint log files contain any errors

    """
    flake8_logs = flake8_log_path.read_text().strip()
    pylint_logs = pylint_log_path.read_text().strip()
    if flake8_logs or pylint_logs:
        flake8_parsed = parse_flake8_logs(flake8_logs)
        pylint_parsed = parse_pylint_json_logs(pylint_logs)
        console = Console()
        display_lint_logs(console, flake8_parsed + pylint_parsed)

    if_found_unlink(flake8_log_path)
    if_found_unlink(pylint_log_path)


@beartype
def _lint_python() -> list[DoitAction]:
    """Lint specified files creating summary log file of errors.

    Args:
        lint_paths: list of file and directory paths to lint
        path_flake8: path to flake8 configuration file
        ignore_logs: list of error codes to ignore (beyond the flake8 config settings). Default is to ignore Code Tags
        xenon_args: string arguments passed to xenon. Default is for most strict options available
        diff_fail_under: integer minimum test coverage. Default is 80
        diff_branch: string branch to compare against. Default is `origin/main`

    Returns:
        list[DoitAction]: doit task

    """
    task_dir = SETTINGS.task_dir().as_posix()
    flake8_log_path = SETTINGS.PROJ_DIR / '.pft_flake8.log'
    pylint_log_path = SETTINGS.PROJ_DIR / '.pft_pylint.json'

    return [
        (if_found_unlink, (flake8_log_path,)),
        Interactive(
            f'poetry run flake8 {task_dir} --config=.flake8 --output-file={flake8_log_path.as_posix()} --color=never --exit-zero',
        ),
        (if_found_unlink, (pylint_log_path,)),
        Interactive(
            f'poetry run pylint {task_dir} --rcfile=.pylintrc --output-format=json --output={pylint_log_path.as_posix()} --exit-zero',
        ),
        (_merge_linting_logs, (flake8_log_path, pylint_log_path)),
    ]


@beartype
def task_check() -> DoitTask:
    """Run code quality checks.

    Returns:
        DoitTask: doit task

    """
    return debug_task(_lint_python())


@beartype
def task_build_diagrams() -> DoitTask:
    """Create shareable code diagrams.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir()
    package = task_dir.as_posix().replace('/', '.')
    diagrams_dir = task_dir / 'diagrams'

    def log_pyreverse_file_locations() -> None:
        console = Console()
        console.print(f'Created code diagrams in {diagrams_dir}')

    return debug_task([
        (partial(diagrams_dir.mkdir, exist_ok=True), ()),
        f'poetry run pyreverse {package} --output png --output-directory={diagrams_dir.as_posix()}',
        (log_pyreverse_file_locations, ()),
    ])


# ================== Optional Tasks ==================


@beartype
def task_watch_changes() -> DoitTask:
    """Re-run tests on changes with pytest watcher.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir().as_posix()
    return {
        'actions': [Interactive(f'poetry run ptw "{task_dir}" {SETTINGS.ARGS_PYTEST}')],
        'verbosity': 2,
    }


@beartype
def task_check_types() -> DoitTask:
    """Run type annotation checks with MyPy.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir().as_posix()
    return debug_task([
        Interactive(f'poetry run mypy {task_dir} {SETTINGS.ARGS_MYPY}'),
    ])


TASKS_PTW = [
    'format',
    'test',
    'check',
    'build_diagrams',
]
"""Full suite of tasks for local development."""

DOIT_CONFIG = {
    'action_string_formatting': 'old',  # Required for keyword-based tasks
    'default_tasks': TASKS_PTW,
    'reporter': SummaryReporter,
}
"""doit Configuration Settings. Run with `poetry run doit`."""

__all__ = ['DOIT_CONFIG'] + [fn for fn in locals() if fn.startswith('task_')]
"""Support star-import."""
