import pytest

from pattern_feedback_tool.doit_tasks import (
    task_build_diagrams, task_check, task_check_types, task_format, task_next_task, task_play, task_ptw, task_test,
)


@pytest.mark.parametrize(
    ('task'), [
        task_build_diagrams,
        task_check,
        task_check_types,
        task_format,
        task_next_task,
        task_play,
        task_ptw,
        task_test,
    ],
)
def test_task_test(task, assert_against_cache):
    """Regression test each task set of commands."""
    result = task()

    assert_against_cache(result)
