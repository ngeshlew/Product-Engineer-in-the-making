#!/usr/bin/env python3
import os, json, pathlib
from dataclasses import dataclass
from typing import List

try:
	from sentence_transformers import SentenceTransformer
	exist_models = True
except Exception:
	exist_models = False

try:
	import faiss
	exist_faiss = True
except Exception:
	exist_faiss = False

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs'
SOURCES = DOCS / 'sources'
INDEX_DIR = ROOT / 'capstone' / 'rag' / 'index'
INDEX_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = os.environ.get('EMBED_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')

@dataclass
class Doc:
	path: str
	title: str
	text: str


def load_docs() -> List[Doc]:
	docs: List[Doc] = []
	for p in SOURCES.glob('*.md'):
		text = p.read_text(encoding='utf-8')
		if not text:
			continue
		docs.append(Doc(path=str(p), title=p.stem, text=text))
	return docs


def build_index():
	if not (exist_models and exist_faiss):
		print('Skipping index build; missing sentence-transformers or faiss')
		return
	model = SentenceTransformer(MODEL_NAME)
	docs = load_docs()
	texts = [d.text for d in docs]
	emb = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
	dim = emb.shape[1]
	index = faiss.IndexFlatIP(dim)
	faiss.normalize_L2(emb)
	index.add(emb)
	faiss.write_index(index, str(INDEX_DIR / 'docs.index'))
	with open(INDEX_DIR / 'meta.json', 'w') as f:
		json.dump([d.__dict__ for d in docs], f)
	print(f'Indexed {len(docs)} docs')

if __name__ == '__main__':
	build_index()