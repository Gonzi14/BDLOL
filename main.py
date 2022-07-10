from ast import Is
import csv
from ctypes.wintypes import PINT
from filecmp import cmp
import sys
from sqlite3 import Row
from tkinter import Menu, ttk
from unicodedata import name
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
# Para ver si 2 numeros estan cerca
import math

# Informacion general de las APIs
api_key = 'RGAPI-646391cb-df01-494c-aaab-f02654e6a3fd'
watcher = LolWatcher(api_key)
my_region = 'la2'
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
        api(name)
        last_match = my_matches[0]

def bar(dataBase):
    plt.style.use('ggplot')   
    plt.bar(dataBase.name ,dataBase.points, color='#e36685')
    plt.subplots_adjust(wspace=0.9, bottom=0.1)
    ax = plt.subplot()  
    # Se crea un grafico tipo bar
    for i, txt in enumerate(dataBase.name):
        # Por cada champ, se ve si la diferencia entre él y el siguiente es cercana a 1614
        try:
            if not math.isclose(dataBase.points[i], dataBase.points[i+1], abs_tol= 1614) :
                # Si no es cercana, se dibuja su nombre
                # Esto es asi para que no se llene el grafico con 160 nombres todos apretados
                ax.annotate(txt, (dataBase.name[i], dataBase.points[i]))
        except:
            exit
    plt.grid()
    plt.show()

def free():
    # Gets all the free champions of the week
    freeChamps = (f"https://{my_region}.api.riotgames.com/lol/platform/v3/champion-rotations"+ "?api_key=" + api_key)
    r = requests.get(freeChamps)
    data = json.loads(r.text)
    champsFree = []
    champsDictName = getAllChampions()
    for id in data['freeChampionIds']:
        champsFree.append({'id': id , 'name': champsDictName[id]})
    ToJson(champsFree, "free")
    return champsFree

def api(name):
    me = watcher.summoner.by_name(my_region, name)
    summonerID = me['id']
    puuid = me['puuid']
    APIchampions = (f"https://{my_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerID}" + "?api_key=" + api_key)
    champsPoints = []
    r = requests.get(APIchampions)
    data = json.loads(r.text)
    champsDictName = getAllChampions()
    # Se consigue de la api los datos necesarios y se pasan a modo json
    for item in data:
        id = item['championId']
        points = item['championPoints']
        champsPoints.append({ 'id' : id , 'points' : points, 'name' : champsDictName[id]})
    # Se pasa a .JSON para tenerlo guardado
    ToJson(champsPoints, "points")
    #df = pd.DataFrame(champsPoints)
    #bar(df)
    # Se grafica

def ToJson(dict, place):
    # Pasa diccionarios a JSON              
    with open(f'./static/{place}.json', "w") as jsonFile:
        jsonFile.write(json.dumps(dict))

#def toCSV(lists):
 #   with open('./static/campeones.csv', 'w') as f:
  #      writer = csv.writer(f)
   #     writer.writerows(lists)

def getAllChampions():
    champsDict = {}
    file = open('./static/champion.json', encoding= "utf8")
    data2 = json.load(file)
    todo = data2['data']
    # Se consigue toda la data de los campeones
    for champions in data2['data']:
        champion = todo[champions]
        #champion es toda la informacion que hay de cada campeon
        #print(champion)
        id = int(champion['key'])
        name = champion['name']
        champsDict.update({id : name})
        # Se achica la data para que sea solo el ID y su nombre
    return champsDict

#free()
api("JimCharles3")
#matches(puuid)
