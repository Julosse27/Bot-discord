from discord.ext import commands
import requests

url_test = "https://bot-discord-13wx.onrender.com/test.txt"

def check_me(*ids):
        
        async def predicate(ctx: commands.Context):
            for id in ids:
                if ctx.author.get_role(id) != None:
                    return True
            else:
                await ctx.send(content= f"Vous n'avez pas les permisions requises {ctx.author.name}!!!")
                return False

        return commands.check(predicate)

def get_test():
     result = requests.get(url_test)
     return result.content


