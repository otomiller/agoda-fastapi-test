from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields

settings = Settings()