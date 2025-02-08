from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings(EnvBaseSettings):
    token: SecretStr = Field(alias="BOT_TOKEN")


class LoggingSettings(EnvBaseSettings):
    level: int = Field(alias="LOG_LEVEL")


class PostgresSettings(EnvBaseSettings):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    db: str = Field(alias="POSTGRES_DB")
    user: str = Field(alias="POSTGRES_USER")
    password: SecretStr = Field(alias="POSTGRES_PASSWORD")

    @property
    def url(self) -> str:
        """Generate the PostgreSQL connection URL."""
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"



class RedisSettings(EnvBaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB")
    password: SecretStr = Field(alias="REDIS_PASSWORD")
    ttl: int = Field(alias="REDIS_TTL")

    @property
    def url(self) -> str:
        """Generate the Redis connection URL."""
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class SiteSettings(EnvBaseSettings):
    year_id: int = Field(alias="YEAR_ID")
    semestr: int = Field(alias="SEMESTR")


class Settings:
    def __init__(self):
        self.bot = BotSettings()
        self.logging = LoggingSettings()
        self.postgres = PostgresSettings()
        self.redis = RedisSettings()
        self.site = SiteSettings()


settings = Settings()
