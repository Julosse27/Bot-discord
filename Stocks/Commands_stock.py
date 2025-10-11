from discord.ext import commands
from discord import app_commands, Interaction, datetime
from time import asctime

mois = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def check_basic_command(*ids):
    
    async def predicate(ctx):
        for id in ids:
            if ctx.author.get_role(id) != None:
                return True
        else:
            await ctx.send(content= "Vous n'avez pas les permisions requises !!!")
            return False

    return commands.check(predicate)

def check_slash_command(*ids):
    
    async def predicate(interaction: Interaction):
        for id in ids:
            if interaction.user.get_role(id) != None: # type: ignore
                return True
        else:
            await interaction.response.send_message(content= "Vous n'avez pas les permisions requises !!!")
            return False

    return app_commands.check(predicate)

def get_actual_time(format: bool = True) -> list[int] | datetime:
    """
    C'est une fonction qui va donner le temps soit dans une liste ou dans une classe
    spéciale pour un bot discord.

    Paramètres
    ------------
    format(optionel): :class:`bool`

        Définit le format de l'heure dont la fonction doit renvoyer l'information.
        De base le format :class:`list` représenté `True` mais peut être changé pour
        `False` correspondant à :class:`~discord.datetime`.
    """
    date_time = asctime()

    annee: int = int(date_time[20:])
    mois_date: int = mois.index(date_time[4:7])
    jour: int = int(date_time[8:10])
    heures: int = int(date_time[11:13])
    minutes: int = int(date_time[14:16])
    secondes: int = int(date_time[17:19])

    if format:
        return [annee, mois_date, jour, heures, minutes, secondes]
    else:
        return datetime(annee, mois_date, jour, heures, minutes, secondes)

def get_defer_time(defer: int | list[int], /,format: bool = False) -> list[int] | datetime:
    """
    C'est une fonction qui va donner le temps soit dans une liste ou dans une classe
    spéciale pour un bot discord.

    Elle va aussi y ajouter un nombre de secondes données.

    Paramètres
    ------------
    defer: Union[:class:`int`, :class:`list[int]`]

        Définit soit juste le nombre de secondes dont le programe doit avancer
        le temps actuel ou dans le cas d'une liste définit dans l'ordre :variable:`secondes`,
        :variable:`minutes`, :variable:`heures`, :variable:`jours`, :variable:`mois`, :variable:`année`
    format: :class:`bool` (optionel)

        Définit le format de l'heure dont la fonction doit renvoyer l'information.
        De base le format :class:`~discord.datetime` représenté `False` mais peut être changé pour
        `True` correspondant à :class:`list`.
    Raises
    --------
    ValueError
        Le nombre ou les nombres dans le paramètre :parameter:`defer` ne correspondent pas aux limites assignées.
    """

    date_time = asctime()

    annee: int = int(date_time[20:])
    mois_date: int = mois.index(date_time[4:7])
    jour: int = int(date_time[8:10])
    heures: int = int(date_time[11:13])
    minutes: int = int(date_time[14:16])
    secondes: int = int(date_time[17:19])

    if type(defer) == int:
        if defer >= 60:
            raise ValueError("Le nombre ou les nombre dans le paramètre defer ne correspondent pas aux exigences de niveau de temps.")
        if defer + secondes >= 60:
            minutes += 1
            secondes: int = secondes + defer - 60
        else:
            secondes += defer
        reponse = [annee, mois_date, jour, heures, minutes, secondes]
    else:
        date_time = [secondes, minutes, heures, jour, mois_date, annee]
        limites = [60, 60, 24, 31, 12, None]
        for i in range(len(defer)): #type: ignore
            if limites[i] != None and not defer[i] <= limites[i]: #type: ignore
                if date_time[i] + defer[i] >= limites[i]: #type: ignore
                    date_time[i+1] += 1
                    date_time[i] = date_time[i] + defer[i] - limites[i] #type: ignore
            elif defer[i] <= limites[i]: #type: ignore
                raise ValueError("Le nombre ou les nombre dans le paramètre defer ne correspondent pas aux exigences de niveau de temps.")

        reponse = list(reversed(date_time))

    if format:
        return reponse
    else:
        return datetime(year= reponse[0], month= reponse[1], day= reponse[2], hour= reponse[3], minute= reponse[4], second= reponse[5])
