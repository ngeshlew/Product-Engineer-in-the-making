import os
from pathlib import Path

def define_env(env):
	root = Path(env.project_dir)
	docs = root / 'docs'
	sources_dir = docs / 'sources'

	def list_sources():
		items = []
		for p in sorted(sources_dir.glob('*.md')):
			if p.name == 'index.md':
				continue
			rel = p.relative_to(docs)
			title = p.stem
			items.append(f"- [{title}]({rel.as_posix()})")
		return "\n".join(items) if items else "(No sources ingested yet)"

	env.macro(list_sources)