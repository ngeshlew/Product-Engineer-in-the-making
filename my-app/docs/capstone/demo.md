---
title: Capstone Demo
slug: capstone-demo
updated_at: "2025-08-16"
---

# Capstone Demo

Start the API locally and point your client to it.

```bash
uvicorn capstone.server.main:app --reload --port 8080
```

Health check: `GET http://localhost:8080/health`

Search (stub): `GET http://localhost:8080/search?q=rag`
