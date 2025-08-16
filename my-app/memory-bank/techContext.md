# Technical Context

## Technology Stack
- Docs: MkDocs Material (Python), mkdocs-macros, mkdocs-glightbox
- Ingestion: Python (requests, trafilatura, BeautifulSoup, lxml, Pillow)
- News: Python (feedparser)
- Capstone (planned): Rivet for conversation flows; RAG index with FAISS or LanceDB; FastAPI/Express for server; Tailwind+Radix or Material 3 for UI

## Environment
- Local dev with Python venv; internal site only
- Assets stored under `docs/assets/` (WebP), pages under `docs/`

## Dependencies / Libraries
- requests, trafilatura, bs4, lxml, Pillow, feedparser, PyYAML

## Performance & Metrics
- Docs build time < 2s on small sets; images compressed to WebP (quality 85)

## Build & CI
- Future: GitHub Actions to run ingestion (check mode), build docs, link/license check, deploy preview; scheduled news refresh

## Security & Secrets
- No external secrets required yet; treat copied content as internal; maintain attributions in frontmatter and captions

## Design System Implementation (capstone UI)
- Tailwind + Radix (shadcn/ui) for fast accessible chat UI; design tokens to enable theming
- Alternative: Material 3 for enterprise consistency
