from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agoda API"
    PROJECT_VERSION: str = "1.0.0"
    API_KEY: str = "1234567890abcdef"  # Replace with your actual API key
    AVAILABILITY_API_URL: str = "https://api.example.com/availability"  # Replace with the actual API URL
    DATABASE_URL: str = "postgresql://postgres:9vtTWvyxyHCpEvq@10.0.255.250:5432/agoda"
    DB_NAME: str = "agoda"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "9vtTWvyxyHCpEvq"
    DB_HOST: str = "10.0.255.250"
    DB_PORT: str = "5432"
    REDIS_URL: str = "redis://10.0.255.234:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()