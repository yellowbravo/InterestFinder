from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from bson import json_util
from bson.objectid import ObjectId
from IF_App.forms import SearchCandidate

mongolab_uri = 'mongodb://nico:interestfinder2015@ds055762.mongolab.com:55762/interestfinder'

from pymongo import MongoClient
client = MongoClient(mongolab_uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)
db = client['interestfinder']


def economic_sectors(request):
    sectors = ['Agriculture, sylviculture et pêche',
               "Industrie manufacturière, industries extractives et autres",
               'Construction',
               "Commerce de gros et de détail, transports, hôtels et restaurants",
               'Information et communication',
               'Activités financières et d’assurance',
               'Activités immobilières',
               "Activités spécialisées, scientifiques et techniques et activités de services administratifs et de soutien",
               'Administration publique, défense, enseignement, santé humaine et action sociale'
               'Autres activités de services']
    return render(request, 'economic_sectors.html', context={'sectors': sectors})


def cantons_list(request):
    cantons = ['Aargau',
               'Appenzell Inner Rhodes',
               'Appenzell Outer Rhodes',
               'Bern',
               'Basel Country',
               'Basel City',
               'Fribourg',
               'Geneva',
               'Glarus',
               'Graubünden',
               'Jura',
               'Lucerne',
               'Neuchâtel',
               'Nidwalden',
               'Obwalden',
               'St Gallen',
               'Schaffhausen',
               'Solothurn',
               'Schwyz',
               'Thurgau',
               'Ticino',
               'Uri',
               'Vaud',
               'Valais',
               'Zug',
               'Zurich']

    context = {'cantons': cantons,
               }

    return render(request, 'cantons_list.html', context=context)


def data_viz(request):
    return render(request, 'data_viz.html')


def main(request):
    if request.POST:
        search_form = SearchCandidate(data=request.POST)
        if search_form.is_valid():
            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()

            collec = db['candidates']
            cand = dict()
            try:
                for c in collec.find({'lastname': last_name}):
                    if c['firstname'] == first_name:
                        cand = c
                    break

                url = '/candidate/' + str(cand['_id']) + '/'

                return HttpResponseRedirect(url)

            except KeyError:
                return HttpResponseRedirect('/')
    else:
        search_form = SearchCandidate()

    context = {'search_form': search_form
               }

    return render(request, 'index.html', context=context)


def canton(request, canton_name):
    collection = db['candidates']

    candidates = list()
    for cand in collection.find({'district': canton_name}):
        try:
            cand['LINK_photo'] = 'https://www.smartvote.ch' + cand['LINK_photo']
        except TypeError:
            cand['LINK_photo'] = 'https://www.smartvote.ch/images/responder/candidate/placeholder.gif'
        cand['profile_link'] = '/candidate/' + str(cand['_id']) + '/'
        try:
            cand['year_of_birth'] = int(cand['year_of_birth'])
        except ValueError:
            pass
        candidates.append(cand)
    context = {'name': canton_name,
               'candidates': candidates
               }

    return render(request, 'canton.html', context=context)


def candidate_profile(request, candidate_id):
    collection = db['candidates']

    data = collection.find_one({'_id': ObjectId(candidate_id)})

    try:
        data['LINK_photo'] = 'https://www.smartvote.ch' + data['LINK_photo']
    except TypeError:
        data['LINK_photo'] = 'https://www.smartvote.ch/images/responder/candidate/placeholder.gif'

    data['year_of_birth'] = int(data['year_of_birth'])

    try:
        if data['corporations'] is None or data['corporations'] == []:
            data['corporations'] = ['Aucun intérêt découvert']
    except KeyError:
        data['corporations'] = ['Aucun intérêt découvert']

    context = {'candidate': data
               }
    return render(request, 'candidate_profile.html', context=context)
