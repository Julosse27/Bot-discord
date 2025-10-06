import discord
from discord.ext import commands
from Stocks.Commands_stock import check_me


class Modération(commands.Cog):
    def slashs_commands(self):
        @self.app_command.command(name= "re_test")
        async def test_slash(interaction: discord.Interaction):
            await interaction.response.send_message(content= "test")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Cog spécialisé dans les commandes de moderations."
        self.slashs_commands()

    @commands.command(name= "message", aliases= ["mes", "ping"], description= "Envois un message à qui tu veut.", brief= "Envois un mp.")
    @check_me(1417199810099937411, 1382302424366186516, 1382303940921659412, 1382455975549599854)
    async def message(self, ctx, member: discord.Member, *, contenu: str):
        await member.send(content= contenu)
        await ctx.send(content = 'Message envoyé !')

    @

    @commands.command(name= "kick", aliases= ["k"], description= "Kick la personne que t'aime pas de ce serveur.", brief= "Kick quelqu'un.")
    @check_me(1382302424366186516)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason= reason)
        await ctx.send(f"{member.name} a bien été exclu(e).")

async def setup(bot: commands.Bot):
    await bot.add_cog(Modération(bot))
