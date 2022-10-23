"""DoIt tasks."""

from pathlib import Path

from beartype import beartype
from calcipy.doit_tasks.base import debug_task
from calcipy.doit_tasks.doit_globals import DoitTask
from calcipy.doit_tasks.summary_reporter import SummaryReporter
from doit.tools import Interactive

from .settings import SETTINGS


@beartype
def resolve_task_dir() -> Path:
    return SETTINGS.CWD / SETTINGS.ACTIVE_TASK

# ================== Core Tasks ==================


@beartype
def task_format() -> DoitTask:
    """Format code with black.

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        Interactive(f'poetry run black "{resolve_task_dir()}"'),
        Interactive(f'poetry run isort "{resolve_task_dir()}"'),
    ])


@beartype
def task_test() -> DoitTask:
    """Run tests with Pytest.

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        Interactive(f'poetry run pytest "{resolve_task_dir()}/tests" {SETTINGS.ARGS_PYTEST}'),
    ])


@beartype
def task_check() -> DoitTask:
    """Run code quality checks.

    Returns:
        DoitTask: doit task

    """
    raise NotImplementedError("Not yet implemented!")


# ================== Optional Tasks ==================

@beartype
def ptw_task() -> DoitTask:
    """Re-run tests on changes with pytest watcher.

    Returns:
        DoitTask: doit task

    """
    return {
        'actions': [Interactive(f'poetry run ptw "{resolve_task_dir()}" {SETTINGS.ARGS_PYTEST}')],
        'verbosity': 2,
    }


@beartype
def task_check_types() -> DoitTask:
    """Run type annotation checks with MyPy.

    Returns:
        DoitTask: doit task

    """
    return debug_task([
        Interactive(f'poetry run mypy {resolve_task_dir()} {SETTINGS.ARGS_MYPY}'),
    ])


TASKS_PTW = [
    'format',
    'test',
    'check',
]
"""Full suite of tasks for local development."""

DOIT_CONFIG_PFT = {
    'action_string_formatting': 'old',  # Required for keyword-based tasks
    'backend': 'sqlite3',  # Best support for concurrency
    'default_tasks': TASKS_PTW,
    'dep_file': '.doit-db.sqlite',
    'reporter': SummaryReporter,
}
"""doit Configuration Settings. Run with `poetry run doit`."""
