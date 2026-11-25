/* BAD DECISIONS · shared site script */
(function () {
  'use strict';

  // ---------- CONFIG: paste the DICE link here when it exists ----------
  var DICE_URL = '';   // e.g. 'https://dice.fm/event/...'  (empty = buttons go to the Tickets section)

  var doc = document.documentElement;
  var ES = doc.lang === 'es';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function parse(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  var MON3 = ES ? ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'] : ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  var MONTHS = ES ? ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'] : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DOW = ES ? ['LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB', 'DOM'] : ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];
  var T = ES
    ? { opening: 'Noche de opening', every: 'Cada lunes', note: 'Lista gratis hasta la 01:30 · Entradas desde 11 €', list: 'Lista gratis', buy: 'Comprar entradas', prev: 'Mes anterior', next: 'Mes siguiente', copied: 'Enlace copiado. Contagia la mala influencia.', share: 'La peor decisión que tomarás en toda la semana.' }
    : { opening: 'Opening night', every: 'Every Monday', note: 'Free list until 01:30 · Tickets from 11 €', list: 'Join free list', buy: 'Buy tickets', prev: 'Previous month', next: 'Next month', copied: 'Link copied. Spread the bad influence.', share: "The worst decision you'll make all week." };

  // ---------- DICE links ----------
  var fallback = doc.getAttribute('data-tickets') || '#tickets';
  function diceHref() { return DICE_URL || fallback; }
  $$('[data-dice]').forEach(function (a) {
    a.href = diceHref();
    if (DICE_URL) { a.target = '_blank'; a.rel = 'noopener'; } else { a.removeAttribute('target'); a.removeAttribute('rel'); }
  });

  // ---------- events (single source: the JSON the build writes into every page) ----------
  var EVENTS = [];
  try { EVENTS = JSON.parse($('#bd-events').textContent).map(function (e) { e.date = parse(e.id); return e; }); } catch (e) {}
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var upcoming = EVENTS.filter(function (e) { return e.date >= today; });
  var NEXT = upcoming[0] || EVENTS[EVENTS.length - 1];
  function nice(d) { return DOW[0] + ' ' + d.getDate() + ' ' + MON3[d.getMonth()]; }
  if (NEXT) {
    $$('[data-next-date]').forEach(function (el) { el.textContent = nice(NEXT.date); });
    $$('[data-next-name]').forEach(function (el) { el.textContent = NEXT.special ? 'Opening' : 'Bad Monday'; });
  }
  $$('.ev[data-date]').forEach(function (el) { if (parse(el.getAttribute('data-date')) < today) el.classList.add('is-past'); });
  // home teaser: show only the next 3
  $$('[data-teaser]').forEach(function (list) {
    var shown = 0;
    $$('.ev', list).forEach(function (el) {
      var past = parse(el.getAttribute('data-date')) < today;
      el.hidden = past || shown >= 3; if (!el.hidden) shown++;
    });
  });

  // ---------- countdown (doors: midnight on Monday night) ----------
  (function () {
    var els = $$('[data-countdown]'); if (!els.length || !NEXT) return;
    var t = new Date(NEXT.date); t.setDate(t.getDate() + 1); t.setHours(0, 0, 0, 0);
    function tick() {
      var ms = Math.max(0, t - new Date());
      var v = { d: Math.floor(ms / 864e5), h: Math.floor(ms / 36e5) % 24, m: Math.floor(ms / 6e4) % 60, s: Math.floor(ms / 1e3) % 60 };
      els.forEach(function (el) { $$('[data-u]', el).forEach(function (u) { u.textContent = pad(v[u.getAttribute('data-u')]); }); });
    }
    tick(); setInterval(tick, 1000);
  })();

  // ---------- calendar ----------
  (function () {
    var root = $('#calendar'); if (!root || !EVENTS.length) return;
    var byId = {}; EVENTS.forEach(function (e) { byId[e.id] = e; });
    var cur = new Date(NEXT.date.getFullYear(), NEXT.date.getMonth(), 1);
    var min = new Date(EVENTS[0].date.getFullYear(), EVENTS[0].date.getMonth(), 1);
    var last = EVENTS[EVENTS.length - 1].date, max = new Date(last.getFullYear(), last.getMonth(), 1);
    var sel = NEXT.id;
    function iso(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
    function render() {
      var start = (cur.getDay() + 6) % 7, days = new Date(cur.getFullYear(), cur.getMonth() + 1, 0).getDate();
      var h = '<div class="cal-head"><button class="cal-nav" data-cal="-1" aria-label="' + T.prev + '"' + (cur <= min ? ' disabled' : '') + '>&larr;</button>' +
        '<h3 class="cal-title">' + MONTHS[cur.getMonth()] + ' <span>' + cur.getFullYear() + '</span></h3>' +
        '<button class="cal-nav" data-cal="1" aria-label="' + T.next + '"' + (cur >= max ? ' disabled' : '') + '>&rarr;</button></div><div class="cal-grid">';
      DOW.forEach(function (d, i) { h += '<div class="cal-dow' + (i ? '' : ' is-mon') + '">' + d + '</div>'; });
      for (var i = 0; i < start; i++) h += '<div class="cal-day is-empty"></div>';
      for (var d = 1; d <= days; d++) {
        var k = iso(new Date(cur.getFullYear(), cur.getMonth(), d)), e = byId[k];
        var cls = 'cal-day' + (e ? ' is-event' + (e.special ? ' is-special' : '') : '') + (k === sel ? ' is-selected' : '');
        h += e ? '<button class="' + cls + '" data-day="' + k + '" aria-label="' + esc(e.name + ' ' + k) + '">' + d + '</button>' : '<div class="' + cls + '">' + d + '</div>';
      }
      root.innerHTML = h + '</div>';
      detail(byId[sel]);
    }
    function detail(e) {
      var el = $('#event-detail'); if (!el || !e) return;
      var ext = DICE_URL ? ' target="_blank" rel="noopener"' : '';
      el.innerHTML = '<p class="det-kicker">' + (e.special ? T.opening : T.every) + ' · ' + nice(e.date) + ' · 00:00–05:00</p>' +
        '<h3 class="det-name">' + esc(e.name) + '</h3><p class="det-tag">' + esc(e.tag) + '</p>' +
        '<p class="det-note">' + T.note + '</p>' +
        '<div class="det-actions"><a class="btn btn-list" href="' + diceHref() + '"' + ext + '>' + T.list + '</a>' +
        '<a class="btn btn-ticket" href="' + diceHref() + '"' + ext + '>' + T.buy + '</a></div>';
    }
    root.addEventListener('click', function (ev) {
      var n = ev.target.closest('[data-cal]');
      if (n) { cur.setMonth(cur.getMonth() + +n.getAttribute('data-cal')); render(); return; }
      var d = ev.target.closest('[data-day]'); if (d) { sel = d.getAttribute('data-day'); render(); }
    });
    render();
  })();

  // ---------- share ----------
  var toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'bd-toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('show'); clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove('show'); }, 3200);
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-action="share"]'); if (!b) return; ev.preventDefault();
    var url = location.href.split('#')[0].split('?')[0];
    if (navigator.share) navigator.share({ title: 'BAD DECISIONS', text: T.share, url: url }).catch(function () {});
    else { try { navigator.clipboard.writeText(url); toast(T.copied); } catch (e) { toast(url); } }
  });

  // ---------- reveal on scroll ----------
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .12 });
    $$('.reveal').forEach(function (el) { io.observe(el); });
    doc.classList.add('js-reveal');
  }

  // ---------- nav background on scroll ----------
  var nav = $('#nav');
  function onScroll() { nav.classList.toggle('solid', window.scrollY > 40); }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // ---------- 3D coin (home only) ----------
  var coin = $('#coin'), scene = $('#scene');
  if (coin && scene) {
    var TH = 26, N = 24;
    coin.querySelector('.front').style.transform = 'translateZ(' + (TH / 2 + 1) + 'px)';
    coin.querySelector('.back').style.transform = 'rotateY(180deg) translateZ(' + (TH / 2 + 1) + 'px)';
    for (var i = 0; i < N; i++) { var d = document.createElement('div'); d.className = 'edge'; d.style.transform = 'translateZ(' + (-TH / 2 + i * TH / (N - 1)) + 'px) scale(.995)'; coin.insertBefore(d, coin.firstChild); }
    var rotY = -25, rotX = 8, vel = reduce ? 0 : .6, tiltX = 0, tiltY = 0, dragging = false, lastX = 0, lastT = 0, t = 0;
    (function frame() {
      t += 1;
      if (!dragging) { rotY += vel; vel += ((reduce ? 0 : .6) - vel) * .02; }
      var bob = reduce ? 0 : Math.sin(t / 40) * 8;
      coin.style.transform = 'translateY(' + bob + 'px) rotateX(' + (rotX + tiltX) + 'deg) rotateY(' + (rotY + tiltY) + 'deg)';
      requestAnimationFrame(frame);
    })();
    scene.addEventListener('pointerdown', function (e) { dragging = true; lastX = e.clientX; lastT = performance.now(); scene.setPointerCapture(e.pointerId); });
    scene.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var now = performance.now(), dx = e.clientX - lastX;
      rotY += dx * .6; vel = dx * .6 / Math.max(1, (now - lastT) / 16); lastX = e.clientX; lastT = now;
    });
    var up = function () { dragging = false; vel = Math.max(-25, Math.min(25, vel)); };
    scene.addEventListener('pointerup', up); scene.addEventListener('pointercancel', up);
    if (!reduce) addEventListener('mousemove', function (e) { tiltY = (e.clientX / innerWidth - .5) * 20; tiltX = -(e.clientY / innerHeight - .5) * 16; });
  }

  // ---------- 3D tilt on cards ----------
  if (!reduce) $$('.tilt').forEach(function (el) {
    el.style.transformStyle = 'preserve-3d';
    el.addEventListener('mousemove', function (e) {
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.transform = 'perspective(800px) rotateY(' + (x * 12) + 'deg) rotateX(' + (-y * 12) + 'deg) translateZ(6px)';
    });
    el.addEventListener('mouseleave', function () { el.style.transform = ''; });
  });
})();
