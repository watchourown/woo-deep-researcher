# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    ENV_NAME: str = "local"
    API_TITLE: str = "MyApp"
    API_VERSION: str = "0.1.0"

    # This config allows pydantic to read from .env
    # and also accepts unknown env variables without error.
    model_config = ConfigDict(
        env_file=".env",
        extra="allow"  # Permits extra env variables
    )