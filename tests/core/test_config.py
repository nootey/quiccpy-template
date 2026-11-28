from pathlib import Path

import pytest
from pydantic import ValidationError

from src.core.config import Config


def test_config_loads(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("APP_ENVIRONMENT=production\nAPP_LOGGING__LEVEL=DEBUG\n")

    config = Config(_env_file=env_file)
    assert config.environment == "production"
    assert config.logging.level == "DEBUG"


def test_config_defaults(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("")

    config = Config(_env_file=env_file)
    assert config.environment == "local"
    assert config.logging.level == "INFO"


def test_config_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("APP_LOGGING__LEVEL=DEBUG\n")

    monkeypatch.setenv("APP_LOGGING__LEVEL", "WARNING")
    config = Config(_env_file=env_file)
    assert config.logging.level == "WARNING"


def test_config_missing_file() -> None:
    config = Config(_env_file="nonexistent.env")
    assert config.logging.level == "INFO"


@pytest.mark.parametrize("name", ["APP_ENVIRONMENT", "APP_LOGGING__LEVEL"])
def test_config_rejects_unknown_values(
    name: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(name, "garbage")
    with pytest.raises(ValidationError):
        Config(_env_file=None)
