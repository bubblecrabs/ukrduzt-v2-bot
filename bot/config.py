from urllib.parse import quote

from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr


class BotSettings(BaseSettings):
    admin: int = Field(alias="ADMIN")
    token: SecretStr = Field(alias="BOT_TOKEN")


class SiteSettings(BaseSettings):
    year_id: int = Field(alias="YEAR_ID")
    semestr: int = Field(alias="SEMESTR")


class LoggingSettings(BaseSettings):
    level: int = Field(alias="LOG_LEVEL")


class PostgresSettings(BaseSettings):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    db: str = Field(alias="POSTGRES_DB")
    user: str = Field(alias="POSTGRES_USER")
    password: SecretStr = Field(alias="POSTGRES_PASSWORD")

    @property
    def url(self) -> str:
        """Generate the PostgreSQL connection URL."""
        encoded_password: str = quote(self.password.get_secret_value())
        return (
            f"postgresql+asyncpg://{self.user}:{encoded_password}@"
            f"{self.host}:{self.port}/{self.db}"
        )


class RedisSettings(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB")
    password: SecretStr = Field(alias="REDIS_PASSWORD")
    ttl: int = Field(alias="REDIS_TTL")

    @property
    def url(self) -> str:
        """Generate the Redis connection URL."""
        encoded_password: str = quote(self.password.get_secret_value())
        return f"redis://:{encoded_password}@{self.host}:{self.port}/{self.db}"


class Config:
    bot: BotSettings = BotSettings()
    site: SiteSettings = SiteSettings()
    logging: LoggingSettings = LoggingSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()

    class BaseConfig:
        env_file: str = "../.env"
        env_file_encoding: str = "utf-8"