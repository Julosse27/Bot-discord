version = "V2"
executable = True

url_base = f"https://bot-discord-13wx.onrender.com/Kenji_Battle/{version}"

import os
from requests import get

bureau = rf"{os.path.realpath(os.getenv("homepath", ""))}\Desktop"

print("Voulez vous l'installer sur le bureau ou dans le même fichier que celui-ci ?")
rep = input("O pour oui, N pour non").lower()

if rep == "o":
    pass

if not os.path.exists(bureau):
    if os.getenv("computername") == "JULOSSEPC2":
        bureau = r"d:\User\Jules\Bureau"
    else:
        bureau = os.path.realpath(".")
        print(f"Le fichier sera téléchargé ici: {bureau} puisque votre bureau n'est pas disponible.")
        print("Etes vous d'accord ? (Réponse: O pour oui N pour non)")
        rep = input().lower()
        if rep == "n":
            raise Exception("Placez ce fichiez dans le dosier où vous voulez l'installer.")

if executable:
    architecture = get(f"{url_base}/architecture_exe.txt").content.decode().splitlines()
else:
    architecture = get(f"{url_base}/architecture.txt").content.decode().splitlines()

if not os.path.exists(rf"{bureau}\Kenji_Battle\{version}"):
    os.makedirs(rf"{bureau}\Kenji_Battle\{version}")

for file in architecture:
    file = file.split(", ")

    chemin = fr"{bureau}\{file[0]}"
    file = f"{url_base}/{file[1]}"

    response = get(file)
    
    if not os.path.exists(os.path.dirname(chemin)):
        os.makedirs(os.path.realpath(os.path.dirname(chemin)))
    
    open(chemin, "w+b").write(response.content)