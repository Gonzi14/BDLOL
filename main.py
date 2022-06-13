from csv import writer
import sys
from sqlite3 import Row
from xml.etree.ElementTree import tostring
# Para hacer graficos
import matplotlib.pyplot as plt
#Para modificar csv
import pandas as pd

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

def bar(campeones, puntos):
    plt.style.use('ggplot')
    plt.bar(campeones, puntos, color='#e36685')
    plt.grid()
    plt.show()

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

main(sys.argv[1], sys.argv[2], sys.argv[3])