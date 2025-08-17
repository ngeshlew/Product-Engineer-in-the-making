import json, pathlib, re, uuid, time
from typing import Any, Dict, List, Tuple
from capstone.rag.index import hybrid_search
from capstone.server.store import get_session as db_get_session, save_session as db_save_session, create_ticket

ROOT = pathlib.Path(__file__).resolve().parents[2]
FLOWS = ROOT / 'capstone' / 'rivet' / 'flows.json'

def classify_intent(text: str) -> str:
	t = text.lower()
	if any(k in t for k in ['bill', 'invoice', 'price']):
		return 'billing'
	if any(k in t for k in ['error', 'bug', 'fail']):
		return 'technical'
	if any(k in t for k in ['agent', 'human', 'escalate', 'handoff']):
		return 'handoff'
	return 'faq'


def with_retries(fn, *args, **kwargs):
	for attempt in range(3):
		try:
			return fn(*args, **kwargs)
		except Exception:
			time.sleep(0.2 * (attempt+1))
	raise


def run_flow(query: str, session_id: str | None = None) -> Dict[str, Any]:
	flow = json.loads(FLOWS.read_text())['flows'][0]
	session_id = session_id or uuid.uuid4().hex
	sess = db_get_session(session_id)
	state = sess['state']
	history = sess['history']

	intent = classify_intent(query)
	results = hybrid_search(query, k=5)
	citations = [{
		'title': r['title'],
		'path': r['path'],
		'snippet': r.get('snippet', ''),
		'quote': r.get('quote', '')
	} for r in results]
	needs_handoff = (intent == 'handoff')
	if needs_handoff:
		state['handoff'] = True

	if intent == 'technical' and 'error' in query.lower():
		# create ticket in backend with retries
		ticket_id = with_retries(create_ticket, title=f"Auto ticket: {query[:40]}", body=query)
		state.setdefault('tickets', []).append(ticket_id)

	answer = f"Intent: {intent}. Here's what I found with citations."
	msg = {
		'message': answer,
		'citations': citations,
		'needs_handoff': needs_handoff,
		'session_id': session_id
	}
	history.append({"user": query, "bot": msg})
	db_save_session(session_id, state, history)
	return msg