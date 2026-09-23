from src.core.config import Config


def test_config_loads(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("APP_LOGGING__LEVEL=DEBUG\n")

    config = Config(_env_file=env_file)
    assert config.logging.level == "DEBUG"


def test_config_defaults(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("")

    config = Config(_env_file=env_file)
    assert config.logging.level == "INFO"


def test_config_env_override(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("APP_LOGGING__LEVEL=DEBUG\n")

    monkeypatch.setenv("APP_LOGGING__LEVEL", "WARNING")
    config = Config(_env_file=env_file)
    assert config.logging.level == "WARNING"


def test_config_missing_file():
    config = Config(_env_file="nonexistent.env")
    assert config.logging.level == "INFO"
