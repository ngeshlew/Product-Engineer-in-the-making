import sqlite3, json, pathlib, threading
from typing import Any, Dict, Optional

ROOT = pathlib.Path(__file__).resolve().parents[2]
DB_PATH = ROOT / 'capstone' / 'server' / 'data.db'
_lock = threading.Lock()

def _conn():
	DB_PATH.parent.mkdir(parents=True, exist_ok=True)
	cx = sqlite3.connect(DB_PATH)
	cx.execute('CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, state TEXT, history TEXT)')
	cx.execute('CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)')
	return cx


def get_session(session_id: str) -> Dict[str, Any]:
	with _lock:
		cx = _conn()
		cur = cx.execute('SELECT state, history FROM sessions WHERE id=?', (session_id,))
		row = cur.fetchone()
		if not row:
			state = {}
			history = []
			cx.execute('INSERT INTO sessions(id, state, history) VALUES(?,?,?)', (session_id, json.dumps(state), json.dumps(history)))
			cx.commit()
			return {"state": state, "history": history}
		state = json.loads(row[0] or '{}')
		history = json.loads(row[1] or '[]')
		return {"state": state, "history": history}


def save_session(session_id: str, state: Dict[str, Any], history: Any) -> None:
	with _lock:
		cx = _conn()
		cx.execute('UPDATE sessions SET state=?, history=? WHERE id=?', (json.dumps(state), json.dumps(history), session_id))
		cx.commit()


def create_ticket(title: str, body: str) -> int:
	with _lock:
		cx = _conn()
		cur = cx.execute('INSERT INTO tickets(title, body) VALUES(?,?)', (title, body))
		cx.commit()
		return cur.lastrowid