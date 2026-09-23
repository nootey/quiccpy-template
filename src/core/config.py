from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingConfig(BaseModel):
    level: str = "INFO"


class Config(BaseSettings):
    # env vars take priority over .env values
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        env_nested_delimiter="__",
    )

    logging: LoggingConfig = LoggingConfig()
