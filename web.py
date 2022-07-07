from cProfile import run
from flask import Flask, render_template, json, url_for
import main 
import os

app = Flask(__name__)

@app.route('/')
def index():

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "points.json")
    data = json.load(open(json_url))
    return render_template('table.html', data = data)

if __name__ == "__main__":
    app.run()
    #main