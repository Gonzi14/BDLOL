from cProfile import run
from flask import Flask, render_template, json, url_for
import main 
import os

app = Flask(__name__)

@app.route('/table')
def table():

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "points.json")
    dataMine = json.load(open(json_url))
    return render_template('table.html', dataMine = dataMine )

@app.route('/free')
def free():

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "free.json")
    dataMine = json.load(open(json_url))
    return render_template('free.html', dataMine = dataMine )

@app.route('/chart')
def chart():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "points.json")
    dataMine = json.load(open(json_url))
    return render_template('chart.html', dataMine = dataMine )
if __name__ == "__main__":
    app.run()
    # Se pueda buscar por nombre, cambiando el nombre del cual se busca a traves de un input
    # Ver quienes se actualizaron y cuanto
    # Agregar filtros
    # Agregar los champs gratis
    # Poder clickear un champ y que me lleve a un lugar con toda info suya(champion.json)
    # Agregar despues el main.py