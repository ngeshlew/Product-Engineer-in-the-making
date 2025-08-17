#!/usr/bin/env python3
import sys, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCES = ROOT / 'docs' / 'sources'

REQUIRED = [
    'title', 'slug', 'sources', 'updated_at'
]

OK = True
for p in sorted(SOURCES.glob('*.md')):
    if p.name == 'index.md':
        continue
    text = p.read_text(encoding='utf-8')
    if not text.startswith('---'):
        print(f"[lint] {p}: missing frontmatter")
        OK = False
        continue
    fm_end = text.find('\n---', 3)
    fm = yaml.safe_load(text[4:fm_end]) or {}
    for k in REQUIRED:
        if k not in fm:
            print(f"[lint] {p}: missing '{k}' in frontmatter")
            OK = False
    if 'figures' in fm:
        for i, f in enumerate(fm['figures'] or [], 1):
            for k in ['path', 'caption', 'credit_name', 'credit_url', 'license']:
                if k not in f:
                    print(f"[lint] {p}: figure {i} missing '{k}'")
                    OK = False

if not OK:
    sys.exit(1)
print("[lint] sources OK")