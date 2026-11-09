/* ===== 메모: 본문을 드래그해서 모르는 곳에 메모를 남긴다 =====
   - 로컬 서버(tools/serve.py)로 열면 notes/<챕터>.json 에 저장 → Claude가 읽고 답변(reply)을 적는다.
   - 서버가 없으면 localStorage 에 저장하고, "메모 복사"로 내보낸다. */
(function () {
  'use strict';

  var chapter = document.body.dataset.chapter;
  var article = document.querySelector('.chapter');
  if (!chapter || !article) return;

  var store = window.StudyStore;
  var LKEY = 'notes:' + chapter;
  var API = 'api/notes/' + chapter;
  var BLOCKS = 'p, li, td, th, figcaption, .t, .qq, .a, .eq, .qz-stmt, .qz-expl, h2, h3, .ans';
  var notes = store.get(LKEY, []);
  var serverMode = false;

  var $ = function (s, r) { return (r || document).querySelector(s); };
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function now() { return new Date().toISOString(); }
  function fmtTime(iso) {
    var d = new Date(iso);
    return (d.getMonth() + 1) + '/' + d.getDate() + ' ' + d.getHours() + ':' + String(d.getMinutes()).padStart(2, '0');
  }

  /* ---------- 저장 ---------- */
  function save() {
    store.set(LKEY, notes);
    if (!serverMode) return Promise.resolve();
    return fetch(API, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chapter: chapter, notes: notes })
    }).then(function (r) { return r.json(); })
      .then(function (d) { notes = d.notes; store.set(LKEY, notes); })
      .catch(function () { setStatus('서버에 저장하지 못했다. 브라우저에만 저장됨'); });
  }
  function load() {
    return fetch(API, { cache: 'no-store' })
      .then(function (r) {
        if (!r.ok || !/json/.test(r.headers.get('Content-Type') || '')) throw new Error('no server');
        return r.json();
      })
      .then(function (d) {
        serverMode = true;
        // 서버가 비어 있고 브라우저에만 있던 메모가 있으면 올린다
        if (!d.notes.length && notes.length) return save();
        notes = d.notes;
        store.set(LKEY, notes);
      })
      .catch(function () { serverMode = false; });
  }

  /* ---------- 본문 위치 ↔ 텍스트 오프셋 ---------- */
  function blocks() {
    return Array.prototype.filter.call(article.querySelectorAll(BLOCKS), function (b) {
      return !b.parentNode.closest(BLOCKS) && !b.closest('.quiz-static.replaced');
    });
  }
  function blockOf(node) {
    var el = node.nodeType === 1 ? node : node.parentNode;
    var b = el && el.closest(BLOCKS);
    while (b && b.parentNode.closest(BLOCKS)) b = b.parentNode.closest(BLOCKS);
    return b && article.contains(b) ? b : null;
  }
  function offsetIn(block, node, off) {
    var r = document.createRange();
    r.setStart(block, 0);
    r.setEnd(node, off);
    return r.toString().length;
  }
  function sectionOf(el) {
    var heads = article.querySelectorAll('h2[id], h3[id]'), found = null;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING || heads[i] === el) found = heads[i];
      else break;
    }
    return found;
  }

  // block 안의 [start, end) 글자 범위를 <mark>로 감싼다 (여러 텍스트 노드에 걸쳐도 됨)
  function wrapRange(block, start, end, id) {
    var walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT), pos = 0, n, parts = [];
    while ((n = walker.nextNode())) {
      var len = n.nodeValue.length, s = Math.max(start - pos, 0), e = Math.min(end - pos, len);
      if (s < e) parts.push([n, s, e]);
      pos += len;
      if (pos >= end) break;
    }
    parts.forEach(function (p) {
      var node = p[0];
      if (p[2] < node.nodeValue.length) node.splitText(p[2]);
      if (p[1] > 0) node = node.splitText(p[1]);
      var m = document.createElement('mark');
      m.className = 'note-mark';
      m.dataset.note = id;
      node.parentNode.insertBefore(m, node);
      m.appendChild(node);
    });
  }
  function clearMarks() {
    Array.prototype.forEach.call(article.querySelectorAll('mark.note-mark'), function (m) {
      var p = m.parentNode;
      while (m.firstChild) p.insertBefore(m.firstChild, m);
      p.removeChild(m);
      p.normalize();
    });
  }
  // 메모의 인용문을 본문에서 다시 찾는다 (본문이 고쳐져도 최대한 찾아낸다)
  function locate(note, list) {
    function find(b) {
      var t = b.textContent, i = t.indexOf((note.prefix || '') + note.quote);
      if (i >= 0) return i + (note.prefix || '').length;
      return t.indexOf(note.quote);
    }
    var b = list[note.block];
    if (b) { var i = find(b); if (i >= 0) return [b, i]; }
    for (var k = 0; k < list.length; k++) { var j = find(list[k]); if (j >= 0) return [list[k], j]; }
    return null;
  }
  function paint() {
    clearMarks();
    var list = blocks();
    notes.forEach(function (n) {
      var hit = locate(n, list);
      n._found = !!hit;
      if (hit) wrapRange(hit[0], hit[1], hit[1] + n.quote.length, n.id);
    });
    Array.prototype.forEach.call(article.querySelectorAll('mark.note-mark'), function (m) {
      var n = byId(m.dataset.note);
      m.classList.toggle('has-reply', !!(n && n.reply));
    });
    updateCount();
  }
  function byId(id) { return notes.filter(function (n) { return n.id === id; })[0]; }

  /* ---------- UI 뼈대 ---------- */
  var addBtn = document.createElement('button');
  addBtn.type = 'button';
  addBtn.className = 'note-add no-print';
  addBtn.textContent = '✎ 메모';
  addBtn.hidden = true;
  document.body.appendChild(addBtn);

  var editor = document.createElement('div');
  editor.className = 'note-editor no-print';
  editor.hidden = true;
  editor.innerHTML = '<div class="note-editor-card" role="dialog" aria-label="메모">' +
    '<div class="note-quote"></div>' +
    '<textarea rows="4" placeholder="무엇이 헷갈리는지, 어떻게 이해했는지 적어 두자"></textarea>' +
    '<div class="note-reply"></div>' +
    '<div class="note-editor-actions"><button type="button" class="btn ghost note-del">삭제</button>' +
    '<span style="flex:1"></span><button type="button" class="btn ghost note-cancel">취소</button>' +
    '<button type="button" class="btn note-save">저장</button></div></div>';
  document.body.appendChild(editor);

  var drawer = document.createElement('aside');
  drawer.className = 'note-drawer no-print';
  drawer.hidden = true;
  drawer.setAttribute('aria-label', '메모 목록');
  drawer.innerHTML = '<div class="note-drawer-head"><b>메모</b><span class="note-mode"></span>' +
    '<button type="button" class="icon-btn note-close" aria-label="닫기">✕</button></div>' +
    '<div class="note-drawer-tools"><button type="button" class="btn ghost note-copy">메모 복사</button>' +
    '<span class="note-status"></span></div>' +
    '<div class="note-list"></div>' +
    '<p class="note-help">본문을 드래그하면 <b>✎ 메모</b> 버튼이 뜬다. 메모를 남긴 뒤 Claude에게 "메모 봐줘"라고 하면 읽고 답변을 적어 준다.</p>';
  document.body.appendChild(drawer);

  var topBtn = document.createElement('button');
  topBtn.type = 'button';
  topBtn.className = 'icon-btn note-top';
  topBtn.setAttribute('aria-label', '메모 목록');
  topBtn.innerHTML = '✎<span class="note-count"></span>';
  var themeBtn = $('#theme-toggle');
  if (themeBtn) themeBtn.parentNode.insertBefore(topBtn, themeBtn);

  function updateCount() {
    var c = $('.note-count', topBtn);
    var unread = notes.filter(function (n) { return n.reply && !n.replySeen; }).length;
    c.textContent = notes.length ? String(notes.length) : '';
    topBtn.classList.toggle('has-new', unread > 0);
    topBtn.title = '메모 ' + notes.length + '개' + (unread ? ' · 새 답변 ' + unread + '개' : '');
  }
  function setStatus(t) { $('.note-status', drawer).textContent = t; }

  /* ---------- 드래그 → 메모 버튼 ---------- */
  var pending = null;   // 새로 만들 메모의 위치 정보
  function readSelection() {
    var sel = window.getSelection();
    if (!sel.rangeCount || sel.isCollapsed) return null;
    var r = sel.getRangeAt(0);
    var b = blockOf(r.startContainer);
    if (!b || !article.contains(r.startContainer)) return null;
    if (r.startContainer.parentNode && r.startContainer.parentNode.closest && r.startContainer.parentNode.closest('svg')) return null;
    var start = offsetIn(b, r.startContainer, r.startOffset);
    var end = b.contains(r.endContainer) ? offsetIn(b, r.endContainer, r.endOffset) : b.textContent.length;
    var text = b.textContent;
    // 앞뒤 공백은 빼고 저장
    while (start < end && /\s/.test(text[start])) start++;
    while (end > start && /\s/.test(text[end - 1])) end--;
    if (end - start < 1) return null;
    var list = blocks();
    var sec = sectionOf(b);
    return {
      block: list.indexOf(b), start: start, quote: text.slice(start, end),
      prefix: text.slice(Math.max(0, start - 20), start),
      section: sec ? sec.id : '', sectionTitle: sec ? sec.textContent.replace(/\s+/g, ' ').trim() : '',
      rect: r.getBoundingClientRect()
    };
  }
  function showAdd() {
    var p = readSelection();
    if (!p) { addBtn.hidden = true; pending = null; return; }
    pending = p;
    addBtn.hidden = false;
    var top = p.rect.top + window.scrollY - addBtn.offsetHeight - 8;
    if (p.rect.top < 110) top = p.rect.bottom + window.scrollY + 8;
    addBtn.style.top = top + 'px';
    addBtn.style.left = Math.max(8, Math.min(window.innerWidth - 90, p.rect.left + p.rect.width / 2 - 40)) + 'px';
  }
  var selTimer;
  document.addEventListener('selectionchange', function () {
    clearTimeout(selTimer);
    selTimer = setTimeout(showAdd, 250);
  });
  addBtn.addEventListener('mousedown', function (e) { e.preventDefault(); });   // 선택이 풀리지 않게
  addBtn.addEventListener('click', function () {
    if (!pending) return;
    openEditor(null, pending);
    addBtn.hidden = true;
  });

  /* ---------- 메모 편집 ---------- */
  var editing = null;   // { note } 또는 { draft }
  function openEditor(note, draft) {
    editing = note ? { note: note } : { draft: draft };
    var q = note ? note.quote : draft.quote;
    $('.note-quote', editor).textContent = q.length > 160 ? q.slice(0, 160) + '…' : q;
    $('textarea', editor).value = note ? note.text : '';
    $('.note-del', editor).hidden = !note;
    var rep = $('.note-reply', editor);
    rep.hidden = !(note && note.reply);
    if (note && note.reply) {
      rep.innerHTML = '<div class="note-reply-head">Claude 답변 · ' + (note.replyAt ? fmtTime(note.replyAt) : '') + '</div>' + esc(note.reply).replace(/\n/g, '<br>');
      if (!note.replySeen) { note.replySeen = true; save(); updateCount(); }
    }
    editor.hidden = false;
    $('textarea', editor).focus();
  }
  function closeEditor() { editor.hidden = true; editing = null; }
  $('.note-cancel', editor).addEventListener('click', closeEditor);
  editor.addEventListener('click', function (e) { if (e.target === editor) closeEditor(); });
  $('.note-save', editor).addEventListener('click', function () {
    var text = $('textarea', editor).value.trim();
    if (editing.note) {
      editing.note.text = text;
      editing.note.updatedAt = now();
    } else {
      var d = editing.draft;
      notes.push({
        id: 'n' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5),
        section: d.section, sectionTitle: d.sectionTitle, block: d.block,
        quote: d.quote, prefix: d.prefix, text: text, createdAt: now(), updatedAt: now()
      });
      window.getSelection().removeAllRanges();
    }
    closeEditor();
    save().then(function () { paint(); renderList(); });
  });
  $('.note-del', editor).addEventListener('click', function () {
    if (!confirm('이 메모를 지울까요?')) return;
    var id = editing.note.id;
    notes = notes.filter(function (n) { return n.id !== id; });
    closeEditor();
    save().then(function () { paint(); renderList(); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !editor.hidden) closeEditor();
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter' && !editor.hidden) $('.note-save', editor).click();
  });
  article.addEventListener('click', function (e) {
    var m = e.target.closest('mark.note-mark');
    if (m && window.getSelection().isCollapsed) { var n = byId(m.dataset.note); if (n) openEditor(n); }
  });

  /* ---------- 메모 목록 ---------- */
  function sorted() {   // 본문 순서대로
    return notes.slice().sort(function (a, b) {
      var ma = article.querySelector('mark[data-note="' + a.id + '"]'), mb = article.querySelector('mark[data-note="' + b.id + '"]');
      if (ma && mb && ma !== mb) return ma.compareDocumentPosition(mb) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
      return (a.block || 0) - (b.block || 0);
    });
  }
  function renderList() {
    $('.note-mode', drawer).textContent = serverMode ? '폴더에 저장 중 (notes/' + chapter + '.json)' : '브라우저에만 저장 중';
    var box = $('.note-list', drawer);
    if (!notes.length) { box.innerHTML = '<p class="note-empty">아직 메모가 없다.</p>'; return; }
    var html = '', last = null;
    sorted().forEach(function (n) {
      if (n.sectionTitle !== last) { html += '<div class="note-sec">' + esc(n.sectionTitle || '—') + '</div>'; last = n.sectionTitle; }
      html += '<div class="note-item' + (n.reply ? ' has-reply' : '') + (n.reply && !n.replySeen ? ' is-new' : '') + '" data-id="' + n.id + '">' +
        '<div class="note-item-quote">' + esc(n.quote.length > 80 ? n.quote.slice(0, 80) + '…' : n.quote) +
        (n._found === false ? ' <span class="note-lost">(본문에서 위치를 못 찾음)</span>' : '') + '</div>' +
        '<div class="note-item-text">' + (n.text ? esc(n.text).replace(/\n/g, '<br>') : '<i>(내용 없음)</i>') + '</div>' +
        (n.reply ? '<div class="note-item-reply"><b>Claude</b> ' + esc(n.reply).replace(/\n/g, '<br>') + '</div>' : '') +
        '<div class="note-item-time">' + fmtTime(n.createdAt) + '</div></div>';
    });
    box.innerHTML = html;
  }
  function openDrawer() {
    load().then(function () { paint(); renderList(); });
    renderList();
    drawer.hidden = false;
    document.body.classList.add('notes-open');
  }
  function closeDrawer() { drawer.hidden = true; document.body.classList.remove('notes-open'); }
  topBtn.addEventListener('click', function () { if (drawer.hidden) openDrawer(); else closeDrawer(); });
  $('.note-close', drawer).addEventListener('click', closeDrawer);
  $('.note-list', drawer).addEventListener('click', function (e) {
    var it = e.target.closest('.note-item');
    if (!it) return;
    var n = byId(it.dataset.id);
    var m = article.querySelector('mark[data-note="' + it.dataset.id + '"]');
    if (m) {
      m.scrollIntoView({ behavior: 'smooth', block: 'center' });
      m.classList.add('flash');
      setTimeout(function () { m.classList.remove('flash'); }, 1600);
    }
    if (window.matchMedia('(max-width: 960px)').matches) closeDrawer();
    if (n) setTimeout(function () { openEditor(n); }, m ? 450 : 0);
  });

  // 대화창에 붙여 넣기 좋은 형태로 복사
  $('.note-copy', drawer).addEventListener('click', function () {
    var md = '# ' + chapter + ' 메모 ' + notes.length + '개\n\n';
    sorted().forEach(function (n, i) {
      md += (i + 1) + '. [' + (n.sectionTitle || '') + '] "' + n.quote + '"\n   → ' + (n.text || '(내용 없음)').replace(/\n/g, '\n     ') + '\n';
    });
    function done() { setStatus('복사됨. 대화창에 붙여 넣으면 된다'); }
    if (navigator.clipboard) navigator.clipboard.writeText(md).then(done, function () { fallbackCopy(md); done(); });
    else { fallbackCopy(md); done(); }
  });
  function fallbackCopy(t) {
    var ta = document.createElement('textarea');
    ta.value = t; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    ta.remove();
  }

  /* ---------- 시작: 그림·퀴즈가 자리 잡은 뒤 칠한다 ---------- */
  load().then(function () { setTimeout(function () { paint(); renderList(); }, 600); });
  window.StudyNotes = { repaint: paint };
})();
