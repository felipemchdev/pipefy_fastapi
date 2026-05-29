from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Client Management and Pipefy Integration"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:////app/data/app.db"

    PIPEFY_API_URL: str = "https://api.pipefy.com/graphql"
    PIPEFY_API_TOKEN: str = ""

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
