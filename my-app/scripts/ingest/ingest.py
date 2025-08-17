#!/usr/bin/env python3
import os, io, re, sys, time, hashlib, urllib.parse, pathlib, textwrap
from datetime import datetime, timezone
import requests
import yaml
import trafilatura
from bs4 import BeautifulSoup
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / 'docs'
OUT_DIR = DOCS_DIR / 'sources'
ASSETS_DIR = DOCS_DIR / 'assets'
ALLOWED = ROOT / 'scripts' / 'ingest' / 'allowlist.txt'
REGISTRY = ROOT / 'scripts' / 'ingest' / 'registry.yaml'
UA = 'InternalLearningBot/1.0 (+https://example.internal)'

TEMPLATE = """---
{frontmatter}
---

# {title}

> Synthesis: TODO

{body}

{figures_section}
"""


def slugify(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip('/').replace('/', '-').strip('-') or 'index'
    host = parsed.netloc.replace(':', '-')
    return f"{host}-{path}"[:120]


def domain(url: str) -> str:
    return urllib.parse.urlparse(url).netloc


def fetch(url: str) -> str:
    resp = requests.get(url, headers={'User-Agent': UA}, timeout=30)
    resp.raise_for_status()
    return resp.text


def extract_main(html: str, base_url: str, selector: str | None) -> tuple[str, list[dict]]:
    soup = BeautifulSoup(html, 'lxml')
    main = soup.select_one(selector) if selector else None
    container = main or soup
    # Resolve image URLs and collect data
    images = []
    for img in container.find_all('img'):
        src = img.get('src') or img.get('data-src') or ''
        if not src:
            continue
        abs_url = urllib.parse.urljoin(base_url, src)
        alt = (img.get('alt') or '').strip()
        # try nearby figcaption
        caption = ''
        if img.parent and img.parent.name == 'figure':
            figcap = img.parent.find('figcaption')
            caption = (figcap.get_text(strip=True) if figcap else '')
        images.append({'url': abs_url, 'alt': alt, 'caption': caption})
        # Replace src to local placeholder path to be post-processed
        img['src'] = abs_url
    # Use trafilatura to get clean text/markdownish content
    extracted = trafilatura.extract(html, include_tables=True, include_formatting=True, url=base_url) or ''
    if not extracted:
        extracted = container.get_text("\n", strip=True)
    return extracted, images


def hash_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()[:12]


def download_and_process_image(url: str, dest_dir: pathlib.Path) -> tuple[str, int, int]:
    r = requests.get(url, headers={'User-Agent': UA}, timeout=30)
    r.raise_for_status()
    data = r.content
    h = hash_bytes(data)
    dest_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(io.BytesIO(data)).convert('RGB')
    out_path = dest_dir / f"{h}.webp"
    img.save(out_path, format='WEBP', quality=85, method=6)
    # Return path relative to DOCS root
    return str(out_path.relative_to(DOCS_DIR)), img.width, img.height


def build_frontmatter(meta: dict) -> str:
    # Order keys for readability
    ordered = {
        'title': meta.get('title'),
        'slug': meta.get('slug'),
        'tags': meta.get('tags', ['source']),
        'why_for_designers': meta.get('why_for_designers', 'TODO'),
        'bot_application': meta.get('bot_application', 'TODO'),
        'collaboration_prompts': meta.get('collaboration_prompts', ['What retrieval strategy applies here?']),
        'sources': meta.get('sources', []),
        'figures': meta.get('figures', []),
        'updated_at': meta.get('updated_at'),
        'completed': False,
    }
    return yaml.safe_dump(ordered, sort_keys=False).strip()


def ingest_one(url: str, registry: dict) -> None:
    d = domain(url)
    policy = registry.get('domains', {}).get(d, {}).get('policy', 'copy')
    selector = registry.get('domains', {}).get(d, {}).get('selectors', {}).get('main')
    html = fetch(url)
    body_text, images = extract_main(html, url, selector)

    slug = slugify(url)
    title = slug
    out_dir = OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    fig_entries = []
    asset_base = ASSETS_DIR / d / slug
    for img in images[:12]:  # cap to avoid huge pages
        try:
            rel_path_from_docs, w, h = download_and_process_image(img['url'], asset_base)
            # Compute path relative to docs/sources (where this markdown resides)
            md_rel_path = os.path.relpath((DOCS_DIR / rel_path_from_docs), start=OUT_DIR)
            fig_entries.append({
                'path': md_rel_path.replace('\\', '/'),
                'caption': img['caption'] or img['alt'] or 'Figure',
                'credit_name': d,
                'credit_url': img['url'],
                'license': 'internal-copy'
            })
        except Exception:
            continue

    meta = {
        'title': title,
        'slug': slug,
        'tags': ['source'],
        'sources': [{
            'url': url,
            'title': title,
            'author': '',
            'license': 'internal-copy',
            'retrieved_at': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
            'policy': policy,
        }],
        'figures': fig_entries,
        'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d')
    }

    fm = build_frontmatter(meta)
    body = body_text if body_text.strip() else f"(Content to be scraped from {url})"

    # Render figures inline
    figs_md = []
    for i, f in enumerate(fig_entries, start=1):
        figs_md.append(f"![{f['caption']}]({f['path']})\n<figcaption>Figure {i}. Credit: [{f['credit_name']}]({f['credit_url']}), License: {f['license']}</figcaption>")
    figures_section = "\n\n".join(figs_md)

    out_path = out_dir / f"{slug}.md"
    out_path.write_text(TEMPLATE.format(frontmatter=fm, title=title, body=body, figures_section=figures_section), encoding='utf-8')
    print(f"Wrote {out_path}")


def main():
    registry = yaml.safe_load(REGISTRY.read_text()) if REGISTRY.exists() else {}
    urls = [u.strip() for u in ALLOWED.read_text().splitlines() if u.strip() and not u.strip().startswith('#')]
    for u in urls:
        try:
            ingest_one(u, registry)
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed {u}: {e}")

if __name__ == '__main__':
    main()