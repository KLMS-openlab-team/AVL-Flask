import re
import requests
from urllib.request import urlopen

from bs4 import BeautifulSoup

info=[]
URL = 'https://en.wikipedia.org/wiki/AVL_tree'
page = requests.get(URL)
content = page.content
soup = BeautifulSoup(content,'html.parser')
job_elems = soup.find_all('div', class_='mw-parser-output')
for d in job_elems:
    name = list(d.find_all('p'))
    par=name[0].get_text().replace('\n','').replace('[2]','').replace('{\displaystyle n}','')
    info.append(par)
    par2=name[1].get_text().replace('\n','').replace('[3]','')
    info.append(par2)
    par3=name[2].get_text().replace('\n','').replace('[4]','').replace('[5]','').replace('\u2061','').replace('{\\displaystyle {\\text{O}}(\\log n)}','').replace('Both are, in general, neither weight-balanced nor μ{\\displaystyle \\mu }-balanced for any μ≤12{\\displaystyle \\mu \\leq {\\tfrac {1}{2}}}; that is, sibling nodes can have hugely differing numbers of descendants.','')
    info.append(par3)
    head=list(d.find_all('h3'))
    head1=head[0].get_text().replace('[edit]','')
    info.append(head1+':')
    par4=name[3].get_text().replace('\n','')
    info.append(par4)

URL = 'https://www.programiz.com/dsa/avl-tree'
page = requests.get(URL)
content = page.content
soup = BeautifulSoup(content,'html.parser')
job_elems = soup.find_all('div', class_='content')
imgs=soup.find_all('img')
if len(imgs)>=4:
    link="http:"+imgs[3]['src']
for d in job_elems:
    p=list(d.find_all('p'))
    info.append(p[3].get_text())
    info.append(p[4].get_text())
    head2=list(d.find_all('h2'))
    info.append(head2[6].get_text()+':')
    td=list(d.find_all('td'))
    info.append(td[0].get_text()+':')
    info.append(td[3].get_text())
    info.append(td[1].get_text()+':')
    info.append(td[4].get_text())
    info.append(td[2].get_text()+':')
    info.append(td[5].get_text())
    li=list(d.find_all('li'))
#     print(li[0].get_text(),li[7].get_text(),li[8].get_text(),li[9].get_text())
# for i in info:
#     print(i)
avl_tree_info=('\n\n'.join(info)).strip()
avl_tree_imglink=link