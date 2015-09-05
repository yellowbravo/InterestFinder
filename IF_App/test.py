#!/usr/bin/python

# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
from urllib import request


def get_person(first, last):
    url = 'http://tools.letemps.ch/zefix/app/webservice.php?auth=password&type=people&name={}&firstname={}'.format(last, first)
    response = request.urlopen(url)

    html = response.read().decode('utf-8')
    data = json.loads(html)
    return data


def get_corp(first, last, residence):
    cities = db['switzerland_cities']
    dict_data = get_person(first, last)
    pers = {}
    for p in dict_data:
        if p['name'] == first and p['firstName'] == last and p['residenceCity'] == residence:
            pers = p
            break

    if pers == {}:
        canton_code = cities.find_one({'postal code': postal_code})['canton']
        for p in dict_data:
            if p['name'] == first and p['firstName'] == last and p['residenceCity'] == residence:
                pers = p
                break


    url = 'http://tools.letemps.ch/zefix/app/webservice.php?auth=password&type=companies&name={}&firstname={}&mrMrs={}&personKind={}&originCity={}&residenceCity={}'.format(first, last, pers['mrMrs'], pers['personKind'], pers['originCity'], pers['residenceCity'])
    url = url.replace(' ', '%20')
    response = request.urlopen(url)

    html = response.read().decode('utf-8')
    data = json.loads(html)

    return data


firstname = supprime_accent('Hans')
lastname = supprime_accent('Egloff')
postal_code = 8904
city = Aesch
try:
    canton_code = cities.find_one({'postal code': postal_code})['canton']
    try:
        corps = get_corp(lastname, firstname, city)
    except KeyError:
        try:
            corps = get_corp(lastname, firstname, city + ' ' + canton_code)
        except KeyError:
            corps = []

    print(firstname, lastname, corps)
    collec.update({'_id': cand['_id']}, {"$set": {"corporations": corps}}, upsert=True)
except TypeError:
    pass








