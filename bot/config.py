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

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

# Create settings instance
config = Config()
