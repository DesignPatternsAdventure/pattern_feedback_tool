import pytest

from pattern_feedback_tool.doit_tasks import (
    task_build_diagrams, task_check, task_check_all, task_check_types,
    task_format, task_format_all, task_play, task_test, task_watch_changes,
)


@pytest.mark.parametrize(
    ('task'), [
        task_build_diagrams,
        task_check,
        task_check_all,
        task_check_types,
        task_format,
        task_format_all,
        task_play,
        task_test,
        task_watch_changes,
    ],
)
def test_task_test(task, assert_against_cache):
    """Regression test each task set of commands."""
    result = task()

    assert_against_cache(result)
