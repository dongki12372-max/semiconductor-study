from kit import *
import math
# Id-Vg
s=S(560,250)
L,R,T,B=70,330,30,215
s.t(200,16,'I_D–V_GS 곡선 (세로축 로그)','middle',NAVY,10.5,True)
s.line(L,B,R,B,'#333',1,arrow='k'); s.line(L,B,L,T,'#333',1,arrow='k')
s.t(R,B+30,'게이트 전압 V_GS →','end','#333',9.5); s.t(L-6,T+4,'log I_D','end','#333',9)
pts=[]
for i in range(101):
    v=i/100*1.0
    logI=-12+ v/0.065 if v<0.38 else (-12+0.38/0.065)+ (1-math.exp(-(v-0.38)/0.12))*2.2
    x=L+v*240; y=B-(logI+12)/9*(B-T)
    pts.append(f'{x:.1f},{y:.1f}')
s.path('M'+' L'.join(pts),c=RED,w=2.2)
vth=0.38; xv=L+vth*240
s.line(xv,B,xv,T+10,'#888',1,'4,3'); s.t(xv,B+16,'V_th','middle','#333',9.5,True)
s.t(L+2,B-8,'I_off','start',BLUE,9,True); s.t(L+240-2,T+36,'I_on','end',BLUE,9,True)
s.t(L+175,B-60,'서브문턱 영역 (V_th 아래)','middle','#555',9)
s.t(L+175,B-46,'기울기 한계 ≈ 60 mV/dec','middle',ORG,9,True)
s.t(L+175,B-32,'(상온 열적 한계)','middle','#555',8.5)
s.line(L+120,B-55,L+60,B-70,ORG,0.8)
s.line(L+240,B,L+240,B-4,'#333',1); s.t(L+240,B+16,'V_DD','middle','#333',9)
# right explanation
s.rect(360,40,190,170,'#f6f8fb','#ccd',0.8,rx=6)
lines=['· V_th 아래: 꺼짐. 그래도 지수적으로','  조금씩 새는 전류(I_off)가 있음','· V_th 위: 켜짐. 전류 I_on','· 좋은 스위치 = I_on/I_off가 크고,','  꺼짐→켜짐이 가파를 것','· 가파름의 한계: 60 mV에 10배','  → V_th를 마음대로 못 낮춤','  → 전압을 못 줄임 (1.8절)']
for i,l in enumerate(lines): s.t(370+(10 if l.startswith('  ') else 0),62+i*19,l.strip(),'start','#333',9.3)
s.save('idvg')

# CMOS inverter
s=S(560,240)
def inv(X,inp):
    s.t(X+120,16,f'입력 {inp} → 출력 {1-inp}','middle',NAVY,10.5,True)
    s.line(X+120,30,X+120,52,'#333',1.5); s.t(X+120,28,'V_DD (1)','middle','#333',9)
    s.rect(X+95,52,50,40,'#dbe8f6' if inp==0 else '#eee','#2d6a9f' if inp==0 else '#aaa',1.2,rx=4)
    s.t(X+120,70,'PMOS','middle','#333',9.5,True); s.t(X+120,84,'ON' if inp==0 else 'OFF','middle',GRN if inp==0 else '#999',9,True)
    s.line(X+120,92,X+120,148,'#333',1.5); s.circ(X+120,120,3.5,'#333')
    s.line(X+120,120,X+200,120,'#333',1.5); s.t(X+205,124,f'출력 = {1-inp}','start',RED,10,True)
    s.rect(X+95,148,50,40,'#dbe8f6' if inp==1 else '#eee','#2d6a9f' if inp==1 else '#aaa',1.2,rx=4)
    s.t(X+120,166,'NMOS','middle','#333',9.5,True); s.t(X+120,180,'ON' if inp==1 else 'OFF','middle',GRN if inp==1 else '#999',9,True)
    s.line(X+120,188,X+120,210,'#333',1.5); s.t(X+120,224,'GND (0)','middle','#333',9)
    s.line(X+20,120,X+70,120,'#333',1.5); s.line(X+70,72,X+70,168,'#333',1.2)
    s.line(X+70,72,X+95,72,'#333',1.2); s.line(X+70,168,X+95,168,'#333',1.2)
    s.t(X+18,116,f'입력 {inp}','end',BLUE,10,True)
    if inp==0: s.path(f'M{X+130},40 L{X+130},112 L{X+190},112',c=RED,w=1.5,dash='4,3',arrow='r')
    else: s.path(f'M{X+190},128 L{X+130},128 L{X+130},205',c=RED,w=1.5,dash='4,3',arrow='r')
inv(20,0); inv(300,1)
s.line(290,30,290,225,'#ddd',1)
s.save('cmos')

# tunneling
s=S(580,215)
def panel(X,title,bw,bh,col,note,leak):
    s.t(X+90,16,title,'middle',NAVY,10.5,True)
    s.line(X,150,X+180,150,'#bbb',0.8)
    bx=X+90-bw/2
    s.rect(bx,150-bh,bw,bh,col,'#555',0.8,0.7)
    pts=[]
    for i in range(0,61):
        x=X+5+i*(bx-X-5)/60; pts.append(f'{x:.1f},{110+12*math.sin(i/60*6*math.pi):.1f}')
    s.path('M'+' L'.join(pts),c=BLUE,w=1.6)
    k=0.05 if bh>60 else 0.045
    pts=[]
    for i in range(0,31):
        x=bx+i*bw/30; a=12*math.exp(-k*(x-bx)); pts.append(f'{x:.1f},{110+a*math.sin((x-bx)/6):.1f}')
    s.path('M'+' L'.join(pts),c=BLUE,w=1.6)
    amp=12*math.exp(-k*bw)
    pts=[]
    for i in range(0,41):
        x=bx+bw+i*(X+175-bx-bw)/40; pts.append(f'{x:.1f},{110+amp*math.sin((x-bx-bw)/4):.1f}')
    s.path('M'+' L'.join(pts),c=RED if amp>3 else BLUE,w=1.6)
    s.t(X+90,172,note,'middle','#333',9)
    s.t(X+90,187,leak,'middle',RED if '큼' in leak else GRN,9,True)
panel(5,'두꺼운 SiO₂',60,80,OX,'벽이 두꺼움','새는 전자 거의 없음')
panel(200,'얇은 SiO₂ (~1.2 nm)',16,80,OX,'벽이 얇아 파동이 뚫고 나감','터널링 누설 큼')
panel(395,'HfO₂ (high-k)',46,55,'#f0c27b','유전율 ~5배 → 두껍게 써도 같은 C_ox','누설 크게 줄어듦')
s.t(290,207,'파란 파동 = 전자의 파동함수. 벽(절연막)을 지나며 지수적으로 줄어들지만, 벽이 얇으면 반대편까지 살아남는다.','middle','#555',8.8)
s.save('tunnel')

# damascene
s=S(580,175)
CU='#d98c4a'
def dpanel(i,title,tag,draw):
    X=5+i*145
    s.rect(X,22,138,130,'white','#ccc',0.8)
    s.t(X+6,37,f'{i+1}. {title}','start',NAVY,9.5,True)
    if tag:
        s.rect(X+100,27,34,14,ORG,'none',0,rx=3); s.t(X+117,37.5,tag,'middle','white',8.5,True)
    draw(X)
def lowk(X,trench=False):
    s.rect(X+10,120,118,20,'#cfd6dd','#777',0.5)
    s.rect(X+10,70,118,50,'#b9e3c6','#2e8b57',0.6)
    if trench: s.rect(X+45,70,48,35,'white','#2e8b57',0.6); s.line(X+45,70,X+93,70,'white',1.5)
dpanel(0,'절연막 증착','',lambda X:(lowk(X),s.t(X+69,98,'low-k 절연막','middle','#1b5e20',8.5)))
dpanel(1,'홈 식각','식각',lambda X:(lowk(X,True),s.t(X+69,62,'배선 모양 홈','middle',ORG,8.5)))
def p3(X):
    lowk(X,True); s.rect(X+10,58,118,12,CU,'#8a4b16',0.5); s.rect(X+45,70,48,35,CU,'#8a4b16',0.5)
    s.path(f'M{X+45},70 L{X+45},105 L{X+93},105 L{X+93},70',c='#555',w=1.5)
    s.t(X+69,52,'배리어(Ta/TaN) + Cu 채움','middle','#8a4b16',8)
dpanel(2,'Cu 채움','',p3)
def p4(X):
    lowk(X,True); s.rect(X+45,70,48,35,CU,'#8a4b16',0.5)
    s.path(f'M{X+45},70 L{X+45},105 L{X+93},105 L{X+93},70',c='#555',w=1.5)
    s.t(X+69,62,'넘친 Cu를 갈아냄','middle','#333',8)
dpanel(3,'CMP 평탄화','',p4)
s.t(290,168,'금속을 깎는 대신 절연막에 홈을 깎고 금속을 채운다 → 식각 대상이 금속에서 절연막으로 바뀜','middle','#555',9)
s.save('damascene')

# SAC
s=S(580,250)
s.t(290,16,'자기정렬 콘택(SAC): 마스크가 어긋나도 질화막이 게이트를 지켜 준다','middle',NAVY,10.5,True)
s.rect(40,190,500,40,SUB,'#777'); s.t(536,222,'Si (소스/드레인)','end',BRN,9)
s.rect(40,60,500,130,OX,GRN,0.6); s.t(532,78,'SiO₂','end','#1b5e20',9.5,True)
for gx in (130,330):
    s.rect(gx-14,90,128,100,SIN,'#7d4a92',0.8)
    s.rect(gx,110,100,80,GATE,'#333',0.8)
    s.t(gx+50,155,'게이트','middle','white',9.5,True)
s.path('M230,60 L290,60 L290,190 L244,190 L244,90 L230,90 Z',f='white',c='#555',w=0.8)
s.rect(40,44,190,16,'#f5c99b','#b5650c'); s.rect(290,44,250,16,'#f5c99b','#b5650c')
s.t(260,38,'열린 자리: 왼쪽으로 어긋남','middle',RED,9,True)
s.path('M258,66 L258,180',c=RED,w=1.5,dash='4,3',arrow='r')
s.t(78,140,'SiN 캡·','middle','#7d4a92',9,True); s.t(78,153,'스페이서','middle','#7d4a92',9,True); s.line(100,146,116,146,'#7d4a92',0.8)
s.t(226,83,'SiN에서 멈춤 →','end',RED,8.5,True)
s.t(290,244,'SiO₂는 빠르게, SiN은 거의 안 깎는 고선택비 식각 → 어긋난 부분은 SiN 위에서 멈추고, 나머지만 Si까지 내려감','middle','#555',8.8)
s.save('sac')

# Moore vs Dennard vs scaling
s=S(580,250)
s.rect(15,30,170,95,'#fff4e5',ORG,1.2,rx=8); s.t(100,52,'무어의 법칙','middle',ORG,11,True)
for i,l in enumerate(['"칩당 트랜지스터 수가','약 2년마다 2배"','= 관찰이자 업계의 목표']): s.t(100,72+i*15,l,'middle','#333',9.3)
s.rect(205,30,170,95,'#eef4fa',BLUE,1.2,rx=8); s.t(290,52,'스케일링','middle',BLUE,11,True)
for i,l in enumerate(['트랜지스터를 작게 만들기','= 목표를 달성하는','주된 수단']): s.t(290,72+i*15,l,'middle','#333',9.3)
s.rect(395,30,170,95,'#eef7ee',GRN,1.2,rx=8); s.t(480,52,'데너드 스케일링','middle',GRN,11,True)
for i,l in enumerate(['작게 만들면 왜 이득인가','= 같은 전력 밀도로','더 빠르고 싸진다는 규칙']): s.t(480,72+i*15,l,'middle','#333',9.3)
s.line(203,78,188,78,'#333',1.5,arrow='k'); s.t(196,140,'수단','middle','#333',9)
s.line(393,78,378,78,'#333',1.5,arrow='k'); s.t(386,140,'근거','middle','#333',9)
# timeline
s.line(40,190,560,190,'#333',1.2,arrow='k')
def yx(y): return 40+(y-1970)/(2030-1970)*510
for y in range(1970,2031,10): s.line(yx(y),186,yx(y),194,'#333',1); s.t(yx(y),208,str(y),'middle','#555',8.5)
s.rect(yx(1974),162,yx(2005)-yx(1974),14,GRN,'none',0,0.6); s.t((yx(1974)+yx(2005))/2,173,'데너드 유효: 작게 = 빠르고 저전력','middle','white',8.5,True)
s.rect(yx(2005),162,yx(2028)-yx(2005),14,'#c9cfd6','none',0); s.t((yx(2005)+yx(2028))/2,173,'전압 못 줄임 → 클럭 정체','middle','#333',8.5,True)
s.rect(yx(1971),145,yx(2028)-yx(1971),14,ORG,'none',0,0.5); s.t((yx(1971)+yx(2028))/2,156,'무어의 법칙: 계속 (속도는 점점 둔화)','middle','#333',8.5,True)
s.t(290,232,'2005년 무렵 이후: 작게 만드는 이득이 줄자 멀티코어 · 새 구조(FinFET, GAA) · 3D 적층으로 무어의 법칙을 이어감','middle','#555',9)
s.save('moore_dennard')
print('B ok')
