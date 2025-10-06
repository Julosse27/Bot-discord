import discord
from discord.ext import commands
from Stocks.Exo_stock import exos
from Stocks.Commands_stock import check_basic_command

class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label= "Exo sur les types de valeurs",
                value= "0"
            ),
            discord.SelectOption(
                label= "Exo sur le transtypage et les instructions conditionelles",
                value= "1"
            )
        ]

        super().__init__(placeholder="Quel exo voulez vous ?", min_values= 1, max_values= 1, options= options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view= exos[int(self.values[0])]())
        
            

class Menu_view(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())


class Tutos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Tout les tutos doivents bien venir de quelque part non ?"

    @commands.command(name = "exos_select", aliases = ["exos", "exo"], description = "Une commande qui permet de s'exercer aux diferents tutos.", brief = "Fait spawn un exo.")
    @check_basic_command(1417199810099937411)
    async def monExo(self, ctx: commands.Context):
        message = await ctx.send(view= Menu_view())

async def setup(bot: commands.Bot):    
    await bot.add_cog(Tutos(bot))
