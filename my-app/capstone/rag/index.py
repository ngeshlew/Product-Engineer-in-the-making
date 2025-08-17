#!/usr/bin/env python3
import os, json, pathlib, re
from dataclasses import dataclass
from typing import List, Tuple

from rank_bm25 import BM25Okapi
import numpy as np
try:
	import faiss
	from sentence_transformers import SentenceTransformer, util as st_util
	HAS_EMB = True
except Exception:
	HAS_EMB = False

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs'
SOURCES = DOCS / 'sources'
INDEX_DIR = ROOT / 'capstone' / 'rag' / 'index'
INDEX_DIR.mkdir(parents=True, exist_ok=True)

EMB_MODEL = os.getenv('EMBED_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')

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


def build_bm25(docs: List[Doc]) -> Tuple[BM25Okapi, List[Doc]]:
	tokenized = [re.findall(r"\w+", d.text.lower()) for d in docs]
	bm25 = BM25Okapi(tokenized)
	return bm25, docs


def save_bm25():
	docs = load_docs()
	bm25, docs = build_bm25(docs)
	corpus = [re.findall(r"\w+", d.text.lower()) for d in docs]
	(INDEX_DIR / 'bm25.json').write_text(json.dumps(corpus))
	(INDEX_DIR / 'meta.json').write_text(json.dumps([d.__dict__ for d in docs]))
	print(f'BM25 indexed {len(docs)} docs')


def query_bm25(q: str, k: int = 5) -> List[dict]:
	meta_p = INDEX_DIR / 'meta.json'
	corp_p = INDEX_DIR / 'bm25.json'
	if not (meta_p.exists() and corp_p.exists()):
		return []
	meta = json.loads(meta_p.read_text())
	corpus = json.loads(corp_p.read_text())
	bm25 = BM25Okapi(corpus)
	tokens = re.findall(r"\w+", q.lower())
	scores = bm25.get_scores(tokens)
	pairs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
	res = [meta[i] for i, _ in pairs]
	for r in res:
		r['snippet'] = make_snippet(r['text'], q)
	return res


def make_snippet(text: str, q: str, size: int = 280) -> str:
	qt = re.escape(q.split()[0]) if q.split() else ''
	m = re.search(qt, text, flags=re.IGNORECASE) if qt else None
	start = max(0, (m.start() if m else 0) - 40)
	return text[start:start+size].replace('\n', ' ')

# Embeddings

def save_embeddings():
	if not HAS_EMB:
		print('Embeddings not available')
		return
	docs = load_docs()
	model = SentenceTransformer(EMB_MODEL)
	texts = [d.text for d in docs]
	emb = model.encode(texts, convert_to_numpy=True, show_progress_bar=True, normalize_embeddings=True)
	dim = emb.shape[1]
	index = faiss.IndexFlatIP(dim)
	index.add(emb)
	faiss.write_index(index, str(INDEX_DIR / 'emb.index'))
	(INDEX_DIR / 'meta.json').write_text(json.dumps([d.__dict__ for d in docs]))
	print(f'Embeddings indexed {len(docs)} docs')


def query_embeddings(q: str, k: int = 5) -> List[dict]:
	if not HAS_EMB:
		return []
	meta_p = INDEX_DIR / 'meta.json'
	idx_p = INDEX_DIR / 'emb.index'
	if not (meta_p.exists() and idx_p.exists()):
		return []
	meta = json.loads(meta_p.read_text())
	model = SentenceTransformer(EMB_MODEL)
	qv = model.encode([q], convert_to_numpy=True, normalize_embeddings=True)
	index = faiss.read_index(str(idx_p))
	scores, ids = index.search(qv, k)
	ids = ids[0].tolist()
	res = [meta[i] for i in ids if i >= 0]
	for r in res:
		r['snippet'] = make_snippet(r['text'], q)
	return res


def hybrid_search(q: str, k: int = 5) -> List[dict]:
	bm = query_bm25(q, k)
	em = query_embeddings(q, k)
	seen = {}
	combined = []
	for r in bm + em:
		key = r['path']
		if key in seen:
			continue
		seen[key] = True
		combined.append(r)
	return combined[:k]

if __name__ == '__main__':
	save_bm25()
	save_embeddings()