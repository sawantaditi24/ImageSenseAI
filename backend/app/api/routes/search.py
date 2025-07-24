from fastapi import APIRouter, Request
from app.utils.embeddings import get_text_embedding
from app.utils.faiss_index import search
import logging

router = APIRouter()

@router.post("/search")
async def search_screenshots(request: Request):
    """
    Search screenshots using semantic search
    """
    data = await request.json()
    query = data.get("query", "")
    if not query:
        print("[SEARCH] Empty query received.")
        return {"results": []}
    query_embedding = get_text_embedding(query)
    results = search(query_embedding, top_k=5)
    print(f"[SEARCH] Query: {query}")
    print(f"[SEARCH] Results: {results}")
    return {"results": results}

@router.get("/search/suggestions")
async def get_search_suggestions():
    """
    Get search suggestions based on user history
    """
    return {"message": "Search suggestions feature coming soon."} 
