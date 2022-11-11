import pytest

from pattern_feedback_tool.doit_tasks import (
    task__priv_build_diagrams, task__priv_check, task__priv_check_types, task__priv_format,
    task__priv_test, task__priv_update, task__priv_watch_changes, task_build_diagrams,
    task_check, task_check_types, task_format, task_play, task_test, task_watch_changes,
)


@pytest.mark.parametrize(
    'task', [
        task__priv_build_diagrams,
        task__priv_check,
        task__priv_check_types,
        task__priv_format,
        task__priv_update,
        task__priv_watch_changes,
        task_build_diagrams,
        task_check,
        task_check_types,
        task__priv_test,
        task_format,
        task_play,
        task_test,
        task_watch_changes,
    ],
)
def test_task_test(task, assert_against_cache):
    """Regression test each task set of commands."""
    result = task()

    assert_against_cache(result)
