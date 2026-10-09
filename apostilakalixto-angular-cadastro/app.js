(function () {
  function codeBlock(file) {
    const wrap = document.createElement('div');
    wrap.className = 'cb';
    const head = document.createElement('div');
    head.className = 'cb-head';
    const name = document.createElement('span');
    name.textContent = file.nome;
    const btn = document.createElement('button');
    btn.className = 'copy';
    btn.type = 'button';
    btn.textContent = 'Copiar';
    btn.addEventListener('click', function () {
      const done = function () { btn.textContent = 'Copiado!'; setTimeout(function () { btn.textContent = 'Copiar'; }, 1400); };
      if (navigator.clipboard) navigator.clipboard.writeText(file.code).then(done, done);
    });
    head.append(name, btn);
    const pre = document.createElement('pre');
    const code = document.createElement('code');
    code.className = 'language-' + file.lang;
    code.textContent = file.code;
    pre.appendChild(code);
    wrap.append(head, pre);
    if (window.hljs && file.lang !== 'plaintext') hljs.highlightElement(code);
    return wrap;
  }

  /* Blocos de código nas seções */
  document.querySelectorAll('.code[data-ref]').forEach(function (el) {
    const parts = el.dataset.ref.split(':');
    const step = STEPS[parts[0]];
    if (!step) return;
    const file = step.files[Number(parts[1])];
    if (file) el.appendChild(codeBlock(file));
  });

  /* Painel lateral */
  const drawer = document.getElementById('drawer');
  const scrim = document.getElementById('scrim');
  const tabs = document.getElementById('dr-tabs');
  const area = document.getElementById('dr-code');
  let lastFocus = null;

  function showFile(step, i) {
    area.innerHTML = '';
    area.appendChild(codeBlock(step.files[i]));
    tabs.querySelectorAll('button').forEach(function (b, j) {
      b.classList.toggle('on', j === i);
      b.setAttribute('aria-selected', j === i);
    });
  }

  function open(id) {
    const step = STEPS[id];
    if (!step) return;
    document.getElementById('dr-phase').textContent = step.fase;
    document.getElementById('dr-title').textContent = step.titulo;
    document.getElementById('dr-desc').textContent = step.desc;
    document.getElementById('dr-go').href = '#' + id;
    tabs.innerHTML = '';
    step.files.forEach(function (f, i) {
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.textContent = f.nome.split('/').pop();
      b.title = f.nome;
      b.addEventListener('click', function () { showFile(step, i); });
      tabs.appendChild(b);
    });
    showFile(step, 0);
    lastFocus = document.activeElement;
    scrim.hidden = false;
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    document.getElementById('dr-close').focus();
  }

  function close() {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    scrim.hidden = true;
    if (lastFocus) lastFocus.focus();
  }

  document.querySelectorAll('[data-step]').forEach(function (n) {
    n.addEventListener('click', function () { open(n.dataset.step); });
  });
  document.getElementById('dr-close').addEventListener('click', close);
  document.getElementById('dr-go').addEventListener('click', close);
  scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  /* Destaca no sumário a seção visível */
  const links = document.querySelectorAll('.toc a');
  const obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id); });
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  document.querySelectorAll('main section[id]').forEach(function (s) { obs.observe(s); });
})();
