from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class NatsSettings(EnvBaseSettings):
    host: str = Field(alias="NATS_HOST")
    port: int = Field(alias="NATS_PORT")
    user: str = Field(alias="NATS_USER")
    password: SecretStr = Field(alias="NATS_PASSWORD")

    @property
    def url(self) -> str:
        """Generate the NATS connection URL."""
        return f"nats://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}"
