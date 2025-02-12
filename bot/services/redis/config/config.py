from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class RedisSettings(EnvBaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    user: str = Field(alias="REDIS_USER")
    password: SecretStr = Field(alias="REDIS_PASSWORD")
    db: int = Field(alias="REDIS_DB")
    ttl: int = Field(alias="REDIS_TTL")

    @property
    def url(self) -> str:
        """Generate the Redis connection URL."""
        return f"redis://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"
