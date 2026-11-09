/* ===== 반도체·식각 자습 교재 — 공통 기능 =====
   의존성 없음. 각 기능은 독립된 함수로, 페이지에 해당 요소가 없으면 그냥 건너뛴다. */
(function () {
  'use strict';

  /* ---------- 저장소: 막혀 있어도 동작하도록 ---------- */
  var store = {
    get: function (k, d) {
      try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; }
    },
    set: function (k, v) {
      try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* 저장 불가: 무시 */ }
    }
  };
  window.StudyStore = store;

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var chapterId = document.body.dataset.chapter || null;
  var book = window.BOOK || { chapters: [], parts: [] };

  /* ---------- 테마 ---------- */
  function initTheme() {
    var btn = $('#theme-toggle');
    if (!btn) return;
    function current() {
      var t = document.documentElement.dataset.theme;
      if (t) return t;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    function label() { btn.title = current() === 'dark' ? '라이트 모드로' : '다크 모드로'; }
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem('theme', next); } catch (e) {}
      label();
    });
    label();
  }

  /* ---------- 챕터 이전/다음 ---------- */
  function initChapterNav() {
    var nav = $('.chapter-nav');
    if (!nav || !chapterId) return;
    var list = book.chapters.filter(function (c) { return c.file; });
    var i = list.findIndex(function (c) { return c.id === chapterId; });
    function link(c, dir) {
      if (!c) return '<span>' + (dir < 0 ? '‹' : '›') + '</span>';
      return '<a href="' + c.file + '" title="' + c.no + ' ' + c.title + '">' +
        (dir < 0 ? '‹ <span class="label">' + c.no + '</span>' : '<span class="label">' + c.no + '</span> ›') + '</a>';
    }
    nav.innerHTML = link(list[i - 1], -1) + '<a href="index.html" title="전체 목차">목차</a>' + link(list[i + 1], 1);
  }

  /* ---------- 사이드바 목차 + 현재 위치 ---------- */
  function headingText(h) {
    return h.textContent.replace(/\s+/g, ' ').trim();
  }
  function initToc() {
    var toc = $('.toc');
    var article = $('.chapter');
    if (!toc || !article) return;
    // 인쇄용 퀴즈 해설 제목은 화면 목차에서 뺀다 (화면에서는 해설이 문항 아래에 붙는다)
    var heads = $$('h2[id], h3[id]', article).filter(function (h) { return !h.closest('.quiz-static'); });
    var html = '<ol>';
    heads.forEach(function (h) {
      html += '<li class="' + (h.tagName === 'H2' ? 'lv2' : 'lv3') + '" data-for="' + h.id + '">' +
        '<a href="#' + h.id + '"><span class="toc-text">' + h.innerHTML.replace(/<br\s*\/?>/g, ' ') + '</span></a></li>';
    });
    toc.innerHTML = html + '</ol>';

    var links = {};
    $$('a', toc).forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });

    var active = null;
    function update() {
      var y = window.scrollY + 90;
      var cur = heads[0];
      for (var k = 0; k < heads.length; k++) {
        if (heads[k].offsetTop <= y) cur = heads[k]; else break;
      }
      if (cur && cur.id !== active) {
        if (active && links[active]) links[active].classList.remove('active');
        active = cur.id;
        var a = links[active];
        if (a) {
          a.classList.add('active');
          var sb = $('#sidebar');
          var r = a.getBoundingClientRect(), sr = sb.getBoundingClientRect();
          if (r.top < sr.top + 20 || r.bottom > sr.bottom - 20) sb.scrollTop += r.top - sr.top - sr.height / 3;
        }
      }
    }
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; update(); }); }
    }, { passive: true });
    window.addEventListener('resize', update);
    update();
    window.StudyToc = { update: update };

    // 모바일: 목차 열고 닫기
    var btn = $('#toc-toggle'), scrim = $('.scrim');
    function setOpen(open) {
      document.body.classList.toggle('toc-open', open);
      if (btn) btn.setAttribute('aria-expanded', String(open));
      if (scrim) scrim.hidden = !open;
    }
    if (btn) btn.addEventListener('click', function () { setOpen(!document.body.classList.contains('toc-open')); });
    if (scrim) scrim.addEventListener('click', function () { setOpen(false); });
    toc.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
  }

  /* ---------- 읽기 진행률 바 ---------- */
  function initProgress() {
    var bar = $('.progress-bar');
    if (!bar) return;
    function update() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? Math.min(100, window.scrollY / max * 100) : 0) + '%';
    }
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- 그림: <img> SVG를 인라인으로 (폰트·다크 모드용) ---------- */
  function inlineFigures() {
    var imgs = $$('.fig-media img[src$=".svg"]');
    return Promise.all(imgs.map(function (img) {
      return fetch(img.getAttribute('src'))
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(function (txt) {
          var doc = new DOMParser().parseFromString(txt, 'image/svg+xml');
          var svg = doc.documentElement;
          if (svg.nodeName !== 'svg') return;
          svg.setAttribute('role', 'img');
          svg.setAttribute('aria-label', img.alt);
          svg.removeAttribute('width');
          svg.removeAttribute('height');
          img.replaceWith(document.importNode(svg, true));
        })
        .catch(function () { /* file:// 등에서는 <img> 그대로 둔다 */ });
    })).then(function () { if (window.StudyToc) window.StudyToc.update(); });
  }

  /* ---------- 라이트박스 ---------- */
  function initLightbox() {
    var figs = $$('.fig-media');
    if (!figs.length) return;
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.hidden = true;
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.innerHTML = '<button class="icon-btn lightbox-close" aria-label="닫기">✕</button>' +
      '<div class="lightbox-inner"><div class="lightbox-media"></div><div class="lightbox-cap"></div></div>';
    document.body.appendChild(box);
    var media = $('.lightbox-media', box), cap = $('.lightbox-cap', box), lastFocus = null;

    function open(fig) {
      media.innerHTML = '';
      Array.prototype.forEach.call(fig.children, function (n) { media.appendChild(n.cloneNode(true)); });
      var fc = fig.parentNode.querySelector('figcaption');
      cap.innerHTML = fc ? fc.innerHTML : '';
      lastFocus = document.activeElement;
      box.hidden = false;
      $('.lightbox-close', box).focus();
    }
    function close() {
      box.hidden = true;
      media.innerHTML = '';
      if (lastFocus) lastFocus.focus();
    }
    figs.forEach(function (f) {
      f.tabIndex = 0;
      f.setAttribute('aria-label', '그림 크게 보기');
      f.addEventListener('click', function () { open(f); });
      f.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(f); } });
    });
    box.addEventListener('click', function (e) { if (!e.target.closest('.lightbox-media, .lightbox-cap')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });
  }

  /* ---------- 표지: 챕터 카드 ---------- */
  function initHome() {
    var root = $('#chapter-cards');
    if (!root) return;
    var html = '';
    book.parts.forEach(function (p) {
      var chs = book.chapters.filter(function (c) { return c.part === p.id; });
      if (!chs.length) return;
      html += '<section class="part-block"><div class="part-label">' + p.label + '</div><div class="cards">';
      chs.forEach(function (c) {
        var body = '<span class="no">' + c.no + '</span><span class="ttl">' + c.title + '</span>' +
          '<span class="desc">' + (c.desc || '') + '</span>';
        if (c.file) {
          html += '<a class="card" href="' + c.file + '" data-chapter="' + c.id + '">' + body +
            '<span class="meta">' + progressMeta(c.id) + '</span></a>';
        } else {
          html += '<div class="card soon">' + body + '<span class="meta">준비 중</span></div>';
        }
      });
      html += '</div></section>';
    });
    root.innerHTML = html;
  }
  function progressMeta(id) {
    var p = store.get('progress:' + id, null);
    if (!p || !p.total) return '<span>아직 읽지 않음</span>';
    var n = (p.read || []).length, pct = Math.round(n / p.total * 100);
    return '<span class="bar"><i style="width:' + pct + '%"></i></span><span>' + n + ' / ' + p.total + '절 읽음</span>';
  }

  /* ---------- OX 퀴즈: 다 풀면 자동 채점, 해설은 문항 아래 ---------- */
  function initQuiz() {
    var app = $('.quiz-app[data-quiz]');
    if (!app) return;
    fetch(app.dataset.quiz)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) { renderQuiz(app, data); })
      .catch(function () { /* 불러오지 못하면 원래 표 + 해설을 그대로 보여 준다 */ });
  }

  function renderQuiz(app, data) {
    var items = data.items;
    var key = 'quiz:' + data.chapter;
    var st = store.get(key, null) || {};
    st.answers = st.answers || {};        // { 문항번호: 'O' | 'X' }
    st.graded = !!st.graded;              // 채점 끝났는지
    st.retry = st.retry || null;          // 다시 푸는 중인 문항 번호 목록
    function save() { store.set(key, st); }

    function secTitle(id) {
      var h = document.getElementById(id);
      return h ? headingText(h) : id;
    }
    function active() {                   // 지금 풀어야 하는 문항
      return st.retry ? items.filter(function (q) { return st.retry.indexOf(q.no) >= 0; }) : items;
    }

    var html = '<div class="quiz-bar">' +
      '<div class="quiz-status"></div>' +
      '<div class="quiz-actions">' +
      '<button type="button" class="btn quiz-retry">틀린 문항만 다시 풀기</button>' +
      '<button type="button" class="btn ghost quiz-reset">초기화</button></div></div>' +
      '<ol class="quiz-list">';
    items.forEach(function (q) {
      html += '<li class="qz" data-no="' + q.no + '">' +
        '<div class="qz-q"><span class="qz-no">' + q.no + '</span><div class="qz-stmt">' + q.statement + '</div></div>' +
        '<div class="qz-btns" role="group" aria-label="' + q.no + '번 답">' +
        '<button type="button" class="ox" data-v="O" aria-pressed="false">O</button>' +
        '<button type="button" class="ox" data-v="X" aria-pressed="false">X</button></div>' +
        '<div class="qz-res" hidden><div class="qz-verdict"></div>' +
        '<div class="qz-expl">' + q.explanation + '</div>' +
        '<a class="qz-link" href="#' + q.section + '">관련 절: ' + secTitle(q.section) + ' →</a></div>' +
        '</li>';
    });
    html += '</ol>';
    app.innerHTML = html;
    app.hidden = false;
    var stat = $('.quiz-static');
    if (stat) stat.classList.add('replaced');
    document.body.classList.add('quiz-on');

    var status = $('.quiz-status', app), btnRetry = $('.quiz-retry', app);

    function draw() {
      var act = active(), done = act.filter(function (q) { return st.answers[q.no]; }).length;
      var correct = items.filter(function (q) { return st.answers[q.no] === q.answer; }).length;
      items.forEach(function (q) {
        var li = $('.qz[data-no="' + q.no + '"]', app);
        var a = st.answers[q.no];
        var inPlay = act.indexOf(q) >= 0;
        var show = st.graded && !st.retry;
        li.hidden = !!st.retry && !inPlay;
        li.classList.toggle('ok', show && a === q.answer);
        li.classList.toggle('bad', show && a !== q.answer);
        $$('.ox', li).forEach(function (b) {
          var v = b.dataset.v;
          b.setAttribute('aria-pressed', String(a === v));
          b.disabled = show;
          b.classList.toggle('is-answer', show && v === q.answer);
        });
        var res = $('.qz-res', li);
        res.hidden = !show;
        if (show) {
          $('.qz-verdict', li).innerHTML = a === q.answer
            ? '<b>맞음</b> · 정답 ' + q.answer
            : '<b>틀림</b> · 고른 답 ' + a + ' / 정답 ' + q.answer;
        }
      });
      if (st.graded && !st.retry) {
        var wrong = items.length - correct;
        status.innerHTML = '<span class="quiz-score">' + correct + ' / ' + items.length + '</span>' +
          (wrong ? '틀린 문항 ' + wrong + '개 · 해설과 관련 절을 확인하자' : '모두 맞았다!');
        btnRetry.hidden = !wrong;
      } else {
        status.innerHTML = (st.retry ? '틀린 문항 다시 풀기 · ' : '') +
          '<b>' + done + ' / ' + act.length + '</b> 답함' +
          '<span class="quiz-hint">' + (done < act.length ? ' · 다 풀면 자동으로 채점된다' : '') + '</span>';
        btnRetry.hidden = true;
      }
      app.classList.toggle('graded', st.graded && !st.retry);
    }

    app.addEventListener('click', function (e) {
      var b = e.target.closest('.ox');
      if (!b || b.disabled) return;
      var no = +b.closest('.qz').dataset.no;
      st.answers[no] = b.dataset.v;
      var act = active();
      var allDone = act.every(function (q) { return st.answers[q.no]; });
      if (allDone) { st.graded = true; st.retry = null; }
      save();
      draw();
      if (allDone) app.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    btnRetry.addEventListener('click', function () {
      st.retry = items.filter(function (q) { return st.answers[q.no] !== q.answer; }).map(function (q) { return q.no; });
      st.retry.forEach(function (n) { delete st.answers[n]; });
      save();
      draw();
      app.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    $('.quiz-reset', app).addEventListener('click', function () {
      if (!confirm('풀이 기록을 모두 지울까요?')) return;
      st = { answers: {}, graded: false, retry: null };
      save();
      draw();
      app.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    draw();
    if (window.StudyToc) window.StudyToc.update();
  }

  /* ---------- 시작 ---------- */
  initTheme();
  initChapterNav();
  initToc();
  initProgress();
  initHome();
  initQuiz();
  inlineFigures().then(initLightbox);
})();
