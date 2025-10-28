from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    APP_NAME: str = "Tracker2"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 9444
    EXTERNAL_URL: str | None = None
    TRUST_PROXY: int = 1

    UI_USERNAME: str = "admin"
    UI_PASSWORD_HASH: str = ""
    API_TOKEN: str = "change-me"

    DB_URL: str = "sqlite+aiosqlite:///./dev.db"

    CORS_ORIGINS: List[AnyHttpUrl] = []
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | List[AnyHttpUrl]) -> List[str] | List[AnyHttpUrl]:
        if isinstance(value, str):
            if not value.strip():
                return []
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            if not value.strip():
                return []
            return [host.strip() for host in value.split(",") if host.strip()]
        return value

settings = Settings()
