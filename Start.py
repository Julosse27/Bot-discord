import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

class Le_bot(commands.Bot):
    async def setup_hook(self) -> None:
        for extension in ["Modération", "Tests"]:
            await self.load_extension(f"Cogs.{extension}")

intents = discord.Intents.all()

bot = Le_bot(command_prefix= "$", description= "Le bot qui sers à tout et à rien !!!", intents=intents)

keep_alive()

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    synced = await bot.tree.sync()
    print(f'{len(synced)} commande(s) syncronisée(s)')

bot.run(token= token)