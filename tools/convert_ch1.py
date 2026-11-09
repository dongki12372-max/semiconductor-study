"""ch1_full_reference.html → site/ch1.html 본문 + site/assets/figs/ch1/*.svg

한 번만 돌리는 변환 스크립트다. 사이트 자체는 빌드 없이 열린다.
본문 문장은 건드리지 않고, 구조(제목 id, 그림 파일 분리, 상자 마크업)만 바꾼다.

사용: python3 tools/convert_ch1.py   (프로젝트 루트에서)

주의: 메모 피드백으로 site/ch1.html 본문을 직접 고치기 시작한 뒤에는 다시 돌리지 말 것.
      그 수정이 모두 덮어써진다. 그 뒤로는 site/ch1.html 이 원본이다.
"""
import re, glob, os, shutil, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'textbook_source', 'ch1')
SITE = os.path.join(ROOT, 'site')
FIGDIR = os.path.join(SITE, 'assets', 'figs', 'ch1')
CH = 1

# fig/ 에 원본 파일이 없는, 완성본 속 손으로 쓴 SVG 두 개의 이름 (등장 순서)
EXTRA_NAMES = ['nmos_xs', 'nmos_onoff']

doc = open(os.path.join(SRC, 'ch1_full_reference.html'), encoding='utf-8').read()
body = doc[doc.index('<body>') + 6: doc.rindex('</body>')]

# ── 1. 그림: 인라인 SVG → 파일 + <img> ────────────────────────────
os.makedirs(FIGDIR, exist_ok=True)
files = {}
for f in sorted(glob.glob(os.path.join(SRC, 'fig', '*.svg'))):
    files.setdefault(open(f, encoding='utf-8').read().strip(), os.path.basename(f)[:-4])
extra = iter(EXTRA_NAMES)
used = []

def svg_to_img(m):
    svg = m.group(0).strip()
    name = files.get(svg)
    if name is None:
        name = next(extra)
        open(os.path.join(FIGDIR, name + '.svg'), 'w', encoding='utf-8').write(svg + '\n')
    else:
        shutil.copy(os.path.join(SRC, 'fig', name + '.svg'), os.path.join(FIGDIR, name + '.svg'))
    used.append(name)
    return f'<img src="assets/figs/ch{CH}/{name}.svg" alt="" data-fig="{name}">'

body = re.sub(r'<svg.*?</svg>', svg_to_img, body, flags=re.S)

# 그림 번호 → figure id, alt
fig_no = {}
def fig_block(m):
    block = m.group(0)
    n = re.search(r'<b class="fn">그림 \d+-(\d+)\.</b>', block).group(1)
    cap = re.sub(r'<[^>]+>', '', block.split('<figcaption>')[1]).strip()
    block = block.replace('alt=""', f'alt="{html.escape(cap, quote=True)}"', 1)
    imgs = re.findall(r'<img [^>]+>', block)
    media = '<div class="fig-media">' + ''.join(imgs) + '</div>'
    block = re.sub(r'\s*<img [^>]+>\s*', '', block)
    block = block.replace('<figure>', f'<figure id="fig-{CH}-{n}">{media}', 1)
    return block

body = re.sub(r'<figure>.*?</figure>', fig_block, body, flags=re.S)

# ── 2. 표지 → 장 머리말 ───────────────────────────────────────────
cover = re.search(r'<div class="cover">.*?\n</div>\n', body, flags=re.S).group(0)
body = body.replace(cover, '')
part = re.search(r'<div class="part">(.*?)</div>', cover).group(1)
title = re.search(r'<h1>(.*?)</h1>', cover, flags=re.S).group(1)
sub = re.search(r'<div class="sub">(.*?)</div>', cover).group(1)
toc_lines = [l.strip() for l in re.search(r'<div class="toc">(.*?)</div>', cover, flags=re.S).group(1).split('<br>')]
legend = re.search(r'<div class="legend">.*?</div>', cover, flags=re.S).group(0)

# ── 3. 제목에 id ─────────────────────────────────────────────────
counter = {}
cur_h2 = None
def heading_id(m):
    global cur_h2
    tag, attrs, inner = m.group(1), m.group(2), m.group(3)
    text = re.sub(r'<[^>]+>', '', inner)
    num = re.match(r'(\d+(?:\.\d+)+)\s', text)
    if num:
        hid = 's' + num.group(1).replace('.', '-')
    elif tag == 'h3' and cur_h2:
        counter[cur_h2] = counter.get(cur_h2, 0) + 1
        hid = f'{cur_h2}-{chr(96 + counter[cur_h2])}'
    else:
        hid = {'면접 예상 질문': f's{CH}-interview'}.get(text.strip(), 'h-' + str(len(counter)))
    if hid in ids:  # "1.12 OX 퀴즈 해설" 처럼 번호가 겹치는 경우
        hid += '-2'
    ids.add(hid)
    if tag == 'h2':
        cur_h2 = hid
    return f'<{tag} id="{hid}"{attrs}>{inner}</{tag}>'

ids = set()
body = re.sub(r'<(h[23])((?: [^>]*)?)>(.*?)</\1>', heading_id, body, flags=re.S)

# 표지 목차 줄 → 해당 h2 링크
def toc_link(line):
    num = re.match(r'(\d+\.\d+)\s', line).group(1)
    return f'<li><a href="#s{num.replace(".", "-")}">{line}</a></li>'
toc_html = '<ol class="ch-toc">' + ''.join(toc_link(l) for l in toc_lines) + '</ol>'

# ── 4. OX 퀴즈 → data/ch1_quiz.json ──────────────────────────────
# 해설에는 관련 절이 적혀 있지 않아 본문을 보고 정했다.
QUIZ_SECTION = {
    1: 's1-1-4', 2: 's1-1-2', 3: 's1-1-4', 4: 's1-1-5', 5: 's1-1-5', 6: 's1-2-1', 7: 's1-2-1',
    8: 's1-3', 9: 's1-2-2', 10: 's1-4-2', 11: 's1-4-2', 12: 's1-4-4', 13: 's1-4-4', 14: 's1-4-3',
    15: 's1-5-d', 16: 's1-6-d', 17: 's1-7-b', 18: 's1-7-c', 19: 's1-7-d', 20: 's1-8-1', 21: 's1-8-1',
    22: 's1-8-2', 23: 's1-9-4', 24: 's1-9-6', 25: 's1-1-2', 26: 's1-4-4', 27: 's1-1-5', 28: 's1-3',
}
rows = re.findall(r'<tr><td>(\d+)</td><td>(.*?)</td><td></td></tr>', body)
anss = re.findall(r'<div class="ans"><span class="num">(\d+)</span><span class="mark [ox]">([OX])</span> (.*?)</div>', body)
assert len(rows) == len(anss) == len(QUIZ_SECTION), (len(rows), len(anss))
quiz = []
for (n, stmt), (n2, mark, expl) in zip(rows, anss):
    assert n == n2
    quiz.append({'no': int(n), 'statement': stmt, 'answer': mark, 'explanation': expl,
                 'section': QUIZ_SECTION[int(n)]})
os.makedirs(os.path.join(SITE, 'data'), exist_ok=True)
import json
with open(os.path.join(SITE, 'data', f'ch{CH}_quiz.json'), 'w', encoding='utf-8') as f:
    json.dump({'chapter': f'ch{CH}', 'items': quiz}, f, ensure_ascii=False, indent=1)

# 안내 문장: 화면(퀴즈 앱)용과 인쇄용을 따로 둔다
QUIZ_INTRO_PRINT = '먼저 풀어 보고 다음 쪽 해설로 확인하자. 틀린 문항은 해당 절로 돌아가 다시 읽으면 된다.'
QUIZ_INTRO_WEB = '다 풀면 자동으로 채점되고, 문항마다 해설과 관련 절 링크가 붙는다. 틀린 문항은 해당 절로 돌아가 다시 읽으면 된다.'
assert QUIZ_INTRO_PRINT in body
body = body.replace(QUIZ_INTRO_PRINT, f'<span class="quiz-intro-print">{QUIZ_INTRO_PRINT}</span>'
                                      f'<span class="quiz-intro-web">{QUIZ_INTRO_WEB}</span>')

# 원래의 문제 표 + 해설은 인쇄용으로 남기고, 화면에서는 퀴즈 앱으로 대체한다
qs = body.index('<table class="quiz">')
qe = body.rindex('<div class="ans">')
qe = body.index('</div>', qe) + len('</div>')
body = (body[:qs] + f'<div class="quiz-app no-print" data-quiz="data/ch{CH}_quiz.json" hidden></div>\n'
        '<div class="quiz-static">' + body[qs:qe] + '</div>' + body[qe:])

# 넓은 표는 가로 스크롤되도록 감싼다
body = re.sub(r'<table.*?</table>', lambda m: f'<div class="table-wrap">{m.group(0)}</div>', body, flags=re.S)

header = f'''<header class="ch-head">
  <div class="part">{part}</div>
  <h1>{title}</h1>
  <div class="sub">{sub}</div>
  <nav class="ch-toc-wrap" aria-label="이 장의 내용">
    <div class="ch-toc-title">이 장의 내용</div>
    {toc_html}
  </nav>
  {legend}
</header>
'''

article = header + body.strip() + '\n'
open(os.path.join(ROOT, 'tools', 'ch1_article.html'), 'w', encoding='utf-8').write(article)

# site/ch1.html 의 <article> 안을 교체
page_path = os.path.join(SITE, 'ch1.html')
page = open(page_path, encoding='utf-8').read()
start = page.index('<!-- ARTICLE:BEGIN -->') + len('<!-- ARTICLE:BEGIN -->')
end = page.index('<!-- ARTICLE:END -->')
page = page[:start] + '\n' + article + page[end:]
open(page_path, 'w', encoding='utf-8').write(page)

print('figures', len(used), 'files', len(set(used)), 'headings', len(ids))
