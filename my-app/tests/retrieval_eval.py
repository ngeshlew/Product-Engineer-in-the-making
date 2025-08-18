#!/usr/bin/env python3
import os, json, urllib.parse, urllib.request

def get_json(url: str):
	with urllib.request.urlopen(url, timeout=20) as r:
		return json.loads(r.read().decode('utf-8'))

def contains_any(results, substrings):
	joined = json.dumps(results).lower()
	return any(s.lower() in joined for s in substrings)

def main():
	base = os.environ.get('API_BASE', 'http://localhost:8080')
	cases = [
		{'q': 'stream outputs', 'expect_any': ['stream', 'langgraph']},
		{'q': 'multimodality', 'expect_any': ['multimodality', 'image']},
	]
	fails = []
	for c in cases:
		j = get_json(f"{base}/search?q={urllib.parse.quote(c['q'])}")
		ok = ('results' in j and len(j['results']) > 0 and contains_any(j['results'], c['expect_any']))
		if not ok:
			fails.append(c)
	print(json.dumps({'ok': len(fails) == 0, 'failed': fails}, ensure_ascii=False))
	if fails:
		raise SystemExit(1)

if __name__ == '__main__':
	main()

#!/usr/bin/env python3
import os, json, urllib.parse, urllib.request

def get_json(url: str):
	with urllib.request.urlopen(url, timeout=20) as r:
		return json.loads(r.read().decode('utf-8'))

def contains_any(results, substrings):
	joined = json.dumps(results).lower()
	return any(s.lower() in joined for s in substrings)

def main():
	base = os.environ.get('API_BASE', 'http://localhost:8080')
	cases = [
		{'q': 'stream outputs', 'expect_any': ['stream', 'langgraph']},
		{'q': 'multimodality', 'expect_any': ['multimodality', 'image']},
	]
	fails = []
	for c in cases:
		j = get_json(f"{base}/search?q={urllib.parse.quote(c['q'])}")
		ok = ('results' in j and len(j['results']) > 0 and contains_any(j['results'], c['expect_any']))
		if not ok:
			fails.append(c)
	print(json.dumps({'ok': len(fails) == 0, 'failed': fails}, ensure_ascii=False))
	if fails:
		raise SystemExit(1)

if __name__ == '__main__':
	main()

