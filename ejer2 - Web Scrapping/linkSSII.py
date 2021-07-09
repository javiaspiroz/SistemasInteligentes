import requests
from bs4 import BeautifulSoup

def scrap():
    url ="http://esp.uem.es/ssii/holaMundo.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.prettify())
    ps = soup.find_all('p')
    texts = []
    for p in ps:
        texts.append(p.text)
    print(texts)