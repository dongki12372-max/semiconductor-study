import math
C=math.cos(math.radians(30))
F='font-family="Noto Sans CJK KR"'
def shade(h,f):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    if f>1: r,g,b=[int(v+(255-v)*(f-1)) for v in (r,g,b)]
    else: r,g,b=[int(v*f) for v in (r,g,b)]
    return '#%02x%02x%02x'%(r,g,b)
class Iso:
    def __init__(s,ox,oy,sc): s.ox,s.oy,s.s=ox,oy,sc; s.o=[]
    def P(s,x,y,z): return (s.ox+(x-y)*C*s.s, s.oy+((x+y)*0.5-z)*s.s)
    def poly(s,pts,fill,op=1,stroke='#333',sw=0.8,dash=None):
        d=' '.join('%.1f,%.1f'%s.P(*p) for p in pts)
        da=f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<polygon points="{d}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{da}/>')
    def box(s,x0,x1,y0,y1,z0,z1,col,op=1,stroke='#444'):
        s.poly([(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],shade(col,0.78),op,stroke)
        s.poly([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],shade(col,0.9),op,stroke)
        s.poly([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],shade(col,1.08),op,stroke)
    def arrow(s,a,b,col='#c0392b',w=2.2,dash=None):
        (x1,y1),(x2,y2)=s.P(*a),s.P(*b)
        da=f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" marker-end="url(#ah)"{da}/>')
    def label(s,p,txt,tx,ty,col='#222',anchor='start',bold=False,size=10.5):
        x,y=s.P(*p); fw=' font-weight="bold"' if bold else ''
        s.o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{tx}" y2="{ty}" stroke="#666" stroke-width="0.7"/>')
        s.o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#333"/>')
        s.o.append(f'<text x="{tx+(3 if anchor=="start" else -3)}" y="{ty+4}" text-anchor="{anchor}" fill="{col}" font-size="{size}"{fw}>{txt}</text>')
    def text(s,x,y,t,anchor='middle',col='#222',size=11,bold=False):
        fw=' font-weight="bold"' if bold else ''
        s.o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{col}" font-size="{size}"{fw}>{t}</text>')
DEFS='<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/></marker><marker id="ahb" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2d6a9f"/></marker></defs>'
def svg(w,h,body): return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" {F} font-size="11">{DEFS}{body}</svg>'
SUB='#efdcb8'; SD='#a9c8ec'; CH='#f2a68f'; GATE='#7f8c9d'; OX='#8fd19e'; STI='#dfe7ef'

def axes(s,x,y):
    # small axis triad at origin in iso space offset
    o=Iso(x,y,14)
    o.o=[]
    a=o.P(0,0,0); 
    for v,t,c in [((2.2,0,0),'L (전류 방향)','#c0392b'),((0,2.2,0),'W (폭)','#2d6a9f'),((0,0,2.0),'높이','#333')]:
        b=o.P(*v)
        o.o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{c}" stroke-width="1.5" marker-end="url(#ah)"/>')
        o.o.append(f'<text x="{b[0]+(4 if v[0] else -4 if v[1] else 4):.1f}" y="{b[1]+(10 if v[0] else 10 if v[1] else 0):.1f}" text-anchor="{"start" if v[0] or v[2] else "end"}" fill="{c}" font-size="9.5">{t}</text>')
    s.o+=o.o

# ---------- Fig: planar 3D ----------
s=Iso(205,70,21)
s.box(0,10,0,6,-3,-0.6,SUB)
s.box(0,3.6,0,6,-0.6,0,SD); s.box(3.6,6.4,0,6,-0.6,0,SUB); s.box(6.4,10,0,6,-0.6,0,SD)
s.poly([(3.6,0,0),(6.4,0,0),(6.4,6,0),(3.6,6,0)],CH,0.9)
s.arrow((1.0,3,0),(9.3,3,0),dash='6,3')
s.box(3.7,6.3,0,6,0,0.18,OX)
s.box(3.7,6.3,0,6,0.18,2.0,GATE,0.93)
s.poly([(5,-0.6,-3.2),(5,6.6,-3.2),(5,6.6,2.6),(5,-0.6,2.6)],'none',1,'#c0392b',1.4,'5,3')
s.label((1.5,1.5,0),'소스 (n⁺)',95,45,anchor='end',bold=True)
s.label((5,1,2),'게이트',235,22,anchor='end',bold=True)
s.label((8.5,1,0),'드레인 (n⁺)',420,130,bold=True)
s.label((6.3,3,0.09),'게이트 절연막 (초록 얇은 층)',420,165,col='#2e8b57')
s.label((2,6,-2),'p형 실리콘 기판',95,240,anchor='end')
x,y=s.P(5,-0.6,2.6); s.text(x+5,y-6,"자르는 면 A–A′",'start','#c0392b',10,True)
s.text(345,222,'전류 S → D','start','#c0392b',10,True)
s.text(345,236,'(게이트 바로 아래 표면 = 채널)','start','#c0392b',9.5)
axes(s,470,250)
open('fig/planar3d.svg','w').write(svg(560,300,''.join(s.o)))

# ---------- Fig: FinFET 3D ----------
s=Iso(215,95,20)
s.box(0,10,-2,4,-3.2,-1.6,SUB)
s.box(0,10,-2,4,-1.6,-0.4,STI)
s.box(0,3.6,0.5,1.5,-0.4,3.0,SD)
s.box(3.6,6.4,0.5,1.5,-0.4,3.0,CH)
s.arrow((0.6,1,2.0),(9.6,1,2.0),dash='6,3')
s.box(3.7,6.3,-1.6,3.6,-0.4,3.9,GATE,0.42,'#2b3640')
s.box(6.4,10,0.5,1.5,-0.4,3.0,SD)
s.label((1.5,1,3),'소스',150,35,anchor='end',bold=True)
s.label((5,-1.6,3.9),'게이트 (반투명으로 그림)',360,30,bold=True)
s.label((8.8,1.5,2.4),'드레인',430,120,bold=True)
s.label((5,1.5,1.0),'핀 속 채널 (빨강)',430,165,col='#c0392b',bold=True)
s.text(433,183,'윗면 + 양옆면을 게이트가 감쌈','start','#c0392b',9.5)
s.label((2,4,-0.4),'STI 산화막',120,180,anchor='end')
s.label((2,4,-2.6),'기판',120,225,anchor='end')
axes(s,470,265)
open('fig/fin3d.svg','w').write(svg(560,320,''.join(s.o)))

# ---------- Fig: GAA 3D ----------
s=Iso(215,95,20)
s.box(0,10,-2,4.5,-3.2,-1.6,SUB)
s.box(0,10,-2,4.5,-1.6,-0.4,STI)
s.box(0,3.5,-0.2,2.7,-0.4,3.4,SD)
for z0 in (0.0,1.2,2.4):
    s.box(3.5,6.5,0,2.5,z0,z0+0.5,CH)
s.arrow((0.8,1.25,3.4),(9.4,1.25,3.4),dash='6,3')
s.box(3.5,6.5,-1.0,3.5,-0.4,3.9,GATE,0.38,'#2b3640')
s.box(6.5,10,-0.2,2.7,-0.4,3.4,SD)
s.label((1.5,0.5,3.4),'소스 (에피 성장)',170,30,anchor='end',bold=True)
s.label((5,-1,3.9),'게이트 (반투명): 시트 사이까지 채움',350,28,bold=True)
s.label((8.8,2.7,2.4),'드레인',430,150,bold=True)
s.label((5,2.5,2.65),'Si 나노시트 3장 (빨강 = 채널)',430,195,col='#c0392b',bold=True)
s.label((2,4.5,-0.4),'STI',120,185,anchor='end')
axes(s,470,265)
open('fig/gaa3d.svg','w').write(svg(560,320,''.join(s.o)))

# ---------- Fig: cross sections A-A' ----------
o=[]
def rect(x,y,w,h,f,st='#444',sw=0.8,op=1): o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}" fill-opacity="{op}" stroke="{st}" stroke-width="{sw}"/>')
def line(x1,y1,x2,y2,c='#c0392b',w=3.2,d=None):
    dd=f' stroke-dasharray="{d}"' if d else ''
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{dd}/>')
def t(x,y,s,a='middle',c='#222',sz=10.5,b=False):
    o.append(f'<text x="{x}" y="{y}" text-anchor="{a}" fill="{c}" font-size="{sz}"{" font-weight=\"bold\"" if b else ""}>{s}</text>')
# planar panel 0..180
X=10
t(X+85,16,'Planar',b=True,c='#1b3a5c')
rect(X,110,170,110,SUB)
rect(X,110,28,45,STI); rect(X+142,110,28,45,STI)
rect(X+38,104,104,6,OX); rect(X+38,55,104,49,GATE)
t(X+90,84,'게이트','middle','white',10.5,True)
line(X+38,110,X+142,110)
for i,op in enumerate([0.45,0.3,0.18,0.08]):
    rect(X+38,112+i*12,104,12,'#c0392b','none',0,op)
t(X+90,178,'↓ 아래로 갈수록','middle','#7a4a10',9.5); t(X+90,191,'게이트 영향 약함','middle','#7a4a10',9.5)
t(X+90,208,'→ 누설이 새는 길','middle','#c0392b',9.5,True)
t(X+24,135,'STI','middle','#556',9)
# FinFET panel
X=205
t(X+85,16,'FinFET',b=True,c='#1b3a5c')
rect(X,170,170,50,SUB); rect(X,140,170,30,STI)
rect(X+70,62,30,108,'#f5d3c4')
# oxide around fin
o.append(f'<path d="M{X+64},140 L{X+64},56 L{X+106},56 L{X+106},140 L{X+100},140 L{X+100},62 L{X+70},62 L{X+70},140 Z" fill="{OX}" stroke="#2e8b57" stroke-width="0.6"/>')
o.append(f'<path d="M{X+25},140 L{X+25},30 L{X+145},30 L{X+145},140 L{X+106},140 L{X+106},56 L{X+64},56 L{X+64},140 Z" fill="{GATE}" stroke="#333" stroke-width="0.8"/>')
line(X+70,140,X+70,62); line(X+70,62,X+100,62); line(X+100,62,X+100,140)
t(X+85,46,'게이트','middle','white',10.5,True)
t(X+85,105,'핀','middle','#7a4a10',9.5)
o.append(f'<line x1="{X+70}" y1="150" x2="{X+100}" y2="150" stroke="#2d6a9f" marker-end="url(#ahb)"/>')
t(X+85,162,'W_fin','middle','#2d6a9f',9)
o.append(f'<line x1="{X+152}" y1="140" x2="{X+152}" y2="66" stroke="#2d6a9f" marker-end="url(#ahb)"/>')
t(X+158,105,'H_fin','start','#2d6a9f',9)
t(X+85,200,'핀이 얇아 몸통 전체가','middle','#7a4a10',9.5); t(X+85,213,'게이트 영향권','middle','#7a4a10',9.5)
# GAA panel
X=400
t(X+85,16,'GAA (나노시트)',b=True,c='#1b3a5c')
rect(X,170,170,50,SUB); rect(X,150,170,20,STI)
rect(X+25,30,120,120,GATE)
for yy in (48,85,122):
    rect(X+45,yy-5,80,23,OX,'#2e8b57',0.6)
    rect(X+50,yy,70,13,'#f5d3c4')
    o.append(f'<rect x="{X+50}" y="{yy}" width="70" height="13" fill="none" stroke="#c0392b" stroke-width="3"/>')
t(X+85,41,'게이트','middle','white',10,True)
o.append(f'<line x1="{X+50}" y1="27" x2="{X+120}" y2="27" stroke="#2d6a9f" marker-end="url(#ahb)"/>')
t(X+150,58,'T = 시트','start','#2d6a9f',9); t(X+150,70,'두께','start','#2d6a9f',9)
t(X+85,205,'시트마다 4면을','middle','#7a4a10',9.5); t(X+85,218,'게이트가 완전히 감쌈','middle','#7a4a10',9.5)
t(X+40,30,'W','middle','#2d6a9f',9)
o.append('<text x="290" y="246" text-anchor="middle" font-size="10" fill="#c0392b">빨간 선 = 게이트가 직접 맞닿아 통제하는 채널 표면. 전류는 지면을 뚫고 들어가는 방향(⊗).</text>')
items=[('#efdcb8','Si 기판 (반도체)'),('#dfe7ef','STI 산화막 (절연체)'),('#f5d3c4','채널이 되는 Si'),('#8fd19e','게이트 절연막'),('#7f8c9d','게이트 (금속)')]
for k,(c,n) in enumerate(items):
    x=20+k*114
    o.append(f'<rect x="{x}" y="262" width="14" height="10" fill="{c}" stroke="#777" stroke-width="0.5"/>')
    t(x+18,271,n,'start','#333',8.8)
open('fig/xsec.svg','w').write(svg(580,282,''.join(o)))

# ---------- Fig: short channel tug of war (longitudinal) ----------
o=[]
def panel(X,L,title,short):
    t(X+125,16,title,b=True,c='#1b3a5c')
    rect(X,60,250,110,SUB)
    gx0=125-L/2; gx1=125+L/2
    rect(X+gx0-55,60,55,28,SD); rect(X+gx1,60,55,28,SD)
    t(X+gx0-28,79,'S','middle','#1b3a5c',11,True); t(X+gx1+28,79,'D','middle','#1b3a5c',11,True)
    rect(X+gx0,54,L,6,OX); rect(X+gx0,28,L,26,GATE); t(X+125,46,'G','middle','white',11,True)
    # depletion regions
    rs=16; rd=28 if not short else 40
    o.append(f'<path d="M{X+gx0-55},88 Q{X+gx0-55},{88+rs} {X+gx0-20},{88+rs} Q{X+gx0+rs-4},{88+rs} {X+gx0+rs-4},60" fill="none" stroke="#2d6a9f" stroke-dasharray="4,3"/>')
    o.append(f'<path d="M{X+gx1+55},88 Q{X+gx1+55},{88+rd} {X+gx1+20},{88+rd} Q{X+gx1-rd+6},{88+rd} {X+gx1-rd+6},60" fill="none" stroke="#2d6a9f" stroke-dasharray="4,3"/>')
    # gate field arrows
    for k in range(4 if not short else 2):
        xx=X+gx0+ (L/5)*(k+1) if not short else X+gx0+L/3*(k+1)
        o.append(f'<line x1="{xx}" y1="62" x2="{xx}" y2="78" stroke="#555" stroke-width="1.2" marker-end="url(#ah)"/>')
    if short:
        o.append(f'<path d="M{X+gx0+2},100 Q{X+125},128 {X+gx1-4},104" fill="none" stroke="#c0392b" stroke-width="2.4" stroke-dasharray="5,3" marker-end="url(#ah)"/>')
        t(X+125,150,'두 공핍층이 거의 맞닿아 게이트 아래로 누설','middle','#c0392b',9.5,True)
        t(X+125,163,'드레인 전압이 장벽을 낮춤 (DIBL)','middle','#c0392b',9.5)
    else:
        t(X+125,150,'채널이 길어 게이트가 장벽을 단단히 쥠','middle','#2e8b57',9.5,True)
panel(10,120,'긴 채널: 게이트가 이김',False)
panel(320,46,'짧은 채널: 드레인이 끼어듦',True)
t(290,190,'파란 점선 = 소스·드레인 주변 공핍층(드레인 쪽은 전압이 걸려 더 넓음)','middle','#2d6a9f',9.5)
open('fig/shortch.svg','w').write(svg(580,198,''.join(o)))

# ---------- Fig: top-view layout ----------
o=[]
rect(20,20,330,200,'#f7f7f7','#bbb')
fins=[55,85,155,185]
for fy in fins: rect(20,fy,330,12,'#e8cfa6','#b5650c',0.6)
gates=[90,175,260]
for gx in gates: rect(gx,30,22,180,GATE,'#333',0.8,0.92)
for gx in gates:
    for fy in fins:
        o.append(f'<rect x="{gx}" y="{fy}" width="22" height="12" fill="{CH}" stroke="#c0392b" stroke-width="1.5"/>')
o.append('<rect x="168" y="48" width="36" height="58" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-dasharray="5,3"/>')
rect(207,117,130,16,'white','#c0392b',0.6,0.95); t(212,129,'← 트랜지스터 1개 (핀 2개)','start','#c0392b',9.5,True)
for gx in gates: t(gx+11,226,'게이트','middle','#333',9)
t(32,64,'핀','start','#7a4a10',9)
t(130,44,'S/D','middle','#2d6a9f',9); t(220,44,'S/D','middle','#2d6a9f',9)
o.append('<text x="370" y="50" font-size="10.5" fill="#222"><tspan x="370" dy="0" font-weight="bold">위에서 내려다본 레이아웃</tspan>'
 '<tspan x="370" dy="20">· 가로 줄무늬 = 핀 (전류 방향)</tspan>'
 '<tspan x="370" dy="17">· 세로 줄 = 게이트</tspan>'
 '<tspan x="370" dy="17">· 둘이 교차하는 칸 = 채널</tspan>'
 '<tspan x="370" dy="17">· 게이트 양옆 핀 = 소스·드레인</tspan>'
 '<tspan x="370" dy="26" font-weight="bold" fill="#c0392b">핀 2개를 게이트 하나가</tspan>'
 '<tspan x="370" dy="16" font-weight="bold" fill="#c0392b">묶으면 폭이 2배인 트랜지스터</tspan>'
 '<tspan x="370" dy="22">→ 폭을 핀 개수로만 조절</tspan>'
 '<tspan x="370" dy="16">  (정수배, "fin quantization")</tspan></text>')
open('fig/layout.svg','w').write(svg(580,236,''.join(o)))

# ---------- Fig: GAA process flow (longitudinal) ----------
o=[]
SIGE='#c7d9a6'; SIN='#c9a3d9'; POLY='#b9b9b9'
PW,PH=140,150
def stack(X,Y,layers_mask=None):
    pass
def pnl(i,title,tag,draw):
    col=i%4; row=i//4
    X=5+col*(PW+5); Y=10+row*(PH+28)
    rect(X,Y,PW,PH,'white','#ccc',0.8)
    t(X+6,Y+15,f'{i+1}. {title}','start','#1b3a5c',9.5,True)
    if tag:
        o.append(f'<rect x="{X+PW-34}" y="{Y+5}" width="30" height="14" rx="3" fill="#e08a1e"/>')
        t(X+PW-19,Y+15.5,tag,'middle','white',8.5,True)
    draw(X,Y)
base=100; lh=8
def layers(X,Y,x0,x1,which='all'):
    for k in range(6):
        y=Y+base-(k+1)*lh
        c=SIGE if k%2==0 else '#f0d9b5'
        rect(X+x0,y,x1-x0,lh,c,'#777',0.4)
def sub(X,Y): rect(X+8,Y+base,PW-16,18,SUB,'#777',0.5)
G0,G1=55,85
def d1(X,Y): sub(X,Y); layers(X,Y,8,PW-8); t(X+PW/2,Y+base+33,'SiGe / Si 교대 에피 성장','middle','#555',7.5)
def d2(X,Y):
    sub(X,Y); layers(X,Y,8,PW-8)
    top=Y+base-6*lh
    rect(X+G0,top-34,G1-G0,34,POLY,'#555',0.6); rect(X+G0-6,top-34,6,34,SIN,'#555',0.5); rect(X+G1,top-34,6,34,SIN,'#555',0.5)
    t(X+(G0+G1)/2,top-14,'더미','middle','#333',8)
    t(X+PW/2,Y+base+33,'임시 게이트로 자리만 잡음','middle','#555',7.5)
def d3(X,Y):
    sub(X,Y); layers(X,Y,G0-6,G1+6)
    top=Y+base-6*lh
    rect(X+G0,top-34,G1-G0,34,POLY,'#555',0.6); rect(X+G0-6,top-34,6,34,SIN,'#555',0.5); rect(X+G1,top-34,6,34,SIN,'#555',0.5)
    t(X+28,Y+80,'파냄','middle','#b5650c',8.5); t(X+PW-28,Y+80,'파냄','middle','#b5650c',8.5); t(X+PW/2,Y+base+33,'게이트 밖 스택을 수직으로 제거','middle','#555',7.5)
def d4(X,Y,cap=True):
    sub(X,Y)
    for k in range(6):
        y=Y+base-(k+1)*lh
        if k%2==0:
            rect(X+G0-6,y,6,lh,SIN,'#777',0.4); rect(X+G1,y,6,lh,SIN,'#777',0.4); rect(X+G0,y,G1-G0,lh,SIGE,'#777',0.4)
        else: rect(X+G0-6,y,G1-G0+12,lh,'#f0d9b5','#777',0.4)
    top=Y+base-6*lh
    rect(X+G0,top-34,G1-G0,34,POLY,'#555',0.6); rect(X+G0-6,top-34,6,34,SIN,'#555',0.5); rect(X+G1,top-34,6,34,SIN,'#555',0.5)
    if cap: t(X+PW/2,Y+base+33,'SiGe 끝만 옆으로 파고 SiN 채움','middle','#555',7.5)
def d5(X,Y):
    d4(X,Y,False)
    t(X+PW/2,Y+base+33,'빈 S/D 자리에 Si를 키워 채움','middle','#555',7.5)
    top=Y+base-6*lh
    rect(X+8,top,G0-6-8,6*lh,SD,'#2d6a9f',0.6); rect(X+G1+6,top,PW-8-(G1+6),6*lh,SD,'#2d6a9f',0.6)
    t(X+28,top+26,'S','middle','#1b3a5c',10,True); t(X+PW-26,top+26,'D','middle','#1b3a5c',10,True)
def d6(X,Y):
    sub(X,Y); top=Y+base-6*lh
    rect(X+8,top,G0-6-8,6*lh,SD,'#2d6a9f',0.6); rect(X+G1+6,top,PW-8-(G1+6),6*lh,SD,'#2d6a9f',0.6)
    for k in range(6):
        y=Y+base-(k+1)*lh
        if k%2==0: rect(X+G0-6,y,6,lh,SIN,'#777',0.4); rect(X+G1,y,6,lh,SIN,'#777',0.4)
        else: rect(X+G0-6,y,G1-G0+12,lh,'#f0d9b5','#777',0.4)
    rect(X+G0-6,top-34,6,34,SIN,'#555',0.5); rect(X+G1,top-34,6,34,SIN,'#555',0.5)
    t(X+(G0+G1)/2,top-14,'빈 공간','middle','#999',7.5)
    t(X+PW/2,Y+base+33,'Si 시트만 공중에 남음','middle','#555',7.5)
def d7(X,Y):
    sub(X,Y); top=Y+base-6*lh
    rect(X+8,top,G0-6-8,6*lh,SD,'#2d6a9f',0.6); rect(X+G1+6,top,PW-8-(G1+6),6*lh,SD,'#2d6a9f',0.6)
    rect(X+G0,top-34,G1-G0,34+6*lh,GATE,'#333',0.6)
    for k in range(6):
        y=Y+base-(k+1)*lh
        if k%2==0: rect(X+G0-6,y,6,lh,SIN,'#777',0.4); rect(X+G1,y,6,lh,SIN,'#777',0.4)
        else: rect(X+G0-6,y,G1-G0+12,lh,CH,'#c0392b',0.8)
    rect(X+G0-6,top-34,6,34,SIN,'#555',0.5); rect(X+G1,top-34,6,34,SIN,'#555',0.5)
    t(X+(G0+G1)/2,top-14,'HKMG','middle','white',8,True)
    t(X+PW/2,Y+base+33,'빈 공간에 HfO₂ + 금속 게이트','middle','#555',7.5)
pnl(0,'초격자 적층','',d1)
pnl(1,'핀·더미 게이트','식각',d2)
pnl(2,'S/D 리세스','식각',d3)
pnl(3,'내부 스페이서','식각',d4)
pnl(4,'S/D 에피 성장','',d5)
pnl(5,'채널 릴리즈','식각',d6)
pnl(6,'HKMG 채움','',d7)
# legend
X=5+3*(PW+5); Y=10+1*(PH+28)
rect(X,Y,PW,PH,'#fafafa','#ccc')
for k,(c,n) in enumerate([('#f0d9b5','Si (채널이 될 층)'),(SIGE,'SiGe (희생층)'),(POLY,'더미 게이트 (poly)'),(SIN,'SiN 스페이서'),(SD,'S/D 에피'),(GATE,'최종 게이트'),(SUB,'기판')]):
    rect(X+10,Y+12+k*17,14,10,c,'#777',0.5); t(X+30,Y+21+k*17,n,'start','#333',8.5)
o.append(f'<rect x="{X+10}" y="{Y+12+7*17}" width="22" height="10" rx="2" fill="#e08a1e"/>'); t(X+38,Y+21+7*17,'= 식각 단계','start','#b5650c',8.5,True)
open('fig/gaaflow.svg','w').write(svg(590,365,''.join(o)))
print('done')
