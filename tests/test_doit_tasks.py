import pytest

from pattern_feedback_tool.doit_tasks import ptw_task, task_check_types, task_format, task_test


@pytest.mark.parametrize(
    ('task'), [
        task_format,
        task_test,
        # task_check,
        ptw_task,
        task_check_types,
    ],
)
def test_task_test(task, assert_against_cache):
    """Regression test each task set of commands."""
    result = task()

    assert_against_cache(result)
