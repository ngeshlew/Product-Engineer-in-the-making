---
title: Search
slug: search
---

# Search

Use the box below to query the course content. Results show titles and snippets. Click to open the source page.

<input id="q" placeholder="Search..." style="width:70%"> <button id="go">Go</button>

<div id="res"></div>

<script>
const API = (window.SEARCH_API || 'http://localhost:8080');
const q = document.getElementById('q');
const go = document.getElementById('go');
const res = document.getElementById('res');
async function run(){
	const v = q.value.trim(); if(!v) return;
	res.innerHTML = 'Searching...';
	try{
		const r = await fetch(`${API}/search?q=${encodeURIComponent(v)}`);
		const j = await r.json();
		res.innerHTML = (j.results||[]).map(h=>{
			const rel = (h.path||'').replace(/^.*docs\//,'');
			const sn = h.snippet ? `<div><small>${h.snippet}</small></div>` : '';
			return `<div style="margin:12px 0"><a href="/${rel}" target="_blank" rel="noopener">${h.title||rel}</a>${sn}</div>`;
		}).join('') || '<p><em>No results</em></p>';
	}catch(e){ res.textContent = 'Error: '+e.message; }
}
go.addEventListener('click', run);
q.addEventListener('keydown', (e)=>{ if(e.key==='Enter') run(); });
</script>
