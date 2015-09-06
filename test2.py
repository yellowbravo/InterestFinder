#!/usr/bin/python
# -*-coding:Latin-1 -*
from bs4 import BeautifulSoup
import mechanize


mongolab_uri = 'mongodb://nico:interestfinder2015@ds055762.mongolab.com:55762/interestfinder'

from pymongo import MongoClient
client = MongoClient(mongolab_uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
db = client['interestfinder']


def get_noga(first, last):

    url = "http://www.monetas.ch/htm/666/fr/Personnes-resultats-de-la-recherche.htm?Personensuche={}+{}&CompanySearchSubmit=1".format(first, last)

    br = mechanize.Browser()
    response = br.open(url)

    data_link = ""

    html = response.get_data()
    soup = BeautifulSoup(html)
    link = soup.findAll('a')
    for l in link:
        if l.text.strip() == '{} {}'.format(first, last):
            #print l.text
            data_req = br.follow_link(text='{} {}'.format(first, last))

            return parse_page(BeautifulSoup(data_req.get_data()))



def parse_page(soup):
    links = soup.findAll('a')
    for l in links:
        if l.text == 'Afficher tous les mandats actuels':
            url = l['href']
            break

    br = mechanize.Browser()
    response = br.open(url)
    html = response.get_data()

    soup = BeautifulSoup(html)

    link = soup.findAll('a')

    cpt = 0

    corps = []

    for l in link:
        cpt = cpt + 1
        if l.text == 'Tweet':
            break
        if cpt > 14:
            corps.append(l.text)

    return corps


def supprime_accent(ligne):
    """ supprime les accents du texte source """
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â', 'ü', 'ä', 'ö', 'ë', 'ì', 'í']
    sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a', 'u', 'a', 'o', 'e', 'i', 'i']
    i = 0
    while i < len(accent):
        ligne = ligne.replace(accent[i], sans_accent[i])
        i += 1
    return ligne


def main():
    collec = db['candidates']
    for cand in collec.find():
        firstname = supprime_accent(cand['firstname'])
        lastname = supprime_accent(cand['lastname'])
        corps = get_noga(firstname, lastname)

        collec.update({'_id': cand['_id']}, {"$set": {"corporations": corps}}, upsert=True)




if __name__ == '__main__':
    main()
