# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 15:31:26 2018

@author: JN
"""

#version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.


import pandas as pd
import requests
from bs4 import BeautifulSoup

#récupérons déjà la liste des liens vers des annonces en Idf:

# paramètres généraux des requêtes et regex utilisée pour extraire les liens vers les annonces
url = "https://www.leboncoin.fr/recherche/?category=2&regions=12&model=Zoe&brand=Renault"
region = "ile_de_france"
request_headers = {
       "Accept-Language": "en-US,en;q=0.5",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
       "Referer": "http://thewebsite.com",
       "Connection": "keep-alive"
   }
regex = '(?<=href=)\"\/(.+?)(?=\s)'


#%%
#le nombre de résultats affichés par page semble limité à 35, on fait donc une boucle qui va récupérer les liens à partir de chaque page de résultats
# initialisation de la boucle
r = requests.get(url, headers = request_headers)
soup = BeautifulSoup(r.content, "html.parser")
annonces = list(soup.find_all(class_="_3DFQ-"))
liste_annonces = [str(element) for element in annonces]
df_annonces = pd.DataFrame(liste_annonces)
df_annonces["lien"] = df_annonces[0].str.extract(regex)
i = 1

#corps de la boucle
while r.status_code == 200:
    i += 1
    page = "https://www.leboncoin.fr/recherche/?category=2&regions=12&model=Zoe&brand=Renault&page=" + str(i)
    r = requests.get(page, headers = request_headers)
    if r.status_code != 200:
        break
    soup = BeautifulSoup(r.content, "html.parser")
    annonces = list(soup.find_all(class_="_3DFQ-"))
    liste_annonces = [str(element) for element in annonces]
    if len(liste_annonces) == 0:
        break
    df_ad = pd.DataFrame(liste_annonces)
    df_ad["lien"] = df_ad[0].str.extract(regex)
    df_annonces = pd.concat([df_annonces, df_ad], axis = 0)

#%%   
#une fois la liste des liens obtenue, extrayons-en les informations demandées

#from selenium.webdriver import Firefox
#from selenium.webdriver.firefox.options import Options
#opts = Options()
#opts.set_headless()
#assert opts.headless
#browser = Firefox(options=opts)
#browser.get('https://duckduckgo.com')

tel_template = '0[0-9]{9}'
regex_life = '[lLiIfFeE]{4}'
regex_zen = '[zZeEnN]{3}'
regex_intens = '[iInNtTeEnNsS]{6}'

df = pd.DataFrame(df_annonces["lien"].values)
df.rename(columns = {0 : "lien"}, inplace = True)

def get_soup(row):
    link = "https://www.leboncoin.fr/" + row["lien"].replace('"','')
    r2 = requests.get(link, headers = request_headers)
    if r2.status_code != 200:
        return np.Nan
    else:
        return BeautifulSoup(r2.content, "html.parser")
    
df["soup"] = df.apply(get_soup, axis = 1)

#%%


def get_year(row):
    data = row["soup"].find_all(class_="_3Jxf3")
    items=[k for k in ga]
    year = int(items[2].text)
    return year

def get_km(row):
    data = row["soup"].find_all(class_="_3Jxf3")
    items=[k for k in ga]
    km = int(items[3].text[:-3])
    return km

def get_price(row):
    return int(row["soup"].find(class_="_1F5u3").text.replace(' ','').replace('€',''))

def get_vendor_type(row):
    if (str([k for k in row["soup"].find_all("li")]).find("SIREN") == -1):
        return "part"
    else:
        return "pro"

def get_ad_title(row):
    return row["soup"].find(class_ = "_1KQme")

df["year"] = df.apply(get_year, axis = 1)
df["km"] = df.apply(get_km, axis = 1)
df["price"] = df.apply(get_price, axis = 1)

df["vendor_type"] = df.apply(get_vendor_type, axis = 1)
df["ad_title"] = df.apply(get_ad_title, axis = 1)
#df["is_life"] = df["ad_title"].str.contains(regex_life)
#df["is_zen"] = df["ad_title"].str.contains(regex_zen)
#df["is_intens"] = df["ad_title"].str.contains(regex_intens)
