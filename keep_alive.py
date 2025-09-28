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

@app.route("/Kenji_Battle/V2")
def a():
    return recup_fichier("Kenji_Battle/V2/V2.py"), recup_fichier("Kenji_Battle.ico")

def run():
    app.run(host= "0.0.0.0", port= 8080)

def keep_alive():
    t = Thread(target= run)
    t.start()   
