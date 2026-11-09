import re
a=open('part_a.html').read(); b=open('part_b.html').read()
a=a[:a.rindex('</body>')]
doc=a+b
doc=doc.replace('틀린 문항은 괄호 안의 절로 돌아가 다시 읽으면 된다.','틀린 문항은 해당 절로 돌아가 다시 읽으면 된다.')
# insert svg for data-src figures
def ins(m):
    name=m.group(1); svg=open(f'fig/{name}.svg').read()
    return f'<figure>{svg}'
doc=re.sub(r'<figure data-src="([a-z_0-9]+)">',ins,doc)
# number figures
num={}; c=[0]
def capn(m):
    c[0]+=1; num[m.group(1)]=c[0]
    return f'<figcaption><b class="fn">그림 1-{c[0]}.</b> '
doc=re.sub(r'<figcaption data-key="([a-z_0-9]+)">',capn,doc)
doc=re.sub(r'\{\{ref:([a-z_0-9]+)\}\}',lambda m:f'그림 1-{num[m.group(1)]}',doc)
# unicode sub/superscripts outside svg -> tags
parts=re.split(r'(<svg.*?</svg>)',doc,flags=re.S)
SUBM={c:str(i) for i,c in enumerate('₀₁₂₃₄₅₆₇₈₉')}
SUPM={c:str(i) for i,c in enumerate('⁰¹²³⁴⁵⁶⁷⁸⁹')}; SUPM.update({'⁺':'+','⁻':'−'})
def conv(t):
    t=re.sub('['+''.join(SUBM)+']+',lambda m:'<sub>'+''.join(SUBM[x] for x in m.group(0))+'</sub>',t)
    t=re.sub('['+''.join(SUPM)+']+',lambda m:'<sup>'+''.join(SUPM[x] for x in m.group(0))+'</sup>',t)
    return t
doc=''.join(p if p.startswith('<svg') else conv(p) for p in parts)
open('full.html','w').write(doc)
import weasyprint
weasyprint.HTML('full.html',base_url='.').write_pdf('ch1.pdf')
print('figs',c[0])
