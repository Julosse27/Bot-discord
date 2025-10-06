import discord
from discord.ext import commands
from Stocks.Commands_stock import check_basic_command, check_slash_command
from discord import app_commands

class Modération(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Cog spécialisé dans les commandes de moderations."

    @app_commands.command(name= "kick", description= "Kick un membre pour une raison(optionel)")
    @check_slash_command(1410343531402367006, 1382302424366186516, 1382303940921659412, 1382455975549599854)
    async def test(self, interaction: discord.Interaction, member: discord.Member, reason: str | None = None):
        # await member.kick(reason= reason)
        if reason == None:
            await interaction.response.send_message(content= f"Le membre {member.name} à été kick du serveur par {interaction.user.name} pour aucune raison.")
        else:
            await interaction.response.send_message(content= f"Le membre {member.name} à été kick du serveur par {interaction.user.name} pour la raison: {reason}.")

    @commands.command(name= "message", aliases= ["mes", "ping"], description= "Envois un message à qui tu veut.", brief= "Envois un mp.")
    @check_basic_command(1417199810099937411, 1382302424366186516, 1382303940921659412, 1382455975549599854)
    async def message(self, ctx, member: discord.Member, *, contenu: str):
        await member.send(content= contenu)
        await ctx.send(content = 'Message envoyé !')

    @commands.command(name= "kick", aliases= ["k"], description= "Kick la personne que t'aime pas de ce serveur.", brief= "Kick quelqu'un.")
    @check_basic_command(1382302424366186516)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason= reason)
        await ctx.send(f"{member.name} a bien été exclu(e).")

async def setup(bot: commands.Bot):
    await bot.add_cog(Modération(bot))
