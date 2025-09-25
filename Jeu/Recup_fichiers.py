import os

dirname = os.path.relpath(os.path.dirname(__file__))

def recup_fichier(fichier: str):

    return open(__file__, "r"), __file__


