"""Parsers for lint module output."""

import json

import pyparsing as pp
from beartype import beartype
from pydantic import BaseModel
from rich.console import Console


class LintLog(BaseModel):

    kind: str | None = None
    obj: str | None = None
    line: str
    column: str
    end_line: str | None = None
    end_column: str | None = None
    file_path: str
    message: str
    message_id: str

    @classmethod
    def from_pylint(cls, pylint_data: dict) -> 'LintLog':
        """Dropped keys: module, symbol."""
        keys = ['obj', 'line', 'column', 'message']
        return cls(
            kind=pylint_data['type'],
            end_line=pylint_data['endLine'],
            end_column=pylint_data['endColumn'],
            file_path=pylint_data['path'],
            message_id=pylint_data['message-id'],
            **{key: pylint_data[key] for key in keys},
        )


@beartype
def parse_pylint_json_logs(pylint_logs: str) -> list[LintLog]:
    """Parse data from pylint json output."""
    return [LintLog.from_pylint(item) for item in json.loads(pylint_logs)]


@beartype
def _extract_flake8_data(line: str) -> LintLog:
    """Parse data from flake8 for a single line of regular text output."""
    integer = pp.Word(pp.nums).set_parse_action(lambda _t: int(_t[0]))
    full_path = pp.Regex(r'[^:]+')('file_path') + ':' + integer('line') + ':' + integer('column') + pp.Literal(':')
    code = pp.Word(pp.alphanums)('message_id')
    obj = pp.Opt(pp.QuotedString("'"))('obj')
    message = pp.Regex(r'.+')('message')

    flake8_grammar = full_path + code + obj + message
    parsed_log = flake8_grammar.parse_string(line, parse_all=True)

    return LintLog(**parsed_log.as_dict())


@beartype
def parse_flake8_logs(flake8_logs: str) -> list[LintLog]:
    """Parse data from flake8 regular text output."""
    logs = []
    for raw_line in flake8_logs.split('\n'):
        if line := raw_line.strip():
            logs.append(_extract_flake8_data(line))
    return logs


@beartype
def display_lint_logs(console: Console, logs: list[LintLog]) -> None:
    """Use rich to display an easily readable output from found LintLogs."""
    raise NotImplementedError('...')
