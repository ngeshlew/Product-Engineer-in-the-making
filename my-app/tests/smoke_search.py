#!/usr/bin/env python3
import os, json
import urllib.request

def get(url: str):
	with urllib.request.urlopen(url, timeout=15) as r:
		return r.read().decode('utf-8')

def main():
	base = os.environ.get('API_BASE', 'http://localhost:8080')
	# health
	h = get(f"{base}/health")
	assert 'ok' in h, f"health failed: {h}"
	# search
	s = get(f"{base}/search?q=stream")
	j = json.loads(s)
	assert 'results' in j and isinstance(j['results'], list), 'missing results'
	assert len(j['results']) > 0, 'no search results'
	first = j['results'][0]
	assert 'title' in first and 'path' in first, 'missing fields'
	print(json.dumps({'ok': True, 'first_title': first['title']}))

if __name__ == '__main__':
	main()

