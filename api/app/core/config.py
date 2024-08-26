from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agoda API"
    PROJECT_VERSION: str = "1.0.0"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./test.db"

settings = Settings()