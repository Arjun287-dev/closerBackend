from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Closer"
    API_V1_STR: str = "/api/v1"
    
    # DB
    DATABASE_URL: str = "postgresql+asyncpg://closer_user:closer_password@localhost:5432/closer_db"
    
    # JWT Auth
    JWT_SECRET: str = "supersecretkey_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
