from flask import Flask
from threading import Thread
from Stocks.File_stock.Recup_fichiers import recup_fichier, recup_path

app = Flask("")

@app.route('/')
def home():
    return "Le Bot est en ligne !"

@app.route("/Test.txt")
def render():
    return recup_fichier("test.txt")

@app.route("/kenji_battle.ico")
def img():
    return recup_fichier("Kenji_Battle.ico")

@app.route("/Kenji_Battle/V2/V2.py")
def a():
    return recup_fichier("Kenji_Battle/V2/V2.py")

@app.route("/Kenji_Battle/V2/architecture.txt")
def b():
    return recup_fichier("Kenji_Battle/V2/architecture.txt")

@app.route("/Kenji_Battle/V2/architecture_exe.txt")
def e():
    return recup_fichier("Kenji_Battle/V2/architecture_exe.txt")

@app.route("/Kenji_Battle/V2/V2.exe")
def f():
    return recup_fichier("Kenji_Battle/V2/V2.exe")

@app.route("/Kenji_Battle/V2/Données.sq3")
def c():
    return recup_fichier("Kenji_Battle/V2/Données.sq3")

@app.route("/Kenji_Battle/V2/kenji_battle_ressources.pyxres")
def d():
    return recup_fichier("Kenji_Battle/V2/Kenji_Battle_Ressource.pyxres")

def run():
    app.run(host= "0.0.0.0", port= 8080)

def keep_alive():
    t = Thread(target= run)
    t.start()
