from kit import *
import math
def spin(s,x,y,up=True,c=RED):
    s.line(x,y+7 if up else y-7,x,y-7 if up else y+7,c,1.8,arrow='r')

# ---- periodic table excerpt + Si atom
s=S(580,250)
s.t(170,16,'주기율표 일부: 이 교재에 나오는 원소들','middle',NAVY,10.5,True)
els=[['B','C','N','O','F'],['Al','Si','P','S','Cl'],['Ga','Ge','As','Se','Br'],['In','Sn','Sb','Te','I']]
grp=['13족','14족','15족','16족','17족']; per=['2주기','3주기','4주기','5주기']
role={'B':('#d9ecd9','p형 도펀트'),'Si':(BLUE,'주인공'),'P':('#f8d7c4','n형 도펀트'),'As':('#f8d7c4','n형 도펀트'),'Ge':('#e6dcf2','SiGe'),'C':('#eee','SiC·CFx'),'O':('#cfeedd','SiO₂'),'N':('#cfeedd','Si₃N₄'),'F':('#ffe2bf','식각 가스'),'Cl':('#ffe2bf','식각 가스'),'Br':('#ffe2bf','식각 가스(HBr)'),'Sn':('#eee','')}
for j,g in enumerate(grp): s.t(60+j*56+26,40,g,'middle','#555',9)
for i,row in enumerate(els):
    s.t(25,70+i*46,per[i],'middle','#555',8.5)
    for j,e in enumerate(row):
        x=60+j*56; y=48+i*46
        col,lab=role.get(e,('white',''))
        s.rect(x,y,52,42,col,'#888',0.8,rx=3)
        s.t(x+26,y+22,e,'middle','white' if e=='Si' else '#222',14,True)
        if lab: s.t(x+26,y+36,lab,'middle','white' if e=='Si' else '#444',7.3)
s.t(170,240,'14족 = 바깥 전자 4개. 한 칸 왼쪽(13족)은 3개 → p형, 한 칸 오른쪽(15족)은 5개 → n형','middle','#333',8.8)
# Si atom
cx,cy=455,125
s.t(cx,16,'실리콘 원자 (원자번호 14)','middle',NAVY,10.5,True)
for r,n,c in ((26,2,'#999'),(50,8,'#999'),(76,4,RED)):
    s.circ(cx,cy,r,'none','#bbb',1)
    for k in range(n):
        a=2*math.pi*k/n+0.3
        s.circ(cx+r*math.cos(a),cy+r*math.sin(a),5 if c==RED else 4,c)
s.circ(cx,cy,14,'#f1e3c8',BRN); s.t(cx,cy+4,'+14','middle',BRN,9,True)
s.t(cx,215,'1s² 2s² 2p⁶ | 3s² 3p²','middle','#333',9.5)
s.t(cx,230,'안쪽 10개는 핵에 꽉 묶임, 바깥 4개(빨강)가 결합·전도의 주인공','middle',RED,8.5)
s.save('periodic')

# ---- H2 bonding
s=S(580,270)
s.t(150,16,'① 두 1s 파동함수를 더하는 두 가지 방법','middle',NAVY,10.5,True)
def wave(y0,sign,col,label,sub,off=18):
    s.line(20,y0,280,y0,'#ccc',0.8)
    for xa in (110,190): s.circ(xa,y0,3.5,'#333'); 
    pts=[]
    for i in range(0,261):
        x=20+i; a=math.exp(-abs(x-110)/22); b=sign*math.exp(-abs(x-190)/22)
        pts.append(f'{x},{y0-(a+b)*38:.1f}')
    s.path('M'+' L'.join(pts),c=col,w=2)
    s.t(150,y0+off,label,'middle',col,9.5,True); s.t(150,y0+off+13,sub,'middle','#555',8.5)
wave(75,1,BLUE,'같은 부호로 더함 → 결합 상태 σ','두 핵 사이에 전자 확률이 쌓임 → 두 핵을 끌어당김 → 에너지 낮음')
s.t(110,90,'H','middle','#333',9); s.t(190,90,'H','middle','#333',9)
wave(165,-1,RED,'반대 부호로 더함 → 반결합 상태 σ*','가운데에 마디(확률 0) → 핵끼리 반발 → 에너지 높음',off=58)
# energy diagram
s.t(440,16,'② 에너지 그림: 자리(상태) 2개, 전자 2개','middle',NAVY,10.5,True)
s.line(320,240,320,30,'#333',1,arrow='k'); s.t(325,36,'에너지','start','#333',9)
s.line(340,130,385,130,'#333',2); s.t(362,150,'H 원자 A','middle','#333',8.5); spin(s,362,122)
s.line(500,130,545,130,'#333',2); s.t(522,150,'H 원자 B','middle','#333',8.5); spin(s,522,122,False)
s.line(415,80,470,80,RED,2.5); s.t(442,72,'σ* (빔)','middle',RED,9,True)
s.line(415,185,470,185,BLUE,2.5); s.t(442,205,'σ (전자 2개, 스핀 ↑↓)','middle',BLUE,9,True)
spin(s,435,177); spin(s,450,177,False)
for x1,x2 in ((385,415),(500,470)):
    s.line(x1,130,x2,80,'#999',0.8,'3,3'); s.line(x1,130,x2,185,'#999',0.8,'3,3')
s.t(442,228,'두 전자가 낮은 σ에 함께 들어가 에너지가 내려감 = 결합이 생김','middle','#333',8.5)
s.t(442,242,'"준위가 갈라진다" = 전자가 아니라 "자리"가 둘로 갈라진다는 뜻','middle',ORG,8.5,True)
s.save('h2_bond')

# ---- coupled oscillators
s=S(580,250)
s.t(290,16,'물리학도용 비유: 결합된 진자. 연결하면 진동수가 갈라진다','middle',NAVY,10.5,True)
def pend(x0,n,phase,title,sub,col):
    s.t(x0+n*22,40,title,'middle',col,9.5,True)
    s.line(x0-10,50,x0+n*44-24,50,'#555',2)
    for k in range(n):
        x=x0+k*44; dx=(10 if phase[k]>0 else -10)
        s.line(x,50,x+dx,115,'#555',1.2); s.circ(x+dx,120,8,col)
        if k<n-1:
            nx=x0+(k+1)*44+(10 if phase[k+1]>0 else -10)
            s.path(f'M{x+dx+8},100 '+' '.join(f'l{(nx-x-dx-16)/8:.1f},{(-5 if j%2 else 5)}' for j in range(8)),c=ORG,w=1.2)
    s.t(x0+n*22-11,148,sub,'middle','#333',8.5)
pend(40,2,[1,1],'같은 방향으로 흔들림','스프링이 안 늘어남 → 느림 (낮은 진동수)',BLUE)
pend(220,2,[1,-1],'반대 방향으로 흔들림','스프링이 늘어남 → 빠름 (높은 진동수)',RED)
s.t(450,40,'진자 N개를 연결하면','middle',NAVY,9.5,True)
for k in range(12): s.line(395,60+k*6,505,60+k*6,BLUE if k<6 else RED,1.2)
s.t(450,148,'진동 모드 N개가 촘촘히 → 띠','middle','#333',8.5)
s.line(15,165,565,165,'#ddd',1)
for i,l in enumerate(['진자 하나의 진동수 = 원자의 준위 하나.  스프링 = 파동함수의 겹침(결합).',
    '진자 2개를 이으면 "같이 흔들림 / 엇갈려 흔들림" 두 모드가 생기고 진동수가 위아래로 갈라진다 (결합 / 반결합).',
    '진자 N개면 모드도 정확히 N개다. 모드 수는 진자 수를 넘지도 모자라지도 않는다 → 원자 N개 = 상태 N개.',
    '스프링이 셀수록(원자가 가까울수록) 진동수가 더 크게 갈라진다 → 결합이 강할수록 갭이 크다 (1.1.4).']):
    s.t(20,185+i*17,l,'start','#333',9)
s.save('coupled')

# ---- VB/CB real space
s=S(580,250)
s.t(150,16,'① 실제 공간: 결정 속 실리콘 원자와 결합','middle',NAVY,10.5,True)
for i in range(4):
    for j in range(4):
        x=40+i*65; y=45+j*50
        if i<3: s.line(x+12,y-3,x+53,y-3,'#bbb',1); s.line(x+12,y+3,x+53,y+3,'#bbb',1)
        if j<3: s.line(x-3,y+12,x-3,y+38,'#bbb',1); s.line(x+3,y+12,x+3,y+38,'#bbb',1)
for i in range(4):
    for j in range(4):
        x=40+i*65; y=45+j*50
        s.circ(x,y,11,'#cfe0f0',BLUE); s.t(x,y+4,'Si','middle',NAVY,8.5)
        if i<3:
            for dx in (22,38):
                if not (i==1 and j==1 and dx==38): s.circ(x+dx,y,2.6,'#555')
        if j<3:
            for dy in (20,30): s.circ(x,y+dy,2.6,'#555')
s.hole(143,95); s.elec(200,128)
s.path('M200,128 Q230,140 245,175',c=RED,w=1.3,dash='3,2',arrow='r')
s.t(150,225,'검은 점 = 결합에 묶인 전자. 하나가 풀려나(빨강) 돌아다니고, 빈자리(정공) 남음','middle','#333',8.5)
# right band
s.t(440,16,'② 같은 상황을 에너지 띠로 보면','middle',NAVY,10.5,True)
s.rect(330,40,220,55,'#cfe0f0','none',0); s.line(330,95,550,95,BLUE,2)
s.rect(330,150,220,60,BLUE,'none',0,0.75); s.line(330,150,550,150,BLUE,2)
s.t(335,55,'전도대','start',NAVY,9.5,True); s.t(335,200,'가전자대','start','white',9.5,True)
s.elec(440,80); s.hole(440,163)
s.line(440,155,440,96,ORG,1.2,'3,2'); 
s.t(545,58,'결합에서 풀려나 결정 전체를','end',NAVY,8.3); s.t(545,70,'자유롭게 다니는 전자의 상태','end',NAVY,8.3)
s.t(545,180,'결합에 묶인 전자들의 상태','end','white',8.3); s.t(545,192,'(원래 꽉 참)','end','white',8.3)
s.t(440,228,'전도대는 "비어 있는 자리"다. 전자가 들어오면 그 전자가 전류를 나른다','middle','#333',8.5)
s.t(440,242,'(정공은 가전자대에서 전류를 나른다)','middle','#555',8.3)
s.save('vbcb')

# ---- Fermi
s=S(580,240)
s.t(140,16,'① 페르미–디랙 분포: 에너지 E에 전자가 있을 확률','middle',NAVY,10.5,True)
L,R,T,B=40,250,40,200
s.line(L,B,R,B,'#333',1,arrow='k'); s.line(L,B,L,T-10,'#333',1,arrow='k')
s.t(R,B+15,'에너지 E →','end','#333',9); s.t(L-4,T,'1','end','#333',9); s.t(L-4,(T+B)/2+3,'1/2','end','#333',9); s.t(L-4,B,'0','end','#333',9)
xf=150
s.path(f'M{L},{T} L{xf},{T} L{xf},{B} L{R},{B}',c='#999',w=1.5,dash='5,3')
pts=[]
for i in range(0,211):
    x=L+i; f=1/(1+math.exp((x-xf)/9)); pts.append(f'{x},{B-f*(B-T):.1f}')
s.path('M'+' L'.join(pts),c=RED,w=2.2)
s.line(xf,B,xf,T-10,ORG,1,'3,3'); s.t(xf,T-14,'E_F','middle',ORG,10,True)
s.t(85,T+16,'0 K: 계단','middle','#777',8.5); s.t(205,(T+B)/2,'상온: 수 k_BT 폭으로','middle',RED,8.5); s.t(205,(T+B)/2+12,'부드럽게 번짐','middle',RED,8.5)
s.t(145,228,'E_F = 확률이 정확히 1/2인 "수위". 그 에너지에 실제 상태가 없어도 된다','middle','#333',8.5)
# right three band diagrams
s.t(430,16,'② 반도체에서 E_F의 위치','middle',NAVY,10.5,True)
for k,(lab,y,col) in enumerate((('순수 (진성)',117,'#555'),('n형',68,RED),('p형',166,GRN))):
    X=300+k*92
    s.rect(X,40,70,20,'#cfe0f0','none',0); s.line(X,60,X+70,60,BLUE,1.5)
    s.rect(X,175,70,20,BLUE,'none',0,0.75); s.line(X,175,X+70,175,BLUE,1.5)
    s.line(X-4,y,X+74,y,ORG,1.6,'5,3')
    s.t(X+35,213,lab,'middle',col,9.5,True)
    if k==1:
        for xx in (X+15,X+35,X+55): s.elec(xx,50,3.8)
    if k==2:
        for xx in (X+15,X+35,X+55): s.hole(xx,185,3.8)
s.t(296,64,'E_c','end',BLUE,8.5); s.t(296,179,'E_v','end',BLUE,8.5)
s.t(430,232,'전자가 많을수록 수위(E_F)가 전도대 쪽으로 올라간다','middle','#333',8.5)
s.save('fermi')

# ---- pn IV with breakdown
s=S(580,240)
s.t(290,16,'다이오드의 전류–전압 특성 (항복 포함, 개념도)','middle',NAVY,10.5,True)
X0,Y0=360,120
s.line(40,Y0,560,Y0,'#333',1,arrow='k'); s.line(X0,225,X0,30,'#333',1,arrow='k')
s.t(556,Y0+15,'전압 V','end','#333',9); s.t(X0+5,38,'전류 I','start','#333',9)
pts=[]
for i in range(0,121):
    v=i/120*0.8; I=0.25*(math.exp(v/0.06)-1); y=Y0-min(I,85); x=X0+v*170
    pts.append(f'{x:.1f},{y:.1f}')
s.path('M'+' L'.join(pts),c=RED,w=2.2)
s.path(f'M{X0},{Y0} L{X0-200},{Y0+3} Q{X0-215},{Y0+5} {X0-222},{Y0+40} L{X0-232},{Y0+100}',c=RED,w=2.2)
s.line(X0-218,Y0-5,X0-218,Y0+5,'#333',1); s.t(X0-218,Y0-10,'−V_BR','middle','#333',9,True)
s.t(X0+125,60,'순방향: 약 0.6~0.7 V부터 급증','middle',GRN,9,True)
s.t(X0-100,Y0-14,'역방향: 거의 0 (아주 작은 누설)','middle','#555',9)
s.t(X0-250,Y0+70,'항복','end',RED,10,True); s.t(X0-250,Y0+84,'전기장이 너무 세져','end','#555',8.5); s.t(X0-250,Y0+96,'전류가 터짐','end','#555',8.5)
s.t(290,234,'실제 V_BR은 도핑에 따라 수 V~수백 V로, 순방향 문턱(0.7 V)보다 훨씬 크다. 그림은 비율을 무시하고 그렸다.','middle','#555',8.5)
s.save('pn_iv')

# ---- CMOS water analogy
s=S(580,250)
def tank(X,inp):
    s.t(X+130,16,f'입력 {inp} → 출력 {1-inp}','middle',NAVY,10.5,True)
    s.rect(X+80,30,100,30,'#cfe0f0',BLUE); s.t(X+130,50,'V_DD = 물탱크 (1)','middle',NAVY,9)
    top_open = inp==0
    s.rect(X+120,60,20,40,'white','#555')
    s.rect(X+105,75,50,10,GRN if top_open else '#ccc','#333',0.8); s.t(X+190,84,'PMOS 밸브: '+('열림' if top_open else '닫힘'),'start',GRN if top_open else '#888',9,True)
    s.rect(X+95,100,70,55,'white','#333',1.2)
    if top_open: s.rect(X+96,108,68,46,'#9ec5ee','none',0)
    s.t(X+130,135,'출력 = '+('1 (참)' if top_open else '0 (빔)'),'middle',RED,9.5,True)
    s.rect(X+120,155,20,40,'white','#555')
    s.rect(X+105,170,50,10,GRN if not top_open else '#ccc','#333',0.8); s.t(X+190,179,'NMOS 밸브: '+('열림' if not top_open else '닫힘'),'start',GRN if not top_open else '#888',9,True)
    s.rect(X+80,195,100,25,'#ddd','#777'); s.t(X+130,212,'GND = 하수구 (0)','middle','#333',9)
    if top_open: s.line(X+130,62,X+130,104,BLUE,2,arrow='b')
    else: s.line(X+130,150,X+130,197,BLUE,2,arrow='b')
tank(-20,0); tank(270,1)
s.t(290,240,'두 밸브는 같은 입력으로 움직이지만 성질이 반대라 항상 하나만 열린다 → 탱크와 하수구가 직접 이어지는 일이 없다','middle','#333',8.5)
s.save('cmos_water')

# ---- CMOS cross-section
s=S(580,270)
s.t(290,16,'CMOS 인버터의 실제 단면: 한 웨이퍼 위에 NMOS와 PMOS를 나란히','middle',NAVY,10.5,True)
s.rect(20,150,540,90,'#fbe3d9','#777'); s.t(30,232,'p형 기판','start',GRN,9.5,True)
s.path('M300,150 L300,205 Q300,220 315,220 L525,220 Q540,220 540,205 L540,150',f='#dbe8f6',c=BLUE,w=1)
s.t(420,214,'n-well (n형 우물)','middle',BLUE,9.5,True)
for x in (20,280,540-20):
    s.rect(x,150,20,40,STI,'#777')
def fet(x,typ):
    c=SD if typ=='n' else '#bfe0bf'; lab='n⁺' if typ=='n' else 'p⁺'
    s.rect(x,150,55,22,c,'#555'); s.t(x+27,165,lab,'middle','#333',9,True)
    s.rect(x+120,150,55,22,c,'#555'); s.t(x+147,165,lab,'middle','#333',9,True)
    s.rect(x+60,144,55,6,OX,GRN); s.rect(x+60,118,55,26,GATE,'#333'); s.t(x+87,135,'G','middle','white',10,True)
fet(55,'n'); fet(330,'p')
s.t(147,190,'NMOS','middle',NAVY,10,True); s.t(422,190,'PMOS','middle',NAVY,10,True)
# wires
W='#333'
s.line(82,150,82,100,W,1.5); s.t(82,94,'GND','middle',W,9,True)          # NMOS source
s.line(357,150,357,80,W,1.5); s.line(357,80,357,60,W,1.5); s.t(357,55,'V_DD','middle',W,9,True)  # PMOS source
s.line(202,150,202,100,W,1.5); s.line(477,150,477,100,W,1.5); s.line(202,100,477,100,RED,1.8); s.line(477,100,540,100,RED,1.8,arrow='r'); s.t(545,104,'출력','start',RED,9.5,True)
s.line(142,118,142,75,W,1.5); s.line(417,118,417,75,W,1.5); s.line(142,75,417,75,BLUE,1.8); s.line(142,75,40,75,BLUE,1.8); s.t(36,79,'입력','end',BLUE,9.5,True)
s.t(290,256,'두 게이트는 입력에, 두 드레인은 출력에 묶인다. PMOS는 n형 우물 안에 만들어야 하므로 공정이 NMOS 단독보다 복잡하다.','middle','#555',8.5)
s.save('cmos_xs')

# ---- current formula pipe
s=S(580,250)
s.t(290,16,'전류 = (채널 속 전하량) × (전하가 달리는 속도)','middle',NAVY,10.5,True)
s.rect(90,110,400,40,'#f5d3c4',RED,1); s.rect(70,110,20,40,SD,'#555'); s.rect(490,110,20,40,SD,'#555')
s.t(80,170,'S','middle',NAVY,10,True); s.t(500,170,'D','middle',NAVY,10,True)
s.rect(90,94,400,8,OX,GRN); s.rect(90,60,400,34,GATE,'#333'); s.t(290,82,'게이트 (전압 V_GS)','middle','white',9.5,True)
for k in range(14): s.elec(110+k*28,130,4)
s.line(110,160,470,160,'#333',1,arrow='k'); s.t(290,175,'길이 L','middle','#333',9)
s.t(510,130,'→','start',RED,14,True)
s.t(300,198,'① 전하 밀도 Q = C_ox (V_GS − V_th)     ② 속도 v = μE = μ V_DS / L     ③ 폭 W만큼 나란히','middle','#333',9.5)
s.t(300,220,'I_D ≈ W × Q × v = μ C_ox (W/L)(V_GS − V_th) V_DS      (선형 영역)','middle',RED,10,True)
s.t(300,240,'포화 영역에서는 드레인 근처 채널이 얇아지며(핀치오프) ½ μ C_ox (W/L)(V_GS − V_th)² 꼴이 된다','middle','#555',8.5)
s.t(40,140,'μ','middle',BLUE,12,True); s.t(40,155,'얼마나','middle',BLUE,7.5); s.t(40,165,'잘 달리나','middle',BLUE,7.5)
s.t(540,82,'C_ox','middle',GRN,11,True); s.t(540,96,'= ε/t_ox','middle',GRN,8.5)
s.save('id_pipe')

# ---- Id-Vds
s=S(560,230)
L,R,T,B=60,330,30,200
s.t(200,16,'I_D–V_DS 곡선 (게이트 전압별)','middle',NAVY,10.5,True)
s.line(L,B,R,B,'#333',1,arrow='k'); s.line(L,B,L,T,'#333',1,arrow='k')
s.t(R,B+15,'V_DS','end','#333',9); s.t(L-5,T+5,'I_D','end','#333',9)
for k,vg in enumerate((0.4,0.6,0.8,1.0)):
    vov=vg-0.3; pts=[]
    for i in range(0,101):
        vd=i/100*1.2; 
        I=(vov*vd-vd*vd/2) if vd<vov else vov*vov/2
        I*=(1+0.05*vd)
        pts.append(f'{L+vd/1.2*(R-L-10):.1f},{B-I/0.26*(B-T-10):.1f}')
    s.path('M'+' L'.join(pts),c=[ '#9ec5ee','#5f9bd6',BLUE,NAVY][k],w=2)
    s.t(R-5,B-(vov*vov/2*1.06)/0.26*(B-T-10)-5,f'V_GS={vg}','end','#333',8)
s.path('M'+' L'.join(f'{L+v/1.2*(R-L-10):.1f},{B-(v*v/2*(1+0.05*v))/0.26*(B-T-10):.1f}' for v in [i*0.0075 for i in range(0,101)]),c=ORG,w=1.2,dash='4,3')
s.t(L+35,B-25,'선형','middle','#555',9); s.t(L+190,B-40,'포화','middle','#555',9)
s.rect(360,40,190,160,'#f6f8fb','#ccd',0.8,rx=6)
for i,l in enumerate(['선형 영역: 채널이 균일한','저항처럼 동작 (I ∝ V_DS)','포화 영역: 드레인 쪽 채널이','얇아져 끊기며(핀치오프)','V_DS를 올려도 전류가 거의 일정','','디지털 스위치는 주로','포화 영역 전류(I_on)로 평가']):
    s.t(370,62+i*17,l,'start','#333',9)
s.save('id_vds')

# ---- STI flow
s=S(590,175)
def pn(i,title,tag,draw):
    X=5+i*117
    s.rect(X,22,112,128,'white','#ccc',0.8); s.t(X+5,36,f'{i+1}. {title}','start',NAVY,8.8,True)
    if tag: s.rect(X+76,26,32,13,ORG,'none',0,rx=3); s.t(X+92,36,tag,'middle','white',8,True)
    draw(X)
def si(X,trench=False,fill=False,sinpad=True,cmp=False,final=False):
    s.rect(X+6,70,100,60,SUB,'#777',0.5)
    if trench:
        s.rect(X+40,70,32,32,'white' if not fill else OX,'#777' if not fill else GRN,0.5)
    if sinpad and not final:
        s.rect(X+6,64,34,6,'#e6e6e6','#777',0.4); s.rect(X+72,64,34,6,'#e6e6e6','#777',0.4)
        s.rect(X+6,54,34,10,SIN,'#7d4a92',0.5); s.rect(X+72,54,34,10,SIN,'#7d4a92',0.5)
        if not trench: s.rect(X+40,64,32,6,'#e6e6e6','#777',0.4); s.rect(X+40,54,32,10,SIN,'#7d4a92',0.5)
    if fill and not cmp: s.rect(X+6,44,100,10,OX,GRN,0.5); s.rect(X+40,54,32,16,OX,GRN,0.5)
    if cmp and not final: s.rect(X+40,54,32,16,OX,GRN,0.5)
    if final: s.rect(X+40,62,32,8,OX,GRN,0.5)
pn(0,'SiN·패드 산화막','',lambda X:(si(X),s.rect(X+6,44,34,10,'#f5c99b','#b5650c',0.5),s.rect(X+72,44,34,10,'#f5c99b','#b5650c',0.5),s.t(X+56,145,'마스크(PR)로 자리 표시','middle','#555',7.5)))
pn(1,'트렌치 식각','식각',lambda X:(si(X,True),s.t(X+56,145,'SiN을 마스크로 Si를 팜','middle','#555',7.5)))
pn(2,'SiO₂ 채움','',lambda X:(si(X,True,True),s.t(X+56,145,'산화막을 넘치게 증착','middle','#555',7.5)))
pn(3,'CMP','',lambda X:(si(X,True,True,cmp=True),s.t(X+56,145,'SiN에서 멈추게 연마','middle','#555',7.5)))
pn(4,'SiN 제거','식각',lambda X:(si(X,True,True,final=True),s.t(X+56,145,'습식(인산)으로 SiN 제거','middle','#555',7.5)))
s.t(295,168,'완성된 산화막 담장(STI)이 양옆 트랜지스터를 전기적으로 갈라놓는다','middle','#333',9)
s.save('sti')

# ---- CFET
s=S(580,250)
s.t(145,16,'GAA로 만든 CMOS: 옆으로 나란히','middle',NAVY,10.5,True)
s.t(435,16,'CFET: 위아래로 쌓기','middle',NAVY,10.5,True)
def stack(x,y,col,lab):
    for k in range(3): s.rect(x,y+k*20,60,10,col,'#555',0.6)
    s.t(x+30,y+75,lab,'middle','#333',9,True)
s.rect(20,190,250,25,SUB,'#777'); s.rect(30,40,230,150,GATE,'#333',0.8,0.85)
stack(50,90,'#f5d3c4','NMOS 시트'); stack(170,90,'#cfe8cf','PMOS 시트')
s.line(150,85,150,185,'#e6e6e6',3,'4,3'); s.t(150,60,'공유 게이트','middle','white',9,True)
s.line(30,232,260,232,'#333',1,arrow='k'); s.t(145,247,'셀 폭 = NMOS + PMOS + 간격','middle','#333',9)
s.rect(330,190,210,25,SUB,'#777'); s.rect(370,30,130,160,GATE,'#333',0.8,0.85)
stack(405,40,'#f5d3c4',''); s.t(520,62,'NMOS 시트','start','#333',9,True); s.t(520,74,'(위층)','start','#333',8.5); s.rect(395,113,80,10,'#dfe7ef','#777',0.6); s.t(510,121,'절연 분리층','start','#555',8.5)
stack(405,128,'#cfe8cf','')
s.t(435,195+0,'','middle')
s.t(520,170,'PMOS 시트','start','#333',9,True); s.t(520,182,'(아래층)','start','#333',8.5)
s.line(370,232,500,232,'#333',1,arrow='k'); s.t(435,247,'셀 폭 ≈ 절반 가까이','middle',RED,9,True)
s.save('cfet')
print('C ok')
