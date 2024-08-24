from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agoda API"
    PROJECT_VERSION: str = "1.0.0"
    API_KEY: str = "1234567890abcdef"  # Replace with your actual API key
    AVAILABILITY_API_URL: str = "https://api.example.com/availability"  # Replace with the actual API URL
    DATABASE_URL: str = "postgresql://postgres:9vtTWvyxyHCpEvq@10.0.255.250:5432/agoda"

    class Config:
        env_file = ".env"

settings = Settings()