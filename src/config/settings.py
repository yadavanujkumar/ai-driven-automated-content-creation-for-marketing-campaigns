import os
from pydantic import BaseSettings, Field, AnyHttpUrl, validator
from typing import List, Optional

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = Field("AI-Driven Automated Content Creation", env="APP_NAME")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")  # development, staging, production
    DEBUG: bool = Field(True, env="DEBUG")

    # API keys and secrets
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(None, env="AWS_SECRET_ACCESS_KEY")

    # Database settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(10, env="DATABASE_POOL_SIZE")

    # Redis settings
    REDIS_URL: str = Field(..., env="REDIS_URL")
    REDIS_CACHE_TTL: int = Field(3600, env="REDIS_CACHE_TTL")  # Time-to-live for cache in seconds

    # Allowed origins for CORS
    ALLOWED_ORIGINS: List[AnyHttpUrl] = Field(
        ["http://localhost:3000"], env="ALLOWED_ORIGINS"
    )

    # Email settings
    SMTP_SERVER: Optional[str] = Field(None, env="SMTP_SERVER")
    SMTP_PORT: Optional[int] = Field(587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(None, env="SMTP_PASSWORD")
    EMAIL_FROM: Optional[str] = Field(None, env="EMAIL_FROM")

    # Logging settings
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    # Validator for ALLOWED_ORIGINS
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_allowed_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # Validator for environment
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        if v not in {"development", "staging", "production"}:
            raise ValueError("ENVIRONMENT must be one of 'development', 'staging', or 'production'")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instantiate the settings object
settings = Settings()