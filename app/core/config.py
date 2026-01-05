from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = False
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
