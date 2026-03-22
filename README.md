# ╔══════════════════════════════════════╗
# ║     SmartHire AI                     ║
# ║     Resume × Job Intelligence System ║
# ╚══════════════════════════════════════╝

![Status](https://img.shields.io/badge/Status-Industry--Grade-emerald)
![Tech](https://img.shields.io/badge/FastAPI-Pydantic-blue)
![Tech](https://img.shields.io/badge/React-Tailwind-cyan)
![AI](https://img.shields.io/badge/BERT-SentenceTransformer-indigo)
![AI](https://img.shields.io/badge/LLM-RAG--FAISS-orange)

### 🎯 Overview
SmartHire AI is an industry-grade recruitment intelligence platform that automates candidate matching using transformer-based embeddings (BERT) and identifies skill gaps with machine learning. It streamlines hiring by auto-generating role-specific interview questions using RAG (Retrieval-Augmented Generation) and presenting everything in a high-end, glassmorphic dashboard.

---

### 🏗️ Architecture Diagram

```ascii
[ Recruiter ] -> [ React Frontend ] -> [ FastAPI Gateway ]
                         |                    |
                  (File Uploads)        (Match Engine)
                         |                    |
                  [ Celery Worker ] <--- [ Redis Broker ]
                         |                    |
               [ BERT ] + [ FAISS ]     [ PostgreSQL DB ]
                         |                    |
             (Embedder + RAG Gen)      (Persisted Intel)
```

### 🤖 Core AI/ML Stack
*   **Embedder:** `all-MiniLM-L6-v2` (BERT) for dense vector representation of textual data.
*   **Matcher:** Cosine similarity engine for semantic (not keyword) matching.
*   **Analyzer:** Random Forest classifier for prioritizing skill gaps based on role importance.
*   **RAG Gen:** LangChain + FAISS + Hugging Face Hub (flan-t5) for targeted interview question synthesis.

### 🚀 Getting Started

#### Prerequisites
- Docker & Docker Compose
- Hugging Face API Key (for interview generation)

#### Setup
1. Clone the repository: `git clone <repo-url>`
2. Configure environment: `cp .env.example .env`
3. Spin up the cluster:
   ```bash
   docker-compose up --build
   ```
4. Access the apps once the services are running.

---

### 📂 Directory Structure
*   `backend/`: FastAPI source, ORM models, and async task definitions.
*   `frontend/`: React components with Tailwind CSS and Framer Motion.
*   `ml/`: The intelligence layer (Parsers, Embedders, Matchers, Gaps, RAG).
*   `data/`: Sample data for testing and demonstrations.

---

### ✅ Quality & Standards
- **Scalable:** Asynchronous resume processing using Celery + Redis.
- **Fast:** Redis-cached match results for identical queries.
- **Reliable:** Pydantic v2 validation for all API interactions.
- **Modern:** Premium UI/UX with glassmorphism and micro-animations.

---
