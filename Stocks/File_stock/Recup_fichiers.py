import os
from typing import Literal

dirname = os.path.realpath(os.path.dirname(__file__))

file_not_exist = f"{dirname}/file_not_exist.txt"

def recup_fichier(fichier: str):
    r"""
    Cette fonction va permettre de rechercher un fichier 
    dans les dossiers du bot.
    Elle le renverra sous la forme de bits (mode `rb`) pour convenir à
    tout les formats de fichiers.
    
    :param fichier: Le chemin jusqu'au fichier du bot.
    :type fichier: str

    :return file: Le fichier qui est trouvé à l'enplacement
    /!\ si il n'est pas trouvé cette fonction renverra un fichier type.
    """

    if not os.path.exists(f"{dirname}/{fichier}"):
        return open(file_not_exist, "rb")
    
    file = open(f"{dirname}/{fichier}", "rb")
    
    return file

def recup_sqlite(nom_fichier: str):
    """
    Cette fonction va récupérer un fichier sqlite.
    
    :param nom_fichier: Le nom du fichier que vous voulez trouver.
    :type nom_fichier: str

    :return path: Le chemin complet jusqu'a ce fichier.
    """
    path = f"{dirname}/sqlite/{nom_fichier}"
    
    return path

def recup_path(fichier: str):
    r"""
    Cette fonction va permettre de rechercher le chemin complet d'un fichier 
    dans les dossiers du bot.
    
    :param fichier: Le chemin jusqu'au fichier du bot.
    :type fichier: str

    :return file: Le chemin du fichier.
    /!\ si il n'est pas trouvé cette fonction renverra le chemin d'un fichier type.
    """

    path = f"{dirname}/{fichier}"

    if not os.path.exists(path):
        return file_not_exist
    
    return path
