import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

token = os.getenv("DISCORD_TOKEN", "")

class Global(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Groupe de commandes générales presque basiques."

    @commands.command(name= "help", brief= "Un peu d'aide.", description= "Donne de l'aide sur une commande ou un groupe commandes.")
    async def help(self, ctx: commands.Context, command = None):
        
        if command == None:
            em = discord.Embed(title= "Help", description= "Utilisez cette même commande avec le nom de la commande ou du groupe de commandes(cog) que vous voulez comprendre pour avoir de l'aide.", color= ctx.author.color)

            for name in self.bot.cogs:

                list_name_command = []
                for command in self.bot.cogs.get(name, commands.Cog).__cog_commands__:
                    list_name_command.append(f"'command.name'")

                em.add_field(name= name, value= f"Commandes: {", ".join(list_name_command)}.")
        
        else:
            for command_help in liste_commands:
                if command == command_help.name or command in command_help.aliases:
                    if command_help.hidden:
                        em = discord.Embed(title= "Cette commande/cog n'est pas disponible.")
                        break
                    else:
                        em = discord.Embed(title= command_help.name, description= command_help.description, color= ctx.author.color)

                        aliases = command_help.aliases

                        if len(aliases) != 0:
                            em.add_field(name= "Aliases", value= f"{", ".join(aliases)}.")

                        break
            else:
                for cog in liste_help_cog:
                    if command == cog.__cog_name__:
                        em = discord.Embed(title= cog.__cog_name__, description= cog.description, color= ctx.author.color)

                        for commands_help in cog.get_commands():
                            if not commands_help.hidden:
                                em.add_field(name= commands_help.name, value= commands_help.brief)
                        break
                else:
                    em = discord.Embed(title= "Cette commande/cog n'est pas disponible.")

        await ctx.send(embed= em)

class Le_bot(commands.Bot):

    async def setup_hook(self):

        liste_cogs = ["Modération", "Tests", "Tutos"]

        global liste_commands, liste_help_cog

        liste_commands = []
        liste_help_cog = []

        self.remove_command("help")

        for extension in liste_cogs:

            for cog in self.cogs:
                await self.remove_cog(cog)
                print(f"L'ancienne extension {extension} à bien été remplacée.")
            
            await self.load_extension(f"Cogs.{extension}")

            for command in self.cogs.get(extension, commands.Cog(self)).get_commands():
                liste_commands.append(command)
            
            liste_help_cog.append(self.get_cog(extension))

        await self.add_cog(Global(self))

        for command in self.cogs.get("Global", commands.Cog(self)).get_commands():
            liste_commands.append(command)

        liste_help_cog.append(self.get_cog("Global"))

    async def on_ready(self):
        print(f"Connecté en tant que {bot.user}")
        synced = await bot.tree.sync()
        print(f'{len(synced)} commande(s) syncronisée(s)')

intents = discord.Intents.all()

bot = Le_bot(command_prefix= "$", description= "Le bot qui sers à tout et à rien !!!", intents=intents, owner_id= 948981926264467466)

keep_alive()

bot.run(token= token)
