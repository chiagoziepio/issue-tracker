from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ISSUER: str = "issue-tracker"
    AUDIENCE: str = "issue-tracker"
    JWT_FRESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore[call-arg]
