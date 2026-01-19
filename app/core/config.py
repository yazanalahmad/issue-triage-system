from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings():
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url=str
    db_schema: str = "issue_triage"


settings = Settings()