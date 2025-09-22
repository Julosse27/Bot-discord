from discord.ext import commands
from requests import get

contenu_f = {"test.txt": get("https://bot-discord-13wx.onrender.com/test.txt").content}

def check_me(*ids):
        
        async def predicate(ctx: commands.Context):
            for id in ids:
                if ctx.author.get_role(id) != None:
                    return True
            else:
                await ctx.send(content= "Vous n'avez pas les permisions requises !!!")
                return False

        return commands.check(predicate)

def get_test(nom_fichier: str) -> bytes:
     return contenu_f[nom_fichier]
