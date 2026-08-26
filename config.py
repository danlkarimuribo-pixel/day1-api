from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./notes.db"

    class Config:
        env_file = ".env"


settings = Settings()
