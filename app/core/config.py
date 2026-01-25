from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url:str
    db_schema: str = "issue_triage"


if TYPE_CHECKING:
    settings = Settings(database_url="postgresql+psycopg://example")
else:
    settings = Settings()
