from flask import Flask, request, jsonify, render_template_string
from threading import Thread
from Stocks.File_stock.Recup_fichiers import recup_fichier, recup_sqlite, recup_script_sql
from requests import head, get
from logging import info
from time import sleep
from sqlite3 import connect
from urllib.parse import quote
from json import load

app = Flask("")

@app.route('/', methods = ['POST', 'GET', 'HEAD'])
def home():
    rep = ""
    if request.method == 'POST':
        conn = connect(recup_sqlite(f"donnees_stock_cafet"))
        cur = conn.cursor()
        try:
            data: list = request.get_json()
            if data != None:
                donnees = list(map(str, data))

                cur.execute(f'''insert into ventes_journalières(stocks_achete, annee_scolaire) values({", ".join(donnees)})''')
                conn.commit()
                rep = "Il n'y a eu aucun problème."
            else:
                rep = "Les données n'ont pas été bien chargées"
        except Exception as e:
            rep = f"Il y a eu une erreur:\n{e}"
    elif request.method == 'GET':
        rep = render_template_string(recup_fichier("template.html", "r"), icone = quote(recup_fichier("icon.svg", "r")))
    elif request.method == 'HEAD':
        rep = "Le site est encore en ligne."
    return rep

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

@app.route('/Cafet/donnees', methods = ['POST', 'GET'])
def créer():
    conn = connect(recup_sqlite(f"donnees_stock_cafet"))
    cur = conn.cursor()
    rep = ""
    if request.method == 'POST':
        try:
            test_supp = request.get_data(as_text= True)
            if test_supp == "réinitialisation":
                cur.executescript(recup_script_sql("script_réinitialisation"))
                conn.commit()
                rep = f"La base de donnée a bien été réinitialisé."
            else:
                json_data = ", ".join(request.get_json())
                cur.execute(f"insert into ventes_journalières values ({json_data})")
        except Exception as e:
            rep = f"Il y a eu une erreur:\n{e}"
    elif request.method == 'GET':
        recuperation_donnees = request.args.get('recup', default= False, type= bool)
        if recuperation_donnees:
            rep = {}
            for nom_table in cur.execute("""select name from sqlite_master where type='table' and name not like 'sqlite_%'""").fetchall():
                rep[nom_table] = cur.execute(f"select * from {nom_table}").fetchall()

            rep = jsonify(rep)
        else:
            reinitialisation = request.args.get('reinit', False, bool)
            if reinitialisation:
                cur.executescript(recup_script_sql('script_réinitialisation_cafet'))
            else:
                table = request.args.get('table', default= "ventes")
                if table in ("suivi", "stock", "ventes"):
                    if table == "ventes":
                        annee_scolaire = request.args.get('annee_scolaire', default = '2025-2026')

                        contenu_base = cur.execute(f"select * from ventes_journalières where annee_scolaire = '{annee_scolaire}'").fetchall()

                        rep = list[dict]()

                        for element in contenu_base:
                            i = {}
                            i["stocks_achetee"] = load(element[0])
                            i["date"] = element[1]
                            i["annee_scolaire"] = element[2]

                            rep.append(i)

                        rep = jsonify(rep)
                    elif table == "stock":
                        contenu_base = cur.execute(f"select * from stocks").fetchall()

                        rep = list[dict]()

                        for element in contenu_base:
                            i = {}
                            i["nom"] = element[0]
                            i["stock"] = element[1]
                            i["etat_stock"] = element[2]

                            rep.append(i)

                        rep = jsonify(rep)
                    else:
                        annee_scolaire = request.args.get('annee_scolaire', default = '2025-2026')

                        contenu_base = cur.execute(f"select * from suivi_stocks where annee_scolaire='{annee_scolaire}'").fetchall()

                        rep = list[dict]()

                        for element in contenu_base:
                            i = {}
                            i["id"] = element[0]
                            i["nom_consommation"] = element[1]
                            i["quantite"] = element[2]
                            i["date"] = element[3]
                            i["annee_scolaire"] = element[4]

                            rep.append(i)

                        rep = jsonify(rep)
        
    cur.close()
    conn.close()
    return rep

def recuperation():
    try:
        response = get("https://bot-discord-13wx.onrender.com/Cafet/donnees?recup=True")
        anciennes_infos: dict[str, list] = load(response.content.decode())  #type:ignore
        conn = connect(recup_sqlite("donnees_stocks_cafet"))
        cur = conn.cursor()
        cur.execute("disable trigger verif_stocks, enregistrement_vente, maj_stocks")
        for nom_table, elements in anciennes_infos.items():
            if nom_table != "stocks":
                elements = list(map(str, elements))
                cur.execute(f"insert into {nom_table} values{", ".join(elements)}")
            else:
                nom_type = elements[0]
                donnees = list(map(str, elements[1:]))
                cur.execute(f"update stocks set stock = {donnees[0]}, etat_stock = {donnees[1]} where nom = {nom_type}")
                
        cur.execute("enable trigger verif_stocks, enregistrement_vente, maj_stocks")
        conn.commit()
        cur.close()
        conn.close()
    except:
        info("L'ancienne version de la base de donnée n'est pas disponible.")

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
    a = Thread(target= recuperation)
    a.start()
    a.join(10.0)
    t = Thread(target= run)
    t.start()
    e = Thread(target= ping)
    e.start()