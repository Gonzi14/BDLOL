from csv import writer, DictWriter
from filecmp import cmp
import sys
from sqlite3 import Row
from tkinter import Menu, ttk
# Para hacer graficos
import matplotlib.pyplot as plt
# Para modificar csv
import pandas as pd
# Para APIs
from riotwatcher import LolWatcher, ApiError
import requests
import json
# Para no matar a la API
import time
# Para mandar la informacion a la pagina
import json

# Informacion general de las APIs
api_key = 'RGAPI-646391cb-df01-494c-aaab-f02654e6a3fd'
watcher = LolWatcher(api_key)
my_region = 'la2'
me = watcher.summoner.by_name(my_region, 'JimCharles3')
summonerID = me['id']
puuid = me['puuid']
APIchampions = (f"https://{my_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerID}" + "?api_key=" + api_key)
current_champ_list = watcher.data_dragon.champions('12.11.1')

def matches(puuid):
    # Esto hace que busque los datos de mis partidas
    while True:
        my_matches = watcher.match.matchlist_by_puuid(my_region, puuid)
        last_match = my_matches[0]
        while last_match == my_matches[0]:
            # Mientras que no se juegue partida, que se fija si cambia
            my_matches = watcher.match.matchlist_by_puuid(my_region, puuid)
            time.sleep(1)
        # Si se jugo una partida, que se llame al metodo api
        api(APIchampions)
        last_match = my_matches[0]

def bar(dataBase):
    # Se hace 
    plt.style.use('ggplot')
    plt.bar(dataBase.keys(), dataBase.values(), color='#e36685')
    plt.grid()
    plt.show()

def api(API):
    champsDicPoints = {}
    r = requests.get(API)
    data = json.loads(r.text)
    # Se consigue de la api los datos necesarios y se pasan a modo json
    for item in data:
        ID = item['championId']
        points = item['championPoints']
        champsDicPoints.update({ID: points})
        # Se crea un diccionario con los puntos y los ID de los champs
    champsDictName = getAllChampions()
    pointsDictN = sort(champsDicPoints)
    nameDictN = sort(champsDictName)
    # Se ordenan los diccionarios por el ID, para que esten en sincronia
    for i in nameDictN:
        # Por cada campeon que hay, que se modifique la Key de todo el diccionario, cambiandola por el nombre del otro diccionario
        try:
            pointsDictN[nameDictN[i]] = pointsDictN[i]
            del pointsDictN[i]
        except:
            # Si hay un champ que no tiene puntos, que se escriba 0
            pointsDictN[nameDictN[i]] = 0
    toCSV(pointsDictN)
    # Se pasa a .CSV para tenerlo guardado
    ToJson(pointsDictN)
    bar(pointsDictN)
    # Se grafica

def ToJson(data):
    with open('points.json', "w") as jsonFile:
        jsonFile.write(json.dumps(data))

def sort(dictionary):
    # Ordenamiento de diccionarios
    items = dictionary.items()
    itemsSorted = sorted(items)
    newDict = dict((x, y) for x, y in itemsSorted)
    return newDict

def toCSV(dict):
    # Pasa diccionarios a CSV
    with open('Campeones.csv', 'w') as f:
        writer = DictWriter(f, dict.keys())
        writer.writeheader()
        writer.writerow(dict)

def getAllChampions():
    champsDict = {}
    file = open('champion.json', encoding= "utf8")
    data2 = json.load(file)
    todo = data2['data']
    # Se consigue toda la data de los campeones
    for champions in data2['data']:
        champion = todo[champions]
        id = int(champion['key'])
        champsDict.update({id : champions})
        # Se achica la data para que sea solo el ID y su nombre
    return champsDict

api(APIchampions)
#matches(puuid)
