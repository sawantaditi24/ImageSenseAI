from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Screenshot Organizer"
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
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