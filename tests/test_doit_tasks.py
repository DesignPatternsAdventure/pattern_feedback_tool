import pytest

from pattern_feedback_tool.doit_tasks import (
    task__build_diagrams, task__check, task__check_types, task__format, task__test,
    task__update, task__watch_changes, task_build_diagrams, task_check, task_check_types,
    task_format, task_play, task_reset_map, task_test, task_watch_changes,
)


@pytest.mark.parametrize(
    'task', [
        task__build_diagrams,
        task__check,
        task__check_types,
        task__format,
        task__update,
        task_reset_map,
        task__watch_changes,
        task_build_diagrams,
        task_check,
        task_check_types,
        task__test,
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
