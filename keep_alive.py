from flask import Flask, request, jsonify
from threading import Thread
from Stocks.File_stock.Recup_fichiers import recup_fichier, recup_sqlite
from requests import head, get
from logging import info
from time import sleep
from sqlite3 import connect

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

@app.route('/Cafet/données', methods = ['POST', 'GET'])
def créer():
    conn = connect(recup_sqlite("données.sq3"))
    cur = conn.cursor()
    rep = ""
    if request.method == 'POST':
        try:
            test_supp = request.get_data(as_text= True)
            if test_supp == "réinitialisation":
                cur.execute("delete from ventes_journalières")
                conn.commit()
            data: dict[str, int | str] = request.json
            noms: list[str] = []
            donnees: list[str] = []

            for nom, donnee in data.items():
                if type(donnee) == int:
                    donnee = str(donnee)
                elif type(donnee) == str:
                    donnee = f"'{donnee}'"
                noms.append(nom)
                donnees.append(donnee)  # pyright: ignore[reportArgumentType]

            cur.execute(f'''insert into ventes_journalières({", ".join(noms)}) values({", ".join(donnees)})''')
            conn.commit()
            rep = "Il n'y a eu aucun problème."
        except Exception as e:
            rep = f"Il y a eu une erreur:\n{e}"
    elif request.method == 'GET':
        rep = jsonify(cur.execute("select * from ventes_journalières").fetchall())
        
    cur.close()
    conn.close()
    return rep

def recuperation():
    response = get("https://bot-discord-13wx.onrender.com/Cafet/données")
    anciennes_infos = response.json()
    info(anciennes_infos)
    conn = connect(recup_sqlite("données.sq3"))
    cur = conn.cursor()
    for donnees in anciennes_infos:
        for i in range(len(donnees)):
            element = donnees[i]
            if type(element) == str:
                donnees[i] = f"'{element}'"
            elif type(element) == int:
                donnees[i] = str(element)
        cur.execute(f"insert into ventes_journalières(capucino, noisette, caramel, citron, menthe, café, chocolat, nom_jour, date) values({", ".join(donnees)})") # pyright: ignore[reportArgumentType, reportCallIssue]
    conn.commit()
    cur.close()
    conn.close()

def run():
    app.run(host= "0.0.0.0", port= 8080)

def ping():
    while True:
        response = head("https://bot-discord-13wx.onrender.com")
        if response.status_code == 404:
            info("L'accés au site est impossible.")
            return
        elif response.status_code == 200:
            info("Tout c'est bien passé durant ce ping.")
        else:
            info(f"Le site à un problème inconnu dont le code est {response.status_code}.")
        sleep(120)

def keep_alive():
    recuperation()
    t = Thread(target= run)
    t.start()
    e = Thread(target= ping)
    e.start()