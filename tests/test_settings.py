from pattern_feedback_tool.settings import SETTINGS

from .configuration import TEST_DIR


def test_settings_user_config():
    result = SETTINGS.USER_CONFIG.relative_to(TEST_DIR.parent)

    assert result.name == result.as_posix()  # i.e. only a filename
    assert result.suffix == '.toml'
