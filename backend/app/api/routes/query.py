from fastapi import APIRouter, Query
from app.utils.embeddings import get_text_embedding
from app.utils.faiss_index import search as faiss_search
from app.models import Screenshot
from app.db import SessionLocal
from app.core.config import settings

router = APIRouter()

CATEGORY_KEYWORDS = {
    "job post": ["job post", "hiring", "apply", "opening"],
    "resource/reference": ["resource", "reference", "guide", "tutorial", "learning"],
    "job search strategy": ["strategy", "tips", "advice", "how to", "journey"]
}

@router.get("/query")
def unified_query(query: str = Query(..., description="User query"), user_id: str = "default_user", top_k: int = 5):
    """
    Unified search endpoint: interprets query as category or semantic search and returns relevant screenshots.
    """
    db = SessionLocal()
    try:
        # Simple logic: if query matches a category keyword, filter by category
        query_lower = query.lower()
        matched_category = None
        for cat, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in query_lower for kw in keywords):
                matched_category = cat
                break
        
        if matched_category:
            # Category search
            screenshots = db.query(Screenshot).filter(Screenshot.user_id == user_id, Screenshot.category == matched_category).order_by(Screenshot.upload_time.desc()).limit(top_k).all()
            results = []
            for s in screenshots:
                image_url = f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{s.s3_key}"
                results.append({
                    "id": s.id,
                    "filename": s.filename,
                    "category": s.category,
                    "upload_time": s.upload_time.isoformat() if s.upload_time else None,
                    "image_url": image_url
                })
            return {"type": "category", "category": matched_category, "results": results}
        else:
            # Semantic search
            query_embedding = get_text_embedding(query)
            faiss_results = faiss_search(query_embedding, top_k=top_k)
            # Optionally, fetch more info from DB
            results = []
            for meta in faiss_results:
                s = db.query(Screenshot).filter(Screenshot.id == meta["id"]).first()
                if s:
                    image_url = f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{s.s3_key}"
                    results.append({
                        "id": s.id,
                        "filename": s.filename,
                        "category": s.category,
                        "upload_time": s.upload_time.isoformat() if s.upload_time else None,
                        "image_url": image_url
                    })
            return {"type": "semantic", "results": results}
    finally:
        db.close()
