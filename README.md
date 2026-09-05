# 🚀 Lenny Growth Assistant

<p align="center">
  <img src="https://img.shields.io/badge/AI-Growth%20Assistant-7C3AED?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/RAG-🧠-FF6B6B?style=flat-square" />
  <img src="https://img.shields.io/badge/Ollama-🦙-000000?style=flat-square" />
  <img src="https://img.shields.io/badge/Claude-☁️-D97706?style=flat-square" />
  <img src="https://img.shields.io/badge/pgvector-🔎-336791?style=flat-square" />
  <img src="https://img.shields.io/badge/Docker-🐳-2496ED?style=flat-square" />
</p>

<p align="center">
  <b>An AI-powered product & growth assistant grounded in Lenny's Podcast and Newsletter insights.</b>
</p>

---

## 🌟 What is Lenny Growth Assistant?

**Lenny Growth Assistant** is an AI-powered conversational assistant that helps users get practical advice about **product management, startups, and growth**.

Instead of giving generic AI answers, the assistant searches through **Lenny's Podcast and Newsletter transcripts**, retrieves relevant discussions, and uses that evidence to generate a grounded response.

### 💡 In simple words

> **Ask a product question → Search Lenny's knowledge → Get an AI answer → See the sources → Turn the idea into useful content.**

---

## ✨ Key Features

| 🔥 Feature              | 💡 What it does                                    |
| ----------------------- | -------------------------------------------------- |
| 🤖 **AI Assistant**     | Answers product & growth questions                 |
| 🔍 **RAG Search**       | Finds relevant Lenny transcript content            |
| 📚 **Source Grounding** | Shows which transcript supports the answer         |
| 💬 **Persistent Chats** | Maintains independent conversation sessions        |
| 🦙 **Local AI**         | Supports Ollama for local LLM execution            |
| ☁️ **Cloud AI**         | Supports Anthropic Claude                          |
| 🔄 **Model Switching**  | Change providers without changing application code |
| ✍️ **Ship 30 Skill**    | Converts discussions into structured articles      |
| 🎨 **Artifacts**        | Generates Markdown / HTML / CSS                    |
| 🔐 **Secure Rendering** | Treats generated HTML as untrusted                 |
| 🐳 **Docker Ready**     | Reproducible local setup                           |

---

# 🧠 How It Works

```text
                    👤 USER
                      │
                      ▼
             ┌─────────────────┐
             │   💬 Chat UI    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    ⚡ FastAPI   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   🤖 AI Agent   │
             └───────┬─────────┘
                     │
              ┌──────┴──────┐
              ▼             ▼
       🔍 RAG Retrieval   💬 Context
              │             │
              ▼             │
       📚 Lenny Transcripts │
              │             │
              └──────┬──────┘
                     ▼
             ┌─────────────────┐
             │ 🧠 LLM Provider │
             │                 │
             │ 🦙 Ollama       │
             │ ☁️ Claude       │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ ✨ Grounded     │
             │    Response     │
             └────────┬────────┘
                      │
               ┌──────┴───────┐
               ▼              ▼
            📚 Sources      🎨 Artifact
```

---

# 🛠️ Tech Stack

### 🎨 Frontend

![React](https://img.shields.io/badge/React-2026-61DAFB?style=flat-square\&logo=react\&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square\&logo=typescript\&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-Latest-646CFF?style=flat-square\&logo=vite\&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-3.x-06B6D4?style=flat-square\&logo=tailwindcss\&logoColor=white)

### ⚙️ Backend

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-High_Performance-009688?style=flat-square\&logo=fastapi\&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?style=flat-square)

### 🗄️ Data

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=flat-square\&logo=postgresql\&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-Vector_Search-336791?style=flat-square)

### 🤖 AI

![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=flat-square)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-D97706?style=flat-square)
![RAG](https://img.shields.io/badge/RAG-Grounded_AI-8B5CF6?style=flat-square)

### 🐳 Infrastructure

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square\&logo=docker\&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=flat-square\&logo=pytest\&logoColor=white)

---

# 🔎 RAG Knowledge Base

The assistant uses **Lenny's Podcast / Newsletter transcripts** as its knowledge source.

### 📥 Ingestion Pipeline

```text
📄 Transcript
     │
     ▼
🧹 Clean & Validate
     │
     ▼
✂️ Semantic Chunking
     │
     ▼
🧠 Generate Embeddings
     │
     ▼
🗄️ PostgreSQL + pgvector
     │
     ▼
🔍 Similarity Search
     │
     ▼
📚 Relevant Evidence
     │
     ▼
🤖 LLM Response
```

Each retrieved chunk maintains source metadata including:

* 📌 Transcript ID
* 📝 Transcript title
* 👤 Speaker
* 🔗 Source URL
* 🔎 Chunk ID
* 📊 Similarity score

This allows every grounded response to be traced back to its source.

---

# 🤖 AI Agent

The agent acts as the **brain of the application**.

It handles:

```text
User Question
      ↓
Understand Intent
      ↓
Retrieve Evidence
      ↓
Build Context
      ↓
Generate Response
      ↓
Attach Sources
```

The agent is designed to avoid hallucinating information that isn't supported by the transcript knowledge base.

If there isn't enough evidence:

> ⚠️ The assistant explicitly tells the user that the available material does not provide enough information.

---

# 🦙 Local + ☁️ Cloud LLM

The application supports two provider types.

### 🦙 Ollama

Used for the **mandatory local demo**.

Advantages:

* 🔒 Local execution
* 💰 No cloud inference cost
* 🌐 Works without external API calls
* 🧪 Easy local experimentation

### ☁️ Anthropic Claude

Used as the cloud LLM option.

Advantages:

* 🧠 Strong reasoning
* ✨ High-quality generation
* ☁️ Managed infrastructure

---

# 🔄 Provider Switching

No application code needs to change.

### Local Ollama

```env
LLM_PROVIDER=ollama
```

### Anthropic Claude

```env
LLM_PROVIDER=anthropic
```

The selected provider and model are exposed through application configuration/health information.

---

# ✍️ Ship 30 for 30

The project includes a dedicated **Ship 30 for 30 content skill**.

Example:

```text
User:
"Turn our discussion about user retention into a Ship 30 article."
```

The skill creates approximately **1,250 words** with:

* 🎣 Strong hook
* 📖 Clear narrative
* 🧩 Structured sections
* **Selective emphasis**
* 📌 Useful takeaways
* 📚 Transcript-grounded claims

The skill does not fabricate Lenny quotes, statistics, or sources.

---

# 🎨 Artifacts

The assistant can generate:

```text
📝 Markdown
🌐 HTML
🎨 CSS
```

Generated content can be displayed using the application's **Artifact Viewer**.

### 🔐 Security

Generated HTML is treated as **untrusted content**.

The viewer uses isolation/sanitization so generated content cannot freely interact with the main application.

---

# 💬 Conversation Sessions

Every conversation receives its own session ID.

```text
Session A
├── Question
├── Answer
└── Follow-up

Session B
├── Question
└── Answer
```

Session A's context is never mixed with Session B.

Conversations are persisted in PostgreSQL.

---

# 📁 Project Structure

```text
lenny-growth-assistant/
│
├── 🎨 frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── App.tsx
│
├── ⚙️ backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agent/
│   │   │   └── skills/
│   │   ├── rag/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── security/
│   │   ├── config.py
│   │   └── main.py
│   │
│   └── tests/
│
├── 📚 data/
│   └── transcripts/
│
├── 📖 docs/
│   ├── PRD.md
│   ├── architecture.md
│   └── design.md
│
├── 📝 agent-transcripts/
│
├── 🐳 docker-compose.yml
├── 🔐 .env.example
├── 🚫 .gitignore
└── 📘 README.md
```

---

# 🚀 Quick Start

## 1️⃣ Clone

```bash
git clone https://github.com/krishnamnamithaa/lenny-growth-assistant.git

cd lenny-growth-assistant
```

## 2️⃣ Configure Environment

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## 3️⃣ Configure Ollama

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=<your-model>
```

Pull the configured model:

```bash
ollama pull <your-model>
```

## 4️⃣ Start Application

```bash
docker compose up --build
```

That's it. 🚀

---

# 🧪 Testing

Run:

```bash
cd backend
pytest
```

Tests cover:

* ✅ API validation
* ✅ Session persistence
* ✅ Session isolation
* ✅ RAG retrieval
* ✅ Transcript ingestion
* ✅ Embeddings
* ✅ LLM providers
* ✅ Agent routing
* ✅ Grounding
* ✅ Source attribution
* ✅ Ship 30 skill
* ✅ Error handling

External LLM APIs are mocked during automated tests.

---

# 🔌 API Endpoints

| Method  | Endpoint            | Purpose                  |
| ------- | ------------------- | ------------------------ |
| 🟢 GET  | `/health`           | Application health       |
| 🔵 POST | `/sessions`         | Create session           |
| 🔵 POST | `/chat`             | Conversational AI        |
| 🔵 POST | `/retrieval/search` | Transcript search        |
| 🔵 POST | `/llm/test`         | Test LLM provider        |
| 🔵 POST | `/content/ship30`   | Generate Ship 30 article |
| 🔵 POST | `/artifacts`        | Generate artifact        |

---

# 🐳 Docker

Start:

```bash
docker compose up --build
```

Background:

```bash
docker compose up -d --build
```

Logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

---

# 🔐 Security

The project follows several security principles:

* 🔒 Secrets stored in environment variables
* 🚫 `.env` excluded from Git
* 🔑 API keys never returned by APIs
* 🛡️ Generated HTML treated as untrusted
* 🧠 Prompt injection defenses
* 🔐 Session isolation
* 🚨 Safe error responses
* 📝 Structured logging without secrets

---

# 📊 Project Status

| Component               | Status |
| ----------------------- | :----: |
| 🏗️ Project Foundation  |   🟢   |
| ⚡ FastAPI Backend       |   🟢   |
| 🗄️ PostgreSQL          |   🟢   |
| 💬 Session Persistence  |   🟢   |
| 🔎 RAG Knowledge Base   |   🟢   |
| 🦙 Ollama               |   🟢   |
| ☁️ Anthropic            |   🟢   |
| 🤖 Agent Layer          |   🟢   |
| 📚 Grounded Chat        |   🟢   |
| ✍️ Ship 30 Skill        |   🟢   |
| 🎨 Artifact Generation  |   🟡   |
| 🖥️ Artifact Viewer     |   🟡   |
| 🎯 Final UI Integration |   🟡   |
| 🧪 Final Verification   |   🟡   |

> 🟢 Completed & verified
> 🟡 In progress / final integration

---

# 🧠 Key Engineering Decisions

### 🔍 RAG instead of sending all transcripts

RAG keeps the context focused on relevant evidence and improves source traceability.

### 🦙 Local Ollama + ☁️ Cloud Claude

The abstraction layer allows the evaluator to compare local and cloud models without changing application code.

### 🗄️ PostgreSQL

PostgreSQL stores both application data and vector embeddings, keeping the architecture relatively simple.

### 🔐 Isolated Artifacts

Generated HTML is treated as untrusted because AI-generated code should not automatically receive unrestricted application privileges.

---

# 📚 Documentation

Detailed documentation is available in:

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

These include implementation decisions, failed attempts, corrections, and lessons learned.

---

# 🎥 Demo

The final demonstration covers:

1. 🚀 Product overview
2. 💬 Conversational Q&A
3. 🔎 RAG retrieval
4. 📚 Source grounding
5. 🦙 Local Ollama
6. 🔄 Provider configuration
7. ✍️ Ship 30 content generation
8. 🎨 Artifact generation
9. 🔐 Security approach
10. ⚖️ Key technical trade-off

---

# 🌟 Project Goal

> **Make Lenny's product and growth knowledge easy to explore, trust, and turn into useful content through an AI-powered conversational experience.**

---

<p align="center">

### 🚀 Built with AI • RAG • FastAPI • PostgreSQL • Ollama • Claude

**Lenny Growth Assistant**

</p>

