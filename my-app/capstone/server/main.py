#!/usr/bin/env python3
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import json, pathlib

app = FastAPI(title="Capstone API")
ROOT = pathlib.Path(__file__).resolve().parents[2]
INDEX_DIR = ROOT / 'capstone' / 'rag' / 'index'

@app.get('/health')
def health():
	return {'ok': True}

@app.get('/search')
def search(q: str = Query(..., min_length=2)):
	meta_p = INDEX_DIR / 'meta.json'
	if not meta_p.exists():
		return JSONResponse({'results': [], 'note': 'index not built'}, status_code=200)
	meta = json.loads(meta_p.read_text())
	# stub: return top N doc titles containing q
	hits = [m for m in meta if q.lower() in m['text'].lower()][:5]
	return {'results': [{'title': h['title'], 'path': h['path']} for h in hits]}