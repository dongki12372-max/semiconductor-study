from kit import *
import math
# 1 band formation
s=S(580,250)
s.t(140,16,'① 원자가 모일수록 준위가 갈라진다','middle',NAVY,10.5,True)
cols=[(40,1,'원자 1개'),(100,2,'2개'),(160,4,'4개'),(230,40,'N개 (고체)')]
for x,n,lab in cols:
    if n<40:
        for k in range(n):
            y=110 - (n-1)*7 + k*14 if n>1 else 110
            s.line(x-18,y,x+18,y,BLUE,2)
    else:
        s.rect(x-25,80,50,60,'#cfe0f0',BLUE,0.8)
        for k in range(16): s.line(x-25,82+k*3.6,x+25,82+k*3.6,BLUE,0.5)
    s.t(x,175,lab,'middle','#333',10)
s.t(230,72,'= 띠(band)','middle',BLUE,9.5,True)
s.line(10,195,280,195,'#bbb',0.6)
s.t(145,213,'파울리 배타 원리: 같은 상태엔 전자 2개(스핀 ↑↓)까지만','middle','#555',9)
s.t(145,227,'→ 원자 N개가 가까워지면 준위 하나가 N개로 갈라져 띠가 된다','middle','#555',9)
# right panel: E vs distance
s.t(445,16,'② 실리콘: 원자 사이 거리에 따른 에너지','middle',NAVY,10.5,True)
s.line(315,205,570,205,'#333',1,arrow='k'); s.t(565,222,'원자 사이 거리 →','end','#333',9.5)
s.line(315,205,315,25,'#333',1,arrow='k'); s.t(320,32,'에너지','start','#333',9.5)
s.path('M550,70 L420,40 L420,100 Z',f='#cfe0f0',c=BLUE,w=0.8)
s.path('M550,130 L420,100 L420,160 Z',f='#cfe0f0',c=BLUE,w=0.8)
s.path('M420,40 L330,30 L330,78 L420,96 Z',f='#cfe0f0',c=BLUE,w=0.8)
s.path('M420,104 L330,112 L330,180 L420,160 Z',f=BLUE,c=BLUE,w=0.8,op=0.75)
s.line(553,70,568,70,BLUE,2); s.t(570,74,'3p','start',BLUE,9.5)
s.line(553,130,568,130,BLUE,2); s.t(570,134,'3s','start',BLUE,9.5)
s.line(352,25,352,205,'#888',1,'4,3'); s.t(352,218,'Si 실제 간격','middle','#555',9)
s.line(345,82,345,107,ORG,2); s.t(338,98,'E_g','end',ORG,10,True)
s.t(375,58,'전도대','middle',NAVY,9.5,True); s.t(375,70,'(반결합 · 빔)','middle',NAVY,8.5)
s.t(375,145,'가전자대','middle','white',9.5,True); s.t(375,157,'(결합 · 꽉 참)','middle','white',8.5)
s.t(485,192,'멀리 떨어진 원자: 준위만 있음','middle','#555',8.5)
s.save('band_split')

# 2 bandgap trend
s=S(560,200)
s.t(280,16,'같은 4족인데 밴드갭이 다른 이유: 결합이 강할수록 갭이 크다','middle',NAVY,10.5,True)
data=[('C (다이아몬드)',5.5,'0.154 nm','#555'),('Si',1.12,'0.235 nm',BLUE),('Ge',0.66,'0.245 nm','#555'),('α-Sn (회색 주석)',0.08,'0.281 nm','#555')]
for i,(n,eg,bl,c) in enumerate(data):
    y=40+i*34
    s.t(140,y+14,n,'end','#222',10,n=='Si')
    w=eg/6*300
    s.rect(150,y,max(w,2),20,'#cfe0f0' if n!='Si' else BLUE,BLUE,0.8)
    s.t(155+max(w,2),y+14,f'{eg} eV','start','#222',9.5)
    s.t(545,y+14,bl,'end','#555',9.5)
s.t(545,32,'결합 길이','end','#555',9,True)
s.t(280,188,'원자가 작고 결합이 짧고 강할수록 결합·반결합 준위가 멀리 벌어져 갭이 커진다 (아래로 갈수록 금속에 가까움)','middle','#555',8.8)
s.save('eg_trend')

# 3 oxidation
s=S(580,215)
s.t(150,16,'① 열산화로 (퍼니스)','middle',NAVY,10.5,True)
s.rect(20,60,260,80,'#f4f8fb','#7a8a9a',1.2,rx=30)
for k in range(9):
    x=40+k*26
    s.path(f'M{x},50 l6,-8 l6,8 l6,-8 l7,8',c=ORG,w=1.5)
    s.path(f'M{x},150 l6,8 l6,-8 l6,8 l7,-8',c=ORG,w=1.5)
s.t(150,36,'히터: 800–1200 °C','middle',ORG,9,True)
s.rect(80,125,140,6,'#bbb','#777')
for k in range(12): s.rect(88+k*11,72,3,53,'#9aa7b5','#556',0.4)
s.line(-2,100,30,100,BLUE,2,arrow='b'); s.t(2,80,'O₂','start',BLUE,10,True); s.t(2,92,'또는 H₂O','start',BLUE,7.5)
s.line(270,100,298,100,'#777',1.5,arrow='k'); s.t(150,185,'석영관 안을 산소 가스로 채운 상태 = "산소 분위기"','middle','#333',9.5)
s.t(150,200,'Si + O₂ → SiO₂','middle',BLUE,10,True)
# right: cross section
s.t(445,16,'② 산화막은 실리콘을 먹으며 자란다','middle',NAVY,10.5,True)
s.rect(320,107,90,73,SUB,'#777'); s.t(365,150,'Si','middle',BRN,11,True); s.t(365,195,'산화 전','middle','#555',9.5)
s.line(310,107,575,107,RED,1,'5,3'); s.t(318,101,'원래 Si 표면','start',RED,8.5)
s.rect(470,125,90,55,SUB,'#777'); s.rect(470,82,90,43,OX,GRN)
s.t(515,100,'SiO₂','middle','#1b5e20',11,True); s.t(515,160,'Si','middle',BRN,11,True)
s.line(564,82,564,125,'#333',1); s.t(568,108,'t','start','#333',10,True)
s.line(465,82,465,105,BLUE,1); s.line(465,109,465,125,ORG,1); s.t(462,97,'≈56%','end',BLUE,8.5,True); s.t(462,121,'≈44%','end',ORG,8.5,True); s.t(462,135,'(Si 소모)','end',ORG,8)
s.t(515,195,'산화 후','middle','#555',9.5)
s.save('oxidation')

# 4 selectivity
s=S(580,200)
def base(X,hole=None,gouge=0,mask=True,maskthin=False):
    s.rect(X,120,160,45,SUB,'#777'); s.rect(X,75,160,45,OX,GRN)
    if mask:
        mh=8 if maskthin else 16
        s.rect(X,75-mh,60,mh,'#f5c99b','#b5650c'); s.rect(X+100,75-mh,60,mh,'#f5c99b','#b5650c')
    if hole:
        s.rect(X+60,75,40,45,'white','white',0)
        s.line(X+60,75,X+60,120,GRN,0.8); s.line(X+100,75,X+100,120,GRN,0.8)
        if gouge: s.path(f'M{X+60},120 Q{X+80},{120+gouge*2} {X+100},120',f='white',c='#777',w=0.8)
s.t(80+10,20,'① 식각 전','middle',NAVY,10.5,True)
base(10,False); s.rect(70,59,40,16,'white','white',0)
s.t(160,95,'SiO₂','start','#1b5e20',9); s.t(160,145,'Si','start',BRN,9); s.t(150,52,'마스크','end','#b5650c',9)
s.t(290,20,'② 선택비 높음 (이상적)','middle',NAVY,10.5,True)
base(210,True); s.t(290,185,'SiO₂만 뚫고 Si 표면에서 멈춤','middle',GRN,9.5,True)
s.t(490,20,'③ 선택비 낮음','middle',NAVY,10.5,True)
base(410,True,gouge=10,maskthin=True); s.t(490,185,'Si까지 파이고 마스크도 닳음','middle',RED,9.5,True)
s.t(90,185,'구멍을 뚫을 자리만 열어 둠','middle','#555',9.5)
s.save('selectivity')

# 5 CZ
s=S(560,262)
s.t(160,16,'초크랄스키(CZ) 단결정 성장','middle',NAVY,10.5,True)
s.o.append('<g transform="translate(0,22)">')
s.path('M60,150 L60,215 Q60,225 70,225 L250,225 Q260,225 260,215 L260,150',f='#e8eef3',c='#7a8a9a',w=1.5)
s.rect(62,170,196,53,'#f4a460','none',0,0.85); s.t(160,212,'실리콘 융액 (1414 °C 이상)','middle','#7a3000',9.5)
for y in (160,185,210): s.rect(40,y,8,14,ORG,'none'); s.rect(272,y,8,14,ORG,'none')
s.t(30,200,'히터','end',ORG,9)
s.path('M140,170 L140,150 Q140,138 128,130 L128,70 L192,70 L192,130 Q180,138 180,150 L180,170 Z',f='#c9cfd6',c='#556',w=1)
s.rect(155,30,10,40,'#888','#444'); s.t(172,42,'씨결정','start','#333',9)
s.t(160,105,'단결정','middle','#333',9.5,True); s.t(160,118,'잉곳','middle','#333',9.5,True)
s.line(160,30,160,8,BLUE,1.8,arrow='b'); s.t(168,14,'천천히 끌어올림','start',BLUE,9)
s.path('M115,55 A45,10 0 0 0 205,55',c=GRN,w=1.5,arrow='g'); s.t(212,58,'회전','start',GRN,9)
s.o.append('</g>')
# wafer slicing
s.t(430,16,'자르고 → 갈고 → 연마','middle',NAVY,10.5,True)
s.rect(330,60,170,50,'#c9cfd6','#556')
for k in range(1,8): s.line(330+k*21,60,330+k*21,110,'#556',0.8,'3,2')
s.t(415,130,'잉곳 → 얇게 절단','middle','#555',9)
for k in range(3):
    s.path(f'M{360+k*55},190 m-22,0 a22,8 0 1,0 44,0 a22,8 0 1,0 -44,0',f='#dfe6ee',c='#556')
s.t(415,222,'지름 300 mm · 두께 약 775 μm','middle','#333',9.5,True)
s.save('cz')

# 6 donor/acceptor levels
s=S(580,215)
for X,typ in ((20,'n'),(310,'p')):
    s.t(X+125,16,'n형 (인 P 도핑)' if typ=='n' else 'p형 (붕소 B 도핑)','middle',NAVY,10.5,True)
    s.rect(X,28,250,40,'#cfe0f0','none',0); s.line(X,68,X+250,68,BLUE,2); s.t(X+3,45,'전도대','start',NAVY,9.5,True)
    s.rect(X,150,250,40,BLUE,'none',0,0.75); s.line(X,150,X+250,150,BLUE,2); s.t(X+3,180,'가전자대','start','white',9.5,True)
    s.t(X+248,64,'E_c','end',BLUE,9); s.t(X+248,162,'E_v','end','white',9)
    if typ=='n':
        for k in range(6):
            x=X+30+k*35; s.line(x-10,80,x+10,80,RED,2)
            if k<5: s.t(x,96,'⊕','middle',RED,11); s.elec(x+4,52)
            else: s.elec(x,76)
        s.t(X+125,118,'도너 준위: E_c 아래 약 0.045 eV','middle',RED,9.5,True)
        s.t(X+125,133,'상온 열에너지(≈0.026 eV)로 대부분 튀어오름','middle','#555',9)
    else:
        for k in range(6):
            x=X+30+k*35; s.line(x-10,138,x+10,138,GRN,2)
            if k<5: s.t(x,128,'⊖','middle',GRN,11); s.hole(x+4,168)
            else: s.hole(x,142)
        s.t(X+125,100,'억셉터 준위: E_v 위 약 0.045 eV','middle',GRN,9.5,True)
        s.t(X+125,115,'가전자대 전자가 쉽게 올라와 정공을 남김','middle','#555',9)
    s.t(X+125,207,'⊕/⊖ = 이온화된 도펀트 (움직이지 못함)','middle','#555',8.5)
s.line(290,25,290,200,'#ccc',0.8)
s.save('donor')

# 7 drift
s=S(560,200)
s.t(280,14,'전압을 걸면: 밴드가 기울고, 이미 자유로운 캐리어가 경사를 따라 움직인다','middle',NAVY,10.5,True)
s.rect(30,40,30,120,'#ddd','#555'); s.t(45,35,'(−) 극','middle','#333',9.5)
s.rect(500,40,30,120,'#ddd','#555'); s.t(515,35,'(+) 극','middle','#333',9.5)
s.line(60,55,500,105,BLUE,2); s.t(150,58,'E_c','middle',BLUE,9.5)
s.line(60,105,500,155,BLUE,2); s.t(150,118,'E_v','middle',BLUE,9.5)
for k,x in enumerate((140,250,360)):
    y=55+(x-60)*50/440-6; s.elec(x,y)
    s.line(x+8,y+2,x+40,y+6,RED,1.5,arrow='r')
    y2=105+(x-60)*50/440+7; s.hole(x+30,y2)
    s.line(x+22,y2-1,x-8,y2-4,GRN,1.5,arrow='g')
s.t(280,178,'전자는 (+)극 쪽으로 "굴러 내려가고", 정공은 반대로 "떠오른다"','middle','#333',9.5)
s.t(280,195,'전기장은 전자를 가전자대→전도대로 들어 올리지 못한다. 들어 올리는 건 열(또는 빛), 움직이게 하는 건 전기장.','middle','#555',8.8)
s.save('drift')

# 8 pn formation
s=S(580,250)
def region(X,W,typ,carriers=True,ions=True):
    s.rect(X,50,W,90,'#fbe3d9' if typ=='p' else '#dbe8f6','#777')
for X,typ in ((15,'p'),(155,'n')):
    region(X,120,typ)
    for i in range(4):
        for j in range(3):
            x=X+18+i*28; y=68+j*28
            if typ=='p': s.t(x+8,y+4,'⊖','middle','#888',10); s.hole(x-4,y-2)
            else: s.t(x+8,y+4,'⊕','middle','#888',10); s.elec(x-4,y-2)
    s.t(X+60,160,'p형: 정공 많음' if typ=='p' else 'n형: 전자 많음','middle',GRN if typ=='p' else RED,9.5,True)
s.t(145,22,'① 붙이기 전','middle',NAVY,10.5,True)
# joined
X=310
s.t(445,22,'② 붙인 후 (평형)','middle',NAVY,10.5,True)
s.rect(X,50,260,90,'#fbe3d9','#777'); s.rect(X+130,50,130,90,'#dbe8f6','#777')
s.rect(X+95,50,70,90,'#ffffff','#777',0.8,0.85,dash='4,2')
for i in range(3):
    for j in range(3):
        x=X+18+i*28; y=68+j*28; s.t(x+8,y+4,'⊖','middle','#888',10); s.hole(x-4,y-2)
        x=X+185+i*28; s.t(x+8,y+4,'⊕','middle','#888',10); s.elec(x-4,y-2)
for j in range(3):
    y=68+j*28; s.t(X+110,y+4,'⊖','middle',GRN,13,True); s.t(X+150,y+4,'⊕','middle',RED,13,True)
s.line(X+150,148,X+108,148,'#333',1.8,arrow='k'); s.t(X+130,163,'내부 전기장 E','middle','#333',9,True)
s.t(X+130,185,'공핍층','middle',NAVY,10,True); s.t(X+130,198,'(움직이는 캐리어 없음,','middle','#555',8.5); s.t(X+130,210,'고정 이온만 남음)','middle','#555',8.5)
s.t(290,238,'경계에서 전자와 정공이 건너가 만나 사라지고(재결합), 남은 이온이 만드는 전기장이 더 이상의 확산을 막는다','middle','#555',9)
s.save('pn_form')

# 9 pn band
s=S(560,200)
s.t(280,16,'PN 접합의 밴드 그림: 전자가 넘어야 할 "언덕"이 생긴다','middle',NAVY,10.5,True)
def bands(dy):
    s.path(f'M30,{50} L220,{50} C270,{50} 290,{50+dy} 340,{50+dy} L530,{50+dy}',c=BLUE,w=2)
    s.path(f'M30,{110} L220,{110} C270,{110} 290,{110+dy} 340,{110+dy} L530,{110+dy}',c=BLUE,w=2)
bands(50)
s.line(30,105,530,105,'#888',1,'5,3'); s.t(535,109,'E_F','start','#555',9)
s.t(40,45,'E_c','start',BLUE,9); s.t(40,124,'E_v','start',BLUE,9); s.t(535,96,'E_c','start',BLUE,9)
s.t(120,180,'p 쪽','middle',GRN,10,True); s.t(440,180,'n 쪽','middle',RED,10,True)
for x in (380,410,440,470): s.elec(x,94)
for x in (90,120,150): s.hole(x,116)
s.line(500,50,500,100,ORG,1.5); s.line(495,50,505,50,ORG,1); s.t(505,70,'장벽 qV_bi','start',ORG,9.5,True)
s.t(505,84,'(Si ≈ 0.7 V)','start',ORG,8.5)
s.line(220,40,220,185,'#ccc',0.8,'3,3'); s.line(340,40,340,185,'#ccc',0.8,'3,3'); s.t(280,192,'공핍층','middle','#555',9)
s.save('pn_band')

# 10 pn bias + IV
s=S(580,230)
def mini(X,title,dy,wd,col,note):
    s.t(X+90,16,title,'middle',col,10.5,True)
    s.path(f'M{X},{45} L{X+80-wd/2},45 C{X+90},45 {X+90},{45+dy} {X+100+wd/2},{45+dy} L{X+180},{45+dy}',c=BLUE,w=2)
    s.path(f'M{X},{95} L{X+80-wd/2},95 C{X+90},95 {X+90},{95+dy} {X+100+wd/2},{95+dy} L{X+180},{95+dy}',c=BLUE,w=2)
    for x in (X+130,X+150,X+170): s.elec(x,45+dy-6)
    s.t(X+90,175,note,'middle','#333',9)
mini(10,'순방향 (p에 +)',20,20,GRN,'언덕 낮아짐 → 전자가 넘어감')
s.line(120,58,80,52,RED,1.5,arrow='r')
s.t(100,190,'공핍층 좁아짐 · 전류 큼','middle',GRN,9,True)
mini(200,'역방향 (n에 +)',85,70,RED,'언덕 높아짐 → 거의 못 넘음')
s.t(290,190,'공핍층 넓어짐 · 전류 ≈ 0','middle',RED,9,True)
# IV
X0,Y0=470,150
s.t(480,16,'전류–전압 특성','middle',NAVY,10.5,True)
s.line(390,Y0,570,Y0,'#333',1,arrow='k'); s.line(X0,200,X0,30,'#333',1,arrow='k')
s.t(568,Y0+14,'V','end','#333',9.5); s.t(X0+5,38,'I','start','#333',9.5)
pts=[]
for i in range(0,101):
    v=-0.8+i*0.016*0.95
    I=0.6*(math.exp(v/0.06)-1)
    y=Y0-min(I,110); x=X0+v*90
    pts.append(f'{x:.1f},{y:.1f}')
s.path('M'+' L'.join(pts),c=RED,w=2)
s.line(X0+0.7*90,Y0+4,X0+0.7*90,Y0-4,'#333',1); s.t(X0+0.7*90,Y0+16,'~0.7 V','middle','#333',8.5)
s.t(400,Y0+30,'역방향: 거의 0','start','#555',8.5); s.t(X0-5,60,'순방향:','end','#555',8.5); s.t(X0-5,72,'지수적 증가','end','#555',8.5)
s.save('pn_bias')

# 11 Moore chart
s=S(560,280)
L,R,T,B=70,540,30,240
s.t(300,16,'무어의 법칙: 칩 하나의 트랜지스터 수 (로그 눈금)','middle',NAVY,10.5,True)
def X(y): return L+(y-1970)/(2025-1970)*(R-L)
def Y(n): return B-(math.log10(n)-3)/(12-3)*(B-T)
s.line(L,B,R,B,'#333',1); s.line(L,B,L,T,'#333',1)
for e in range(3,13):
    s.line(L-4,Y(10**e),R,Y(10**e),'#eee',0.6); s.t(L-6,Y(10**e)+3,f'10^{e}','end','#555',8)
for yr in range(1970,2030,10): s.t(X(yr),B+14,str(yr),'middle','#555',8.5)
s.line(X(1971),Y(2300),X(2024),Y(2300*2**((2024-1971)/2)),ORG,1.5,'6,4')
s.t(X(2004),Y(2300*2**((2004-1971)/2))-30,'2년마다 2배 추세선','middle',ORG,9,True)
data=[(1971,2300,'4004'),(1978,29000,'8086'),(1985,275000,'386'),(1993,3.1e6,'Pentium'),(2000,4.2e7,'Pentium 4'),(2006,2.91e8,'Core 2 Duo'),(2012,1.4e9,'Ivy Bridge'),(2020,1.6e10,'Apple M1'),(2022,1.14e11,'M1 Ultra')]
for yr,n,lab in data:
    s.circ(X(yr),Y(n),4,BLUE); s.t(X(yr)+6,Y(n)+12,lab,'start','#333',8)
s.t(300,268,'1971년 2,300개 → 2022년 1,000억 개 이상: 약 50년간 대략 2년마다 2배','middle','#555',9)
s.save('moore')
print('A ok')
