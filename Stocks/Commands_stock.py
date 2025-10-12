from discord.ext import commands
from discord import app_commands, Interaction, datetime, Message, InteractionMessage
from time import asctime, sleep

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

    mois = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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

def get_defer_time(defer: int | list[int], /,format: bool = False) -> list[int] | datetime | None:
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
        Retourne :arg:`None` si un nombre dépase sa limite assignée
    """

    mois = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    date_time = asctime()

    annee: int = int(date_time[20:])
    mois_date: int = mois.index(date_time[4:7])
    jour: int = int(date_time[8:10])
    heures: int = int(date_time[11:13])
    minutes: int = int(date_time[14:16])
    secondes: int = int(date_time[17:19])

    if type(defer) == int:
        if defer > 60:
            return
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
            if limites[i] == None:
                date_time[i] += defer[i] #type: ignore
            elif defer[i] <= limites[i]: #type: ignore
                if date_time[i] + defer[i] >= limites[i]: #type: ignore
                    date_time[i+1] += 1
                    date_time[i] = date_time[i] + defer[i] - limites[i] #type: ignore
                else:
                    date_time[i] += defer[i] #type: ignore
            else:
                return

        reponse = list(reversed(date_time))

    if format:
        return reponse
    else:
        return datetime(year= reponse[0], month= reponse[1], day= reponse[2], hour= reponse[3], minute= reponse[4], second= reponse[5])

async def timer(secondes: int, message: Message | InteractionMessage, begining_rep: str = "", end_rep: str = "", minutes: int = 0, heures: int = 0, jours: int = 0, mois: int = 0, annee: int = 0) -> bool: #type:ignore
    r"""|coro|

    Cette fonction va elle même modifier le message qui a été préalablement ecrit avec un
    minuteur jusqu'au moment décidé.

    Pour fonctionner cette fonction doit récupérer l'interaction :class:`~discord.Interaction`
    ou le contexte :class:`~commands.Context`. 
    
    Paramètres
    ------------
    secondes: :class:`int`

        Le nombre de secondes que le minuteur doit afficher.
    fonction:

        La fonction que doit utiliser cette fonction pour pouvoir modifier le message.
    begining_rep: :class:`str`

        Le texte qui prècède le timer
    end_rep: :class:`str`

        Le texte qui suit le timer.
    minutes: Optionel[:class:`int`]

        Le nombre de minutes que le minuteur doit afficher.
    heures: Optionel[:class:`int`]

        Le nombre de heures que le minuteur doit afficher.
    jours: Optionel[:class:`int`]

        Le nombre de jours que le minuteur doit afficher.
    mois: Optionel[:class:`int`]

        Le nombre de mois que le minuteur doit afficher.
    annee: Optionel[:class:`int`]

        Le nombre de annee que le minuteur doit afficher.
    """

    tps = [secondes, minutes, heures, jours, mois, annee]
    noms = ["secondes", 'minutes', "heures", "jours", "mois", "année"]
    limites = [60, 60, 24, None, 12]
    limites_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if get_defer_time(tps) == None:
        return False

    while True:
        tps[0] -= 1
        for i in range(len(tps) - 1):
            if tps[i] < 0:
                tps[i + 1] -= 1
                if i != 3:
                    tps[i] = limites[i] - 1
                else:
                    tps[3] = limites_mois[get_actual_time()[1]] #type: ignore
        
        arreter = True
        rep = []
        for i in range(len(tps)):
            if tps[i] != 0:
                arreter = False
                rep.append(f"{tps[i]} {noms[i]}")
        
        if arreter:
            break

        rep = " et ".join(rep)

        message_content = f"{begining_rep} {rep} {end_rep}"

        await message.edit(content= message_content)

        sleep(1)

    return True
