from urllib.parse import quote

from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr


class Config(BaseSettings):
    # Bot settings
    admin: int = Field(alias="ADMIN")
    token: SecretStr = Field(alias="BOT_TOKEN")

    # Site settings
    year_id: int = Field(alias="YEAR_ID")
    semestr: int = Field(alias="SEMESTR")

    # Logging settings
    logging_level: int = Field(alias="LOG_LEVEL")

    # PostgreSQL settings
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: SecretStr = Field(alias="POSTGRES_PASSWORD")

    # Redis settings
    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    redis_db: int = Field(alias="REDIS_DB")
    redis_password: SecretStr = Field(alias="REDIS_PASSWORD")
    redis_ttl: int = Field(alias="REDIS_TTL")

    class Config:
        env_file: str = "../.env"
        env_file_encoding: str = "utf-8"

    def get_redis_url(self) -> str:
        """Generate the Redis connection URL."""
        encoded_password: str = quote(self.redis_password.get_secret_value())
        return f"redis://:{encoded_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
