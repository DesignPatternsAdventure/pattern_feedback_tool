import json

from rich.console import Console

from pattern_feedback_tool.lint_parsers import display_lint_logs, parse_flake8_logs, parse_pylint_json_logs


def test_parse_pylint_json_logs(assert_against_cache):
    pylint_logs = json.dumps([
        {
            'type': 'refactor',
            'module': 'src.__main__',
            'obj': 'MyWindow',
            'line': 13,
            'column': 0,
            'endLine': 13,
            'endColumn': 14,
            'path': 'src/__main__.py',
            'symbol': 'too-many-ancestors',
            'message': 'Too many ancestors (6/3)',
            'message-id': 'R0901',
        },
        {
            'type': 'warning',
            'module': 'src.tasks.task1',
            'obj': 'SpriteGenerator.__init__',
            'line': 35,
            'column': 8,
            'endLine': 35,
            'endColumn': 12,
            'path': 'src/tasks/task1.py',
            'symbol': 'unnecessary-pass',
            'message': 'Unnecessary pass statement',
            'message-id': 'W0107',
        },
    ])

    results = parse_pylint_json_logs(pylint_logs)

    assert_against_cache([_r.dict() for _r in results])


def test_parse_flake8_logs(assert_against_cache):
    flake8_logs = """
src/tasks/__init__.py:3:1: F401 '.task1.SpriteGenerator' imported but unused
src/tasks/task1.py:61:1: E800 Found commented out code
"""

    results = parse_flake8_logs(flake8_logs)

    assert_against_cache([_r.dict() for _r in results])


def test_display_lint_logs():
    console = Console()
    logs = []

    display_lint_logs(console, logs)

    assert False
