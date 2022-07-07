from ast import Is
from csv import writer, DictWriter
from ctypes.wintypes import PINT
from filecmp import cmp
import sys
from sqlite3 import Row
from tkinter import Menu, ttk
# Para hacer graficos
import matplotlib.pyplot as plt
# Para modificar csv
import pandas as pd
from pyparsing import punc8bit
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
    print(dataBase.values())
    plt.style.use('ggplot')
    plt.bar(dataBase.keys(), dataBase.values(), color='#e36685')
    plt.grid()
    plt.show()

def api(API):
    champsDicPoints = []
    r = requests.get(API)
    data = json.loads(r.text)
    champsDictName = getAllChampions()
    # Se consigue de la api los datos necesarios y se pasan a modo json
    for item in data:
        id = item['championId']
        points = item['championPoints']
        champsDicPoints.append({ 'id' : id , 'points' : points, 'name' : champsDictName[id]})
    # Se pasa a .CSV para tenerlo guardado
    ToJson(champsDicPoints)
    #df = pd.DataFrame(pointsDictN)
    #print(df)
    #bar(pointsDictN)
    # Se grafica

def ToJson(data):
    # Pasa diccionarios a JSON              
    with open('./static/points.json', "w") as jsonFile:
        jsonFile.write(json.dumps(data))

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
