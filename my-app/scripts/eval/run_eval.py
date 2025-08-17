#!/usr/bin/env python3
import time, json, statistics, pathlib
import requests

API = 'http://localhost:8080'
DATASET = pathlib.Path(__file__).resolve().parent / 'dataset.json'


def main():
	cases = json.loads(DATASET.read_text())
	latencies = []
	covered = 0
	report = []
	for i, item in enumerate(cases, 1):
		q = item['q']
		exp = item.get('expect_keywords', [])
		start = time.time()
		r = requests.get(f"{API}/search", params={"q": q}, timeout=10)
		dur = (time.time() - start) * 1000
		latencies.append(dur)
		j = r.json()
		text = " ".join(hit['title'] for hit in j.get('results', []))
		hits = sum(1 for k in exp if k.lower() in text.lower())
		ok = hits > 0
		covered += 1 if ok else 0
		record = {"q": q, "latency_ms": dur, "keywords_hit": hits, "ok": ok}
		report.append(record)
		print(f"[{i}] {q} => {len(j.get('results', []))} hits, kw={hits} in {dur:.1f} ms")
	print("---")
	print(f"Coverage: {covered}/{len(cases)}")
	if latencies:
		print(f"Latency (ms): p50={statistics.median(latencies):.1f}, max={max(latencies):.1f}")
	(pathlib.Path(__file__).resolve().parent / 'report.json').write_text(json.dumps(report, indent=2))

if __name__ == '__main__':
	main()