from fastapi import APIRouter

router = APIRouter()

@router.get("/storage/usage")
async def get_storage_usage():
    """
    Get storage usage statistics
    """
    return {"message": "Storage monitoring functionality coming soon"}

@router.post("/storage/cleanup")
async def cleanup_storage():
    """
    Clean up old files
    """
    return {"message": "Storage cleanup functionality coming soon"} 
