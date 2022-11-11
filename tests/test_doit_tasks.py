import pytest

from pattern_feedback_tool.doit_tasks import (
    task___build_diagrams, task___check, task___check_types, task___format,
    task___test, task___update, task___watch_changes, task_build_diagrams, task_check,
    task_check_types, task_format, task_play, task_test, task_watch_changes,
)


@pytest.mark.parametrize(
    'task', [
        task___build_diagrams,
        task___check,
        task___check_types,
        task___format,
        task___update,
        task___watch_changes,
        task_build_diagrams,
        task_check,
        task_check_types,
        task___test,
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
