from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located

k=0

Hotel=[]
for i in range(2,3):
    
    URL = 'https://www.petitfute.com/v35259-grenoble-38000/c1173-visites-points-d-interet/?page={}'.format(i)
    page = requests.get(URL)
    print('************************')
    print('************************')
    print(URL)
    print('************************')
    print('************************')
    soup = BeautifulSoup(page.content, 'html.parser')
    results=soup.find_all('div',class_='etab-infos')
    print('fgehsfgs')
    chrome_driver_path='chromedriver/chromedriver.exe'
    chrome_options=Options()
    chrome_options.add_argument("headless")
    driver=webdriver.Chrome(
        executable_path=chrome_driver_path
    )
    
    driver.get(URL)
    if driver.find_element_by_xpath("(//div[@class='adresse-listing'])[1]"):
        main_window = driver.current_window_handle
        print(driver.current_url)
        # get the number of details to click
        addr = len(driver.find_elements_by_xpath("//div[@class='adresse-item  item-prems']"))
        if addr==0:
            addr = len(driver.find_elements_by_xpath("//div[@class='adresse-item ']"))
            print('tafa')
        print(addr)
        # iterate through all the details links  (used the index rather elements list as it may lead to staleeleemnt exception after clicking on the first detiails link)
        for addrNum in range(addr):
            element={}
            ele = driver.find_element_by_xpath("(//div[@class='etab-title'])[" + str (addrNum+1) + "]")
            Activite=ele.find_element_by_xpath("(//span[@class='ss-cat'])["+ str(addrNum+1)+"]")
            if Activite:
                element['Activités']=Activite.text
                print(Activite.text)
            else:
                element['Activités']=''
            ele.click()
            print(driver.current_url)


            urllien=driver.current_url
            page1 = requests.get(urllien)
            soup1=BeautifulSoup(page1.content, 'html.parser')
        
            Nom=soup1.find('h1')
            print(Nom.text.strip())
            element['Nom']=Nom.text.strip()
            
            Rue=soup1.find('span',itemprop="streetAddress")
            if Rue:
                Rue=Rue.text.strip()
            else:
                Rue=''
            Codepostal=soup1.find('span',itemprop="postalCode")
            if Codepostal:
                Codepostal=Codepostal.text.strip()
            else:
                Codepostal=''
            Locale=soup1.find('span',itemprop="addressLocality")
            if Locale:
                Locale=Locale.text.strip()
            else:
                Locale=''
            Country=soup1.find('span',itemprop="addressCountry")
            if Country:
                Country=Country.text.strip()
            else:
                Country=''
            Adresse=''+Rue+' '+Codepostal+' '+Locale+' '+Country
            print(Adresse)
            element['Adresse']=Adresse
            
            

            Telephone=soup1.find('a',class_='phone_clear')
            if Telephone:
                element['Téléphone']=Telephone.text.strip()
                print(element['Téléphone'])
            else:
                Telephone=soup1.find('span',class_='inline-block')
                if Telephone:
                    element['Téléphone']=Telephone.text.strip()
                    print(element['Téléphone'])
                else:
                    element['Téléphone']=''
            Hotel.append(element)

            driver.get(URL)
            print(driver.current_url)
            print('************************')
    
    driver.close()    
    time.sleep(1)
    df=pd.DataFrame(Hotel)
    writer=pd.ExcelWriter('Visiter_Grenoble/A_Visiter_Grenoble_{}.xlsx'.format(i),engine='xlsxwriter')
    df.to_excel(writer,sheet_name='Sheet1') 
    writer.save()
    time.sleep(5)