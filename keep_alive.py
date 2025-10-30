from flask import Flask
from threading import Thread
from Stocks.File_stock.Recup_fichiers import recup_fichier

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
    return recup_fichier("Kenji_Battle/V2/kenji_battle_ressources.pyxres")

@app.route("/telechargement_logo.png")
def de():
    return recup_fichier("logo_tel.png")

@app.route("/Kenji_Battle/V0.5/kenji_battle_ressources.pyxres")
def ge():
    return recup_fichier("/Kenji_Battle/V0.5/kenji_battle_ressources.pyxres")

@app.route("/Kenji_Battle/V0.5/architecture.txt")
def ls():
    return recup_fichier("Kenji_Battle/V0.5/architecture.txt")

@app.route('/Kenji_Battle/V0.5/V0.5.py')
def ld():
    return recup_fichier("Kenji_Battle/V0.5/V0.5.py")

@app.route("/Kenji_Battle/V0.5/architecture_exe.txt")
def dds():
    return recup_fichier("Kenji_Battle/V0.5/architecture_exe.txt")

@app.route('/Kenji_Battle/V0.5/V0.5.exe')
def fdfdf():
    return recup_fichier('Kenji_Battle/V0.5/V0.5.exe')

def run():
    app.run(host= "0.0.0.0", port= 8080)

def keep_alive():
    t = Thread(target= run)
    t.start()