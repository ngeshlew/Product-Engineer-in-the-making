---
title: RAG & Knowledge
slug: capstone-rag
updated_at: "2025-08-16"
---

# RAG & Knowledge

Index course pages, store embeddings, re‑rank results, and cite sources inline.

## Environment

- `EMBED_MODEL` (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `RERANK_MODEL` (default: `cross-encoder/ms-marco-MiniLM-L-6-v2`)
- Optional tracing:
  - `OTEL_EXPORTER_OTLP_ENDPOINT`
  - `OTEL_EXPORTER_OTLP_HEADERS`

## Build Indexes

```bash
source .venv/bin/activate  # if using venv
npm run ingest              # fetch sources into docs/sources
python3 capstone/rag/index.py  # builds BM25 + embeddings
```

## API Search

- `/search` now uses hybrid retrieval (BM25 + embeddings) with CrossEncoder reranking and returns `quote` and `snippet` fields.
  - Configure models via env vars above.
  - Models are warmed on startup to reduce first‑query latency.

## Run

```bash
npm run api   # FastAPI on :8080
npm run dev   # mkdocs site on :8000
```