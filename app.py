from flask import Flask, redirect, render_template, request
from helpers import VillesListe, LanguesListe, recommendation

app = Flask(__name__)

use_reloader=True

villes = VillesListe()
langues = LanguesListe()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        if request.form['action'] == 'Ajoute un hotêl':
            return redirect("/encours")
        return redirect("/suggestion")
    

@app.route("/suggestion", methods=["GET", "POST"])
def suggestion():
    if request.method == "POST":
        if request.form.get('vil'):
            vil = str(request.form.get('vil'))
        else:
            vil = None
        if request.form.get('lan'):
            lan = str(request.form.get('lan'))
        else:
            lan = None
        if request.form.get('prompt'):
            prompt = str(request.form.get('prompt'))
        else:
            prompt = None
        # if request.form.get('price'):
        #     price = str(request.form.get('price'))
        # else:
        #     price = None

        result = recommendation(ville=vil, langue=lan, preference=prompt) #, prix=price
        output = []
        for element in result:
            element[5] = str(element[5])
            output.append("<br>".join(element))

        return render_template("suggestion.html", villes=villes, langues=langues, result=output)
    else:
        return render_template("suggestion.html", villes=villes, langues=langues, result="")


@app.route("/encours", methods=["GET", "POST"])
def encours():
    return render_template("encours.html")