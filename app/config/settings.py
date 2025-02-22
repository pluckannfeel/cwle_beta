import os

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, Union
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "介護福祉士試験対策アプリのAPI(Backend)"

    # Database
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000",]

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ENVIRONMENT: str = "development"

    # # OpenAI
    # OPENAI_API_KEY: str
    # OPENAI_ORGANIZATION: str = "your_openai_org_id"
    # # AWS
    # ACCESS_KEY_ID_AWS: str = "your_default_access_key_id"
    # SECRET_ACCESS_KEY_AWS: str
    # REGION_AWS: str = "ap-northeast-1"

    # OPENAI_API_KEY: str
    # OPENAI_ORGANIZATION: str = "your_openai_org_id"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
    OPENAI_ORGANIZATION: str = os.getenv(
        "OPENAI_ORGANIZATION", "your_openai_org_id")

    # AWS Credentials (Environment variables should be set on Lambda)
    ACCESS_KEY_ID_AWS: str = os.getenv(
        "ACCESS_KEY_ID_AWS", "your_default_access_key_id")
    SECRET_ACCESS_KEY_AWS: str = os.getenv("SECRET_ACCESS_KEY_AWS")
    REGION_AWS: str = os.getenv("REGION_AWS", "ap-northeast-1")

    # LOG PATH
    LOG_PATH: str

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
