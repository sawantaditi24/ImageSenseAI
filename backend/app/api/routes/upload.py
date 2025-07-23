from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import logging

from app.services.s3_service import S3Service
from app.core.config import settings
from app.utils.ocr import extract_text_from_image
from app.utils.categorize import categorize_text_with_llm
from app.models import Screenshot
from app.db import SessionLocal
from app.utils.embeddings import get_text_embedding
from app.utils.faiss_index import add_embedding

logger = logging.getLogger(__name__)
router = APIRouter()

def get_s3_service():
    return S3Service()

@router.post("/upload")
async def upload_screenshot(
    file: UploadFile = File(...),
    user_id: str = "default_user",  # TODO: Implement proper authentication
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    Upload a screenshot to S3 with optimization
    """
    db = SessionLocal()
    try:
        # Validate file type
        if not any(file.filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Validate file size
        file_size = 0
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        # Check user storage limits
        usage = s3_service.get_storage_usage(user_id)
        if usage['total_size_bytes'] + file_size > settings.MAX_STORAGE_PER_USER:
            raise HTTPException(
                status_code=400,
                detail="User storage limit exceeded"
            )
        
        # OCR: Extract text from the uploaded image
        text = extract_text_from_image(file_content)
        print(f"EXTRACTED TEXT: {text}")  # Debug print
        logger.info(f"Extracted text: {text}")

        # LLM-based categorization
        category = categorize_text_with_llm(text)
        print(f"CATEGORY: {category}")  # Debug print
        logger.info(f"Category: {category}")
        
        # Upload to S3
        result = s3_service.upload_screenshot(
            image_file=file_content,
            user_id=user_id,
            filename=file.filename
        )
        
        logger.info(f"Successfully uploaded file {file.filename} for user {user_id}")
        
        # Store screenshot info in the database
        screenshot = Screenshot(
            user_id=user_id,
            filename=file.filename,
            s3_key=result["s3_key"] if "s3_key" in result else result.get("key", file.filename),
            extracted_text=text,
            category=category
        )
        db.add(screenshot)
        db.commit()
        db.refresh(screenshot)

        # --- Add embedding to FAISS index ---
        embedding = get_text_embedding(text)
        # Compose metadata for FAISS (id, category, s3_key, filename, image_url)
        meta = {
            "id": screenshot.id,
            "category": category,
            "s3_key": screenshot.s3_key,
            "filename": file.filename,
            # Always use the public S3 thumbnail URL for imageUrl
            "imageUrl": result.get("thumbnail_url")
        }
        add_embedding(embedding, meta)
        # --- End FAISS addition ---
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Screenshot uploaded successfully",
                "data": result,
                "category": category,
                "db_id": screenshot.id
            }
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )
    finally:
        db.close()

@router.delete("/screenshots/{file_id}")
async def delete_screenshot(
    file_id: str,
    user_id: str = "default_user",  # TODO: Implement proper authentication
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    Delete a screenshot from S3
    """
    try:
        success = s3_service.delete_screenshot(user_id, file_id)
        
        if success:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Screenshot deleted successfully",
                    "file_id": file_id
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete screenshot"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )

@router.get("/upload/status")
async def get_upload_status(
    user_id: str = "default_user",  # TODO: Implement proper authentication
    s3_service: S3Service = Depends(get_s3_service)
):
    """
    Get upload status and storage usage
    """
    try:
        usage = s3_service.get_storage_usage(user_id)
        
        return {
            "user_id": user_id,
            "storage_usage": usage,
            "limits": {
                "max_storage_mb": settings.MAX_STORAGE_PER_USER / (1024 * 1024),
                "max_files": settings.MAX_FILES_PER_USER,
                "max_file_size_mb": settings.MAX_FILE_SIZE / (1024 * 1024)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get upload status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get upload status: {str(e)}"
        ) 

@router.get("/screenshots")
def list_screenshots(user_id: str = "default_user"):
    """
    List all screenshots for a user
    """
    from app.models import Screenshot
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        screenshots = db.query(Screenshot).filter(Screenshot.user_id == user_id).order_by(Screenshot.upload_time.desc()).all()
        result = [
            {
                "id": s.id,
                "filename": s.filename,
                "s3_key": s.s3_key,
                "extracted_text": s.extracted_text,
                "upload_time": s.upload_time.isoformat() if s.upload_time else None
            }
            for s in screenshots
        ]
        return {"screenshots": result}
    finally:
        db.close() 