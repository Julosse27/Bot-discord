import os

dirname = os.path.realpath(os.path.dirname(__file__))

def recup_fichier(fichier: str):

    return open(f"{dirname}/{fichier}", "rb")






