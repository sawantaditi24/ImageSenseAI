from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.routes import upload, search, storage

app = FastAPI(
    title="AI Screenshot Organizer",
    description="An intelligent screenshot management system with AI-powered categorization and search",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(storage.router, prefix="/api/v1", tags=["storage"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Screenshot Organizer is running"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Screenshot Organizer API",
        "version": "1.0.0",
        "docs": "/docs"
    } 
