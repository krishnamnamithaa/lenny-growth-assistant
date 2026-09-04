# Phase 3 Log & Agent Transcript: RAG Ingestion & Vector Retrieval Pipeline

## Execution Date
- Date: 2026-09-05

## RAG Architecture Decisions
1. **Embedding Model**:
   - Standardized on `all-MiniLM-L6-v2` (`SentenceTransformer`) with 384-dimensional vector output.
   - Built pluggable `EmbeddingProvider` interface with fallback mock support for ultra-fast offline unit testing.
2. **Text Chunking Strategy**:
   - Recursive character text splitting configured with `chunk_size=500` characters and `overlap=100` characters to preserve semantic continuity across sentence boundaries.
   - Preserves speaker tags (`Lenny Rachitsky:`, `Guest:`) within metadata.
3. **Dual Search Engine (PGVector & SQLite Fallback)**:
   - **PostgreSQL / PGVector**: Native `<=>` cosine distance operator with SIMD vector acceleration.
   - **SQLite / In-Memory Fallback**: Vector dot product with NumPy normalized L2 norms for seamless local development and automated CI testing.
4. **Data Ingestion Pipeline & CLI**:
   - CLI tool (`python -m app.cli ingest`) to scan, validate JSON/Markdown transcripts in `data/transcripts/`, generate chunk embeddings, and upsert records into the database.
   - Idempotent upserts: Existing transcripts matching `source_url` are updated and stale chunks automatically replaced.
5. **API Endpoints**:
   - Exposed POST `/retrieval/search` and `/api/v1/retrieval/search` with Pydantic request validation (`top_k`, `min_similarity`, non-empty query).

## Verification
- Comprehensive test coverage with 30 passing Pytest unit and integration tests across chunking, embeddings, ingestion, models, and retrieval search API endpoints.
