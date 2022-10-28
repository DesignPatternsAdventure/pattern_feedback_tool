"""Parsers for lint module output."""

import json
from enum import Enum
from pathlib import Path

import pyparsing as pp
from beartype import beartype
from calcipy.doit_tasks.base import defaultdict
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table


class Linter(Enum):

    PYLINT = 'pylint'
    FLAKE8 = 'flake8'


class LintLog(BaseModel):

    source: Linter
    message: str
    message_id: str
    kind: str | None = None
    file_path: str
    line: str
    column: str
    end_line: str | None = None
    end_column: str | None = None
    obj: str | None = None

    @classmethod
    @beartype
    def from_pylint(cls, **kwargs) -> 'LintLog':  # type: ignore [no-untyped-def]
        """Dropped keys: module, symbol."""
        keys = ['obj', 'line', 'column', 'message']
        return cls(
            source=Linter.PYLINT,
            message_id=kwargs['message-id'],
            kind=kwargs['type'],
            file_path=kwargs['path'],
            end_line=kwargs['endLine'],
            end_column=kwargs['endColumn'],
            **{key: kwargs[key] for key in keys},
        )


@beartype
def parse_pylint_json_logs(pylint_logs: str) -> list[LintLog]:
    """Parse data from pylint json output."""
    return [LintLog.from_pylint(**item) for item in json.loads(pylint_logs)]


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

    return LintLog(source=Linter.FLAKE8, **parsed_log.as_dict())


@beartype
def parse_flake8_logs(flake8_logs: str) -> list[LintLog]:
    """Parse data from flake8 regular text output."""
    logs = []
    for raw_line in flake8_logs.split('\n'):
        if line := raw_line.strip():
            logs.append(_extract_flake8_data(line))
    return logs


# PLANNED: Move to a file that handles console output?
@beartype
def display_lint_logs(console: Console, logs: list[LintLog]) -> None:
    """Use rich to display an easily readable output from found LintLogs."""
    table = Table(show_header=True, header_style='bold')

    table.add_column('Source', style='Dim')
    table.add_column('File Path')
    table.add_column('Code', style='Bold')
    table.add_column('Message')

    grouped_logs = defaultdict(list)
    for log in logs:
        grouped_logs[log.file_path].append(log)

    for pth in sorted(grouped_logs):
        for log in grouped_logs[pth]:
            link = f'{log.file_path}:{log.line}:{log.column}'
            # Follows: https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda#file-uris-and-the-hostname
            file_uri = f'file:/{(Path.cwd() / link).as_posix()}'
            table.add_row(
                log.source.value,
                f'[link={file_uri}]{link}[/link]',
                f'[magenta]{log.message_id}[/]',
                f'{log.message} ({log.obj})' if log.obj else log.message,
            )

    console.print(table)
