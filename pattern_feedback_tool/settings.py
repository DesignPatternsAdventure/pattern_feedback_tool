"""User Settings."""

from pathlib import Path

import tomlkit
from beartype import beartype
from pydantic import BaseSettings, Field


class _Settings(BaseSettings):

    PROJ_DIR: Path = Field(default_factory=lambda: Path('.'))
    USER_CONFIG: Path = Field(default_factory=lambda: Path('.pft_config.toml'))

    ACTIVE_TASK: str = 'task_1'
    COMPLETED_TASKS: list[str] = Field(default_factory=list)

    # Extra hooks to modify task behavior. Intended for internal use only
    ARGS_PYTEST: str = ''
    ARGS_PYLINT: str = ''
    ARGS_FLAKE8: str = ''
    ARGS_MYPY: str = ''

    class Config:
        prefix = 'PFT_'

    @beartype
    def task_dir(self) -> Path:
        return self.PROJ_DIR / 'game/tasks'  # / self.ACTIVE_TASK` << FIXME: Use sub-directories

    @beartype
    def next_task(self) -> None:
        # TODO: Call self.persist() and update the ACTIVE_TASK & COMPLETED_TASKS
        # TODO: Generate the task directory based on existing user code, the new skeleton code, and README
        raise NotImplementedError('Sorry, but there is no Task2 yet')

    @beartype
    def persist(self) -> None:
        self.USER_CONFIG.write_text(tomlkit.dumps(self.dict()))


@beartype
def _merge_saved_settings(settings: _Settings) -> _Settings:
    user_settings = {}  # type: ignore [var-annotated]
    if settings.USER_CONFIG.is_file():
        user_settings = tomlkit.loads(settings.USER_CONFIG.read_text())
    kwargs = settings.dict() | user_settings
    return _Settings(**kwargs)


SETTINGS = _merge_saved_settings(_Settings())
"""Singleton settings object."""
