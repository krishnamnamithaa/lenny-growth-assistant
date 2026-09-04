from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
from app.db import get_db
from app.rag import retrieve_relevant_chunks

router = APIRouter(tags=["Retrieval"])

class SearchRequest(BaseModel):
    query: str = Field(..., description="Semantic search query text", example="How do great teams improve user activation?")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of top relevant chunks to return (1-20)")
    min_similarity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Minimum similarity score threshold")

    @field_validator("query")
    @classmethod
    def validate_query_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query string cannot be empty or contain only whitespace.")
        return v.strip()

class SearchResultItem(BaseModel):
    chunk_id: str
    transcript_id: str
    content: str
    title: str
    source_url: Optional[str] = None
    speaker: Optional[str] = None
    similarity: float
    metadata: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    query: str
    results_count: int
    results: List[SearchResultItem]

@router.post("/retrieval/search", response_model=SearchResponse)
@router.post("/api/v1/retrieval/search", response_model=SearchResponse)
async def search_retrieval(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    try:
        chunks = retrieve_relevant_chunks(
            query=request.query,
            top_k=request.top_k,
            min_similarity=request.min_similarity,
            db=db
        )
        return SearchResponse(
            query=request.query,
            results_count=len(chunks),
            results=[SearchResultItem(**c) for c in chunks]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retrieval search operation failed: {str(e)}"
        )
