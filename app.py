from flask import Flask, redirect, render_template, request, flash
from helpers import VillesListe, LanguesListe, recommendation

app = Flask(__name__)

use_reloader=True
app.secret_key = "pfa{it's_a_secret}"

villes = VillesListe()
langues = LanguesListe()
villes.remove("tangier")
villes.remove("fez")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        if request.form['action'] == 'Ajoute un hôtel':
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
        if request.form.get('price'):
            price = str(request.form.get('price'))
        else:
            price = None
        if request.form.get('pamen'):
            pamen = True
        else:
            pamen = False
        if request.form.get('rfea'):
            rfean = True
        else:
            rfea = False
        if request.form.get('rtyp'):
            rtyp = True
        else:
            rtyp = False

        result = recommendation(ville=vil, langue=lan, preference=prompt, prix=price, pamen=pamen, rfea=rfea, rtyp=rtyp) 
        output = []
        for element in result:
            element[1] = str(element[1])
            element[2] = str(element[2])
            element[5] = str(element[5])
            element[7] = str(element[7])
            output.append("<br>".join(element))
        if len(output) == 0:
            flash('Aucun résultat trouvé.')
        return render_template("suggestion.html", villes=villes, langues=langues, result=output)
    else:
        return render_template("suggestion.html", villes=villes, langues=langues, result="")


@app.route("/encours", methods=["GET", "POST"])
def encours():
    return render_template("encours.html")