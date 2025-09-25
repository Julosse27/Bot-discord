import os

dirname = os.path.realpath(os.path.dirname(__file__))

file_not_exist = f"{dirname}/file_not_exist.txt"

def recup_fichier(fichier: str):

    if not os.path.exists(f"{dirname}/{fichier}"):
        return open(file_not_exist, "r")
    
    file = open(f"{dirname}/{fichier}", "rb")
    
    return file

def recup_path(fichier: str):

    path = f"{dirname}/{fichier}"

    if not os.path.exists(path):
        return None
    
    return path
