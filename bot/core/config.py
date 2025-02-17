from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

from bot.services.database.config.config import PostgresSettings
from bot.services.redis.config.config import RedisSettings


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings(EnvBaseSettings):
    token: SecretStr = Field(alias="BOT_TOKEN")


class Settings(EnvBaseSettings):
    bot: BotSettings = Field(default_factory=BotSettings)
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)


settings = Settings()
