import os

dirname = os.path.relpath(os.path.dirname(__file__))

def recup_fichier(fichier: str):
    return open(fr"{dirname}\{fichier}", "rb")