#!/usr/bin/env python3
import os, sys, time, hashlib, urllib.parse, pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs' / 'sources'
ALLOWED = ROOT / 'scripts' / 'ingest' / 'allowlist.txt'

TEMPLATE = """---
title: {title}
slug: {slug}
tags: [source]
why_for_designers: |
  TODO
bot_application: |
  TODO
collaboration_prompts:
  - What retrieval strategy applies here?
sources:
  - url: {url}
    title: {title}
    author: 
    license: internal-copy
    retrieved_at: {retrieved}
    policy: copy
figures: []
updated_at: {retrieved}
completed: false
---

# {title}

> Synthesis: TODO

(Content to be scraped from {url})
"""

def slugify(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip('/').replace('/', '-').strip('-') or 'index'
    host = parsed.netloc.replace(':', '-')
    return f"{host}-{path}"[:120]


def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    urls = [u.strip() for u in ALLOWED.read_text().splitlines() if u.strip()]
    now = datetime.utcnow().strftime('%Y-%m-%d')
    for url in urls:
        slug = slugify(url)
        title = slug
        out = DOCS / f"{slug}.md"
        if out.exists():
            continue
        out.write_text(TEMPLATE.format(title=title, slug=slug, url=url, retrieved=now))
        print(f"Wrote {out}")

if __name__ == '__main__':
    main()