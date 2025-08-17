#!/usr/bin/env python3
import time, json, statistics
import requests

API = 'http://localhost:8080'
QUERIES = [
	{"q": "What is RAG?"},
	{"q": "How to stream model outputs?"},
	{"q": "What are agents?"}
]

def main():
	latencies = []
	covered = 0
	for i, item in enumerate(QUERIES, 1):
		q = item['q']
		start = time.time()
		r = requests.get(f"{API}/search", params={"q": q}, timeout=10)
		dur = (time.time() - start) * 1000
		latencies.append(dur)
		j = r.json()
		if j.get('results'):
			covered += 1
		print(f"[{i}] {q} => {len(j.get('results', []))} hits in {dur:.1f} ms")
	print("---")
	print(f"Coverage: {covered}/{len(QUERIES)}")
	if latencies:
		print(f"Latency (ms): p50={statistics.median(latencies):.1f}, max={max(latencies):.1f}")

if __name__ == '__main__':
	main()