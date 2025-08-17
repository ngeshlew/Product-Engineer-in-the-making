(function () {
  function canonicalKey() {
    const path = location.pathname.replace(/\/index\.html$/, '/');
    return `progress:${path}`;
  }

  function getProgress() {
    try { return JSON.parse(localStorage.getItem('progress:index') || '{}'); } catch { return {}; }
  }

  function setProgress(map) {
    localStorage.setItem('progress:index', JSON.stringify(map));
  }

  function updateHeader() {
    const map = getProgress();
    const done = Object.values(map).filter(Boolean).length;
    const total = Math.max(done, document.querySelectorAll('nav a.md-nav__link').length || 1);
    const ratio = total ? Math.min(1, done / total) : 0;
    let bar = document.getElementById('progress-bar');
    if (!bar) {
      bar = document.createElement('div');
      bar.id = 'progress-bar';
      Object.assign(bar.style, {position:'fixed', top:'0', left:'0', height:'3px', background:'#22c55e', width:'0%', zIndex:'9999'});
      document.body.appendChild(bar);
    }
    bar.style.width = `${Math.round(ratio*100)}%`;
  }

  function injectToggle() {
    const container = document.querySelector('header .md-header__inner') || document.body;
    const toggle = document.createElement('button');
    toggle.textContent = 'Mark complete';
    toggle.setAttribute('type', 'button');
    Object.assign(toggle.style, {marginLeft:'auto', background:'#111827', color:'#fff', border:'none', padding:'6px 10px', borderRadius:'6px', cursor:'pointer'});
    container && container.appendChild(toggle);

    const key = canonicalKey();
    const map = getProgress();
    const current = !!map[key];
    toggle.dataset.state = current ? 'done' : 'todo';
    toggle.textContent = current ? 'Completed ✓' : 'Mark complete';

    toggle.addEventListener('click', () => {
      const mapNow = getProgress();
      mapNow[key] = !(mapNow[key]);
      setProgress(mapNow);
      toggle.dataset.state = mapNow[key] ? 'done' : 'todo';
      toggle.textContent = mapNow[key] ? 'Completed ✓' : 'Mark complete';
      updateHeader();
      renderDashboard();
    });
  }

  function collectAllPages() {
    const links = Array.from(document.querySelectorAll('nav a.md-nav__link'));
    const pages = links.map(a => ({ href: a.getAttribute('href'), title: a.textContent.trim() })).filter(p => p.href && !p.href.startsWith('#'));
    // normalize hrefs to path-only keys
    pages.forEach(p => { p.key = `progress:${new URL(p.href, location.origin).pathname}`; });
    return pages;
  }

  function renderDashboard() {
    const isProgressPage = /\/progress\/?(index\.html)?$/.test(location.pathname);
    if (!isProgressPage) return;
    const container = document.querySelector('article.md-content__inner');
    if (!container) return;

    let panel = document.getElementById('progress-dashboard');
    if (!panel) {
      panel = document.createElement('div');
      panel.id = 'progress-dashboard';
      container.appendChild(panel);
    }

    const pages = collectAllPages();
    const map = getProgress();
    const done = pages.filter(p => map[p.key]);
    const todo = pages.filter(p => !map[p.key]);

    const exportBtn = `<button id="pg-export" style="margin-right:8px">Export JSON</button>`;
    const importBtn = `<label style="cursor:pointer"><input type="file" id="pg-import" accept="application/json" style="display:none">Import JSON</label>`;

    panel.innerHTML = `
      <h2>Overview</h2>
      <p>${done.length} / ${pages.length} completed</p>
      ${exportBtn}${importBtn}
      <div style="display:flex; gap:24px; flex-wrap:wrap; margin-top:12px">
        <div style="flex:1; min-width:260px">
          <h3>Completed</h3>
          <ul>${done.map(p => `<li><a href="${p.href}">${p.title}</a></li>`).join('') || '<li>(none)</li>'}</ul>
        </div>
        <div style="flex:1; min-width:260px">
          <h3>Remaining</h3>
          <ul>${todo.map(p => `<li><a href="${p.href}">${p.title}</a></li>`).join('') || '<li>(none)</li>'}</ul>
        </div>
      </div>
    `;

    const exportEl = document.getElementById('pg-export');
    const importEl = document.getElementById('pg-import');
    exportEl?.addEventListener('click', () => {
      const data = new Blob([JSON.stringify(getProgress(), null, 2)], {type: 'application/json'});
      const url = URL.createObjectURL(data);
      const a = document.createElement('a');
      a.href = url; a.download = 'progress.json'; a.click();
      URL.revokeObjectURL(url);
    });
    importEl?.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => { try { setProgress(JSON.parse(reader.result)); updateHeader(); renderDashboard(); } catch {} };
      reader.readAsText(file);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    injectToggle();
    updateHeader();
    renderDashboard();
  });
})();