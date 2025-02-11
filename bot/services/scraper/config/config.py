from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class SiteSettings(EnvBaseSettings):
    year_id: int = Field(alias="YEAR_ID")
    semestr: int = Field(alias="SEMESTR")
