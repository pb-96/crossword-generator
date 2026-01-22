from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    create_db: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()