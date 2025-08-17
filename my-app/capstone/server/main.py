#!/usr/bin/env python3
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, pathlib, time, asyncio
from typing import Any

from capstone.rag.index import query_bm25, save_bm25
from capstone.server.otel import setup_tracing
from capstone.server.flows import run_flow

app = FastAPI(title="Capstone API")
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
ROOT = pathlib.Path(__file__).resolve().parents[2]
INDEX_DIR = ROOT / 'capstone' / 'rag' / 'index'

TRACING = setup_tracing()

@app.middleware("http")
async def log_requests(request: Request, call_next):
	start = time.time()
	response = await call_next(request)
	dur = int((time.time() - start) * 1000)
	path = request.url.path
	traceparent = request.headers.get('traceparent')
	if traceparent:
		response.headers['traceparent'] = traceparent
	print(f"[req] {request.method} {path} {dur}ms {response.status_code}")
	return response

@app.get('/health')
def health():
	return {'ok': True}

@app.post('/build-index')
def build_index():
	save_bm25()
	return {'ok': True}

@app.get('/search')
def search(q: str = Query(..., min_length=2), request: Request = None):
	hits = query_bm25(q, k=5)
	return {'results': [{'title': h['title'], 'path': h['path'], 'quote': h.get('quote'), 'snippet': h.get('snippet')} for h in hits], 'traceparent': request.headers.get('traceparent') if request else None}

@app.post('/chat')
def chat(payload: dict[str, Any], request: Request = None):
	q = payload.get('message', '')
	session_id = payload.get('session_id')
	msg = run_flow(q, session_id=session_id)
	msg['traceparent'] = request.headers.get('traceparent') if request else None
	msg['model'] = 'miniLM+bm25'
	msg['cost'] = 0
	return msg

@app.post('/chat/stream')
async def chat_stream(payload: dict[str, Any], request: Request = None):
	q = payload.get('message', '')
	session_id = payload.get('session_id')
	msg = run_flow(q, session_id=session_id)
	traceparent = request.headers.get('traceparent') if request else None
	async def gen():
		content = msg['message']
		for i in range(1, len(content)+1):
			chunk = content[:i]
			yield f"data: {json.dumps({'delta': chunk[-1], 'traceparent': traceparent, 'model':'miniLM+bm25','cost':0})}\n\n"
			await asyncio.sleep(0.01)
		# final payload with citations
		yield f"data: {json.dumps({'done': True, 'citations': msg['citations']})}\n\n"
	return StreamingResponse(gen(), media_type='text/event-stream')