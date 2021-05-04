import requests
from flask import Flask, render_template,url_for, redirect
import sys

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
    # print("name length",len(name))
    par=name[0].get_text().replace('\n','').replace('[2]','').replace('{\displaystyle n}','') 
    info.append(par)
    # print(info) 
    # print("2nd Para")
    par2=name[1].get_text().replace('\n','').replace('[3]','')
    info.append(par2) 
    # print(info)
    # print("3rd Para")
    par3=name[2].get_text().replace('\n','').replace('[4]','').replace('[5]','').replace('\u2061','').replace('{\\displaystyle {\\text{O}}(\\log n)}','').replace('Both are, in general, neither weight-balanced nor μ{\\displaystyle \\mu }-balanced for any μ≤12{\\displaystyle \\mu \\leq {\\tfrac {1}{2}}}; that is, sibling nodes can have hugely differing numbers of descendants.','')
    info.append(par3) 
    # print(info) 
    # tbl=list(d.find_all('table'))
    # print("length of tables",len(tbl))
    # print(tbl[0].get_text())
    head=list(d.find_all('h3'))
    # print("heading3 count",len(head))
    head1=head[0].get_text().replace('[edit]','')
    info.append(head1+':')
    # print("4th Para")
    par4=name[3].get_text().replace('\n','')
    info.append(par4) 
    # print(info) 
    # li=list(d.find_all('li'))
    # print("length1",len(li))
    # print(li[25].get_text(),li[26].get_text(),li[27].get_text())
    # info.append(li[25].get_text())
    # info.append(li[26].get_text())
    # info.append(li[27].get_text())
   
    
URL = 'https://www.programiz.com/dsa/avl-tree'
page = requests.get(URL)
content = page.content
soup = BeautifulSoup(content,'html.parser')
job_elems = soup.find_all('div', class_='content')
for d in job_elems:
    # img=d.find('img')
    # print(img['src'])
    # link="http:"+img['src']
    # info.append(link)
    # print(info) 
    p=list(d.find_all('p'))
    print("length2",len(p)) 
    # print(p[3].get_text(),p[4].get_text())
    info.append(p[3].get_text())
    info.append(p[4].get_text())
    head2=list(d.find_all('h2'))
    # print("h2 length",len(head2)) 
    info.append(head2[6].get_text()+':') 
    td=list(d.find_all('td'))
    # print("length3",len(td))
    info.append(td[0].get_text()+':')
    info.append(td[3].get_text())
    info.append(td[1].get_text()+':')
    info.append(td[4].get_text())
    info.append(td[2].get_text()+':')
    info.append(td[5].get_text())
    # for i in range(0,6):
    #     # print(td[i].get_text())
    #     info.append(td[i].get_text())
    # img=list(d.find_all('figure'))
    # print('figures',len(img))
    # print(img[0].get_text())
    li=list(d.find_all('li'))
    print("length4",len(li))
    print(li[0].get_text(),li[7].get_text(),li[8].get_text(),li[9].get_text())
    # info.append(li[6].get_text())
    # info.append(li[7].get_text())
    # info.append(li[8].get_text())
    # info.append(li[9].get_text())
# print(len(info))
print('\n')
for i in info:
    print(i,'\n') 
app = Flask(__name__)
@app.route('/')
def main1():
#    return render_template('main.html',info=info)
    print(info)
if __name__ == '__main__':
   app.run(debug=True)