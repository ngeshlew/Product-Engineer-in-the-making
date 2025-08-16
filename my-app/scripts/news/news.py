#!/usr/bin/env python3
import pathlib, datetime
import feedparser

ROOT = pathlib.Path(__file__).resolve().parents[2]
NEWS = ROOT / 'docs' / 'news.md'
FEEDS = [
  ('OpenAI', 'https://openai.com/blog/rss.xml'),
  ('Anthropic', 'https://www.anthropic.com/news/rss.xml'),
  ('Google AI', 'https://ai.googleblog.com/atom.xml'),
  ('DeepMind', 'https://deepmind.google/discover/feeds/blog.xml')
]

HEADER = """---
title: News
slug: news
updated_at: {date}
---

# News

Latest updates from OpenAI, Anthropic, Google/DeepMind, and more.
"""

def main():
    today = datetime.date.today().isoformat()
    parts = [HEADER.format(date=today)]
    for name, url in FEEDS:
        d = feedparser.parse(url)
        parts.append(f"\n## {name}\n")
        for entry in d.entries[:8]:
            title = getattr(entry, 'title', 'Untitled')
            link = getattr(entry, 'link', '')
            date = getattr(entry, 'published', '')
            parts.append(f"- [{title}]({link}) — {date}")
    NEWS.write_text("\n".join(parts))
    print(f"Wrote {NEWS}")

if __name__ == '__main__':
    main()