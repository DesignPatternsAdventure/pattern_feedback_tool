from pattern_feedback_tool.settings import SETTINGS


def test_settings_user_config():
    result = SETTINGS.USER_CONFIG

    assert result.name == result.as_posix()  # i.e. only a filename
    assert result.suffix == '.toml'
