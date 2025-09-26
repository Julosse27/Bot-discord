import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

class Le_bot(commands.Bot):

    async def setup_hook(self):

        liste_cogs = ["Modération", "Tests", "Tutos"]

        global liste_commands, liste_help_cog

        liste_commands = []
        liste_help_cog = []

        for extension in liste_cogs:

            self.remove_command("help")

            if self.get_cog(extension) != None:

                await self.unload_extension(extension)
                print(f"L'ancienne extension {extension} à bien été remplacée.")
            
            await self.load_extension(f"Cogs.{extension}")

            for command in self.get_cog(extension).get_commands():
                liste_commands.append(command)
            
            liste_help_cog.append(self.get_cog(extension))

    async def on_ready(self):
        print(f"Connecté en tant que {bot.user}")
        synced = await bot.tree.sync()
        print(f'{len(synced)} commande(s) syncronisée(s)')

intents = discord.Intents.all()

bot = Le_bot(command_prefix= "$", description= "Le bot qui sers à tout et à rien !!!", intents=intents, owner_id= 948981926264467466)

@bot.command(name= "help", brief= "Juste de l'aide", description= "Donne de l'aide sur une commande ou sur un groupe de commandes(cog).")
async def help(ctx: commands.Context, command = None):
    if command == None:
        em = discord.Embed(title= "Help", description= "Utilisez cette même commande avec le nom de la commande que vous voulez comprendre pour avoir de l'aide.", color= ctx.author.color)

        em.add_field(name= "Modération", value= "Commandes: 'message', 'kick'")
        em.add_field(name= "Tests", value= "Commandes: 'bouton', 'menu', 'download'")
        em.add_field(name= "Tutos", value= "Commandes: 'exos_select'")
    else:
        for command_help in liste_commands:
            if command == command_help.name or command in command_help.aliases:
                if command_help.hidden:
                    em = discord.Embed(title= "Cette commande/cog n'est pas disponible.")
                    break
                else:
                    em = discord.Embed(title= command_help.name, description= command_help.description, color= ctx.author.color)
                    break
        else:
            for cog in liste_help_cog:
                if command == cog.__cog_name__:
                    em = discord.Embed(title= cog.__cog_name__, description= cog.description, color= ctx.author.color)

                    for commands in cog.get_commands():
                        em.add_field(name= commands.name, value= commands.brief)
                    
                    break
            else:
                em = discord.Embed(title= "Cette commande/cog n'est pas disponible.")

    await ctx.send(embed= em)

keep_alive()

bot.run(token= token)
