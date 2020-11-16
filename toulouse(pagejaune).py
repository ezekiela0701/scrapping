import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

titre={"Nom","Adresse","Téléphone",}
Hotel=[]

# Hotel.append(titre)

for j in range(1,7):
    URL = 'https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=commerces%20alimentaires&ou=paris&idOu=L07505600&contexte=lQ0OhcTW8ioTGBuqtPupDAxISMRndNFsTX8Pg%2Byl0iE%3D&proximite=0&filtres%5BRUBRIQUES%5D%5B0%5D=46053600&quoiQuiInterprete=commerces%20alimentaires&page={}'.format(j)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results=soup.find_all('article',class_='bi-bloc blocs clearfix with-zone-produit bi-pro')
    for company in results:
        element={}

        company_name=company.find('a',class_='denomination-links')
        
        element['Nom']=company_name.text.strip()
        Adresse=company.find('a',class_='adresse')
        
        element['Adresse']=Adresse.text.strip()
        print(Adresse.text.strip())
        print(company_name.text.strip())
        
        num=company.find('strong',class_='num')
        if num:
            num=company.find('strong',class_='num')
            element['Téléphone']=num.text.strip()
            print("telephone : "+num.text.strip())
        else:
            num='aucun'
        
        Hotel.append(element)
       
    print('pause 2s ')     
    time.sleep(1.2)


df=pd.DataFrame(Hotel)

      
writer=pd.ExcelWriter('Glaciers.xlsx',engine='xlsxwriter')

df.to_excel(writer,sheet_name='Sheet1')

writer.save() 