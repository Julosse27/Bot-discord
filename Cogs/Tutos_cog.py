import discord
from discord.ext import commands
from Exos.Exos_stock import Tuto_1

class Menu(discord.ui.Select):  
    def __init__(self):
        options = [
            discord.SelectOption(
                label= "Exo sur les types de valeurs",
                value= "Exo 1"
            ),
            discord.SelectOption(
                label= "Exo sur le transtypage et les boucles",
                value= "Exo 2"
            )
        ]

        super().__init__(placeholder="Quel exo voulez vous ?", min_values= 1, max_values= 1, options= options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Exo 1":
            await interaction.user.send(Tuto_1())

class Menu_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

class TutosCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name = "Exos_select", aliases = ["Exos", "Exo"], description = "Une commande qui permet de s'exercer aux diferents tutos.", brief = "Fait spawn un exo.")
    async def monTuto(self, ctx):
        await ctx.send(view= Menu_view())

async def setup(bot: commands.Bot):
    await bot.add_cog(TutosCog(bot))