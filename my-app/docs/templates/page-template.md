---
title: <Title>
slug: <slug>
tags: [concept]
difficulty: beginner
learning_objectives:
  - <objective 1>
  - <objective 2>
why_for_designers: |
  <why this matters>
bot_application: |
  <how this applies to the AI-powered bot>
collaboration_prompts:
  - <question to ask engineers>
sources:
  - url: <source url>
    title: <source title>
    author: <author>
    license: <license or internal-copy>
    retrieved_at: <YYYY-MM-DD>
    policy: copy
figures:
  - path: assets/<domain>/<slug>/<hash>.webp
    caption: <caption>
    credit_name: <site or author>
    credit_url: <link>
    license: <license>
updated_at: "2025-08-16"
completed: false
---

# <Title>

> Synthesis: <short synthesis>

## Why it’s important for designers to know

{{ page.meta.why_for_designers }}

## How this applies to the AI-powered bot

{{ page.meta.bot_application }}

## Collaboration prompts for engineers

- {{ page.meta.collaboration_prompts | join("\n- ") }}

## Sources

{% for s in page.meta.sources %}
- [{{ s.title or s.url }}]({{ s.url }}) — {{ s.license }} (retrieved {{ s.retrieved_at }})
{% endfor %}

## Figures

{% for f in page.meta.figures %}
![{{ f.caption }}]({{ f.path }})
<figcaption>Credit: [{{ f.credit_name }}]({{ f.credit_url }}), License: {{ f.license }}</figcaption>
{% endfor %}