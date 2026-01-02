from typing import List, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # App Config
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # AI Config
    ANTHROPIC_BASE_URL: str = "https://api.anthropic.com"
    ANTHROPIC_API_KEE: Optional[str] = None
    AI_MODEL: str = "claude-3-haiku-20240307"
    AI_MAX_TOKENS: int = 4096

    # Tool Config
    EMT4J_PATH: str = "~/.emt4j/emt4j-0.8.0"
    EMT4J_VERSION: str = "0.8.0"
    
    OPENREWRITE_MAVEN_PLUGIN_VERSION: str = "5.40.0"
    
    # Migration Defaults
    DEFAULT_FROM_VERSION: int = 8
    DEFAULT_TO_VERSION: int = 21

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
