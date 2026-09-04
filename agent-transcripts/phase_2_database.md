# Phase 2 Log & Agent Transcript: Database Schema & Models

## Execution Date
- Date: 2026-09-04

## Schema & Architecture Decisions
1. **Model Hierarchy**:
   - `SessionModel` (`sessions` table): Primary container for chat threads with UUID primary keys and `user_metadata` JSON support.
   - `MessageModel` (`messages` table): Stores exchange history with `session_id` foreign key, `role`, `content`, `sources` (JSON array), and `artifact` (JSON object). Configured with `ON DELETE CASCADE`.
   - `TranscriptModel` (`transcripts` table): Master document record for podcast/newsletter transcripts with metadata.
   - `TranscriptChunkModel` (`transcript_chunks` table): Text chunks linked to master transcript with `pgvector.sqlalchemy.Vector(384)` for semantic search embeddings.
2. **Session Isolation**:
   - Cascading relationship `cascade="all, delete-orphan"` guarantees that operations on sessions do not spill into adjacent user sessions.
3. **PGVector Initialization**:
   - `init_db.py` executes `CREATE EXTENSION IF NOT EXISTS vector;` on PostgreSQL connection before `create_all()`.
4. **Pydantic Validation**:
   - Built matching schemas (`SessionCreate`, `MessageCreate`, `TranscriptCreate`, `MessageSource`, `ArtifactPayload`) with `from_attributes=True` ORM mode for seamless serialization.
