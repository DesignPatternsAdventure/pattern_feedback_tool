"""DoIt tasks."""

import sys
from collections import defaultdict
from collections.abc import Iterable
from functools import lru_cache, partial
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


@lru_cache(maxsize=1)
def run_mod() -> str:
    """Return the currently active Python."""
    return f'{sys.executable} -m'


@beartype
def user_task(actions: Iterable[DoitAction], verbosity: int = 2) -> DoitTask:
    """Show reduced output for user-facing commands.

    Args:
        actions: list of doit actions
        verbosity: 2 is maximum, while 0 is deactivated. Default is 2

    Returns:
        DoitTask: doit task

    """
    task: DoitTask = defaultdict(list)
    task['actions'] = actions
    task['title'] = lambda _task: ''
    task['verbosity'] = verbosity
    return task


@beartype
def task___update() -> DoitTask:
    """Run update operations and update the requirements file.

    Returns:
        DoitTask: DoIt task

    """
    return debug_task(
        [
            Interactive('poetry lock --no-update'),
            Interactive(
                'poetry export --format=requirements.txt --output=requirements.txt --without-hashes --with=dev',
            ),
        ],
    )

# ================== Core Interaction Tasks ==================


@beartype
def task_play() -> DoitTask:
    """Launch and play the game!

    Returns:
        DoitTask: doit task

    """
    return user_task([
        Interactive(f'{run_mod()} -m game.play'),
    ])


# ================== Feedback and Pass/Fail Tasks ==================


@beartype
def task___format() -> DoitTask:
    """Format all project code and not just the tasks.

    Returns:
        DoitTask: doit task

    """
    paths = 'tests game ./dodo.py'
    cwd = Path.cwd()
    tracked_files = [*(cwd / 'game').rglob('*.py')] + [*(cwd / 'tests').rglob('*.py')] + [cwd / 'dodo.py']
    file_paths = ' '.join([f'"{pth.relative_to(cwd).as_posix()}"' for pth in tracked_files])
    docfmt_args = '--blank --close-quotes-on-newline --in-place --wrap-summaries=120 --wrap-descriptions=120'
    return debug_task([
        f'{run_mod()} black {paths} --quiet',
        f'{run_mod()} pyupgrade {file_paths} --py310-plus --keep-runtime-typing --exit-zero',
        f'{run_mod()} unimport {paths} --include-star-import --remove',
        f'{run_mod()} absolufy-imports {file_paths} --never',
        f'{run_mod()} isort {paths}',
        f'{run_mod()} docformatter {file_paths} {docfmt_args}',
    ])


@beartype
def task_format() -> DoitTask:
    """Format code with black and isort.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir().as_posix()
    return user_task([
        Interactive(f'{run_mod()} black "{task_dir}"'),
        Interactive(f'{run_mod()} unimport "{task_dir}" --remove'),
        Interactive(f'{run_mod()} isort "{task_dir}"'),
    ])


@beartype
def task___test() -> DoitTask:
    """Run all tests using Pytest.

    Returns:
        DoitTask: doit task

    """
    return user_task([
        Interactive(f'{run_mod()} pytest tests {SETTINGS.ARGS_PYTEST}'),
    ])


@beartype
def task_test() -> DoitTask:
    """Run all tests marked with 'tasks' using Pytest.

    Returns:
        DoitTask: doit task

    """
    pytest_args = '--disable-warnings -m tasks'
    return user_task([
        Interactive(f'{run_mod()} pytest tests {pytest_args} {SETTINGS.ARGS_PYTEST}'),
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
def _lint_python(paths: str) -> list[DoitAction]:
    """Lint specified files creating summary log file of errors.

    Args:
        paths: str set of paths to lint

    Returns:
        list[DoitAction]: doit task

    """
    flake8_log_path = SETTINGS.PROJ_DIR / '.pft_flake8.log'
    pylint_log_path = SETTINGS.PROJ_DIR / '.pft_pylint.json'

    flake8_args = '--config=.flake8 --color=never --exit-zero'
    pylint_args = '--rcfile=.pylintrc --output-format=json --exit-zero'

    return [
        (if_found_unlink, (flake8_log_path,)),
        Interactive(
            f'{run_mod()} flake8 {paths} --output-file={flake8_log_path.as_posix()} {flake8_args}',
        ),
        (if_found_unlink, (pylint_log_path,)),
        Interactive(
            f'{run_mod()} pylint {paths} --output={pylint_log_path.as_posix()} {pylint_args}',
        ),
        (_merge_linting_logs, (flake8_log_path, pylint_log_path)),
    ]


@beartype
def task___check() -> DoitTask:
    """Format all project code and not just the tasks.

    Returns:
        DoitTask: doit task

    """
    paths = 'tests game ./dodo.py'
    return debug_task(_lint_python(paths))


@beartype
def task_check() -> DoitTask:
    """Run code quality checks.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir().as_posix()
    return user_task(_lint_python(task_dir))


@beartype
def _log_pyreverse_file_locations(diagrams_dir: Path) -> None:
    console = Console()
    console.print(f'Created code diagrams in {diagrams_dir}', style='bold green')


@beartype
def task___build_diagrams() -> DoitTask:
    """Create shareable code diagrams for entire project.

    Returns:
        DoitTask: doit task

    """
    package = 'game'
    diagrams_dir = Path(package) / 'diagrams'
    return debug_task([
        (partial(diagrams_dir.mkdir, exist_ok=True), ()),
        f'poetry run pyreverse {package} --output png --output-directory={diagrams_dir.as_posix()}',
        (_log_pyreverse_file_locations, (diagrams_dir,)),
    ])


@beartype
def task_build_diagrams() -> DoitTask:
    """Create shareable code diagrams.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir()
    package = task_dir.as_posix().replace('/', '.')
    diagrams_dir = task_dir / 'diagrams'

    return user_task([
        (partial(diagrams_dir.mkdir, exist_ok=True), ()),
        f'poetry run pyreverse {package} --output png --output-directory={diagrams_dir.as_posix()}',
        (_log_pyreverse_file_locations, (diagrams_dir,)),
    ])


# ================== Optional Tasks ==================


@beartype
def _build_ptw(pytest_args: str) -> DoitTask:
    task_dir = SETTINGS.task_dir().as_posix()
    return {
        'actions': [Interactive(f'{run_mod()} ptw "{task_dir}" {pytest_args} {SETTINGS.ARGS_PYTEST}')],
        'verbosity': 2,
    }


@beartype
def task___watch_changes() -> DoitTask:
    """Re-run tests on changes with pytest watcher.

    Returns:
        DoitTask: doit task

    """
    return _build_ptw('')


@beartype
def task_watch_changes() -> DoitTask:
    """Re-run tests tagged with tasks on changes with pytest watcher.

    Returns:
        DoitTask: doit task

    """
    return _build_ptw('--disable-warnings -m tasks')


@beartype
def task___check_types() -> DoitTask:
    """Run type annotation checks with MyPy against the entire package.

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        Interactive(f'{run_mod()} mypy game {SETTINGS.ARGS_MYPY}'),
    ])


@beartype
def task_check_types() -> DoitTask:
    """Run type annotation checks with MyPy.

    Returns:
        DoitTask: doit task

    """
    task_dir = SETTINGS.task_dir().as_posix()
    return user_task([
        Interactive(f'{run_mod()} mypy {task_dir} {SETTINGS.ARGS_MYPY}'),
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
