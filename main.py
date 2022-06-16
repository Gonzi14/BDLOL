from csv import writer, DictWriter
from filecmp import cmp
import sys
from sqlite3 import Row
from textwrap import dedent
from xml.etree.ElementTree import tostring
# Para hacer graficos
import matplotlib.pyplot as plt
# Para modificar csv
import pandas as pd
# Para APIs
from riotwatcher import LolWatcher, ApiError
import requests
import json
# Para ordenar los diccionarios
import collections
# Para no matar a la API
import time

api_key = ''
watcher = LolWatcher(api_key)
my_region = 'la2'
me = watcher.summoner.by_name(my_region, 'JimCharles3')
summonerID = me['id']
puuid = me['puuid']
API = (f"https://{my_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerID}" + "?api_key=" + api_key)
current_champ_list = watcher.data_dragon.champions('12.11.1')


def matches(puuid):
    while True:
        my_matches = watcher.match.matchlist_by_puuid(my_region, puuid)
        last_match = my_matches[0]
        while last_match == my_matches[0]:
            my_matches = watcher.match.matchlist_by_puuid(my_region, puuid)
            time.sleep(1)
            print(last_match)
        api(API)
        print("Ya esta")
        last_match = my_matches[0]
def bar(dataBase):
    plt.style.use('ggplot')
    plt.bar(dataBase.keys(), dataBase.values(), color='#e36685')
    plt.grid()
    plt.show()

def api(API):
    champsDicPoints = {}
    r = requests.get(API)
    data = json.loads(r.text)
    for item in data:
        ID = item['championId']
        points = item['championPoints']
        champsDicPoints.update({ID: points})
    champsDictName = getAllChampions()
    pointsDictN = sort(champsDicPoints)
    nameDictN = sort(champsDictName)
    for i in nameDictN:
        try:
            pointsDictN[nameDictN[i]] = pointsDictN[i]
            del pointsDictN[i]
        except:
            pointsDictN[nameDictN[i]] = 0
    toCSV(pointsDictN)
    bar(pointsDictN)    

def sort(dictionary):
    items = dictionary.items()
    itemsSorted = sorted(items)
    newDict = dict((x, y) for x, y in itemsSorted)
    return newDict

def toCSV(dict):
    with open('Campeones.csv', 'w') as f:
        writer = DictWriter(f, dict.keys())
        writer.writeheader()
        writer.writerow(dict)

def getAllChampions():
    champsDict = {}
    file = open('champion.json', encoding= "utf8")
    data2 = json.load(file)
    todo = data2['data']
    for champions in data2['data']:
        champion = todo[champions]
        id = int(champion['key'])
        champsDict.update({id : champions})
    return champsDict

def main(tipo, champ, puntos):
    print(tipo)
    print(champ)
    print(puntos)
    if int(tipo) == 0:
        agregar(champ, puntos)
    elif int(tipo) == 1:
        eliminar(champ)
    elif int(tipo) == 2:
        modificar(champ, puntos)

def agregar(campeon, puntos):
    with open(r"Campeones.csv", 'a') as df:
        champ = [campeon, puntos]
        agregar = writer(df)
        agregar.writerow(champ)
        df.close()

def eliminar(campeon):
    df = pd.read_csv(r"Campeones.csv")
    posicion = df.Campeones[df.Campeones == campeon].index.tolist()
    print(posicion)
    df = df.drop(df.index[posicion])
    print(df)
    df.to_csv(r"Campeones.csv", index = False)

def modificar(campeon, puntos):
    df = pd.read_csv(r"Campeones.csv")
    posicion = df.Campeones[df.Campeones == campeon].index.tolist()
    df.loc[posicion] = [campeon, puntos]
    df['Puntos'] = df['Puntos'].astype(int)
    df['Puntos'].sort_values()
    print(df)
    df.to_csv(r"Campeones.csv", index = False)
    bar(df['Campeones'], df['Puntos'])

matches(puuid)