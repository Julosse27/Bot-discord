from flask import Flask
from threading import Thread
from Jeu.Recup_fichiers import recup_fichier

app = Flask("")

@app.route('/')
def home():
    return "Le Bot est en ligne !"

@app.route("/Test.txt")
def render():
    return open("Test_txt.txt", "rb")

@app.route("/Tel_jeu/kenji_battle.ico")
def img():
    return recup_fichier("Kenji_Battle.ico")

def run():
    app.run(host= "0.0.0.0", port= 8080)

def keep_alive():
    t = Thread(target= run)
    t.start()


