import logging
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import TranscriptChunkModel, TranscriptModel
from app.rag.embeddings import get_embedding_provider, EmbeddingProvider
from app.config import settings

logger = logging.getLogger(__name__)

DEFAULT_MIN_SIMILARITY = 0.35

def retrieve_relevant_chunks(
    query: str,
    top_k: int = 5,
    min_similarity: Optional[float] = None,
    db: Session = None,
    embedding_provider: EmbeddingProvider = None
) -> List[Dict[str, Any]]:
    """
    Retrieve top_k most relevant transcript chunks for a user query using pgvector similarity search.
    
    Args:
        query: Search query text string
        top_k: Number of top chunks to return (1 <= top_k <= 20)
        min_similarity: Minimum cosine similarity threshold (default 0.35)
        db: SQLAlchemy DB Session
        embedding_provider: Embedding provider instance
        
    Returns:
        List of dicts containing chunk content, title, speaker, source_url, and similarity score
    """
    if not query or not query.strip():
        logger.warning("Empty query provided to retrieve_relevant_chunks.")
        return []

    # Enforce safe top_k limits
    safe_top_k = max(1, min(int(top_k), 20))
    threshold = min_similarity if min_similarity is not None else getattr(settings, "RETRIEVAL_MIN_SIMILARITY", DEFAULT_MIN_SIMILARITY)

    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    if embedding_provider is None:
        embedding_provider = get_embedding_provider()

    try:
        query_vec = embedding_provider.embed_text(query.strip())
        
        # Determine database dialect
        is_postgres = "postgresql" in str(db.bind.url) if db.bind else False
        
        results = []
        if is_postgres:
            # Execute pgvector cosine distance search
            # Cosine distance operator in pgvector is <=>
            # Cosine similarity = 1 - (embedding <=> query_vec)
            query_sql = text("""
                SELECT 
                    c.id AS chunk_id,
                    c.transcript_id,
                    c.content,
                    c.chunk_index,
                    c.chunk_metadata,
                    t.title,
                    t.guest AS speaker,
                    t.url AS source_url,
                    1 - (c.embedding <=> :query_vec) AS similarity
                FROM transcript_chunks c
                JOIN transcripts t ON c.transcript_id = t.id
                WHERE c.embedding IS NOT NULL
                ORDER BY c.embedding <=> :query_vec ASC
                LIMIT :top_k
            """)
            
            # Format query_vec as vector string for pgvector SQL bind
            vec_str = "[" + ",".join(str(float(x)) for x in query_vec) + "]"
            rows = db.execute(query_sql, {"query_vec": vec_str, "top_k": safe_top_k}).fetchall()
            
            for row in rows:
                sim = float(row.similarity)
                if sim >= threshold:
                    results.append({
                        "chunk_id": str(row.chunk_id),
                        "transcript_id": str(row.transcript_id),
                        "content": row.content,
                        "title": row.title,
                        "source_url": row.source_url,
                        "speaker": row.speaker,
                        "similarity": round(sim, 4),
                        "metadata": row.chunk_metadata or {}
                    })
        else:
            # Fallback Python cosine distance calculation for SQLite / testing
            import numpy as np
            q_arr = np.array(query_vec)
            norm_q = np.linalg.norm(q_arr)
            
            chunks = db.query(TranscriptChunkModel, TranscriptModel)\
                .join(TranscriptModel, TranscriptChunkModel.transcript_id == TranscriptModel.id)\
                .all()
                
            scored_chunks = []
            for chunk, transcript in chunks:
                if chunk.embedding is not None:
                    c_arr = np.array(chunk.embedding)
                    norm_c = np.linalg.norm(c_arr)
                    if norm_q > 0 and norm_c > 0:
                        sim = float(np.dot(q_arr, c_arr) / (norm_q * norm_c))
                        if sim >= threshold:
                            scored_chunks.append({
                                "chunk_id": str(chunk.id),
                                "transcript_id": str(transcript.id),
                                "content": chunk.content,
                                "title": transcript.title,
                                "source_url": transcript.url,
                                "speaker": transcript.guest,
                                "similarity": round(sim, 4),
                                "metadata": chunk.chunk_metadata or {}
                            })
                            
            # Sort by similarity descending
            scored_chunks.sort(key=lambda x: x["similarity"], reverse=True)
            results = scored_chunks[:safe_top_k]

        logger.info(f"Retrieval search for query '{query[:30]}...' returned {len(results)} chunks (top_k={safe_top_k}, threshold={threshold})")
        return results

    except Exception as e:
        logger.error(f"Error during retrieval search: {e}")
        return []
    finally:
        if close_db:
            db.close()
