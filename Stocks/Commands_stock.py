from discord.ext import commands
from discord import app_commands, Interaction

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
                if interaction.user.get_role(id) != None:
                    return True
            else:
                await interaction.response.send_message(content= "Vous n'avez pas les permisions requises !!!")
                return False

        return app_commands.check(predicate)
