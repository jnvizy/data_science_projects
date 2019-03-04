# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 13:37:10 2018

@author: JN
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


# Extraction de la liste des 256 utilisateurs les plus actifs

# création d'un data frame à partir d'un objet soup basé sur le code html de la
# page de github
url = "https://gist.github.com/paulmillr/2657075"
res = requests.get(url)
soup = BeautifulSoup(res.content, "html.parser")
data = list(soup.find_all("td"))
x = pd.DataFrame([k.text for k in data]).loc[:1020]

# nettoyage du dataframe (suppression des lignes non désirées à l'aide de 
# la fonction get_username, appliquée à l'ensemble du dataframe)
x["mod4"] = x.index % 4
top_users = x.where(x["mod4"] == 0).dropna()


def get_username(row):
    return row[0].split(' ')[0]

top_users["user_name"] = top_users.apply(get_username, axis=1)


# suppression des champs inutiles
top_users.drop("mod4", axis=1, inplace=True)
top_users.drop(0, axis=1, inplace=True)

# obtention des identifiants nécessaires pour faire des requêtes sur 
# l'API GitHub
token_file = open("C:/Users/JN/Desktop/Telecom PT/Kit data science/git_exos/Seance_3/token.txt", encoding="utf8")
token = token_file.read()
myname = "LaVize"

# on définit une fonction get_average_stars qu'on applique ensuite à chaque ligne 
# du dataframe


def get_average_stars(row):
    r = requests.get("https://api.github.com/users/"+row["user_name"]+"/repos", auth=(myname, token))
    json_res = json.loads(r.text)

    c = 0
    S = 0
    for i in range(len(json_res)):
        S += json_res[i]["stargazers_count"]
        c += 1
    if (c == 0):
        return 0
    else:
        return S/c
    
top_users["avg_stars_per_repo"] = top_users.apply(get_average_stars, axis=1)

# on trie enfin le dataframe à partir du nombre moyen d'étoiles par répertoire
top_users.sort_values(['avg_stars_per_repo'], ascending=False, inplace=True)

print(top_users)
