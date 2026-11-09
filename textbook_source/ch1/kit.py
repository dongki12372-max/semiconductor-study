F='font-family="Noto Sans CJK KR"'
SUB='#efdcb8'; SD='#a9c8ec'; CH='#f2a68f'; GATE='#7f8c9d'; OX='#8fd19e'; STI='#dfe7ef'; SIN='#c9a3d9'; NAVY='#1b3a5c'; BLUE='#2d6a9f'; RED='#c0392b'; ORG='#e08a1e'; GRN='#2e8b57'; BRN='#7a4a10'
DEFS=('<defs>'
 '<marker id="ah" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/></marker>'
 '<marker id="ahb" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#2d6a9f"/></marker>'
 '<marker id="ahk" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#333"/></marker>'
 '<marker id="ahg" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#2e8b57"/></marker>'
 '<marker id="aho" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#e08a1e"/></marker>'
 '</defs>')
class S:
    def __init__(s,w,h): s.w,s.h=w,h; s.o=[]
    def rect(s,x,y,w,h,f,st='#444',sw=0.8,op=1,rx=0,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" fill-opacity="{op}" stroke="{st}" stroke-width="{sw}"{d}/>')
    def line(s,x1,y1,x2,y2,c='#333',w=1.2,dash=None,arrow=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        m={'r':'ah','b':'ahb','k':'ahk','g':'ahg','o':'aho'}.get(arrow)
        mk=f' marker-end="url(#{m})"' if m else ''
        s.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}{mk}/>')
    def path(s,d,f='none',c='#333',w=1.2,dash=None,arrow=None,op=1):
        dd=f' stroke-dasharray="{dash}"' if dash else ''
        m={'r':'ah','b':'ahb','k':'ahk','g':'ahg','o':'aho'}.get(arrow)
        mk=f' marker-end="url(#{m})"' if m else ''
        s.o.append(f'<path d="{d}" fill="{f}" fill-opacity="{op}" stroke="{c}" stroke-width="{w}"{dd}{mk}/>')
    def circ(s,x,y,r,f,st='none',sw=1):
        s.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    def t(s,x,y,txt,a='middle',c='#222',sz=10.5,b=False,it=False):
        import re
        txt=re.sub(r'([A-Za-z])_([A-Za-z0-9]+)',r'\1<tspan baseline-shift="sub" font-size="75%">\2</tspan>',str(txt))
        txt=re.sub(r'\^([0-9]+)',r'<tspan baseline-shift="super" font-size="75%">\1</tspan>',txt)
        s.o.append(f'<text x="{x}" y="{y}" text-anchor="{a}" fill="{c}" font-size="{sz}"{" font-weight=\"bold\"" if b else ""}{" font-style=\"italic\"" if it else ""}>{txt}</text>')
    def elec(s,x,y,r=4.5): s.circ(x,y,r,RED); s.t(x,y+3,'−','middle','white',8,True)
    def hole(s,x,y,r=4.5): s.circ(x,y,r,'white',GRN,1.5); s.t(x,y+3,'+','middle',GRN,8,True)
    def svg(s): return f'<svg width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}" xmlns="http://www.w3.org/2000/svg" {F} font-size="11">{DEFS}{"".join(s.o)}</svg>'
    def save(s,name): open(f'fig/{name}.svg','w').write(s.svg())
