from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "ASPM - Vulnerability Management"
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://secure_dojo:secure_dojo_pass@localhost:5432/secure_coding_dojo",
        env="DATABASE_URL"
    )
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")

    class Config:
        env_file = ".env"

settings = Settings()
