import os
from typing import Literal

dirname = os.path.realpath(os.path.dirname(__file__))

file_not_exist = f"{dirname}/file_not_exist.txt"

def recup_fichier(fichier: str, mode: Literal["rb", "r"] = "rb"):
    r"""
    Cette fonction va permettre de rechercher un fichier 
    dans les dossiers du bot.
    Elle le renverra sous la forme de bits (mode `rb` ou `r`) pour convenir à
    tout les formats de fichiers.
    
    :param fichier: Le chemin jusqu'au fichier du bot.
    :type fichier: str
    :param mode: Par default `rb` celui change le mode de lecture.
    :type mode: Literal["rb", "r"]

    :return file: Le fichier qui est trouvé à l'emplacement.
    /!\ si il n'est pas trouvé cette fonction renverra un fichier type.
    """

    if not os.path.exists(f"{dirname}/{fichier}"):
        with open(file_not_exist, mode) as file:
            return_file = file.read()
        return return_file
    
    with open(f"{dirname}/{fichier}", mode) as file:
        return_file = file.read()
    
    return return_file

def recup_sqlite(nom_fichier: str):
    """
    Cette fonction va récupérer un fichier sqlite.
    
    :param nom_fichier: Le nom du fichier que vous voulez trouver.
    :type nom_fichier: str

    :return path: Le chemin complet jusqu'a ce fichier.
    """
    path = f"{dirname}/sqlite/{nom_fichier}.sq3"
    
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

def recup_script_sql(nom_fichier:str):
    r"""
    Cette fonction va permettre de rechercher le script sql avec le nom donné.

    :param nom_fichier: Le nom du fichier dans la mémoire du bot.
    :type nom_fichier: str

    :return file: Le contenu du fichier en str.
    /!\ si il n'est pas trouvé cette fonction renverra le chemin d'un fichier type.
    """

    path = f"{dirname}/sqlite/scripts/{nom_fichier}.sql"

    if not os.path.exists(path):
        with open(file_not_exist) as file:
            rep = file.read()
    else:
        with open(path) as file:
            rep = file.read()
    
    return rep