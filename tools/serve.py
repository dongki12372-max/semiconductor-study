"""교재 사이트 로컬 서버: site/ 를 서빙하고, 메모를 notes/<챕터>.json 에 저장한다.

  python3 tools/serve.py [포트]

- 127.0.0.1 에만 열린다 (같은 컴퓨터에서만 접속).
- GET /api/notes/ch1  → notes/ch1.json
- PUT /api/notes/ch1  → 저장. reply / replyAt 은 Claude가 파일에 직접 적는 필드라서
  브라우저가 보낸 값보다 파일에 있는 값을 우선한다.
"""
import json, os, re, sys, http.server, functools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
NOTES = os.path.join(ROOT, 'notes')
CHAPTER_RE = re.compile(r'^/api/notes/([a-z0-9_-]{1,32})$')
SERVER_FIELDS = ('reply', 'replyAt')


def notes_path(ch):
    return os.path.join(NOTES, ch + '.json')


def read_notes(ch):
    try:
        with open(notes_path(ch), encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'chapter': ch, 'notes': []}


class Handler(http.server.SimpleHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        m = CHAPTER_RE.match(self.path.split('?')[0])
        if m:
            return self._json(200, read_notes(m.group(1)))
        return super().do_GET()

    def do_PUT(self):
        m = CHAPTER_RE.match(self.path.split('?')[0])
        if not m:
            return self._json(404, {'error': 'not found'})
        ch = m.group(1)
        try:
            n = int(self.headers.get('Content-Length', 0))
            incoming = json.loads(self.rfile.read(n).decode('utf-8'))
            notes = incoming['notes']
            assert isinstance(notes, list)
        except Exception:
            return self._json(400, {'error': 'bad request'})
        old = {x.get('id'): x for x in read_notes(ch).get('notes', [])}
        for note in notes:
            prev = old.get(note.get('id'), {})
            for k in SERVER_FIELDS:
                if prev.get(k):
                    note[k] = prev[k]
        data = {'chapter': ch, 'notes': notes}
        os.makedirs(NOTES, exist_ok=True)
        tmp = notes_path(ch) + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        os.replace(tmp, notes_path(ch))
        return self._json(200, data)

    def end_headers(self):
        # 수정한 본문이 바로 보이도록 캐시하지 않는다
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        # 일반 요청 로그는 숨기고, 메모 저장만 알린다
        try:
            msg = fmt % args
        except Exception:
            return
        if msg.startswith('"PUT /api/notes/'):
            sys.stderr.write('메모 저장됨\n')


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(Handler, directory=SITE)
    with http.server.ThreadingHTTPServer(('127.0.0.1', port), handler) as httpd:
        print(f'교재 서버 실행 중: http://localhost:{port}  (창을 닫으면 종료)')
        httpd.serve_forever()
