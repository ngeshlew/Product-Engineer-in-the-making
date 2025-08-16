---
title: Capstone Overview
slug: capstone
updated_at: "2025-08-16"
---

# Capstone: Customer‑Service Chatbot (Rivet)

Build a grounded, safe, and observable chatbot using Rivet, powered by RAG over this course content.

## Goals
- Deflection and resolution with citations
- Streaming UX and tool actions
- Safety (injection, PII), observability, and evals

## Development
- Build index: `python3 capstone/rag/index.py`
- Start API: `uvicorn capstone.server.main:app --reload --port 8080`