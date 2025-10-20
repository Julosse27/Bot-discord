import tkinter as tk
from requests import get

fenetre = tk.Tk()
fenetre.title("Télécharger un jeu !!")
fenetre.geometry("400x500")
fenetre.iconbitmap(get("https://bot-discord-13wx.onrender.com/telechargement_logo.bmp"))

jeu = tk.StringVar(value= "Kenji_Battle")
version = tk.IntVar(value= 1)
executable = tk.BooleanVar(value= True)
spécifications = {
    "Kenji_Battle": {
        "intro": "Kenji Battle est le jeu que Julosse\ncode en ce moment même.\nIl est bien sur disponible au\ntéléchargement et je le recommande.",
        "versions": ["V0.5", "V2"],
        "dispo": True,
        "v_dispo": [True, False]
    },

    "Battle_Boat": {
        "intro" : "Battle Boat n'est qu'un petit jeu\nque l'on a créé lors d'un concour. \n Il n'est malheureusement pas disponible.",
        "versions": [],
        "dispo": False,
        "v_dispo": []
    }
}
versions_names = tk.Variable(value= spécifications["Kenji_Battle"]["versions"])

def change_parametres(*args):
    global url_base
    if spécifications[jeu.get()]["dispo"]:
        url_base = f"https://bot-discord-13wx.onrender.com/{jeu.get()}/{spécifications[jeu.get()]['versions'][version.get()]}"
    else:
        url_base = "Le jeu n'est pas dispo"
    print(url_base)

change_parametres()

def change_affichage(*args):
    description.config(text= spécifications[jeu.get()]["intro"])
    versions_names.set(value= spécifications[jeu.get()]["versions"])

    for name in select_version.children:
        select_version.children.get(name, tk.Label()).pack_forget()
    
    for name in versions_names.get():
        tk.Radiobutton(select_version, text= name, value= versions_names.get().index(name), variable= version, fg= "red", font= ("arial", 11)).pack(side= tk.LEFT, padx= 3)

tk.Label(fenetre, text= "Un jeu à\ntélécharger?", font= ("Arial", 20), fg= "darkorange").pack()

select_jeu = tk.Frame(fenetre)
select_jeu.pack(pady= (20, 0))

tk.Radiobutton(select_jeu, text= "Kenji Battle", variable= jeu, value= 'Kenji_Battle', fg= "blue", font= ("arial", 11, "bold")).pack(side= tk.LEFT)
tk.Radiobutton(select_jeu, text= "Battle Boat", variable= jeu, value= 'Battle_Boat', fg= "blue", font= ("arial", 11, "bold")).pack(side= tk.LEFT)

description = tk.Label(fenetre, text= "", font= ("Arial", 13), fg= "darkgreen")
description.pack()

tk.Label(fenetre, text= "Quelle version veut tu ?", font= ("arial", 14)).pack()

select_version = tk.Frame(fenetre)
select_version.pack(pady= (10, 0))

change_affichage()

jeu.trace_add('write', change_parametres)
jeu.trace_add('write', change_affichage)
version.trace_add('write', change_parametres)

fenetre.mainloop()