import requests
from flask import Flask, render_template,url_for, redirect
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

info=[]
images=[]
book=input()
URL = 'https://en.wikipedia.org/wiki/'+book.replace(' ','_') 
page = requests.get(URL)
content = page.content
soup = BeautifulSoup(content,'html.parser')
job_elems = soup.find_all('div', class_='mw-parser-output')
for d in job_elems:
    img=d.find('img')
    # print(img['src'])
    link="http:"+img['src']
    images.append(link)
    print(images) 
    name = list(d.find_all('p'))
    par=name[2].get_text().replace('/n','') 
    info.append(par)
    # print(info) 
    print("2nd Para")
    par2=name[3].get_text().replace('/n','') .replace('[2]','').replace('[3]','')
    info.append(par2) 
    # print(info)

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