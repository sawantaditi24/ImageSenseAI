from fastapi import APIRouter

router = APIRouter()

@router.get("/storage/usage")
async def get_storage_usage():
    """
    Get storage usage statistics
    """
    return {"message": "Storage monitoring coming soon!"}

@router.post("/storage/cleanup")
async def cleanup_storage():
    """
    Clean up old files
    """
    return {"message": "Storage cleanup coming soon!"} 