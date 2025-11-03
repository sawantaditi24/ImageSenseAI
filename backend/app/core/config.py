from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Screenshot Organizer"
    DEBUG: bool = False
    
    # CORS - can be set via environment variable as comma-separated string
    # Default includes production URLs
    ALLOWED_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://imagesenseai-1.onrender.com",
        "https://imagesenseai.onrender.com"
    ]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse comma-separated string or return list as-is"""
        if isinstance(v, str):
            # Parse comma-separated origins from env
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            return origins
        return v
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./screenshot_organizer.db"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-vision-preview"
    
    # Vector Database (Pinecone)
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    PINECONE_INDEX_NAME: str = "screenshot-embeddings"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".png", ".jpg", ".jpeg", ".webp"]
    
    # Storage Limits
    MAX_STORAGE_PER_USER: int = 100 * 1024 * 1024  # 100MB per user
    MAX_FILES_PER_USER: int = 1000
    
    # Image Processing
    THUMBNAIL_SIZE: tuple = (200, 150)
    MAX_IMAGE_SIZE: tuple = (1200, 800)
    IMAGE_QUALITY: int = 85
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 