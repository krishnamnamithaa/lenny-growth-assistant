import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.db import SessionLocal, init_db
from app.models import TranscriptModel, TranscriptChunkModel
from app.rag.chunking import clean_transcript_text, chunk_transcript
from app.rag.embeddings import get_embedding_provider, EmbeddingProvider
from app.config import settings

logger = logging.getLogger(__name__)

class TranscriptValidationError(Exception):
    pass

def validate_transcript_record(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input transcript payload."""
    if not isinstance(data, dict):
        raise TranscriptValidationError("Record is not a valid JSON object.")
        
    title = data.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        raise TranscriptValidationError("Missing or invalid required field 'title'.")
        
    content = data.get("content")
    if not content or not isinstance(content, str) or not content.strip():
        raise TranscriptValidationError("Missing or invalid required field 'content'.")
        
    return {
        "title": title.strip(),
        "content": content.strip(),
        "source_url": data.get("source_url") or data.get("url"),
        "speaker": data.get("speaker") or data.get("guest"),
        "published_at": data.get("published_at"),
        "description": data.get("description"),
        "transcript_type": data.get("transcript_type", "podcast"),
        "metadata": data.get("metadata", {})
    }

def ingest_transcript_data(
    db: Session,
    validated_data: Dict[str, Any],
    embedding_provider: EmbeddingProvider,
    chunk_size: int = None,
    chunk_overlap: int = None
) -> Dict[str, Any]:
    """
    Ingest a single validated transcript record into PostgreSQL/pgvector.
    
    Handles creation, update, text cleaning, chunking, batch embeddings, and chunk persistence safely.
    """
    c_size = chunk_size or settings.CHUNK_SIZE
    c_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    title = validated_data["title"]
    source_url = validated_data["source_url"]
    speaker = validated_data["speaker"]
    raw_content = validated_data["content"]
    cleaned_content = clean_transcript_text(raw_content)

    # Check for existing transcript record by source_url or title
    existing = None
    if source_url:
        existing = db.query(TranscriptModel).filter(TranscriptModel.url == source_url).first()
    if not existing:
        existing = db.query(TranscriptModel).filter(TranscriptModel.title == title).first()

    # Use database transaction
    try:
        if existing:
            transcript = existing
            transcript.title = title
            transcript.guest = speaker
            transcript.url = source_url
            transcript.raw_content = cleaned_content
            transcript.extra_metadata = {
                "published_at": validated_data.get("published_at"),
                "description": validated_data.get("description")
            }
            # Delete stale chunks cleanly
            db.query(TranscriptChunkModel).filter(
                TranscriptChunkModel.transcript_id == transcript.id
            ).delete(synchronize_session=False)
            db.flush()
        else:
            transcript = TranscriptModel(
                title=title,
                guest=speaker,
                url=source_url,
                transcript_type=validated_data.get("transcript_type", "podcast"),
                raw_content=cleaned_content,
                extra_metadata={
                    "published_at": validated_data.get("published_at"),
                    "description": validated_data.get("description")
                }
            )
            db.add(transcript)
            db.flush() # Populate transcript.id

        # Chunk content
        raw_chunks = chunk_transcript(
            cleaned_content,
            chunk_size=c_size,
            chunk_overlap=c_overlap,
            default_speaker=speaker
        )

        if not raw_chunks:
            db.commit()
            return {"transcript_id": transcript.id, "chunks_created": 0}

        # Generate batch embeddings
        chunk_texts = [c["content"] for c in raw_chunks]
        embeddings = embedding_provider.embed_batch(chunk_texts)

        # Store chunks with vectors
        db_chunks = []
        for idx, (chunk_data, vec) in enumerate(zip(raw_chunks, embeddings)):
            chunk_obj = TranscriptChunkModel(
                transcript_id=transcript.id,
                chunk_index=chunk_data["chunk_index"],
                content=chunk_data["content"],
                embedding=vec,
                start_char=chunk_data.get("start_char"),
                end_char=chunk_data.get("end_char"),
                chunk_metadata={
                    **(chunk_data.get("metadata") or {}),
                    "title": title,
                    "guest": speaker,
                    "source_url": source_url
                }
            )
            db_chunks.append(chunk_obj)

        db.add_all(db_chunks)
        db.commit()

        return {
            "transcript_id": transcript.id,
            "title": title,
            "chunks_created": len(db_chunks)
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction rollback during transcript ingestion '{title}': {e}")
        raise e

def run_ingestion_pipeline(
    transcripts_dir: str = "data/transcripts",
    db: Session = None,
    embedding_provider: EmbeddingProvider = None
) -> Dict[str, int]:
    """
    Scan transcripts directory and ingest all JSON/JSONL files.
    
    Returns statistical summary: found, processed, chunks_created, skipped, errors.
    """
    stats = {
        "found": 0,
        "processed": 0,
        "chunks_created": 0,
        "skipped": 0,
        "errors": 0
    }

    dir_path = Path(transcripts_dir)
    if not dir_path.exists():
        fallback_path = Path("..") / transcripts_dir
        if fallback_path.exists():
            dir_path = fallback_path

    if not dir_path.exists():
        logger.warning(f"Transcripts directory '{transcripts_dir}' does not exist.")
        return stats

    files = list(dir_path.glob("*.json")) + list(dir_path.glob("*.jsonl"))
    stats["found"] = len(files)

    if stats["found"] == 0:
        logger.info(f"No JSON/JSONL files found in '{transcripts_dir}'.")
        return stats

    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    if embedding_provider is None:
        embedding_provider = get_embedding_provider()

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if file_path.suffix == ".jsonl":
                    records = [json.loads(line) for line in f if line.strip()]
                else:
                    data = json.load(f)
                    records = data if isinstance(data, list) else [data]

            for record in records:
                try:
                    validated = validate_transcript_record(record)
                    res = ingest_transcript_data(db, validated, embedding_provider)
                    stats["processed"] += 1
                    stats["chunks_created"] += res["chunks_created"]
                    logger.info(f"Successfully ingested '{validated['title']}' ({res['chunks_created']} chunks)")
                except TranscriptValidationError as ve:
                    stats["skipped"] += 1
                    logger.warning(f"Skipped invalid transcript in {file_path.name}: {ve}")
                except Exception as ex:
                    stats["errors"] += 1
                    logger.error(f"Error ingesting transcript in {file_path.name}: {ex}")

        except Exception as file_err:
            stats["errors"] += 1
            logger.error(f"Failed to read file {file_path.name}: {file_err}")

    if close_db:
        db.close()

    return stats
