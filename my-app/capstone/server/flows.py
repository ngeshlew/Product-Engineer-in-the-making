import json, pathlib, re, uuid
from typing import Any, Dict, List, Tuple
from capstone.rag.index import query_bm25

ROOT = pathlib.Path(__file__).resolve().parents[2]
FLOWS = ROOT / 'capstone' / 'rivet' / 'flows.json'

SESSIONS: Dict[str, Dict[str, Any]] = {}


def get_session(session_id: str | None) -> Tuple[str, Dict[str, Any]]:
	if not session_id:
		session_id = uuid.uuid4().hex
	s = SESSIONS.setdefault(session_id, {"history": [], "state": {}})
	return session_id, s


def classify_intent(text: str) -> str:
	t = text.lower()
	if any(k in t for k in ['bill', 'invoice', 'price']):
		return 'billing'
	if any(k in t for k in ['error', 'bug', 'fail']):
		return 'technical'
	if any(k in t for k in ['agent', 'human', 'escalate', 'handoff']):
		return 'handoff'
	return 'faq'


def run_flow(query: str, session_id: str | None = None) -> Dict[str, Any]:
	flow = json.loads(FLOWS.read_text())['flows'][0]
	session_id, sess = get_session(session_id)

	# greet (implicit)
	intent = classify_intent(query)
	results = query_bm25(query, k=5)
	citations = [{
		'title': r['title'],
		'path': r['path']
	} for r in results]
	needs_handoff = (intent == 'handoff')
	answer = f"Intent: {intent}. Here's what I found with citations."
	msg = {
		'message': answer,
		'citations': citations,
		'needs_handoff': needs_handoff,
		'session_id': session_id
	}
	sess['history'].append({"user": query, "bot": msg})
	return msg