# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    ENV_NAME: str = "local"
    API_TITLE: str = "MyApp"
    API_VERSION: str = "0.1.0"

    # MongoDB Connection
    MONGO_URI: str
    MONGO_DB_NAME: str

    # Milvus Connection
    MILVUS_HOST: str
    MILVUS_PORT: int

    # Additional API keys / secrets
    TAVILY_API_KEY: str
    OLLAMA_HOST: str

    # Log directory for file-based logging
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")

    # Updated for Pydantic v2: Use model_config instead of Config
    model_config = ConfigDict(
        extra="allow",  # Allows extra env variables
        env_file=".env",  # Reads environment variables from .env
        env_file_encoding="utf-8"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()