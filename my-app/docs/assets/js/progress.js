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
    const total = document.querySelectorAll('article.md-content__inner h1').length ? 1 : 1;
    const done = Object.values(map).filter(Boolean).length;
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
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    injectToggle();
    updateHeader();
  });
})();