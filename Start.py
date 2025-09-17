import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

token = os.getenv("DISCORD_TOKEN")

class Le_bot(commands.Bot):
    async def setup_hook(self):
        liste_cogs = ["AdminCog", "TestsCog", "TutosCog"]
        liste_fichiers = ["Modération", "Tests", "Tutos_cog"]
        for extension in liste_fichiers:
            if self.get_cog(liste_cogs[liste_fichiers.index(extension)]) != None:
                await self.unload_extension(liste_cogs[liste_fichiers.index(extension)])
                print(f"L'ancienne extension {liste_cogs[liste_fichiers.index(extension)]} à bien été remplacée.")
            await self.load_extension(f"Cogs.{extension}")

    async def on_ready(self):
        print(f"Connecté en tant que {bot.user}")
        synced = await bot.tree.sync()
        print(f'{len(synced)} commande(s) syncronisée(s)')

    async def on_command_error(self, context: commands.Context, exception: commands.CommandError) -> None:
        if exception == "failed":
            await context.send(content= "Vous n'avez pas les permisions requises !!!")
        else:
            return await super().on_command_error(context, exception)

intents = discord.Intents.all()

bot = Le_bot(command_prefix= "$", description= "Le bot qui sers à tout et à rien !!!", intents=intents, owner_id= 948981926264467466)

keep_alive()

bot.run(token= token)





