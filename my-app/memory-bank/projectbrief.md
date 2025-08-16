# Project Brief

## Purpose
Internal learning site to master AI/LLMs while building a customer‑service chatbot capstone (using Rivet). Content aggregates authoritative sources, stores local images with attributions, and teaches human‑centered AI product design.

## Outcomes
- Expert modules with consistent sections: Synthesis, Why for designers, How it applies to the bot, Collaboration prompts
- Ingestion pipeline: fetch pages, normalize to Markdown with frontmatter, download images (WebP) with captions/credits
- Progress tracking: page toggle (localStorage) + dashboard
- News aggregator: OpenAI/Anthropic/Google/DeepMind feeds to a News page
- Capstone: Rivet chatbot with RAG over course content, streaming, safety, and observability

## Scope (initial)
- Docs stack: MkDocs Material, macros, glightbox; directory `docs/`
- Structure: `docs/modules/*`, `docs/capstone/*`, `docs/perspectives/*`, `docs/competitors/*`, `docs/sources/*`, `docs/assets/*`
- Scripts: `scripts/ingest/*` (registry + allowlist + scraper), `scripts/news/news.py`
- Progress UI: `docs/assets/js/progress.js`, `docs/assets/css/progress.css`
- Config: `config.json`; critical code example at `src/critical.js` (!cc)

## Non‑Goals (for now)
- Public distribution or licensing beyond internal use
- Advanced diagram generation or heavy CI security gates

## Deliverables (Phase 1)
- Working site with nav and modules skeleton
- Ingested starter sources with local images + credits
- News page generated from RSS feeds
- Documented attribution in frontmatter/captions

## Success Measures
- Site builds green; nav and search functional
- ≥ 10 curated source pages ingested with images/credits
- Progress toggle visible and persists per page
- Capstone scaffold present; RAG indexing runs on docs

## Constraints & Assumptions
- Internal-only use; treat copied text/images as "internal-copy" with citation
- Prefer open/affordable LLMs for capstone; easy provider switching via env
