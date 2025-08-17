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
			# Link using filename only so it works from sources/index.md
			items.append(f"- [{p.stem}]({p.name})")
		return "\n".join(items) if items else "(No sources ingested yet)"

	env.macro(list_sources)