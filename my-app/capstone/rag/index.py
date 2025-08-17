#!/usr/bin/env python3
import os, json, pathlib, re
from dataclasses import dataclass
from typing import List, Tuple

from rank_bm25 import BM25Okapi

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs'
SOURCES = DOCS / 'sources'
INDEX_DIR = ROOT / 'capstone' / 'rag' / 'index'
INDEX_DIR.mkdir(parents=True, exist_ok=True)

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
	# serialize tokenized corpus and doc meta
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
	return [meta[i] for i, _ in pairs]

if __name__ == '__main__':
	save_bm25()