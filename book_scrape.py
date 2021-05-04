import re
import requests
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup


def scrapeinfo(book):
    info=[]
    images=[]
    URL = 'https://en.wikipedia.org/wiki/'+book.replace(' ','_')
    page = requests.get(URL)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    job_elems = soup.find_all('div', class_='mw-parser-output')
    for d in job_elems:

        img=d.find('img')
        link="http:"+img['src']
        images.append(link)
        # print(images)
        name = list(d.find_all('p'))
        if len(name)>=3:
            par=name[2].get_text().replace('/n','')
            par=re.sub(r'[/[0-9]*]','',par)
            info.append(par)

        if len(name)>=4:
            par2=name[3].get_text().replace('/n','')
            par2=re.sub(r'[/[0-9]*]','',par2)
            info.append(par2)

    ans=''
    for i in info:
        print(i,'\n')
    ans='\n\n'.join(info)
    return ((ans,(None if len(images)==0 else images[0])))