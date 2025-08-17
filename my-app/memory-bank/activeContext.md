# Active Context

## Plan (2025-08-16T20:53:37+00:00)
- Target files: mkdocs.yml, docs/modules/*, docs/capstone/*, docs/perspectives/index.md, docs/competitors/*, docs/news.md
- Acceptance checks: Site builds, nav renders, search works

## Research (2025-08-16T20:55:11+00:00)
- Questions:
- Hypotheses:
- Sources to consult:
- Findings:
- Decisions:

## Innovate (2025-08-16T22:46:16+00:00)
- Ideas:
- Experiments to try:
- Design directions:
- Assumptions and risks:
- Metrics of success:

## Plan (2025-08-16T22:51:17+00:00)
- Target files: scripts/ingest/*, docs/sources/*, docs/assets/**, scripts/news/news.py, docs/assets/js/progress.js
- Acceptance checks: Ingestion writes Markdown with frontmatter and images; News page generates; Page toggle works

## Execute (2025-08-16)
- Implemented hybrid retrieval (BM25+embeddings) with cross-encoder reranker and quote-level citations
- Flow runner uses sqlite-backed sessions; actions wired (ticket create) with retries
- Added SSE endpoint for streaming; UI shows trace/latency chips
- Expanded eval and CI to start API, build index, and publish report
- OTLP endpoint configurable; ingestion adds snapshots, license normalization, and policy checks

## Risks
- Embedding/reranker models increase build time and CI cost
- Streaming remains SSE (WebSocket upgrade later)

## Protection
- Critical sections identified for protection. Annotate with markers per `.cursor/rules/code-protection.mdc` (e.g., `!cp`, `!cc`).
