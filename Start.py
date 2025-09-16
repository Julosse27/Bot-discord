import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

token = os.getenv("DISCORD_TOKEN")

class Le_bot(commands.Bot):
    async def setup_hook(self):
        self.remove_command("Exos_select")
        for extension in ["Modération", "Tests", "Tutos_cog"]:
            await self.load_extension(f"Cogs.{extension}")

    async def on_ready(self):
        print(f"Connecté en tant que {bot.user}")
        synced = await bot.tree.sync()
        print(f'{len(synced)} commande(s) syncronisée(s)')

intents = discord.Intents.all()

bot = Le_bot(command_prefix= "$", description= "Le bot qui sers à tout et à rien !!!", intents=intents, owner_id= 948981926264467466)

keep_alive()

bot.run(token= token)

