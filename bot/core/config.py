from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

from bot.services.database.config.config import PostgresSettings
from bot.services.redis.config.config import RedisSettings
from bot.services.nats.config.config import NatsSettings
from bot.services.scraper.config.config import SiteSettings


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings(EnvBaseSettings):
    token: SecretStr = Field(alias="BOT_TOKEN")


class LoggingSettings(EnvBaseSettings):
    level: int = Field(alias="LOG_LEVEL")


class Settings:
    def __init__(self):
        self.bot = BotSettings()
        self.logging = LoggingSettings()
        self.postgres = PostgresSettings()
        self.redis = RedisSettings()
        self.nats = NatsSettings()
        self.site = SiteSettings()


settings = Settings()
