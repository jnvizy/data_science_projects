# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 19:57:53 2018

@author: JN
"""

import requests
from bs4 import BeautifulSoup
from time import strftime

#éléments à extraire : 
#* les ventes au quartier à fin décembre 2018
#* le prix de l'action et son % de changement au moment du crawling
#* le % Shares Owned des investisseurs institutionels
#* le dividend yield de la company, le secteur et de l'industrie


url_list = {"lvmh" : "https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA",
            "airbus" : "https://www.reuters.com/finance/stocks/financial-highlights/AIR.PA",
            "danone" : "https://www.reuters.com/finance/stocks/financial-highlights/DANO.PA"}

current_date = strftime("%d/%m/%Y")

for v in url_list.values():
    print_output(v)


# crée un objet soup par entreprise et imprime les infos issues de Reuters
def print_output(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    print("Company ticker: " + (url[-7:-1] + url[-1]).replace("/",""))
    print("Sales estimates for the 4th quarter of 2018: " + get_stock_price(soup)[0]+" "+get_sales(soup) + " millions")
    print("Stock price as at " + current_date+ " " + get_stock_price(soup)[2] + ": " + get_stock_price(soup)[0] + " " + get_stock_price(soup)[1])
    print("Price change (intraday): " + get_price_change(soup))
    print("% of shares owned by institutional investors: " + get_instit_stake(soup))
    print("Dividend yield of the company: " + get_div_yields(soup)[0])
    print("Dividend yield of the sector: " + get_div_yields(soup)[1])
    print("Dividend yield of the industry: " + get_div_yields(soup)[2])
    print("\n")


# extrait d'une soupe les prévisions de CA pour le 4T20158
def get_sales(soup):
    data = list(soup.find_all("td"))
    for i in range(len(data)):
        if "SALES (in millions)" in data[i].text:
            return data[i+3].text


# supprime sauts de ligne, tabulations, etc... du texte issu d'une soupe
def cleaning(soup_text):
    soup_text.replace("\t", "")
    split = soup_text.split("\n")
    result = []
    for i in range(len(split)):
        if (split[i] == '' or split[i] == '\r'):
            pass
        else:
            word = split[i].replace('\t', '')
            result.append(word)
    return result


# extrait le prix de l'action d'une soupe
def get_stock_price(soup):
    quote = cleaning(soup.find(class_="sectionQuoteDetail").text)
    currency = quote[1][-3:-1]+quote[1][-1]
    price = quote[1][:-3]
    time = quote[2]
    return [currency, price, time]

# extrait la variation du prix de l'action d'une soupe
def get_price_change(soup):
    raw_text = cleaning(soup.find(class_="valueContentPercent").text)
    price_change = raw_text[0][raw_text[0].find("(")+1:raw_text[0].find(")")]
    return price_change


# extrait d'une soupe la part des institutionnels dans le capital
def get_instit_stake(soup):
    data = list(soup.find_all("td"))
    for i in range(len(data)):
        if "% Shares Owned" in data[i].text:
            return data[i+1].text


# extrait les dividend yields d'une soupe
def get_div_yields(soup):
    data = list(soup.find_all("td"))
    for i in range(len(data)):
        if "Dividend Yield" in data[i].text:
            return [data[i+1].text, data[i+2].text, data[i+3].text]    
