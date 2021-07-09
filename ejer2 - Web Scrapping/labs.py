import requests
from bs4 import BeautifulSoup

def scrap():
    url="http://esp.uem.es/digitalAED/laboratorios.php?lab=C306"
    mainurl="http://esp.uem.es/digitalAED/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    labs = soup.find_all('option')
    print(labs)
    cont = 0
    links = []
    for lab in labs:
        num = lab.text
        print(cont," - ",num)
        cont = cont+1
        link = lab.attrs['value']
        links.append(link)
    inp = int(input("Introduce el laboratorio: "))
    if(inp>(cont-1)):
        print("Valor introducido no váido. Ejecución terminada")
        exit(0)
    page = requests.get(mainurl+links[inp])
    soupLab = BeautifulSoup(page.content, 'html.parser')
    cent = soupLab.find('center')
    cent = cent.find('h2')
    sib = cent.next_sibling
    bol=True
    progs=[]
    while bol:
        try:
            sib = sib.next_sibling
            progs.append(sib)
        except:
            print("Final lista")
            bol=False
    cont=1
    print("\nProgramas del laboratorio seleccionado:\n")
    programas = []
    for prog in progs:
        #print(prog)
        if((cont%2)==0 and prog.strip()!=''):
            print(prog.strip())
            programas.append(prog.strip())
        cont=cont+1
    
    # print(programas)