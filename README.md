# Lenny Growth Assistant

An AI-powered conversational assistant that provides product and growth insights grounded in **Lenny’s Podcast and Newsletter transcripts**.

The goal is simple: users can ask product and growth questions, get evidence-based answers from Lenny's content, continue the conversation naturally, and turn useful discussions into structured written content.

---

## ✨ Features

* **Grounded Product & Growth Q&A** — Ask questions about product management, startups, growth, retention, prioritization, and related topics.
* **RAG Knowledge Base** — Retrieves relevant transcript chunks before generating an answer.
* **Source Traceability** — Answers include the transcript/source used to support the response.
* **Conversational Sessions** — Each chat maintains independent context and is persisted in PostgreSQL.
* **Flexible LLM Providers** — Supports local Ollama and cloud-based Anthropic Claude.
* **Provider Switching** — Switch the LLM provider through configuration without changing application code.
* **Ship 30 for 30 Skill** — Converts grounded discussions into approximately 1,250-word structured articles.
* **Artifact Generation** — Generates Markdown and HTML/CSS artifacts that can be rendered inside the application.
* **Safe Artifact Rendering** — Generated HTML is treated as untrusted and rendered using an isolated/sanitized approach.
* **FastAPI Backend** — Clear API contracts, validation, health checks, and structured errors.
* **Docker Compose** — Reproducible local development environment.
* **Automated Tests** — Tests for API, RAG, agent routing, persistence, LLM providers, and content generation.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────┐
│                 React Frontend              │
│                                             │
│       Chat        Sources      Artifacts    │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                 FastAPI API                 │
│                                             │
│ Sessions │ Chat │ Agent │ Content │ Artifacts│
└──────────────────────┬──────────────────────┘
                       │
              ┌────────┴─────────┐
              ▼                  ▼
        ┌───────────┐      ┌──────────────┐
        │ RAG Layer │      │ Agent Layer  │
        │           │      │              │
        │ Retrieval │      │ Routing      │
        │ Embeddings│      │ Skills       │
        └─────┬─────┘      └──────┬───────┘
              │                   │
              └─────────┬─────────┘
                        ▼
                ┌──────────────┐
                │ LLM Provider │
                │              │
                │ Ollama       │
                │ Anthropic    │
                └──────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
   PostgreSQL + pgvector          Transcript Data
```

---

## 🧰 Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

### Database

* PostgreSQL
* pgvector

### AI / RAG

* Ollama
* Anthropic Claude
* Sentence Transformers
* Vector similarity search

### Agent

* Anthropic Claude Agent SDK / configured agent framework
* Modular skills and routing

### Infrastructure

* Docker
* Docker Compose

### Testing

* Pytest
* Frontend testing tools

---

## 📁 Project Structure

```text
lenny-growth-assistant/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── sessions.py
│   │   │   ├── artifacts.py
│   │   │   └── content.py
│   │   │
│   │   ├── agent/
│   │   │   ├── assistant.py
│   │   │   ├── router.py
│   │   │   ├── context.py
│   │   │   ├── tools.py
│   │   │   └── skills/
│   │   │       └── ship_30.py
│   │   │
│   │   ├── rag/
│   │   │   ├── ingestion.py
│   │   │   ├── chunking.py
│   │   │   ├── embeddings.py
│   │   │   └── retrieval.py
│   │   │
│   │   ├── llm/
│   │   │   ├── base.py
│   │   │   ├── ollama.py
│   │   │   ├── anthropic.py
│   │   │   └── factory.py
│   │   │
│   │   ├── models/
│   │   ├── security/
│   │   ├── config.py
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Chat.tsx
│       │   ├── Sidebar.tsx
│       │   ├── Sources.tsx
│       │   └── ArtifactViewer.tsx
│       └── App.tsx
│
├── data/
│   └── transcripts/
│
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   └── design.md
│
├── agent-transcripts/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Install:

* Git
* Docker Desktop
* Python 3.11+
* Node.js 20+
* Ollama

Anthropic is optional for local development when using Ollama.

---

## 1. Clone the Repository

```bash
git clone https://github.com/krishnamnamithaa/lenny-growth-assistant.git
cd lenny-growth-assistant
```

---

## 2. Configure Environment Variables

Create `.env` from `.env.example`.

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Example configuration:

```env
LLM_PROVIDER=ollama

OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=<configured-local-model>

ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=<configured-claude-model>

LLM_TIMEOUT_SECONDS=60

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/lenny
```

Never commit `.env`.

---

# 🦙 Ollama Setup

Ollama is the required local LLM option for the demo.

Install Ollama and pull the model configured in `.env`.

```bash
ollama pull <configured-local-model>
```

Verify:

```bash
ollama list
```

When running through Docker Compose, the backend communicates with Ollama using:

```text
http://ollama:11434
```

---

# ☁️ Anthropic Setup

To use Anthropic Claude, configure:

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=<configured-claude-model>
```

The API key must remain in `.env`.

No API key is committed to GitHub.

---

# 🔄 Switching LLM Providers

The provider can be changed without modifying application code.

For local Ollama:

```env
LLM_PROVIDER=ollama
```

For Anthropic:

```env
LLM_PROVIDER=anthropic
```

The selected provider and model are exposed through the application's configuration/health information.

---

# 🧠 Knowledge Base

The assistant uses Lenny’s Podcast/Newsletter transcript material as its knowledge base.

### Ingestion Flow

```text
Transcript Files
      ↓
Validation & Cleaning
      ↓
Semantic Chunking
      ↓
Embeddings
      ↓
PostgreSQL + pgvector
      ↓
Similarity Retrieval
      ↓
Relevant Evidence
      ↓
LLM
```

Each chunk retains source metadata such as:

* Transcript ID
* Title
* Source URL
* Speaker
* Chunk ID
* Similarity score

This allows generated answers to be traced back to their supporting transcript sources.

---

# 🔎 RAG Retrieval

For every grounded question:

```text
User Question
     ↓
Embedding
     ↓
Vector Search
     ↓
Top Relevant Transcript Chunks
     ↓
Grounded Context
     ↓
LLM Response
```

If relevant evidence cannot be found, the assistant explicitly states that the available transcript material is insufficient rather than inventing an answer.

---

# 🤖 Conversational Agent

The agent is responsible for:

* Understanding the user's request
* Selecting the appropriate workflow
* Calling transcript retrieval
* Building grounded context
* Generating the response
* Maintaining session context
* Returning source references

Conversation history is stored in PostgreSQL.

Each session is isolated from other sessions.

---

# ✍️ Ship 30 for 30

The assistant includes a dedicated Ship 30 for 30 content skill.

Example:

```text
User:
"Turn our discussion about retention into a Ship 30 article."
```

The skill:

1. Retrieves relevant evidence.
2. Uses the current conversation context.
3. Generates approximately 1,250 words.
4. Creates a strong hook.
5. Uses clear headings and skimmable formatting.
6. Provides actionable takeaways.
7. Includes supporting transcript sources.

Unsupported topics are not fabricated.

---

# 🎨 Artifacts

The assistant can generate:

* Markdown
* HTML
* CSS

Generated artifacts can be displayed inside the application's Artifact Viewer.

Generated HTML is treated as **untrusted content**.

The application uses an isolation/sanitization strategy to prevent generated code from accessing the main application context.

---

# 🔐 Security

The project follows these principles:

* Secrets stored in environment variables.
* `.env` excluded from Git.
* API keys never returned by APIs.
* Generated HTML treated as untrusted.
* User input treated as untrusted.
* Retrieved transcript content treated as untrusted.
* Prompt injection protections applied at the agent layer.
* Session data isolated by session ID.
* Server errors are not exposed as raw stack traces.

---

# 🐳 Running with Docker

Build and start the application:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

---

# 🗄️ Database

PostgreSQL is used for:

* Sessions
* Messages
* User metadata
* Transcript metadata
* Transcript chunks
* Embeddings
* Source references

pgvector is used for semantic similarity search.

Database migrations are managed using Alembic.

---

# 🔌 API

Important endpoints include:

```text
GET  /health
POST /sessions
GET  /sessions/{session_id}
POST /chat
POST /retrieval/search
POST /llm/test
POST /content/ship30
POST /artifacts
```

Request and response models are validated using Pydantic.

---

# 🧪 Testing

Run backend tests:

```bash
cd backend
pytest
```

The tests cover critical functionality including:

* API validation
* Session persistence
* Session isolation
* RAG retrieval
* Transcript ingestion
* Embeddings
* LLM providers
* Agent routing
* Grounding
* Source attribution
* Ship 30 generation
* Failure handling

External API calls are mocked during automated tests.

---

# 🩺 Troubleshooting

### Ollama unavailable

Check:

```bash
ollama list
```

and verify the configured model exists.

If using Docker, ensure the backend uses:

```text
http://ollama:11434
```

rather than `localhost`.

---

### Anthropic authentication error

Verify:

```env
ANTHROPIC_API_KEY=...
```

and make sure the selected provider is:

```env
LLM_PROVIDER=anthropic
```

---

### Empty retrieval results

Verify:

1. Transcript files exist.
2. Ingestion completed successfully.
3. PostgreSQL is running.
4. pgvector is enabled.
5. Embeddings were generated.

---

### Database connection failure

Check:

```bash
docker compose ps
```

and:

```bash
docker compose logs postgres
```

---

### Model timeout

Check:

```env
LLM_TIMEOUT_SECONDS=60
```

Increase it only when necessary for slower local models.

---

# 📊 Key Technical Trade-offs

### Local vs Cloud LLM

**Ollama**

* No external API dependency
* Better privacy
* No per-request cloud cost
* Model quality may be lower
* Requires local compute

**Anthropic Claude**

* Stronger reasoning and generation quality
* Cloud infrastructure
* API cost
* Requires credentials and network connectivity

The provider abstraction allows the application to support both without changing application logic.

### RAG vs Full Transcript Context

RAG was selected because it:

* reduces unnecessary context
* improves source traceability
* scales better as transcript volume grows
* reduces LLM token usage

---

# 📚 Documentation

Additional documentation:

```text
docs/
├── PRD.md
├── architecture.md
└── design.md
```

Agent development records:

```text
agent-transcripts/
```

These documents explain implementation decisions, trade-offs, failed attempts, corrections, and operational handoff.

---

# 🎥 Demo

The final demo demonstrates:

1. The product problem.
2. The conversational assistant.
3. Grounded transcript retrieval.
4. Source references.
5. Local Ollama execution.
6. Follow-up conversation.
7. Ship 30 content generation.
8. Artifact generation/viewer.
9. One important technical trade-off.

---

# 📌 Project Status

| Component                     | Status |
| ----------------------------- | ------ |
| Project Foundation            | ✅      |
| FastAPI Backend               | ✅      |
| PostgreSQL                    | ✅      |
| Session Persistence           | ✅      |
| RAG Knowledge Base            | ✅      |
| Ollama                        | ✅      |
| Anthropic Provider            | ✅      |
| Agent Layer                   | ✅      |
| Grounded Chat                 | ✅      |
| Ship 30 Skill                 | ✅      |
| Artifact Generation           | 🚧     |
| Artifact Viewer               | 🚧     |
| Final UI Integration          | 🚧     |
| Final Deployment Verification | 🚧     |

---

## 🎯 Goal

The final product is designed to feel like a simple AI assistant from the user's perspective while internally combining:

**FastAPI + PostgreSQL + pgvector + RAG + Agent Architecture + Ollama + Claude + Content Skills + Secure Artifact Rendering.**

The user should not need to understand prompts, models, retrieval systems, or infrastructure to use it.
KRISHNAM NAMITHAA
