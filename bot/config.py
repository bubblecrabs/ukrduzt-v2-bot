from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, computed_field

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

    @computed_field
    def postgres_dsn(self) -> str:
        """Computes the PostgreSQL DSN string and returns it for use in database connection."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
config = Config()
