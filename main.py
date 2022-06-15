from csv import writer
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

api_key = ''
watcher = LolWatcher(api_key)
my_region = 'la2'
summonerID = "46xpRlJSHOMNuWC9dTkUlSI4idgwCuzi0VJLGxNRnW3U33A"
API = (f"https://{my_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerID}" + "?api_key=" + api_key)

def bar(dataBase):
    plt.style.use('ggplot')
    plt.bar(dataBase[0].keys(), dataBase[0].values(), color='#e36685')
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
    champs_dictName = getAllChampions()
    for keys in sorted (champsDicPoints) :
        print((keys, champsDicPoints[keys]), end =" ")
        if champs_dictName[keys] == champsDicPoints[keys]:
            champsDicPoints[keys] = {champs_dictName[keys]: points}
    print(champsDicPoints)
    #dict_final = {}

current_champ_list = watcher.data_dragon.champions('12.11.1')
#print(current_champ_list)

def getAllChampions():
    champs_dict = {}
    file = open('champion.json', encoding= "utf8")
    data2 = json.load(file)
    todo = data2['data']
    for champions in data2['data']:
        champion = todo[champions]
        id = champion['key']
        champs_dict.update({id : champions})
    return champs_dict

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

#main(sys.argv[1], sys.argv[2], sys.argv[3])
api(API)